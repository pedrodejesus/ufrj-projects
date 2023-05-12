// The goal of this program is to demonstrate the use of conditional sync
// between threads using shared variables. It works in the following way:
// threads 1 and 2 say hello to John and Mary, in any order, but they must do
// it before the message telling them to sit is printed. The thread 3 prints
// the sit message. Then, only after it, the 2 bye messages can be printed in
// any order.
// To do so, we will make use of some resources of the pthred library in c,
// including: mutex locks, thread conditions, condition signals and broadcast.

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define N_THREADS 5

int n_arrived = 0;
bool sat = false;
pthread_mutex_t lock;
pthread_cond_t arrived;
pthread_cond_t seated;

void *hello(void *arg) {
  // Hello {name}!
  char* name = (char*) arg;
  printf("Oi %s!\n", name);
 
  // Locks the thread to modify the shared variables
  pthread_mutex_lock(&lock);
 
  // Increments arrived and checks if both of them already arrived
  n_arrived++;
  if(n_arrived == 2) {
    pthread_cond_signal(&arrived);
  }
  
  // Unlocks and exit the thread
  pthread_mutex_unlock(&lock);
  pthread_exit(NULL);
}

void *sit(void *arg) {
  // Locks the thread and wait for them to arrive
  pthread_mutex_lock(&lock);
  while (n_arrived != 2) {
    pthread_cond_wait(&arrived, &lock);
  }
  
  // Tell them to sit and notify via broadcast the seated condition
  printf("Sentem-se por favor.\n");
  sat = true;
  pthread_cond_broadcast(&seated);
  
  // Unlocks and exit the thread
  pthread_mutex_unlock(&lock);
  pthread_exit(NULL);
}

void *bye(void *arg){
  // Locks the thread, wait for them to me seated and them unlocks the thread
  pthread_mutex_lock(&lock);
  while (n_arrived != 2 && sat == false) {
    pthread_cond_wait(&seated, &lock);
  }

  // Bye {name}!
  char* name = (char*) arg;
  printf("Até Mais %s!\n", name);

  // Unlocks and exit the thread
  pthread_mutex_unlock(&lock);
  pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
  pthread_t threads[N_THREADS];
  
  // Initializes the mutex lock and the sync conditions
  pthread_mutex_init(&lock, NULL);
  pthread_cond_init (&arrived, NULL);
  pthread_cond_init (&seated, NULL);

  char* mary = "Maria";
  char* john = "João";

  // Initializes all threads
  pthread_create(&threads[0], NULL, hello, (void*) mary);
  pthread_create(&threads[1], NULL, hello, (void*) john);
  pthread_create(&threads[2], NULL, sit, NULL);
  pthread_create(&threads[3], NULL, bye, (void*) john);
  pthread_create(&threads[4], NULL, bye, (void*) mary);

  // Join the created threads
  for (int i = 0; i < N_THREADS; i++) {
    pthread_join(threads[i], NULL);
  }
  
  // Destry the lock and the sync variables
  pthread_mutex_destroy(&lock);
  pthread_cond_destroy(&arrived);
  pthread_cond_destroy(&seated);

  return 0;
}

