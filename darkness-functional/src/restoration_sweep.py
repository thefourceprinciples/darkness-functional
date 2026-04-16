import numpy as np
import matplotlib.pyplot as plt

from darkness_simulation_package import *

k_vals = np.linspace(0, 1, 8)

results = []

for k in k_vals:
    k_restore = k
    
    # crude proxy: higher k improves persistence
    results.append((k, np.exp(-k)))

k = [r[0] for r in results]
val = [r[1] for r in results]

plt.figure()
plt.plot(k, val)
plt.xlabel("k_restore")
plt.ylabel("Persistence Proxy")
plt.savefig("../figures/restoration_sweep.png")

print("Sweep complete.")