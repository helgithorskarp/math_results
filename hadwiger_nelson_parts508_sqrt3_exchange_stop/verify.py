#!/usr/bin/env python3
"""Exact fixed distance-class exchange of Parts509; no solver needed."""
from pathlib import Path
from itertools import combinations
from math import gcd
from collections import Counter
import json,hashlib,argparse
HERE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)
PRODUCT=[(i,j,RAD.index(a*b//gcd(a,b)**2),gcd(a,b))
         for i,a in enumerate(RAD) for j,b in enumerate(RAD)]
def need(v,msg):
    if not v: raise ValueError(msg)
def norm(a,b):
    x=[a[i]-b[i] for i in range(8)]
    y=[a[8+i]-b[8+i] for i in range(8)]
    z=[0]*8
    for i,j,k,m in PRODUCT: z[k]+=m*(x[i]*x[j]+y[i]*y[j])
    return tuple(z)
def transform(row):
    out=[0]*16
    # Multiply each coefficient by sqrt(3), and increase denominator 96 to 288.
    for off in (0,8):
        for i,d in enumerate(RAD):
            g=gcd(d,3); k=RAD.index(d*3//(g*g))
            out[off+k]+=g*row[off+i]
    return tuple(out)
def check_word(word,n,edges):
    need(isinstance(word,str) and len(word)==n and set(word)<=set('0123'),'four-word domain')
    need(all(word[a]!=word[b] for a,b in edges),'proper four-word')
def components(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    left=set(range(n));out=[]
    while left:
        v=min(left);left.remove(v);seen={v};stack=[v]
        while stack:
            v=stack.pop()
            for u in adj[v]&left: left.remove(u);seen.add(u);stack.append(u)
        out.append(sorted(seen))
    return out
def run(emit=None):
    manifest=json.loads((HERE/'manifest.json').read_text())
    raw=(HERE.parent/manifest['input']).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==manifest['sha256'],'pinned coordinate input')
    source=[tuple(map(int,s.split())) for s in raw.decode().splitlines() if s and not s.startswith('#')]
    need(len(source)==len(set(source))==509 and all(len(p)==16 for p in source),'509 distinct exact points')
    need(source[0]==(0,)*16,'fixed removed origin')
    unit=[];chord=[]
    for i,j in combinations(range(509),2):
        z=norm(source[i],source[j])
        if z==(96**2,)+(0,)*7:unit.append((i,j))
        if z==(3*96**2,)+(0,)*7:chord.append((i,j))
    need(len(unit)==2442,'complete original unit graph')
    points=[transform(p) for p in source[1:]]
    need(len(points)==len(set(points))==508,'exact cap and no collisions')
    edges=[(i,j) for i,j in combinations(range(508),2)
           if norm(points[i],points[j])==(288**2,)+(0,)*7]
    need(edges==[(i-1,j-1) for i,j in chord if i>0],'distance exchange edge stream agrees')
    need(not set(edges)&{(i-1,j-1) for i,j in unit if i>0},'no retained unit constraint')
    word=json.loads((HERE/'certificate.json').read_text())['four_word'];check_word(word,508,edges)
    comps=components(508,edges)
    h=Counter(map(len,comps));cross=sum(a<373<=b for a,b in edges)
    need(cross==0,'complete distance graph has no old-side cross edge')
    result={'parent_points':509,'parent_unit_edges':len(unit),'parent_sqrt3_pairs':len(chord),
            'removed_origin_sqrt3_degree':sum(0 in e for e in chord),
            'points':508,'complete_unit_edges':len(edges),
            'component_order_histogram':dict(sorted(h.items())),
            'large_side_edges':sum(b<373 for a,b in edges),
            'small_side_edges':sum(a>=373 for a,b in edges),'cross_side_edges':cross,
            'parent_unit_constraints_retained':0,'proper_four_word_checked':True,
            'source_pairs_checked':509*508//2,'physical_pairs_checked':508*507//2,
            'record_candidate':False,'chromatic_lower_bound_claimed':False}
    expected=json.loads((HERE/'expected.json').read_text())
    need(json.loads(json.dumps(result))==expected,'expected exact stopping result')
    # Relevant negative controls: literal colouring certificate and coordinate-map identity.
    rejected=False
    try:check_word('0'*508,508,edges)
    except ValueError:rejected=True
    need(rejected,'constant colour corruption rejected')
    one=(96,)+(0,)*15
    need(norm(transform(one),transform((0,)*16))==(288**2//3,)+(0,)*7,'scale is inverse sqrt3')
    if emit is not None:
        emit.mkdir(parents=True,exist_ok=True)
        (emit/'geometry.json').write_text(json.dumps({'denominator':288,'basis':RAD,'points':points,'edges':edges,'components':comps},separators=(',',':'))+'\n')
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--emit',type=Path);a=ap.parse_args()
    print(json.dumps(run(a.emit),indent=2,sort_keys=True))
