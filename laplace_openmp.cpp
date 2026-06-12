#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <omp.h>

using namespace std;
using namespace chrono;

void initialize(vector<vector<double>>& grid, int N) {
    #pragma omp parallel for
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            grid[i][j] = 0.0;

    for (int j = 0; j < N; j++)
        grid[0][j] = 100.0;  // top boundary = 100
}

void laplace_solve(vector<vector<double>>& grid, int N, int epochs) {
    vector<vector<double>> new_grid(N, vector<double>(N, 0.0));

    for (int j = 0; j < N; j++)
        new_grid[0][j] = 100.0;

    for (int epoch = 0; epoch < epochs; epoch++) {
        #pragma omp parallel for schedule(static)
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                new_grid[i][j] = 0.25 * (grid[i-1][j] + grid[i+1][j] +
                                          grid[i][j-1] + grid[i][j+1]);
            }
        }
        swap(grid, new_grid);
    }
}

int main(int argc, char* argv[]) {
    int N       = (argc > 1) ? atoi(argv[1]) : 256;
    int epochs  = (argc > 2) ? atoi(argv[2]) : 1000;
    int threads = (argc > 3) ? atoi(argv[3]) : omp_get_max_threads();

    omp_set_num_threads(threads);

    vector<vector<double>> grid(N, vector<double>(N, 0.0));
    initialize(grid, N);

    auto start = high_resolution_clock::now();
    laplace_solve(grid, N, epochs);
    auto end   = high_resolution_clock::now();

    double elapsed = duration<double>(end - start).count();

    cout << "OpenMP | N=" << N << " epochs=" << epochs
         << " threads=" << threads
         << " | Time: " << elapsed << "s" << endl;
    cout << "Center value: " << grid[N/2][N/2] << endl;

    return 0;
}

