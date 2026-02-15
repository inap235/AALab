import time
import matplotlib.pyplot as plt
import random

def slowsort(arr, i, j):
    if i >= j:
        return  # Base case: single element or invalid range

    mid = (i + j) // 2
    slowsort(arr, i, mid)  # Recursively sort the left half
    slowsort(arr, mid + 1, j)  # Recursively sort the right half

    # Place the maximum element at the end
    if arr[mid] > arr[j]:
        arr[mid], arr[j] = arr[j], arr[mid]

    # Recurse one last time on the full segment
    slowsort(arr, i, j - 1)

def performance():
    """Performance testing for Slow Sort - use small sizes only!"""
    test_sizes = [5, 10, 15, 20, 25, 30]  # Much smaller sizes for this slow algorithm
    repeats = 3
    
    slow_times = []
    
    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\n=== SLOW SORT PERFORMANCE (multiply-and-surrender paradigm) ===")
    print("WARNING: This algorithm is intentionally slow!")
    print(header)
    print("-" * len(header))
    
    for size in test_sizes:
        slow_execs = []
        
        for _ in range(repeats):
            # Generate random array
            arr = [random.randint(1, 100) for _ in range(size)]
            
            start = time.perf_counter()
            slowsort(arr, 0, len(arr) - 1)
            end = time.perf_counter()
            slow_execs.append((end - start) * 1000)
        
        avg_time = sum(slow_execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in slow_execs) + f"  {avg_time:>10.3f}"
        print(row)
        slow_times.append(avg_time)
    
    # Create plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linear scale
    axes[0].plot(
        test_sizes,
        slow_times,
        marker="o",
        linestyle="-",
        color="red",
        label="Slow Sort (worse than O(n²))",
        linewidth=2,
        markersize=8,
    )
    axes[0].set_title("Slow Sort: Linear Scale")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True)
    
    # Log scale
    axes[1].plot(
        test_sizes,
        slow_times,
        marker="o",
        linestyle="-",
        color="red",
        label="Slow Sort (worse than O(n²))",
        linewidth=2,
        markersize=8,
    )
    axes[1].set_yscale("log")
    axes[1].set_title("Slow Sort: Log Scale")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Execution Time (ms) - Log Scale")
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\n=== NOTES ===")
    print("Slow Sort: Intentionally inefficient - worse than O(n²)")
    print("Based on 'multiply and surrender' paradigm")
    print("Complexity: approximately O(n^(log n / (2 + ε)))")
    print("Not practical - used for educational/humorous purposes")


if __name__ == "__main__":
    performance()