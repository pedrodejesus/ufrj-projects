// This script multiplies all elements of a vector of size VECTOR_SIZE by 2 
// concurrently. It creates two threads and assigns half of the vector to each
// thread for processing. Finally, it verifies the correctness of the 
// multiplication for all elements in the vector.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

#define VECTOR_SIZE 10000
int vector[VECTOR_SIZE];

// Multiply all elements of the vector by 2, assigning the first half of it to
// the first thread, and the second half to the second thread.
void *multiply_elements(void *thread_id) {
  int start, end;

  switch((long) thread_id){
    case 0:
      start = 0; end = VECTOR_SIZE/2;
      break;
    case 1:
      start = VECTOR_SIZE/2; end = VECTOR_SIZE;
  }

  for (int i = start; i < end; i++) {
    vector[i] *= 2;
  }

  pthread_exit(NULL);
}

int main() {
  pthread_t threads[2];

  // Initialize the vector with random numbers between 0 and 1000.
  // Uses the current time as the seed for the srand function.
	srand(time(NULL));
  for(int i = 0; i < VECTOR_SIZE; i++) {
    vector[i] = rand() % 1000;
  }

  // Creates 2 threads to multiply the elements
  for (long tid = 0; tid < 2; tid++) {
    pthread_create(&threads[tid], NULL, multiply_elements, (void*) tid);
  }

  // Join the created threads
  for (long tid = 0; tid < 2; tid++) {
    pthread_join(threads[tid], NULL);
  }

  // Checks the correctness of the multiplication across all of the vector
  for (int i = 0; i < VECTOR_SIZE; i++) {
    if (vector[i] % 2 != 0) {
      printf("Error during multiplication!\n");
      exit(0);
    }
  }
  printf("Multiplication finished correctly!\n");
}

