#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;
using namespace chrono;

void initialize(vector<vector<double>>& grid, int N) {
    // Boundary conditions: top=100, rest=0
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            grid[i][j] = 0.0;

    for (int j = 0; j < N; j++)
        grid[0][j] = 100.0;  // top boundary = 100
}

double laplace_solve(vector<vector<double>>& grid, int N, int epochs) {
    vector<vector<double>> new_grid(N, vector<double>(N, 0.0));

    // Keep boundaries fixed
    for (int j = 0; j < N; j++) {
        new_grid[0][j] = 100.0;
    }

    for (int epoch = 0; epoch < epochs; epoch++) {
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                new_grid[i][j] = 0.25 * (grid[i-1][j] + grid[i+1][j] +
                                          grid[i][j-1] + grid[i][j+1]);
            }
        }
        swap(grid, new_grid);
    }
    return 0.0;
}

int main(int argc, char* argv[]) {
    int N      = (argc > 1) ? atoi(argv[1]) : 256;
    int epochs = (argc > 2) ? atoi(argv[2]) : 1000;

    vector<vector<double>> grid(N, vector<double>(N, 0.0));
    initialize(grid, N);

    auto start = high_resolution_clock::now();
    laplace_solve(grid, N, epochs);
    auto end   = high_resolution_clock::now();

    double elapsed = duration<double>(end - start).count();

    cout << "Serial | N=" << N << " epochs=" << epochs
         << " | Time: " << elapsed << "s" << endl;

    // Print center value as correctness check
    cout << "Center value: " << grid[N/2][N/2] << endl;

    return 0;
}
