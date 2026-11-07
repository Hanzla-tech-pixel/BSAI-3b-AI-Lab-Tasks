# Lab 3 input data: the A-G graph, start A, goal G.
# The order of each list is the successor order used by every search.
GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}

# Edge weights (synthetic lab values). Each corridor is two-way.
WEIGHTS = {
    ("A", "B"): 2,
    ("A", "C"): 5,
    ("B", "D"): 4,
    ("B", "E"): 2,
    ("C", "F"): 6,
    ("E", "F"): 3,
    ("F", "G"): 2,
}

START = "A"
GOAL = "G"




# lab3_bfs_dfs.py

# python
# from lab3_graph import GRAPH, START, GOAL
# task 1

def show(paths):
    return "[" + ", ".join("-".join(p) for p in paths) + "]"


def bfs(graph, start, goal):
    frontier = [[start]]            # a queue of paths
    visited = []
    steps = []
    step = 0
    while frontier:
        path = frontier.pop(0)      # queue: take from the FRONT
        node = path[-1]
        step += 1
        if node in visited:
            steps.append((step, path, "skipped (already visited)", list(frontier)))
            continue
        visited.append(node)
        if node == goal:
            steps.append((step, path, "GOAL", list(frontier)))
            return path, visited, steps
        for nxt in graph[node]:
            if nxt not in visited:
                frontier.append(path + [nxt])
        steps.append((step, path, "processed", list(frontier)))
    return None, visited, steps


def dfs(graph, start, goal):
    frontier = [[start]]            # a stack of paths
    visited = []
    steps = []
    step = 0
    while frontier:
        path = frontier.pop()       # stack: took from the END
        node = path[-1]
        step += 1
        if node in visited:
            steps.append((step, path, "skipped (already visited)", list(frontier)))
            continue
        visited.append(node)
        if node == goal:
            steps.append((step, path, "GOAL", list(frontier)))
            return path, visited, steps
        # pushed in reverse so the FIRST successor is explored first
        for nxt in reversed(graph[node]):
            if nxt not in visited:
                frontier.append(path + [nxt])
        steps.append((step, path, "processed", list(frontier)))
    return None, visited, steps


def print_trace(name, steps, frontier_name):
    print(name)
    print("step | popped path | result | " + frontier_name + " after the step")
    for step, path, result, frontier in steps:
        print(step, "|", "-".join(path), "|", result, "|", show(frontier))


