#!/usr/bin/env python3
"""Rebuild the exact support and check the physical four-colour stopping proof."""
import argparse
import hashlib
import json
from itertools import combinations, product
from math import gcd, isqrt, lcm
from pathlib import Path
from fold import build, require, dump_cnf

HERE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)

def product_gcd(a,b):
    r=[0]*8
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            d=gcd(RAD[i],RAD[j])
            k=RAD.index(RAD[i]*RAD[j]//(d*d))
            r[k]+=d*x*y
    return r

def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]

def sign128(a):
    if not any(a):return 0
    s=1<<128;lo=hi=0
    for c,d in zip(a,RAD):
        r=isqrt(d*s*s);u=r if r*r==d*s*s else r+1
        lo+=c*(r if c>=0 else u);hi+=c*(u if c>=0 else r)
    require(lo>0 or hi<0,'independent exact side enclosure')
    return 1 if lo>0 else -1

def run(emit=None):
    cert=json.loads((HERE/'certificate.json').read_text())
    raw=(HERE/'points.tsv').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==cert['source_points_sha256'],'source identity')
    original=[tuple(map(int,line.split())) for line in raw.decode().splitlines()
              if line and not line.startswith('#')]
    g=build(HERE/'points.tsv')
    den=lcm(96,g['denominator'])
    old=[[x*(den//96) for x in row] for row in original]
    new=[[x*(den//g['denominator']) for x in row] for row in g['points']]
    a,b=cert['source_pair'];require([a,b]==[264,438],'frozen pair')
    normal=sub(old[b],old[a]);centre2=add(old[a],old[b])
    for i,p in enumerate(old):
        q=new[g['image_of'][i]]
        offset=sub([2*x for x in p],centre2)
        dot=add(product_gcd(offset[:8],normal[:8]),product_gcd(offset[8:],normal[8:]))
        s=sign128(dot);require(s==g['side'][i],'half-plane classification')
        if s>=0:
            require(q==p,'fixed side is unchanged')
        else:
            delta=sub(q,p)
            cross=sub(product_gcd(delta[:8],normal[8:]),product_gcd(delta[8:],normal[:8]))
            midpoint=sub(add(q,p),centre2)
            ndot=add(product_gcd(midpoint[:8],normal[:8]),product_gcd(midpoint[8:],normal[8:]))
            require(not any(cross) and not any(ndot),'defining reflection identities')
    n=len(new);edges=g['edges'];word=cert['four_word']
    require(len(word)==n and set(word)<=set('0123'),'ordinary four-word domain')
    require(all(word[a]!=word[b] for a,b in edges),'proper word on every physical unit edge')
    m=cert['moser_images'];require(len(m)==len(set(m))==7,'seven distinct core points')
    es={tuple(e) for e in edges}
    me=[(i,j) for i,j in combinations(range(7),2) if tuple(sorted((m[i],m[j]))) in es]
    require(len(me)==11 and not any(all(c[a]!=c[b] for a,b in me)
            for c in product(range(3),repeat=7)),'exhaustive seven-point non-three proof')
    left={g['image_of'][i] for i,s in enumerate(g['side']) if s<0}
    right={g['image_of'][i] for i,s in enumerate(g['side']) if s>0}
    le=[e for e in edges if set(e)<=left];re=[e for e in edges if set(e)<=right]
    other=[e for e in edges if not (set(e)<=left or set(e)<=right)]
    require(len(left&right)==1 and not other,'one-vertex sum, with no private cross edges')
    result=dict(g['facts'],left_image_points=len(left),right_image_points=len(right),
        shared_image=sorted(left&right),left_internal_edges=len(le),right_internal_edges=len(re),
        private_cross_edges=len(other),chromatic_number=4,proper_four_word_checked=True,
        moser_non_three_checked=True,record_candidate=False)
    for k in ('inherited_moser_edges','inherited_moser_image_indices'):result.pop(k)
    require(result==json.loads((HERE/'expected.json').read_text()),'frozen output')
    if emit:
        emit.mkdir(parents=True,exist_ok=True)
        (emit/'geometry.json').write_text(json.dumps(g,separators=(',',':'))+'\n')
        dump_cnf(emit/'four.cnf',n,edges)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--emit',type=Path)
    a=ap.parse_args()
    print(json.dumps(run(a.emit),indent=2))
