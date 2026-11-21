from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

DEFAULT_FIG_DIR = Path(__file__).resolve().parent.parent / "figures"


def array_potential(x: np.ndarray, y: np.ndarray, nodes: np.ndarray, M: float, eps: float) -> np.ndarray:
    phi = np.zeros_like(x, dtype=float)
    for nx, ny in nodes:
        r2 = (x - nx) ** 2 + (y - ny) ** 2
        phi -= M / np.sqrt(r2 + eps ** 2)
    return phi


def array_gradient(x: np.ndarray, y: np.ndarray, nodes: np.ndarray, M: float, eps: float) -> tuple[np.ndarray, np.ndarray]:
    fx = np.zeros_like(x, dtype=float)
    fy = np.zeros_like(y, dtype=float)
    for nx, ny in nodes:
        dx = x - nx
        dy = y - ny
        denom = (dx ** 2 + dy ** 2 + eps ** 2) ** 1.5
        fx -= M * dx / denom
        fy -= M * dy / denom
    return fx, fy


def simulate_lens_array_transit(
    spacing_d: float = 2.5,
    num_lenses: int = 6,
    M: float = 1.4,
    eps: float = 0.45,
    ambient_lambda0: float = 0.85,
    noise_sigma: float = 0.18,
    n_trajectories: int = 40,
    seed: int = 7,
) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    lens_x = np.arange(num_lenses) * spacing_d + 1.5
    nodes = np.column_stack([lens_x, np.zeros(num_lenses)])
    x_max = lens_x[-1] + 2.0

    dt = 0.02
    steps = int(x_max / dt)

    pos_x = np.zeros(n_trajectories)
    pos_y = rng.normal(0.0, 0.35, n_trajectories)
    vel_x = np.ones(n_trajectories) * 1.0
    vel_y = rng.normal(0.0, 0.12, n_trajectories)
    theta = rng.normal(0.0, 0.25, n_trajectories)

    x_trace = np.zeros(steps)
    r_trace = np.zeros(steps)
    d_trace = np.zeros(steps)
    s_trace = np.zeros(steps)
    y_paths = np.zeros((steps, n_trajectories))

    for step in range(steps):
        fx, fy = array_gradient(pos_x, pos_y, nodes, M, eps)
        phi_local = array_potential(pos_x, pos_y, nodes, M, eps)

        well_relief = np.clip(-phi_local, 0.0, ambient_lambda0)
        effective_lambda = ambient_lambda0 - well_relief

        vel_y += dt * (fy - 0.15 * vel_y) + rng.normal(0.0, noise_sigma * np.sqrt(dt), n_trajectories)
        pos_x += dt * vel_x
        pos_y += dt * vel_y

        psi_mean = np.angle(np.mean(np.exp(1j * theta)))
        phase_restore = 0.9 * well_relief * np.sin(psi_mean - theta)
        theta += dt * phase_restore + rng.normal(0.0, noise_sigma * np.sqrt(dt), n_trajectories)

        r = float(np.abs(np.mean(np.exp(1j * theta))))
        N_load = float(np.var(vel_y) + np.mean(effective_lambda))
        FC_load = float(np.mean(np.maximum(0.0, np.abs(pos_y) - 0.8) ** 2))
        MI_load = float(np.std(well_relief))

        D = 1.0 * (1.0 - r) + 0.8 * N_load + 0.7 * FC_load + 1.3 * MI_load
        C_omega = float(np.exp(-0.5 * FC_load))
        Phi_flux = float(1.0 + 0.5 * np.mean(well_relief))
        S = r * C_omega * Phi_flux * np.exp(-D)

        x_trace[step] = float(np.mean(pos_x))
        r_trace[step] = r
        d_trace[step] = D
        s_trace[step] = S
        y_paths[step] = pos_y

    return {"x": x_trace, "r": r_trace, "D": d_trace, "S": s_trace, "y_paths": y_paths, "nodes": nodes}


if __name__ == "__main__":
    DEFAULT_FIG_DIR.mkdir(parents=True, exist_ok=True)
    tight = simulate_lens_array_transit(spacing_d=1.8)
    wide = simulate_lens_array_transit(spacing_d=4.5)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    ax1.plot(tight["x"], tight["S"], color="navy", linewidth=2, label="Sub-Critical Array (d = 1.8)")
    ax1.plot(wide["x"], wide["S"], "--", color="crimson", linewidth=2, label="Super-Critical Array (d = 4.5)")
    ax1.set_ylabel("Spatial Persistence S(x)")
    ax1.set_title("Spatial Potential Array: Persistence Across a Constrained Region")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(tight["x"], tight["D"], color="navy", linewidth=2, label="Darkness Load D(x) [d = 1.8]")
    ax2.plot(wide["x"], wide["D"], "--", color="crimson", linewidth=2, label="Darkness Load D(x) [d = 4.5]")
    ax2.set_xlabel("Propagation Distance x")
    ax2.set_ylabel("Darkness Functional D[Σ, x]")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(DEFAULT_FIG_DIR / "lens_array_persistence.png", dpi=150)
    plt.close()
    print("Lens array transit simulation complete.")
