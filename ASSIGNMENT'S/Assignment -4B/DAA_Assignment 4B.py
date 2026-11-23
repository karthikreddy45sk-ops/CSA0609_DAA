import time
import math
from itertools import combinations

# TASK 1 - WORD WRAP USING DYNAMIC PROGRAMMING

def word_wrap(words, width):
    n = len(words)
    dp = [float("inf")] * (n + 1)
    parent = [-1] * (n + 1)

    dp[0] = 0

    for i in range(1, n + 1):
        length = 0

        for j in range(i, 0, -1):
            length += len(words[j - 1])

            if j < i:
                length += 1

            if length > width:
                break

            spaces = width - length
            penalty = 0 if i == n else spaces ** 2
            cost = dp[j - 1] + penalty

            if cost < dp[i]:
                dp[i] = cost
                parent[i] = j - 1

    lines = []
    end = n

    while end > 0:
        start = parent[end]
        if start == -1:
            raise ValueError("A word is longer than the line width.")
        lines.append(words[start:end])
        end = start

    lines.reverse()

    print("Minimum Penalty:", dp[n])

    for line in lines:
        text = " ".join(line)
        spaces = width - len(text)
        penalty = 0 if line == lines[-1] else spaces ** 2
        print(text, "| Unused Spaces:", spaces, "| Penalty:", penalty)

    print("DP States:", dp)


def task1():
    print("\nTASK 1 - WORD WRAP")

    words = [
        "Dynamic", "Programming", "is", "used",
        "to", "solve", "optimization", "problems"
    ]

    for width in [15, 20, 25]:
        print("\nLine Width:", width)
        word_wrap(words, width)


# TASK 2 - FRACTIONAL AND 0/1 KNAPSACK

def fractional_knapsack(weights, values, capacity):
    items = []

    for i in range(len(weights)):
        items.append((values[i] / weights[i], i))

    items.sort(reverse=True)

    total = 0
    selected = []
    operations = 0

    for ratio, i in items:
        operations += 1

        if capacity == 0:
            break

        fraction = min(1, capacity / weights[i])
        selected.append((i + 1, fraction))
        total += values[i] * fraction
        capacity -= weights[i] * fraction

    return total, selected, operations


def zero_one_knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    operations = 0

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            operations += 1

            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i)
            w -= weights[i - 1]

    selected.reverse()

    return dp[n][capacity], selected, operations, dp


def task2():
    print("\nTASK 2 - KNAPSACK")

    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    total, selected, operations = fractional_knapsack(
        weights, values, capacity
    )

    print("\nFractional Knapsack")
    print("Selected Items and Fractions:", selected)
    print("Maximum Value:", total)
    print("Operations:", operations)

    total, selected, operations, dp = zero_one_knapsack(
        weights, values, capacity
    )

    print("\n0/1 Knapsack")
    print("Selected Items:", selected)
    print("Maximum Value:", total)
    print("Operations:", operations)
    print("DP Table:")

    for row in dp:
        print(row)

    print("\nGreedy Counterexample")

    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    total, selected, operations = fractional_knapsack(
        weights, values, capacity
    )

    print("Fractional Result:", total, selected)

    total, selected, operations, dp = zero_one_knapsack(
        weights, values, capacity
    )

    print("0/1 Optimal Result:", total, selected)


# TASK 3 - SHORTEST PATH ALGORITHMS

def dijkstra(graph, source):
    distance = {v: float("inf") for v in graph}
    previous = {v: None for v in graph}
    visited = set()
    order = []

    distance[source] = 0

    while len(visited) < len(graph):
        current = None

        for v in graph:
            if v not in visited:
                if current is None or distance[v] < distance[current]:
                    current = v

        if current is None or distance[current] == float("inf"):
            break

        visited.add(current)
        order.append(current)

        for neighbour, weight in graph[current]:
            if distance[current] + weight < distance[neighbour]:
                distance[neighbour] = distance[current] + weight
                previous[neighbour] = current

    return distance, previous, order


