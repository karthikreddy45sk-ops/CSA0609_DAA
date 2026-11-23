from itertools import combinations

# ==========================================
# B1 - GRAPH COLOURING USING BACKTRACKING
# ==========================================

def graph_coloring(graph, vertices, colors, heuristic=False):

    color = [-1] * vertices

    stats = {
        "nodes": 0,
        "attempts": 0,
        "rejected": 0,
        "backtracks": 0,
        "max_depth": 0
    }

    if heuristic:
        order = sorted(
            range(vertices),
            key=lambda v: len(graph[v]),
            reverse=True
        )
    else:
        order = list(range(vertices))

    def is_safe(vertex, c):
        for neighbour in graph[vertex]:
            if color[neighbour] == c:
                return False
        return True

    def solve(index):

        stats["nodes"] += 1
        stats["max_depth"] = max(
            stats["max_depth"], index
        )

        if index == vertices:
            return True

        vertex = order[index]

        for c in range(colors):

            stats["attempts"] += 1

            if is_safe(vertex, c):

                color[vertex] = c

                if solve(index + 1):
                    return True

                color[vertex] = -1
                stats["backtracks"] += 1

            else:
                stats["rejected"] += 1

        return False

    result = solve(0)

    return result, color, stats


def make_graph(vertices, edges):

    graph = [[] for _ in range(vertices)]

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    return graph


def display_graph_result(name, graph, vertices, colors):

    print("\n", name)

    for heuristic in [False, True]:

        version = (
            "Degree Heuristic"
            if heuristic else "Input Order"
        )

        result, coloring, stats = graph_coloring(
            graph, vertices, colors, heuristic
        )

        print("\nStrategy:", version)
        print("Colourable:", result)

        if result:
            print("Final Colouring:")

            for i in range(vertices):
                print(
                    "Vertex", i,
                    "-> Colour", coloring[i] + 1
                )

        print("Search Nodes:", stats["nodes"])
        print("Candidate Assignments:", stats["attempts"])
        print("Rejected Branches:", stats["rejected"])
        print("Backtracks:", stats["backtracks"])
        print("Maximum Search Depth:", stats["max_depth"])


def task_b1():

    print("\n========== B1: GRAPH COLOURING ==========")

    # Colourable graph
    edges1 = [
        (0, 1), (0, 2), (1, 2),
        (1, 3), (2, 4), (3, 4)
    ]

    graph1 = make_graph(5, edges1)

    display_graph_result(
        "Colourable Graph", graph1, 5, 3
    )

    # Non-colourable graph K4 using 3 colours
    edges2 = list(combinations(range(4), 2))

    graph2 = make_graph(4, edges2)

    display_graph_result(
        "Non-Colourable Graph", graph2, 4, 3
    )

    # Boundary case: no edges
    graph3 = make_graph(4, [])

    display_graph_result(
        "Boundary Case - No Edges", graph3, 4, 1
    )


# ==========================================
# B2 - ADVERSARIAL GRAPH TESTING
# ==========================================

def task_b2():

    print("\n========== B2: ADVERSARIAL INPUT ==========")

    # Graph A: Path graph
    edges_a = [
        (0, 1), (1, 2), (2, 3),
        (3, 4), (4, 5)
    ]

    # Graph B: Complete graph K6
    edges_b = list(combinations(range(6), 2))

    graph_a = make_graph(6, edges_a)
    graph_b = make_graph(6, edges_b)

    for name, graph in [
        ("Graph A - Path Graph", graph_a),
        ("Graph B - Complete Graph K6", graph_b)
    ]:

        result, coloring, stats = graph_coloring(
            graph, 6, 3
        )

        print("\n", name)
        print("Colourable:", result)
        print("Search Nodes:", stats["nodes"])
        print("Candidate Assignments:", stats["attempts"])
        print("Rejected Branches:", stats["rejected"])
        print("Backtracks:", stats["backtracks"])


# ==========================================
# B3 - EXACT AND GREEDY SET COVER
# ==========================================

def exact_set_cover(universe, centres):

    names = list(centres.keys())
    operations = 0

    for size in range(1, len(names) + 1):

        for group in combinations(names, size):

            operations += 1
            covered = set()

            for name in group:
                covered.update(centres[name])

            if universe.issubset(covered):
                return list(group), operations

    return None, operations


def greedy_set_cover(universe, centres):

    uncovered = set(universe)
    selected = []
    operations = 0

    while uncovered:

        best_centre = None
        best_gain = 0

        for name, zones in centres.items():

            if name in selected:
                continue

            gain = len(uncovered.intersection(zones))
            operations += 1

            if gain > best_gain:
                best_gain = gain
                best_centre = name

        if best_centre is None:
            return None, operations

        selected.append(best_centre)
        uncovered -= centres[best_centre]

    return selected, operations