# Results worked out by hand BEFORE running the code
MANUAL = {
    "BFS": (["A", "C", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"]),
    "DFS": (["A", "B", "E", "F", "G"], ["A", "B", "D", "E", "F", "C", "G"]),
}

if __name__ == "__main__":
    for name, function, frontier_name in [("BFS", bfs, "queue"), ("DFS", dfs, "stack (top is on the right)")]:
        path, visited, steps = function(GRAPH, START, GOAL)
        print_trace(name, steps, frontier_name)
        print("Final path :", "-".join(path))
        print("Visit order:", ", ".join(visited))
        print("Matches manual trace:", (path, visited) == MANUAL[name])
        print()




#         lab3_depth_search.py  task 2

# python
# from lab3_graph import GRAPH, START, GOAL


def dls(graph, node, goal, limit, path, counter):
    counter[0] = counter[0] + 1            # count every node we visit
    if node == goal:
        return "FOUND", path
    if limit == 0:
        return "CUTOFF", None              # depth limit reached
    cutoff = False
    for nxt in graph[node]:
        if nxt in path:                    # cycle check: current path only
            continue
        status, result = dls(graph, nxt, goal, limit - 1, path + [nxt], counter)
        if status == "FOUND":
            return "FOUND", result
        if status == "CUTOFF":
            cutoff = True
    if cutoff:
        return "CUTOFF", None
    return "FAILURE", None                 # everything below was searched


def iddfs(graph, start, goal, max_depth):
    attempts = []                          # (limit, status, nodes visited)
    for limit in range(1, max_depth + 1):
        counter = [0]
        status, path = dls(graph, start, goal, limit, [start], counter)
        attempts.append((limit, status, counter[0]))
        if status == "FOUND":
            return "FOUND", path, attempts
        if status == "FAILURE":
            return "FAILURE", None, attempts
    return "CUTOFF", None, attempts


def text(path):
    return "-".join(path) if path else "none"


if __name__ == "__main__":
    print("DLS on goal", GOAL)
    for limit in [1, 2, 3, 4]:
        counter = [0]
        status, path = dls(GRAPH, START, GOAL, limit, [START], counter)
        print("limit", limit, "| status", status, "| path", text(path), "| nodes visited", counter[0])

    print()
    print("IDDFS on goal", GOAL)
    for max_depth in [1, 2, 3, 4]:
        status, path, attempts = iddfs(GRAPH, START, GOAL, max_depth)
        limits = [a[0] for a in attempts]
        per_limit = [a[2] for a in attempts]
        print("max depth", max_depth, "| status", status, "| path", text(path),
              "| limits attempted", limits, "| nodes per limit", per_limit,
              "| total nodes", sum(per_limit))

    print()
    print("Edge case: goal H is not connected to the graph")
    for limit in [4, 5, 6]:
        counter = [0]
        status, path = dls(GRAPH, START, "H", limit, [START], counter)
        print("DLS limit", limit, "| status", status)
    status, path, attempts = iddfs(GRAPH, START, "H", 7)
    print("IDDFS max depth 7 | status", status, "| limits attempted", [a[0] for a in attempts])



#     lab3_ucs.py task 3

# python
# from lab3_graph import GRAPH, WEIGHTS, START, GOAL
# from lab3_bfs_dfs import bfs


def edge_cost(a, b):
    # every corridor is two-way, so look the pair up in either order
    if (a, b) in WEIGHTS:
        return WEIGHTS[(a, b)]
    return WEIGHTS[(b, a)]


def ucs(graph, start, goal):
    frontier = [(0, [start])]       # (cost so far, path)
    visited = []
    steps = []
    step = 0
    while frontier:
        cost, path = frontier.pop(0)    # frontier is sorted: cheapest first
        node = path[-1]
        step += 1
        if node in visited:
            steps.append((step, cost, path, "skipped (already visited)", list(frontier)))
            continue
        visited.append(node)
        if node == goal:
            steps.append((step, cost, path, "GOAL", list(frontier)))
            return cost, path, visited, steps
        for nxt in graph[node]:
            if nxt not in visited:
                frontier.append((cost + edge_cost(node, nxt), path + [nxt]))
        frontier.sort()                 # sort by cost
        steps.append((step, cost, path, "processed", list(frontier)))
    return None, None, visited, steps


def path_cost(path):
    # independent check: add up the edge weights of a finished path
    total = 0
    parts = []
    for i in range(len(path) - 1):
        w = edge_cost(path[i], path[i + 1])
        parts.append(str(w))
        total = total + w
    return total, " + ".join(parts)


def show(frontier):
    return "[" + ", ".join(str(c) + ":" + "-".join(p) for c, p in frontier) + "]"


if __name__ == "__main__":
    print("Weighted edges:")
    for (a, b), w in WEIGHTS.items():
        print("  ", a, "-", b, "=", w)
    print()

    cost, path, visited, steps = ucs(GRAPH, START, GOAL)
    print("UCS trace (cost:path)")
    for step, c, p, result, frontier in steps:
        print(step, "| popped", str(c) + ":" + "-".join(p), "|", result, "| frontier after", show(frontier))
    print("UCS path        :", "-".join(path), "| hops", len(path) - 1)
    print("UCS cost (search):", cost)
    total, parts = path_cost(path)
    print("UCS cost (re-added):", parts, "=", total)
    print("Processing order:", ", ".join(visited))
    print()

    bfs_path, bfs_visited, bfs_steps = bfs(GRAPH, START, GOAL)
    total2, parts2 = path_cost(bfs_path)
    print("BFS path on the same topology:", "-".join(bfs_path), "| hops", len(bfs_path) - 1)
    print("BFS path cost:", parts2, "=", total2)
    print("UCS cost", total, "<= BFS cost", total2, ":", total <= total2)