def bellman_ford(vertices, edges, source):
    distance = {v: float("inf") for v in vertices}
    previous = {v: None for v in vertices}

    distance[source] = 0

    for _ in range(len(vertices) - 1):
        changed = False

        for u, v, weight in edges:
            if distance[u] != float("inf"):
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    previous[v] = u
                    changed = True

        if not changed:
            break

    for u, v, weight in edges:
        if distance[u] != float("inf"):
            if distance[u] + weight < distance[v]:
                return None, None, True

    return distance, previous, False


def floyd_warshall(vertices, edges):
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    distance = [[float("inf")] * n for _ in range(n)]

    for i in range(n):
        distance[i][i] = 0

    for u, v, weight in edges:
        distance[index[u]][index[v]] = weight

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]

    return distance


def warshall(vertices, edges):
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    reach = [[0] * n for _ in range(n)]

    for i in range(n):
        reach[i][i] = 1

    for u, v, weight in edges:
        reach[index[u]][index[v]] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = (
                    reach[i][j] or
                    (reach[i][k] and reach[k][j])
                )

    return reach


def show_path(previous, source, destination):
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if path[0] == source:
        return path

    return []


def task3():
    print("\nTASK 3 - ROUTING ALGORITHMS")

    vertices = list("ABCDEFGH")

    edges = [
        ("A", "B", 4), ("A", "C", 8),
        ("B", "C", 2), ("B", "D", 5),
        ("C", "D", 1), ("C", "E", 6),
        ("D", "E", 3), ("D", "F", 7),
        ("E", "F", 2), ("E", "G", 5),
        ("F", "G", 1), ("G", "H", 3),
        ("F", "H", 6), ("B", "H", 12)
    ]

    graph = {v: [] for v in vertices}

    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    distance, previous, order = dijkstra(graph, "A")

    print("\nDijkstra")
    print("Distances:", distance)
    print("Predecessors:", previous)
    print("Finalisation Order:", order)
    print("Path A to H:", show_path(previous, "A", "H"))

    directed_edges = [
        ("A", "B", 4), ("A", "C", 8),
        ("B", "C", 2), ("B", "D", 5),
        ("C", "D", 1), ("C", "E", 6),
        ("D", "E", 3), ("D", "F", 7),
        ("E", "F", 2), ("E", "G", 5),
        ("F", "G", 1), ("G", "H", 3),
        ("F", "H", 6), ("B", "H", 12)
    ]

    modified_edges = directed_edges + [("A", "H", -2)]

    print("\nBellman-Ford with Negative Edge")
    distance, previous, cycle = bellman_ford(
        vertices, modified_edges, "A"
    )

    if cycle:
        print("Negative Cycle Detected")
    else:
        print("Distances:", distance)
        print("Path A to H:", show_path(previous, "A", "H"))

    cycle_edges = modified_edges + [("H", "A", -5)]

    print("\nNegative Cycle Test")
    distance, previous, cycle = bellman_ford(
        vertices, cycle_edges, "A"
    )

    if cycle:
        print("Reachable Negative Cycle Detected")

    print("\nFloyd-Warshall Matrix")
    matrix = floyd_warshall(vertices, directed_edges)

    for row in matrix:
        print(row)

    print("\nWarshall Reachability Matrix")
    matrix = warshall(vertices, directed_edges)

    for row in matrix:
        print(row)


# TASK 4 - ASSEMBLY LINE SCHEDULING

