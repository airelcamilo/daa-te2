from memory_profiler import memory_usage
import time
"""
Airel Camilo Khairan
2106652581
Modified from: https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/
"""

# Dynamic Programming
def unboundedKnapsack(W, v, w): 
    # Kompleksitas: O(W*n)
    # dp[i] akan menyimpan maks value dengan kapasitas knapsack i
    dp = [0 for i in range(W + 1)] 
    n = len(w)

    # Mengisi dp[] 
    for i in range(W + 1): 
        for j in range(n): 
            if (w[j] <= i): 
                dp[i] = max(dp[i], dp[i - w[j]] + v[j])
    return dp[W] 

if __name__ == '__main__':
    with open("dataset.txt", "r") as file:
        for _ in range(3):
            n, _ = file.readline().split(" ")
            w = [int(num) for num in file.readline().split(" ")]
            v = [int(num) for num in file.readline().split(" ")]
            W = int(0.1 * sum(w))
            print(f"Ukuran {n}")
            print(f"Weight knapsack : {W}")

            memory_before = memory_usage()[0]
            start_time = time.perf_counter()

            res = unboundedKnapsack(W, v, w)
            print(f"Best value      : {res}")

            total_runtime = time.perf_counter() - start_time
            memory_used = memory_usage()[0] - memory_before
            
            print(f"Total runtime   : {(total_runtime):.4f}s")
            print(f"Memory usage    : {(memory_used * 1024):.4f}KiB\n")