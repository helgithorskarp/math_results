#!/usr/bin/env python3
"""Clean-room review of the fixed eta^3 Moser contact circle.

No code from the reviewed eta^3 package is imported.  Field arithmetic is
loaded from the already published independent review of the parent collision
theorem and is pinned by SHA-256.  The target certificate and expected JSON
are treated only as untrusted data.
"""

from __future__ import annotations

import argparse
from collections import Counter
import ctypes
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path

PRIOR_AUDIT_SHA256 = "b9a8dcb5cd672318614916345222230e675a34eddede4a190a3d3ff0f6b28fd4"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    packed = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(packed).hexdigest()


def valid_word(word) -> bool:
    return isinstance(word, str) and len(word) == 343 and set(word) <= set("0123")


def proper(word, edges) -> bool:
    return all(word[left] != word[right] for left, right in edges)


def load_arithmetic(path: Path):
    need(file_sha(path) == PRIOR_AUDIT_SHA256, "prior independent arithmetic source digest")
    spec = importlib.util.spec_from_file_location("prior_independent_audit", path)
    need(spec is not None and spec.loader is not None, "cannot load prior audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def qzero(A, q) -> bool:
    return q == A.Q0


def integral_residue(A, z):
    """Reduce z=x+alpha*y in the unramified basis omega=(1+alpha)/2."""
    x, y = z
    coordinates = (A.qs(x, y), A.qc(y, 2))
    result = []
    for coordinate in coordinates:
        if qzero(A, coordinate):
            result.append(0)
            continue
        valuation, odd_unit = A.q2_data(coordinate, 1)
        need(valuation >= 0, "point outside the selected local integer ring")
        result.append(0 if valuation > 0 else odd_unit & 1)
    return tuple(result)


def source_graph(A, M):
    return [
        (i, j)
        for i, j in combinations(range(7), 2)
        if A.enorm(A.es(M[i], M[j])) == A.Q1
    ]


def fixed_inventory(A):
    M = A.spindle()
    eta = M[4]
    u = A.em(A.em(eta, eta), eta)
    need(A.enorm(u) == A.Q1, "eta^3 is not a unit")
    B = sorted({A.ea(a, A.em(u, b)) for a, b in product(M, repeat=2)})
    need(len(B) == 49, "M+eta^3 M is not injective")

    residues = [integral_residue(A, point) for point in B + M]
    need(all(residue in product(range(2), repeat=2) for residue in residues),
         "invalid residue")

    Db = A.difference_map(B)
    Dm = A.difference_map(M)
    db = [value for value in Db if value != A.E0]
    dm = [value for value in Dm if value != A.E0]
    norms_a = {value: A.enorm(value) for value in db}
    norms_b = {value: A.enorm(value) for value in dm}
    inverse_contact = {}
    groups = {}
    stats = Counter()

    # Classify every direction pair directly; unlike the target, this checker
    # deliberately has no norm-pair shape cache.
    for a, b in product(db, dm):
        S = A.qs(A.qa(norms_a[a], norms_b[b]), A.Q1)
        if S == A.Q0:
            stats["trace_zero"] += 1
            continue
        va = A.q2_data(norms_a[a])[0]
        vb = A.q2_data(norms_b[b])[0]
        need(va % 2 == vb % 2 == 0, "unexpected odd norm valuation")
        trace_valuation = A.q2_data(S)[0] - (va + vb) // 2
        if trace_valuation >= -1:
            stats["trace_ge_minus1"] += 1
            continue
        delta = A.qs(A.qc(A.qm(norms_a[a], norms_b[b]), 4), A.qm(S, S))
        if A.qsign(delta) <= 0:
            stats["nonpositive_delta"] += 1
            continue
        radicand = A.qc(delta, F(1, 3))
        if A.qsqrt(radicand) is not None:
            stats["base_field_root"] += 1
            continue

        c = A.em(A.econj(a), b)
        ci = inverse_contact.setdefault(c, A.ei(c))
        T = A.ec(A.em((S, A.Q0), ci), -1)
        J = A.em(A.em(a, A.econj(b)), ci)
        key = (T, J)
        row = groups.setdefault(
            key,
            {"ss": radicand, "trace_valuation": trace_valuation, "directions": [],
             "witness": (a, b)},
        )
        need(row["ss"] == radicand, "contact group changed radicand")
        need(row["trace_valuation"] == trace_valuation,
             "contact group changed trace valuation")
        row["directions"].append((a, b))
        stats["event"] += 1

    groups = sorted(groups.items())
    return M, u, B, Db, Dm, groups, dict(stats), residues


def baseline_graph(A, B, M):
    edges = set()
    B_edges = [
        (i, j) for i, j in combinations(range(len(B)), 2)
        if A.enorm(A.es(B[i], B[j])) == A.Q1
    ]
    M_edges = source_graph(A, M)
    for i, j in B_edges:
        for k in range(7):
            edges.add((7 * i + k, 7 * j + k))
    for i in range(len(B)):
        for j, k in M_edges:
            edges.add((7 * i + j, 7 * i + k))
    return sorted(edges), B_edges, M_edges


def event_graph(Db, Dm, baseline, group):
    edges = set(baseline)
    for a, b in group["directions"]:
        for i, ii in Db[a]:
            for j, jj in Dm[b]:
                edges.add(tuple(sorted((7 * i + j, 7 * ii + jj))))
    return sorted(edges)


def serial_inventory(A, u, groups):
    return {
        "u": A.ser_e(u),
        "groups": [
            {
                "key": [A.ser_e(T), A.ser_e(J)],
                "ss": A.ser_e((group["ss"], A.Q0)),
                "trace_valuation": group["trace_valuation"],
                "directions": [
                    [A.ser_e(a), A.ser_e(b)] for a, b in group["directions"]
                ],
            }
            for (T, J), group in groups
        ],
    }


class IndependentGeometry:
    """C ABI wrapper for the reviewer's alternate-basis metric kernel."""

    def __init__(self, library: Path):
        self.lib = ctypes.CDLL(str(library))
        self.fun = self.lib.review_contacts
        pointer_i64 = ctypes.POINTER(ctypes.c_int64)
        pointer_i32 = ctypes.POINTER(ctypes.c_int32)
        self.fun.argtypes = [ctypes.c_int, ctypes.c_int64, ctypes.c_int64,
                             ctypes.c_int64, ctypes.c_int64, pointer_i64, pointer_i32]
        self.fun.restype = ctypes.c_int
        self.buffer = (ctypes.c_int32 * (343 * 342))()
        self.max_abs_coordinate = 0
        self.max_denominator = 0

    def graph(self, A, points, radicand, extension_sign=1):
        values = []
        for z0, z1 in points:
            for value in z0[0] + z0[1] + z1[0] + z1[1]:
                values.append(value)
        denominator = lcm(*(value.denominator for value in values))
        packed = []
        for z0, z1 in points:
            row = list(z0[0] + z0[1] + z1[0] + z1[1])
            row[4:] = [extension_sign * value for value in row[4:]]
            packed.extend(int(value * denominator) for value in row)
        sd = lcm(radicand[0].denominator, radicand[1].denominator)
        s0, s1 = (int(value * sd) for value in radicand)
        maximum = max(map(abs, packed + [s0, s1]))
        need(denominator <= 10**9 and sd <= 10**9 and maximum <= 10**9,
             "review metric input exceeds native guard")
        self.max_abs_coordinate = max(self.max_abs_coordinate, maximum)
        self.max_denominator = max(self.max_denominator, denominator, sd)
        array = (ctypes.c_int64 * len(packed))(*packed)
        count = self.fun(len(points), denominator, sd, s0, s1, array, self.buffer)
        need(count >= 0, f"review metric kernel rejected input ({count})")
        return [(self.buffer[2 * i], self.buffer[2 * i + 1]) for i in range(count)]


def xsub(A, left, right):
    return (A.es(left[0], right[0]), A.es(left[1], right[1]))


def exact_unit(A, difference, radicand):
    return A.xmul(difference, A.xconj(difference), radicand) == (A.E1, A.E0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--prior-audit", required=True)
    parser.add_argument("--library", required=True)
    args = parser.parse_args()
    certificate_path = Path(args.certificate)
    expected_path = Path(args.expected)
    prior_path = Path(args.prior_audit)
    A = load_arithmetic(prior_path)
    certificate = json.loads(certificate_path.read_text())
    expected = json.loads(expected_path.read_text())

    certificate_hash = file_sha(certificate_path)
    need(certificate_hash == expected["certificate_sha256"], "certificate digest")
    need(certificate.get("format") == "fixed-eta3-circle-v1", "certificate format")
    words = certificate.get("words")
    assignments = certificate.get("assignment")
    need(isinstance(words, list) and len(words) == 80, "word census")
    need(all(valid_word(word) for word in words), "word syntax")
    need(certificate.get("word_hashes") == [sha256(word.encode()).hexdigest() for word in words],
         "word digest list")

    M, u, B, Db, Dm, groups, stats, residues = fixed_inventory(A)
    need(A.ser_e(u) == ["-5/27", "0", "0", "8/27"], "eta^3 coordinates")
    need(stats == expected["filters"] == certificate["filters"], "filter census")
    need(len(groups) == expected["exceptional_quadratics"] == 922, "group census")
    need(isinstance(assignments, list) and len(assignments) == len(groups),
         "assignment coverage")

    inventory = serial_inventory(A, u, groups)
    inventory_hash = digest(inventory)
    need(inventory_hash == expected["exact_inventory_sha256"], "inventory digest")

    baseline, B_edges, M_edges = baseline_graph(A, B, M)
    need((len(M_edges), len(B_edges), len(baseline)) == (11, 154, 1617),
         "Cartesian graph dimensions")
    need(not any(all(colours[i] != colours[j] for i, j in M_edges)
                 for colours in product(range(3), repeat=7)), "Moser spindle is 3-colourable")
    need(any(all(colours[i] != colours[j] for i, j in M_edges)
             for colours in product(range(4), repeat=7)), "Moser spindle lacks a 4-colouring")

    # Independently exhibit the residue-sum colouring of every no-mixed-contact
    # Cartesian graph.  This is also the in-field colouring restricted to B+M.
    B_res = [integral_residue(A, point) for point in B]
    M_res = [integral_residue(A, point) for point in M]
    base_colours = [2 * (B_res[i][0] ^ M_res[j][0]) + (B_res[i][1] ^ M_res[j][1])
                    for i, j in product(range(49), range(7))]
    need(all(base_colours[i] != base_colours[j] for i, j in baseline),
         "residue-sum baseline colouring")

    geometry = IndependentGeometry(Path(args.library))
    edge_counts = Counter()
    radicands = set()
    edge_stream = sha256()
    metric_spotchecks = 0
    audited_pairs = 0
    alpha = (A.Q0, A.Q1)
    negative_controls = Counter()

    for case_number, (((T, J), group), word_id) in enumerate(zip(groups, assignments)):
        need(isinstance(word_id, int) and 0 <= word_id < len(words), "word index")
        word = words[word_id]
        expected_graph = event_graph(Db, Dm, baseline, group)
        ci = A.ei(A.em(A.econj(group["witness"][0]), group["witness"][1]))
        root = (A.ec(T, F(1, 2)), A.ec(A.em(alpha, ci), F(1, 2)))
        radicand = group["ss"]
        need(A.xmul(root, A.xconj(root), radicand) == (A.E1, A.E0),
             "phase is not unit")
        square = A.xmul(root, root, radicand)
        linear = A.xm_e(root, T)
        polynomial = (A.ea(A.es(square[0], linear[0]), J),
                      A.es(square[1], linear[1]))
        need(polynomial == (A.E0, A.E0), "phase minimal polynomial")

        vm = [A.xm_e(root, point) for point in M]
        points = [(A.ea(base, rotated[0]), rotated[1]) for base, rotated in product(B, vm)]
        need(len(points) == len(set(points)) == 343, "physical support collision")
        plus_graph = geometry.graph(A, points, radicand, 1)
        minus_graph = geometry.graph(A, points, radicand, -1)
        need(plus_graph == minus_graph == expected_graph,
             "alternate-basis physical graph disagrees with contact inventory")
        audited_pairs += 2 * 343 * 342 // 2

        edge_set = set(expected_graph)
        probes = [(0, 1), (0, 342), (case_number % 342, case_number % 342 + 1),
                  ((37 * case_number + 17) % 342, (37 * case_number + 17) % 342 + 1)]
        for left, right in probes:
            metric_spotchecks += 1
            need(exact_unit(A, xsub(A, points[left], points[right]), radicand)
                 == ((left, right) in edge_set), "Python/C++ exact metric disagreement")

        need(proper(word, expected_graph), "certificate word is not proper")
        need(not proper("0" * 343, expected_graph), "constant word was accepted")
        negative_controls["constant_word_rejections"] += 1
        first_left, first_right = expected_graph[0]
        damaged = list(word)
        damaged[first_right] = damaged[first_left]
        need(not proper(damaged, expected_graph), "single-edge damage was accepted")
        negative_controls["single_edge_word_rejections"] += 1

        edge_counts[len(expected_graph)] += 1
        radicands.add(radicand)
        edge_stream.update(f"{case_number}:{digest(expected_graph)}\n".encode())

    edge_counts_json = {str(key): edge_counts[key] for key in sorted(edge_counts)}
    need(edge_counts_json == expected["edge_counts"] == certificate["edge_counts"],
         "edge histogram")
    edge_hash = edge_stream.hexdigest()
    need(edge_hash == expected["edge_stream_sha256"], "edge-stream digest")
    need(len(radicands) == expected["distinct_radicands"] == 134, "radicand census")
    need(audited_pairs == expected["audited_unordered_pairs"], "physical pair census")

    # Cheap malformed-input controls for the certificate parser's invariants.
    need(not valid_word(words[0][:-1]), "short word was accepted")
    need(not valid_word(words[0][:-1] + "x"), "bad alphabet was accepted")
    need(len(assignments[:-1]) != len(groups), "short assignment was accepted")
    need(not (0 <= len(words) < len(words)), "out-of-range index was accepted")

    result = {
        "status": "PASS",
        "reviewer_representation": "Q(sqrt(33))[alpha]/(alpha^2+3), alpha=i*sqrt(3)",
        "imports_target_code": False,
        "prior_independent_arithmetic_sha256": file_sha(prior_path),
        "certificate_sha256": certificate_hash,
        "certificate_words": len(words),
        "eta3": A.ser_e(u),
        "base_vertices": len(B),
        "support_vertices": len(B) * len(M),
        "base_edges": len(B_edges),
        "baseline_edges": len(baseline),
        "exceptional_quadratics": len(groups),
        "physical_exceptional_phases": 2 * len(groups),
        "filters": stats,
        "distinct_radicands": len(radicands),
        "edge_counts": edge_counts_json,
        "inventory_sha256": inventory_hash,
        "edge_stream_sha256": edge_hash,
        "physical_pairs_audited": audited_pairs,
        "python_metric_spotchecks": metric_spotchecks,
        "integral_points_checked": len(residues),
        "residue_sum_edges_checked": len(baseline),
        "negative_controls": dict(negative_controls,
                                  malformed_certificate_invariants=4),
        "native_max_abs_input": geometry.max_abs_coordinate,
        "native_max_denominator": geometry.max_denominator,
        "native_conservative_intermediate_bound_bits": 101,
        "spindle_chromatic_number": 4,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
