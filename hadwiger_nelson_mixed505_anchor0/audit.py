#!/usr/bin/env python3
"""Alternative arithmetic, reflection, complete census and coloring replay."""

from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
TRIPLE=HERE.parent/'hadwiger_nelson_nonmono159_moser_triple'
PATH=TRIPLE/'audit.py'
if sha256(PATH.read_bytes()).hexdigest()!='ba06bb3a168fe0fea78d5e0c71341f80cfddbd5af9a6241b5ffaec8bb27ae021':
    raise ValueError('alternative arithmetic dependency mismatch')
spec=importlib.util.spec_from_file_location('triple_arithmetic',PATH)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
R=M.R


def read_points(n):
    hashes={159:'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',
            214:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}
    raw=(HERE.parent/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes()
    if sha256(raw).hexdigest()!=hashes[n]:raise ValueError('coordinate hash mismatch')
    out=[]
    for line in raw.decode().splitlines():
        if not line or line.startswith('#'):continue
        a=tuple(map(int,line.split()))
        if len(a)!=16 or any(a[i] for i in range(16) if i not in (0,5,9,12)):
            raise ValueError('point outside E')
        out.append(((Q(a[0],12),Q(a[5],12)),(Q(a[9],12),Q(a[12],36))))
    if len(out)!=len(set(out)) or len(out)!=n:raise ValueError('wrong input size')
    return out


def construction():
    A=read_points(159)
    t=((Q(5,6),Q(0)),(Q(0),Q(1,18)))
    image=[M.multiply(t,a) for a in A]
    B=list(dict.fromkeys(A+image))
    V=read_points(214);q=V[0]
    if q!=((Q(1),Q(-1,6)),R.ZERO):raise ValueError('wrong chosen anchor')
    H=[(R.add(x,R.scale(q[0],-1)),R.add(y,R.scale(q[1],-1))) for x,y in V]
    labels={h:i for i,h in enumerate(H)}
    reflection=[labels[M.conjugate(h)] for h in H]
    if sorted(reflection)!=list(range(214)) or reflection[0]!=0:
        raise ValueError('bad reflection permutation')
    if any(reflection[reflection[i]]!=i for i in range(214)):
        raise ValueError('reflection is not an involution')
    EB,EH=M.edges(B),M.edges(H)
    if (len(B),len(EB),len(H),len(EH))!=(292,1251,214,977):
        raise ValueError('incorrect component geometry')
    if B[0]!=(R.ZERO,R.ZERO) or H[0]!=(R.ZERO,R.ZERO):raise ValueError('missing origin')
    return B,H,EB,EH,reflection


def main():
    B,H,EB,EH,reflection=construction()
    libB=M.library('colors_B.txt',len(B),EB)
    libH=M.library(HERE/'colors_H.txt',len(H),EH)
    perms=[(0,)+p for p in permutations((1,2,3))]
    normsB=[R.norm(z) for z in B];normsH=[R.norm(z) for z in H]
    classification,partition=sha256(),sha256()
    counts=Counter();groups=defaultdict(list)
    for i,(x,y) in enumerate(B[1:],1):
        for j,(X,Y) in enumerate(H[1:],1):
            S=R.add(R.add(normsB[i],normsH[j]),(-Q(1),Q(0)))
            delta=R.add(R.scale(R.mul(normsB[i],normsH[j]),4),R.scale(R.mul(S,S),-1))
            if not R.nonnegative(delta):case='no_unit_roots'
            elif R.square_root(R.scale(delta,Q(1,3))) is not None:case='roots_in_E'
            else:
                case='outside_E_pairs'
                cr=R.add(R.mul(x,X),R.scale(R.mul(y,Y),3))
                ci=R.add(R.mul(x,Y),R.scale(R.mul(y,X),-1))
                if S!=R.ZERO:key=('middle',R.divide(cr,S),R.divide(ci,S))
                elif cr!=R.ZERO:key=('zero',R.divide(ci,cr))
                else:key=('vertical',)
                groups[key].append((i,j))
            counts[case]+=1
            classification.update(f'0:{i},{j}:{case}\n'.encode())
    for ee in sorted(tuple(sorted(v)) for v in groups.values()):
        partition.update(('0:'+';'.join(f'{i},{j}' for i,j in ee)+'\n').encode())
        if not any(all(cb[i]!=p[ch[j]] for i,j in ee) for cb in libB for ch in libH for p in perms):
            raise ValueError('uncovered independent class')
    result={'B_vertices':len(B),'B_edges':len(EB),'H_vertices':len(H),'H_edges':len(EH),
            'reflection_sha256':sha256(json.dumps(reflection).encode()).hexdigest(),
            'pairs':dict(counts),'quadratic_classes':len(groups),'unit_multipliers':2*len(groups),
            'cross_edge_histogram':dict(sorted(Counter(map(len,groups.values())).items())),
            'classification_sha256':classification.hexdigest(),'edge_partition_sha256':partition.hexdigest(),
            'uncovered_classes':0}
    expected=json.loads((HERE/'expected.json').read_text())
    for key in ('reflection_sha256','classification_sha256','edge_partition_sha256'):
        if result[key]!=expected[key]:raise ValueError(f'entry-level mismatch: {key}')
    result['entry_level_match']=True
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
