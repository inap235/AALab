import time
import matplotlib.pyplot as plt
import random
import numpy as np
from heapSort import heapSort as heap_sort
from mergeSort import mergeSort as merge_sort_func
from quickSort import quickSort as quick_sort_func
from slowSort import slowsort


def mergeSort(arr):
    merge_sort_func(arr, 0, len(arr) - 1)


def quickSort(arr):
    quick_sort_func(arr, 0, len(arr) - 1)


def slowSort(arr):
    slowsort(arr, 0, len(arr) - 1)


def heapSort(arr):
    heap_sort(arr)


def comprehensive_comparison():
    
    efficient_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    slow_sizes = [5, 10, 15, 20, 25, 30] 
    
    repeats = 3
    
    algorithms = {
        "Heap Sort": (heapSort, efficient_sizes),
        "Merge Sort": (mergeSort, efficient_sizes),
        "Quick Sort": (quickSort, efficient_sizes),
        "Slow Sort": (slowSort, slow_sizes),
    }
    
    results = {}
    print("\n" + "="*80)
    print("COMPREHENSIVE SORTING ALGORITHMS COMPARISON")
    print("="*80)
    for algo_name, (algo_func, test_sizes) in algorithms.items():
        print(f"\n=== {algo_name.upper()} ===")
        header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
        print(header)
        print("-" * len(header))
        algo_times = []
        for size in test_sizes:
            execs = []
            
            for i in range(repeats):
                arr = [random.randint(1, 10000) for _ in range(size)]
                
                start = time.perf_counter()
                algo_func(arr.copy())
                end = time.perf_counter()
                execs.append((end - start) * 1000)
            
            avg_time = sum(execs) / repeats
            row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in execs) + f"  {avg_time:>10.3f}"
            print(row)
            algo_times.append(avg_time)
        
        results[algo_name] = (test_sizes, algo_times)
    create_comparison_plots(results)
    


def create_comparison_plots(results):
    
    # Figure 1: Efficient algorithms comparison
    fig1, axes1 = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = {"Heap Sort": "purple", "Merge Sort": "blue", "Quick Sort": "green"}
    markers = {"Heap Sort": "o", "Merge Sort": "s", "Quick Sort": "^"}
    
    for algo_name in ["Heap Sort", "Merge Sort", "Quick Sort"]:
        if algo_name in results:
            sizes, times = results[algo_name]
            
            # Linear scale
            axes1[0].plot(
                sizes, times,
                marker=markers[algo_name],
                linestyle="-",
                color=colors[algo_name],
                label=algo_name,
                linewidth=2,
                markersize=8,
            )
            
            # Log scale
            axes1[1].plot(
                sizes, times,
                marker=markers[algo_name],
                linestyle="-",
                color=colors[algo_name],
                label=algo_name,
                linewidth=2,
                markersize=8,
            )
    
    axes1[0].set_title("Efficient Sorting Algorithms: Linear Scale", fontsize=14, fontweight='bold')
    axes1[0].set_xlabel("Array Size (n)", fontsize=12)
    axes1[0].set_ylabel("Execution Time (ms)", fontsize=12)
    axes1[0].legend(fontsize=11)
    axes1[0].grid(True, alpha=0.3)
    
    axes1[1].set_xscale("log")
    axes1[1].set_yscale("log")
    axes1[1].set_title("Efficient Sorting Algorithms: Log Scale", fontsize=14, fontweight='bold')
    axes1[1].set_xlabel("Array Size (n) - Log Scale", fontsize=12)
    axes1[1].set_ylabel("Execution Time (ms) - Log Scale", fontsize=12)
    axes1[1].legend(fontsize=11)
    axes1[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Lab2/images/comparison_efficient.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Figure 2: Slow sort comparison
    if "Slow Sort" in results:
        fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))
        
        slow_sizes, slow_times = results["Slow Sort"]
        
        # Linear scale
        axes2[0].plot(
            slow_sizes, slow_times,
            marker="o",
            linestyle="-",
            color="red",
            label="Slow Sort",
            linewidth=2,
            markersize=8,
        )
        axes2[0].set_title("Slow Sort Performance: Linear Scale", fontsize=14, fontweight='bold')
        axes2[0].set_xlabel("Array Size (n)", fontsize=12)
        axes2[0].set_ylabel("Execution Time (ms)", fontsize=12)
        axes2[0].legend(fontsize=11)
        axes2[0].grid(True, alpha=0.3)
        
        # Log scale
        axes2[1].plot(
            slow_sizes, slow_times,
            marker="o",
            linestyle="-",
            color="red",
            label="Slow Sort",
            linewidth=2,
            markersize=8,
        )
        axes2[1].set_yscale("log")
        axes2[1].set_title("Slow Sort Performance: Log Scale", fontsize=14, fontweight='bold')
        axes2[1].set_xlabel("Array Size (n)", fontsize=12)
        axes2[1].set_ylabel("Execution Time (ms) - Log Scale", fontsize=12)
        axes2[1].legend(fontsize=11)
        axes2[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('Lab2/images/comparison_slow.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Figure 3: All algorithms together (showing the dramatic difference)
    fig3, ax3 = plt.subplots(figsize=(12, 7))
    
    # Plot efficient algorithms on the same range as slow sort
    for algo_name in ["Heap Sort", "Merge Sort", "Quick Sort"]:
        if algo_name in results:
            sizes, times = results[algo_name]
            # Filter to show only the overlapping range with slow sort
            slow_sizes_set = set(results["Slow Sort"][0]) if "Slow Sort" in results else set()
            filtered_data = [(s, t) for s, t in zip(sizes, times) if s in slow_sizes_set]
            if filtered_data:
                filtered_sizes, filtered_times = zip(*filtered_data)
                ax3.plot(
                    filtered_sizes, filtered_times,
                    marker=markers[algo_name],
                    linestyle="-",
                    color=colors[algo_name],
                    label=f"{algo_name} O(n log n)",
                    linewidth=2,
                    markersize=8,
                )
    
    if "Slow Sort" in results:
        slow_sizes, slow_times = results["Slow Sort"]
        ax3.plot(
            slow_sizes, slow_times,
            marker="o",
            linestyle="-",
            color="red",
            label="Slow Sort O(n^(log n))",
            linewidth=3,
            markersize=10,
        )
    
    ax3.set_title("All Sorting Algorithms Comparison (Same Scale)", fontsize=14, fontweight='bold')
    ax3.set_xlabel("Array Size (n)", fontsize=12)
    ax3.set_ylabel("Execution Time (ms)", fontsize=12)
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Lab2/images/comparison_all.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    comprehensive_comparison()
