# Laplace Solver - HPC Project

## Dependencies
- g++ (C++11), OpenMP, MPICH/OpenMPI, CMake >= 3.10

## Build
```bash
mkdir build && cd build && cmake .. && make && cd ..
```

## Run
```bash
# Serial
./build/laplace_serial <N> <epochs>

# OpenMP
./build/laplace_openmp <N> <epochs> <threads>

# MPI
mpirun -np <procs> ./build/laplace_mpi <N> <epochs>
```

## Structure
