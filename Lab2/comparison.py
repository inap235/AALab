import time
import matplotlib.pyplot as plt
import random
import sys
from pathlib import Path
from heapSort import heapSort as heap_sort
from mergeSort import mergeSort as merge_sort_func
from quickSort import quickSort as quick_sort_func
from slowSort import slowsort

sys.setrecursionlimit(50000)

IMAGE_DIR = Path(__file__).parent / "images"
IMAGE_DIR.mkdir(exist_ok=True)


# ── wrappers ──────────────────────────────────────────────────────────────────
def mergeSort(arr):
    merge_sort_func(arr, 0, len(arr) - 1)

def quickSort(arr):
    quick_sort_func(arr, 0, len(arr) - 1)

def slowSort(arr):
    slowsort(arr, 0, len(arr) - 1)

def heapSort(arr):
    heap_sort(arr)


# ── input generators ─────────────────────────────────────────────────────────
def gen_random_integers(n):
    return [random.randint(1, 10_000) for _ in range(n)]

def gen_sorted_ascending(n):
    return list(range(1, n + 1))

def gen_sorted_descending(n):
    return list(range(n, 0, -1))

def gen_negative_numbers(n):
    return [random.randint(-10_000, -1) for _ in range(n)]

def gen_floating_point(n):
    return [random.uniform(-1000.0, 1000.0) for _ in range(n)]

def gen_complex_magnitudes(n):
    return [abs(complex(random.uniform(-100, 100), random.uniform(-100, 100)))
            for _ in range(n)]

