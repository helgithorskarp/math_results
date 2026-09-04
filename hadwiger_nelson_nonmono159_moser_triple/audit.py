#!/usr/bin/env python3
"""Full arithmetic/certificate replay in the alternative E=R+sqrt(-3)R representation.

Does not import verify.py, census.py, or coloring.py. It reuses the previously
published alternative real-quadratic arithmetic, pinned before import.
"""

from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'hadwiger_nelson_nonmono159_origin_pencil/audit.py'
if sha256(PATH.read_bytes()).hexdigest()!='ffbd972b74933acfb96bea73d47b5a3664bd479f7a2fda85d9a0869f9b6cd7d6':
    raise ValueError('alternative arithmetic hash mismatch')
spec=importlib.util.spec_from_file_location('quadratic_arithmetic',PATH)
R=importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def multiply(z,w):
    x,y=z;X,Y=w
    return R.add(R.mul(x,X),R.scale(R.mul(y,Y),-3)),R.add(R.mul(x,Y),R.mul(y,X))


def conjugate(z):
    return z[0],R.scale(z[1],-1)


def edges(points):
    out=[]
    for i,(x,y) in enumerate(points):
        for j,(X,Y) in enumerate(points[:i]):
            if R.norm((R.add(x,R.scale(X,-1)),R.add(y,R.scale(Y,-1))))==R.ONE:
                out.append((j,i))
    return out


def library(name,nn,ee):
    out=[tuple(map(int,s)) for s in (HERE/name).read_text().splitlines()]
    if not out or any(len(c)!=nn or c[0]!=0 or any(v not in range(4) for v in c)
                      or any(c[i]==c[j] for i,j in ee) for c in out):
        raise ValueError('invalid component library')
    return out


def main():
    raw=(HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv').read_bytes()
    if sha256(raw).hexdigest()!='4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02':
        raise ValueError('coordinate hash mismatch')
    A=[]
    for line in raw.decode().splitlines():
        if not line or line.startswith('#'):continue
        a=tuple(map(int,line.split()))
        if len(a)!=16 or any(a[i] for i in range(16) if i not in (0,5,9,12)):
            raise ValueError('unsupported coordinates')
        A.append(((Q(a[0],12),Q(a[5],12)),(Q(a[9],12),Q(a[12],36))))
    t=((Q(5,6),Q(0)),(Q(0),Q(1,18)))
    if R.norm(t)!=R.ONE:raise ValueError('nonunit multiplier')
    image=[multiply(t,a) for a in A]
    B=list(dict.fromkeys(A+image))
    if (len(A),len(B),len(set(A)&set(image)))!=(159,292,26) or A[0]!=(R.ZERO,R.ZERO):
        raise ValueError('wrong inner geometry')
    EA,EB=edges(A),edges(B)
    if (len(EA),len(EB))!=(646,1251):raise ValueError('wrong strict internal graphs')
    lab={v:i for i,v in enumerate(B)}
    inherited=set(EA)|{tuple(sorted((lab[image[i]],lab[image[j]]))) for i,j in EA}
    if len(set(EB)-inherited)!=18:raise ValueError('wrong new inner edges')
    libA,libB=library('colors_A.txt',len(A),EA),library('colors_B.txt',len(B),EB)
    perms=[(0,)+p for p in permutations((1,2,3))]
    classification,partition=sha256(),sha256()
    summaries=[]
    normsA=[R.norm(z) for z in A];normsB=[R.norm(z) for z in B]
    for reflected in (False,True):
        groups=defaultdict(list);counts=Counter()
        for i,(x,y) in enumerate(B[1:],1):
            for j,(X,Y0) in enumerate(A[1:],1):
                Y=R.scale(Y0,-1) if reflected else Y0
                S=R.add(R.add(normsB[i],normsA[j]),(-Q(1),Q(0)))
                delta=R.add(R.scale(R.mul(normsB[i],normsA[j]),4),R.scale(R.mul(S,S),-1))
                if not R.nonnegative(delta):
                    case='no_unit_roots'
                elif R.square_root(R.scale(delta,Q(1,3))) is not None:
                    case='roots_in_E'
                else:
                    case='outside_E_pairs'
                    cr=R.add(R.mul(x,X),R.scale(R.mul(y,Y),3))
                    ci=R.add(R.mul(x,Y),R.scale(R.mul(y,X),-1))
                    if S!=R.ZERO:key=('middle',R.divide(cr,S),R.divide(ci,S))
                    elif cr!=R.ZERO:key=('zero',R.divide(ci,cr))
                    else:key=('vertical',)
                    groups[key].append((i,j))
                counts[case]+=1
                classification.update(f'{int(reflected)}:{i},{j}:{case}\n'.encode())
        for ee in sorted(tuple(sorted(v)) for v in groups.values()):
            line=f'{int(reflected)}:'+';'.join(f'{i},{j}' for i,j in ee)+'\n'
            partition.update(line.encode())
            if not any(all(cb[i]!=p[ca[j]] for i,j in ee)
                       for cb in libB for ca in libA for p in perms):
                raise ValueError('uncovered independent class')
        summaries.append({'reflected':reflected,'classes':len(groups),'pairs':dict(counts)})
    result={'A_vertices':len(A),'A_edges':len(EA),'B_vertices':len(B),'B_edges':len(EB),
            'families':summaries,'classification_sha256':classification.hexdigest(),
            'edge_partition_sha256':partition.hexdigest(),'uncovered_classes':0}
    expected=json.loads((HERE/'expected.json').read_text())
    for name in ('classification_sha256','edge_partition_sha256'):
        if result[name]!=expected[name]:raise ValueError(f'entry-level mismatch: {name}')
    result['entry_level_match']=True
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
