"""Independent product-coefficient completeness checker for row transcripts."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from model import canon, graph, require
from primary import domains

def coefficient_count(costs, size, cap):
    # Coefficients of product_q (1 + z*x**cost(q)); no row recursion.
    dp = [[0]*(cap+1) for _ in range(size+1)]
    dp[0][0] = 1
    for w in costs:
        if w > cap:
            continue
        for k in range(size, 0, -1):
            for b in range(cap, w-1, -1):
                dp[k][b] += dp[k-1][b-w]
    return sum(dp[size])

def alternate_graph():
    # Euler characters and multiplied neighborhoods, instead of squares and
    # Euclidean literal ratios in the primary graph.
    S = tuple(q for q in range(1,617) if pow(q,308,617) == 1)
    T = tuple(q for q in range(1,617) if pow(q,308,617) == 616)
    support = set()
    for d in range(1,617):
        row = [(1+j*d)%617 for j in range(1,7)]
        if all(pow(q,308,617) == 616 for q in row):
            support.update(row)
    D = support | {pow(q,615,617) for q in support}
    rows = tuple(sum(1 << T.index(t) for t in {s*d%617 for d in D}) for s in S)
    require((S,T,rows) == graph()[:3], "whole alternate field graph")
    return rows

def check(which, first, last, stream):
    S,T,_,_,cores = domains()
    rows = alternate_graph()
    columns = tuple(sum(1 << i for i,r in enumerate(rows) if r >> j & 1)
                    for j in range(308))
    a,b,cap = (11,11,11) if which == "balanced" else (10,12,12)
    domain = [c for c in cores if len(c[2]) >= b-(5*cap//a)
              and b-len(c[2])+sum(w for w,q in c[3][:a-5]) <= cap]
    require(0 <= first <= last <= len(domain), "range")
    expected = {}
    for i in range(first,last):
        A0,C,B0,costs = domain[i]
        mask = sum(1 << j for j in B0)
        weights = [(mask & ~row).bit_count() for q,row in enumerate(rows) if q not in A0]
        require(sorted(weights) == [w for w,q in costs], "all303 costs")
        expected[(A0,B0)] = coefficient_count(weights,a-5,cap-(b-len(B0)))
    seen = set()
    counts = Counter()
    histogram = Counter()
    h = hashlib.sha256()
    for line in stream.read_text().splitlines(keepends=True):
        record = json.loads(line)
        require(isinstance(record,list) and len(record)==6, "record schema")
        A0,B0,added,g,best,missing = record
        A0,B0,added = tuple(A0),tuple(B0),tuple(added)
        require((A0,B0) in expected, "unexpected core")
        require(A0==tuple(sorted(set(A0))) and len(A0)==5 and A0[0]==0,
                "five literal rows")
        require(B0==tuple(sorted(set(B0))), "literal columns")
        require(added==tuple(sorted(set(added))) and len(added)==a-5
                and not set(A0)&set(added), "distinct added rows")
        require(all(type(q) is int and 0<=q<308 for q in A0+B0+added), "index range")
        C = (1<<308)-1
        for q in A0:
            C &= rows[q]
        require(all(C >> j & 1 for j in B0), "core columns")
        maskB = sum(1<<j for j in B0)
        actual_g = sum((maskB & ~rows[q]).bit_count() for q in added)
        require(g==actual_g and g<=cap-(b-len(B0)), "core cost/budget")
        A = tuple(sorted(A0+added))
        ma = sum(1<<q for q in A)
        actual_best = sorted([a-(ma & col).bit_count(),j]
                             for j,col in enumerate(columns) if not C>>j&1)[:b-len(B0)]
        require(best==actual_best, "whole best columns outside FULL C")
        require(missing==actual_g+sum(w for w,j in actual_best), "literal missing count")
        require(line==canon(record), "canonical whole record")
        key = (A0,B0,added)
        require(key not in seen, "duplicate selection")
        seen.add(key)
        counts[(A0,B0)]+=1
        histogram[missing]+=1
        h.update(line.encode())
    require(all(counts[key]==count for key,count in expected.items()),
            "product coefficient incomplete enumeration")
    return dict(which=which, range=[first,last], cores=len(expected),
                count=len(seen), histogram=sorted(histogram.items()),
                stream_sha256=h.hexdigest(), all303_weight_coefficients=True,
                alternate_graph_equal=True)

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--which",choices=("balanced","stronger"),required=True)
    ap.add_argument("--start",type=int,required=True)
    ap.add_argument("--stop",type=int,required=True)
    ap.add_argument("--stream",type=Path,required=True)
    x=ap.parse_args()
    print(canon(check(x.which,x.start,x.stop,x.stream)),end="")
