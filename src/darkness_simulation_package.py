"""
Darkness Functional baseline simulation.

This script provides a small, readable toy model for exploring the Darkness
Functional in a coupled oscillator system. It is not empirical validation.
It is a reproducible starting point for computational experiments.

Run:
    python src/darkness_simulation_package.py

Outputs:
    figures/comparison_r.png
    figures/comparison_D.png
    figures/comparison_S.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for the oscillator simulation."""

    n_oscillators: int = 48
    steps: int = 600
    dt: float = 0.05
    coupling: float = 0.35
    noise_scale: float = 0.08
    perturb_start: int = 220
    perturb_end: int = 360
    perturb_strength: float = 0.85
    restoration_strength: float = 0.45
    seed: int = 42


@dataclass(frozen=True)
class DarknessWeights:
    """Weights for the Darkness Functional."""

    alpha: float = 1.0  # incoherence weight
    beta: float = 0.7   # noise weight
    gamma: float = 0.8  # constraint failure weight
    delta: float = 0.9  # interface mismatch weight


def order_parameter(theta: np.ndarray) -> float:
    """Return Kuramoto-style coherence score R in [0, 1]."""

    return float(abs(np.mean(np.exp(1j * theta))))


def circular_mismatch(theta: np.ndarray) -> float:
    """Estimate interface mismatch between two halves of the oscillator array."""

    half = len(theta) // 2
    left = order_parameter(theta[:half])
    right = order_parameter(theta[half:])
    global_r = order_parameter(theta)
    return float(max(0.0, ((left + right) / 2.0) - global_r))


def darkness_load(
    r: float,
    noise: float,
    constraint_failure: float,
    mismatch: float,
    weights: DarknessWeights,
) -> float:
    """Compute D = alpha(1-r) + beta*N + gamma*F_C + delta*M_I."""

    return float(
        weights.alpha * (1.0 - r)
        + weights.beta * noise
        + weights.gamma * constraint_failure
        + weights.delta * mismatch
    )


def persistence_score(
    r: float,
    constraint_integrity: float,
    throughput: float,
    darkness: float,
) -> float:
    """Compute S = r * C * Phi * exp(-D)."""

    return float(r * constraint_integrity * throughput * np.exp(-darkness))


def simulate(
    config: SimulationConfig,
    weights: DarknessWeights,
    restoration: bool = False,
) -> Dict[str, np.ndarray]:
    """Run the toy oscillator model."""

    rng = np.random.default_rng(config.seed)
    theta = rng.uniform(0.0, 2.0 * np.pi, config.n_oscillators)
    natural_frequency = rng.normal(1.0, 0.05, config.n_oscillators)

    r_values = np.zeros(config.steps)
    d_values = np.zeros(config.steps)
    s_values = np.zeros(config.steps)
    mismatch_values = np.zeros(config.steps)
    constraint_values = np.zeros(config.steps)

    target_phase = 0.0

    for step in range(config.steps):
        in_perturbation = config.perturb_start <= step <= config.perturb_end

        perturbation = config.perturb_strength if in_perturbation else 0.0
        constraint_failure = perturbation
        constraint_integrity = max(0.0, 1.0 - constraint_failure)

        coupling_term = config.coupling * np.sin(np.mean(theta) - theta)
        noise = config.noise_scale + perturbation * rng.uniform(0.0, 1.0)
        stochastic_term = rng.normal(0.0, noise, config.n_oscillators)

        if restoration and step > config.perturb_end:
            restore_term = config.restoration_strength * np.sin(target_phase - theta)
        else:
            restore_term = 0.0

        theta = theta + config.dt * (natural_frequency + coupling_term + restore_term) + stochastic_term

        r = order_parameter(theta)
        mismatch = circular_mismatch(theta)
        darkness = darkness_load(r, noise, constraint_failure, mismatch, weights)
        throughput = 1.0
        persistence = persistence_score(r, constraint_integrity, throughput, darkness)

        r_values[step] = r
        d_values[step] = darkness
        s_values[step] = persistence
        mismatch_values[step] = mismatch
        constraint_values[step] = constraint_integrity

    return {
        "r": r_values,
        "D": d_values,
        "S": s_values,
        "mismatch": mismatch_values,
        "constraint_integrity": constraint_values,
    }


def plot_comparison(
    baseline: Dict[str, np.ndarray],
    restored: Dict[str, np.ndarray],
    key: str,
    ylabel: str,
    output_path: Path,
) -> None:
    """Plot baseline versus restored condition for one metric."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 5))
    plt.plot(baseline[key], label="baseline")
    plt.plot(restored[key], label="restoration")
    plt.xlabel("time step")
    plt.ylabel(ylabel)
    plt.title(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def run_experiment() -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Run baseline and restoration scenarios, then save comparison plots."""

    config = SimulationConfig()
    weights = DarknessWeights()

    baseline = simulate(config, weights, restoration=False)
    restored = simulate(config, weights, restoration=True)

    figure_dir = Path("figures")
    plot_comparison(baseline, restored, "r", "Coherence R(t)", figure_dir / "comparison_r.png")
    plot_comparison(baseline, restored, "D", "Darkness Load D(t)", figure_dir / "comparison_D.png")
    plot_comparison(baseline, restored, "S", "Persistence S(t)", figure_dir / "comparison_S.png")

    return baseline, restored


if __name__ == "__main__":
    baseline_result, restored_result = run_experiment()
    print("Baseline final R:", round(float(baseline_result["r"][-1]), 4))
    print("Restored final R:", round(float(restored_result["r"][-1]), 4))
    print("Baseline final D:", round(float(baseline_result["D"][-1]), 4))
    print("Restored final D:", round(float(restored_result["D"][-1]), 4))
    print("Baseline final S:", round(float(baseline_result["S"][-1]), 4))
    print("Restored final S:", round(float(restored_result["S"][-1]), 4))
