"""Definition-level checks using unordered sums, including repeated summands."""
import argparse
import itertools
import json
import time
from pathlib import Path

def is_sidon(a):
    sums = [x + y for x, y in itertools.combinations_with_replacement(a, 2)]
    return len(sums) == len(set(sums))

def endpoint_reference(n, k):
    """Fixed endpoints, increasing interiors; no Golomb-length input or differences."""
    a = [0, n-1]
    answers = []
    def visit(start, remain, sums):
        if remain == 0:
            answers.append(tuple(sorted(a)))
            return
        for x in range(start, n-remain):
            fresh = {x+y for y in a} | {2*x}
            if len(fresh) != len(a)+1 or fresh & sums:
                continue
            a.append(x)
            visit(x+1, remain-1, sums | fresh)
            a.pop()
    visit(1, k-2, {0, n-1, 2*(n-1)})
    return sorted(answers)

def load(path, n, k, endpoints=False):
    rows=[]
    for line in Path(path).read_text().splitlines():
        a=tuple(map(int,line.split()))
        assert len(a)==k and tuple(sorted(set(a)))==a, ('bad row',a)
        assert 0<=a[0]<=a[-1]<n and is_sidon(a), ('invalid set',a)
        assert not endpoints or (a[0]==0 and a[-1]==n-1)
        rows.append(a)
    assert len(rows)==len(set(rows)), 'duplicate rows'
    return sorted(rows)

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('n',type=int);p.add_argument('k',type=int);p.add_argument('file');p.add_argument('--endpoints',action='store_true');p.add_argument('--reference',action='store_true');args=p.parse_args()
    started=time.monotonic(); rows=load(args.file,args.n,args.k,args.endpoints)
    if args.reference:
        assert args.endpoints
        expected=endpoint_reference(args.n,args.k)
        assert rows==expected, {'actual':len(rows),'expected':len(expected),'missing':sorted(set(expected)-set(rows))[:5],'extra':sorted(set(rows)-set(expected))[:5]}
    assert sorted(tuple(args.n-1-x for x in reversed(a)) for a in rows)==rows, 'reflection not closed'
    print(json.dumps({'n':args.n,'k':args.k,'sets':len(rows),'valid':True,'reference_equal':args.reference,'reflection_closed':True,'seconds':time.monotonic()-started}))
