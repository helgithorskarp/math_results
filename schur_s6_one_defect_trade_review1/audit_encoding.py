"""Independently audit every clause of the ten one-defect trade encodings."""

import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_external_class_trade"
sys.path.insert(0, str(SOURCE))
import verify_one_defect as target  # noqa: E402

N = 537
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def var(vertex, colour):
    return 6 * (vertex - 1) + colour


def z_order_triples():
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            yield tuple(sorted({x, z - x, z}))


def x_order_triples():
    for x in range(1, N // 2 + 1):
        for y in range(x, N - x + 1):
            yield tuple(sorted({x, y, x + y}))


def expect(clauses, position, clause, group):
    if position >= len(clauses) or clauses[position] != clause:
        raise AssertionError(f"{group}: clause {position} differs: expected {clause}")
    return position + 1


def check_group(old, group, triples, manifest):
    free = {v for v in range(1, N + 1) if old[v] in group}
    clauses, free_count, active, variables = target.encode(old, set(group))
    assert len(free) == free_count
    position = 0
    label = "".join(map(str, group))
    for vertex in sorted(free):
        position = expect(clauses, position, [var(vertex, colour) for colour in range(1, 7)], label)
        for c, d in itertools.combinations(range(1, 7), 2):
            position = expect(clauses, position, [-var(vertex, c), -var(vertex, d)], label)

    selectors = []
    for triple in triples:
        moving = [v for v in triple if v in free]
        fixed = [v for v in triple if v not in free]
        possible = [c for c in range(1, 7) if all(old[v] == c for v in fixed)]
        if not possible:
            continue
        selector = 6 * N + len(selectors) + 1
        selectors.append(selector)
        for colour in possible:
            clause = [selector] + [-var(v, colour) for v in moving]
            position = expect(clauses, position, clause, label)
    assert len(selectors) == active

    prefixes = [6 * N + active + i for i in range(1, active)]
    for i, selector in enumerate(selectors):
        if i < len(prefixes):
            position = expect(clauses, position, [-selector, prefixes[i]], label)
        if i > 0:
            position = expect(clauses, position, [-selector, -prefixes[i - 1]], label)
        if 0 < i < len(prefixes):
            position = expect(clauses, position, [-prefixes[i - 1], prefixes[i]], label)
    assert position == len(clauses)
    assert variables == 6 * N + 2 * active - 1
    assert (free_count, active, variables, len(clauses)) == (
        manifest["free"], manifest["active_edges"],
        manifest["variables"], manifest["clauses"],
    )
    return len(clauses)


def main():
    seed_bytes = (SOURCE / "seed537.txt").read_bytes()
    assert hashlib.sha256(seed_bytes).hexdigest() == SEED_SHA256
    word = seed_bytes.decode("ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    old = [0] + [int(c) for c in word]
    assert [word.count(str(c)) for c in range(1, 7)] == [93, 163, 119, 35, 63, 64]
    z_triples = list(z_order_triples())
    x_triples = list(x_order_triples())
    assert len(z_triples) == len(x_triples) == len(set(z_triples)) == 72092
    assert set(z_triples) == set(x_triples)
    defects = [triple for triple in z_triples if len({old[v] for v in triple}) == 1]
    assert defects == [(12, 24), (12, 24, 36)]
    expected = {item["group"]: item for item in json.loads(
        (SOURCE / "expected_one_defect.json").read_text())}
    groups = list(itertools.combinations(range(1, 7), 3))
    groups = [group for group in groups if 4 in group]
    assert len(groups) == len(expected) == 10
    total_clauses = 0
    for group in groups:
        label = "".join(map(str, group))
        total_clauses += check_group(old, group, x_triples, expected[label])
    print("PASS seed_defects=2 triples=72092 groups=10 clauses_checked="
          f"{total_clauses} sequential_counter=all")


if __name__ == "__main__":
    main()
