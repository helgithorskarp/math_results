"""Exact linearized endpoint-coincidence framework of the fixed five coronas.

Integer axial vertex coordinates are three times the centre-lattice coordinates.
The infinitesimal rotation matrix A is sqrt(3) times physical quarter-turn J.
Modular elimination certifies rational rank; no floating point or SAT is used.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from math import isqrt
import sys

import marked_corona as mc
import hex_domain as hd

FIXTURE_SHA256 = 'd857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a'

N = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
A = ((-1, -2), (2, 1))


def rotation(p, k):
    x, y = p
    return ((x, y), (-y, x+y), (-x-y, x), (-x, -y),
            (y, -x-y), (x+y, -x))[k % 6]


def motion(p, ref, k):
    return rotation((p[0]+p[1], -p[1]) if ref else p, k)


def multiply(matrix, p):
    return tuple(sum(a*b for a, b in zip(row, p)) for row in matrix)


def vertex_set(tile):
    cells = set(map(tuple, tile))
    vertices = set()
    for x, y in cells:
        for d, (dx, dy) in enumerate(N):
            if (x+dx, y+dy) in cells:
                continue
            for e in ((d-1) % 6, (d+1) % 6):
                vertices.add((3*x+dx+N[e][0], 3*y+dy+N[e][1]))
    return sorted(vertices)


def framework(witness):
    direct_checks = mc.check_witness(witness)
    tile = witness['tile']
    vertices = vertex_set(tile)
    n, copies = len(vertices), len(witness['patch'])
    variables = 2*n+3*(copies-1)
    owners, motions = defaultdict(list), []
    for a, record in enumerate(witness['patch']):
        ref, k = record['reflect'], record['turns']
        raw = [motion(p, ref, k) for p in tile]
        offset = min(x for x, y in raw), min(y for x, y in raw)
        tx, ty = record['translation']
        t = 3*(tx-offset[0]), 3*(ty-offset[1])
        columns = [motion(e, ref, k) for e in ((1, 0), (0, 1))]
        matrix = tuple(tuple(columns[j][i] for j in range(2)) for i in range(2))
        transformed = [motion(v, ref, k) for v in vertices]
        for i, v in enumerate(transformed):
            owners[v[0]+t[0], v[1]+t[1]].append((a, i))
        motions.append({'matrix': matrix, 'translation': t, 'hand': -1 if ref else 1,
                        'transformed_vertices': transformed})
    rows, descriptions = [], []
    for point, incidents in sorted(owners.items()):
        anchor = incidents[0]
        for b, j in incidents[1:]:
            a, i = anchor
            for coordinate in (0, 1):
                row = defaultdict(int)
                for copy, vertex, sign in ((a, i, 1), (b, j, -1)):
                    m = motions[copy]
                    for d in (0, 1):
                        row[2*vertex+d] += sign*m['matrix'][coordinate][d]
                    if copy:
                        base = 2*n+3*(copy-1)
                        row[base+coordinate] += sign
                        row[base+2] += sign*multiply(A, m['transformed_vertices'][vertex])[coordinate]
                rows.append({i: x for i, x in row.items() if x})
                descriptions.append({'point': point, 'anchor': anchor,
                                     'other': (b, j), 'coordinate': coordinate})
    kernel = []
    for kind in ('translation_x', 'translation_y', 'scale', 'rotation'):
        vector = [0]*variables
        for i, v in enumerate(vertices):
            q = (1, 0) if kind == 'translation_x' else (0, 1) if kind == 'translation_y' else v if kind == 'scale' else multiply(A, v)
            vector[2*i:2*i+2] = q
        for a in range(1, copies):
            m = motions[a]
            if kind.startswith('translation_'):
                q = (1, 0) if kind == 'translation_x' else (0, 1)
                rq = multiply(m['matrix'], q)
                t, omega = (q[0]-rq[0], q[1]-rq[1]), 0
            elif kind == 'scale':
                t, omega = m['translation'], 0
            else:
                t, omega = multiply(A, m['translation']), 1-m['hand']
            vector[2*n+3*(a-1):2*n+3*a] = [*t, omega]
        if any(sum(x*vector[i] for i, x in row.items()) for row in rows):
            raise ValueError('Similarity direction is not in the exact kernel: '+kind)
        kernel.append(vector)
    return vertices, motions, rows, descriptions, kernel, direct_checks


def modular_rank(rows, variables, prime):
    if prime < 2 or any(prime % d == 0 for d in range(2, isqrt(prime)+1)):
        raise ValueError('Modulus must be prime')
    pivots, chosen = {}, []
    for number, original in enumerate(rows):
        row = {i: x % prime for i, x in original.items() if x % prime}
        while row:
            column = min(row)
            if column not in pivots:
                inverse = pow(row[column], -1, prime)
                pivots[column] = {i: x*inverse % prime for i, x in row.items()}
                chosen.append((number, column))
                break
            value = row[column]
            for i, x in pivots[column].items():
                updated = (row.get(i, 0)-value*x) % prime
                if updated:
                    row[i] = updated
                else:
                    row.pop(i, None)
    return len(pivots), chosen


def determinant_mod(matrix, prime):
    """A separate dense elimination for the indicated square minor."""
    a = [[x % prime for x in row] for row in matrix]
    n, determinant = len(a), 1
    for j in range(n):
        i = next((i for i in range(j, n) if a[i][j]), None)
        if i is None:
            return 0
        if i != j:
            a[i], a[j] = a[j], a[i]
            determinant = -determinant % prime
        pivot = a[j][j]
        determinant = determinant*pivot % prime
        inv = pow(pivot, -1, prime)
        for i in range(j+1, n):
            if a[i][j]:
                multiplier = a[i][j]*inv % prime
                a[i][j:] = [(x-multiplier*y) % prime for x, y in zip(a[i][j:], a[j][j:])]
    return determinant


def interface_endpoint_groups(witness, vertices):
    """Independent repeated-rotation port decoder, unlike the closed-form map.

    It constructs endpoints from the actual adjacent cell centres, and then
    uses inverse motions to recover original vertex labels.
    """
    index = {v: i for i, v in enumerate(vertices)}
    edges, inverses = defaultdict(list), []
    for a, record in enumerate(witness['patch']):
        ref, k = record['reflect'], record['turns']
        tx, ty = record['translation']
        raw = [hd.transform(tuple(p), ref, k) for p in witness['tile']]
        x0, y0 = min(x for x, y in raw), min(y for x, y in raw)
        t = 3*(tx-x0), 3*(ty-y0)
        _, ports = hd.oriented(witness['tile'], ref, k)
        for ends, _ in ports:
            moved = tuple(sorted((x+tx, y+ty) for x, y in ends))
            edges[moved].append(a)

        def inverse(point, t=t, k=k, ref=ref):
            p = point[0]-t[0], point[1]-t[1]
            p = hd.transform(p, False, (-k) % 6)
            return hd.transform(p, ref, 0)

        inverses.append(inverse)
    groups, interfaces = defaultdict(set), 0
    for (u, v), copies in sorted(edges.items()):
        if len(copies) == 1:
            continue
        if len(copies) != 2:
            raise ValueError('A full unit port must have exactly two owners')
        d = N.index((v[0]-u[0], v[1]-u[1]))
        for e in ((d-1) % 6, (d+1) % 6):
            point = 3*u[0]+N[d][0]+N[e][0], 3*u[1]+N[d][1]+N[e][1]
            for a in copies:
                original = inverses[a](point)
                groups[point].add((a, index[original]))
        interfaces += 1
    return dict(groups), interfaces


def main():
    path = Path(__file__).with_name('signed_hex4_depth5.witness.json')
    fixture_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if fixture_hash != FIXTURE_SHA256:
        raise ValueError('The fixed five-corona baseline has changed')
    witness = json.loads(path.read_text())
    vertices, motions, rows, descriptions, kernel, checks = framework(witness)
    groups, interfaces = interface_endpoint_groups(witness, vertices)
    generated_groups = defaultdict(set)
    for d in descriptions:
        generated_groups[tuple(d['point'])].update([tuple(d['anchor']), tuple(d['other'])])
    if dict(generated_groups) != groups:
        raise ValueError('Vertex-coincidence and independent full-port decoders disagree')
    variables = len(kernel[0])
    prime = 1009
    rank, chosen = modular_rank(rows, variables, prime)
    row_ids, columns = [x[0] for x in chosen], sorted(x[1] for x in chosen)
    determinant = determinant_mod([[rows[i].get(j, 0) for j in columns] for i in row_ids], prime)
    independent_kernel_rank, _ = modular_rank([{i: x for i, x in enumerate(v) if x} for v in kernel], variables, prime)
    if (len(vertices), len(motions), len(rows), variables, rank, independent_kernel_rank,
        determinant, len(groups), interfaces) != (18, 131, 2410, 426, 422, 4, 379, 995, 1075):
        raise ValueError('Endpoint rigidity certificate changed')
    data = {'agent': 'six-heesch-3', 'role': 'researcher', 'fixture_sha256': fixture_hash,
            'vertices': vertices, 'copies': len(motions), 'variables': variables,
            'rows': len(rows), 'shared_vertex_groups': len(groups),
            'unit_interfaces_independently_decoded': interfaces,
            'row_sha256': hashlib.sha256(json.dumps([sorted(r.items()) for r in rows], separators=(',', ':')).encode()).hexdigest(),
            'modulus': prime, 'modular_rank': rank, 'known_independent_integer_kernel_vectors': 4,
            'exact_rational_rank': rank, 'kernel': ['translation_x', 'translation_y', 'scale', 'rotation'],
            'minor_rows': row_ids, 'minor_columns': columns, 'minor_determinant_mod_prime': determinant,
            'direct_fixture_checks': checks,
            'scope': 'Local Euclidean endpoint and pose deformations preserving the original complete full-port endpoint network'}
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
