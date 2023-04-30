g++ -o barrier.out barrier.cpp -fopenmp
OMP_NUM_THREADS=4 ./barrier.out