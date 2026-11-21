from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

DEFAULT_FIG_DIR = Path(__file__).resolve().parent.parent / "figures"


def order_parameter(theta: np.ndarray) -> tuple[float, float]:
    """Compute Kuramoto order parameter magnitude r in [0, 1] and mean phase psi."""
    z = np.mean(np.exp(1j * theta))
    return float(np.abs(z)), float(np.angle(z))


def group_order_parameters(theta: np.ndarray, group_ids: np.ndarray, groups: int) -> np.ndarray:
    """Compute order parameter r_g for each subsystem group."""
    vals = []
    for g in range(groups):
        rg_val, _ = order_parameter(theta[group_ids == g])
        vals.append(rg_val)
    return np.array(vals)


def interface_mismatch(rg: np.ndarray, r_global: float) -> float:
    """
    Measure subsystem interface mismatch M_I(t):
    combines inter-group coherence dispersion and local-vs-global phase divergence.
    """
    inter_group_spread = float(np.mean(np.abs(rg - np.mean(rg))))
    local_global_gap = max(0.0, float(np.mean(rg)) - r_global)
    return inter_group_spread + local_global_gap


def constraint_failure(theta: np.ndarray, bound: float = 1.2) -> float:
    """Quadratic boundary degradation penalty F_C(t) outside admissible phase window."""
    return float(np.mean(np.maximum(0.0, np.abs(theta) - bound) ** 2))


def noise_metric(deterministic_vel: np.ndarray, stochastic_kick: np.ndarray, dt: float) -> float:
    """Perturbation load N(t) combining velocity dispersion and active stochastic variance."""
    effective_noise = stochastic_kick / np.sqrt(dt)
    return float(np.var(deterministic_vel) + np.var(effective_noise))


def run_simulation(
    k_restore: float = 0.8,
    seed: int = 7,
    N: int = 60,
    groups: int = 3,
    T: float = 40.0,
    dt: float = 0.02,
    K_local: float = 1.2,
    K_global: float = 0.4,
    noise_base: float = 0.08,
    noise_perturb: float = 0.22,
    perturb_window: tuple[float, float] = (10.0, 18.0),
    restore_window: tuple[float, float] = (22.0, 34.0),
    weights: tuple[float, float, float, float] = (1.0, 0.8, 0.7, 1.3),
    C_omega_base: float = 1.0,
    phi_base: float = 1.0,
    phi_restore_boost: float = 0.25,
) -> dict[str, np.ndarray]:
    """Simulate constrained Kuramoto network under perturbation and restoration."""
    rng = np.random.default_rng(seed)
    steps = int(T / dt)
    alpha, beta, gamma, delta = weights
    t_p0, t_p1 = perturb_window
    t_r0, t_r1 = restore_window

    theta = rng.uniform(-np.pi, np.pi, N)
    omega = rng.normal(0.0, 0.25, N)
    group_ids = np.array([i % groups for i in range(N)])

    same_group = group_ids[:, None] == group_ids[None, :]
    K_matrix = np.where(same_group, K_local, K_global) / N
    np.fill_diagonal(K_matrix, 0.0)

    t_log = np.zeros(steps)
    r_log = np.zeros(steps)
    r_local_mean_log = np.zeros(steps)
    d_log = np.zeros(steps)
    d_cum_log = np.zeros(steps)
    s_log = np.zeros(steps)
    components_log = np.zeros((steps, 4))

    cumulative_darkness = 0.0

    for step in range(steps):
        t = step * dt
        in_perturb = t_p0 < t < t_p1
        in_restore = t_r0 < t < t_r1
        noise_sigma = noise_perturb if in_perturb else noise_base

        phase_diff = theta[None, :] - theta[:, None]
        coupling = np.sum(K_matrix * np.sin(phase_diff), axis=1)

        r, psi = order_parameter(theta)
        control = k_restore * np.sin(psi - theta) if in_restore else np.zeros(N)

        deterministic_vel = omega + coupling + control
        stochastic_kick = rng.normal(0.0, noise_sigma * np.sqrt(dt), N)

        theta = theta + dt * deterministic_vel + stochastic_kick
        theta = (theta + np.pi) % (2.0 * np.pi) - np.pi

        r, _ = order_parameter(theta)
        rg = group_order_parameters(theta, group_ids, groups)

        decoherence = 1.0 - r
        N_val = noise_metric(deterministic_vel, stochastic_kick, dt)
        FC_val = constraint_failure(theta)
        MI_val = interface_mismatch(rg, r)

        D = alpha * decoherence + beta * N_val + gamma * FC_val + delta * MI_val
        cumulative_darkness += D * dt

        C_omega = C_omega_base * np.exp(-0.5 * FC_val)
        Phi = phi_base + (phi_restore_boost * k_restore if in_restore else 0.0)
        S = r * C_omega * Phi * np.exp(-D)

        t_log[step] = t
        r_log[step] = r
        r_local_mean_log[step] = float(np.mean(rg))
        d_log[step] = D
        d_cum_log[step] = cumulative_darkness
        s_log[step] = S
        components_log[step] = [
            alpha * decoherence,
            beta * N_val,
            gamma * FC_val,
            delta * MI_val,
        ]

    return {
        "t": t_log,
        "r": r_log,
        "r_local_mean": r_local_mean_log,
        "D": d_log,
        "D_cum": d_cum_log,
        "S": s_log,
        "components": components_log,
    }


def save_baseline_figures(results: dict[str, np.ndarray], fig_dir: Path | str = DEFAULT_FIG_DIR) -> None:
    """Generate diagnostic plots for r(t), D[Sigma, t], and S(t)."""
    out_dir = Path(fig_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t = results["t"]

    plt.figure(figsize=(8, 4))
    plt.plot(t, results["r"], label="Global Coherence r(t)", linewidth=2)
    plt.plot(t, results["r_local_mean"], "--", label="Mean Local Group Coherence", alpha=0.8)
    plt.axvspan(10, 18, color="red", alpha=0.1, label="Perturbation")
    plt.axvspan(22, 34, color="green", alpha=0.1, label="Restoration")
    plt.xlabel("Time t")
    plt.ylabel("Order Parameter r(t)")
    plt.title("Global vs. Local Subsystem Coherence")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "comparison_r.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(t, results["D"], color="black", linewidth=2, label="Total Darkness D[Σ, t]")
    labels = ["α(1 - r)", "β N(t)", "γ F_C(t)", "δ M_I(t)"]
    for idx, label in enumerate(labels):
        plt.plot(t, results["components"][:, idx], alpha=0.75, label=label)
    plt.axvspan(10, 18, color="red", alpha=0.1)
    plt.axvspan(22, 34, color="green", alpha=0.1)
    plt.xlabel("Time t")
    plt.ylabel("Darkness Load")
    plt.title("Darkness Functional D[Σ, t] Component Breakdown")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "comparison_D.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(t, results["S"], color="navy", linewidth=2, label="Persistence S(t)")
    plt.axvspan(10, 18, color="red", alpha=0.1, label="Perturbation")
    plt.axvspan(22, 34, color="green", alpha=0.1, label="Restoration")
    plt.xlabel("Time t")
    plt.ylabel("Persistence S(t)")
    plt.title("Darkness-Aware Persistence S(t) = r · C(Ω,t) · Φ(t) · exp(-D)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "comparison_S.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    res = run_simulation(k_restore=0.8, seed=7)
    save_baseline_figures(res)
    print(f"Simulation complete. Final S(T)={res['S'][-1]:.3f}, Cumulative D={res['D_cum'][-1]:.2f}")

