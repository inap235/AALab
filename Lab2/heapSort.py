import time
import matplotlib.pyplot as plt
import random

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def heapify_iterative(arr, n, i):
    temp = arr[i]
    while True:
        l = 2 * i + 1
        r = l + 1
        if l >= n:
            break
        child = l
        if r < n and arr[r] > arr[l]:
            child = r
        if arr[child] <= temp:
            break
        arr[i] = arr[child]
        i = child
    arr[i] = temp

def heapSortOptimized(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify_iterative(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_iterative(arr, i, 0)


def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    heap_times = []
    heap_times_opt = []
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== HEAP SORT PERFORMANCE - ORIGINAL O(n log n) ===")
    print(header)
    print("-" * len(header))
    datasets = {
        size: [[random.randint(1, 10000) for _ in range(size)] for _ in range(repeats)]
        for size in test_sizes
    }
    for size in test_sizes:
        heap_execs = []
        for run in range(repeats):
            arr = datasets[size][run].copy()
            start = time.perf_counter()
            heapSort(arr)
            end = time.perf_counter()
            heap_execs.append((end - start) * 1000)
        avg_time = sum(heap_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in heap_execs) + f"  {avg_time:>10.3f}"
        print(row)
        heap_times.append(avg_time)
    print("\n=== HEAP SORT PERFORMANCE - OPTIMIZED (Iterative Heapify) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        heap_execs_opt = []
        for run in range(repeats):
            arr = datasets[size][run].copy()
            start = time.perf_counter()
            heapSortOptimized(arr)
            end = time.perf_counter()
            heap_execs_opt.append((end - start) * 1000)
        
        avg_time = sum(heap_execs_opt) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in heap_execs_opt) + f"  {avg_time:>10.3f}"
        print(row)
        heap_times_opt.append(avg_time)
    
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(test_sizes, heap_times, marker="o", linestyle="-", color="purple", 
        label="Original Heap Sort", linewidth=2, markersize=8)
    ax.plot(test_sizes, heap_times_opt, marker="s", linestyle="--", color="orange",
        label="Optimized (Iterative)", linewidth=2, markersize=8)
    ax.set_title("Heap Sort: Linear Scale")
    ax.set_xlabel("Array Size (n)")
    ax.set_ylabel("Execution Time (ms)")
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\n=== OPTIMIZATION IMPROVEMENT ===")
    for i, size in enumerate(test_sizes):
        improvement = ((heap_times[i] - heap_times_opt[i]) / heap_times[i]) * 100
        print(f"Size {size}: {improvement:+.2f}% improvement")


if __name__ == "__main__":
    performance()