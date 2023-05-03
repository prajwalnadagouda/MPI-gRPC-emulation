// Online C compiler to run C program online
#include <stdio.h>

int main() {
    int size=9;
    int rank=0;
    int mask;
    while(rank<size){
        int adjsize=16;
        adjsize >>=1;
        int remote;
        
        if (adjsize != size) {
            if (rank >= adjsize) {
                /* send message to lower ranked node */
                remote = rank - adjsize;
                printf("*%d-%d\n",rank,remote);


            } else if (rank < (size - adjsize)) {
                // printf("%d-%d\n",rank,remote);
                printf("\n");

            }
        }

        /* exchange messages */
        if ( rank < adjsize ) {
            mask = 0x1;
            while ( mask < adjsize ) {
                remote = rank ^ mask;
                mask <<= 1;
                if (remote >= adjsize) continue;
                printf("%d-%d\n",rank,remote);

            }
        }

    /* non-power of 2 case */
        if (adjsize != size) {
            if (rank < (size - adjsize)) {
                /* send enter message to higher ranked node */
                remote = rank + adjsize;
                // printf("%d-%d\n",rank,remote);
                printf("\n");
                }
        }

        rank++;
        printf("\n");
    }
    return 0;
}