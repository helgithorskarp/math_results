"""Exact original-label fan rotation cover. Author: six-tammes-1, researcher."""
from collections import Counter
from itertools import combinations, product
import json

def need(condition, message):
    if not condition: raise ValueError(message)

def edges_of(triangles):
    return frozenset(e for t in triangles for e in combinations(sorted(t),2))

def fan(v, neighbors):
    return frozenset(tuple(sorted((v,neighbors[k],neighbors[k+1]))) for k in range(4))

def build(i,j):
    a={i:1,i-1:2,i+1:3}
    b={j:0,j-1:3,j+1:2}
    for k,v in zip((k for k in range(5) if k not in a),(4,5)): a[k]=v
    for k,v in zip((k for k in range(5) if k not in b),(6,7)): b[k]=v
    aa=tuple(a[k] for k in range(5)); bb=tuple(b[k] for k in range(5))
    fa,fb=fan(0,aa),fan(1,bb)
    need(fa&fb=={(0,1,2),(0,1,3)},'shared triangles')
    return aa,bb,fa|fb

def boundary_cycle(triangles):
    counts=Counter(e for t in triangles for e in combinations(sorted(t),2))
    need(all(v in (1,2) for v in counts.values()),'edge incidence')
    bd={e for e,c in counts.items() if c==1}
    vertices=set(v for e in bd for v in e)
    nb={v:sorted(w for e in bd if v in e for w in e if w!=v) for v in vertices}
    need(all(len(q)==2 for q in nb.values()),'boundary degree two')
    s=min(vertices); cycle=[s,nb[s][0]]
    while True:
        q=next(v for v in nb[cycle[-1]] if v!=cycle[-2])
        if q==s: break
        need(q not in cycle,'early boundary repetition')
        cycle.append(q)
    need(set(cycle)==vertices,'connected boundary')
    return tuple(cycle)

def canonical(triangles):
    cycle=boundary_cycle(triangles); n=len(cycle)
    pos={v:k for k,v in enumerate(cycle)}
    ed=edges_of(triangles)
    masks=[]
    pairs=tuple(combinations(range(n),2))
    for s in range(n):
        for sign in (-1,1):
            image={tuple(sorted(((s+sign*pos[v])%n for v in e))) for e in ed}
            masks.append(sum(1<<k for k,e in enumerate(pairs) if e in image))
    return min(masks)

def analyze(triangles):
    ed=edges_of(triangles)
    vs=set(v for t in triangles for v in t)
    tc=Counter(v for t in triangles for v in t)
    deg=Counter(v for e in ed for v in e)
    cycle=boundary_cycle(triangles)
    need(set(cycle)==vs and len(ed)==2*len(vs)-3 and len(triangles)==len(vs)-2,'polygon counts')
    # Independent check: on the actual boundary order no diagonals cross.
    pos={v:i for i,v in enumerate(cycle)}
    pairs=[tuple(sorted((pos[u],pos[v]))) for u,v in ed]
    def crosses(e,f):
        return len(set(e+f))==4 and ((e[0]<f[0]<e[1])!=(e[0]<f[1]<e[1]))
    need(not any(crosses(e,f) for e,f in combinations(pairs,2)),'noncrossing')
    return {'vertices':len(vs),'edges':len(ed),'triangles':len(triangles),'cycle':cycle,
            'triangle_counts':dict(sorted(tc.items())),'degrees':dict(sorted(deg.items())),
            'canonical_mask':canonical(triangles)}

def run():
    rows=[]
    for i,j in product(range(1,4),repeat=2):
        aa,bb,tris=build(i,j)
        rows.append({'i':i,'j':j,'a_link':aa,'b_link':bb,'faces':sorted(tris),**analyze(tris)})
    return rows

def star_path(v,triangles):
    link={tuple(w for w in t if w!=v) for t in triangles if v in t}
    vs=set(w for e in link for w in e)
    nb={w:sorted(z for e in link if w in e for z in e if z!=w) for w in vs}
    ends=sorted(w for w in vs if len(nb[w])==1)
    need(len(ends)==2 and all(len(z) in (1,2) for z in nb.values()),'star link path')
    p=[ends[0]]
    while p[-1]!=ends[1]:
        p.append(next(w for w in nb[p[-1]] if w not in p))
    need(set(p)==vs,'whole star path')
    return tuple(p)

def extend_third_five(triangles,c):
    path=star_path(c,triangles)
    rows=[]
    for offset in range(6-len(path)):
        link={offset+k:v for k,v in enumerate(path)}
        for k,new in zip((k for k in range(5) if k not in link),range(8,10)): link[k]=new
        neighbors=tuple(link[k] for k in range(5))
        full=triangles|fan(c,neighbors)
        stats=analyze(full)
        over=[v for v,tc in stats['triangle_counts'].items() if v not in (0,1,c) and tc>2]
        rows.append({'c':c,'offset':offset,'link':neighbors,'faces':sorted(full),
                     'nonfive_triangle_overflow':over,'survives_triangle_ceiling':not over,**stats})
    return rows

def triple_run():
    rows=[]
    for i,j in product(range(1,4),repeat=2):
        aa,bb,tris=build(i,j)
        counts=Counter(v for t in tris for v in t)
        forced=[v for v in (2,3) if counts[v]>=3]
        if len(forced)==2:
            rows.append({'i':i,'j':j,'status':'two further fives required'}); continue
        if forced:
            cs=forced
        else:
            # A third F adjacent to A or B must occupy a T-T position
            # outside the already shared two neighbor positions.
            cs=[aa[k] for k in range(1,4) if aa[k] not in (1,2,3)]
            cs += [bb[k] for k in range(1,4) if bb[k] not in (0,2,3)]
        for c in cs:
            for extension in extend_third_five(tris,c):
                rows.append({'i':i,'j':j,'third_five_contact_type':'K3' if forced else 'P3',**extension})
    return rows
