#!/usr/bin/env python3
"""Exact finite obligations; standard library only, with no assert statements."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1)]
B = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
EDGES = [(i, j) for i in range(4) for j in range(4)
         if sum(a*b for a, b in zip(A[i], B[j])) > 0]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def mv(m, x):
    return [dot(row, x) for row in m]


def members(mask, n=8):
    return [i for i in range(n) if mask >> i & 1]


def reflection(mask):
    basis = []
    for i in members(mask & 15):
        v = list(map(Q, A[i]))
        for u in basis:
            coefficient = dot(v, u)/dot(u, u)
            v = [x-coefficient*y for x, y in zip(v, u)]
        if dot(v, v):
            basis.append(v)
    return [[2*sum((u[i]*u[j]/dot(u, u) for u in basis), Q(0))
             - (i == j) for j in range(3)] for i in range(3)]


def geometry():
    independent = [m for m in range(256)
                   if all(not (m >> i & 1 and m >> (j+4) & 1)
                          for i, j in EDGES)]
    maximal = [m for m in independent
               if not any(m != n and m & n == m for n in independent)]
    return independent, maximal


def make_certificate():
    independent, maximal = geometry()
    return {
        'schema': 'square-cone-minimax-faces-v1',
        'A': A, 'B': B, 'strict_cross_edges': EDGES,
        'independent_support_count': len(independent),
        'maximal_faces': [
            {'mask': m, 'reflection': [[str(x) for x in row]
                                      for row in reflection(m)]}
            for m in maximal],
        'contrast_bound': '3/7',
        'sharp_unit_edge_flow': ['0', '2/7', '2/7', '0', '0', '3/7', '0', '0'],
        'sharp_probability_packet': ['1/7', '1/7', '3/14', '0',
                                     '1/7', '0', '3/14', '1/7'],
    }


def flow_matrix():
    return [[Q(int((a, d) in EDGES)+int((c, b) in EDGES), 2)
             for c, d in EDGES] for a, b in EDGES]


def stationary(matrix, support):
    """RREF; reject inconsistent systems and explicitly verify unique lambda."""
    k = len(support)
    rows = [[matrix[i][j] for j in support]+[Q(-1), Q(0)]
            for i in support]
    rows.append([Q(1)]*k+[Q(0), Q(1)])
    original = [row[:] for row in rows]
    pivots = []
    rank = 0
    for column in range(k+1):
        pivot = next((i for i in range(rank, k+1) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [x/scale for x in rows[rank]]
        for i in range(k+1):
            if i != rank and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[rank])]
        pivots.append(column)
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return None
    require(k in pivots, 'lambda must have a pivot')
    lambda_row = rows[pivots.index(k)]
    require(all(lambda_row[c] == 0 for c in range(k+1) if c not in pivots),
            'lambda must not depend on a free variable')
    solution = [Q(0)]*(k+1)
    for r, c in enumerate(pivots):
        solution[c] = rows[r][-1]
    require(all(dot(row[:-1], solution) == row[-1] for row in original),
            'stationary equation substitution failed')
    return solution[k], rank, k+1-rank


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def audit(certificate):
    canonical = json.loads(json.dumps(make_certificate()))
    require(certificate == canonical, 'certificate differs from exact canonical instance')
    x = A + [tuple(-c for c in b) for b in B] + [(0, 0, 0)]
    y = A + B + [(0, 0, 0)]
    loss_pairs = []
    for i in range(9):
        for j in range(i):
            source = dot([a-b for a, b in zip(x[i], x[j])],
                         [a-b for a, b in zip(x[i], x[j])])
            target = dot([a-b for a, b in zip(y[i], y[j])],
                         [a-b for a, b in zip(y[i], y[j])])
            require(source >= target, 'map is not a contraction')
            if source != target:
                require((source, target) == (9, 1), 'strict distances not 9 and 1')
                loss_pairs.append((j, i-4))
    require(sorted(loss_pairs) == EDGES, 'cross-edge description incomplete')
    scalar_checks = 0
    strict_sites = 0
    for face in certificate['maximal_faces']:
        m = face['mask']
        s = [[Q(c) for c in row] for row in face['reflection']]
        require(all(s[i][j] == s[j][i] and dot(s[i], s[j]) == (i == j)
                    for i in range(3) for j in range(3)), 'not an orthogonal involution')
        core = members(m)+[8]
        require(all(mv(s, x[j]) == list(y[j]) for j in core), 'wrong face isometry')
        for i in range(9):
            v = mv(s, y[i])
            require(dot(v, v) == dot(x[i], x[i]), 'unequal observation-center norms')
            d = [a-b for a, b in zip(v, x[i])]
            products = [dot(x[j], d) for j in core]
            require(min(products) >= 0, 'polarization halfspace failed')
            scalar_checks += len(products)
            if i not in core:
                require(max(products) > 0, 'missing strict derivative at an exterior site')
                strict_sites += 1
    matrix = flow_matrix()
    records = []
    for mask in range(1, 256):
        result = stationary(matrix, members(mask))
        if result is None:
            records.append({'mask': mask, 'inconsistent': True})
        else:
            value, rank, nullity = result
            require(value >= Q(3, 7), 'stationary value below claimed bound')
            records.append({'mask': mask, 'value': str(value),
                            'rank': rank, 'nullity': nullity})
    z = list(map(Q, certificate['sharp_unit_edge_flow']))
    require(sum(z) == 1 and min(z) >= 0, 'not a unit edge flow')
    loads = [sum(z[e] for e, (a, b) in enumerate(EDGES)
                 if (i < 4 and a == i) or (i >= 4 and b == i-4))
             for i in range(8)]
    weights = list(map(Q, certificate['sharp_probability_packet']))
    require(weights == [c/2 for c in loads], 'flow does not produce packet')
    independent, maximal = geometry()
    delta = min(sum(weights[i] for i in range(8) if not (m >> i & 1)) for m in maximal)
    tau = sum(weights[a]*weights[b+4] for a, b in EDGES)
    require(delta == Q(1, 2) and tau == Q(3, 28), 'sharp fixture failed')
    require(dot(z, mv(matrix, z)) == Q(3, 7), 'sharp flow failed')
    return {
        'schema': 'square-cone-minimax-exact-audit-v1',
        'vertices_including_origin': 9, 'strict_cross_edges': len(EDGES),
        'independent_supports': len(independent), 'maximal_face_masks': maximal,
        'polarization_scalar_checks': scalar_checks, 'strict_exterior_sites': strict_sites,
        'stationary_systems': len(records),
        'consistent_systems': sum('value' in r for r in records),
        'inconsistent_systems': sum('inconsistent' in r for r in records),
        'singular_consistent_systems': sum(r.get('nullity', 0) > 0 for r in records),
        'minimum_stationary_value': str(min(Q(r['value']) for r in records if 'value' in r)),
        'minimum_support_masks': [r['mask'] for r in records if r.get('value') == '3/7'],
        'stationary_records_sha256': digest(records),
        'sharp_delta': str(delta), 'sharp_tau': str(tau),
        'certificate_canonical_sha256': digest(certificate),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=HERE/'CERTIFICATE.json')
    parser.add_argument('--write-certificate', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    if args.write_certificate:
        args.certificate.write_text(json.dumps(make_certificate(), indent=2)+'\n')
    record = audit(json.loads(args.certificate.read_text()))
    expected = HERE/'EXPECTED.json'
    if args.write_expected:
        expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    require(record == json.loads(expected.read_text()), 'expected audit record mismatch')
    print(json.dumps({'status': 'EXACT_FINITE_OBLIGATIONS_PASS',
                      'record_sha256': digest(record), **record}, sort_keys=True))


if __name__ == '__main__':
    main()
