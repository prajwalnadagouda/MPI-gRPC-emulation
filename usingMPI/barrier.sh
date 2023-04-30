mpicc barrier.c -o barrier.out
mpirun -np 4 ./barrier.out