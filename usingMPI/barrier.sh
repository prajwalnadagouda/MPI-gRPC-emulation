mpicc barrier.c -o barrier.out
mpirun -np 3 ./barrier.out