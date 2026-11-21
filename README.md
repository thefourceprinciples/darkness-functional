# Darkness Functional

![CI Status](https://github.com)
[![License: MIT](https://shields.io)](LICENSE)

A quantitative diagnostic framework and closed-loop stabilization suite for modeling coherence failure, interface mismatch, and persistence collapse under constraint.

**Author:** Gage Fry (Rockford, Illinois)  
**Project Lineage:** The Fource Principles / Coherence Under Constraint (CUC)  
**Status:** v0.2.0 — Simulation Benchmarks, Automated CI, AI Memory Case Study & CUC-Array v1 Hardware Blueprint  

---

## Overview

Complex dynamical networks, agentic AI memory stores, and physical sensor-actuator arrays rarely fail instantaneously. Instead, they suffer from **silent coherence collapse** driven by phase drift, stochastic noise, boundary degradation, and inter-subsystem contradiction.

Within the **Coherence Under Constraint (CUC)** framework, darkness is not treated as a moral category, mystical substance, or new physical force. It is modeled as a quantitative **coherence-loss load** (\(D[\Sigma, t]\)) that exponentially penalizes usable system persistence (S(t))—paired with an active restoration controller (\(k_{\text{restore}}\)) that stabilizes systems before macroscopic failure occurs.

---

## Mathematical Scaffold

### 1. The Darkness Functional
\[D[\Sigma, t] = \alpha\bigl(1 - r(t)\bigr) + \beta N(t) + \gamma F_C(t) + \delta M_I(t)\]

* **1 - r(t):** Global phase or semantic synchronization loss (r ∈).
* **N(t):** Stochastic noise, turbulent velocity variance, or retrieval distractor load.
* **\(F_C(t)\):** Constraint failure or boundary drift outside admissible operating limits.
* **\(M_I(t)\):** Subsystem interface mismatch (local-vs-global divergence or cross-document contradiction).

### 2. Darkness-Aware Persistence & Hysteresis
\[S(t) = r(t) \cdot C(\Omega, t) \cdot \Phi(t) \cdot \exp\bigl(-D[\Sigma, t]\bigr), \qquad \mathcal{H}_D(t) = \int_0^t D[\Sigma, \tau]\,d\tau\]

---

## Repository Structure

```text
darkness-functional/
├── .github/workflows/
│   └── test.yml                            # Automated pytest & figure generation CI
├── src/
│   ├── darkness_simulation_package.py      # Multi-group Kuramoto network & D[Σ, t] diagnostics
│   ├── restoration_sweep.py                # Ensemble restoration coupling (k_restore) sweep
│   ├── ai_memory_darkness.py               # AI agent memory contradiction & throughput benchmark
│   └── lens_array_bridge.py                # Spatial potential / acoustic array critical spacing model
├── hardware/
│   ├── README.md                           # CUC-Array v1 BOM, wiring guide & bring-up instructions
│   ├── bracket.scad                        # 3D-printable 34.3 mm resonant C-bracket (OpenSCAD)
│   ├── live_telemetry_plot.py              # Real-time 3-panel USB Serial oscilloscope & CSV logger
│   └── firmware/
│       └── darkness_levitator_esp32s3.ino  # Auto-calibrated 40 kHz ESP32-S3 phase-restoration firmware
├── tests/
│   └── test_darkness_functional.py         # Automated mathematical invariant & prediction tests
├── paper/
│   ├── darkness_functional.md              # Markdown manuscript
│   └── darkness_functional.tex             # LaTeX preprint manuscript
├── dssp/                                   # Dark-Sector Stewardship Project (DSSP Master Packet v1.0)
├── docs/                                   # Glossary & conceptual notes
├── figures/                                # Diagnostic output plots
├── CITATION.cff
├── LICENSE
├── VERSION.md
└── requirements.txt
```

---

## Quickstart

```bash
pip install -r requirements.txt
pytest -v

# Run core simulation benchmarks
python src/darkness_simulation_package.py
python src/restoration_sweep.py
python src/ai_memory_darkness.py
python src/lens_array_bridge.py

# Launch live CUC-Array v1 hardware telemetry dashboard (requires ESP32-S3 connected via USB)
python hardware/live_telemetry_plot.py
```

---

## Citation

```bibtex
@misc{fry2026darkness,
  author       = {Fry, Gage},
  title        = {Darkness Functional: A Diagnostic Framework for Coherence Loss Under Constraint},
  year         = {2026},
  publisher    = {GitHub},
  howpublished \(= {\url{https://github.com/thefourceprinciples/darkness-functional}} \)}
```

