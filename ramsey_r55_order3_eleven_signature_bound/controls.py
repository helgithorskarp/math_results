#!/usr/bin/env python3
"""Exact arithmetic, sharp graph fixtures, and primary-cut semantics."""
from pathlib import Path
import argparse
import json
import audit
import model


def controls(work):
    a, b = model.arithmetic(), audit.direct_arithmetic()
    model.require(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), 'arithmetic mismatch')
    model.require(model.tail() == audit.expected_tail(), 'literal tail reconstruction')
    fixtures = []
    for index, bits in model.CORES.items():
        p = work / f'core{index}.edges'
        p.write_text(model.fixture(index))
        report = audit.inspect(p)
        model.require(report['core_words'] == bits, 'fixture core')
        fixtures.append(dict(index=index, **report))
    original = (work / 'core8.edges').read_text().splitlines()
    rejected = []
    for name in ('duplicate_edge', 'wrong_order', 'planted_red_five'):
        rows = original.copy()
        if name == 'duplicate_edge':
            rows.append(rows[-1])
        elif name == 'wrong_order':
            rows[0] = '43 81'
        else:
            edges = {tuple(map(int, line.split())) for line in rows[1:]}
            edges.update((a, b) for a in range(5) for b in range(a+1, 5))
            rows = [f'19 {len(edges)}']+[f'{a} {b}' for a, b in sorted(edges)]
        p = work / (name+'.edges')
        p.write_text('\n'.join(rows)+'\n')
        try:
            audit.inspect(p)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed fixture accepted')
        p.unlink()
    return dict(arithmetic=a, fixtures=fixtures, cut_semantics=audit.semantic_controls(),
                signature_clauses=1623, rejected_fixture_mutations=rejected)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    model.require(not a.work.resolve().is_relative_to(model.ROOT.parent), 'control output outside Git')
    a.work.mkdir(parents=True, exist_ok=True)
    report = controls(a.work)
    (a.work / 'controls.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('PASS arithmetic, three sharp 19-vertex fixtures and all cut truth tables')