def gen_nearly_sorted(n):
    arr = list(range(1, n + 1))
    swaps = max(1, n // 20)         
    for _ in range(swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def gen_many_duplicates(n):
    return [random.randint(1, 10) for _ in range(n)]


INPUT_TYPES = {
    "Random Integers":      gen_random_integers,
    "Sorted Ascending":     gen_sorted_ascending,
    "Sorted Descending":    gen_sorted_descending,
    "Negative Numbers":     gen_negative_numbers,
    "Floating Point":       gen_floating_point,
    "Complex (Magnitude)":  gen_complex_magnitudes,
    "Nearly Sorted":        gen_nearly_sorted,
    "Many Duplicates":      gen_many_duplicates,
}

EFFICIENT_ALGOS = {
    "Heap Sort":  heapSort,
    "Merge Sort": mergeSort,
    "Quick Sort": quickSort,
}

COLORS  = {"Heap Sort": "purple", "Merge Sort": "blue",
           "Quick Sort": "green",  "Slow Sort": "red"}
MARKERS = {"Heap Sort": "o", "Merge Sort": "s",
           "Quick Sort": "^", "Slow Sort": "v"}


# ── benchmarking ──────────────────────────────────────────────────────────────
def benchmark(algo_func, generator, sizes, repeats=3):
    """Return list of avg times (ms) per size. None if RecursionError."""
    times = []
    for size in sizes:
        execs = []
        for _ in range(repeats):
            arr = generator(size)
            try:
                start = time.perf_counter()
                algo_func(arr.copy())
                end = time.perf_counter()
                execs.append((end - start) * 1000)
            except RecursionError:
                execs.append(None)
        valid = [e for e in execs if e is not None]
        times.append(sum(valid) / len(valid) if valid else None)
    return times


def comprehensive_comparison():
    efficient_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    slow_sizes      = [5, 10, 15, 20, 25, 30]
    repeats = 3

    all_results = {}   # {input_name: {algo_name: (sizes, times)}}

    print("\n" + "=" * 80)
    print("COMPREHENSIVE SORTING ALGORITHMS COMPARISON")
    print("=" * 80)

    for input_name, generator in INPUT_TYPES.items():
        print(f"\n{'─' * 60}")
        print(f"  INPUT: {input_name}")
        print(f"{'─' * 60}")
        input_results = {}

        # efficient algorithms
        for algo_name, algo_func in EFFICIENT_ALGOS.items():
            times = benchmark(algo_func, generator, efficient_sizes, repeats)
            input_results[algo_name] = (efficient_sizes, times)
            print(f"  {algo_name:<12}  " +
                  "  ".join(f"{t:>8.3f}" if t is not None else "   ERROR"
                            for t in times))

        # slow sort
        times = benchmark(slowSort, generator, slow_sizes, repeats)
        input_results["Slow Sort"] = (slow_sizes, times)
        print(f"  {'Slow Sort':<12}  " +
              "  ".join(f"{t:>8.3f}" if t is not None else "   ERROR"
                        for t in times))

        all_results[input_name] = input_results

    # ── plots ─────────────────────────────────────────────────────────────────

    # Figure 1: Efficient algorithms – one subplot per input type (2 × 4)
    fig1, axes1 = plt.subplots(2, 4, figsize=(22, 10))
    fig1.suptitle("Efficient Sorting Algorithms – Performance by Input Type",
                  fontsize=16, fontweight="bold", y=1.01)

    for idx, (input_name, input_results) in enumerate(all_results.items()):
        ax = axes1[idx // 4][idx % 4]
        for algo_name in ["Heap Sort", "Merge Sort", "Quick Sort"]:
            sizes, times = input_results[algo_name]
            valid = [(s, t) for s, t in zip(sizes, times) if t is not None]
            if valid:
                vs, vt = zip(*valid)
                ax.plot(vs, vt, marker=MARKERS[algo_name], color=COLORS[algo_name],
                        label=algo_name, linewidth=1.8, markersize=5)
        ax.set_title(input_name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Array size (n)", fontsize=9)
        ax.set_ylabel("Time (ms)", fontsize=9)
        ax.legend(fontsize=7, loc="upper left")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig1.savefig(str(IMAGE_DIR / "comparison_input_types.png"),
                 dpi=300, bbox_inches="tight")
    plt.show()

    # Figure 2: Slow Sort – one subplot per input type (2 × 4)
    fig2, axes2 = plt.subplots(2, 4, figsize=(22, 10))
    fig2.suptitle("Slow Sort – Performance by Input Type",
                  fontsize=16, fontweight="bold", y=1.01)

    for idx, (input_name, input_results) in enumerate(all_results.items()):
        ax = axes2[idx // 4][idx % 4]
        sizes, times = input_results["Slow Sort"]
        valid = [(s, t) for s, t in zip(sizes, times) if t is not None]
        if valid:
            vs, vt = zip(*valid)
            ax.plot(vs, vt, marker="v", color="red",
                    label="Slow Sort", linewidth=2, markersize=6)
        ax.set_title(input_name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Array size (n)", fontsize=9)
        ax.set_ylabel("Time (ms)", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig2.savefig(str(IMAGE_DIR / "comparison_slow_input_types.png"),
                 dpi=300, bbox_inches="tight")
    plt.show()

    # Figure 3: All four algorithms on random integers (the "classic" plot)
    fig3, ax3 = plt.subplots(figsize=(12, 7))
    rand_res = all_results["Random Integers"]
    for algo_name in ["Heap Sort", "Merge Sort", "Quick Sort", "Slow Sort"]:
        sizes, times = rand_res[algo_name]
        valid = [(s, t) for s, t in zip(sizes, times) if t is not None]
        if valid:
            vs, vt = zip(*valid)
            ax3.plot(vs, vt, marker=MARKERS[algo_name], color=COLORS[algo_name],
                     label=algo_name, linewidth=2.5, markersize=8)
    ax3.set_title("All Sorting Algorithms – Random Integers",
                  fontsize=16, fontweight="bold")
    ax3.set_xlabel("Array Size (n)", fontsize=13)
    ax3.set_ylabel("Execution Time (ms)", fontsize=13)
    ax3.legend(fontsize=12, loc="upper left")
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    fig3.savefig(str(IMAGE_DIR / "comparison_all.png"),
                 dpi=300, bbox_inches="tight")
    plt.show()

    print("\n✓ Plots saved to", IMAGE_DIR)


if __name__ == "__main__":
    comprehensive_comparison()
