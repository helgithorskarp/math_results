#!/usr/bin/env python3
"""Independent semantic audit of the pinned complete M=214 OPB formulation.

No imports from the generator, its C++ checker, or the scalar-model checker.
This is a formula/reduction audit, not a SAT/UNSAT computation.
"""

import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import subprocess

N = 43
PAIRS = [None] + list(it.combinations(range(N), 2))
TRIPLES = list(it.combinations(range(N), 3))
NE = len(PAIRS) - 1
NV = NE + len(TRIPLES)
NF = math.comb(N, 5)
EDGE_ID = {p: i for i, p in enumerate(PAIRS) if p is not None}
E = frozenset(range(13))
ANCHOR_RED = frozenset(range(6)) | frozenset(range(14, 29))
FORMULA_HASH = "88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58"
SCALAR_COMMIT = "7205fe40e336de80aec92ef998411a3302065d12"
SCALAR_PATH = "ramsey_r55_m214_scalar_relaxation/PSEUDOMODEL.json"
SCALAR_HASH = "e59a33cf352645528217125b3cae0e65a1a10dcbcc0ff8795e544ad964a5a550"
BLOCKS = [
    ("five_sets", 2 * NF, NF, 3),
    ("triangle_gates", 4 * len(TRIPLES), len(TRIPLES), 15),
    ("degrees", N, N, 1),
    ("local_triangles", N, N, 1),
    ("exceptional_degrees", N, N, 1),
    ("anchor", N - 1, N, 1),
]
CHOOSE = [[math.comb(v, k) for k in range(6)] for v in range(N)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_row(raw):
    words = raw.split()
    require(len(words) >= 5 and len(words) % 2 == 1, "row arity")
    require(words[-1] == b";" and words[-3] in (b"=", b">="), "row relation")
    terms = []
    for i in range(0, len(words) - 3, 2):
        coefficient, variable = words[i:i + 2]
        require(variable.startswith(b"x"), "variable syntax")
        index = int(variable[1:])
        require(1 <= index <= NV, "variable range")
        terms.append((int(coefficient), index))
    require(len({v for _, v in terms}) == len(terms), "duplicate variable")
    return terms, words[-3].decode(), int(words[-2])


def common_vertex(supports):
    common = set(supports[0])
    for support in supports[1:]:
        common.intersection_update(support)
    require(len(common) == 1, "support has no unique common vertex")
    return next(iter(common))


def classify(block, terms, relation, rhs):
    """Return an order-independent coverage key and obligation bit."""
    if block == "five_sets":
        require(len(terms) == 10 and relation == ">=", "five-set arity/relation")
        sign = terms[0][0]
        require(sign in (-1, 1) and all(c == sign for c, _ in terms), "five-set signs")
        require(rhs == (1 if sign == 1 else -9), "five-set threshold")
        require(all(v <= NE for _, v in terms), "five-set variable type")
        vertices = sorted({u for _, v in terms for u in PAIRS[v]})
        require(len(vertices) == 5, "five-set support")
        # Ten distinct edges on five endpoints are precisely that complete graph.
        rank = sum(CHOOSE[v][i + 1] for i, v in enumerate(vertices))
        return rank, 1 if sign == 1 else 2
    if block == "triangle_gates":
        zs = [(c, v) for c, v in terms if v > NE]
        es = [(c, v) for c, v in terms if v <= NE]
        require(len(zs) == 1 and relation == ">=", "gate variable types")
        zc, z = zs[0]
        edges = tuple(EDGE_ID[p] for p in it.combinations(TRIPLES[z - NE - 1], 2))
        if len(terms) == 2:
            require(zc == -1 and es[0][0] == 1 and rhs == 0, "upper gate signs")
            require(es[0][1] in edges, "upper gate support")
            bit = 1 << edges.index(es[0][1])
        else:
            require(len(terms) == 4 and zc == 1 and rhs == -2, "lower gate signs")
            require(all(c == -1 for c, _ in es), "lower gate edge signs")
            require({v for _, v in es} == set(edges), "lower gate support")
            bit = 8
        return z - NE - 1, bit
    require(all(c == 1 for c, _ in terms), "incidence coefficient")
    if block == "local_triangles":
        require(len(terms) == math.comb(42, 2) and relation == "=", "local arity/relation")
        require(all(v > NE for _, v in terms), "local variable type")
        vertex = common_vertex([TRIPLES[v - NE - 1] for _, v in terms])
        require(rhs == (93 if vertex in E else 100), "local triangle target")
        return vertex, 1
    require(all(v <= NE for _, v in terms), "edge incidence variable type")
    if block == "anchor":
        require(len(terms) == 1 and relation == "=", "anchor arity/relation")
        pair = PAIRS[terms[0][1]]
        require(13 in pair, "anchor endpoint")
        other = next(v for v in pair if v != 13)
        require(rhs == int(other in ANCHOR_RED), "anchor polarity")
        return other, 1
    vertex = common_vertex([PAIRS[v] for _, v in terms])
    if block == "degrees":
        require(len(terms) == 42 and relation == "=", "degree arity/relation")
        require(rhs == (20 if vertex in E else 21), "degree target")
    else:
        require(block == "exceptional_degrees", "unknown block")
        require(relation == ">=" and rhs == 6, "exceptional threshold")
        neighbors = {u for _, v in terms for u in PAIRS[v] if u != vertex}
        require(neighbors == E - {vertex}, "exceptional support")
    return vertex, 1


def add_coverage(seen, key, bit):
    require(0 <= key < len(seen) and not (seen[key] & bit), "duplicate/out-of-range obligation")
    seen[key] |= bit


def reduction_checks():
    weights = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}
    require(all(w >= 3 * abs(d - 21) for d, w in weights.items()), "weight inequality")
    # Equality at total deviation -13 permits only d=20 or d=21.
    equality_nonpositive = [d for d, w in weights.items() if w == 3 * abs(d - 21) and d <= 21]
    require(equality_nonpositive == [20, 21], "weight equality case")
    require(2 * 445 - 43 * 21 == -13 and 13 * 3 == 39, "M214 deviation")
    require((1247 - 39) // 2 == 604 and 604 - 86 * 7 == 2, "deficiency arithmetic")
    red_cap_sum = 13 * 93 + 30 * 100
    red_excess = [e for e in range(3) if (red_cap_sum - e) % 3 == 0]
    require(red_excess == [0] and red_cap_sum // 3 == 1403, "red divisibility")
    for degree in (20, 21):
        require(math.comb(42 - degree, 2) - 445 + 21 * degree == 206, "local identity constant")
    require(13 * 20 - 43 * 6 == 2 and 30 - 2 == 28, "exact anchor bound")
    require(445 - 21 - 100 - (210 - 100) == 214, "normalized M")
    # Check the local logical gadgets on every Boolean assignment.
    for edges in it.product((0, 1), repeat=10):
        require((sum(edges) >= 1 and -sum(edges) >= -9) == (0 < sum(edges) < 10), "five-set truth table")
    for edges in it.product((0, 1), repeat=3):
        for z in (0, 1):
            gadget = all(edge >= z for edge in edges) and z - sum(edges) >= -2
            require(gadget == (z == math.prod(edges)), "triangle truth table")
    return {"degree_profile": {"20": 13, "21": 30}, "red_excess": red_excess,
            "exact_central_anchors_at_least": 28, "five_set_truth_cases": 1024,
            "triangle_gate_truth_cases": 16}


def negative_tests():
    def reject(call):
        try:
            call()
        except ValueError:
            return
        raise ValueError("negative test was accepted")

    edge_terms = [(1, EDGE_ID[p]) for p in it.combinations(range(5), 2)]
    reject(lambda: classify("five_sets", edge_terms, ">=", 2))
    reject(lambda: parse_row(b"+1 x1 +1 x1 >= 1 ;"))
    reject(lambda: parse_row(b"+1 x13245 >= 1 ;"))
    reject(lambda: classify("triangle_gates", [(-1, NE + 1), (1, EDGE_ID[(0, 3)])], ">=", 0))
    reject(lambda: classify("triangle_gates", [(1, NE + 1)] + [(-1, EDGE_ID[p]) for p in ((0, 1), (0, 2), (1, 2))], ">=", -3))
    star = [(1, EDGE_ID[tuple(sorted((0, u)))]) for u in range(1, N)]
    reject(lambda: classify("degrees", star, "=", 21))
    local = [(1, NE + 1 + i) for i, tri in enumerate(TRIPLES) if 0 in tri]
    reject(lambda: classify("local_triangles", local, "=", 94))
    exceptional = [(1, EDGE_ID[(u, 13)]) for u in range(12)]
    reject(lambda: classify("exceptional_degrees", exceptional, ">=", 6))
    reject(lambda: classify("anchor", [(1, EDGE_ID[(0, 13)])], "=", 0))
    seen = bytearray(1)
    add_coverage(seen, 0, 1)
    reject(lambda: add_coverage(seen, 0, 1))
    return 10


def scalar_fixture(repository):
    data = subprocess.check_output(["git", "-C", str(repository), "show", f"{SCALAR_COMMIT}:{SCALAR_PATH}"])
    require(hashlib.sha256(data).hexdigest() == SCALAR_HASH, "pinned scalar hash")
    cert = json.loads(data)
    adj = [set() for _ in range(N)]

    def edge(i, j):
        adj[i].add(j)
        adj[j].add(i)

    differences = set(cert["exceptional_core"]["red_difference_set_mod_13"])
    for i, j in it.combinations(range(13), 2):
        if (j - i) % 13 in differences:
            edge(i, j)
    for c, signature in enumerate(cert["central_signatures"], 13):
        for e in range(13):
            if (signature >> e) & 1:
                edge(e, c)
    distances = set(cert["central_red_graph"]["cyclic_distances"])
    deleted = tuple(cert["central_red_graph"]["deleted_edge"])
    for i, j in it.combinations(range(30), 2):
        if min(j - i, 30 - j + i) in distances and (i, j) != deleted:
            edge(i + 13, j + 13)
    require([len(a) for a in adj] == [20] * 13 + [21] * 30, "scalar degree fixture")
    # Canonicalize an actual size-six central vertex. This checks that rejection
    # is not an artifact of imposing anchor labels on an unnormalized fixture.
    anchor = next(c for c in range(13, N) if len(adj[c] & E) == 6)
    old_at_new = (sorted(adj[anchor] & E) + sorted(E - adj[anchor]) + [anchor]
                  + sorted(adj[anchor] - E) + sorted(set(range(13, N)) - adj[anchor] - {anchor}))
    require(sorted(old_at_new) == list(range(N)), "scalar relabeling")
    inverse = {old: new for new, old in enumerate(old_at_new)}
    adj = [{inverse[u] for u in adj[old]} for old in old_at_new]
    require(adj[13] == ANCHOR_RED, "scalar anchor normalization")
    bits = [0] + [int(j in adj[i]) for i, j in PAIRS[1:]]
    bits += [int(j in adj[i] and k in adj[i] and k in adj[j]) for i, j, k in TRIPLES]
    red_locals = [sum(b in adj[a] for a, b in it.combinations(adj[v], 2)) for v in range(N)]
    blue_locals = []
    for v in range(N):
        nonneighbors = set(range(N)) - adj[v] - {v}
        blue_locals.append(sum(b not in adj[a] for a, b in it.combinations(nonneighbors, 2)))
    for v in range(N):
        require(red_locals[v] + blue_locals[v] == 206 - len(adj[v] & E), "scalar actual local identity")
    k5 = {}
    witnesses = {}
    for color in ("red", "blue"):
        masks = []
        for v in range(N):
            neighbors = adj[v] if color == "red" else set(range(N)) - adj[v] - {v}
            masks.append(sum(1 << u for u in neighbors))
        count = 0
        witness = None

        def visit(chosen, candidates):
            nonlocal count, witness
            if len(chosen) == 5:
                count += 1
                if witness is None:
                    witness = chosen
                return
            while candidates:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                visit(chosen + [v], candidates & masks[v])

        visit([], (1 << N) - 1)
        k5[color] = count
        witnesses[color] = witness
    return bits, {"certificate_sha256": SCALAR_HASH, "normalized_old_vertex_at_new_label": old_at_new,
                  "actual_red_triangles": sum(red_locals) // 3, "actual_blue_triangles": sum(blue_locals) // 3,
                  "local_red_target_mismatches": sum(t != (93 if v in E else 100) for v, t in enumerate(red_locals)),
                  "monochromatic_five_sets": k5, "first_normalized_witnesses": witnesses}


def audit(path, fixture_bits):
    digest = hashlib.sha256()
    rows = equalities = size = 0
    violations = {}
    coverage = {}
    with path.open("rb") as source:
        header = source.readline()
        digest.update(header)
        size += len(header)
        require(header.split() == b"* #variable= 13244 #constraint= 1974731 #equal= 128 intsize= 64".split(), "header")
        for name, count, obligations, full in BLOCKS:
            seen = bytearray(obligations)
            bad = 0
            for _ in range(count):
                raw = source.readline()
                require(bool(raw), "premature EOF")
                digest.update(raw)
                size += len(raw)
                terms, relation, rhs = parse_row(raw)
                key, bit = classify(name, terms, relation, rhs)
                add_coverage(seen, key, bit)
                value = sum(c * fixture_bits[v] for c, v in terms)
                bad += not (value == rhs if relation == "=" else value >= rhs)
                rows += 1
                equalities += relation == "="
            expected = bytearray([full]) * obligations
            if name == "anchor":
                expected[13] = 0
            require(seen == expected, f"{name} incomplete coverage")
            coverage[name] = count
            violations[name] = bad
            print(f"PASS semantic_block {name} rows={count} fixture_violations={bad}", flush=True)
        require(not source.read(1), "trailing data")
    require(rows == 1974731 and equalities == 128, "global counts")
    require(digest.hexdigest() == FORMULA_HASH and size == 167913049, "canonical bytes/hash")
    return {"sha256": digest.hexdigest(), "bytes": size, "constraints": rows, "equalities": equalities,
            "variables": NV, "coverage": coverage, "fixture_violations": violations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opb", required=True, type=Path)
    parser.add_argument("--source-repository", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    reduction = reduction_checks()
    negative_count = negative_tests()
    bits, fixture = scalar_fixture(args.source_repository)
    result = audit(args.opb, bits)
    require(result["fixture_violations"]["five_sets"] == sum(fixture["monochromatic_five_sets"].values()), "independent K5 count")
    require(result["fixture_violations"]["local_triangles"] == fixture["local_red_target_mismatches"], "independent local count")
    require(all(result["fixture_violations"][name] == 0 for name in ("triangle_gates", "degrees", "exceptional_degrees", "anchor")), "unexpected fixture violation")
    report = {"claim_scope": "canonical formula and necessary reduction audited; no SAT/UNSAT verdict",
              "formula": result, "reduction": reduction, "negative_tests_rejected": negative_count,
              "scalar_fixture": fixture}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS independent_semantic_audit negative_tests=10 five_set_truth_cases=1024 triangle_truth_cases=16")
    print("NO_VERDICT no SAT/UNSAT search was run")


if __name__ == "__main__":
    main()
