import time
import matplotlib.pyplot as plt
import random

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
        
    i = 0  
    j = 0  
    k = left  

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        mergeSort(arr, left, mid)
        mergeSort(arr, mid + 1, right)
        merge(arr, left, mid, right)

def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def mergeOptimized(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
    i = j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSortOptimized(arr, left, right, threshold=10):
    if right - left + 1 <= threshold:
        insertion_sort(arr, left, right)
    elif left < right:
        mid = (left + right) // 2
        mergeSortOptimized(arr, left, mid, threshold)
        mergeSortOptimized(arr, mid + 1, right, threshold)
        mergeOptimized(arr, left, mid, right)


def performance():
    """Performance testing for Merge Sort - Original vs Optimized"""
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    merge_times = []
    merge_times_opt = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== MERGE SORT PERFORMANCE - ORIGINAL O(n log n) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        merge_execs = []
        for _ in range(repeats):
            arr = [random.randint(1, 10000) for _ in range(size)]
            start = time.perf_counter()
            mergeSort(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            merge_execs.append((end - start) * 1000)
        
        avg_time = sum(merge_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in merge_execs) + f"  {avg_time:>10.3f}"
        print(row)
        merge_times.append(avg_time)
    
    print("\n=== MERGE SORT PERFORMANCE - OPTIMIZED (Adaptive + Insertion Sort) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        merge_execs_opt = []
        for _ in range(repeats):
            arr = [random.randint(1, 10000) for _ in range(size)]
            start = time.perf_counter()
            mergeSortOptimized(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            merge_execs_opt.append((end - start) * 1000)
        
        avg_time = sum(merge_execs_opt) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in merge_execs_opt) + f"  {avg_time:>10.3f}"
        print(row)
        merge_times_opt.append(avg_time)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_sizes, merge_times, marker="s", linestyle="-", color="blue",
        label="Original Merge Sort", linewidth=2, markersize=8)
    axes[0].set_title("Merge Sort: Original")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(test_sizes, merge_times, marker="s", linestyle="-", color="blue",
        label="Original Merge Sort", linewidth=2, markersize=8)
    axes[1].plot(test_sizes, merge_times_opt, marker="^", linestyle="--", color="cyan",
        label="Optimized (Adaptive)", linewidth=2, markersize=8)
    axes[1].set_title("Merge Sort: Original vs Optimized")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Execution Time (ms)")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()
    
    print("\n=== OPTIMIZATION IMPROVEMENT ===")
    for i, size in enumerate(test_sizes):
        improvement = ((merge_times[i] - merge_times_opt[i]) / merge_times[i]) * 100
        print(f"Size {size}: {improvement:+.2f}% improvement")


if __name__ == "__main__":
    performance()