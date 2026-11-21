import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT_DIR / "hardware" / "logs"
FIG_DIR = ROOT_DIR / "figures"


def load_telemetry_csv(csv_path: Path) -> dict[str, np.ndarray]:
    """Parse a 10-column CUC-Array v1 CSV log into named NumPy arrays."""
    cols = {
        "Time_ms": [],
        "Target_deg": [],
        "r_coh": [],
        "N_noise": [],
        "FC_drift": [],
        "D_load": [],
        "S_persist": [],
        "Cascade_Gamma": [],
        "Gate_State": [],
        "k_restore": [],
    }
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                for k in cols:
                    cols[k].append(float(row[k]))
            except (KeyError, ValueError, TypeError):
                continue

    if not cols["Time_ms"]:
        raise ValueError(f"No valid telemetry rows found in {csv_path}")

    arrays = {k: np.array(v, dtype=float) for k, v in cols.items()}
    arrays["t_sec"] = (arrays["Time_ms"] - arrays["Time_ms"].item(0)) / 1000.0
    return arrays


def generate_synthetic_bench_run(seed: int = 7) -> dict[str, np.ndarray]:
    """
    Generate a realistic synthetic 25-second bench run (calm baseline -> benign acoustic
    room noise -> cross-flow turbulence gust -> closed-loop recovery) for offline testing.
    """
    rng = np.random.default_rng(seed)
    dt = 0.01
    t = np.arange(0.0, 25.0, dt)
    n = len(t)

    r = np.clip(0.97 + rng.normal(0.0, 0.01, n), 0.0, 1.0)
    noise = np.clip(0.05 + rng.normal(0.0, 0.012, n), 0.0, 2.0)
    fc = np.clip(0.005 + rng.normal(0.0, 0.002, n), 0.0, 1.0)
    gamma = np.clip(1.02 + rng.normal(0.0, 0.08, n), 0.5, 6.0)

    # Benign room speech/clap window (t in [6, 8]s): minor acoustic ripple, NOT trap collapse
    benign_mask = (t >= 6.0) & (t <= 8.0)
    noise[benign_mask] += 0.07 + rng.normal(0.0, 0.015, np.sum(benign_mask))
    gamma[benign_mask] += 0.45

    # Active cross-flow air gust window (t in [12, 16]s): genuine standing-wave perturbation
    gust_mask = (t >= 12.0) & (t <= 16.0)
    gust_profile = np.sin(np.pi * (t[gust_mask] - 12.0) / 4.0)
    r[gust_mask] -= 0.24 * gust_profile
    noise[gust_mask] += 0.32 * gust_profile
    fc[gust_mask] += 0.14 * gust_profile
    gamma[gust_mask] += 2.60 * gust_profile

    D = 1.0 * (1.0 - r) + 0.8 * noise + 0.7 * fc
    S = r * np.exp(-D)

    gate = np.zeros(n, dtype=float)
    k_rest = np.zeros(n, dtype=float)
    for i in range(n):
        if D.item(i) > 0.35 or gamma.item(i) >= 3.0:
            gate[i] = 2.0
            k_rest[i] = min(0.85, max(0.25, (D.item(i) - 0.35) * 1.5))
        elif gamma.item(i) >= 1.8:
            gate[i] = 1.0

    return {
        "Time_ms": t * 1000.0,
        "t_sec": t,
        "Target_deg": np.zeros(n),
        "r_coh": r,
        "N_noise": noise,
        "FC_drift": fc,
        "D_load": D,
        "S_persist": S,
        "Cascade_Gamma": gamma,
        "Gate_State": gate,
        "k_restore": k_rest,
    }


