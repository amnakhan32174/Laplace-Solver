import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

serial = {256: 0.0640, 512: 0.2578, 1024: 3.4596}

omp = {
    256:  {1: 0.0587, 2: 0.0368, 4: 0.1085},
    512:  {1: 0.2632, 2: 0.1710, 4: 0.2631},
    1024: {1: 3.4219, 2: 2.8329, 4: 2.6695},
}

mpi = {
    256:  {1: 0.0542, 2: 0.0435, 4: 0.0711},
    512:  {1: 0.2376, 2: 0.1566, 4: 0.3149},
    1024: {1: 3.2824, 2: 2.8841, 4: 3.5986},
}

sizes  = [256, 512, 1024]
labels = ['256x256', '512x512', '1024x1024']
x = np.arange(len(sizes))
w = 0.12

# Plot 1: Time comparison
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - 3*w, [serial[n]    for n in sizes], w, label='Serial',    color='gray')
ax.bar(x - 2*w, [omp[n][1]    for n in sizes], w, label='OMP 1T',   color='#4C72B0')
ax.bar(x - 1*w, [omp[n][2]    for n in sizes], w, label='OMP 2T',   color='#55A868')
ax.bar(x,       [omp[n][4]    for n in sizes], w, label='OMP 4T',   color='#C44E52')
ax.bar(x + 1*w, [mpi[n][1]    for n in sizes], w, label='MPI 1P',   color='#8172B2')
ax.bar(x + 2*w, [mpi[n][2]    for n in sizes], w, label='MPI 2P',   color='#CCB974')
ax.bar(x + 3*w, [mpi[n][4]    for n in sizes], w, label='MPI 4P',   color='#64B5CD')
ax.set_xlabel('Grid Size', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('Laplace Solver: Serial vs OpenMP vs MPI', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('report/time_comparison.png', dpi=150)
print("Saved time_comparison.png")

# Plot 2: Speedup
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, n in enumerate(sizes):
    ax = axes[idx]
    base = serial[n]
    procs = [1, 2, 4]
    omp_speedup = [base / omp[n][p] for p in procs]
    mpi_speedup = [base / mpi[n][p] for p in procs]
    ax.plot(procs, procs,       'k--', label='Ideal')
    ax.plot(procs, omp_speedup, 'o-',  label='OpenMP', color='#55A868', linewidth=2)
    ax.plot(procs, mpi_speedup, 's-',  label='MPI',    color='#8172B2', linewidth=2)
    ax.set_title(f'Speedup — {n}x{n}', fontsize=12)
    ax.set_xlabel('Threads / Processes')
    ax.set_ylabel('Speedup')
    ax.set_xticks(procs)
    ax.legend()
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('report/speedup.png', dpi=150)
print("Saved speedup.png")

# Plot 3: Scaling with grid size (MPI 2 proc vs Serial)
fig, ax = plt.subplots(figsize=(8, 5))
ns = [256, 512, 1024]
ax.plot(ns, [serial[n] for n in ns],  'o-', label='Serial',    color='gray',    linewidth=2)
ax.plot(ns, [omp[n][2] for n in ns],  's-', label='OpenMP 2T', color='#55A868', linewidth=2)
ax.plot(ns, [mpi[n][2] for n in ns],  '^-', label='MPI 2P',    color='#8172B2', linewidth=2)
ax.set_xlabel('Grid Size (N)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('Scaling with Problem Size', fontsize=14)
ax.set_xticks(ns)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('report/scaling.png', dpi=150)
print("Saved scaling.png")
