import random
import time
import math

# Q1 - MAXIMUM, MINIMUM AND BINARY SEARCH

def find_max_min(a):
    if len(a) == 1:
        return a[0], a[0], 0

    if len(a) == 2:
        if a[0] > a[1]:
            return a[0], a[1], 1
        return a[1], a[0], 1

    mid = len(a) // 2

    max1, min1, c1 = find_max_min(a[:mid])
    max2, min2, c2 = find_max_min(a[mid:])

    maximum = max(max1, max2)
    minimum = min(min1, min2)

    return maximum, minimum, c1 + c2 + 2


def binary_search(a, target):
    low = 0
    high = len(a) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        if a[mid] == target:
            return mid, comparisons
        elif a[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


def q1():
    print("\nQ1 - MAX MIN AND BINARY SEARCH")

    a = [10, 5, 20, 3, 15, 8]

    maximum, minimum, count = find_max_min(a)

    print("Array:", a)
    print("Maximum:", maximum)
    print("Minimum:", minimum)
    print("Comparisons:", count)

    a.sort()
    print("Sorted Array:", a)

    position, comparisons = binary_search(a, 15)

    print("Search Position:", position)
    print("Search Comparisons:", comparisons)


# Q2 - MERGE SORT AND QUICK SORT

def merge_sort(a):
    if len(a) <= 1:
        return a

    mid = len(a) // 2

    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def quick_sort(a):
    if len(a) <= 1:
        return a

    pivot = a[-1]

    left = [x for x in a[:-1] if x <= pivot]
    right = [x for x in a[:-1] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)


def q2():
    print("\nQ2 - MERGE SORT AND QUICK SORT")

    a = [8, 4, 7, 3, 9, 2, 6, 1]

    print("Original Array:", a)
    print("Merge Sort:", merge_sort(a))
    print("Quick Sort:", quick_sort(a))

    b = [1, 2, 3, 4, 5, 6, 7, 8]

    print("Sorted Input Quick Sort:", quick_sort(b))


# Q3 - KARATSUBA MULTIPLICATION

def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    power = 10 ** m

    a = x // power
    b = x % power
    c = y // power
    d = y % power

    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    middle = karatsuba(a + b, c + d) - ac - bd

    return ac * (10 ** (2 * m)) + middle * power + bd


def q3():
    print("\nQ3 - KARATSUBA MULTIPLICATION")

    x = 1234
    y = 5678

    print("First Number:", x)
    print("Second Number:", y)
    print("Normal Multiplication:", x * y)
    print("Karatsuba Multiplication:", karatsuba(x, y))


# Q4 - STRASSEN MATRIX MULTIPLICATION

def add_matrix(a, b):
    n = len(a)
    return [
        [a[i][j] + b[i][j] for j in range(n)]
        for i in range(n)
    ]


def subtract_matrix(a, b):
    n = len(a)
    return [
        [a[i][j] - b[i][j] for j in range(n)]
        for i in range(n)
    ]


def strassen(a, b):
    n = len(a)

    if n == 1:
        return [[a[0][0] * b[0][0]]]

    mid = n // 2

    a11 = [row[:mid] for row in a[:mid]]
    a12 = [row[mid:] for row in a[:mid]]
    a21 = [row[:mid] for row in a[mid:]]
    a22 = [row[mid:] for row in a[mid:]]

    b11 = [row[:mid] for row in b[:mid]]
    b12 = [row[mid:] for row in b[:mid]]
    b21 = [row[:mid] for row in b[mid:]]
    b22 = [row[mid:] for row in b[mid:]]

    m1 = strassen(add_matrix(a11, a22), add_matrix(b11, b22))
    m2 = strassen(add_matrix(a21, a22), b11)
    m3 = strassen(a11, subtract_matrix(b12, b22))
    m4 = strassen(a22, subtract_matrix(b21, b11))
    m5 = strassen(add_matrix(a11, a12), b22)
    m6 = strassen(subtract_matrix(a21, a11), add_matrix(b11, b12))
    m7 = strassen(subtract_matrix(a12, a22), add_matrix(b21, b22))

    c11 = add_matrix(subtract_matrix(add_matrix(m1, m4), m5), m7)
    c12 = add_matrix(m3, m5)
    c21 = add_matrix(m2, m4)
    c22 = add_matrix(add_matrix(subtract_matrix(m1, m2), m3), m6)

    result = []

    for i in range(mid):
        result.append(c11[i] + c12[i])

    for i in range(mid):
        result.append(c21[i] + c22[i])

    return result


def q4():
    print("\nQ4 - STRASSEN MATRIX MULTIPLICATION")

    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    print("First Matrix:", a)
    print("Second Matrix:", b)
    print("Result:", strassen(a, b))


# Q5 - CLOSEST PAIR USING DIVIDE AND CONQUER

def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def brute_closest(points):
    best = float("inf")
    pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = distance(points[i], points[j])

            if d < best:
                best = d
                pair = (points[i], points[j])

    return pair, best


def closest_pair(points):
    points = sorted(points)

    def solve(px):
        n = len(px)

        if n <= 3:
            return brute_closest(px)

        mid = n // 2
        middle_x = px[mid][0]

        left_pair, left_dist = solve(px[:mid])
        right_pair, right_dist = solve(px[mid:])

        if left_dist < right_dist:
            best_pair = left_pair
            best_dist = left_dist
        else:
            best_pair = right_pair
            best_dist = right_dist

        strip = [
            p for p in px
            if abs(p[0] - middle_x) < best_dist
        ]

        strip.sort(key=lambda p: p[1])

        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= best_dist:
                    break

                d = distance(strip[i], strip[j])

                if d < best_dist:
                    best_dist = d
                    best_pair = (strip[i], strip[j])

        return best_pair, best_dist

    return solve(points)


def q5():
    print("\nQ5 - CLOSEST PAIR")

    points = [
        (2, 3), (12, 30), (40, 50),
        (5, 1), (12, 10), (3, 4)
    ]

    pair, minimum = closest_pair(points)

    print("Points:", points)
    print("Closest Pair:", pair)
    print("Minimum Distance:", round(minimum, 2))


# Q6 - MEDIAN OF MEDIANS AND MEET IN THE MIDDLE

def median_of_medians(a, k):
    if len(a) <= 5:
        return sorted(a)[k]

    groups = [
        a[i:i + 5]
        for i in range(0, len(a), 5)
    ]

    medians = [
        sorted(group)[len(group) // 2]
        for group in groups
    ]

    pivot = median_of_medians(
        medians, len(medians) // 2
    )

    smaller = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    greater = [x for x in a if x > pivot]

    if k < len(smaller):
        return median_of_medians(smaller, k)

    if k < len(smaller) + len(equal):
        return pivot

    return median_of_medians(
        greater, k - len(smaller) - len(equal)
    )


def quickselect(a, k):
    a = a.copy()

    while True:
        pivot = a[-1]

        left = [x for x in a if x < pivot]
        equal = [x for x in a if x == pivot]
        right = [x for x in a if x > pivot]

        if k < len(left):
            a = left
        elif k < len(left) + len(equal):
            return pivot
        else:
            k -= len(left) + len(equal)
            a = right


def subset_sums(a):
    result = []

    for mask in range(1 << len(a)):
        total = 0

        for i in range(len(a)):
            if mask & (1 << i):
                total += a[i]

        result.append(total)

    return result


def meet_in_middle(a, target):
    mid = len(a) // 2

    left = subset_sums(a[:mid])
    right = sorted(subset_sums(a[mid:]))

    for x in left:
        required = target - x

        low = 0
        high = len(right) - 1

        while low <= high:
            m = (low + high) // 2

            if right[m] == required:
                return True

            elif right[m] < required:
                low = m + 1

            else:
                high = m - 1

    return False


def q6():
    print("\nQ6 - ADVANCED DIVIDE AND CONQUER")

    a = [12, 3, 5, 7, 4, 19, 1]

    k = 3

    print("Array:", a)
    print("K-th Smallest using Median of Medians:",
          median_of_medians(a, k - 1))
    print("K-th Smallest using QuickSelect:",
          quickselect(a, k - 1))

    numbers = [3, 4, 7, 8, 10]
    target = 11

    print("\nSubset Sum Array:", numbers)
    print("Target:", target)
    print("Meet in the Middle Result:",
          meet_in_middle(numbers, target))


def main():
    q1()
    q2()
    q3()
    q4()
    q5()
    q6()


main()
