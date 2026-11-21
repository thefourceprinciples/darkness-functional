import argparse
import csv
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("Error: pyserial is required. Install it with: pip install pyserial")
    sys.exit(1)

CSV_COLUMNS = [
    "Time_ms",
    "Target_deg",
    "r_coh",
    "N_noise",
    "FC_drift",
    "D_load",
    "S_persist",
    "Cascade_Gamma",
    "Gate_State",
    "k_restore",
]


def auto_detect_esp32_port() -> str | None:
    """Scan available USB serial ports for common ESP32-S3 UART bridges."""
    ports = list(list_ports.comports())
    for p in ports:
        desc = (p.description or "").lower()
        hwid = (p.hwid or "").lower()
        if any(tag in desc or tag in hwid for tag in ["cp210", "ch340", "ch343", "usb serial", "jtag", "esp32", "303a"]):
            return p.device
    return ports.__getitem__(0).device if ports else None


class LiveTelemetryDashboard:
    """Real-time 3-panel telemetry monitor and CSV logger for CUC-Array v1."""

    def __init__(self, port: str, baud: int = 115200, window_size: int = 300):
        self.port = port
        self.baud = baud
        self.window_size = window_size

        self.ser = serial.Serial(port, baud, timeout=0.05)
        time.sleep(0.5)
        self.ser.reset_input_buffer()

        self.t_buf = deque(maxlen=window_size)
        self.r_buf = deque(maxlen=window_size)
        self.s_buf = deque(maxlen=window_size)
        self.d_buf = deque(maxlen=window_size)
        self.k_buf = deque(maxlen=window_size)
        self.gamma_buf = deque(maxlen=window_size)
        self.gate_buf = deque(maxlen=window_size)

        self.full_records: list[list[float]] = []
        self.t0_ms: float | None = None

        root_dir = Path(__file__).resolve().parent.parent
        self.fig_dir = root_dir / "figures"
        self.log_dir = root_dir / "hardware" / "logs"
        self.fig_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._init_plot()

    def _init_plot(self) -> None:
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        self.fig.canvas.manager.set_window_title(f"CUC-Array v1 Live Telemetry ({self.port})")

        self.line_r, = self.ax1.plot([], [], "--", color="teal", linewidth=1.8, label="Coherence r(t)")
        self.line_s, = self.ax1.plot([], [], "-", color="navy", linewidth=2.2, label="Persistence S(t)")
        self.ax1.set_ylim(-0.05, 1.15)
        self.ax1.set_ylabel("Normalized Score")
        self.ax1.set_title("CUC-Array v1: Live Acoustic Standing-Wave Stability & Cascade Gate")
        self.ax1.legend(loc="upper right", fontsize=8)
        self.ax1.grid(alpha=0.3)

        self.line_d, = self.ax2.plot([], [], "-", color="crimson", linewidth=2.0, label="Darkness Load D[Σ, t]")
        self.line_k, = self.ax2.plot([], [], "-", color="forestgreen", linewidth=2.0, label="Restoration Gain k_restore")
        self.ax2.axhline(0.35, color="gray", linestyle=":", linewidth=1.0, label="Nominal D Threshold")
        self.ax2.set_ylim(-0.05, 1.5)
        self.ax2.set_ylabel("Load / Gain")
        self.ax2.legend(loc="upper right", fontsize=8)
        self.ax2.grid(alpha=0.3)

        self.line_gamma, = self.ax3.plot([], [], "-", color="darkorange", linewidth=2.0, label="Cascade Ratio Γ(t)")
        self.line_gate, = self.ax3.step([], [], where="post", color="purple", linewidth=1.6, label="Gate State (0/1/2)")
        self.ax3.axhline(1.8, color="gold", linestyle="--", linewidth=1.0, label="Warn")
        self.ax3.axhline(3.0, color="red", linestyle="--", linewidth=1.0, label="Trip")
        self.ax3.set_ylim(-0.2, 4.5)
        self.ax3.set_ylabel("Cascade / Gate")
        self.ax3.set_xlabel("Elapsed Time (seconds)")
        self.ax3.legend(loc="upper right", fontsize=8, ncol=2)
        self.ax3.grid(alpha=0.3)

        self.status_text = self.fig.text(
            0.015, 0.01, "Waiting for ESP32-S3 telemetry stream...", fontsize=9, family="monospace"
        )
        plt.tight_layout(rect=[0, 0.03, 1, 1])

    def _poll_serial(self) -> None:
        while self.ser.in_waiting > 0:
            try:
                raw_line = self.ser.readline().decode("utf-8", errors="ignore").strip()
            except serial.SerialException:
                return

            if not raw_line or raw_line.startswith("#") or raw_line.startswith("=") or raw_line.startswith("CUC") or raw_line.startswith("Time_ms"):
                continue

            parts = [p.strip() for p in raw_line.split(",")]
            if len(parts) != 10:
                continue

            try:
                t_ms, _tgt, r_v, _n_v, _fc_v, d_v, s_v, gam_v, gate_v, k_v = [float(x) for x in parts]
            except ValueError:
                continue

            if self.t0_ms is None:
                self.t0_ms = t_ms

            t_sec = (t_ms - self.t0_ms) / 1000.0
            self.t_buf.append(t_sec)
            self.r_buf.append(r_v)
            self.d_buf.append(d_v)
            self.s_buf.append(s_v)
            self.gamma_buf.append(gam_v)
            self.gate_buf.append(gate_v)
            self.k_buf.append(k_v)

            self.full_records.append([t_ms, _tgt, r_v, _n_v, _fc_v, d_v, s_v, gam_v, gate_v, k_v])

    def update_frame(self, _frame: int):
        self._poll_serial()
        if len(self.t_buf) < 2:
            return (
                self.line_r, self.line_s, self.line_d,
                self.line_k, self.line_gamma, self.line_gate
            )

        t_arr = np.array(self.t_buf)
        self.line_r.set_data(t_arr, np.array(self.r_buf))
        self.line_s.set_data(t_arr, np.array(self.s_buf))
        self.line_d.set_data(t_arr, np.array(self.d_buf))
        self.line_k.set_data(t_arr, np.array(self.k_buf))
        self.line_gamma.set_data(t_arr, np.array(self.gamma_buf))
        self.line_gate.set_data(t_arr, np.array(self.gate_buf))

        x_min = max(0.0, t_arr[-1] - 10.0)
        x_max = max(10.0, t_arr[-1] + 0.2)
        for ax in (self.ax1, self.ax2, self.ax3):
            ax.set_xlim(x_min, x_max)

        max_g = max(4.5, float(np.max(self.gamma_buf)) * 1.15)
        self.ax3.set_ylim(-0.2, max_g)

        gate_names = {0: "0: LAMINAR", 1: "1: TRANSITIONAL", 2: "2: TURBULENT_TRIP"}
        cur_gate = int(self.gate_buf[-1])
        self.status_text.set_text(
            f"Port: {self.port} | Samples: {len(self.full_records)} | "
            f"r={self.r_buf[-1]:.2f} | D={self.d_buf[-1]:.2f} | S={self.s_buf[-1]:.2f} | "
            f"Gate={gate_names.get(cur_gate, str(cur_gate))} | k_restore={self.k_buf[-1]:.2f}"
        )

        return (
            self.line_r, self.line_s, self.line_d,
            self.line_k, self.line_gamma, self.line_gate
        )

    def save_session_artifacts(self) -> None:
        if not self.full_records:
            print("No telemetry samples captured; skipping export.")
            return

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = self.log_dir / f"cuc_array_run_{stamp}.csv"
        png_path = self.fig_dir / "cuc_array_live_run.png"

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerows(self.full_records)

        self.fig.savefig(png_path, dpi=150)
        print(f"\nSaved raw telemetry CSV -> {csv_path}")
        print(f"Saved diagnostic figure -> {png_path}")

    def run(self) -> None:
        print(f"Connected to ESP32-S3 on {self.port} @ {self.baud} baud.")
        print("Close the plot window (or press Ctrl+C) to save CSV + PNG artifacts.")
        _ani = animation.FuncAnimation(self.fig, self.update_frame, interval=30, blit=False, cache_frame_data=False)
        try:
            plt.show()
        except KeyboardInterrupt:
            pass
        finally:
            self.ser.close()
            self.save_session_artifacts()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Telemetry Dashboard for CUC-Array v1")
    parser.add_argument("--port", type=str, default=None, help="Serial port (e.g., COM3 or /dev/ttyACM0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    args = parser.parse_args()

    target_port = args.port or auto_detect_esp32_port()
    if not target_port:
        print("No USB serial port detected. Plug in your ESP32-S3 and pass --port COMx.")
        sys.exit(1)

    dashboard = LiveTelemetryDashboard(port=target_port, baud=args.baud)
    dashboard.run()
