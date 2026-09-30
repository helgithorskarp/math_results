"""Exact even/odd profile constraints for a fixed reflected polyhex patch.

The new contact decoder uses closed-form axial motions. Fraction elimination
checks ranks independently of signed-graph propagation. No SAT solver is used.
"""
from collections import deque
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from marked_corona import check_witness

NEIGHBORS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
FIXTURE_SHA256 = 'd857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a'


def rotation(p, k):
    x, y = p
    return ((x, y), (-y, x+y), (-x-y, x), (-x, -y),
            (y, -x-y), (x+y, -x))[k % 6]


def reflection(p):
    x, y = p
    return x+y, -y


def contacts(witness):
    """Decode each real shared unit interface to original ports and handedness."""
    checks = check_witness(witness)
    if witness['grid'] != 'hex':
        raise ValueError('This decoder uses regular polyhexes')
    tile = set(map(tuple, witness['tile']))
    ports = sorted((c, (c[0]+dx, c[1]+dy)) for c in tile
                   for dx, dy in NEIGHBORS if (c[0]+dx, c[1]+dy) not in tile)
    index = {port: i for i, port in enumerate(ports)}
    owners, inverses, hands = {}, [], []
    for number, record in enumerate(witness['patch']):
        k, r = record['turns'], record['reflect']
        raw = [rotation(reflection(p) if r else p, k) for p in tile]
        offset = min(x for x, y in raw), min(y for x, y in raw)
        tx, ty = record['translation']
        for x, y in raw:
            cell = x-offset[0]+tx, y-offset[1]+ty
            if cell in owners:
                raise ValueError('overlapping footprints')
            owners[cell] = number

        def inverse(p, k=k, r=r, offset=offset, tx=tx, ty=ty):
            q = rotation((p[0]+offset[0]-tx, p[1]+offset[1]-ty), -k)
            return reflection(q) if r else q

        inverses.append(inverse)
        hands.append(-1 if r else 1)
    equations, first, interfaces = set(), {}, 0
    for u, a in sorted(owners.items()):
        for dx, dy in NEIGHBORS:
            v = u[0]+dx, u[1]+dy
            b = owners.get(v)
            if b is None or a >= b:
                continue
            i = index[inverses[a](u), inverses[a](v)]
            j = index[inverses[b](v), inverses[b](u)]
            row = min(i, j), max(i, j), hands[a]*hands[b]
            equations.add(row)
            first.setdefault(row, {'equation': list(row), 'copies': [a, b],
                'cells': [list(u), list(v)], 'original_ports': [i, j]})
            interfaces += 1
    return len(ports), sorted(equations), first, interfaces, checks


def coefficient_row(n, i, j, delta):
    row = [0] * n
    row[j] += 1
    row[i] -= delta
    return row


def eliminate(matrix, n):
    """Independent exact rank; determinant when the input is square."""
    rows = [list(map(Fraction, row)) for row in matrix]
    rank, determinant, swaps = 0, Fraction(1), 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            swaps += 1
        value = rows[rank][col]
        determinant *= value
        rows[rank] = [x/value for x in rows[rank]]
        for i in range(rank+1, len(rows)):
            value = rows[i][col]
            if value:
                rows[i] = [x-value*y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    det = determinant * (-1 if swaps % 2 else 1) if len(rows) == n and rank == n else 0
    return rank, str(det) if len(rows) == n else None


def signed_components(n, equations):
    adjacency = [[] for _ in range(n)]
    for i, j, delta in equations:
        adjacency[i].append((j, delta))
        if i != j:
            adjacency[j].append((i, delta))
    remaining, output = set(range(n)), []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        signs, parents, queue, conflict = {root: 1}, [], deque([root]), None
        while queue:
            i = queue.popleft()
            for j, delta in sorted(adjacency[i]):
                if j not in signs:
                    signs[j] = signs[i]*delta
                    remaining.remove(j)
                    parents.append((min(i, j), max(i, j), delta))
                    queue.append(j)
                elif signs[j] != signs[i]*delta and conflict is None:
                    conflict = min(i, j), max(i, j), delta
        output.append({'ports': sorted(signs), 'balanced': conflict is None,
            'tree_equations': [list(e) for e in parents],
            'conflict_equation': list(conflict) if conflict else None,
            'coefficient_signs': [signs[i] for i in sorted(signs)] if conflict is None else None})
    return output


def analyze(witness):
    n, equations, first, interfaces, checks = contacts(witness)
    even_eq = sorted({(i, j, -1) for i, j, _ in equations})
    even = signed_components(n, even_eq)
    odd = signed_components(n, equations)
    even_rows = [coefficient_row(n, *e) for e in even_eq]
    odd_rows = [coefficient_row(n, *e) for e in equations]
    rank_even, _ = eliminate(even_rows, n)
    rank_odd, _ = eliminate(odd_rows, n)
    even_free = sum(c['balanced'] for c in even)
    odd_free = sum(c['balanced'] for c in odd)
    if (n-rank_even, n-rank_odd) != (even_free, odd_free):
        raise ValueError('exact ranks disagree with signed components')
    # One spanning tree plus an inconsistent edge is a full-rank block.
    odd_core = []
    if odd_free == 0:
        for c in odd:
            odd_core.extend(c['tree_equations'])
            odd_core.append(c['conflict_equation'])
        core_rank, determinant = eliminate([coefficient_row(n, *e) for e in odd_core], n)
        if len(odd_core) != n or core_rank != n or determinant == '0':
            raise ValueError('odd full-rank core failed')
    else:
        determinant = None
    # Recover original all-contact coefficient vector when it spans the even
    # kernel. This is checked by multiplication, independently of BFS signs.
    fixture_vector = witness['signs']
    vector_valid = any(fixture_vector) and all(
        sum(a*b for a, b in zip(row, fixture_vector)) == 0 for row in even_rows)
    return {'ports': n, 'copies': len(witness['patch']),
        'unit_interfaces': interfaces, 'distinct_signed_equations': len(equations),
        'fixed_patch_checks': checks, 'even_coefficient_rank': rank_even,
        'odd_coefficient_rank': rank_odd, 'free_even_functions': even_free,
        'free_odd_functions': odd_free, 'even_components': even,
        'odd_components': odd, 'odd_full_rank_core_determinant': determinant,
        'odd_full_rank_core': [first[tuple(e)] for e in odd_core],
        'fixture_vector_is_even_kernel_vector': bool(vector_valid)}


def main():
    path = Path(__file__).with_name('signed_hex4_depth5.witness.json')
    if hashlib.sha256(path.read_bytes()).hexdigest() != FIXTURE_SHA256:
        raise ValueError('fixed baseline differs from published input')
    witness = json.loads(path.read_text())
    result = analyze(witness)
    if (result['ports'], result['copies'], result['unit_interfaces'],
        result['distinct_signed_equations'], result['even_coefficient_rank'],
        result['odd_coefficient_rank'], result['free_even_functions'],
        result['free_odd_functions'], result['odd_full_rank_core_determinant']) != (
            18, 131, 1075, 38, 17, 18, 1, 0, '4'):
        raise ValueError('fixed baseline profile certificate changed')
    if not result['fixture_vector_is_even_kernel_vector']:
        raise ValueError('baseline signed vector failed the even equations')
    result.update(agent='six-heesch-3', role='researcher',
        fixture_sha256=FIXTURE_SHA256,
        theorem='q_i(t)=s_i*e(t) for one symmetric function e; q_17=0',
        signs=witness['signs'],
        scope='fixed motions, chords, complete full-unit-port coincidences; other corona patches remain open')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
