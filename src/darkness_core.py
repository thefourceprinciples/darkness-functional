#!/usr/bin/env python3
"""Canonical Darkness Functional (G01-T006) — CUC v0.2 Diagnostic Engine.

Implements equations [DAR-1, DAR-2, DAR-3, DAR-4] and [CUC-31] from the
Coherence Under Constraint (CUC) v0.2.0-draft.1 Charter:
  - Nonnegative composite degradation D(t) >= 0
  - Component attribution (coherence loss, noise, boundary failure, interface mismatch)
  - Exponential persistence attenuation a_D(t) = exp(-D(t)) in (0, 1]
  - Dominant failure-mode diagnosis
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True, slots=True)
class DarknessWeights:
    """Nonnegative calibration weights for composite Darkness [DAR-2]."""

    alpha_coherence: float = 0.25
    beta_noise: float = 0.25
    gamma_boundary: float = 0.25
    delta_interface: float = 0.25

    def validate(self) -> None:
        if (
            self.alpha_coherence < 0.0
            or self.beta_noise < 0.0
            or self.gamma_boundary < 0.0
            or self.delta_interface < 0.0
        ):
            raise ValueError("All Darkness calibration weights must be nonnegative [DAR-2].")


@dataclass(frozen=True, slots=True)
class DarknessReport:
    """Structured diagnostic output for a single system state."""

    darkness_d: float
    attenuation_factor: float
    contributions: Dict[str, float]
    dominant_driver: str
    severity_band: str


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def classify_darkness_severity(d_val: float) -> str:
    """Map nonnegative D(t) to an operational regime."""
    if d_val <= 0.10:
        return "CLEAR // LOW DISSIPATION"
    if d_val <= 0.25:
        return "NOMINAL // BOUNDED DRIFT"
    if d_val <= 0.50:
        return "ELEVATED // INTERFACE OR BOUNDARY STRAIN"
    return "CRITICAL // HIGH DEGRADATION"


def evaluate_darkness(
    coherence_r: float,
    noise_level: float,
    boundary_failure: float,
    interface_mismatch: float,
    weights: DarknessWeights = DarknessWeights(),
) -> DarknessReport:
    """Evaluate composite Darkness D(t) >= 0 and attribute degradation sources.

    Implements [DAR-1, DAR-2, DAR-4].
    """
    weights.validate()

    c_loss = _clamp01(1.0 - coherence_r)
    n_load = max(0.0, noise_level)
    b_fail = max(0.0, boundary_failure)
    i_mis = max(0.0, interface_mismatch)

    terms: Dict[str, float] = {
        "coherence_loss": weights.alpha_coherence * c_loss,
        "noise_load": weights.beta_noise * n_load,
        "boundary_failure": weights.gamma_boundary * b_fail,
        "interface_mismatch": weights.delta_interface * i_mis,
    }

    d_total = max(0.0, sum(terms.values()))
    attenuation = math.exp(-d_total)

    if d_total == 0.0:
        dominant = "none"
    else:
        dominant = max(terms.items(), key=lambda item: item[1])[0]

    return DarknessReport(
        darkness_d=round(d_total, 6),
        attenuation_factor=round(attenuation, 6),
        contributions={k: round(v, 6) for k, v in terms.items()},
        dominant_driver=dominant,
        severity_band=classify_darkness_severity(d_total),
    )


def propensity_with_darkness(
    capacity_k: float,
    coherence_r: float,
    constraint_fitness_chi: float,
    throughput_adequacy_psi: float,
    darkness_d: float,
    bad_loss_lambda: float = 0.0,
) -> float:
    """Compute reduced persistence-support propensity Q_CUC [CUC-31]."""
    atten = math.exp(-max(0.0, darkness_d))
    denom = 1.0 + max(0.0, bad_loss_lambda)
    return (
        max(0.0, capacity_k)
        * _clamp01(coherence_r)
        * _clamp01(constraint_fitness_chi)
        * _clamp01(throughput_adequacy_psi)
        * (atten / denom)
    )


if __name__ == "__main__":
    sample = evaluate_darkness(
        coherence_r=0.82,
        noise_level=0.14,
        boundary_failure=0.08,
        interface_mismatch=0.35,
    )
    print(f"D(t)={sample.darkness_d:.4f} | exp(-D)={sample.attenuation_factor:.4f}")
    print(f"Dominant Driver: {sample.dominant_driver} | Regime: {sample.severity_band}")
