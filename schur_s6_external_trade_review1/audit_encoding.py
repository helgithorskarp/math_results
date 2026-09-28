"""Independent clause-multiset audit of the ten restricted Schur CNFs."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import importlib.util

N = 537
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_external_class_trade"


def load_source():
    spec = importlib.util.spec_from_file_location("source_trade_verify", SOURCE / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edges():
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            yield (x, z) if x == y else (x, y, z)


def literal(v, colour):
    return 6 * (v - 1) + colour


def independent_clauses(word, colours, all_edges):
    free = {v for v in range(1, N + 1) if word[v] in colours}
    clauses = []
    for v in sorted(free):
        clauses.append(tuple(literal(v, c) for c in range(1, 7)))
        clauses.extend((-literal(v, c), -literal(v, d))
                       for c, d in combinations(range(1, 7), 2))
    for vertices in all_edges:
        fixed = {word[v] for v in vertices if v not in free}
        movable = tuple(v for v in vertices if v in free)
        if len(fixed) >= 2:
            continue
        if fixed:
            c = fixed.pop()
            clauses.append(tuple(-literal(v, c) for v in movable))
        else:
            clauses.extend(tuple(-literal(v, c) for v in vertices)
                           for c in range(1, 7))
    return Counter(clauses), len(free), len(clauses)


def main():
    source = load_source()
    word = source.load_seed()
    all_edges = tuple(edges())
    if len(all_edges) != 72092 or len(set(all_edges)) != 72092:
        raise ValueError("edge coverage failure")
    groups = ("124", "134", "145", "146", "234",
              "245", "246", "345", "346", "456")
    expected_free = (291, 247, 191, 192, 317, 261, 262, 217, 218, 162)
    expected_clauses = (111946, 87065, 58777, 59162, 129882,
                        90627, 91377, 69512, 70480, 45720)
    for group, free_expected, clauses_expected in zip(
            groups, expected_free, expected_clauses):
        palette = {int(c) for c in group}
        independent, free, count = independent_clauses(word, palette, all_edges)
        source_clauses, source_free = source.encode(word, palette)
        if (independent != Counter(tuple(c) for c in source_clauses)
                or free != source_free
                or free != free_expected
                or count != clauses_expected):
            raise ValueError(f"group {group}: formula mismatch")
        print(f"{group}: clauses={count} free={free} exact_multiset_match=yes")
    print("PASS ten_restricted_cnfs=10 schur_edges=72092")


if __name__ == "__main__":
    main()
