from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from darkness_simulation_package import run_simulation

DEFAULT_FIG_DIR = Path(__file__).resolve().parent.parent / "figures"


def sweep_restoration(
    k_vals: np.ndarray = np.linspace(0.0, 1.5, 16),
    seeds: tuple[int, ...] = (7, 14, 21, 28, 35),
    fig_dir: Path | str = DEFAULT_FIG_DIR,
) -> None:
    """Sweep restoration coupling k_restore across multiple random seeds."""
    out_dir = Path(fig_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    post_S_mean, post_S_std = [], []
    post_D_mean, post_D_std = [], []
    cum_D_mean, cum_D_std = [], []

    for k in k_vals:
        s_runs, d_runs, dcum_runs = [], [], []
        for s in seeds:
            res = run_simulation(k_restore=float(k), seed=s)
            t = res["t"]
            post_mask = t > 34.0

            s_runs.append(np.mean(res["S"][post_mask]))
            d_runs.append(np.mean(res["D"][post_mask]))
            dcum_runs.append(res["D_cum"][-1])

        post_S_mean.append(np.mean(s_runs))
        post_S_std.append(np.std(s_runs))
        post_D_mean.append(np.mean(d_runs))
        post_D_std.append(np.std(d_runs))
        cum_D_mean.append(np.mean(dcum_runs))
        cum_D_std.append(np.std(dcum_runs))

    post_S_mean = np.array(post_S_mean)
    post_S_std = np.array(post_S_std)
    post_D_mean = np.array(post_D_mean)
    post_D_std = np.array(post_D_std)
    cum_D_mean = np.array(cum_D_mean)
    cum_D_std = np.array(cum_D_std)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.plot(k_vals, post_S_mean, "o-", color="navy", label="Post-Control Persistence S(t > 34)")
    ax1.fill_between(k_vals, post_S_mean - post_S_std, post_S_mean + post_S_std, color="navy", alpha=0.15)
    ax1.plot(k_vals, post_D_mean, "s--", color="crimson", label="Post-Control Darkness D(t > 34)")
    ax1.fill_between(k_vals, post_D_mean - post_D_std, post_D_mean + post_D_std, color="crimson", alpha=0.15)
    ax1.set_xlabel("Restoration Coupling (k_restore)")
    ax1.set_ylabel("Metric Value")
    ax1.set_title("Post-Restoration Persistence vs. Residual Darkness")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(k_vals, cum_D_mean, "^-", color="darkorange", label="Cumulative Historical Load ∫D dt")
    ax2.fill_between(k_vals, cum_D_mean - cum_D_std, cum_D_mean + cum_D_std, color="darkorange", alpha=0.2)
    ax2.set_xlabel("Restoration Coupling (k_restore)")
    ax2.set_ylabel("Cumulative Darkness Load")
    ax2.set_title("Historical Load Retention Under Restoration")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_dir / "restoration_sweep.png", dpi=150)
    plt.close()
    print("Restoration sweep complete.")


if __name__ == "__main__":
    sweep_restoration()