def assembly_line(a, b, transfer1, transfer2, entry1, entry2,
                  exit1, exit2):
    n = len(a)

    dp1 = [0] * n
    dp2 = [0] * n

    path1 = [0] * n
    path2 = [0] * n

    dp1[0] = entry1 + a[0]
    dp2[0] = entry2 + b[0]

    print("\nStation 1")
    print("Line 1 Cost:", dp1[0])
    print("Line 2 Cost:", dp2[0])

    for i in range(1, n):
        stay1 = dp1[i - 1] + a[i]
        change1 = dp2[i - 1] + transfer2[i - 1] + a[i]

        stay2 = dp2[i - 1] + b[i]
        change2 = dp1[i - 1] + transfer1[i - 1] + b[i]

        if stay1 <= change1:
            dp1[i] = stay1
            path1[i] = 1
        else:
            dp1[i] = change1
            path1[i] = 2

        if stay2 <= change2:
            dp2[i] = stay2
            path2[i] = 2
        else:
            dp2[i] = change2
            path2[i] = 1

        print("\nStation", i + 1)
        print("Line 1 - Stay:", stay1, "Transfer:", change1)
        print("Line 2 - Stay:", stay2, "Transfer:", change2)

    final1 = dp1[-1] + exit1
    final2 = dp2[-1] + exit2

    if final1 <= final2:
        minimum = final1
        line = 1
    else:
        minimum = final2
        line = 2

    route = [0] * n
    route[-1] = line

    for i in range(n - 1, 0, -1):
        if route[i] == 1:
            route[i - 1] = path1[i]
        else:
            route[i - 1] = path2[i]

    print("\nOptimal Route:")

    for i, selected in enumerate(route):
        print("Line", selected, "- Station", i + 1)

        if i < n - 1 and route[i] != route[i + 1]:
            print("Transfer to Line", route[i + 1])

    print("Minimum Production Time:", minimum)

    return minimum, route


def task4():
    print("\nTASK 4 - ASSEMBLY LINE")

    a = [7, 9, 3, 4, 8, 4]
    b = [8, 5, 6, 4, 5, 7]

    transfer1 = [2, 3, 1, 3, 4]
    transfer2 = [2, 1, 2, 2, 1]

    assembly_line(
        a, b, transfer1, transfer2,
        2, 4, 3, 2
    )

    print("\nChanged Transfer Time")
    transfer1[2] = 15

    assembly_line(
        a, b, transfer1, transfer2,
        2, 4, 3, 2
    )

    print("\nMachine Disruption")
    a[2] = 20

    assembly_line(
        a, b, transfer1, transfer2,
        2, 4, 3, 2
    )


# TASK 5 - MINIMUM SPANNING TREE

def kruskal(vertices, edges):
    parent = {v: v for v in vertices}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    result = []
    total = 0

    for u, v, weight in sorted(edges, key=lambda x: x[2]):
        root1 = find(u)
        root2 = find(v)

        if root1 != root2:
            parent[root1] = root2
            result.append((u, v, weight))
            total += weight
            print("Kruskal Selected:", u, v, weight)

    return result, total


def prim(vertices, edges):
    graph = {v: [] for v in vertices}

    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    visited = {vertices[0]}
    result = []
    total = 0

    while len(visited) < len(vertices):
        best = None

        for u in visited:
            for v, weight in graph[u]:
                if v not in visited:
                    if best is None or weight < best[2]:
                        best = (u, v, weight)

        if best is None:
            break

        u, v, weight = best
        visited.add(v)
        result.append(best)
        total += weight

        print("Prim Selected:", best)

    return result, total


def boruvka(vertices, edges):
    parent = {v: v for v in vertices}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    result = []
    total = 0

    while True:
        cheapest = {}

        for u, v, weight in edges:
            root1 = find(u)
            root2 = find(v)

            if root1 != root2:
                if root1 not in cheapest or weight < cheapest[root1][2]:
                    cheapest[root1] = (u, v, weight)

                if root2 not in cheapest or weight < cheapest[root2][2]:
                    cheapest[root2] = (u, v, weight)

        if not cheapest:
            break

        added = False

        for edge in cheapest.values():
            u, v, weight = edge
            root1 = find(u)
            root2 = find(v)

            if root1 != root2:
                parent[root1] = root2
                result.append(edge)
                total += weight
                added = True
                print("Boruvka Selected:", edge)

        if not added:
            break

    return result, total


