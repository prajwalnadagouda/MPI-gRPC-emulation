#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    int rank, size, ierr;
    MPI_Request request;
    ierr=MPI_Init(&argc, &argv);
    ierr=MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    ierr=MPI_Comm_size(MPI_COMM_WORLD, &size);
    printf("Hello before ibarrier- Rank %d\n", rank);
    ierr=MPI_Ibarrier(MPI_COMM_WORLD, &request);
    MPI_Wait(&request, MPI_STATUS_IGNORE);
    printf("Hello after ibarrier- Rank %d\n", rank);
    ierr=MPI_Finalize();
    return 0;
}

