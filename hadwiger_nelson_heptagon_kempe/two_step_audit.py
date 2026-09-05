"""Directly construct every second-step row, using disjoint-set components."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

from audit import groups, proper, PARENT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    here = Path(__file__).parent
    expected = json.loads((here / 'two_step_expected.json').read_text())
    assert expected == json.loads((args.out / 'result.json').read_text())
    raw = (args.graph_work / 'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['graph_sha256']
    g = json.loads(raw)
    pts = list(map(tuple, g['points']))
    lookup = {v: i for i, v in enumerate(pts)}
    h = g['host']
    labels = [[lookup[tuple(x-y for x, y in zip(a, b))] for b in h] for a in h]
    anchors = [labels[0][0], labels[7][0], labels[14][0]]
    targets = json.loads((here / 'expected.json').read_text())['unresolved_pairs']
    potentials = json.loads((PARENT / 'potentials.json').read_text())
    trace_raw = (args.out / 'decompositions.json').read_bytes()
    assert sha256(trace_raw).hexdigest() == expected['component_trace_sha256']
    assert len(trace_raw) == expected['component_trace_bytes']
    trace = json.loads(trace_raw)
    first_rows, first_provenance = [], []
    for si, p in enumerate(potentials):
        c = [-1]*421
        for a in range(21):
            for b in range(21):
                vertex = labels[a][b]
                assert c[vertex] in (-1, p[a] ^ p[b])
                c[vertex] = p[a] ^ p[b]
        assert proper(c, g['edges'], 421)
        for a, b in combinations(range(4), 2):
            for block in groups(421, g['edges'], c, a, b):
                d = c.copy()
                for v in block:
                    d[v] = b if c[v] == a else a
                rename = {d[v]: i for i, v in enumerate(anchors)}
                assert len(rename) == 3
                rename[next(v for v in range(4) if v not in rename)] = 3
                row = bytes(rename[v] for v in d)
                assert proper(row, g['edges'], 421)
                assert all(row[u] != row[v] for u, v in targets)
                first_rows.append(row)
                first_provenance.append([si, a, b, block])
    assert first_provenance == trace['first_provenance']
    assert len(first_rows) == len(set(first_rows)) == expected['distinct_first_rows']
    assert sha256(b''.join(sorted(first_rows))).hexdigest() == expected['first_row_stream_sha256']
    assert len(trace['second_partitions']) == len(first_rows)
    count = 0
    hits = set()
    for i, c in enumerate(first_rows):
        assert len(trace['second_partitions'][i]) == 6
        for j, (a, b) in enumerate(combinations(range(4), 2)):
            blocks = groups(421, g['edges'], c, a, b)
            assert blocks == trace['second_partitions'][i][j]
            for block in blocks:
                d = list(c)
                for v in block:
                    d[v] = b if c[v] == a else a
                assert proper(d, g['edges'], 421)
                hits.update((u, v) for u, v in targets if d[u] == d[v])
                count += 1
    assert count == expected['second_components']
    assert hits == set(map(tuple, expected['newly_covered_pairs']))
    assert not hits  # This frozen checkpoint has no newly covered pair.
    result = {
        'status': 'TWO-STEP CENSUS VERIFIED; 42 PAIRS REMAIN UNRESOLVED',
        'first_provenance_records_compared': len(first_rows),
        'second_partitions_compared_entrywise': len(first_rows)*6,
        'second_colourings_directly_checked': count,
        'second_unit_edge_checks': count*len(g['edges']),
        'second_residual_pair_checks': count*len(targets),
        'seconds': time.perf_counter()-started
    }
    (args.out / 'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
