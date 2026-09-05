#!/usr/bin/env python3
"""Optional external comparison; this catalog is not an input to the proof."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def inspect(path):
    raw=path.read_bytes();hist=Counter();regular=[]
    for index,line in enumerate(raw.decode('ascii').splitlines()):
        if len(line)!=19 or line[0]!='N':raise ValueError('expected order-15 graph6 record')
        values=[ord(c)-63 for c in line[1:]]
        if not all(0<=v<64 for v in values):raise ValueError('graph6 character')
        bits=[v>>shift&1 for v in values for shift in range(5,-1,-1)]
        if any(bits[105:]):raise ValueError('graph6 padding')
        near=[set() for _ in range(15)]
        for bit,(a,b) in zip(bits,((i,j) for j in range(1,15) for i in range(j))):
            if bit:near[a].add(b);near[b].add(a)
        if any(len({b in near[a] for a,b in combinations(S,2)})==1 for S in combinations(range(15),4)):
            raise ValueError('catalog entry is not Ramsey (4,4)')
        degrees=list(map(len,near));hist[sum(degrees)//2]+=1
        if len(set(degrees))==1:regular.append([index,degrees[0]])
    return {'source':'https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6',
            'sha256':sha256(raw).hexdigest(),'bytes':len(raw),'entries_checked':sum(hist.values()),
            'edge_histogram':[[e,c] for e,c in sorted(hist.items())],'regular_entries':regular,
            'catalog_completeness_needed_for_main_theorem':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('catalog',type=Path);ap.add_argument('--report',type=Path)
    args=ap.parse_args();text=json.dumps(inspect(args.catalog),indent=2,sort_keys=True)+'\n'
    if args.report:args.report.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
