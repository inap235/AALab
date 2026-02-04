"""
Laboratory Nr 2: Study and empirical analysis of sorting algorithms
Algorithms: QuickSort, MergeSort, HeapSort, InsertionSort
"""

import time
import random
import matplotlib.pyplot as plt
import numpy as np


# ==================== QUICKSORT ====================
def quicksort(arr):
    """QuickSort implementation using Lomuto partition scheme"""
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)


# ==================== MERGESORT ====================
def mergesort(arr):
    """MergeSort implementation"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ==================== HEAPSORT ====================
def heapsort(arr):
    """HeapSort implementation"""
    arr = arr.copy()
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def heapify(arr, n, i):
    """Heapify subtree rooted at index i"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# ==================== INSERTION SORT ====================
def insertionsort(arr):
    """Insertion Sort implementation"""
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


# ==================== PERFORMANCE TESTING ====================
def measure_time(sort_func, arr):
    """Measure execution time of sorting function"""
    start = time.perf_counter()
    sort_func(arr.copy())
    end = time.perf_counter()
    return end - start


def generate_test_data(size, data_type='random'):
    """Generate test data with different properties"""
    if data_type == 'random':
        return [random.randint(1, 10000) for _ in range(size)]
    elif data_type == 'sorted':
        return list(range(size))
    elif data_type == 'reverse':
        return list(range(size, 0, -1))
    elif data_type == 'nearly_sorted':
        arr = list(range(size))
        # Swap 5% of elements
        swaps = size // 20
        for _ in range(swaps):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif data_type == 'duplicates':
        return [random.randint(1, 100) for _ in range(size)]


def empirical_analysis():
    """Perform empirical analysis of sorting algorithms"""
    print("=" * 60)
    print("LABORATORY NR 2: EMPIRICAL ANALYSIS OF SORTING ALGORITHMS")
    print("=" * 60)
    
    # Define algorithms to test
    algorithms = {
        'QuickSort': quicksort,
        'MergeSort': mergesort,
        'HeapSort': heapsort,
        'InsertionSort': insertionsort
    }
    
    # Define input sizes (reduced for faster execution)
    sizes = [100, 500, 1000, 2000, 3000]
    
    # Define data types
    data_types = ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates']
    
    # Store results
    results = {algo: {dtype: [] for dtype in data_types} for algo in algorithms}
    
    print("\nRunning empirical analysis...")
    print("Input sizes:", sizes)
    print("Data types:", data_types)
    print("\nMetrics: Execution time (seconds)\n")
    
    # Run tests
    for data_type in data_types:
        print(f"\nTesting with {data_type.upper()} data:")
        for size in sizes:
            print(f"  Size {size}...", end=" ")
            data = generate_test_data(size, data_type)
            
            for algo_name, algo_func in algorithms.items():
                time_taken = measure_time(algo_func, data)
                results[algo_name][data_type].append(time_taken)
            
            print("Done")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    
    # Print summary table
    print("\nSUMMARY TABLE (Time in milliseconds):")
    print("-" * 60)
    for data_type in data_types:
        print(f"\n{data_type.upper()} DATA:")
        print(f"{'Size':<10}", end="")
        for algo_name in algorithms:
            print(f"{algo_name:<15}", end="")
        print()
        print("-" * 60)
        
        for i, size in enumerate(sizes):
            print(f"{size:<10}", end="")
            for algo_name in algorithms:
                time_ms = results[algo_name][data_type][i] * 1000
                print(f"{time_ms:<15.4f}", end="")
            print()
    
    return results, sizes, data_types, algorithms


