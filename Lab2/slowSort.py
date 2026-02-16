import time
import matplotlib.pyplot as plt
import random

def slowsort(arr, i, j):
    if i >= j:
        return

    mid = (i + j) // 2
    slowsort(arr, i, mid)
    slowsort(arr, mid + 1, j)

    if arr[mid] > arr[j]:
        arr[mid], arr[j] = arr[j], arr[mid]

    slowsort(arr, i, j - 1)

def is_sorted(arr, i, j):
    for k in range(i, j):
        if arr[k] > arr[k + 1]:
            return False
    return True

def slowsortOptimized(arr, i, j):
    if i >= j:
        return
    
    if is_sorted(arr, i, j):
        return

    mid = (i + j) // 2
    slowsortOptimized(arr, i, mid)
    slowsortOptimized(arr, mid + 1, j)

    if arr[mid] > arr[j]:
        arr[mid], arr[j] = arr[j], arr[mid]

    slowsortOptimized(arr, i, j - 1)

def performance():
    test_sizes = [5, 10, 15, 20, 25, 30]
    repeats = 3
    
    slow_times = []
    slow_times_opt = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== SLOW SORT PERFORMANCE - ORIGINAL (multiply-and-surrender paradigm) ===")
    print("This algorithm is intentionally slow!")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        slow_execs = []
        
        for _ in range(repeats):
            arr = [random.randint(1, 100) for _ in range(size)]
            
            start = time.perf_counter()
            slowsort(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            slow_execs.append((end - start) * 1000)
        
        avg_time = sum(slow_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in slow_execs) + f"  {avg_time:>10.3f}"
        print(row)
        slow_times.append(avg_time)
    
    print("\n=== SLOW SORT PERFORMANCE - OPTIMIZED (Early Termination) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        slow_execs_opt = []
        
        for _ in range(repeats):
            arr = [random.randint(1, 100) for _ in range(size)]
            
            start = time.perf_counter()
            slowsortOptimized(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            slow_execs_opt.append((end - start) * 1000)
        
        avg_time = sum(slow_execs_opt) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in slow_execs_opt) + f"  {avg_time:>10.3f}"
        print(row)
        slow_times_opt.append(avg_time)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_sizes, slow_times, marker="o", linestyle="-", color="red",
        label="Original Slow Sort", linewidth=2, markersize=8)
    axes[0].set_title("Slow Sort: Original")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(test_sizes, slow_times, marker="o", linestyle="-", color="red",
        label="Original Slow Sort", linewidth=2, markersize=8)
    axes[1].plot(test_sizes, slow_times_opt, marker="v", linestyle="--", color="darkred",
        label="Optimized (Early Termination)", linewidth=2, markersize=8)
    axes[1].set_title("Slow Sort: Original vs Optimized")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Execution Time (ms)")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()
    
    print("\n=== OPTIMIZATION IMPROVEMENT ===")
    for i, size in enumerate(test_sizes):
        improvement = ((slow_times[i] - slow_times_opt[i]) / slow_times[i]) * 100 if slow_times[i] > 0 else 0
        print(f"Size {size}: {improvement:+.2f}% improvement")

if __name__ == "__main__":
    performance()