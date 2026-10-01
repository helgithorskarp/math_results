#!/usr/bin/env python3
"""Independent fixed-first/resource Y18 census, compared entrywise to literal."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import argparse
import json
import sys
import time

SOURCE = Path(__file__).resolve().parent.parent / 'two_fixed_saturated_upper60'
sys.path.insert(0, str(SOURCE))
import model as M
import seeds
import second_stars as S


def run(args):
    M.require(not args.output.exists(), 'use new primary output')
    started = time.monotonic()
    roots, _ = seeds.root_cases()
    resources, rows = M.orbit_carrier()
    anchors, records = [], []
    for root in roots:
        residual = M.residual(root['anchor'], resources, rows)
        fixed = tuple(r for r in residual if r['weight'] == 1 and r['replications'][17] == 1)
        paired = tuple(r for r in residual if r['weight'] == 2 and r['replications'][17] == 2)
        M.require(all(r['replications'][16] == 0 for r in fixed+paired), 'unsaturated X row')
        for f in (4, 2, 0):
            configurations, covers, nodes = 0, 0, 0
            for choice in combinations(range(len(fixed)), f):
                used = [set(fixed[i]['resources']) for i in choice]
                if any(a & b for a, b in combinations(used, 2)):
                    continue
                base = tuple(sorted(root['anchor'] + tuple(fixed[i]['words'][0] for i in choice)))
                M.check_code(base)
                available = M.residual(base, resources, paired)
                sets = tuple(frozenset(r['resources']) for r in available)
                adjacency = tuple(sum(1 << j for j in range(len(available)) if i != j and
                                      not sets[i] & sets[j]) for i in range(len(available)))
                cliques, visited = S.cliques(adjacency, (18-4-f)//2)
                configurations += 1
                nodes += visited
                covers += len(cliques)
                for q in cliques:
                    words = tuple(sorted(base+tuple(w for i in q for w in available[i]['words'])))
                    stats = M.check_code(words)
                    M.require(stats['words'] == 34 and stats['replications'][16:] == (20, 18) and
                              stats['fixed_words'] == 4+f, 'fixed-first Y18 decoding')
                    anchors.append(dict(fixture=root['fixture'], fixed_Y=f, words=words))
            record = dict(fixture=root['fixture'], fixed_Y=f, fixed_configurations=configurations,
                          paired_completions=covers, nodes=nodes)
            records.append(record)
            print(json.dumps(record, sort_keys=True), flush=True)
    actual = tuple(sorted((a['fixture'], a['fixed_Y'], tuple(a['words'])) for a in anchors))
    M.require(len(actual) == len(set(actual)), 'duplicate fixed-first Y18 anchor')
    literal = json.loads(args.literal.read_text())
    M.require(literal['status'] == 'COMPLETE requested literal Y18 census' and literal['all_Y18_counts'],
              'incomplete literal Y18 census')
    expected = tuple(sorted((a['fixture'], a['fixed_Y'], tuple(a['words'])) for a in literal['anchors']))
    M.require(actual == expected, 'fixed-first and paired-first Y18 anchors differ entrywise')
    result = dict(agent='six-code-2', role='researcher', status='COMPLETE fixed-first Y18 census',
                  anchors=anchors, records=records, anchor_count=len(anchors),
                  anchors_sha256=sha256(M.encoded(anchors)).hexdigest(),
                  canonical_sha256=sha256(M.encoded(actual)).hexdigest(),
                  paired_first_entrywise=True, seconds=time.monotonic()-started)
    args.output.write_bytes(M.encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('anchors','records')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--literal', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args())
