"""Definition-level audit: every (a,d), Euler quotient labels, all 17 cases.

No generator or solver import. Explicit requirements also run under python -O.
"""
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
    # Kernel of x -> x^8 is H. No discrete logarithm computation here.
    image_to_id = {pow(3, 8*j, p): j for j in range(77)}
    subgroup = {pow(3, 77*j, p) for j in range(8)}
    require(len(image_to_id) == 77 and len(subgroup) == 8, "wrong quotient order")
    require(subgroup == {x for x in range(1, p) if pow(x, 8, p) == 1}, "wrong kernel")
    require(pow(3, 308, p) == 616, "root must be a nonsquare")
    return [None] + [image_to_id[pow(x, 8, p)] for x in range(1, p)]


def critical_ap(ids=None):
    if ids is None:
        ids = quotient_ids()
    terms = [3+34*j for j in range(7)]
    labels = [ids[x] for x in terms]
    require(terms == [3, 37, 71, 105, 139, 173, 207], "changed critical AP")
    require(labels == [1, 8, 1, 2, 0, 18, 8], "wrong critical AP labels")
    support = sorted(set(labels))
    require(support == [0, 1, 2, 8, 18], "wrong run-bound support")
    # Audit all 77 rotations as actual field progressions, not just supports.
    for shift in range(77):
        scalar = pow(3, shift, 617)
        positions = [(3+j*34)*scalar % 617 for j in range(7)]
        require(0 not in positions and len(set(positions)) == 7, "degenerate scaled AP")
        require([ids[x] for x in positions] == [(i+shift) % 77 for i in labels],
                "rotation is not field scaling")
    return {"a": 3, "d": 34, "terms": terms, "labels": labels,
            "support": support, "cyclic_run_upper_bound": 18,
            "scaled_rotations_checked": 77}


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
    require(len(edges) == 23177, "wrong punctured edge set")
    require(tuple(critical_ap(ids)["support"]) in edges, "critical AP missing")
    return edges, retained, removed


def normalize_clause(clause):
    return tuple(sorted(clause))


def audit(path, length, edges=None):
    require(2 <= length <= 18, "length outside exact cover")
    variables, actual = read_cnf(path)
    require(variables == 77, "wrong variable count")
    if edges is None:
        edges, _, _ = direct_edges()
    expected = []
    for edge in edges:
        variables_for_edge = tuple(x+1 for x in edge)
        expected.extend((variables_for_edge, tuple(-x for x in variables_for_edge)))
    # Construct the windows backwards, with the terminal position as index.
    for end in range(77):
        window = tuple((end-j) % 77+1 for j in range(length+1))
        expected.extend((window, tuple(-x for x in window)))
    expected.extend((-x,) for x in range(1, length+1))
    expected.extend(((77,), (length+1,)))
    require(Counter(map(normalize_clause, actual)) == Counter(map(normalize_clause, expected)),
            "CNF differs from exact AP, cyclic-window or normalization constraints")
    require(len(actual) == 46510+length, "wrong number of case clauses")
    return {"longest_run": length, "variables": variables, "clauses": len(actual),
            "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def maximal_cyclic_run(bits):
    # Independent transition-based run decomposition, including wraparound.
    n = len(bits)
    starts = [i for i in range(n) if bits[i] != bits[(i-1) % n]]
    if not starts:
        return n
    return max((starts[(j+1) % len(starts)]-start) % n
               for j, start in enumerate(starts))


def cover_controls():
    words = normalized = checked_windows = 0
    for n in (3, 5, 7, 9, 11):
        for bits in itertools.product((0, 1), repeat=n):
            words += 1
            longest = maximal_cyclic_run(bits)
            require(longest >= 2, "odd cycle unexpectedly alternates")
            for upper in range(1, n):
                window_ok = all(len({bits[(i+j) % n] for j in range(upper+1)}) == 2
                                for i in range(n))
                require(window_ok == (longest <= upper), "window/maximal-run equivalence failed")
                checked_windows += 1
            if longest == n:
                continue  # constants are excluded by the explicit critical AP
            start = next(i for i in range(n)
                         if bits[(i-1) % n] != bits[i]
                         and all(bits[(i+j) % n] == bits[i] for j in range(longest)))
            shifted = tuple(bits[(start+j) % n] ^ bits[start] for j in range(n))
            require(shifted[:longest] == (0,)*longest and shifted[-1] == shifted[longest] == 1,
                    "rotation/complement normalization failed")
            require(maximal_cyclic_run(shifted) == longest, "normalization changed maximum run")
            normalized += 1
    return {"odd_cycle_words_checked": words, "nonconstant_normalizations_checked": normalized,
            "window_equivalences_checked": checked_windows}


def audit_cover(work):
    edges, retained, removed = direct_edges()
    cases = [audit(work/f"run-{length}.cnf", length, edges) for length in range(2, 19)]
    require([c["longest_run"] for c in cases] == list(range(2, 19)), "incomplete case cover")
    return {"status": "EXACT_ORDER8_LONGEST_RUN_COVER_AUDITED", "cases": cases,
            "field_edges": len(edges),
            "rank_histogram": dict(sorted(Counter(map(len, edges)).items())),
            "direct_retained_APs": retained, "direct_zero_APs_removed": removed,
            "critical_AP": critical_ap(), "controls": cover_controls()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work", type=Path)
    args = ap.parse_args()
    print(json.dumps(audit_cover(args.work), sort_keys=True))


if __name__ == "__main__":
    main()
