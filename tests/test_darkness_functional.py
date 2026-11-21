import sys
from pathlib import Path
import numpy as np
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from darkness_simulation_package import (
    order_parameter,
    group_order_parameters,
    interface_mismatch,
    constraint_failure,
    run_simulation,
)
from ai_memory_darkness import AIMemoryBenchmark, run_ai_memory_experiment
from lens_array_bridge import simulate_lens_array_transit


def test_order_parameter_bounds():
    """Order parameter r must equal 1.0 for identical phases and ~0 for uniform spread."""
    aligned = np.zeros(50)
    r_sync, psi = order_parameter(aligned)
    assert np.isclose(r_sync, 1.0, atol=1e-6)
    assert np.isclose(psi, 0.0, atol=1e-6)

    uniform_circle = np.linspace(-np.pi, np.pi, 1000, endpoint=False)
    r_async, _ = order_parameter(uniform_circle)
    assert r_async < 1e-3


def test_interface_mismatch_detects_local_vs_global_divergence():
    """Tests Prediction #4: local coherence can mask global instability."""
    groups = 3
    n_per_group = 20
    theta = np.concatenate([
        np.zeros(n_per_group),
        np.full(n_per_group, 2.0 * np.pi / 3.0),
        np.full(n_per_group, -2.0 * np.pi / 3.0),
    ])
    group_ids = np.repeat(np.arange(groups), n_per_group)

    r_global, _ = order_parameter(theta)
    rg = group_order_parameters(theta, group_ids, groups)
    mi = interface_mismatch(rg, r_global)

    assert np.allclose(rg, 1.0, atol=1e-6)
    assert r_global < 1e-6
    assert np.isclose(mi, 1.0, atol=1e-6)


def test_constraint_failure_boundary_behavior():
    """Constraint failure F_C must be 0 inside [-1.2, 1.2] and strictly positive outside."""
    safe_theta = np.array([-1.2, -0.5, 0.0, 0.8, 1.2])
    assert constraint_failure(safe_theta, bound=1.2) == 0.0

    violated_theta = np.array([-1.5, 0.0, 1.7])
    expected = np.mean([0.3**2, 0.0, 0.5**2])
    assert np.isclose(constraint_failure(violated_theta, bound=1.2), expected, atol=1e-6)


def test_perturbation_increases_darkness_and_drops_persistence():
    """Tests Prediction #1: persistence falls as darkness load rises."""
    res = run_simulation(k_restore=0.8, seed=7)
    t = res["t"]

    pre_mask = (t >= 4.0) & (t < 10.0)
    perturb_mask = (t > 10.5) & (t < 17.5)

    assert np.mean(res["D"][perturb_mask]) > np.mean(res["D"][pre_mask])
    assert np.mean(res["S"][perturb_mask]) < np.mean(res["S"][pre_mask])


def test_restoration_recovers_persistence_while_retaining_historical_load():
    """Tests Prediction #3: restoration improves active S(t) without erasing cumulative load."""
    no_restore = run_simulation(k_restore=0.0, seed=14)
    strong_restore = run_simulation(k_restore=1.2, seed=14)

    t = strong_restore["t"]
    restore_mask = (t > 24.0) & (t < 33.5)

    assert np.mean(strong_restore["S"][restore_mask]) > np.mean(no_restore["S"][restore_mask])
    assert strong_restore["D_cum"][-1] > 0.0
    assert np.all(np.diff(strong_restore["D_cum"]) >= 0.0)


def test_parameter_sensitivity_monotonicity():
    """Higher noise weight beta or mismatch weight delta must strictly increase D[Sigma, t]."""
    base = run_simulation(weights=(1.0, 0.8, 0.7, 1.3), seed=7)
    high_beta = run_simulation(weights=(1.0, 2.5, 0.7, 1.3), seed=7)
    high_delta = run_simulation(weights=(1.0, 0.8, 0.7, 3.0), seed=7)

    assert np.mean(high_beta["D"]) > np.mean(base["D"])
    assert np.mean(high_delta["D"]) > np.mean(base["D"])


def test_spatial_lens_array_critical_spacing():
    """Sub-critical node spacing must maintain higher persistence than super-critical spacing."""
    tight = simulate_lens_array_transit(spacing_d=1.8, seed=7)
    wide = simulate_lens_array_transit(spacing_d=4.5, seed=7)

    assert np.mean(tight["S"]) > np.mean(wide["S"])
    assert np.mean(tight["D"]) < np.mean(wide["D"])


def test_ai_memory_contradiction_and_provenance_penalties():
    """Contradictory facts and missing provenance must spike D even when similarity r is high."""
    bench = AIMemoryBenchmark(seed=7)
    topic = bench._unit_vec()
    canonical = {"spec_alpha": 42}

    clean_rec = bench.ingest(topic, "spec_alpha", 42, turn=1, has_provenance=True, jitter=0.01)
    clean_metrics = bench.evaluate_turn(topic, [clean_rec], canonical, throughput_phi=1.0)

    corrupt_rec = bench.ingest(topic, "spec_alpha", 999, turn=2, has_provenance=False, jitter=0.01)
    corrupt_metrics = bench.evaluate_turn(topic, [clean_rec, corrupt_rec], canonical, throughput_phi=1.0)

    assert corrupt_metrics["MI"] > clean_metrics["MI"]
    assert corrupt_metrics["FC"] > clean_metrics["FC"]
    assert corrupt_metrics["D"] > clean_metrics["D"]
    assert corrupt_metrics["S"] < clean_metrics["S"]


def test_ai_memory_consolidation_restores_persistence():
    """Consolidation pass at turn 28 must reduce Darkness D and restore Persistence S."""
    hist = run_ai_memory_experiment(turns=40, seed=7)

    corrupt_window = slice(20, 27)
    consolidated_window = slice(32, 39)

    assert np.mean(hist["D"][consolidated_window]) < np.mean(hist["D"][corrupt_window])
    assert np.mean(hist["S"][consolidated_window]) > np.mean(hist["S"][corrupt_window])
