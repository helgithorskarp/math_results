#!/usr/bin/env python3
"""Canonicalize FINAL_OBSTRUCTION records from range-search stderr logs."""

import argparse,itertools,re
from collections import defaultdict

PATTERN=re.compile(r'^FINAL_OBSTRUCTION core=(\d+) models=([0-9a-f]+),([0-9a-f]+),([0-9a-f]+) edge_bits=([07]) color=(K5|I5) old_pair_mask=([0-9a-f]+)$')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('logs',nargs='+');args=ap.parse_args()
    groups=defaultdict(list);raw=0
    for path in args.logs:
        for line in open(path):
            m=PATTERN.fullmatch(line.strip())
            if not m:continue
            core=int(m[1]);ordered=tuple(int(m[i],16) for i in (2,3,4));models=tuple(sorted(ordered))
            key=(core,models,int(m[5]),m[6],int(m[7],16));groups[key].append(ordered);raw+=1
    print('core\tmodel_a\tmodel_b\tmodel_c\tedge_bits\tcolor\told_pair_mask\told_pair_vertices\tlabeled_permutations')
    for (core,models,bits,color,old),orders in sorted(groups.items()):
        expected=set(itertools.permutations(models))
        if set(orders)!=expected or len(orders)!=len(expected):raise RuntimeError(f'incomplete/duplicate permutation orbit at core {core}')
        vertices=','.join(str(v) for v in range(40) if old&(1<<v))
        print(f'{core}\t{models[0]:010x}\t{models[1]:010x}\t{models[2]:010x}\t{bits}\t{color}\t{old:010x}\t{vertices}\t{len(orders)}')
    if raw!=sum(len(v) for v in groups.values()):raise AssertionError


if __name__=='__main__':main()
