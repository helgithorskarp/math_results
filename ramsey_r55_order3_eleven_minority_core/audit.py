#!/usr/bin/env python3
"""Definition-level audit: literal graphs, vertex maps, and complete cube files."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import random


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph(code):
    bits = list(map(int, code))
    require(len(bits) == 9 and set(bits) <= {0, 1}, 'bad core bits')
    adj = [[False]*9 for _ in range(9)]
    pair = [(0, 1), (0, 2), (1, 2)]
    for a, b in combinations(range(9), 2):
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        red = i == j or bool(bits[3*pair.index((i, j))+(t-s) % 3])
        adj[a][b] = adj[b][a] = red
    return adj


def encode(adj, mapping):
    return ''.join(str(int(adj[mapping[3*i]][mapping[3*j+d]]))
                   for i, j in ((0, 1), (0, 2), (1, 2)) for d in range(3))


def audit_cover(data):
    require(data['format'] == 'r55-k11-r3-core-cover-v1', 'cover format')
    require([r['index'] for r in data['cases']] == list(range(14)), 'case coverage')
    maps = []
    for perm in permutations(range(3)):
        for shift in product(range(3), repeat=3):
            for sign in (1, -1):
                maps.append((sign, [3*perm[i]+(sign*s+shift[i]) % 3
                                    for i in range(3) for s in range(3)]))
    all_codes, seen, details = set(), set(), []
    for v in range(512):
        code = format(v, '09b')
        adj = graph(code)
        bad = any(len({adj[a][b] for a, b in combinations(five, 2)}) == 1
                  for five in combinations(range(9), 5))
        no_complete = all(code[q:q+3] != '111' for q in (0, 3, 6))
        require(bad != no_complete, 'nine-vertex Ramsey equivalence')
        if not bad:
            all_codes.add(code)
    count = 0
    for row in data['cases']:
        adj = graph(row['bits'])
        orbit = {encode(adj, m) for _, m in maps}
        require(orbit == set(row['members']) and len(orbit) == row['labeled'], 'literal orbit mismatch')
        require(not seen & orbit, 'duplicate orbit')
        seen |= orbit
        norm = [c for c in orbit if c[:3] in ('000', '100', '110')
                and c[3:6] in ('000', '100', '110') and c[:3].count('1') <= c[3:6].count('1')]
        require(min(norm) == row['bits'] and len(norm) == row['normalized'], 'normal representative')
        for code in orbit:
            source = graph(code)
            for _, m in maps:
                target_code = encode(source, m)
                require(target_code in orbit, 'orbit not closed')
                target = graph(target_code)
                require(all(target[a][b] == source[m[a]][m[b]] for a, b in combinations(range(9), 2)),
                        'literal edge transport mismatch')
                count += 1
        sigs = []
        for sig in product((0, 1), repeat=3):
            allowed = True
            for color in (False, True):
                neighbors = [v for v in range(9) if bool(sig[v//3]) == color]
                if any(all(adj[a][b] == color for a, b in combinations(four, 2))
                       for four in combinations(neighbors, 4)):
                    allowed = False
            if allowed:
                sigs.append(''.join(map(str, sig)))
        details.append(dict(index=row['index'], fixed_vertex_signatures=sigs))
    require(seen == all_codes and len(seen) == 343 and count == 111132, 'complete domain')
    require(sum(r['normalized'] for r in data['cases']) == data['normalized_cores'] == 42, 'normalized count')
    # Extend every minority map to a normalizer of the entire eleven-cycle action.
    # Reflection, when used, acts on every moving cycle, including the eight blue ones.
    def sigma(v, sign=1):
        return 3*(v//3)+(v % 3+sign) % 3 if v < 33 else v
    rng = random.Random(55110314)
    pair_ids = {}
    for pair in combinations(range(43), 2):
        orb, p = [], pair
        while p not in orb:
            orb.append(p)
            p = tuple(sorted((sigma(p[0]), sigma(p[1]))))
        pair_ids[pair] = min(orb)
    values = {x: bool(rng.randrange(2)) for x in sorted(set(pair_ids.values()))}
    for sign, small in maps:
        m = small+[3*i+(sign*s) % 3 for i in range(3, 11) for s in range(3)]+list(range(33, 43))
        require(sorted(m) == list(range(43)), 'not a full vertex permutation')
        require(all(m[sigma(v)] == sigma(m[v], sign) for v in range(43)), 'normalizer identity')
        for a, b in combinations(range(43), 2):
            p = tuple(sorted((m[a], m[b])))
            q = tuple(sorted((m[sigma(a)], m[sigma(b)])))
            require(values[pair_ids[p]] == values[pair_ids[q]], 'full graph lost invariance')
    return dict(labeled_core_graphs=512, valid_core_graphs=343, classes=14,
                normalized_cores=42, literal_transports=count,
                full_normalizer_maps=324, full_pair_controls=324*903, signatures=details)


def units(code):
    """Recover primary variable meanings through the actual 43-vertex pair action."""
    def sigma(v):
        return 3*(v//3)+(v % 3+1) % 3 if v < 33 else v
    mapping, nv = {}, 0
    # The parent assigns moving-cross orbits first, by least pair representative.
    for a, b in combinations(range(33), 2):
        if a//3 == b//3 or (a, b) in mapping:
            continue
        nv += 1
        p = (a, b)
        while p not in mapping:
            mapping[p] = nv
            p = tuple(sorted((sigma(p[0]), sigma(p[1]))))
    require(nv == 165, 'cross-orbit count')
    variables = [mapping[3*i, 3*j+d] for i, j in ((0, 1), (0, 2), (1, 2)) for d in range(3)]
    require(variables == [1, 2, 3, 4, 5, 6, 31, 32, 33], 'core primary convention')
    return [v if b == '1' else -v for v, b in zip(variables, code)]


def audit_cube(parent, cube, code):
    with parent.open('rb') as a, cube.open('rb') as b:
        header = a.readline().split()
        require(header[:2] == [b'p', b'cnf'], 'parent header')
        nv, nc = map(int, header[2:])
        require(b.readline() == f'p cnf {nv} {nc+9}\n'.encode(), 'cube header')
        for _ in range(nc):
            line = a.readline()
            require(bool(line) and b.readline() == line, 'cube parent prefix')
        require(a.read() == b'', 'parent extra bytes')
        for unit in units(code):
            require(b.readline() == f'{unit} 0\n'.encode(), 'cube unit')
        require(b.read() == b'', 'cube extra bytes')
    return dict(variables=nv, clauses=nc+9, appended_units=9, complete_prefix=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = audit_cover(json.loads(a.cover.read_text()))
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('PASS literal 512-graph census and all 111132 transports')
