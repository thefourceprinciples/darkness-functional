import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)

N = 60
groups = 3
T = 40
dt = 0.02
steps = int(T/dt)

K_local = 1.2
K_global = 0.4

noise_base = 0.08
noise_perturb = 0.22

perturb_start = 10
perturb_end = 18

restore_start = 22
restore_end = 34

k_restore = 0.8

alpha, beta, gamma, delta = 1.0, 0.8, 0.7, 1.3

theta = np.random.uniform(-np.pi, np.pi, N)
omega = np.random.normal(0, 0.25, N)

group_ids = np.array([i % groups for i in range(N)])

def order_parameter(theta):
    z = np.mean(np.exp(1j * theta))
    return np.abs(z), np.angle(z)

def interface_mismatch(rg):
    return np.sum(np.abs(rg - np.mean(rg)))

def constraint_failure(theta):
    return np.mean(np.maximum(0, np.abs(theta) - 1.2)**2)

def noise_metric(v):
    return np.var(v)

t_log, r_log, d_log, s_log = [], [], [], []

for step in range(steps):
    t = step * dt
    
    noise_sigma = noise_base
    if perturb_start < t < perturb_end:
        noise_sigma = noise_perturb
        
    velocities = np.zeros(N)
    
    for i in range(N):
        local = 0
        global_c = 0
        
        for j in range(N):
            if i == j: continue
            s = np.sin(theta[j] - theta[i])
            if group_ids[i] == group_ids[j]:
                local += s
            else:
                global_c += s
        
        local *= K_local / N
        global_c *= K_global / N
        
        control = 0
        if restore_start < t < restore_end:
            _, psi = order_parameter(theta)
            control = k_restore * np.sin(psi - theta[i])
        
        noise = np.random.normal(0, noise_sigma)
        
        velocities[i] = omega[i] + local + global_c + control + noise
    
    theta += dt * velocities
    theta = (theta + np.pi) % (2*np.pi) - np.pi
    
    r, _ = order_parameter(theta)
    
    N_metric = noise_metric(velocities)
    FC_metric = constraint_failure(theta)
    MI_metric = interface_mismatch(np.array([r]))
    
    D = alpha*(1-r) + beta*N_metric + gamma*FC_metric + delta*MI_metric
    S = r * np.exp(-D)
    
    t_log.append(t)
    r_log.append(r)
    d_log.append(D)
    s_log.append(S)

plt.figure()
plt.plot(t_log, r_log)
plt.savefig("../figures/comparison_r.png")

plt.figure()
plt.plot(t_log, d_log)
plt.savefig("../figures/comparison_D.png")

plt.figure()
plt.plot(t_log, s_log)
plt.savefig("../figures/comparison_S.png")

print("Simulation complete.")