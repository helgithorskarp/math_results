"""Low-degree-first neighborhood generation of second-star leaves.

Unlike the target's core/matching/high-attachment generators, this visits
vertices in minimum positive residual degree and chooses their complete
remaining neighborhood. Root branches are all possible edges at a canonical
initial degree-one vertex. Every graph chooses exactly one such branch.
"""
from itertools import combinations, product
import time
from exact import insist, mask, bits, pairs
from first import digest, edge_image, transport

D=tuple(range(1,17))
OLD_PAIRS=frozenset(combinations(D,2))


def baseline(template):
    common=tuple(sorted(tuple(bits(w^1)) for w in template if w&1))
    insist(len(common)==3 and len(set(z for t in common for z in t))==9,'common tails')
    restored=tuple(w|1<<17 for w in template)
    candidates=tuple(mask(q) for q in combinations(D,4)
                     if all(((mask(q)|1)&w).bit_count()<=2 for w in restored))
    return {'triples':common,'candidates':candidates,'common_pairs':frozenset(e for t in common for e in combinations(t,2))}


def degree_graphs(degrees,forbidden):
    # Zero-degree vertices can be discarded; induced support has at most12 points.
    support=tuple(z for z in D if degrees[z])
    eligible={z:frozenset(y for y in support if y!=z and tuple(sorted((z,y))) not in forbidden) for z in support}
    initial=min(support,key=lambda z:(degrees[z],len(eligible[z]),z))
    insist(degrees[initial]==1,'expected initial low point')
    answer=[];total=0;maximum=0;residual={z:degrees[z] for z in support}
    for neighbor in sorted(eligible[initial]):
        started=time.monotonic();nodes=0
        chosen=[tuple(sorted((initial,neighbor)))];residual[initial]=0;residual[neighbor]-=1
        def visit():
            nonlocal nodes
            nodes+=1
            if nodes>200000 or (nodes%1024==0 and time.monotonic()-started>10):
                raise RuntimeError('INCOMPLETE low-degree carrier root guard')
            active=tuple(z for z in support if residual[z])
            if not active:
                answer.append(tuple(sorted(chosen)));return
            candidates={z:tuple(y for y in active if y in eligible[z]) for z in active}
            if any(residual[z]>len(candidates[z]) for z in active):return
            v=min(active,key=lambda z:(residual[z],len(candidates[z]),z))
            degree=residual[v];residual[v]=0
            for ns in combinations(candidates[v],degree):
                if any(residual[z]<1 for z in ns):continue
                for z in ns:residual[z]-=1;chosen.append(tuple(sorted((v,z))))
                visit()
                for z in reversed(ns):residual[z]+=1;chosen.pop()
            residual[v]=degree
        visit();total+=nodes;maximum=max(maximum,nodes)
        residual[initial]=1;residual[neighbor]+=1
    insist(len(set(answer))==len(answer),'degree graph duplicated')
    for g in answer:
        insist(len(g)==9 and all(sum(z in e for e in g)==degrees[z] for z in D) and not set(g)&forbidden,'degree graph literal check')
    return sorted(answer),{'states':total,'max_root_states':maximum}


def mixed_graphs(base,c):
    t=frozenset(z for q in base['triples'] for z in q);c=frozenset(c)
    degrees={z:(4 if z in t else 3) if z in c else int(z in t) for z in D}
    return degree_graphs(degrees,base['common_pairs'])


def double_graphs(base,q,b):
    t=frozenset(z for x in base['triples'] for z in x)
    degrees={z:(7-int(z not in t)) if z==q else (4-int(z not in t)) if z==b else int(z in t) for z in D}
    return degree_graphs(degrees,base['common_pairs'])


def c_orbits(group):
    pending=set(combinations(D,3));records=[]
    while pending:
        rep=min(pending);orbit={tuple(sorted(p[z] for z in rep)) for p in group}
        insist(orbit<=pending,'C orbit overlap/domain');pending-=orbit
        stab=tuple(p for p in group if tuple(sorted(p[z] for z in rep))==rep)
        insist(len(orbit)*len(stab)==len(group),'C orbit-stabilizer')
        records.append((rep,len(orbit),stab))
    return records


def leave_orbits(domain,group):
    pending=set(domain);result=[];weights=0
    for g in domain:
        if g not in pending:continue
        orbit={edge_image(g,p) for p in group}
        insist(orbit<=pending,'leave orbit coverage')
        pending-=orbit;result.append(g);weights+=len(orbit)
    insist(not pending and weights==len(domain),'leave full cover')
    return result


def second(template,base,cover,leave,profile):
    common=tuple(mask((0,17)+t) for t in base['triples'])
    star=tuple(sorted(common+tuple(w|1 for w in cover)))
    first=tuple(w|1<<17 for w in template)
    union=tuple(sorted(set(first+star)))
    insist(len(star)==20 and len(union)==37,'two-star sizes')
    insist(all(w.bit_count()==5 for w in union) and all((a&b).bit_count()<=2 for a,b in combinations(union,2)),'two-star literal compatibility')
    covered=frozenset(e for w in cover for e in pairs(w))
    insist(OLD_PAIRS-covered==set(leave)|base['common_pairs'],'second-star exact leave')
    deficit={z:5-sum(w>>z&1 for w in star) for z in range(1,18)}
    insist(deficit[17]==2 and sorted(v for v in deficit.values() if v)==profile,'second-star row profile')
    return star
