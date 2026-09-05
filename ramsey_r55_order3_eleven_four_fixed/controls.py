#!/usr/bin/env python3
"""Certificate rejection and an independent integer check of the equality case."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
from verify import audit_row, need, parse, preflight, SIG


def equality_profiles():
    """Enumerate incidence profiles using only the proved elementary inequalities."""
    counts = [0]*16
    survivors, visited = [], 0

    def visit(mask, n, degrees):
        nonlocal visited
        visited += 1
        if mask == 16:
            if n == 10:
                survivors.append(counts.copy())
            return
        coordinates = [i for i in range(4) if mask >> i & 1]
        upper = min([10-n]+[4-degrees[i] for i in coordinates])
        if len(coordinates) == 1:
            upper = min(upper, 1)
        elif len(coordinates) == 2:
            upper = min(upper, *(2-counts[1 << i] for i in coordinates))
        for value in range(upper+1):
            counts[mask] = value
            visit(mask+1, n+value,
                  [d+value*(i in coordinates) for i, d in enumerate(degrees)])
        counts[mask] = 0
    visit(1, 0, [0]*4)
    expected = [int(mask in SIG) for mask in range(16)]
    need(survivors == [expected], 'equality profile projection')
    return dict(profiles=len(survivors), nodes=visited, unique_profile=expected)


def run(cover_path, source, report):
    result = json.loads((source/'result.json').read_text())
    cover = json.loads(cover_path.read_text())
    rejected = []

    def reject(name, f):
        try:
            f()
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(name)
        else:
            raise ValueError('accepted malformed certificate: '+name)

    broken = copy.deepcopy(result)
    broken['cases'].pop()
    reject('missing_class', lambda: preflight(broken, cover))
    duplicate = copy.deepcopy(result)
    duplicate['cases'][1] = duplicate['cases'][0]
    reject('duplicate_class', lambda: preflight(duplicate, cover))
    row = copy.deepcopy(result['cases'][0])
    row['allowed'] = [0]+row['allowed']
    reject('forbidden_zero_signature', lambda: audit_row(row, cover['cases'][0]['bits'], source/'graphs'))
    bad_hash = copy.deepcopy(result['cases'][0])
    bad_hash['edge_sha256'][0] = '0'*64
    reject('wrong_edge_digest', lambda: audit_row(bad_hash, cover['cases'][0]['bits'], source/'graphs'))
    raw = (source/'graphs/core000_v0.edges').read_bytes()
    reject('truncated_edges', lambda: parse(raw.rsplit(b'\n', 2)[0]+b'\n'))
    reject('out_of_range_edge', lambda: parse(b'22 1\n0 22\n'))
    reject('duplicate_edge', lambda: parse(b'22 2\n0 1\n0 1\n'))
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        for variant in (0, 1, 2, 4):
            name = f'core000_v{variant}.edges'
            (dest/name).write_bytes((source/'graphs'/name).read_bytes())
        adj = parse(raw)
        # A different, well-formed graph must still fail the exact template contract.
        from verify import serialize
        adj[0] ^= 1 << 1
        adj[1] ^= 1 << 0
        (dest/'core000_v0.edges').write_bytes(serialize(adj))
        reject('changed_template_edge', lambda: audit_row(result['cases'][0], cover['cases'][0]['bits'], dest))
    out = dict(rejected=rejected, equality=equality_profiles())
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    run(a.cover, a.source, a.report)
