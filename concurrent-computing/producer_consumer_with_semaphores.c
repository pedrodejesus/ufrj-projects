// The program implements the producer-consumer pattern with the following modification: during an insertion, 
// the producers fill the buffer completely (assuming the buffer is initially empty). The logic for the 
// consumers remains the same. The program uses semaphores to handle all synchronization requirements of the 
// problem, minimizing the associated costs.

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

// Buffer size, number of producers and number of consumers
#define BUFFER_SIZE 10
#define N_PRODUCERS 2
#define N_CONSUMERS 2

// Semaphores for full and empty slots and mutexes for producers and consumers. Buffer initialization.
sem_t fullSlot, emptySlot;
sem_t mutexProd, mutexCons;
int Buffer[BUFFER_SIZE];

void Insert(int item) {
    // Wait for empty slots before inserting
    sem_wait(&emptySlot);

    // Mutex between producers
    sem_wait(&mutexProd);
    for (int i = 0; i < BUFFER_SIZE; i++) {
      Buffer[i] = item;
      printf("Produtor inseriu o item %d no índice %d do buffer\n", item, i);
    }
    sem_post(&mutexProd);

    // Singal all slots as full after inserting
    for (int i = 0; i < BUFFER_SIZE; i++) sem_post(&fullSlot);
}

int Remove() {
    int item;
    static int out = 0;

    // Wait for full slots before retirar
    sem_wait(&fullSlot);

    // Mutex between consumers
    sem_wait(&mutexCons);
    item = Buffer[out];
    printf("Consumidor retirou o item %d do índice %d do buffer\n", item, out);
    out = (out + 1) % BUFFER_SIZE;

    // Signal all slots as empty after retirar
    if (out == 0) {
        sem_post(&emptySlot);
    }

    sem_post(&mutexCons);

    return item;
}

// Fills the buffer with equal items
void *producer(void *arg) {
    int item = 1;
    while (1) {
        Insert(item);
        item++;
    }
    pthread_exit(NULL);
}

// Consume an item
void *consumer(void *arg) {
    int item;
    while (1) {
        item = Remove();
    }
    pthread_exit(NULL);
}

int main() {
    // Initialize semaphores and mutexes
    sem_init(&mutexCons, 0, 1);
    sem_init(&mutexProd, 0, 1);
    sem_init(&fullSlot, 0, 0);
    sem_init(&emptySlot, 0, BUFFER_SIZE);

    // Initialize threads
    pthread_t producers[N_PRODUCERS];
    pthread_t consumers[N_CONSUMERS];

    // Create the threads of the producers
    for (int i = 0; i < N_PRODUCERS; i++) {
        pthread_create(&producers[i], NULL, producer, NULL);
    }

    // Create the threads of the consumers
    for (int i = 0; i < N_CONSUMERS; i++) {
        pthread_create(&consumers[i], NULL, consumer, NULL);
    }

    // Await the threads of the producers
    for (int i = 0; i < N_PRODUCERS; i++) {
        pthread_join(producers[i], NULL);
    }

    // Await the threads of the consumers
    for (int i = 0; i < N_CONSUMERS; i++) {
        pthread_join(consumers[i], NULL);
    }

    return 0;
}
