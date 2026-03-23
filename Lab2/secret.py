import random
import time
import matplotlib.pyplot as plt

def epstein_sort(arr, protected_ratio=0.30, island_drop_ratio=0.20):
    # split by threshold <18
    island = [x for x in arr if x < 18]
    main   = [x for x in arr if x >= 18]

    n = len(main)
    if n == 0:
        return island[:]

    protected = [random.random() < protected_ratio for i in range(n)]

    #  bubble sort that skips protected elements
    for i in range(n - 1):
        for j in range(n - 1):
            if main[j] > main[j + 1]:
                if not protected[j] and not protected[j + 1]:
                    main[j], main[j + 1] = main[j + 1], main[j]
                    protected[j], protected[j + 1] = protected[j + 1], protected[j]

    # drop some island elements, then reinsert the rest at random positions
    result = main[:]
    for x in island:
        # randomly lose some island elements 
        if random.random() < island_drop_ratio:
            continue
        result.insert(random.randint(0, len(result)), x)

    return result



def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000]
    repeats = 3
    times = []

    header = "n  " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print("\nEpstein is workin ..")
    print(header)
    print("-" * len(header))

    for size in test_sizes:
        execs = []
        for _ in range(repeats):
            arr = [random.randint(1, 10_000) for _ in range(size)]
            start = time.perf_counter()
            epstein_sort(arr)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg = sum(execs) / repeats
        row = f"{size:<6} " + "  ".join(f"{t:>10.3f}" for t in execs) + f"  {avg:>10.3f}"
        print(row)
        times.append(avg)

    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Epstein Sort alone
    axes[0].plot(test_sizes, times, marker="x", linestyle="-", color="crimson",
                 label="Epstein Sort", linewidth=2, markersize=8)
    axes[0].set_title("Epstein Sort (O(n²) – incorrect output)")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Right: comparison with a correct O(n²) sort — plain bubble sort
    bubble_times = []
    for size in test_sizes:
        execs = []
        for _ in range(repeats):
            arr = [random.randint(1, 10_000) for _ in range(size)]
            start = time.perf_counter()
            # standard bubble sort for reference
            a = arr[:]
            n = len(a)
            for i in range(n - 1):
                for j in range(n - 1 - i):
                    if a[j] > a[j + 1]:
                        a[j], a[j + 1] = a[j + 1], a[j]
            end = time.perf_counter()
            execs.append((end - start) * 1000)
        bubble_times.append(sum(execs) / repeats)

    axes[1].plot(test_sizes, times, marker="x", linestyle="-", color="crimson",
                 label="Epstein Sort (incorrect)", linewidth=2, markersize=8)
    axes[1].plot(test_sizes, bubble_times, marker="o", linestyle="--", color="gray",
                 label="Bubble Sort (correct)", linewidth=2, markersize=8)
    axes[1].set_title("Epstein Sort vs Bubble Sort")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Execution Time (ms)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

   
    plt.show()

    print("\ncheck")
    for size in [10, 50, 100]:
        arr = list(range(1, size + 1))
        random.shuffle(arr)
        result = epstein_sort(arr[:])
        correct = result == sorted(arr)
        print(f"  n={size}: {'CORRECT' if correct else 'INCORRECT'} — {result[:10]}{'...' if size > 10 else ''}")


if __name__ == "__main__":
    performance()
