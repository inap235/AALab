import time
import matplotlib.pyplot as plt
import random

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    # Create temp arrays
    L = [0] * n1
    R = [0] * n2

    # Copy data to temp arrays L[] and R[]
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
        
    i = 0  
    j = 0  
    k = left  

    # Merge the temp arrays back
    # into arr[left..right]
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[],
    # if there are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], 
    # if there are any
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


def performance():
    """Performance testing for Merge Sort"""
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3
    
    merge_times = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== MERGE SORT PERFORMANCE O(n log n) ===")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        merge_execs = []
        
        for _ in range(repeats):
            # Generate random array
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            start = time.perf_counter()
            mergeSort(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            merge_execs.append((end - start) * 1000)
        
        avg_time = sum(merge_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in merge_execs) + f"  {avg_time:>10.3f}"
        print(row)
        merge_times.append(avg_time)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(
        test_sizes,
        merge_times,
        marker="s",
        linestyle="-",
        color="blue",
        label="Merge Sort O(n log n)",
        linewidth=2,
        markersize=8,
    )
    axes[0].set_title("Merge Sort: Linear Scale")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].plot(
        test_sizes,
        merge_times,
        marker="s",
        linestyle="-",
        color="blue",
        label="Merge Sort O(n log n)",
        linewidth=2,
        markersize=8,
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_title("Merge Sort: Log Scale")
    axes[1].set_xlabel("Array Size (n) - Log Scale")
    axes[1].set_ylabel("Execution Time (ms) - Log Scale")
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance()