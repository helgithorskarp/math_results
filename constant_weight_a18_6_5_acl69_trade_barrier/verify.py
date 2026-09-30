#!/usr/bin/env python3
"""Exact, dependency-free checks of the ACL69 completion/trade certificate.

Point 1 is bit 0. All arithmetic is Python arbitrary-precision integer arithmetic.
Generation via covered triples and checking via pairwise intersection use
different characterizations of the packing constraint.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def word_mask(word):
    require(len(word) == 18 and set(word) <= {"0", "1"}, "malformed seed word")
    require(word.count("1") == 5, "wrong weight")
    return sum(1 << i for i, x in enumerate(word) if x == "1")


def point_mask(points):
    require(len(points) == 5 and len(set(points)) == 5, "bad candidate points")
    require(all(type(i) is int and 1 <= i <= 18 for i in points), "point out of range")
    return sum(1 << (i - 1) for i in points)


def compatible(a, b):
    return (a & b).bit_count() <= 2


def verify_packing(code):
    require(len(code) == len(set(code)), "duplicate code word")
    require(all(b.bit_count() == 5 and b < 1 << 18 for b in code), "bad mask")
    require(all(compatible(a, b) for a, b in combinations(code, 2)), "packing violation")


def triple_masks(block):
    points = [i for i in range(18) if block >> i & 1]
    return tuple(sum(1 << i for i in t) for t in combinations(points, 3))


def verify_radius5(seed, blocks):
    """Exhaust every improving exchange deleting at most five seed words.

    For outsider B let S(B) be its seed blockers. A new independent set T
    requires deleting their union. If |T| exceeds that union's size, T
    itself is an improvement. An improvement with <=5 deletions contains
    a subfamily with <=6 additions satisfying this inequality.
    """
    seed_set = set(seed)
    low = []
    histogram = Counter()
    for b in blocks:
        if b in seed_set:
            continue
        mask = sum(1 << i for i, c in enumerate(seed) if not compatible(b, c))
        histogram[mask.bit_count()] += 1
        if mask.bit_count() <= 5:
            low.append((b, mask))
    counts = Counter()
    neutral = Counter()

    def visit(start, chosen, removed):
        k = len(chosen)
        if k:
            counts[k] += 1
            d = removed.bit_count()
            require(k <= d, "improving exchange found")
            if k == d:
                neutral[d] += 1
        if k == 6:
            return
        for i in range(start, len(low)):
            b, mask = low[i]
            union = removed | mask
            if union.bit_count() > 5 or any(not compatible(b, c) for c in chosen):
                continue
            visit(i + 1, chosen + [b], union)

    visit(0, [], 0)
    return {
        "outsider_blocker_histogram": dict(sorted(histogram.items())),
        "radius5_nodes_by_added_size": dict(sorted(counts.items())),
        "neutral_exchanges_by_exact_removed_size": dict(sorted(neutral.items())),
        "improving_exchanges_with_at_most5_deletions": 0,
    }


def verify_two_core_deletions(core, candidates, parts, blocks):
    """Generate, then definition-check 14-clique covers for all 1596 cases.

    The backtracking generator need not be trusted for optimality or
    completeness: every returned cover is checked for exhaustive vertex
    coverage and for all within-clique conflicts.
    """
    ordered = sorted(core)
    extra = []
    for b in blocks:
        if b in core or b in candidates:
            continue
        blockers = frozenset(c for c in core if not compatible(b, c))
        if len(blockers) <= 2:
            require(blockers, "missing empty-blocker candidate")
            extra.append((b, blockers))
    digest = sha256()
    histogram = Counter()
    cases = 0
    for first, second in combinations(ordered, 2):
        deleted = {first, second}
        new = [b for b, blockers in extra if blockers <= deleted]
        cover = [clique[:] for clique in parts] + [[first], [second]]

        def fill(pending):
            if not pending:
                return True
            domains = [(b, [i for i, clique in enumerate(cover)
                            if all(not compatible(b, a) for a in clique)]) for b in pending]
            b, allowed = min(domains, key=lambda item: (len(item[1]), item[0]))
            rest = [a for a in pending if a != b]
            for i in allowed:
                cover[i].append(b)
                if fill(rest):
                    return True
                cover[i].pop()
            return False

        require(fill(new), "14-clique cover generator failed")
        # Exact residual universe is C0 + deleted core words + outsiders
        # with nonempty core blocker sets contained in the deleted pair.
        residual = set(candidates) | deleted | set(new)
        require(len(cover) == 14, "wrong two-deletion cover size")
        require({b for clique in cover for b in clique} == residual, "two-deletion cover incomplete")
        require(sum(map(len, cover)) == len(residual), "two-deletion cover repeats a block")
        require(all(not compatible(a, b) for clique in cover for a, b in combinations(clique, 2)),
                "two-deletion conflict clique failed")
        record = [first, second, [sorted(clique) for clique in cover]]
        digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
        histogram[len(residual)] += 1
        cases += 1
    require(cases == 1596, "two-deletion case coverage failed")
    return {
        "largest_code_retaining_at_least55_core_words": 69,
        "two_core_deletion_cases": cases,
        "two_core_deletion_candidate_histogram": dict(sorted(histogram.items())),
        "two_core_deletion_cover_sha256": digest.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius5", action="store_true", help="also exhaust seed exchanges with <=5 deletions")
    args = parser.parse_args()
    start = time.perf_counter()
    cert = json.loads((HERE / "certificate.json").read_text())
    raw = (HERE / "acl69.txt").read_bytes()
    require(sha256(raw).hexdigest() == cert["expected_seed_sha256"], "seed hash mismatch")
    seed = [word_mask(s) for s in raw.decode().splitlines()]
    require(len(seed) == 69, "wrong seed size")
    verify_packing(seed)
    removed = cert["removed_seed_rows"]
    require(len(removed) == 12 and len(set(removed)) == 12, "bad removed rows")
    require(all(type(i) is int and 1 <= i <= 69 for i in removed), "bad seed row index")
    core = set(seed[i - 1] for i in range(1, 70) if i not in removed)
    require(len(core) == 57, "wrong core size")
    candidates = [point_mask(x) for x in cert["completion_candidates"]]
    require(len(candidates) == 26 and len(set(candidates)) == 26, "bad candidate list")
    blocks = [sum(1 << i for i in t) for t in combinations(range(18), 5)]
    require(len(blocks) == 8568 and len(set(blocks)) == 8568, "bad block universe")

    # Independently verify exhaustive candidate coverage by the definition.
    direct = {b for b in blocks if b not in core and all(compatible(b, c) for c in core)}
    require(direct == set(candidates), "candidate list is not exhaustive")
    block_triples = {b: triple_masks(b) for b in blocks}
    covered = {t for c in core for t in block_triples[c]}
    triple_generated = {b for b in blocks if b not in core and all(t not in covered for t in block_triples[b])}
    require(triple_generated == direct, "triple-generation comparison failed")

    parts = cert["conflict_cliques"]
    require(len(parts) == 12, "need twelve cliques")
    require(sorted(i for part in parts for i in part) == list(range(1, 27)), "cliques are not a partition")
    for part in parts:
        require(all(not compatible(candidates[i - 1], candidates[j - 1]) for i, j in combinations(part, 2)),
                "listed set is not a conflict clique")

    # A larger construction frontier: retain any 56 of the 57 core words.
    # New words with exactly one core blocker can be added to existing
    # cliques; the removed core word forms a thirteenth singleton clique.
    one_blocker = {c: [] for c in core}
    for b in blocks:
        if b in core or b in direct:
            continue
        blockers = [c for c in core if not compatible(b, c)]
        if len(blockers) == 1:
            one_blocker[blockers[0]].append(b)
    certificate_extensions = cert["one_core_deletion_extensions"]
    require(set(certificate_extensions) == {str(c) for c, extra in one_blocker.items() if extra},
            "one-core extension list is incomplete")
    deletion_candidate_histogram = Counter()
    for c, extra in one_blocker.items():
        cover = [[candidates[i - 1] for i in part] for part in parts] + [[c]]
        if extra:
            records = certificate_extensions[str(c)]
            require({point_mask(r["points"]) for r in records} == set(extra), "extension candidates differ")
            for record in records:
                b = point_mask(record["points"])
                index = record["clique_index"]
                require(type(index) is int and 1 <= index <= 12, "bad extension clique index")
                cover[index - 1].append(b)
        residual = direct | set(extra) | {c}
        require({b for clique in cover for b in clique} == residual, "extension cover incomplete")
        require(sum(map(len, cover)) == len(residual), "extension cover repeats a block")
        require(all(not compatible(a, b) for clique in cover for a, b in combinations(clique, 2)),
                "one-core extension clique is invalid")
        # Exhaustive candidate coverage follows by splitting the core
        # blocker set into empty, singleton {c}, and the removed word c.
        deletion_candidate_histogram[len(residual)] += 1

    two_deletion = verify_two_core_deletions(
        core, candidates, [[candidates[i - 1] for i in part] for part in parts], blocks)

    # An independent family of size 12 has exactly one element per clique.
    # The 2^10 * 3^2 = 9216 choices cover all maximum completions.
    maximum = []
    choices = 0
    for indices in product(*parts):
        choices += 1
        tail = [candidates[i - 1] for i in indices]
        if all(compatible(a, b) for a, b in combinations(tail, 2)):
            code = tuple(sorted(core | set(tail)))
            verify_packing(code)
            maximum.append(code)
    states = set(maximum)
    require(len(states) == len(maximum) == cert["expected_maximum_completions"], "completion count mismatch")
    require(tuple(sorted(seed)) in states, "seed is not among maximum completions")
    require(set.intersection(*(set(s) for s in states)) == core, "common core mismatch")

    # Build component edges from every five-subset using triple ownership.
    # Closure here permits deleting any seed/core word, so it checks the
    # entire one-word neutral-trade component, not just fixed-core moves.
    adjacency = {}
    for state in states:
        owner = {}
        for c in state:
            for t in block_triples[c]:
                require(t not in owner, "triple is covered twice")
                owner[t] = c
        present = set(state)
        neighbors = set()
        for b in blocks:
            if b in present:
                continue
            blockers = {owner[t] for t in block_triples[b] if t in owner}
            require(blockers, "a word can be appended")
            if len(blockers) == 1:
                nxt = tuple(sorted((present - blockers) | {b}))
                require(nxt in states, "component has an unlisted neighbor")
                neighbors.add(nxt)
        adjacency[state] = neighbors
    reachable = {tuple(sorted(seed))}
    queue = list(reachable)
    for state in queue:
        for nxt in adjacency[state]:
            if nxt not in reachable:
                reachable.add(nxt)
                queue.append(nxt)
    require(reachable == states, "maximum completions are not all reachable")
    require(all(a in adjacency[b] for a, neighbors in adjacency.items() for b in neighbors), "nonreciprocal edge")
    edges = sum(map(len, adjacency.values())) // 2
    require(edges == cert["expected_component_edges"], "edge count mismatch")
    serial = json.dumps(sorted(states), separators=(",", ":"))
    digest = sha256(serial.encode()).hexdigest()
    require(digest == cert["expected_component_sha256"], "component hash mismatch")
    out = {
        "agent": "six-code-2",
        "role": "researcher",
        "seed_size": 69,
        "core_size": 57,
        "completion_candidates": 26,
        "conflict_cliques": 12,
        "largest_code_containing_core": 69,
        "largest_code_retaining_at_least56_core_words": 69,
        "one_core_deletion_cases": len(core),
        "one_core_deletion_candidate_histogram": dict(sorted(deletion_candidate_histogram.items())),
        "maximum_completions": len(states),
        "clique_choice_cases": choices,
        "one_word_component_edges": edges,
        "component_sha256": digest,
        "global_A18_6_5_bound_improvement": False,
    }
    out.update(two_deletion)
    if args.radius5:
        exchange = verify_radius5(seed, blocks)
        require({str(k): v for k, v in exchange["radius5_nodes_by_added_size"].items()} ==
                cert["expected_radius5_nodes_by_added_size"], "radius5 coverage mismatch")
        out.update(exchange)
    out["seconds"] = round(time.perf_counter() - start, 6)
    out["max_rss_kib_linux"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
