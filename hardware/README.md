# CUC-Array v1: Closed-Loop Acoustic Phased-Array Testbed

**CUC-Array v1** (codenamed *The Coherence Trap*) is a low-cost (~$35–$45), open-source 40 kHz ultrasonic levitation testbed built to validate the **Darkness Functional (D[Σ, t])** and **Persistence Score (S(t))** on physical acoustic wave dynamics.

Rather than relying on open-loop standing waves that drop suspended samples when perturbed, CUC-Array v1 uses an **ESP32-S3 microcontroller** and an **electret microphone feedback loop** to measure acoustic coherence (r), turbulent streaming noise (N), and phase drift (F_C) at 100 Hz—triggering automated phase restoration (k_restore) to stabilize floating particles under external air currents.

---

## 1. Bill of Materials (BOM)

| Component | Specification | Qty | Est. Cost | Role |
| :--- | :--- | :---: | :---: | :--- |
| **Microcontroller** | ESP32-S3 DevKitC-1 (Dual-core, hardware LEDC PWM) | 1 | $8 | Runs 40 kHz phase-shifted PWM timers and 100 Hz D[Σ, t] control loop |
| **Ultrasonic Emitters** | `TCT40-16T` 40 kHz Transmitters (16 mm diameter — *must be `T` type*) | 10 | $10 | Top (5×) and Bottom (5×) phased emitter arrays |
| **H-Bridge Driver** | `L293D` DIP-16 Dual H-Bridge IC | 1 | $2 | Boosts 3.3V logic PWM to 24V peak-to-peak differential drive |
| **Buck Converter** | DC-DC Synchronous Buck Module (`12V` → `5V 1A`, LM7805 footprint) | 1 | $4 | Steps 12V main supply down to clean 5V for ESP32-S3 and L293D logic |
| **Acoustic Sensor** | `GY-MAX4466` Electret Microphone Amplifier | 1 | $4 | Measures standing-wave lock (r) and turbulent air noise (N) |
| **Power Supply** | `12V DC 2A` Wall Adapter + `5.5×2.1 mm` Screw-Terminal Barrel Jack | 1 | $7 | Main power input for transducer drivers and buck regulator |
| **Prototyping** | 830-Tie-Point Solderless Breadboard + Dupont Jumper Wires | 1 | $10 | Solderless circuit assembly |
| **Test Media** | 2 mm – 3 mm Expanded Polystyrene (EPS) Foam Beads | 1 bag | $3 | Low-density test particles suspended in standing-wave nodes |

---

## 2. Pin-by-Pin Wiring Guide

### Power Distribution
* **12V Barrel Jack `+`** → Breadboard `+12V` Rail → **L293D Pin 8 (`VCC2`)** & **Buck Converter `VIN+`**
* **12V Barrel Jack `-`** → Breadboard `GND` Rail → **L293D Pins 4, 5, 12, 13**, **Buck Converter `GND`**, & **ESP32-S3 `GND`**
* **Buck Converter `5V OUT+`** → Breadboard `+5V` Rail → **ESP32-S3 `5V/VIN`**, **L293D Pin 1 (`1,2EN`)**, **L293D Pin 9 (`3,4EN`)**, & **L293D Pin 16 (`VCC1`)**

### Signal & Sensor Connections
* **Top Transducer Bank (5× `TCT40-16T` wired in parallel, observing `+` polarity):**
  * `ESP32-S3 GPIO 4` → **L293D Pin 2 (`1A`)**
  * `ESP32-S3 GPIO 5` → **L293D Pin 7 (`2A`)** *(180° inverted complementary wave)*
  * **L293D Pin 3 (`1Y`)** & **Pin 6 (`2Y`)** → Top Transducer Bank `+` and `-` leads
* **Bottom Transducer Bank (5× `TCT40-16T` wired in parallel, observing `+` polarity):**
  * `ESP32-S3 GPIO 6` → **L293D Pin 10 (`3A`)**
  * `ESP32-S3 GPIO 7` → **L293D Pin 15 (`4A`)** *(180° inverted complementary wave)*
  * **L293D Pin 11 (`3Y`)** & **Pin 14 (`4Y`)** → Bottom Transducer Bank `+` and `-` leads
* **MAX4466 Microphone Module (mounted on C-bracket spine facing the 34.3 mm gap):**
  * `VCC` → **ESP32-S3 `3.3V`** | `GND` → **ESP32-S3 `GND`** | `OUT` → **ESP32-S3 `GPIO 1`**
* **Optional 10 kΩ Manual Phase-Sliding Potentiometer:**
  * Outer pins → **ESP32-S3 `3.3V`** and **`GND`** | Center wiper → **ESP32-S3 `GPIO 2`** | Tie **ESP32-S3 `GPIO 3`** to **`3.3V`** to enable knob steering.

---

## 3. Running Telemetry & Calibration

1. Flash `hardware/firmware/darkness_levitator_esp32s3.ino` via Arduino IDE 2.x (`ESP32 Board Package v3.0+`, Board: `ESP32S3 Dev Module`).
2. Hold the cavity steady for 2 seconds on boot (or send `C` over Serial) for automatic room baseline calibration.
3. Run the live Python telemetry dashboard:
   ```bash
   python hardware/live_telemetry_plot.py
   ```
