#!/usr/bin/env python3
"""Paired-first Y18 star census with actual quadruple-pair sets.

All roots still have X20 and lambdaXY4. Unlike the first inventory, this may
also enumerate fixed Y-word counts zero and two. No subfamily absence follows
until the literal census and its residual completion are both finished.
"""
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
import literal


def anchors_for(anchor, fixed_count):
    fixed, paired = literal.literal_rows(anchor)
    target = (18 - 4 - fixed_count)//2
    output, paired_covers, nodes, fixed_tests = [], 0, 0, 0
    start = time.monotonic()

    def tick():
        nonlocal nodes
        nodes += 1
        if nodes > 200000 or time.monotonic()-start > 10:
            raise RuntimeError('INCOMPLETE paired-first Y18 guard')

    def finish(chosen, occupied):
        nonlocal paired_covers, fixed_tests
        paired_covers += 1
        eligible = tuple(r for r in fixed if not r['pairs'] & occupied)
        supports = tuple(frozenset(v//2 for v in r['quads'][0]) for r in eligible)
        M.require(all(len(s) == 2 for s in supports), 'fixed quadruple support')
        for selected in combinations(range(len(eligible)), fixed_count):
            fixed_tests += 1
            if fixed_tests > 200000 or time.monotonic()-start > 10:
                raise RuntimeError('INCOMPLETE fixed-last Y18 guard')
            if len(set().union(*(supports[i] for i in selected))) != 2*fixed_count:
                continue
            words = tuple(sorted(tuple(anchor) + tuple(w for i in chosen for w in paired[i]['words']) +
                                 tuple(eligible[i]['words'][0] for i in selected)))
            stats = M.check_code(words)
            M.require(stats['words'] == 34 and stats['replications'][16:] == (20, 18) and
                      stats['fixed_words'] == 4+fixed_count, 'literal Y18 decoding')
            output.append(words)

    def search(indices, chosen, occupied):
        tick()
        need = target-len(chosen)
        if not need:
            finish(chosen, occupied)
            return
        for j, index in enumerate(indices):
            if len(indices)-j < need:
                return
            row = paired[index]
            if row['pairs'] & occupied:
                continue
            future = tuple(k for k in indices[j+1:] if not row['pairs'] & paired[k]['pairs'])
            search(future, chosen+(index,), occupied | row['pairs'])

    search(tuple(range(len(paired))), (), frozenset())
    M.require(len(output) == len(set(output)), 'duplicate literal Y18 anchor')
    return tuple(sorted(output)), dict(fixed_Y=fixed_count, paired_Y=target,
                                       paired_candidates=len(paired), fixed_candidates=len(fixed),
                                       paired_covers=paired_covers, fixed_tests=fixed_tests,
                                       nodes=nodes, anchors=len(output), seconds=time.monotonic()-start)


def run(args):
    M.require(not args.output.exists(), 'use new literal output')
    roots, _ = seeds.root_cases()
    fixed_counts = (4, 2, 0) if args.fixed == 'all' else (int(args.fixed),)
    records, anchors = [], []
    for root in roots:
        for f in fixed_counts:
            words, record = anchors_for(root['anchor'], f)
            records.append(dict(fixture=root['fixture'], **record))
            anchors.extend(dict(fixture=root['fixture'], fixed_Y=f, words=w) for w in words)
            print(json.dumps(records[-1], sort_keys=True), flush=True)
    primary = json.loads(args.primary.read_text())
    primary_words = tuple(sorted(tuple(a['words']) for a in primary['anchors']))
    actual_four = tuple(sorted(tuple(a['words']) for a in anchors if a['fixed_Y'] == 4))
    if 4 in fixed_counts:
        M.require(actual_four == primary_words, 'paired-first Y18 census differs entrywise')
    result = dict(agent='six-code-2', role='researcher',
                  status='COMPLETE requested literal Y18 census',
                  scope='X20, Y18, lambdaXY4, fixedY counts '+','.join(map(str, fixed_counts)),
                  records=records, anchors=anchors, all_Y18_counts=sorted(fixed_counts)==[0,2,4],
                  anchor_count=len(anchors), anchors_sha256=sha256(M.encoded(anchors)).hexdigest(),
                  entrywise_primary_fixedY4=4 in fixed_counts, residual_search_status='NOT RUN')
    args.output.write_bytes(M.encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('anchors','records')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--primary', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--fixed', choices=('4','2','0','all'), default='4')
    run(p.parse_args())