def run_set_cover_case(
    case_name, universe, centres
):

    exact, exact_ops = exact_set_cover(
        universe, centres
    )

    greedy, greedy_ops = greedy_set_cover(
        universe, centres
    )

    print("\n", case_name)

    print("Exact Cover:", exact)
    print(
        "Exact Cover Size:",
        len(exact) if exact else "No cover"
    )
    print("Exact Search Operations:", exact_ops)

    print("Greedy Cover:", greedy)
    print(
        "Greedy Cover Size:",
        len(greedy) if greedy else "No cover"
    )
    print("Greedy Selection Operations:", greedy_ops)

    same = (
        len(exact) == len(greedy)
        if exact is not None and greedy is not None
        else False
    )

    print("Same Cover Size:", same)


def task_b3():

    print("\n========== B3: SET COVER ==========")

    # Test Case 1
    universe1 = {"A", "B", "C", "D"}

    centres1 = {
        "C1": {"A", "B"},
        "C2": {"C", "D"},
        "C3": {"A", "C"},
        "C4": {"B", "D"}
    }

    # Test Case 2
    universe2 = {"A", "B", "C", "E"}

    centres2 = {
        "C1": {"A", "B", "C"},
        "C2": {"A", "B"},
        "C3": {"C", "E"},
        "C4": {"E"}
    }

    # Test Case 3 - Counterexample
    universe3 = {1, 2, 3, 4, 5, 6}

    centres3 = {
        "C1": {1, 2, 3, 4},
        "C2": {1, 2, 5},
        "C3": {3, 4, 6},
        "C4": {1, 2},
        "C5": {3, 4}
    }

    run_set_cover_case(
        "Test Case 1", universe1, centres1
    )

    run_set_cover_case(
        "Test Case 2", universe2, centres2
    )

    run_set_cover_case(
        "Test Case 3 - Counterexample",
        universe3, centres3
    )

    # Greedy selection trace
    print("\nGreedy Selection Trace:")

    uncovered = set(universe3)
    selected = []

    while uncovered:

        best = None
        best_gain = 0

        for name, zones in centres3.items():

            if name not in selected:

                gain = len(
                    uncovered.intersection(zones)
                )

                if gain > best_gain:
                    best = name
                    best_gain = gain

        if best is None:
            break

        selected.append(best)
        uncovered -= centres3[best]

        print(
            "Selected:", best,
            "| Newly Covered:", best_gain,
            "| Remaining:", sorted(uncovered)
        )

    # Larger test case
    print("\nScalability Test:")

    universe_large = set(range(1, 9))

    centres_large = {
        "C1": {1, 2, 3},
        "C2": {3, 4, 5},
        "C3": {5, 6, 7},
        "C4": {7, 8, 1},
        "C5": {1, 4, 6},
        "C6": {2, 5, 8},
        "C7": {2, 3, 6},
        "C8": {4, 7, 8}
    }

    run_set_cover_case(
        "Larger Set Cover Instance",
        universe_large, centres_large
    )


# ==========================================
# B4 - BIN PACKING USING FIRST FIT
# ==========================================

def first_fit(workloads, capacity):

    servers = []

    for workload in workloads:

        if workload <= 0 or workload > capacity:
            raise ValueError(
                "Workload must be greater than 0 "
                "and no larger than server capacity."
            )

        placed = False

        for server in servers:

            if sum(server) + workload <= capacity:

                server.append(workload)
                placed = True
                break

        if not placed:
            servers.append([workload])

    return servers


def first_fit_decreasing(workloads, capacity):

    sorted_workloads = sorted(
        workloads, reverse=True
    )

    return first_fit(sorted_workloads, capacity)


def display_servers(title, servers, capacity):

    print("\n", title)
    print("Number of Servers:", len(servers))

    for i, server in enumerate(servers, start=1):

        used = sum(server)
        remaining = capacity - used

        print("Server", i)
        print("Workloads:", server)
        print("Used Capacity:", used)
        print("Remaining Capacity:", remaining)


def task_b4():

    print("\n========== B4: BIN PACKING ==========")

    capacity = 10

    # Normal test
    workloads = [4, 3, 7, 2, 5, 6, 1]

    print("\nNormal Workload Test")
    print("Workloads:", workloads)
    print("Server Capacity:", capacity)

    servers = first_fit(workloads, capacity)

    display_servers(
        "First Fit Result", servers, capacity
    )

    # Challenging test
    challenging = [4, 4, 4, 6, 6, 6]

    print("\nChallenging Workload Test")
    print("Workloads:", challenging)

    servers_ff = first_fit(
        challenging, capacity
    )

    display_servers(
        "First Fit Result", servers_ff, capacity
    )

    servers_ffd = first_fit_decreasing(
        challenging, capacity
    )

    display_servers(
        "First Fit Decreasing Result",
        servers_ffd, capacity
    )


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("=" * 55)
    print("DAA ASSIGNMENT 5 - CO5")
    print("SEARCH, COMPLEXITY AND APPROXIMATION ENGINEERING")
    print("=" * 55)

    task_b1()
    task_b2()
    task_b3()
    task_b4()

    print("\n========== PROGRAM COMPLETED ==========")


if __name__ == "__main__":
    main()
