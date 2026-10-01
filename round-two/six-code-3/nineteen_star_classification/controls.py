"""Definition-level, adversarial and incomplete-run controls, not peer review."""
from itertools import combinations
import json
from pathlib import Path
import produce
import verify


def reject(call):
    try:
        call()
    except (ValueError, RuntimeError, KeyError, StopIteration):
        return
    raise RuntimeError("invalid/incomplete control accepted")


def main():
    edges = list(combinations(range(5), 2))
    decisions = 0
    for mask in range(1 << len(edges)):
        neighbors = [set() for _ in range(5)]
        for i, (u, v) in enumerate(edges):
            if (mask >> i) & 1:
                neighbors[u].add(v)
                neighbors[v].add(u)
        bits = [sum(1 << v for v in s) for s in neighbors]
        for k in range(1, 6):
            literal = {q for q in combinations(range(5), k)
                       if all(v in neighbors[u] for u, v in combinations(q, 2))}
            colored, nodes = produce.enumerate_cliques(bits, k)
            maximal, nodes = verify.maximal_cliques(neighbors, k)
            projected = {q for m in maximal for q in combinations(m, k)}
            verify.check(literal == set(colored) == projected, "five-vertex census disagreement")
            decisions += 1
    rejects = 0
    for call in [lambda: produce.enumerate_cliques([2, 1], 1, node_cap=1),
                 lambda: verify.maximal_cliques([{1}, {0}], 1, node_cap=1),
                 lambda: produce.enumerate_cliques([0], 0),
                 lambda: verify.maximal_cliques([set()], 0),
                 lambda: produce.enumerate_cliques([0], 1, node_cap=2000001),
                 lambda: verify.maximal_cliques([set()], 1, seconds=21)]:
        reject(call)
        rejects += 1
    expected = json.loads((Path(__file__).resolve().parent/"expected.json").read_text())
    model = verify.reconstruct((5,))
    cells, anchors, columns, neighbors, holes = model
    q = expected["models"][0]["marked_classes"][0]["clique"]
    words = anchors+[frozenset(columns[i]) for i in q]
    stats, marks = verify.inspect(words)
    verify.check(len(marks) == 1, "positive one-mark control")
    malformed = words.copy()
    malformed[-1] = malformed[0]
    reject(lambda: verify.inspect(malformed))
    malformed2 = words.copy()
    malformed2[-1] = frozenset([17, 18, 19, 20])
    reject(lambda: verify.inspect(malformed2))
    malformed3 = words.copy()
    malformed3[-1] = frozenset([0, 1, 2, 15])
    reject(lambda: verify.inspect(malformed3))
    rejects += 3
    # Exhaust every labelled 5-by-5 binary row/column-degree-two matrix.
    row_holes = list(combinations(range(5), 2))
    counts = {}
    def matrix(rows, degrees):
        if len(rows) == 5:
            if degrees != [2]*5:
                return
            graph = [set() for _ in range(10)]
            for r, cols in enumerate(rows):
                for c in cols:
                    graph[r].add(5+c)
                    graph[5+c].add(r)
            unseen, sizes = set(range(10)), []
            while unseen:
                root = min(unseen)
                reached, pending = {root}, [root]
                while pending:
                    p = pending.pop()
                    for v in graph[p]-reached:
                        reached.add(v)
                        pending.append(v)
                unseen.difference_update(reached)
                sizes.append(len(reached)//2)
            key = tuple(sorted(sizes))
            counts[key] = counts.get(key, 0)+1
            return
        for cols in row_holes:
            next_degrees = degrees.copy()
            for c in cols:
                next_degrees[c] += 1
            if max(next_degrees) <= 2:
                matrix(rows+[cols], next_degrees)
    matrix([], [0]*5)
    verify.check(counts == {(5,): 1440, (2, 3): 600}, "binary matrix coverage")
    print(json.dumps({"status": "COMPLETE", "five_vertex_graphs": 1024,
                      "clique_decisions": decisions, "rejections": rejects,
                      "anchor_matrices": sum(counts.values()),
                      "cycle_type_counts": {str(k): v for k, v in counts.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
