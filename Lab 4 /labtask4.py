# lab4_graph.py

# Lab 4 input data: the hand-drawn campus graph. Start S, goal G.

GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("S", 1), ("C", 2)],
    "B": [("S", 4), ("G", 5)],
    "C": [("A", 2), ("G", 3)],
    "G": [("B", 5), ("C", 3)],
}

# Heuristic h(n): the number written next to each node in the drawing.
H = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

# Zero heuristic for the UCS control run (h = 0 everywhere).
H_ZERO = {"S": 0, "A": 0, "B": 0, "C": 0, "G": 0}

START = "S"
GOAL = "G"

# lab4_astar.py

# Frontier order: lowest f first. Ties are broken by insertion order (first in, first out).
# Goal test: when a node is taken off the frontier. A node already expanded is "stale".
# from lab4_graph import GRAPH, H, H_ZERO, START, GOAL


def astar(graph, h, start, goal):
    frontier = [(h[start], 0, 0, h[start], [start])]   
    order = 1                                          
    expanded = []                                      
    stale_pops = 0
    trace = []
    while frontier:
        frontier.sort()                                
        f, o, g, hn, path = frontier.pop(0)
        node = path[-1]
        if node in expanded:                          
            stale_pops = stale_pops + 1
            trace.append((node, g, hn, f, "stale, skipped", sorted(frontier)))
            continue
        expanded.append(node)
        if node == goal:
            trace.append((node, g, hn, f, "GOAL", sorted(frontier)))
            return g, path, expanded, stale_pops, trace
        for nxt, w in graph[node]:
            if nxt not in expanded:
                new_g = g + w
                frontier.append((new_g + h[nxt], order, new_g, h[nxt], path + [nxt]))
                order = order + 1
        trace.append((node, g, hn, f, "expanded", sorted(frontier)))
    return None, None, expanded, stale_pops, trace


def path_cost(path):
    # independent check: add the edge costs along a finished path
    total = 0
    parts = []
    for i in range(len(path) - 1):
        for nxt, w in GRAPH[path[i]]:
            if nxt == path[i + 1]:
                parts.append(str(w))
                total = total + w
    return total, " + ".join(parts)


def entry_text(entry):
    f, o, g, hn, path = entry
    return "-".join(path) + " (" + str(g) + "+" + str(hn) + "=" + str(f) + ")"


def frontier_text(frontier):
    return "[" + ", ".join(entry_text(e) for e in frontier) + "]"


def print_trace(trace):
    for step, (node, g, hn, f, status, frontier) in enumerate(trace, 1):
        print("step", step, "| pop", node, "| g =", g, "| h =", hn,
              "| f = " + str(g) + " + " + str(hn) + " = " + str(f), "|", status)
        print("        frontier after:", frontier_text(frontier))


def report(name, h):
    cost, path, expanded, stale, trace = astar(GRAPH, h, START, GOAL)
    print("=== " + name + " ===")
    print_trace(trace)
    total, parts = path_cost(path)
    print("Returned path        :", "-".join(path))
    print("Cost from search     :", cost)
    print("Cost summed separately:", parts, "=", total)
    print("Processing order     :", ", ".join(expanded))
    print("Expansions (goal counted):", len(expanded), "| (goal not counted):", len(expanded) - 1)
    print("Stale entries popped :", stale)
    print("Entries left in frontier at the end:", frontier_text(trace[-1][5]))
    print()
    return path, total, expanded


if __name__ == "__main__":
    print("Task 1 and 2: A* with the supplied heuristic")
    print("h =", H)
    print()
    a_path, a_cost, a_order = report("A* (supplied heuristic)", H)
    u_path, u_cost, u_order = report("UCS control (h = 0)", H_ZERO)
    print("Summary: A* expanded", a_order, "UCS expanded", u_order,
          "| same cost:", a_cost == u_cost)


# lab4_overestimate.py

# Task 3: change ONE heuristic value (h(C)) to an overestimate and rerun A*.
# from lab4_graph import GRAPH, H, H_ZERO, START, GOAL
# from lab4_astar import astar, path_cost, frontier_text


def run(h):
    cost, path, expanded, stale, trace = astar(GRAPH, h, START, GOAL)
    return cost, path, expanded, trace


# true remaining cost from C to G (found with h = 0, so it is exact)
true_cost, true_path, _, _, _ = astar(GRAPH, H_ZERO, "C", GOAL)
print("True remaining cost from C to G:", true_cost, "via", "-".join(true_path))
print("Original h(C) =", H["C"], "(underestimates by", true_cost - H["C"], ")")

H_BAD = dict(H)          # copy, then change ONE value only
H_BAD["C"] = 10
print("Modified h(C) =", H_BAD["C"], "(overestimates by", H_BAD["C"] - true_cost, ")")
print()

for name, h in [("Original heuristic", H), ("Modified heuristic h(C)=10", H_BAD)]:
    cost, path, expanded, trace = run(h)
    print("===", name, "===")
    for step, (node, g, hn, f, status, frontier) in enumerate(trace, 1):
        print("step", step, "| pop", node, "| f = " + str(g) + " + " + str(hn) + " = " + str(f),
              "|", status, "| frontier after:", frontier_text(frontier))
    total, parts = path_cost(path)
    print("Path :", "-".join(path))
    print("Cost :", parts, "=", total)
    print("Processing order:", ", ".join(expanded), "| expansions (goal counted):", len(expanded))
    print()

print("Extra check: only h(C) is changed each time")
print("h(C) | path | cost | processing order")
for value in range(2, 11):
    h = dict(H)
    h["C"] = value
    cost, path, expanded, trace = run(h)
    print(value, "|", "-".join(path), "|", cost, "|", ", ".join(expanded))
