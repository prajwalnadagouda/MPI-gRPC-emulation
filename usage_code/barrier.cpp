#include <stdio.h>
#include <omp.h>

int main(int argc, char** argv){
    int i;
    int thread_id;

    #pragma omp parallel 
    {
        int thread_id = omp_get_thread_num();
        for(int i = 0; i < omp_get_max_threads();    i++){
            if(i == omp_get_thread_num()){
                printf("Hello before barrier from process: %d\n", thread_id);
            }
            #pragma omp barrier

        }
        printf("Hello after barrier from process: %d\n", thread_id);
    }
    return 0;
}