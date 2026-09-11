"""Exact critical-event counting by inclusion-exclusion over rows."""
from math import comb

def C(n,k):return comb(n,k) if 0<=k<=n else 0

def count_critical(rows,columns,L):
 sets=[sum(1<<j for j,col in enumerate(columns) if i in col) for i in range(len(rows))]
 N=len(columns)
 for i,(a,f) in enumerate(rows):
  h=a-sets[i].bit_count();assert h>=0
  sets[i]|=((1<<h)-1)<<N;N+=h
 d=len(rows);unions=[0]*(1<<d);sizes=[0]*(1<<d)
 for mask in range(1,1<<d):
  low=mask&-mask;unions[mask]=unions[mask^low]|sets[low.bit_length()-1];sizes[mask]=unions[mask].bit_count()
 left=sum(1<<i for i,(a,f) in enumerate(rows) if f&1)
 right=sum(1<<i for i,(a,f) in enumerate(rows) if f&2)
 total=0;I=left
 while I:
  candidates=sum(1<<j for j in range(d) if right>>j&1 and sets[j]&unions[I]==0)
  J=candidates
  while J:
   sign=-1 if (I.bit_count()+J.bit_count())%2 else 1
   total+=sign*C(N-sizes[I]-sizes[J],L-sizes[I]);J=(J-1)&candidates
  I=(I-1)&left
 return total,N

from itertools import combinations

def incidence_envelope(N, L, rows, edges, weights):
    """Exhaust all clique-column multiplicities with prescribed pair overlaps.

Returns (-1,0,None) when no covering family realizes the input matrix.
    """
    d = len(rows)
    excess = sum(a for a, _ in rows) - N
    index = {p: i for i, p in enumerate(edges)}
    large = []
    for k in range(3, d + 1):
        for us in combinations(range(d), k):
            pairs = list(combinations(us, 2))
            if all(p in index for p in pairs):
                large.append((us, tuple(index[p] for p in pairs)))
    caps = [a for a, _ in rows]
    residual = list(weights)
    columns = []
    best, count, witness = -1, 0, None

    def rec(t):
        nonlocal best, count, witness
        if t == len(large):
            cols, remaining = columns.copy(), caps.copy()
            for (u, v), w in zip(edges, residual):
                remaining[u] -= w
                remaining[v] -= w
                if remaining[u] < 0 or remaining[v] < 0:
                    return
                cols.extend([(u, v)] * w)
            if sum(len(c) - 1 for c in cols) != excess:
                return
            value, n = count_critical(rows, cols, L)
            assert n == N
            count += 1
            if value > best:
                best, witness = value, cols
            return
        us, ix = large[t]
        limit = min([caps[u] for u in us] + [residual[i] for i in ix])
        for c in range(limit + 1):
            for u in us:
                caps[u] -= c
            for i in ix:
                residual[i] -= c
            columns.extend([us] * c)
            rec(t + 1)
            if c:
                del columns[-c:]
            for u in us:
                caps[u] += c
            for i in ix:
                residual[i] += c

    rec(0)
    return best, count, witness
