#!/usr/bin/env python3
"""Verify the complete exact-507-image obstruction for Heule's H510 graph.

The accepted parent certificate supplies 20 rank-501 rhombus bases and a
complete orientation-prefix cover.  This verifier checks that parent first,
then independently enumerates every rank-defect fibre pattern at collision
deficit three.  Every resulting quotient contains a K2,3.  Full-rank branches
are disposed of by the parent orientation cover: each rejected prefix already
forces either a source-edge collapse or a K2,3, while the two survivors are
the injective Galois drawings checked by the parent.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_heule510_plane_realizations"
FULL = (1 << 20) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_parent():
    pins = json.loads((HERE / "inputs.json").read_text())
    for relative, digest in pins.items():
        raw = (HERE / relative).resolve().read_bytes()
        require(sha256(raw).hexdigest() == digest, "parent input hash: " + relative)

    spec = importlib.util.spec_from_file_location("h510_parent_verify", PARENT / "verify.py")
    require(spec is not None and spec.loader is not None, "parent verifier import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = (PARENT / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    parent_result = module.verify(certificate)
    require(parent_result["verified"], "parent certificate verification")
    require(parent_result["rhombus_rank"] == 501, "parent rank")
    require(parent_result["orientation_words"] == 4096, "parent orientation cover")
    require(parent_result["normalized_representatives"] == 4, "parent survivors")
    edges, _, _ = module.load_inputs()
    return edges, certificate, sha256(raw).hexdigest()


def graph_data(edges):
    adjacency = [set() for _ in range(510)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    rhombi = []
    opposite_row = {}
    for a, b in combinations(range(510), 2):
        common = sorted(adjacency[a] & adjacency[b])
        require(len(common) <= 2, "source K2,3")
        if len(common) == 2 and (a, b) < tuple(common):
            row = len(rhombi)
            c, d = common
            rhombi.append((a, b, c, d))
            opposite_row[(a, b)] = row
            opposite_row[(c, d)] = row
    require(len(rhombi) == 3953 and len(opposite_row) == 7906, "rhombus census")
    return adjacency, rhombi, opposite_row


def canonical_groups(groups):
    answer = tuple(sorted(tuple(sorted(group)) for group in groups if len(group) > 1))
    require(sum(len(group) - 1 for group in answer) == 3, "collision deficit")
    require(len({v for group in answer for v in group}) == sum(map(len, answer)), "overlapping fibres")
    return answer


def quotient(adjacency, nontrivial_groups):
    owner = list(range(510))
    for group in nontrivial_groups:
        representative = min(group)
        for vertex in group:
            owner[vertex] = representative
    labels = sorted(set(owner))
    index = {label: i for i, label in enumerate(labels)}
    groups = [[] for _ in labels]
    for vertex, label in enumerate(owner):
        groups[index[label]].append(vertex)
    qadj = [set() for _ in labels]
    for u in range(510):
        for v in adjacency[u]:
            a, b = index[owner[u]], index[owner[v]]
            if a == b:
                return None, groups, (u, v), []
            qadj[a].add(b)
    merged = [i for i, group in enumerate(groups) if len(group) > 1]
    return qadj, groups, None, merged


def first_k23(qadj, merged):
    """Find every newly possible K2,3 centre pair.

    The source has no K2,3.  A new one contains a merged quotient class.  If
    that class is a centre, pair it with every other centre; if it is a leaf,
    both centres lie in its quotient neighbourhood.  These are precisely the
    pairs below.
    """
    candidate_pairs = set()
    for a in merged:
        candidate_pairs.update((min(a, b), max(a, b)) for b in range(len(qadj)) if a != b)
        candidate_pairs.update(combinations(sorted(qadj[a]), 2))
    for a, b in sorted(candidate_pairs):
        common = sorted(qadj[a] & qadj[b])
        if len(common) >= 3:
            return (a, b, *common[:3])
    return None


def assess(adjacency, groups):
    qadj, quotient_groups, collapsed, merged = quotient(adjacency, groups)
    if collapsed is not None:
        return "edge", collapsed
    witness = first_k23(qadj, merged)
    if witness is not None:
        return "k23", tuple(tuple(quotient_groups[v]) for v in witness)
    return "open", None


def row_masks(certificate, rhombi):
    bases = list(map(set, certificate["bases"]))
    require(len(bases) == 20 and all(len(basis) == 501 for basis in bases), "basis shape")
    masks = [sum(1 << i for i, basis in enumerate(bases) if row in basis) for row in range(len(rhombi))]
    require(all(mask != FULL for mask in masks), "single invalid row hits every basis")
    return masks


def covering_row_triples(masks):
    containing = []
    all_rows = (1 << len(masks)) - 1
    for bit in range(20):
        value = 0
        for row, mask in enumerate(masks):
            if mask & (1 << bit):
                value |= 1 << row
        containing.append(value)
    cache = {0: all_rows}

    def eligible(missing):
        if missing not in cache:
            value = all_rows
            for bit in range(20):
                if missing & (1 << bit):
                    value &= containing[bit]
            cache[missing] = value
        return cache[missing]

    triples = []
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            choices = eligible(FULL ^ (masks[i] | masks[j])) & ~((1 << (j + 1)) - 1)
            while choices:
                low = choices & -choices
                triples.append((i, j, low.bit_length() - 1))
                choices ^= low
    require(len(triples) == 8486, "covering row triple census")
    return triples


def invalid_mask(groups, opposite_row, masks):
    result = 0
    for group in groups:
        for pair in combinations(group, 2):
            row = opposite_row.get(tuple(sorted(pair)))
            if row is not None:
                result |= masks[row]
    return result


def repair_pairs_for_k23(adjacency, groups):
    """Pairs of source labels capable of removing the first quotient K2,3."""
    qadj, quotient_groups, collapsed, merged = quotient(adjacency, groups)
    require(collapsed is None, "repair base edge collapse")
    witness = first_k23(qadj, merged)
    require(witness is not None, "rank-covering base without K2,3")
    a, b, x, y, z = witness
    class_pairs = ((a, b), (x, y), (x, z), (y, z))
    answer = set()
    for first, second in class_pairs:
        for u in quotient_groups[first]:
            for v in quotient_groups[second]:
                answer.add(tuple(sorted((u, v))))
    return sorted(answer)


def three_pair_partitions(adjacency, rhombi, masks, covering_triples, certificate):
    partitions = set()
    for rows in covering_triples:
        sides = [(rhombi[row][:2], rhombi[row][2:]) for row in rows]
        for choice in range(8):
            pairs = [tuple(sides[i][(choice >> i) & 1]) for i in range(3)]
            if len({v for pair in pairs for v in pair}) == 6:
                partitions.add(canonical_groups(pairs))

    # Both opposite pairs of one rhombus may collapse; only the two parent
    # two-row covers can then hit every basis.
    for exceptional in certificate["rank_exceptions"]:
        first, second = exceptional["rows"]
        for doubled, single in ((first, second), (second, first)):
            for pair in (rhombi[single][:2], rhombi[single][2:]):
                pairs = [rhombi[doubled][:2], rhombi[doubled][2:], pair]
                if len({v for item in pairs for v in item}) == 6:
                    partitions.add(canonical_groups(pairs))

    # If just two rows cover the bases, an arbitrary third pair is relevant
    # only if it removes the first K2,3 made by the two contractions.
    for exceptional in certificate["rank_exceptions"]:
        for case in exceptional["cases"]:
            base = tuple(sorted(partition_groups(case["pairs"])))
            if sorted(map(len, base)) != [2, 2]:
                continue
            used = {v for group in base for v in group}
            for pair in repair_pairs_for_k23(adjacency, base):
                if not used.intersection(pair) and pair[1] not in adjacency[pair[0]]:
                    partitions.add(canonical_groups((*base, pair)))
    return sorted(partitions)


def opposition_triples(adjacency, opposite_row):
    triples = set()
    for u, v in opposite_row:
        for w in range(510):
            if w != u and w != v and w not in adjacency[u] and w not in adjacency[v]:
                triples.add(tuple(sorted((u, v, w))))
    return sorted(triples)


def triple_pair_partitions(adjacency, rhombi, opposite_row, masks):
    containing = []
    for bit in range(20):
        containing.append([row for row, mask in enumerate(masks) if mask & (1 << bit)])
    cache = {}

    def eligible(missing):
        if missing not in cache:
            bits = [bit for bit in range(20) if missing & (1 << bit)]
            seed = min(bits, key=lambda bit: len(containing[bit]))
            cache[missing] = [row for row in containing[seed] if masks[row] & missing == missing]
        return cache[missing]

    partitions = set()
    full_triples = []
    for triple in opposition_triples(adjacency, opposite_row):
        mask = 0
        for pair in combinations(triple, 2):
            row = opposite_row.get(pair)
            if row is not None:
                mask |= masks[row]
        if mask == FULL:
            full_triples.append(triple)
            continue
        missing = FULL ^ mask
        for row in eligible(missing):
            for pair in (rhombi[row][:2], rhombi[row][2:]):
                if not set(triple).intersection(pair):
                    partitions.add(canonical_groups((triple, pair)))

    require(len(full_triples) == 4, "full-defect triple census")
    for triple in full_triples:
        used = set(triple)
        for pair in repair_pairs_for_k23(adjacency, (triple,)):
            if not used.intersection(pair) and pair[1] not in adjacency[pair[0]]:
                partitions.add(canonical_groups((triple, pair)))
    return sorted(partitions), full_triples


def quadruple_partitions(adjacency, rhombi, opposite_row, masks, covering_triples, full_triples, certificate):
    candidates = set()
    for rows in covering_triples:
        sides = [(rhombi[row][:2], rhombi[row][2:]) for row in rows]
        for choice in range(8):
            vertices = tuple(sorted({v for i in range(3) for v in sides[i][(choice >> i) & 1]}))
            if len(vertices) == 4 and all(v not in adjacency[u] for u, v in combinations(vertices, 2)):
                candidates.add(vertices)

    for exceptional in certificate["rank_exceptions"]:
        first, second = exceptional["rows"]
        sides = ((rhombi[first][:2], rhombi[first][2:]), (rhombi[second][:2], rhombi[second][2:]))
        for choice in range(4):
            vertices = tuple(sorted(set(sides[0][choice & 1]) | set(sides[1][(choice >> 1) & 1])))
            if len(vertices) == 4 and all(v not in adjacency[u] for u, v in combinations(vertices, 2)):
                candidates.add(vertices)

    for triple in full_triples:
        for w in range(510):
            if w not in triple and all(w not in adjacency[u] for u in triple):
                candidates.add(tuple(sorted((*triple, w))))

    opposition = [0] * 510
    source = [0] * 510
    for u in range(510):
        for v in adjacency[u]:
            source[u] |= 1 << v
    for u, v in opposite_row:
        opposition[u] |= 1 << v
        opposition[v] |= 1 << u
    all_vertices = (1 << 510) - 1
    dense_seen = set()
    for u, v in opposite_row:
        for w in range(510):
            triple = tuple(sorted((u, v, w)))
            if len(set(triple)) < 3:
                continue
            a, b, c = triple
            if b in adjacency[a] or c in adjacency[a] or c in adjacency[b]:
                continue
            e3 = sum(pair in opposite_row for pair in combinations(triple, 2))
            need = 4 - e3
            if need <= 1:
                possible = opposition[a] | opposition[b] | opposition[c]
            elif need == 2:
                possible = ((opposition[a] & opposition[b]) | (opposition[a] & opposition[c]) |
                            (opposition[b] & opposition[c]))
            else:
                possible = opposition[a] & opposition[b] & opposition[c]
            possible &= all_vertices ^ (source[a] | source[b] | source[c])
            possible &= ~((1 << (c + 1)) - 1)
            while possible:
                low = possible & -possible
                x = low.bit_length() - 1
                possible ^= low
                quad = (a, b, c, x)
                if quad in dense_seen:
                    continue
                dense_seen.add(quad)
                rows = [opposite_row[pair] for pair in combinations(quad, 2) if pair in opposite_row]
                if len(rows) >= 4:
                    mask = 0
                    for row in rows:
                        mask |= masks[row]
                    if mask == FULL:
                        candidates.add(quad)
    return [canonical_groups((quad,)) for quad in sorted(candidates)], len(dense_seen)


def check_candidate_family(name, partitions, adjacency, opposite_row, masks, stream):
    outcomes = Counter()
    for groups in partitions:
        require(invalid_mask(groups, opposite_row, masks) == FULL, name + " rank coverage")
        status, witness = assess(adjacency, groups)
        require(status in ("edge", "k23"), name + " survivor")
        outcomes[status] += 1
        row = json.dumps({"family": name, "groups": groups, "status": status, "witness": witness},
                         separators=(",", ":"), sort_keys=True).encode() + b"\n"
        stream.update(row)
    return {"candidates": len(partitions), **dict(sorted(outcomes.items()))}


def verify():
    edges, certificate, parent_hash = load_parent()
    adjacency, rhombi, opposite_row = graph_data(edges)
    masks = row_masks(certificate, rhombi)
    covering_triples = covering_row_triples(masks)

    three_pairs = three_pair_partitions(adjacency, rhombi, masks, covering_triples, certificate)
    triple_pair, full_triples = triple_pair_partitions(adjacency, rhombi, opposite_row, masks)
    quadruples, dense_examined = quadruple_partitions(
        adjacency, rhombi, opposite_row, masks, covering_triples, full_triples, certificate
    )

    stream = sha256()
    families = {
        "three_pairs": check_candidate_family("three_pairs", three_pairs, adjacency, opposite_row, masks, stream),
        "triple_pair": check_candidate_family("triple_pair", triple_pair, adjacency, opposite_row, masks, stream),
        "quadruple": check_candidate_family("quadruple", quadruples, adjacency, opposite_row, masks, stream),
    }

    orientation = Counter()
    orientation_stream = sha256()
    rejected = 0
    survivors = 0
    for index, leaf in enumerate(certificate["orientation_cover"]):
        if leaf.get("survivor") is True:
            survivors += 1
            continue
        groups = canonical_groups(partition_groups(leaf["pairs"]))
        status, witness = assess(adjacency, groups)
        require(status in ("edge", "k23"), "full-rank orientation survivor")
        orientation[status] += 1
        rejected += 1
        orientation_stream.update(json.dumps(
            {"leaf": index, "groups": groups, "status": status, "witness": witness},
            separators=(",", ":"), sort_keys=True).encode() + b"\n")
    require(rejected == 34 and survivors == 2, "orientation leaf census")

    return {
        "status": "VERIFIED_NO_EXACT_507_IMAGE_H510_MAP",
        "source_vertices": 510,
        "source_edges": len(edges),
        "rhombi": len(rhombi),
        "rank_bases": 20,
        "rank_per_basis": 501,
        "covering_row_triples": len(covering_triples),
        "full_defect_triples": len(full_triples),
        "dense_quadruples_examined": dense_examined,
        "rank_defect_families": families,
        "rank_defect_stream_sha256": stream.hexdigest(),
        "full_rank_rejected_prefixes": rejected,
        "full_rank_survivors": survivors,
        "full_rank_obstructions": dict(sorted(orientation.items())),
        "orientation_obstruction_stream_sha256": orientation_stream.hexdigest(),
        "parent_certificate_sha256": parent_hash,
        "exact_507_image_realization_exists": False,
        "record_improvement": False,
        "solver_required": False,
    }


def partition_groups(pairs):
    parent = list(range(510))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in pairs:
        a, b = find(u), find(v)
        if a != b:
            parent[b] = a
    groups = {}
    for vertex in range(510):
        groups.setdefault(find(vertex), []).append(vertex)
    return tuple(tuple(group) for group in groups.values() if len(group) > 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        expected = json.loads((HERE / "expected.json").read_text())
        require(result == expected, "expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
