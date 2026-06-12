cmake_minimum_required(VERSION 3.10)
project(LaplaceHPC)

set(CMAKE_CXX_STANDARD 11)

add_executable(laplace_serial src/laplace_serial.cpp)
target_compile_options(laplace_serial PRIVATE -O2)

find_package(OpenMP REQUIRED)
add_executable(laplace_openmp src/laplace_openmp.cpp)
target_compile_options(laplace_openmp PRIVATE -O2)
target_link_libraries(laplace_openmp OpenMP::OpenMP_CXX)

find_package(MPI REQUIRED)
add_executable(laplace_mpi src/laplace_mpi.cpp)
target_compile_options(laplace_mpi PRIVATE -O2)
target_include_directories(laplace_mpi PRIVATE ${MPI_CXX_INCLUDE_DIRS})
target_link_libraries(laplace_mpi ${MPI_CXX_LIBRARIES})
