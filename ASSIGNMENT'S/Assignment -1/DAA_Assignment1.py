import time

# DAA ASSIGNMENT 1 - CO1
# Student Record Search System

# 1. Iterative Sequential Search
def sequential_search(records, target):
    comparisons = 0
    for i in range(len(records)):
        comparisons += 1
        if records[i] == target:
            return i, comparisons
    return -1, comparisons

# 2. Recursive Binary Search (input must be sorted)
def binary_search(records, target, low, high):
    if low > high:
        return -1, 0
    mid = (low + high) // 2
    comparisons = 1
    if records[mid] == target:
        return mid, comparisons
    if target < records[mid]:
        pos, count = binary_search(records, target, low, mid - 1)
    else:
        pos, count = binary_search(records, target, mid + 1, high)
    return pos, comparisons + count

# 3. Hash Table Search (Python dictionary)
def hash_table_search(table, target):
    result = table.get(target, None)
    if result is not None:
        return result, 1
    return -1, 1

# Tasks 2-7: basic operation and recurrence analysis
def display_analysis():
    print("\\n========== TASKS 2-7: ANALYSIS ==========")
    print("Sequential Search: registration-number comparisons; O(n)")
    print("Binary Search: middle-element comparisons; O(log n)")
    print("Hash Table Search: dictionary lookup; average O(1)")
    print("\\nBinary Search recurrence: T(n) = T(n/2) + 1, T(1) = 1")
    print("After k steps: T(n) = T(n/2^k) + k")
    print("Set n/2^k = 1, so k = log2(n). Therefore O(log n).")

# Tasks 8-9: experiments at four input sizes
def run_experiments():
    print("\\n========== TASKS 8-9: EXPERIMENTS ==========")
    for n in [1000, 10000, 100000, 1000000]:
        print("\\n----------------------------------")
        print("Number of Student Records:", n)
        records = list(range(1, n + 1))
        target = n  # last record: sequential-search worst case

        start = time.perf_counter()
        pos, count = sequential_search(records, target)
        seq_time = time.perf_counter() - start
        print("\\nSequential Search:")
        print("Position:", pos, "| Comparisons:", count)
        print("Search Time:", round(seq_time, 6), "seconds")

        start = time.perf_counter()
        sorted_records = sorted(records)
        sort_time = time.perf_counter() - start
        start = time.perf_counter()
        pos, count = binary_search(sorted_records, target, 0, n - 1)
        binary_time = time.perf_counter() - start
        print("\\nRecursive Binary Search:")
        print("Position:", pos, "| Comparisons:", count)
        print("Sorting Time:", round(sort_time, 6), "seconds")
        print("Search Time:", round(binary_time, 6), "seconds")

        start = time.perf_counter()
        table = {reg: reg for reg in records}
        build_time = time.perf_counter() - start
        start = time.perf_counter()
        pos, operations = hash_table_search(table, target)
        hash_time = time.perf_counter() - start
        print("\\nHash Table Search:")
        print("Position:", pos, "| Lookup Operations:", operations)
        print("Hash Table Build Time:", round(build_time, 6), "seconds")
        print("Search Time:", round(hash_time, 6), "seconds")

# Tasks 10-12: comparison and design recommendation
def final_decision():
    print("\\n========== TASKS 10-12: DESIGN DECISION ==========")
    print("Sequential Search grows linearly: O(n).")
    print("Binary Search grows logarithmically after sorting: O(log n).")
    print("Hash Table Search has average O(1) lookup.")
    print("\\nRecommendation: use a hash table for frequent lookups.")
    print("Changed requirement: 1,000,000 records; 50,000 searches/hour; daily updates.")
    print("Day-4 decision: RETAIN the hash-table design.")
    print("Build the table at load time and insert each new record.")
    print("Average lookup and insertion: O(1); worst-case lookup: O(n).")

if __name__ == "__main__":
    display_analysis()
    run_experiments()
    final_decision()
    print("\\n========== ASSIGNMENT 1 COMPLETED ==========")
