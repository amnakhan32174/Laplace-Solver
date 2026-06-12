#include <iostream>
#include <vector>
#include <chrono>
#include <mpi.h>

using namespace std;

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int N      = (argc > 1) ? atoi(argv[1]) : 256;
    int epochs = (argc > 2) ? atoi(argv[2]) : 1000;

    int rows_per_proc = N / size;
    int start_row     = rank * rows_per_proc;
    int end_row       = (rank == size - 1) ? N : start_row + rows_per_proc;
    int local_rows    = end_row - start_row;

    vector<vector<double>> grid    (local_rows + 2, vector<double>(N, 0.0));
    vector<vector<double>> new_grid(local_rows + 2, vector<double>(N, 0.0));

    if (rank == 0) {
        for (int j = 0; j < N; j++) {
            grid[1][j]     = 100.0;
            new_grid[1][j] = 100.0;
        }
    }

    double start_time = MPI_Wtime();

    for (int epoch = 0; epoch < epochs; epoch++) {

        MPI_Request reqs[4];
        int nreqs = 0;

        if (rank < size - 1) {
            MPI_Isend(grid[local_rows].data(),   N, MPI_DOUBLE, rank+1, 0, MPI_COMM_WORLD, &reqs[nreqs++]);
            MPI_Irecv(grid[local_rows+1].data(), N, MPI_DOUBLE, rank+1, 1, MPI_COMM_WORLD, &reqs[nreqs++]);
        }
        if (rank > 0) {
            MPI_Isend(grid[1].data(), N, MPI_DOUBLE, rank-1, 1, MPI_COMM_WORLD, &reqs[nreqs++]);
            MPI_Irecv(grid[0].data(), N, MPI_DOUBLE, rank-1, 0, MPI_COMM_WORLD, &reqs[nreqs++]);
        }
        MPI_Waitall(nreqs, reqs, MPI_STATUSES_IGNORE);

        for (int i = 1; i <= local_rows; i++) {
            if (rank == 0 && i == 1) continue;
            if (rank == size - 1 && i == local_rows) continue;
            for (int j = 1; j < N - 1; j++) {
                new_grid[i][j] = 0.25 * (grid[i-1][j] + grid[i+1][j] +
                                          grid[i][j-1] + grid[i][j+1]);
            }
        }

        if (rank == 0)
            for (int j = 0; j < N; j++) new_grid[1][j] = 100.0;

        swap(grid, new_grid);
    }

    double elapsed = MPI_Wtime() - start_time;

    double max_time;
    MPI_Reduce(&elapsed, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0)
        cout << "MPI | N=" << N << " epochs=" << epochs
             << " procs=" << size
             << " | Time: " << max_time << "s" << endl;

    // Correctness check
    int center_row   = N / 2;
    int center_owner = center_row / rows_per_proc;
    if (center_owner >= size) center_owner = size - 1;
    int local_center_row = center_row - (center_owner * rows_per_proc) + 1;

    double center_val = 0.0;
    if (rank == center_owner)
        center_val = grid[local_center_row][N / 2];

    double global_center;
    MPI_Reduce(&center_val, &global_center, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0)
        cout << "Center value: " << global_center << endl;

    MPI_Finalize();
    return 0;
}
