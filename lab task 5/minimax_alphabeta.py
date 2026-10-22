
import math


def minimax(depth, index, is_max, scores, target, reverse=False):
    if depth == target:
        return scores[index], 1

    best = float('-inf') if is_max else float('inf')
    leaves = 0

    children = (index * 2, index * 2 + 1)
    if reverse:
        children = children[::-1]

    for child in children:
        val, count = minimax(
            depth + 1, child, not is_max, scores, target, reverse
        )
        leaves += count

        if is_max:
            best = max(best, val)
        else:
            best = min(best, val)

    return best, leaves


def alphabeta(depth, index, is_max, scores, target,
              alpha, beta, reverse=False):
    if depth == target:
        return scores[index], 1

    best = float('-inf') if is_max else float('inf')
    leaves = 0

    children = (index * 2, index * 2 + 1)
    if reverse:
        children = children[::-1]

    for child in children:
        val, count = alphabeta(
            depth + 1, child, not is_max, scores, target,
            alpha, beta, reverse
        )
        leaves += count

        if is_max:
            best = max(best, val)
            alpha = max(alpha, best)
        else:
            best = min(best, val)
            beta = min(beta, best)

        if alpha >= beta:
            break

    return best, leaves


scores = [3, 5, 6, 9, 1, 2, 0, -1]
target = int(math.log2(len(scores)))

for reverse in (False, True):
    order = "Right to Left" if reverse else "Left to Right"

    mm_val, mm_leaves = minimax(
        0, 0, True, scores, target, reverse
    )

    ab_val, ab_leaves = alphabeta(
        0, 0, True, scores, target,
        float('-inf'), float('inf'), reverse
    )

    print("Branch Order:", order)
    print("Scores      :", scores)
    print(f"Minimax     : value={mm_val}, leaves={mm_leaves}")
    print(f"Alpha-Beta  : value={ab_val}, leaves={ab_leaves}")
    print()

