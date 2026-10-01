"""Independent definition-level index-88 audit; no generator/solver import."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_cnf(path):
    lines = path.read_text().splitlines()
    require(bool(lines), "empty CNF")
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "bad CNF header")
    n, m = map(int, header[2:])
    require(n > 0 and m >= 0 and len(lines) == m+1, "bad CNF dimensions")
    clauses = []
    for line in lines[1:]:
        tokens = list(map(int, line.split()))
        require(tokens and tokens[-1] == 0 and 0 not in tokens[:-1], "bad clause terminator")
        require(all(1 <= abs(v) <= n for v in tokens[:-1]), "literal outside domain")
        clauses.append(tuple(tokens[:-1]))
    return n, clauses


def quotient_ids():
    p = 617
    require(all(p % d for d in range(2, 25)), "nonprime field order")
    # x -> x^7 has the order-seven kernel H=<3^88>.
    images = {pow(3, 7*j, p): j for j in range(88)}
    subgroup = {pow(3, 88*j, p) for j in range(7)}
    require(len(images) == 88 and len(subgroup) == 7, "wrong quotient order")
    require(subgroup == {x for x in range(1, p) if pow(x, 7, p) == 1}, "wrong kernel")
    require(pow(3, 308, p) == 616, "root must be a nonsquare")
    return [None] + [images[pow(x, 7, p)] for x in range(1, p)]


def critical_ap(ids=None):
    if ids is None:
        ids = quotient_ids()
    terms = [418+2*j for j in range(7)]
    labels = [ids[x] for x in terms]
    require(terms == [418, 420, 422, 424, 426, 428, 430], "changed critical AP")
    require(labels == [32, 0, 27, 5, 1, 13, 17], "wrong critical AP labels")
    support = sorted(set(labels))
    require(support == [0, 1, 5, 13, 17, 27, 32], "wrong run-bound support")
    for shift in range(88):
        scalar = pow(3, shift, 617)
        positions = [(418+j*2)*scalar % 617 for j in range(7)]
        require(0 not in positions and len(set(positions)) == 7, "degenerate scaled AP")
        require([ids[x] for x in positions] == [(i+shift) % 88 for i in labels],
                "rotation is not field scaling")
    return {"a": 418, "d": 2, "terms": terms, "labels": labels,
            "support": support, "cyclic_run_upper_bound": 32,
            "scaled_rotations_checked": 88}


def direct_edges():
    ids = quotient_ids()
    edges = set()
    retained = removed = 0
    for a in range(617):
        for d in range(1, 617):
            positions = [(a+j*d) % 617 for j in range(7)]
            if 0 in positions:
                removed += 1
            else:
                edges.add(tuple(sorted({ids[x] for x in positions})))
                retained += 1
    require(removed == 4312 and retained == 375760, "incomplete direct AP coverage")
    require(len(edges) == 26488, "wrong punctured edge set")
    require(tuple(critical_ap(ids)["support"]) in edges, "critical AP missing")
    require(Counter(map(len, edges)) == {5: 88, 6: 5280, 7: 21120}, "wrong support ranks")
    # 3 is a nonsquare and H consists of squares, so quotient parity is QR.
    require(all({v % 2 for v in edge} == {0, 1} for edge in edges),
            "an alternating QR orientation violates an AP")
    return edges, retained, removed


def audit(path, length, edges=None):
    require(2 <= length <= 32, "length outside exact nonalternating cover")
    variables, actual = read_cnf(path)
    require(variables == 88, "wrong variable count")
    if edges is None:
        edges, _, _ = direct_edges()
    expected = []
    for edge in edges:
        clause = tuple(x+1 for x in edge)
        expected.extend((clause, tuple(-x for x in clause)))
    # Backwards windows indexed by their terminal position.
    for end in range(88):
        window = tuple((end-j) % 88+1 for j in range(length+1))
        expected.extend((window, tuple(-x for x in window)))
    expected.extend((-x,) for x in range(1, length+1))
    expected.extend(((88,), (length+1,)))
    canonical = lambda clause: tuple(sorted(clause))
    require(Counter(map(canonical, actual)) == Counter(map(canonical, expected)),
            "CNF differs from AP, cyclic-window or normalization constraints")
    require(len(actual) == 53154+length, "wrong number of case clauses")
    return {"longest_run": length, "variables": variables, "clauses": len(actual),
            "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def maximal_cyclic_run(bits):
    n = len(bits)
    starts = [i for i in range(n) if bits[i] != bits[(i-1) % n]]
    if not starts:
        return n
    return max((starts[(j+1) % len(starts)]-start) % n
               for j, start in enumerate(starts))


def cover_controls():
    words = normalized = checked_windows = alternating = 0
    for n in range(2, 12):
        for bits in itertools.product((0, 1), repeat=n):
            words += 1
            longest = maximal_cyclic_run(bits)
            is_alternating = all(bits[i] != bits[(i+1) % n] for i in range(n))
            require((longest == 1) == is_alternating, "alternation/run equivalence failed")
            if is_alternating:
                require(n % 2 == 0, "odd binary cycle alternates")
                alternating += 1
            for upper in range(1, n):
                window_ok = all(len({bits[(i+j) % n] for j in range(upper+1)}) == 2
                                for i in range(n))
                require(window_ok == (longest <= upper), "window/maximal-run equivalence failed")
                checked_windows += 1
            if longest == n or is_alternating:
                continue
            require(longest >= 2, "nonalternating run missing")
            start = next(i for i in range(n)
                         if bits[(i-1) % n] != bits[i]
                         and all(bits[(i+j) % n] == bits[i] for j in range(longest)))
            shifted = tuple(bits[(start+j) % n] ^ bits[start] for j in range(n))
            require(shifted[:longest] == (0,)*longest and shifted[-1] == shifted[longest] == 1,
                    "rotation/complement normalization failed")
            require(maximal_cyclic_run(shifted) == longest, "normalization changed maximum run")
            normalized += 1
    return {"cycle_words_checked": words, "nonconstant_nonalternating_normalizations_checked": normalized,
            "window_equivalences_checked": checked_windows, "alternating_words_checked": alternating}


def audit_cover(work):
    edges, retained, removed = direct_edges()
    cases = [audit(work/f"run-{length}.cnf", length, edges) for length in range(2, 33)]
    require([c["longest_run"] for c in cases] == list(range(2, 33)), "incomplete case cover")
    return {"status": "EXACT_ORDER7_NONALTERNATING_RUN_COVER_AUDITED", "cases": cases,
            "field_edges": len(edges), "rank_histogram": dict(sorted(Counter(map(len, edges)).items())),
            "direct_retained_APs": retained, "direct_zero_APs_removed": removed,
            "critical_AP": critical_ap(), "QR_orientations_checked": 2, "controls": cover_controls()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work", type=Path)
    args = ap.parse_args()
    print(json.dumps(audit_cover(args.work), sort_keys=True))


if __name__ == "__main__":
    main()
