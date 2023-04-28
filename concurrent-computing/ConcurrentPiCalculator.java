// This program uses the Leibiniz series to calculate an aproximated pi value.
// It divides the n input of executions by the number of threads given.
// Doing so, each thread will calculate a portion of the series sum total.
// After all threads have finished, the main thread will sum up the results of each individual thread
// and multiply by 4.
// Finally, it will calculates the relative error between the computed value and the value of Math.PI and 
// prints out the results along with the time taken to complete the calculation.

import java.util.Scanner;

public class ConcurrentPiCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(); // number of iterations
        int numberOfThreads = scanner.nextInt(); // number of threads
        
        long startTime = System.currentTimeMillis();
        
        // Initiate the threads
        PiCalculatorThread[] threads = new PiCalculatorThread[numberOfThreads];
        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new PiCalculatorThread(n/numberOfThreads, i*(n/numberOfThreads));
            threads[i].start();
        }
        
        // Sums up the result of each individual thread
        double sum = 0.0;
        for (int i = 0; i < numberOfThreads; i++) {
            try {
                threads[i].join();
                sum += threads[i].getResult();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        
        // Multiply the sum result by four to follow the Leibiniz series formula
        double pi = 4.0 * sum;
        double relativeError = Math.abs(Math.PI-pi) / Math.PI;
        
        System.out.println("Computed pi: " + pi);
        System.out.println("Relative error: " + relativeError);
        System.out.println("Time taken: " + (System.currentTimeMillis() - startTime) + "ms");
    }
}

class PiCalculatorThread extends Thread {
    private final int n;
    private final int start;
    private double result;
    
    public PiCalculatorThread(int n, int start) {
        this.n = n;
        this.start = start;
    }
    
    public double getResult() {
        return result;
    }
    
    @Override
    public void run() {
        for (int i = start; i < start + n; i++) {
            result += (i % 2 == 0 ? 1 : -1) * 1.0 / (2 * i + 1);
        }
    }
}

