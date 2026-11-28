#!/usr/bin/env python3
"""Automated verification tests for src/darkness_core.py (G01-T006)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.darkness_core import (
    DarknessWeights,
    evaluate_darkness,
    propensity_with_darkness,
)


def test_zero_degradation_equilibrium() -> None:
    report = evaluate_darkness(
        coherence_r=1.0,
        noise_level=0.0,
        boundary_failure=0.0,
        interface_mismatch=0.0,
    )
    assert math.isclose(report.darkness_d, 0.0, abs_tol=1e-12)
    assert math.isclose(report.attenuation_factor, 1.0, abs_tol=1e-12)
    assert report.dominant_driver == "none"
    assert report.severity_band.startswith("CLEAR")


def test_nonnegativity_and_dominant_driver_attribution() -> None:
    report = evaluate_darkness(
        coherence_r=0.95,
        noise_level=0.05,
        boundary_failure=0.05,
        interface_mismatch=0.72,
    )
    assert report.darkness_d > 0.0
    assert 0.0 < report.attenuation_factor < 1.0
    assert report.dominant_driver == "interface_mismatch"


def test_negative_weight_rejected() -> None:
    bad_weights = DarknessWeights(alpha_coherence=-0.1)
    try:
        evaluate_darkness(0.9, 0.1, 0.1, 0.1, weights=bad_weights)
        assert False, "Expected ValueError for negative weight"
    except ValueError:
        pass


def test_propensity_attenuation_monotonicity() -> None:
    q_low_dark = propensity_with_darkness(1.0, 0.9, 0.85, 0.95, darkness_d=0.05)
    q_high_dark = propensity_with_darkness(1.0, 0.9, 0.85, 0.95, darkness_d=0.65)
    assert q_low_dark > q_high_dark > 0.0