def evaluate_dssp_gates(
    data: dict[str, np.ndarray],
    calm_window: tuple[float, float] = (0.5, 5.0),
    benign_window: tuple[float, float] = (6.0, 8.0),
    gust_window: tuple[float, float] = (12.0, 16.0),
    recovery_window: tuple[float, float] = (17.5, 22.0),
) -> dict[str, object]:
    """
    Execute DSSP Master Packet v1.0 residual, false-positive, and hysteresis checks:
      1. Residual-First Baseline: subtract ambient sensor floor before scoring anomalies.
      2. False-Darkness Defense: verify benign room noise triggers < 5% false k_restore trips.
      3. Active Detection & Recovery: verify D_load trips during gust and S_persist rebounds.
      4. Historical Hysteresis: verify cumulative load H_D = integral(D dt) increases monotonically.
    """
    t = data["t_sec"]
    D = data["D_load"]
    S = data["S_persist"]
    k_rest = data["k_restore"]
    gate = data["Gate_State"]

    dt_arr = np.diff(t, prepend=t.item(0))
    if len(dt_arr) > 1:
        dt_arr[0] = dt_arr.item(1)
    h_cum = np.cumsum(D * dt_arr)

    c0, c1 = calm_window
    b0, b1 = benign_window
    g0, g1 = gust_window
    r0, r1 = recovery_window

    calm_mask = (t >= c0) & (t <= c1)
    benign_mask = (t >= b0) & (t <= b1)
    gust_mask = (t >= g0) & (t <= g1)
    recov_mask = (t >= r0) & (t <= r1)

    d_floor = float(np.mean(D[calm_mask])) if np.any(calm_mask) else float(np.percentile(D, 15))
    d_residual = np.maximum(0.0, D - d_floor)

    # Gate 1: False-Positive Rate during benign acoustic disturbance
    if np.any(benign_mask):
        false_trip_rate = float(np.mean(k_rest[benign_mask] > 0.0))
    else:
        false_trip_rate = float(np.mean(k_rest[calm_mask] > 0.0)) if np.any(calm_mask) else 0.0

    # Gate 2: True-Positive Detection during active turbulence gust
    if np.any(gust_mask):
        gust_detection_rate = float(np.mean(gate[gust_mask] >= 1.0))
        peak_residual_d = float(np.max(d_residual[gust_mask]))
        mean_k_engage = float(np.mean(k_rest[gust_mask]))
    else:
        gust_detection_rate = float(np.mean(gate >= 1.0))
        peak_residual_d = float(np.max(d_residual))
        mean_k_engage = float(np.mean(k_rest))

    # Gate 3: Post-Gust Persistence Recovery
    s_baseline = float(np.mean(S[calm_mask])) if np.any(calm_mask) else float(np.percentile(S, 85))
    s_recovered = float(np.mean(S[recov_mask])) if np.any(recov_mask) else float(np.mean(S[-50:]))
    recovery_ratio = s_recovered / max(s_baseline, 1e-6)

    # Gate 4: Monotonic Cumulative Darkness Hysteresis
    h_monotonic = bool(np.all(np.diff(h_cum) >= -1e-9)) and float(h_cum[-1]) > 0.0

    report = {
        "dssp_version": "DSSP Master Packet v1.0",
        "samples_analyzed": int(len(t)),
        "duration_sec": round(float(t[-1] - t.item(0)), 2),
        "ambient_darkness_floor": round(d_floor, 4),
        "peak_residual_darkness": round(peak_residual_d, 4),
        "false_positive_trip_rate": round(false_trip_rate, 4),
        "gust_detection_rate": round(gust_detection_rate, 4),
        "mean_restoration_gain_in_gust": round(mean_k_engage, 4),
        "persistence_recovery_ratio": round(recovery_ratio, 4),
        "cumulative_historical_load": round(float(h_cum[-1]), 3),
        "gates_passed": {
            "G1_residual_floor_isolated": d_floor < 0.20,
            "G2_false_darkness_defense_lt_5pct": false_trip_rate < 0.05,
            "G3_turbulence_cascade_detected_gt_70pct": gust_detection_rate >= 0.70,
            "G4_persistence_recovered_gt_90pct": recovery_ratio >= 0.90,
            "G5_historical_hysteresis_monotonic": h_monotonic,
        },
        "d_residual_series": d_residual,
        "h_cum_series": h_cum,
    }
    return report


def save_dssp_audit_figure(
    data: dict[str, np.ndarray],
    report: dict[str, object],
    out_path: Path,
) -> None:
    """Generate a 4-panel publication-grade DSSP validation figure."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t = data["t_sec"]
    d_res = report["d_residual_series"]
    h_cum = report["h_cum_series"]

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    ax1.plot(t, data["r_coh"], "--", color="teal", linewidth=1.6, label="Coherence r(t)")
    ax1.plot(t, data["S_persist"], "-", color="navy", linewidth=2.2, label="Persistence S(t)")
    ax1.set_ylabel("Stability")
    ax1.set_title("CUC-Array v1 Hardware Audit (DSSP Master Packet v1.0 Qualification)")
    ax1.legend(loc="lower right", fontsize=8)
    ax1.grid(alpha=0.3)

    ax2.plot(t, data["D_load"], color="gray", alpha=0.6, linewidth=1.4, label="Raw Darkness D[Σ, t]")
    ax2.plot(t, d_res, color="crimson", linewidth=2.0, label="Residual Darkness D_res(t) = max(0, D - D_floor)")
    ax2.set_ylabel("Residual D")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.grid(alpha=0.3)

    ax3.plot(t, data["Cascade_Gamma"], color="darkorange", linewidth=1.8, label="Navier-Stokes Cascade Γ(t)")
    ax3.plot(t, data["k_restore"], color="forestgreen", linewidth=2.0, label="Restoration Gain k_restore(t)")
    ax3.set_ylabel("Cascade / Gain")
    ax3.legend(loc="upper right", fontsize=8)
    ax3.grid(alpha=0.3)

    ax4.plot(t, h_cum, color="purple", linewidth=2.2, label="Cumulative Historical Load ∫D dt")
    ax4.set_xlabel("Elapsed Time (seconds)")
    ax4.set_ylabel("Hysteresis ∫D dt")
    ax4.legend(loc="upper left", fontsize=8)
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="DSSP Residual & False-Positive Audit for CUC-Array v1 Logs")
    parser.add_argument("--csv", type=str, default=None, help="Path to a recorded CUC-Array v1 CSV log")
    parser.add_argument("--demo", action="store_true", help="Run on synthetic bench run if no CSV exists yet")
    args = parser.parse_args()

    if args.csv:
        csv_path = Path(args.csv)
        data = load_telemetry_csv(csv_path)
        source_label = str(csv_path)
    elif args.demo or not LOG_DIR.exists() or not list(LOG_DIR.glob("*.csv")):
        data = generate_synthetic_bench_run()
        source_label = "Synthetic Bench Validation Run (--demo)"
    else:
        latest_csv = sorted(LOG_DIR.glob("*.csv"))[-1]
        data = load_telemetry_csv(latest_csv)
        source_label = str(latest_csv)

    report = evaluate_dssp_gates(data)
    fig_out = FIG_DIR / "cuc_array_dssp_audit.png"
    save_dssp_audit_figure(data, report, fig_out)

    summary = {k: v for k, v in report.items() if not isinstance(v, np.ndarray)}
    summary["source"] = source_label
    summary["audit_figure"] = str(fig_out)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
