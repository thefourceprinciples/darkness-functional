# Darkness Functional

**A falsifiable degradation and constraint-strain diagnostic for the Coherence Under Constraint (`CUC v0.2`) research program.**

[![Status: Verified E2 Core](https://shields.io)](src/darkness_core.py)
[![Garden Identity: G01-T006](https://shields.io)](https://github.com)
[![License: AGPL-3.0](https://shields.io)](LICENSE)

**Author:** Gage Fry  
**Lineage:** The Fource Principles / Framework Garden  
**Canonical Garden identity:** G01-T006  
**Parent trunk:** [`coherence-under-constraint`](https://github.com) (`G01-T003`, v0.2.0-draft.1)

---

## What the Darkness Functional is

In **Coherence Under Constraint (CUC)**, high coherence alone does not guarantee persistence—systems fail through noise accumulation, boundary erosion, and cross-module interface mismatch.

The **Darkness Functional** D(t) ≥ 0 (`DAR-1`, `DAR-2`) is a nonnegative operational diagnostic that quantifies modeled degradation and attributes strain across four independent channels:

```text
D(t) = α(1 - r_G(t)) + β·noise(t) + γ·boundary_failure(t) + δ·interface_mismatch(t) ≥ 0
```

with exponential persistence attenuation (`DAR-4`):

```text
a_D(t) = exp(-D(t)) ∈ (0, 1]
```

and reduced persistence-support propensity (`CUC-31`):

```text
Q_CUC(t) = K · r_G(t) · χ_M(t) · ψ_J(t) · exp(-D(t)) / (1 + λ_bad(t))
```

## What it is not

- **Not a mystical or cosmological entity:** "Darkness" in CUC is strictly a mathematical measure of organization-degrading loss, noise, and boundary mismatch.
- **Not a standalone replacement for domain physics:** Calibration weights (α, β, γ, δ ≥ 0) must be anchored to observable failure modes in each target domain.

## Quick start

Zero external dependencies (Python 3.11+ standard library only):

```bash
python -m pytest -v tests/test_darkness_core.py
python src/darkness_core.py
```

### Example Python usage

```python
from src.darkness_core import evaluate_darkness, propensity_with_darkness

report = evaluate_darkness(
    coherence_r=0.82,
    noise_level=0.14,
    boundary_failure=0.08,
    interface_mismatch=0.35,
)

print(report.darkness_d)          # 0.1875
print(report.attenuation_factor)  # 0.829029
print(report.dominant_driver)     # 'interface_mismatch'
print(report.severity_band)       # 'NOMINAL // BOUNDED DRIFT'

q_cuc = propensity_with_darkness(
    capacity_k=1.0,
    coherence_r=0.82,
    constraint_fitness_chi=0.88,
    throughput_adequacy_psi=0.95,
    darkness_d=report.darkness_d,
)
```

## Repository structure

```text
.
├── README.md
├── LICENSE
├── src/
│   └── darkness_core.py
├── tests/
│   └── test_darkness_core.py
└── .github/
    └── workflows/
        └── ci.yml
```

## License

Code and repository documentation are released under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE).
