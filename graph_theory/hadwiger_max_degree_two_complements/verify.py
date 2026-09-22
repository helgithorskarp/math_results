#!/usr/bin/env python3
"""Exact audit for complements of disjoint unions of paths and cycles.

The universal theorem is proved in THEOREM.md.  This program independently
checks the constructions and all small boundary obstructions from definitions.
It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path


Component = tuple[str, int]
Signature = tuple[Component, ...]

EXCEPTION_CORES: frozenset[Signature] = frozenset(
    {
        (("C", 3),),
        (("C", 4),),
        (("P", 4),),
        (("P", 5),),
        (("P", 2), ("C", 5)),
        (("P", 3), ("C", 5)),
        (("P", 2), ("C", 6)),
        (("P", 3), ("C", 6)),
    }
)


def component_key(c: Component) -> tuple[int, str]:
    return (c[1], c[0])


def normalized(parts: list[Component] | tuple[Component, ...]) -> Signature:
    return tuple(sorted(parts, key=component_key))


def without_isolates(sig: Signature) -> Signature:
    return tuple(c for c in sig if c != ("P", 1))


def is_exception(sig: Signature) -> bool:
    return without_isolates(sig) in EXCEPTION_CORES


def component_signatures(total: int) -> list[Signature]:
    """Every unlabeled max-degree-two graph signature of a fixed order."""
    types = [("P", m) for m in range(1, total + 1)]
    types += [("C", m) for m in range(3, total + 1)]
    types = sorted(types, key=component_key)
    answer: list[Signature] = []

    def visit(remaining: int, first: int, acc: list[Component]) -> None:
        if remaining == 0:
            answer.append(tuple(acc))
            return
        for i in range(first, len(types)):
            c = types[i]
            if c[1] > remaining:
                break
            acc.append(c)
            visit(remaining - c[1], i, acc)
            acc.pop()

    visit(total, 0, [])
    return answer


def build_graph(sig: Signature) -> tuple[list[set[int]], list[tuple[Component, list[int]]]]:
    n = sum(m for _, m in sig)
    adj = [set() for _ in range(n)]
    components: list[tuple[Component, list[int]]] = []
    start = 0
    for kind, m in sig:
        vertices = list(range(start, start + m))
        components.append(((kind, m), vertices))
        for i in range(m - 1):
            u, v = vertices[i], vertices[i + 1]
            adj[u].add(v)
            adj[v].add(u)
        if kind == "C":
            if m < 3:
                raise ValueError("cycles have order at least three")
            u, v = vertices[-1], vertices[0]
            adj[u].add(v)
            adj[v].add(u)
        start += m
    return adj, components


def independence_number(sig: Signature) -> int:
    return sum((m + 1) // 2 if kind == "P" else m // 2 for kind, m in sig)


def canonical_set(components: list[tuple[Component, list[int]]]) -> set[int]:
    stable: set[int] = set()
    for (kind, m), vertices in components:
        if kind == "P" or m % 2 == 0:
            positions = range(0, m, 2)
        else:
            positions = range(0, m - 1, 2)
        stable.update(vertices[i] for i in positions)
    return stable


def forbidden_graph(
    h_adj: list[set[int]], stable: set[int]
) -> tuple[list[int], set[tuple[int, int]]]:
    residual = sorted(set(range(len(h_adj))) - stable)
    edges: set[tuple[int, int]] = set()
    for u, v in combinations(residual, 2):
        if v in h_adj[u]:
            edges.add((u, v))
    residual_set = set(residual)
    for x in stable:
        nbrs = sorted(h_adj[x] & residual_set)
        for u, v in combinations(nbrs, 2):
            edges.add((u, v))
    return residual, edges


def maximum_allowed_matching(
    vertices: list[int], forbidden: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Maximum matching where every non-forbidden pair is allowed."""
    vertices = sorted(vertices)
    n = len(vertices)

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[tuple[int, int], ...]:
        if mask == 0:
            return ()
        i = (mask & -mask).bit_length() - 1
        best = solve(mask & ~(1 << i))
        u = vertices[i]
        rest = mask & ~(1 << i)
        jmask = rest
        while jmask:
            j = (jmask & -jmask).bit_length() - 1
            v = vertices[j]
            edge = (min(u, v), max(u, v))
            if edge not in forbidden:
                candidate = (edge,) + solve(rest & ~(1 << j))
                if len(candidate) > len(best) or (
                    len(candidate) == len(best) and candidate < best
                ):
                    best = candidate
            jmask &= jmask - 1
        return best

    return list(solve((1 << n) - 1))


def complement_adj(h_adj: list[set[int]]) -> list[set[int]]:
    all_vertices = set(range(len(h_adj)))
    return [all_vertices - {u} - h_adj[u] for u in range(len(h_adj))]


def connected(adj: list[set[int]], block: set[int]) -> bool:
    if not block:
        return False
    seen = {next(iter(block))}
    stack = list(seen)
    while stack:
        u = stack.pop()
        for v in adj[u] & block - seen:
            seen.add(v)
            stack.append(v)
    return seen == block


def verify_minor(h_adj: list[set[int]], branches: list[set[int]]) -> bool:
    g_adj = complement_adj(h_adj)
    used: set[int] = set()
    for block in branches:
        if not block or used & block or not connected(g_adj, block):
            return False
        used |= block
    for i, left in enumerate(branches):
        for right in branches[i + 1 :]:
            if not any(v in g_adj[u] for u in left for v in right):
                return False
    return True