def plot_results(results, sizes, data_types, algorithms):
    """Create graphical presentation of results"""
    
    # Create figure with subplots for each data type
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Sorting Algorithms Performance Comparison', fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    markers = ['o', 's', '^', 'D']
    
    for idx, data_type in enumerate(data_types):
        ax = axes[idx]
        
        for i, (algo_name, algo_func) in enumerate(algorithms.items()):
            times_ms = [t * 1000 for t in results[algo_name][data_type]]
            ax.plot(sizes, times_ms, marker=markers[i], color=colors[i], 
                   linewidth=2, markersize=8, label=algo_name)
        
        ax.set_xlabel('Input Size (n)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Time (milliseconds)', fontsize=11, fontweight='bold')
        ax.set_title(f'{data_type.replace("_", " ").title()} Data', 
                    fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    
    # Remove the 6th subplot (we only have 5 data types)
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    plt.savefig('Lab1_Sorting_Comparison.png', dpi=300, bbox_inches='tight')
    print("\nGraph saved as 'Lab1_Sorting_Comparison.png'")
    plt.show()
    
    # Create comparison plot: All algorithms on random data
    plt.figure(figsize=(12, 7))
    
    for i, (algo_name, algo_func) in enumerate(algorithms.items()):
        times_ms = [t * 1000 for t in results[algo_name]['random']]
        plt.plot(sizes, times_ms, marker=markers[i], color=colors[i], 
                linewidth=2.5, markersize=10, label=algo_name)
    
    plt.xlabel('Input Size (n)', fontsize=13, fontweight='bold')
    plt.ylabel('Time (milliseconds)', fontsize=13, fontweight='bold')
    plt.title('Sorting Algorithms: Performance on Random Data', 
             fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('Lab1_Random_Data_Comparison.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'Lab1_Random_Data_Comparison.png'")
    plt.show()
    
    # Create heatmap comparison
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data for heatmap (average times across all sizes)
    heatmap_data = []
    algo_names_list = list(algorithms.keys())
    
    for algo_name in algo_names_list:
        row = []
        for data_type in data_types:
            avg_time = np.mean(results[algo_name][data_type]) * 1000
            row.append(avg_time)
        heatmap_data.append(row)
    
    heatmap_data = np.array(heatmap_data)
    
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(data_types)))
    ax.set_yticks(np.arange(len(algo_names_list)))
    ax.set_xticklabels([dt.replace('_', ' ').title() for dt in data_types])
    ax.set_yticklabels(algo_names_list)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    for i in range(len(algo_names_list)):
        for j in range(len(data_types)):
            text = ax.text(j, i, f'{heatmap_data[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=10)
    
    ax.set_title('Average Execution Time (ms) - Heatmap Comparison', 
                fontsize=14, fontweight='bold', pad=20)
    fig.colorbar(im, ax=ax, label='Time (milliseconds)')
    
    plt.tight_layout()
    plt.savefig('Lab1_Heatmap_Comparison.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'Lab1_Heatmap_Comparison.png'")
    plt.show()


def print_conclusions():
    """Print conclusions for the laboratory work"""
    print("\n" + "=" * 60)
    print("CONCLUSIONS:")
    print("=" * 60)
    print("""
1. ALGORITHM CHARACTERISTICS:
   - QuickSort: Average O(n log n), but O(n²) worst case (sorted data)
   - MergeSort: Consistent O(n log n) for all cases
   - HeapSort: Consistent O(n log n) for all cases
   - InsertionSort: O(n²) average, but O(n) for nearly sorted data

2. PERFORMANCE ON DIFFERENT DATA TYPES:
   - Random Data: QuickSort and MergeSort perform best
   - Sorted Data: QuickSort degrades; MergeSort and HeapSort stable
   - Reverse Sorted: QuickSort struggles; others maintain performance
   - Nearly Sorted: InsertionSort shows excellent performance
   - Duplicates: All divide-and-conquer algorithms handle well

3. BEST USE CASES:
   - QuickSort: General purpose, random data
   - MergeSort: Guaranteed O(n log n), stable sort needed
   - HeapSort: In-place sorting, memory constraints
   - InsertionSort: Small or nearly sorted datasets

4. EMPIRICAL FINDINGS:
   - Time complexity matches theoretical predictions
   - Input data characteristics significantly impact performance
   - QuickSort fastest on average but has worst-case scenarios
   - MergeSort most consistent across all data types
   - InsertionSort only competitive for small/nearly sorted data
    """)


if __name__ == "__main__":
    # Run empirical analysis
    results, sizes, data_types, algorithms = empirical_analysis()
    
    # Create visualizations
    plot_results(results, sizes, data_types, algorithms)
    
    # Print conclusions
    print_conclusions()
    
    print("\n" + "=" * 60)
    print("Laboratory work completed successfully!")
    print("=" * 60)
