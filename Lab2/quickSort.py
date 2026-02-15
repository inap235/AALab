import time
import matplotlib.pyplot as plt
import random

def partition(arr, low, high):
    
    # choose the pivot
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    
    swap(arr, i + 1, high)
    return i + 1

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def quickSort(arr, low, high):
    if low < high:
        
        # pi is the partition return index of pivot
        pi = partition(arr, low, high)
        
        # recursion calls for smaller elements
        # and greater or equals elements
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def performance():
    """Performance testing for Quick Sort"""
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    quick_times = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== QUICK SORT PERFORMANCE O(n log n) average ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        quick_execs = []
        
        for i in range(repeats):
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            start = time.perf_counter()
            quickSort(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            quick_execs.append((end - start) * 1000)
        
        avg_time = sum(quick_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in quick_execs) + f"  {avg_time:>10.3f}"
        print(row)
        quick_times.append(avg_time)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(
        test_sizes,
        quick_times,
        marker="^",
        linestyle="-",
        color="green",
        label="Quick Sort O(n log n) avg",
        linewidth=2,
        markersize=8,
    )
    axes[0].set_title("Quick Sort: Linear Scale")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].plot(
        test_sizes,
        quick_times,
        marker="^",
        linestyle="-",
        color="green",
        label="Quick Sort O(n log n) avg",
        linewidth=2,
        markersize=8,
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_title("Quick Sort: Log Scale")
    axes[1].set_xlabel("Array Size (n) - Log Scale")
    axes[1].set_ylabel("Execution Time (ms) - Log Scale")
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance()