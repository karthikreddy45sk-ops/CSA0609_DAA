
import time
import math
from itertools import combinations

# =====================================
# Q1 - SORTING ALGORITHMS
# =====================================

def selection_sort(a):
    a = a.copy()
    comparisons = swaps = 0

    for i in range(len(a)):
        min_index = i

        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[min_index]:
                min_index = j

        if min_index != i:
            a[i], a[min_index] = a[min_index], a[i]
            swaps += 1

    return a, comparisons, swaps


def bubble_sort(a):
    a = a.copy()
    comparisons = swaps = 0

    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            comparisons += 1

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1

    return a, comparisons, swaps


def insertion_sort(a):
    a = a.copy()
    comparisons = movements = 0

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if a[j] > key:
                a[j + 1] = a[j]
                movements += 1
                j -= 1
            else:
                break

        a[j + 1] = key

    return a, comparisons, movements


def task1():
    print("\n--- Q1 SORTING ---")

    datasets = {
        "Random": [5, 2, 8, 1, 9, 3],
        "Nearly Sorted": [1, 2, 4, 3, 5, 6],
        "Already Sorted": [1, 2, 3, 4, 5, 6]
    }

    for name, data in datasets.items():
        print("\n", name, ":", data)

        for algorithm in [
            selection_sort, bubble_sort, insertion_sort
        ]:
            result, comp, moves = algorithm(data)

            print(algorithm.__name__)
            print("Sorted:", result)
            print("Comparisons:", comp)
            print("Swaps/Movements:", moves)


# =====================================
# Q2 - SEQUENTIAL SEARCH
# =====================================

def sequential_search(data, target):
    comparisons = 0

    for i in range(len(data)):
        comparisons += 1

        if data[i] == target:
            return i, comparisons

    return -1, comparisons


def task2():
    print("\n--- Q2 SEQUENTIAL SEARCH ---")

    tools = ["T101", "T102", "T103", "T184", "T105"]

    for target in ["T101", "T103", "T105", "T999"]:
        position, comparisons = sequential_search(tools, target)

        print("\nSearching:", target)
        print("Position:", position)
        print("Comparisons:", comparisons)

    # Changed condition: dictionary-based lookup
    tool_index = {tool: i for i, tool in enumerate(tools)}

    print("\nDictionary Search:")
    print("T184 position:", tool_index.get("T184", -1))


# =====================================
# Q3 - BRUTE FORCE STRING MATCHING
# =====================================

def string_matching(text, pattern):
    comparisons = 0
    positions = []

    for i in range(len(text) - len(pattern) + 1):
        j = 0

        while j < len(pattern):
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == len(pattern):
            positions.append(i)

    return positions, comparisons


def task3():
    print("\n--- Q3 STRING MATCHING ---")

    tests = [
        ("HELLO WORLD", "WORLD"),
        ("AAAAAAAAAA", "AAAAB"),
        ("COMPUTER SCIENCE", "SCI")
    ]

    for text, pattern in tests:
        positions, comparisons = string_matching(text, pattern)

        print("\nText:", text)
        print("Pattern:", pattern)
        print("Positions:", positions)
        print("Character Comparisons:", comparisons)


# =====================================
# Q4 - BRUTE FORCE CLOSEST PAIR
# =====================================

def closest_pair(points):
    min_distance = float("inf")
    best_pair = None
    comparisons = 0

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            comparisons += 1

            x1, y1 = points[i]
            x2, y2 = points[j]

            distance = math.sqrt(
                (x2 - x1) ** 2 + (y2 - y1) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                best_pair = (points[i], points[j])

    return best_pair, min_distance, comparisons


def task4():
    print("\n--- Q4 CLOSEST PAIR ---")

    test_data = [
        [(1, 2), (4, 6), (2, 3), (8, 9)],
        [(1, 1), (2, 2), (5, 5), (6, 6), (3, 3)],
        [(0, 0), (10, 10), (2, 2), (3, 3),
         (20, 20), (4, 4), (5, 5), (6, 6)]
    ]

    for points in test_data:
        pair, distance, count = closest_pair(points)

        print("\nPoints:", points)
        print("Closest Pair:", pair)
        print("Minimum Distance:", round(distance, 2))
        print("Pairs Examined:", count)


# =====================================
# Q5 - BRUTE FORCE CONVEX HULL
# =====================================

def cross_product(a, b, c):
    return (
        (b[0] - a[0]) * (c[1] - a[1])
        - (b[1] - a[1]) * (c[0] - a[0])
    )


def convex_hull(points):
    hull_points = set()
    operations = 0
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            left = right = False

            for k in range(n):
                if k == i or k == j:
                    continue

                operations += 1
                value = cross_product(
                    points[i], points[j], points[k]
                )

                if value > 0:
                    left = True
                elif value < 0:
                    right = True

            # All other points must be on one side
            if not (left and right):
                hull_points.add(points[i])
                hull_points.add(points[j])

    # Arrange hull points in boundary order
    if len(hull_points) < 3:
        return list(hull_points), operations

    center_x = sum(p[0] for p in hull_points) / len(hull_points)
    center_y = sum(p[1] for p in hull_points) / len(hull_points)

    ordered = sorted(
        hull_points,
        key=lambda p: math.atan2(
            p[1] - center_y, p[0] - center_x
        )
    )

    return ordered, operations


def task5():
    print("\n--- Q5 CONVEX HULL ---")

    tests = [
        [(0, 0), (0, 4), (4, 0), (4, 4), (2, 2)],
        [(1, 1), (2, 5), (5, 4), (6, 1),
         (3, 2), (3, 3)]
    ]

    for points in tests:
        hull, operations = convex_hull(points)

        print("\nInput Points:", points)
        print("Hull Boundary Points:", hull)
        print("Operations:", operations)


# =====================================
# Q6 - EXHAUSTIVE SEARCH / KNAPSACK
# =====================================

def knapsack(weights, values, capacity):
    n = len(weights)
    best_value = 0
    best_items = []
    candidates = 0

    for mask in range(1 << n):
        total_weight = 0
        total_value = 0
        selected = []

        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
                selected.append(i + 1)

        candidates += 1

        if total_weight <= capacity:
            if total_value > best_value:
                best_value = total_value
                best_items = selected

    return best_items, best_value, candidates


def task6():
    print("\n--- Q6 EXHAUSTIVE SEARCH ---")

    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8

    items, value, candidates = knapsack(
        weights, values, capacity
    )

    print("Weights:", weights)
    print("Values:", values)
    print("Capacity:", capacity)
    print("Selected Items:", items)
    print("Maximum Value:", value)
    print("Candidate Combinations:", candidates)

    # Test increasing problem sizes
    print("\nGrowth Test:")

    for n in [4, 6, 8]:
        weights = list(range(1, n + 1))
        values = list(range(2, n + 2))

        items, value, count = knapsack(
            weights, values, n * 2
        )

        print("Packages:", n)
        print("Combinations:", count)


# =====================================
# Q7 - REDESIGN SEQUENTIAL SEARCH
# =====================================

def task7():
    print("\n--- Q7 REDESIGN ---")

    tools = [
        "T101", "T102", "T103", "T104",
        "T105", "T106", "T107", "T108"
    ]

    target = "T108"

    # Original method
    position, comparisons = sequential_search(
        tools, target
    )

    print("\nSequential Search:")
    print("Position:", position)
    print("Comparisons:", comparisons)

    # Redesigned method using a dictionary
    tool_dictionary = {
        tool: i for i, tool in enumerate(tools)
    }

    print("\nDictionary Search:")
    print("Position:", tool_dictionary.get(target, -1))
    print("Lookup uses a hash table for average O(1) lookup.")

    print("\nRedesign Objective:")
    print("Reduce repeated linear comparisons.")
    print("Trade-off: extra memory is required to build the dictionary.")


# =====================================
# MAIN PROGRAM
# =====================================

def main():
    print("DAA ASSIGNMENT 2 - CO2")
    print("======================")

    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()

    print("\nALL QUESTIONS COMPLETED")


if __name__ == "__main__":
    main()
