#!/usr/bin/env python3
"""Independent direct-complex and asynchronous AC-3 audit of h3911.

This checker imports no code from the reviewed package.  It reconstructs every
Galois action directly in the modular complex coordinate, builds the relaxed
edge CSP, reaches arc consistency with a queue, and checks the disjoint-domain
lower-bound witness.
"""

import argparse
import hashlib
import json
from collections import Counter, deque
from math import gcd
from pathlib import Path


REVIEWED_MANIFEST_SHA256 = (
    "17d1c67fa46c6b3b29a46a3b7faef7fa134c17320ac908506a95881950f0806f"
)
SOURCE_SHA256 = (
    "201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d"
)
EXPECTED_ROWS_SHA256 = (
    "a44ff4236832ca6b4eb14a39c27cdc9b4eb2858bb01c8a780c30cb81e839ced8"
)
EXPECTED_SITES_SHA256 = (
    "b44f53dd1feeab0653f4b57b46aa1cad13f11d9593cad3ef0ef686f9795b041a"
)
EXPECTED_FINAL_SHA256 = (
    "2f4db6e0a7ba543f04ffd1df3ed2695c245703d35e86beff9763ac1da26fad10"
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def object_sha256(value):
    raw = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def is_prime_64(n):
    """Deterministic Miller--Rabin for n below 2**64."""
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            return n == prime
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def unique(values):
    return list(dict.fromkeys(values))


def construct_action(source, prime, root, sqrt5):
    """Evaluate Haugland's complex formulas for one field action."""
    inv8 = pow(8, -1, prime)
    w = pow(root, 7, prime)
    d6 = (pow(root, 6, prime) - pow(root, -6, prime)) % prime
    d12 = (pow(root, 12, prime) - pow(root, -12, prime)) % prime
    need(d6 and d12, "vanishing localized denominator")
    b = ((w - 1) * pow(d6, -1, prime) + w * pow(d12, -1, prime)) % prime
    vectors = [value for j in range(42)
               for value in (pow(root, j, prime), b * pow(root, j, prime) % prime)]

    points = [0]
    for path in source["paths"]:
        z = 0
        for step in path:
            need(type(step) is int and 0 <= step < 84, "invalid path step")
            z = (z + vectors[step]) % prime
            points.append(z)
        need(z == (2 * w - 1) % prime, "path endpoint mismatch")
    g1 = unique(points)
    g2 = unique([
        (pow(w, -1, prime) * z - 1) % prime for z in g1
    ] + [
        (w * z + 1) % prime for z in g1
    ])
    scale = (7 + (2 * w - 1) * sqrt5) * inv8 % prime
    g3 = unique(g2 + [(scale * (z + 1) - 1) % prime for z in g2])
    need([len(g1), len(g2), len(g3)] == [740, 1066, 2131],
         "action point counts differ")
    return g3, vectors


def reconstruct(source, certificate):
    p = certificate["prime"]
    root = certificate["root42"]
    square = certificate["sqrt5"]
    need(is_prime_64(p), "modulus is not prime")
    need(pow(root, 42, p) == 1 and
         all(pow(root, 42 // q, p) != 1 for q in (2, 3, 7)),
         "root does not have exact order 42")
    need(square * square % p == 5, "incorrect square root of five")
    # Phi_42 is X^12+X^11-X^9-X^8+X^6-X^4-X^3+X+1.
    phi = (pow(root, 12, p) + pow(root, 11, p) - pow(root, 9, p) -
           pow(root, 8, p) + pow(root, 6, p) - pow(root, 4, p) -
           pow(root, 3, p) + root + 1) % p
    need(phi == 0, "root does not satisfy Phi_42")

    actions = [(a, sign) for a in range(42) if gcd(a, 42) == 1
               for sign in (1, -1)]
    need(len(actions) == 24, "Galois action count")
    evaluations = []
    direction_evaluations = []
    for exponent, sign in actions:
        points, vectors = construct_action(
            source, p, pow(root, exponent, p), sign * square % p
        )
        need(len(vectors) == 84, "unit-vector count")
        evaluations.append(points)
        direction_evaluations.append(vectors)

    index = {action: i for i, action in enumerate(actions)}
    conjugate = [index[((-a) % 42, sign)] for a, sign in actions]
    edges = [tuple(edge) for edge in source["G3_edges"]]
    need(len(edges) == 12530 and len(edges) == len(set(edges)) and
         edges == sorted(edges) and
         all(len(edge) == 2 and 0 <= edge[0] < edge[1] < 2131 for edge in edges),
         "source edge count or uniqueness")
    for direction in range(84):
        for k in range(24):
            need(direction_evaluations[k][direction] *
                 direction_evaluations[conjugate[k]][direction] % p == 1,
                 "modular unit direction failure")
    for u, v in edges:
        for k in range(24):
            delta = (evaluations[k][u] - evaluations[k][v]) % p
            conjugate_delta = (
                evaluations[conjugate[k]][u] - evaluations[conjugate[k]][v]
            ) % p
            need(delta * conjugate_delta % p == 1, "modular source edge failure")
    rows = [tuple(evaluations[k][v] for k in range(24)) for v in range(2131)]
    need(object_sha256(rows) == EXPECTED_ROWS_SHA256, "action-row stream differs")
    return rows, actions, edges


def build_domains(rows, actions):
    index = {action: i for i, action in enumerate(actions)}
    permutations = [
        [index[(a * c % 42, sign * other)] for c, other in actions]
        for a, sign in actions
    ]
    sites = []
    lookup = {}
    domains = []
    for row in rows:
        domain = set()
        for permutation in permutations:
            image = tuple(row[k] for k in permutation)
            if image not in lookup:
                lookup[image] = len(sites)
                sites.append(image)
            domain.add(lookup[image])
        domains.append(tuple(sorted(domain)))
    need(len(sites) == 6049 and len(set(domains)) == 355,
         "site or orbit count differs")
    need(object_sha256(sites) == EXPECTED_SITES_SHA256, "site stream differs")
    identity = [lookup[row] for row in rows]
    return sites, domains, identity, permutations


def compatibility_tables(sites, domains, edges, prime, actions):
    index = {action: i for i, action in enumerate(actions)}
    conjugate = [index[((-a) % 42, sign)] for a, sign in actions]

    def modular_unit(i, j):
        left, right = sites[i], sites[j]
        return all(
            (left[k] - right[k]) *
            (left[conjugate[k]] - right[conjugate[k]]) % prime == 1
            for k in range(24)
        )

    tables = {}
    for u, v in edges:
        first, second = domains[u], domains[v]
        if (first, second) in tables:
            continue
        forward = {
            i: sum(1 << j for j in second if modular_unit(i, j))
            for i in first
        }
        reverse = {
            j: sum(1 << i for i in first if forward[i] >> j & 1)
            for j in second
        }
        tables[first, second] = forward
        tables[second, first] = reverse
    return tables


def members(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def ac3(domains, edges, tables, anchor, anchor_image):
    current = [sum(1 << site for site in domain) for domain in domains]
    current[anchor] = 1 << anchor_image
    neighbors = [set() for _ in domains]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    queue = deque((u, v) for u, v in edges for u, v in ((u, v), (v, u)))
    revisions = 0
    removed = 0
    while queue:
        u, v = queue.popleft()
        relation = tables[domains[u], domains[v]]
        revised = sum(
            1 << image for image in members(current[u])
            if relation[image] & current[v]
        )
        if revised == current[u]:
            continue
        need(revised, "AC-3 emptied a domain")
        removed += current[u].bit_count() - revised.bit_count()
        current[u] = revised
        revisions += 1
        queue.extend((w, u) for w in neighbors[u] if w != v)
    return current, revisions, removed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reviewed_source", type=Path)
    args = parser.parse_args()
    package = args.reviewed_source
    need(file_sha256(package / "SHA256SUMS") == REVIEWED_MANIFEST_SHA256,
         "reviewed package manifest differs")
    graph_path = package.parent / "hadwiger_nelson_haugland2131_exact_reproduction" / "graph.json"
    need(file_sha256(graph_path) == SOURCE_SHA256, "archived graph input differs")
    source = json.loads(graph_path.read_text())
    certificate = json.loads((package / "certificate.json").read_text())

    rows, actions, edges = reconstruct(source, certificate)
    sites, domains, identity, permutations = build_domains(rows, actions)
    anchor = certificate["anchor"]
    need(anchor == 1069 and len(domains[anchor]) == 24, "anchor orbit")
    anchor_orbit = {
        tuple(rows[anchor][k] for k in permutation) for permutation in permutations
    }
    need(anchor_orbit == {sites[i] for i in domains[anchor]},
         "global normalization misses an anchor image")

    tables = compatibility_tables(
        sites, domains, edges, certificate["prime"], actions
    )
    final, revisions, removed = ac3(
        domains, edges, tables, anchor, identity[anchor]
    )
    need(all(mask >> image & 1 for mask, image in zip(final, identity)),
         "identity solution removed")
    final_lists = [list(members(mask)) for mask in final]
    need(object_sha256(final_lists) == EXPECTED_FINAL_SHA256,
         "AC-3 fixed point differs")
    need(sum(len(domain) for domain in domains) - 23 -
         sum(mask.bit_count() for mask in final) == removed,
         "removed-value accounting differs")
    need(removed == 29983, "removed-value count differs")

    selected = certificate["disjoint_domain_vertices"]
    need(len(selected) == len(set(selected)) ==
         certificate["image_order_lower_bound"] == 1251,
         "witness cardinality")
    occupied = 0
    witness_histogram = Counter()
    for vertex in selected:
        need(type(vertex) is int and 0 <= vertex < 2131, "witness vertex")
        need(final[vertex] and not (occupied & final[vertex]),
             "witness domains overlap")
        witness_histogram[final[vertex].bit_count()] += 1
        occupied |= final[vertex]

    histogram = Counter(mask.bit_count() for mask in final)
    need(histogram == Counter({1: 1075, 6: 1056}), "final domain histogram")
    result = {
        "status": "INDEPENDENT_DIRECT_COMPLEX_AC3_VERIFIED_H3911",
        "actions": len(actions),
        "source_vertices": len(rows),
        "source_edges_checked_per_action": len(edges),
        "source_edge_action_checks": len(edges) * len(actions),
        "unit_direction_action_checks": 84 * len(actions),
        "shadow_sites": len(sites),
        "shadow_orbits": len(set(domains)),
        "anchor": anchor,
        "anchor_orbit": len(domains[anchor]),
        "ac3_domain_revisions": revisions,
        "removed_domain_values_after_anchor": removed,
        "final_domain_size_histogram": dict(sorted(histogram.items())),
        "final_domains_sha256": EXPECTED_FINAL_SHA256,
        "pairwise_disjoint_nonempty_domains": len(selected),
        "witness_domain_size_histogram": dict(sorted(witness_histogram.items())),
        "witness_site_union": occupied.bit_count(),
        "image_order_lower_bound": len(selected),
        "target_508_excluded_in_specified_family": True,
        "chromatic_lower_bound_used": False,
        "record_improvement": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