def task5():
    print("\nTASK 5 - MINIMUM SPANNING TREE")

    vertices = ["A", "B", "C", "D", "E", "F"]

    edges = [
        ("A", "B", 4), ("A", "C", 3),
        ("B", "C", 2), ("B", "D", 5),
        ("C", "D", 3), ("C", "E", 6),
        ("D", "E", 1), ("D", "F", 7),
        ("E", "F", 4), ("B", "F", 8)
    ]

    print("\nKruskal")
    result, total = kruskal(vertices, edges)
    print("MST:", result)
    print("Total Cost:", total)

    print("\nPrim")
    result, total = prim(vertices, edges)
    print("MST:", result)
    print("Total Cost:", total)

    print("\nBoruvka")
    result, total = boruvka(vertices, edges)
    print("MST:", result)
    print("Total Cost:", total)

    print("\nMultiple MST Test")
    equal_edges = [
        ("A", "B", 1), ("A", "C", 1),
        ("B", "C", 1), ("B", "D", 1),
        ("C", "D", 1)
    ]

    result, total = kruskal(["A", "B", "C", "D"], equal_edges)
    print("Kruskal Cost:", total)

    result, total = prim(["A", "B", "C", "D"], equal_edges)
    print("Prim Cost:", total)


# TASK 6 - TRAVELLING SALESPERSON USING DP

def tsp_dp(cost):
    n = len(cost)
    dp = {}
    parent = {}

    dp[(1, 0)] = 0

    for mask in range(1 << n):
        if not (mask & 1):
            continue

        for current in range(n):
            if (mask, current) not in dp:
                continue

            for next_city in range(1, n):
                if not (mask & (1 << next_city)):
                    new_mask = mask | (1 << next_city)
                    new_cost = (
                        dp[(mask, current)] +
                        cost[current][next_city]
                    )

                    key = (new_mask, next_city)

                    if key not in dp or new_cost < dp[key]:
                        dp[key] = new_cost
                        parent[key] = current

    full_mask = (1 << n) - 1
    minimum = float("inf")
    last_city = -1

    for city in range(1, n):
        total = dp[(full_mask, city)] + cost[city][0]

        if total < minimum:
            minimum = total
            last_city = city

    route = []
    mask = full_mask
    current = last_city

    while current != 0:
        route.append(current)
        previous = parent[(mask, current)]
        mask ^= (1 << current)
        current = previous

    route.append(0)
    route.reverse()
    route.append(0)

    return minimum, route, len(dp)


def exhaustive_tsp(cost):
    n = len(cost)
    best = float("inf")
    best_route = None

    for route in combinations(range(1, n), n - 1):
        path = (0,) + route + (0,)
        total = 0

        for i in range(len(path) - 1):
            total += cost[path[i]][path[i + 1]]

        if total < best:
            best = total
            best_route = path

    return best, best_route


def task6():
    print("\nTASK 6 - TRAVELLING SALESPERSON")

    cost = [
        [0, 10, 15, 20, 12, 18, 25],
        [10, 0, 35, 25, 17, 22, 30],
        [15, 35, 0, 30, 20, 16, 28],
        [20, 25, 30, 0, 18, 24, 14],
        [12, 17, 20, 18, 0, 19, 21],
        [18, 22, 16, 24, 19, 0, 13],
        [25, 30, 28, 14, 21, 13, 0]
    ]

    start = time.time()
    minimum, route, states = tsp_dp(cost)
    elapsed = time.time() - start

    names = ["Hub", "A", "B", "C", "D", "E", "F"]

    print("Optimal Route:", " -> ".join(names[i] for i in route))
    print("Minimum Travel Cost:", minimum)
    print("DP States Evaluated:", states)
    print("Execution Time:", round(elapsed, 6), "seconds")

    small_cost = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 17],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 18],
        [25, 17, 20, 18, 0]
    ]

    dp_result, dp_route, dp_states = tsp_dp(small_cost)
    exact_result, exact_route = exhaustive_tsp(small_cost)

    print("\nValidation Test")
    print("DP Result:", dp_result)
    print("Exhaustive Result:", exact_result)
    print("Results Match:", dp_result == exact_result)

    print("\nState Space Growth")

    for locations in range(4, 9):
        matrix = [
            [
                0 if i == j else abs(i - j) + 2
                for j in range(locations + 1)
            ]
            for i in range(locations + 1)
        ]

        start = time.time()
        result, route, states = tsp_dp(matrix)
        elapsed = time.time() - start

        print(
            "Locations:", locations,
            "States:", states,
            "Time:", round(elapsed, 6)
        )


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    main()
