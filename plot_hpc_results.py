import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# HPC Results (compute2 OpenMP, master MPI)
serial_hpc  = {256: 0.0946, 512: 0.3769, 1024: 2.7168}

omp_hpc = {
    256:  {1: 0.1005, 4: 0.0340},
    512:  {1: 0.1005, 4: 0.1136},
    1024: {1: 0.1005, 4: 0.8601},
}

mpi_hpc = {
    256:  {1: 0.1012, 2: 0.0581, 4: 0.0581, 8: 0.0233},
    512:  {1: 0.3838, 2: 0.2028, 4: 0.1087, 8: 0.0635},
    1024: {1: 2.3473, 2: 1.5372, 4: 0.8409, 8: 0.4241},
}

sizes  = [256, 512, 1024]
labels = ['256x256', '512x512', '1024x1024']
x = np.arange(len(sizes))
w = 0.12

# Plot 1: HPC Time comparison
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - 2.5*w, [serial_hpc[n]   for n in sizes], w, label='Serial',    color='gray')
ax.bar(x - 1.5*w, [omp_hpc[n][4]   for n in sizes], w, label='OMP 4T',    color='#C44E52')
ax.bar(x - 0.5*w, [mpi_hpc[n][2]   for n in sizes], w, label='MPI 2P',    color='#55A868')
ax.bar(x + 0.5*w, [mpi_hpc[n][4]   for n in sizes], w, label='MPI 4P',    color='#8172B2')
ax.bar(x + 1.5*w, [mpi_hpc[n][8]   for n in sizes], w, label='MPI 8P',    color='#CCB974')
ax.set_xlabel('Grid Size', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('HPC Results: Serial vs OpenMP vs MPI (SINES HPC)', fontsize=13)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('report/hpc_time_comparison.png', dpi=150)
print("Saved hpc_time_comparison.png")

# Plot 2: MPI Speedup on HPC
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, n in enumerate(sizes):
    ax = axes[idx]
    base = serial_hpc[n]
    procs = [1, 2, 4, 8]
    mpi_speedup = [base / mpi_hpc[n][p] for p in procs]
    ax.plot(procs, procs,       'k--', label='Ideal')
    ax.plot(procs, mpi_speedup, 's-',  label='MPI HPC', color='#8172B2', linewidth=2, markersize=8)
    ax.set_title(f'MPI Speedup — {n}x{n}', fontsize=12)
    ax.set_xlabel('MPI Processes')
    ax.set_ylabel('Speedup')
    ax.set_xticks(procs)
    ax.legend()
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('report/hpc_mpi_speedup.png', dpi=150)
print("Saved hpc_mpi_speedup.png")

# Plot 3: Local vs HPC comparison for MPI 4 proc
fig, ax = plt.subplots(figsize=(9, 5))
local_mpi4 = [0.0711, 0.3149, 3.5986]
hpc_mpi4   = [mpi_hpc[n][4] for n in sizes]
hpc_mpi8   = [mpi_hpc[n][8] for n in sizes]
ax.plot(sizes, local_mpi4, 'o-', label='Local MPI 4P', color='#C44E52', linewidth=2)
ax.plot(sizes, hpc_mpi4,   's-', label='HPC MPI 4P',   color='#8172B2', linewidth=2)
ax.plot(sizes, hpc_mpi8,   '^-', label='HPC MPI 8P',   color='#55A868', linewidth=2)
ax.set_xlabel('Grid Size (N)', fontsize=12)
ax.set_ylabel('Time (seconds)', fontsize=12)
ax.set_title('Local vs HPC: MPI Scaling', fontsize=13)
ax.set_xticks(sizes)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('report/local_vs_hpc.png', dpi=150)
print("Saved local_vs_hpc.png")
