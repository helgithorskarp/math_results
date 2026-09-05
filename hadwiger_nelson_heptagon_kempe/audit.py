"""Disjoint-set replay and direct potential reconstruction; no run.py import."""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'hadwiger_nelson_heptagon_difference_lifts'


def groups(n, edges, c, a, b):
    parent = list(range(n))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        if c[u] in (a, b) and c[v] in (a, b):
            parent[root(u)] = root(v)
    result = defaultdict(list)
    for v in range(n):
        if c[v] in (a, b):
            result[root(v)].append(v)
    return sorted(result.values())


def proper(row, edges, n):
    return len(row) == n and all(type(v) is int and 0 <= v < 4 for v in row) and all(row[u] != row[v] for u, v in edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    raw = (args.graph_work / 'graph.json').read_bytes()
    expected = json.loads((HERE / 'expected.json').read_text())
    assert sha256(raw).hexdigest() == expected['graph_sha256']
    g = json.loads(raw)
    pts = [tuple(p) for p in g['points']]
    lookup = {p: i for i, p in enumerate(pts)}
    h = g['host']
    difference = lambda a, b: tuple(x-y for x, y in zip(a, b))
    labels = [[lookup[difference(a, b)] for b in h] for a in h]
    origin = labels[0][0]
    anchors = [origin, labels[7][0], labels[14][0]]
    opposite = [lookup[tuple(-x for x in p)] for p in pts]
    potentials = json.loads((PARENT / 'potentials.json').read_text())
    records, outcomes, covered = [], set(), set()
    seeds = []
    for p in potentials:
        row = [-1]*421
        for a in range(21):
            for b in range(21):
                i = labels[a][b]
                assert row[i] in (-1, p[a] ^ p[b])
                row[i] = p[a] ^ p[b]
        assert proper(row, g['edges'], 421)
        seeds.append(row)
    # A differently labelled four-colouring is potential exactly when this
    # origin-zero translation reconstructs all ordered differences.
    def is_potential(c):
        z = c[origin]
        p = [c[labels[a][0]] ^ z for a in range(21)]
        return all((c[labels[a][b]] ^ z) == (p[a] ^ p[b])
                   for a in range(21) for b in range(21))

    for si, c in enumerate(seeds):
        for a, b in combinations(range(4), 2):
            blocks = groups(421, g['edges'], c, a, b)
            block_of = {v: k for k, block in enumerate(blocks) for v in block}
            # Exact criterion for swapping any union of these blocks.
            for u, v in g['sqrt3_pairs']:
                if {c[u], c[v]} == {a, b} and block_of[u] != block_of[v]:
                    covered.add((u, v))
            for block in blocks:
                changed = c.copy()
                for v in block:
                    changed[v] = b if c[v] == a else a
                assert proper(changed, g['edges'], 421)
                # Normalize by explicitly locating the three anchor colours.
                rename = {changed[v]: k for k, v in enumerate(anchors)}
                assert len(rename) == 3
                for value in range(4):
                    if value not in rename:
                        rename[value] = 3
                row = bytes(rename[v] for v in changed)
                outcomes.add(row)
                records.append({
                    'seed': si, 'colours': [a, b], 'component': block,
                    'row_sha256': sha256(row).hexdigest(),
                    'potential': is_potential(row),
                    'antipodal': all(row[v] == row[opposite[v]] for v in range(421)),
                    'monochromatic_pairs': [p for p in g['sqrt3_pairs'] if row[p[0]] == row[p[1]]]
                })
    assert records == json.loads((args.out / 'records.json').read_text())
    assert expected == json.loads((args.out / 'result.json').read_text())
    assert covered == set(map(tuple, expected['covered_pairs']))
    assert sha256(b''.join(sorted(outcomes))).hexdigest() == expected['normalized_outcome_stream_sha256']
    assert sum(not r['potential'] for r in records) == expected['nonpotential_outcomes']
    witnesses = json.loads((HERE / 'witnesses.json').read_text())
    assert witnesses == json.loads((args.out / 'witnesses.json').read_text())
    for witness in witnesses:
        assert witness['potential'] == potentials[witness['seed']]
        matches = [r for r in records if all(r[k] == witness[k] for k in
                   ['seed', 'colours', 'component', 'row_sha256'])]
        assert len(matches) == 1 and witness['terminal_pair'] in matches[0]['monochromatic_pairs']
    # In particular the previously UNKNOWN pair has a one-vertex witness.
    first = witnesses[0]
    assert first['terminal_pair'] == [0, 332] and first['component'] == [332]
    c = seeds[first['seed']].copy()
    c[332] ^= 1  # swap colours 2 and 3 on this singleton
    assert c[0] == c[332] and proper(c, g['edges'], 421)
    assert c[332] != c[opposite[332]] and not is_potential(c)
    # Bad colour strings must fail the direct edge/domain check.
    bad = c.copy(); bad[g['edges'][0][0]] = bad[g['edges'][0][1]]
    assert not proper(bad, g['edges'], 421)
    assert not proper(c[:-1], g['edges'], 421)
    bad = c.copy(); bad[0] = 4
    assert not proper(bad, g['edges'], 421)
    # Discharge both old UNKNOWN encodings with this explicit assignment.
    renamed = [{3: 0, 0: 1, 1: 2, 2: 3}[v] for v in c]
    assert [renamed[i] for i in [0, 332, 15, 22]] == [0, 0, 1, 2]
    formulas = []
    with TemporaryDirectory(dir=args.out) as temporary:
        for encoding in ['onehot', 'alo']:
            filename = Path(temporary) / (encoding + '.cnf')
            process = subprocess.run([
                sys.executable, '-B', str(PARENT / 'query.py'),
                '--work', str(args.graph_work), '--encoding', encoding,
                '--output', str(filename)], check=True, text=True, capture_output=True)
            metadata = json.loads(process.stdout)
            raw_cnf = filename.read_bytes()
            lines = raw_cnf.decode().splitlines()
            assert lines[0] == f"p cnf 1684 {metadata['clauses']}"
            for line in lines[1:]:
                literals = list(map(int, line.split()))
                assert literals.pop() == 0 and literals
                assert all(1 <= abs(literal) <= 1684 for literal in literals)
                assert any((renamed[(abs(literal)-1)//4] == (abs(literal)-1)%4)
                           == (literal > 0) for literal in literals)
            assert len(lines)-1 == metadata['clauses']
            digest = sha256(raw_cnf).hexdigest()
            assert digest == metadata['sha256']
            if encoding == 'alo':
                assert digest == 'cd4a235652de1ca3d74bc0c8b06d33799a6a0196e360f1531c12f00322dfbcdd'
            formulas.append({'encoding': encoding, 'clauses': len(lines)-1,
                             'sha256': digest, 'status': 'EXPLICIT MODEL VERIFIED'})
    result = {'status': 'ALL 1260 SWAPS AND SIX ORBIT WITNESSES VERIFIED',
              'records_compared_entrywise': len(records),
              'direct_potential_reconstructions': len(records),
              'union_swap_criterion_covered_pairs': len(covered),
              'remaining_pairs_unresolved': 126-len(covered),
              'invalid_colourings_rejected': 3,
              'previous_unknown_formulas': formulas,
              'seconds': time.perf_counter()-start}
    (args.out / 'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