def local_model(kind: str, vertices: list[int]) -> list[set[int]]:
    """Explicit lower models used by the eight exceptional cores."""
    m = len(vertices)
    v = vertices
    if (kind, m) == ("P", 1):
        return [{v[0]}]
    if (kind, m) == ("P", 2):
        return [{v[0]}]
    if (kind, m) == ("P", 3):
        return [{v[0]}, {v[2]}]
    if (kind, m) == ("P", 4):
        return [{v[0]}, {v[2]}]
    if (kind, m) == ("P", 5):
        return [{v[0]}, {v[2]}, {v[4]}]
    if (kind, m) == ("C", 3):
        return [{v[0]}]
    if (kind, m) == ("C", 4):
        return [{v[0]}, {v[2]}]
    if (kind, m) == ("C", 5):
        return [{v[0]}, {v[2]}, {v[1], v[3], v[4]}]
    if (kind, m) == ("C", 6):
        return [{v[0]}, {v[2]}, {v[4]}, {v[1], v[3], v[5]}]
    raise ValueError(f"no local model for {(kind, m)}")


def certificate(sig: Signature) -> list[set[int]]:
    h_adj, components = build_graph(sig)
    a = independence_number(sig)
    upper = (len(h_adj) + a) // 2
    if is_exception(sig):
        branches: list[set[int]] = []
        for (kind, _), vertices in components:
            branches.extend(local_model(kind, vertices))
        assert len(branches) == upper - 1
        return branches

    core = without_isolates(sig)
    if core in {(("C", 5),), (("C", 6),)}:
        branches = []
        for (kind, _), vertices in components:
            branches.extend(local_model(kind, vertices))
        assert len(branches) == upper
        return branches

    stable = canonical_set(components)
    residual, forbidden = forbidden_graph(h_adj, stable)
    matching = maximum_allowed_matching(residual, forbidden)
    branches = [{x} for x in sorted(stable)]
    branches.extend({u, v} for u, v in matching)
    assert len(branches) == upper
    return branches


def independent(h_adj: list[set[int]], vertices: set[int]) -> bool:
    return all(v not in h_adj[u] for u, v in combinations(sorted(vertices), 2))


def perfect_pairings(vertices: tuple[int, ...]):
    if not vertices:
        yield []
        return
    u = vertices[0]
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_pairings(rest):
            yield [{u, v}] + tail


def equality_model_exists(sig: Signature) -> bool:
    """Raw audit of equality models forced by the counting upper bound."""
    h_adj, _ = build_graph(sig)
    a = independence_number(sig)
    vertices = set(range(len(h_adj)))
    for subset in combinations(range(len(h_adj)), a):
        stable = set(subset)
        if not independent(h_adj, stable):
            continue
        residual = tuple(sorted(vertices - stable))
        for pairs in perfect_pairings(residual):
            branches = [{x} for x in sorted(stable)] + pairs
            if verify_minor(h_adj, branches):
                return True
    return False


def auxiliary_failure_signatures(limit: int = 10) -> dict[str, list[str]]:
    failures: dict[str, list[str]] = {}
    for n in range(1, limit + 1):
        for sig in component_signatures(n):
            # Here sig itself describes an arbitrary max-degree-two F.
            f_adj, _ = build_graph(sig)
            f_edges = {
                (u, v) for u in range(n) for v in f_adj[u] if u < v
            }
            matching = maximum_allowed_matching(list(range(n)), f_edges)
            if len(matching) < n // 2:
                failures.setdefault(str(n), []).append(signature_text(sig))
    return failures


def signature_text(sig: Signature) -> str:
    counts: dict[Component, int] = {}
    for c in sig:
        counts[c] = counts.get(c, 0) + 1
    pieces = []
    for (kind, m), count in sorted(counts.items(), key=lambda item: component_key(item[0])):
        token = f"{kind}{m}"
        pieces.append(token if count == 1 else f"{count}{token}")
    return "+".join(pieces)


def audit(max_order: int = 16) -> dict[str, object]:
    records: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    exception_instances = 0
    for n in range(1, max_order + 1):
        signatures = component_signatures(n)
        counts[str(n)] = len(signatures)
        for sig in signatures:
            h_adj, _ = build_graph(sig)
            a = independence_number(sig)
            upper = (n + a) // 2
            claimed = upper - int(is_exception(sig))
            branches = certificate(sig)
            if len(branches) != claimed or not verify_minor(h_adj, branches):
                raise AssertionError(f"bad certificate for {signature_text(sig)}")
            if is_exception(sig):
                exception_instances += 1
            records.append(
                {
                    "signature": signature_text(sig),
                    "n": n,
                    "alpha": a,
                    "upper": upper,
                    "claimed": claimed,
                    "branches": [sorted(b) for b in branches],
                }
            )

    exceptional_audit: dict[str, bool] = {}
    for core in sorted(EXCEPTION_CORES, key=lambda s: (sum(x[1] for x in s), s)):
        text = signature_text(core)
        has_equality = equality_model_exists(core)
        exceptional_audit[text] = has_equality
        if has_equality:
            raise AssertionError(f"unexpected equality model for {text}")

    failures = auxiliary_failure_signatures()
    expected_failures = {"2": ["P2"], "3": ["C3"], "4": ["P1+C3"]}
    if failures != expected_failures:
        raise AssertionError((failures, expected_failures))

    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return {
        "audit_max_order": max_order,
        "component_signature_counts": counts,
        "exception_instances_through_bound": exception_instances,
        "exceptional_core_equality_models": exceptional_audit,
        "auxiliary_matching_failures_through_order_10": failures,
        "certificate_record_sha256": hashlib.sha256(encoded).hexdigest(),
        "status": "ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=16)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.max_order)
    if args.check_expected:
        expected_path = Path(__file__).with_name("EXPECTED_OUTPUT.json")
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit(
                "computed summary differs from EXPECTED_OUTPUT.json\n"
                + json.dumps(result, indent=2, sort_keys=True)
            )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
