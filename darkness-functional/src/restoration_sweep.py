import os
import numpy as np
import matplotlib.pyplot as plt
from darkness_simulation_package import run_simulation


def sweep_restoration(
    k_vals: np.ndarray = np.linspace(0.0, 1.5, 16),
    seeds: tuple[int, ...] = (7, 14, 21, 28, 35),
    fig_dir: str = "../figures",
) -> None:
    """
    Sweep restoration coupling k_restore across multiple random seeds to evaluate:
    1. Post-restoration Persistence S(t > 34) (tests whether structure holds after control ends)
    2. Active-restoration Darkness D[Sigma, t in (22, 34)]
    3. Cumulative historical Darkness Load int D dt (tests Prediction #3)
    """
    os.makedirs(fig_dir, exist_ok=True)

    post_S_mean, post_S_std = [], []
    post_D_mean, post_D_std = [], []
    cum_D_mean, cum_D_std = [], []

    for k in k_vals:
        s_runs, d_runs, dcum_runs = [], [], []
        for s in seeds:
            res = run_simulation(k_restore=float(k), seed=s)
            t = res["t"]
            post_mask = t > 34.0  # Unassisted persistence window after restoration ends

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

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Panel A: Unassisted Post-Restoration Persistence & Residual Darkness
    ax1 = axes[0]
    ax1.plot(k_vals, post_S_mean, "o-", color="navy", label="Post-Control Persistence S(t > 34)")
    ax1.fill_between(k_vals, post_S_mean - post_S_std, post_S_mean + post_S_std, color="navy", alpha=0.15)
    ax1.plot(k_vals, post_D_mean, "s--", color="crimson", label="Post-Control Darkness D(t > 34)")
    ax1.fill_between(k_vals, post_D_mean - post_D_std, post_D_mean + post_D_std, color="crimson", alpha=0.15)
    ax1.set_xlabel("Restoration Coupling (k_restore)")
    ax1.set_ylabel("Metric Value")
    ax1.set_title("Post-Restoration Persistence vs. Residual Darkness")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Panel B: Cumulative Historical Darkness Load (Prediction #3)
    ax2 = axes[1]
    ax2.plot(k_vals, cum_D_mean, "^-", color="darkorange", label="Cumulative Historical Load ∫D dt")
    ax2.fill_between(k_vals, cum_D_mean - cum_D_std, cum_D_mean + cum_D_std, color="darkorange", alpha=0.2)
    ax2.set_xlabel("Restoration Coupling (k_restore)")
    ax2.set_ylabel("Cumulative Darkness Load")
    ax2.set_title("Historical Load Retention Under Restoration")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "restoration_sweep.png"), dpi=150)
    plt.close()
    print("Restoration sweep complete. Saved figures/restoration_sweep.png")


if __name__ == "__main__":
    sweep_restoration()
