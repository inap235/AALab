import time
import matplotlib.pyplot as plt

def fibonacci_fast_doubling(n):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    
    def fib_doubling(k):
        if k == 0:
            return (0, 1)
        f_m, f_m1 = fib_doubling(k // 2)
        c = f_m * (2 * f_m1 - f_m)
        d = f_m * f_m + f_m1 * f_m1
        
        if k % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)
    
    return fib_doubling(n)[0]


def fibonacci_iterative(n):
    """Iterative Fibonacci - O(n) time, O(1) space"""
    if n == 0:
        return 0
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def performance():
    test_numbers = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    fast_doubling_times = []
    iterative_times = []
    
    header = "n     " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    
    print("Fast Doubling O(log n)")
    print(header)
    print("-" * len(header))
    
    for number in test_numbers:
        execs = []
        
        for _ in range(repeats):
            start = time.perf_counter()
            fibonacci_fast_doubling(number)
            end = time.perf_counter()
            execs.append((end - start) * 1000)
        
        avg_time = sum(execs) / repeats
        row = f"{number:<6} " + "  ".join(f"{t:>8.3f}" for t in execs) + f"  {avg_time:>8.3f}"
        print(row)
        fast_doubling_times.append(avg_time)
    
    print("\nIterative O(n)")
    print(header)
    print("-" * len(header))
    
    for number in test_numbers:
        execs = []
        
        for _ in range(repeats):
            start = time.perf_counter()
            fibonacci_iterative(number)
            end = time.perf_counter()
            execs.append((end - start) * 1000)
        
        avg_time = sum(execs) / repeats
        row = f"{number:<6} " + "  ".join(f"{t:>8.3f}" for t in execs) + f"  {avg_time:>8.3f}"
        print(row)
        iterative_times.append(avg_time)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(
        test_numbers,
        fast_doubling_times,
        marker="o",
        linestyle="-",
        color="r",
        label="Fast Doubling O(log n)",
    )
    plt.plot(
        test_numbers,
        iterative_times,
        marker="s",
        linestyle="-",
        color="b",
        label="Iterative O(n)",
    )
    plt.title("Fibonacci Performance Comparison (Average of 3 runs)")
    plt.xlabel("n")
    plt.ylabel("Execution Time (ms)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()
