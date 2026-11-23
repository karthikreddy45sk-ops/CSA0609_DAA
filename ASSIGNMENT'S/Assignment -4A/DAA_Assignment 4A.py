# TASK 1 - FRACTIONAL KNAPSACK

def fractional_knapsack(weights, values, capacity):
    items = []

    for i in range(len(weights)):
        ratio = values[i] / weights[i]
        items.append((ratio, weights[i], values[i]))

    items.sort(reverse=True)

    total_value = 0
    selected = []

    for ratio, weight, value in items:
        if capacity == 0:
            break

        if weight <= capacity:
            selected.append((weight, 1))
            capacity -= weight
            total_value += value
        else:
            fraction = capacity / weight
            selected.append((weight, fraction))
            total_value += value * fraction
            capacity = 0

    return selected, total_value


def task1():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    selected, total = fractional_knapsack(
        weights, values, capacity
    )

    print("\nTASK 1")
    print("Selected Packages:", selected)
    print("Maximum Value:", total)


# TASK 2 - JOB SEQUENCING WITH DEADLINES

def job_sequencing(jobs):
    jobs.sort(key=lambda x: x[2], reverse=True)

    max_deadline = max(job[1] for job in jobs)
    slots = [None] * max_deadline
    total_profit = 0

    for job in jobs:
        job_id, deadline, profit = job

        for i in range(min(deadline, max_deadline) - 1, -1, -1):
            if slots[i] is None:
                slots[i] = job_id
                total_profit += profit
                break

    return slots, total_profit


def task2():
    jobs = [
        ("A", 2, 80),
        ("B", 1, 35),
        ("C", 2, 60),
        ("D", 3, 40),
        ("E", 1, 25)
    ]

    schedule, profit = job_sequencing(jobs)

    print("\nTASK 2")
    print("Schedule:", schedule)
    print("Total Profit:", profit)


# TASK 3 - 0/1 KNAPSACK USING DYNAMIC PROGRAMMING

def knapsack(weights, values, capacity):
    n = len(weights)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
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
            selected.append(i - 1)
            w -= weights[i - 1]

    selected.reverse()

    return dp[n][capacity], selected


def task3():
    weights = [2, 3, 4, 5]
    values = [12, 20, 25, 30]
    capacity = 7

    maximum, selected = knapsack(
        weights, values, capacity
    )

    print("\nTASK 3")
    print("Selected Items:", selected)
    print("Maximum Value:", maximum)


# TASK 4 - WORD BREAK USING DYNAMIC PROGRAMMING

def word_break(text, dictionary):
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and text[j:i] in dictionary:
                dp[i] = True
                break

    return dp[n]


def task4():
    text = "ilikepython"
    dictionary = {
        "i", "like", "python", "py", "thon"
    }

    print("\nTASK 4")
    print("Text:", text)
    print("Can be Segmented:", word_break(text, dictionary))


# TASK 5 - DIJKSTRA, BELLMAN-FORD AND FLOYD

def dijkstra(graph, source):
    vertices = list(graph.keys())
    distance = {v: float("inf") for v in vertices}
    previous = {v: None for v in vertices}
    visited = set()

    distance[source] = 0

    while len(visited) < len(vertices):
        current = None
        minimum = float("inf")

        for v in vertices:
            if v not in visited and distance[v] < minimum:
                minimum = distance[v]
                current = v

        if current is None:
            break

        visited.add(current)

        for neighbour, weight in graph[current]:
            new_distance = distance[current] + weight

            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = current

    return distance, previous


def bellman_ford(vertices, edges, source):
    distance = {v: float("inf") for v in vertices}
    distance[source] = 0

    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distance[u] != float("inf"):
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight

    for u, v, weight in edges:
        if distance[u] != float("inf"):
            if distance[u] + weight < distance[v]:
                return None, True

    return distance, False


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
                distance[i][j] = min(
                    distance[i][j],
                    distance[i][k] + distance[k][j]
                )

    return distance


def task5():
    vertices = ["A", "B", "C", "D", "E"]

    edges = [
        ("A", "B", 4),
        ("A", "C", 7),
        ("B", "C", 2),
        ("B", "D", 6),
        ("C", "D", 1),
        ("D", "E", 3),
        ("C", "E", 8)
    ]

    graph = {v: [] for v in vertices}

    for u, v, weight in edges:
        graph[u].append((v, weight))

    print("\nTASK 5 - DIJKSTRA")
    distances, previous = dijkstra(graph, "A")
    print("Shortest Distances:", distances)

    print("\nTASK 5 - BELLMAN FORD")
    distances, negative_cycle = bellman_ford(
        vertices, edges, "A"
    )

    if negative_cycle:
        print("Negative Cycle Detected")
    else:
        print("Shortest Distances:", distances)

    print("\nTASK 5 - FLOYD WARSHALL")
    result = floyd_warshall(vertices, edges)

    for row in result:
        print(row)


# TASK 6 - WEIGHTED JOB SCHEDULING

def weighted_job_scheduling(jobs):
    jobs = sorted(jobs, key=lambda x: x[1])
    n = len(jobs)

    previous = []

    for i in range(n):
        compatible = -1

        for j in range(i - 1, -1, -1):
            if jobs[j][1] <= jobs[i][0]:
                compatible = j
                break

        previous.append(compatible)

    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        include = jobs[i - 1][2]

        if previous[i - 1] != -1:
            include += dp[previous[i - 1] + 1]

        exclude = dp[i - 1]

        dp[i] = max(include, exclude)

    selected = []
    i = n

    while i > 0:
        include = jobs[i - 1][2]

        if previous[i - 1] != -1:
            include += dp[previous[i - 1] + 1]

        if include > dp[i - 1]:
            selected.append(jobs[i - 1])
            i = previous[i - 1] + 1
        else:
            i -= 1

    selected.reverse()

    return selected, dp[n]


def task6():
    jobs = [
        ("J1", 1, 3, 20),
        ("J2", 2, 5, 50),
        ("J3", 4, 6, 30),
        ("J4", 6, 8, 40),
        ("J5", 5, 9, 60),
        ("J6", 8, 10, 30),
        ("J7", 9, 11, 50),
        ("J8", 11, 13, 40)
    ]

    selected, maximum = weighted_job_scheduling(
        [(job[1], job[2], job[3], job[0]) for job in jobs]
    )

    print("\nTASK 6")
    print("Selected Jobs:")

    for job in selected:
        print(job[3])

    print("Maximum Energy Saving:", maximum)


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


main()
