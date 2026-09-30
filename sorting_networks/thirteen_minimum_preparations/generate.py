"""Bitmask/DFS regeneration of the new minimum-preparation certificate.
Author six-sorting-1, researcher. No scalar-checker imports.
Finite closure of actual one-zero trajectories and strongest two-zero rows.
"""
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(11), 2))


def starting(fixture):
    cases = []
    for j in (1, 2):
        prefix = fixture['prefix21'] + fixture['tournaments'][str(j)]
        records = {}
        for a, b in PAIRS + tuple((a, b) for a, b in itertools.combinations(range(13), 2) if b >= 11):
            x = (1 << a) | (1 << b)
            deletion = 0
            for u, v in prefix:
                A, B = 1 << u, 1 << v
                deletion += bool(x & (A | B))
                if x & B and not x & A:
                    x ^= A | B
            records[x] = max(records.get(x, deletion), deletion)
        cases.append(tuple(sorted(records.items())))
    assert cases[0] == cases[1] == tuple(sorted(map(tuple, fixture['initial_two_minimum_profile'])))
    return cases[0]


def update(profile, gate):
    A, B = 1 << gate[0], 1 << gate[1]
    records = {}
    for x, deletion in profile:
        deletion += bool(x & (A | B))
        if x & B and not x & A:
            x ^= A | B
        records[x] = max(records.get(x, deletion), deletion)
    if sum(1 << d for d in records.values()) > 512:
        return None
    return tuple(sorted(records.items()))


def main():
    begun = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    initial = starting(fixture)
    root = (0, (0, 1, 5), (0, 0, 0), initial)
    known = {root}
    stack = [root]
    edges = prep_cuts = route_cuts = weight_cuts = 0
    while stack:
        assert len(known) < 50000 and time.monotonic() - begun < 45, 'Incomplete: operational algorithmic budget'
        nongates, positions, counts, profile = stack.pop()
        assert positions != (0, 0, 0), 'A terminal survived; theorem false'
        for a, b in PAIRS:
            edges += 1
            touched = tuple(p == a or p == b for p in positions)
            non = nongates + (not any(touched))
            if non > 2:
                prep_cuts += 1
                continue
            charged = tuple(q + h for q, h in zip(counts, touched))
            moved = tuple(a if h else p for p, h in zip(positions, touched))
            if (any(c > cap for c, cap in zip(charged, (3, 2, 3))) or
                moved != (0, 0, 0) and any(c >= cap for c, cap in zip(charged, (3, 2, 3))) or
                moved == (0, 0, 0) and charged[1] != 2):
                route_cuts += 1
                continue
            updated = update(profile, (a, b))
            if updated is None:
                weight_cuts += 1
                continue
            child = non, moved, charged, updated
            if child not in known:
                known.add(child)
                stack.append(child)
    digest = hashlib.sha256()
    for state in sorted(known):
        digest.update(json.dumps(state, separators=(',', ':')).encode())
    result = {'agent':'six-sorting-1','role':'researcher','status':'complete_bitmask_DFS_closure',
              'n':11,'max_preparations':2,'states':len(known),'edges':edges,
              'preparation_cuts':prep_cuts,'route_cuts':route_cuts,'weight_cuts':weight_cuts,
              'state_sha256':digest.hexdigest(),'seconds':time.monotonic()-begun,
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    expected = json.loads((HERE/'certificate.json').read_text())
    assert expected['fixture_sha256'] == hashlib.sha256((HERE/'fixture.json').read_bytes()).hexdigest()
    assert fixture['conditional_minimum1_passages'] == 2 and fixture['minimum_route_caps'] == [3, 2, 3]
    for key in ('n','max_preparations','states','edges','preparation_cuts','route_cuts','weight_cuts','state_sha256'):
        assert result[key] == expected[key], (key, result[key], expected[key])
    print(json.dumps(result))


if __name__=='__main__':
    main()
