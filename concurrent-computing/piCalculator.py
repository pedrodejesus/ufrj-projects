import math
import sys
from threading import Thread
from time import time

# Global variables
n = 1000000
N_THREADS = int(sys.argv[1])
pi_estimate = 0

# Main calculation class
class PiCalculator(Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid
        self.val = 0

    def run(self):
        for i in range(self.tid, n, N_THREADS):
            self.val += (-1) ** i / (2 * i + 1)

# Store the threads
threads = [PiCalculator(tid) for tid in range(N_THREADS)]

# Initiate the threads and compute time taken
start = time()
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

for thread in threads:
    pi_estimate += thread.val
final_time = time() - start

print("Estimated pi: " + str(4*pi_estimate))
print("math.pi: " + str(math.pi))
print("Time to calculate: " + str(final_time))

# Check if the difference between the real value of pi and the estimate is within a certain tolerance level
tolerance = 1e-6
difference = abs(math.pi - 4 * pi_estimate)
print("Difference: " + str(difference))

if difference <= tolerance:
    print("\nThe estimate is accurate within the tolerance level")
else:
    print("\nThe estimate is not accurate within the tolerance level")
