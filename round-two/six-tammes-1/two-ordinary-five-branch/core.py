"""Exact rational fourteen-position core; adapted prior geometry, no old exclusion imported.
Author: six-tammes-1, researcher. CPython >=3.11 standard library.
Adapted from tammes15_adjacent_fives_exclusion/check.py, source
21d7c373cfa2234494841a11642b53baf0380b7b. Old all-four degree and
Cramer/Bezout exclusion code removed; local construction retained.
The original-vertex/contact/face interpretation is in PROOF.md.
"""
from collections import Counter
from itertools import combinations

from fans import need, run, edges_of, boundary_cycle, star_path
from polynomial import T, ONE, bernstein
from rational import Rat

C=Rat(T); U=Rat(ONE); Z=Rat(); REF=2*C/(U+C)
CLASSES=(((8,12),(9,13)),((10,12),(11,13)))

def dot(x,y):
    return (U-C)*sum((a*b for a,b in zip(x,y)),Z)+C*sum(x,Z)*sum(y,Z)

def sign_open(r):
    def sign(p):
        b=bernstein(p)
        if b and all(x>=0 for x in b) and any(x>0 for x in b):return 1
        if b and all(x<=0 for x in b) and any(x<0 for x in b):return -1
        return 0
    return sign(r.n)*sign(r.d)

def generic_coordinates(triangles):
    original=set(edges_of(triangles));edges=set(original)
    active={v for e in edges for v in e};removed=[]
    while len(active)>3:
        nb={v:{w for e in edges if v in e for w in e if w!=v} for v in active}
        ears=sorted(v for v in active if len(nb[v])==2);need(ears,'missing ear')
        new=ears[0];a,b=sorted(nb[new]);old=(nb[a]&nb[b])-{new}
        need(len(old)==1,'unique old third')
        removed.append((new,a,b,next(iter(old))))
        active.remove(new);edges={e for e in edges if new not in e}
    anchors=tuple(sorted(active));need(edges==set(combinations(anchors,2)),'anchor triangle')
    co={v:tuple(U if j==k else Z for k in range(3)) for j,v in enumerate(anchors)}
    for new,a,b,old in reversed(removed):co[new]=tuple(REF*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
    return co

def direct_coordinates():
    co={1:(U,Z,Z),6:(Z,U,Z),7:(Z,Z,U)}
    for new,a,b,old in ((2,1,6,7),(0,1,2,6),(3,0,1,2),(4,0,3,1),(5,0,4,3)):
        co[new]=tuple(REF*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
    return co

def correspondence(row,rep):
    cycle=boundary_cycle(row['faces']);target=boundary_cycle(rep['faces']);n=len(cycle)
    for shift in range(n):
        for sign in (-1,1):
            m={v:target[(shift+sign*k)%n] for k,v in enumerate(cycle)}
            if {tuple(sorted(m[v] for v in t)) for t in row['faces']}==set(map(tuple,rep['faces'])) and {m[0],m[1]}=={0,1}:return m
    raise ValueError('missing full face/F correspondence')

def paired_fan_cover():
    rows=run();need(len(rows)==9,'nine rotations')
    good=[r for r in rows if max(r['triangle_counts'][v] for v in (2,3))<=2]
    need([(r['i'],r['j']) for r in good]==[(1,1),(3,3)],'two five ceiling')
    rep=good[0];target=generic_coordinates(rep['faces'])
    for row in good:
        need(row['canonical_mask']==172253945,'A8 mask')
        m=correspondence(row,rep);co=generic_coordinates(row['faces'])
        need(all(not (dot(co[a],co[b])-dot(target[m[a]],target[m[b]])).n for a,b in combinations(sorted(co),2)),'Gram correspondence')
    direct=direct_coordinates()
    need(all(direct[v]==target[v] for v in direct),'direct/ear coordinate audit')
    return rows,rep

def complete_core(rep):
    triangles=rep['faces'];co=direct_coordinates();qs=[]
    seeds=((0,2,5,8),(1,3,7,9),(2,6,8,10),(3,4,9,11),(4,5,11,12),(6,7,10,13))
    for f,a,b,new in seeds:
        if f in (0,1):
            path=star_path(f,triangles);need({path[0],path[-1]}=={a,b},'sole F Q endpoints')
        den=U+dot(co[a],co[b]);need(sign_open(den)==1,'positive Q denominator')
        q=tuple(2*C/den*(x+y)-z for x,y,z in zip(co[a],co[b],co[f]))
        need(not (dot(q,q)-U).n,'Q unit norm')
        need(not (dot(q,co[a])-C).n and not (dot(q,co[b])-C).n,'Q contact identity')
        co[new]=q;qs.append((f,a,new,b))
    need(all(not (dot(a,a)-U).n for a in co.values()),'all unit identities')
    need(all(sign_open(Rat(x.d)) for a in co.values() for x in a),'core coordinate poles')
    contacts=[];gaps=[];exceptions={p for row in CLASSES for p in row}
    for a,b in combinations(sorted(co),2):
        g=C-dot(co[a],co[b])
        if not g.n:contacts.append((a,b))
        elif (a,b) in exceptions:
            need(sign_open(U-dot(co[a],co[b]))==1,'distinct exceptional positions')
        else:need(sign_open(g)==1,'strict packing gap');gaps.append((a,b))
    prescribed=set(edges_of(triangles))
    for f,a,new,b in qs:prescribed.update((tuple(sorted((f,a))),tuple(sorted((a,new))),tuple(sorted((new,b))),tuple(sorted((b,f)))))
    need(set(contacts)==prescribed and len(contacts)==25 and len(gaps)==62,'core graph/four exceptions')
    for row in CLASSES:
        a,b=row[0];x,y=row[1]
        need(C-dot(co[a],co[b])==C-dot(co[x],co[y]),'paired exceptional gap identity')
    degrees=dict(sorted(Counter(v for e in contacts for v in e).items()))
    need(degrees=={0:5,1:5,2:4,3:4,4:4,5:4,6:4,7:4,8:3,9:3,10:3,11:3,12:2,13:2},'base core degrees')
    return co,contacts,qs,degrees
