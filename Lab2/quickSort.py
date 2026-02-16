import time
import matplotlib.pyplot as plt
import random

def partition(arr, low, high):
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
        pi = partition(arr, low, high)
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)

def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def median_of_three(arr, low, high):
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        swap(arr, low, mid)
    if arr[low] > arr[high]:
        swap(arr, low, high)
    if arr[mid] > arr[high]:
        swap(arr, mid, high)
    swap(arr, mid, high)
    return high

def partitionOptimized(arr, low, high):
    median_of_three(arr, low, high)
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    
    swap(arr, i + 1, high)
    return i + 1

def quickSortOptimized(arr, low, high, threshold=16):
    while low < high:
        if high - low + 1 <= threshold:
            insertion_sort(arr, low, high)
            break
        
        pi = partitionOptimized(arr, low, high)
        
        if pi - low < high - pi:
            quickSortOptimized(arr, low, pi - 1, threshold)
            low = pi + 1
        else:
            quickSortOptimized(arr, pi + 1, high, threshold)
            high = pi - 1


def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    quick_times = []
    quick_times_opt = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== QUICK SORT PERFORMANCE - ORIGINAL O(n log n) average ===")
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
    
    print("\n=== QUICK SORT PERFORMANCE - OPTIMIZED (Median-of-Three + Insertion Sort) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        quick_execs_opt = []
        
        for i in range(repeats):
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            start = time.perf_counter()
            quickSortOptimized(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            quick_execs_opt.append((end - start) * 1000)
        
        avg_time = sum(quick_execs_opt) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in quick_execs_opt) + f"  {avg_time:>10.3f}"
        print(row)
        quick_times_opt.append(avg_time)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_sizes, quick_times, marker="^", linestyle="-", color="green",
        label="Original Quick Sort", linewidth=2, markersize=8)
    axes[0].set_title("Quick Sort: Original")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(test_sizes, quick_times, marker="^", linestyle="-", color="green",
        label="Original Quick Sort", linewidth=2, markersize=8)
    axes[1].plot(test_sizes, quick_times_opt, marker="D", linestyle="--", color="lime",
        label="Optimized (Median-of-Three)", linewidth=2, markersize=8)
    axes[1].set_title("Quick Sort: Original vs Optimized")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Execution Time (ms)")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()
    
    print("\n=== OPTIMIZATION IMPROVEMENT ===")
    for i, size in enumerate(test_sizes):
        improvement = ((quick_times[i] - quick_times_opt[i]) / quick_times[i]) * 100
        print(f"Size {size}: {improvement:+.2f}% improvement")


if __name__ == "__main__":
    performance()