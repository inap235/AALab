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


def performance():
    """Performance testing for Heap Sort"""
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    heap_times = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== HEAP SORT PERFORMANCE O(n log n) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        heap_execs = []
        
        for _ in range(repeats):
            # Generate random array
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            start = time.perf_counter()
            heapSort(arr)
            end = time.perf_counter()
            heap_execs.append((end - start) * 1000)
        
        avg_time = sum(heap_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in heap_execs) + f"  {avg_time:>10.3f}"
        print(row)
        heap_times.append(avg_time)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(       test_sizes,
        heap_times,
        marker="o",
        linestyle="-",
        color="purple",
        label="Heap Sort O(n log n)",
        linewidth=2,
        markersize=8,
    )
    axes[0].set_title("Heap Sort: Linear Scale")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)
    
    # Log scale
    axes[1].plot(
        test_sizes,
        heap_times,
        marker="o",
        linestyle="-",
        color="purple",
        label="Heap Sort O(n log n)",
        linewidth=2,
        markersize=8,
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_title("Heap Sort: Log Scale")
    axes[1].set_xlabel("Array Size (n) - Log Scale")
    axes[1].set_ylabel("Execution Time (ms) - Log Scale")
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\n=== NOTES ===")
    print("Heap Sort: O(n log n) time complexity - efficient for large datasets")
    print("Space Complexity: O(1) - sorts in place")
    print("Not stable but guarantees O(n log n) in worst case")


if __name__ == "__main__":
    performance()