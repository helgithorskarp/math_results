"""Own exact PSD, projection-row and literal page checks for zero attachment."""
from itertools import combinations
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,time
from incidence import canonical,need,image
from domains import cubic10,matrix,gram
from exact import psd,inverse_integer,quadratic


def points(w,n=10):return tuple(i for i in range(n) if w>>i&1)
def mask(xs):return sum(1<<i for i in xs)
def dot(a,u,v):return sum(a[i][j] for i in points(u) for j in points(v))


def row_grams(a):
    inv,d=inverse_integer(a)
    four=tuple(mask(c) for c in combinations(range(10),4) if dot(inv,mask(c),mask(c))==F(20*d,23))
    five=tuple(mask(c) for c in combinations(range(10),5) if dot(inv,mask(c),mask(c))==F(65*d,69))
    compatible=[set() for _ in four];disjoint=[]
    for i,j in combinations(range(len(four)),2):
        if dot(inv,four[i],four[j])==F(-3*d,23):
            compatible[i].add(j);compatible[j].add(i)
            if not four[i]&four[j]:disjoint.append((i,j))
    if not disjoint:
        return [],dict(four_candidates=len(four),disjoint_pairs=0,H_sets=0,low_subsets=0,grams=0,H_states=0)
    highsets=[];states=0;started=time.monotonic()
    def visit(chosen,available,q):
        nonlocal states
        states+=1;need(states<=200000 and time.monotonic()-started<=10,'INCOMPLETE high-row guard')
        if len(chosen)==5:
            if not any(q) and any(not four[i]&four[j] for i,j in combinations(chosen,2)):
                highsets.append(tuple(four[i] for i in chosen))
            return
        if len(available)<5-len(chosen):return
        for i in sorted(available):
            zs=points(four[i])
            if any(q[z]==0 for z in zs):continue
            nq=list(q)
            for z in zs:nq[z]-=1
            visit(chosen+(i,),{j for j in available&compatible[i] if j>i},tuple(nq))
    visit((),set(range(len(four))),(2,)*10)
    found=[];subsets=0
    for hs in highsets:
        eligible=tuple(w for w in five if all(dot(inv,w,h)==F(2*d,23) for h in hs))
        start=time.monotonic();fiber=0
        for low in combinations(eligible,6):
            fiber+=1;need(fiber<=200000 and time.monotonic()-start<=10,'INCOMPLETE low-row guard')
            if any(sum(w>>z&1 for w in low)!=3 for z in range(10)):continue
            rows=tuple(sorted(hs))+tuple(sorted(low))
            actual=[[sum((w>>i&1)*(w>>j&1) for w in rows) for j in range(10)] for i in range(10)]
            if actual==a:found.append(rows)
        subsets+=fiber
    need(len(found)==len(set(found)),'duplicate full binary Gram')
    return found,dict(four_candidates=len(four),disjoint_pairs=len(disjoint),H_sets=len(highsets),low_subsets=subsets,grams=len(found),H_states=states)


def stars(j,rows,exceptional,forced_triangle=True):
    allpoints=set(range(22));N=range(10);V=range(11);A=set(range(5))-set(exceptional)
    red_x=[{21}|{y for y in N if j[x][y]}|{10+v for v in V if rows[v]>>x&1} for x in N]
    need(all(len(r)==9 for r in red_x),'wrong literal degree-nine N star')
    answer=[]
    for a in sorted(A):
        choices=[]
        for tail in combinations([v for v in V if v!=a],4):
            if forced_triangle and not A-{a}<=set(tail):continue
            red_a=set(points(rows[a]))|{10+v for v in tail}
            need(len(red_a)==8,'wrong literal degree-eight A star')
            blue_a=allpoints-{10+a}-red_a
            if all(len(red_a&red_x[x])<=3 if rows[a]>>x&1 else
                   len(blue_a&(allpoints-{x}-red_x[x]))<=6 for x in N):
                choices.append(mask(tail))
        answer.append(tuple(choices))
    return tuple(answer)


def audit():
    graphs,profiles=cubic10();negative=0;positive=Counter();witness_stream=sha256();graph_stream=sha256();ranks=Counter()
    for es in graphs:
        j=matrix(10,es);s=gram(j);graph_stream.update(json.dumps(es,separators=(',',':')).encode()+b'\n')
        ok,rank,q=psd(s)
        if not ok:
            need(quadratic(s,q)<0,'negative witness failed literal quadratic form')
            witness_stream.update(json.dumps([[x.numerator,x.denominator] for x in q],separators=(',',':')).encode()+b'\n')
            negative+=1
        else:
            ranks[rank]+=1
            words=tuple((1<<u)|(1<<v) for u,v in es)
            c=canonical(words,10,(tuple(range(10)),))
            need(image(words,c['to_canonical'])==c['canonical'],'false positive-core relabeling')
            positive[c['canonical']]+=1
    records=[];forced_records=[];unforced_records=[];allgrams=[]
    for key,count in sorted(positive.items()):
        es=tuple(points(w) for w in key);j=matrix(10,es);s=gram(j)
        need(psd(s)[:2]==(True,10),'singular positive type invalidates projection')
        grams,rec=row_grams(s);placements=0
        for rows in grams:
            need(all(sum(w>>z&1 for w in rows)==5 for z in range(10)),'wrong full Gram column sum')
            allgrams.append(dict(edges=es,rows=rows))
            for pair in combinations(range(5),2):
                if rows[pair[0]]&rows[pair[1]]:continue
                permitted=stars(j,rows,pair)
                need(any(not s for s in permitted),'positive exterior A-star completion')
                forced_records.append(tuple(len(s) for s in permitted))
                unforced=stars(j,rows,pair,False)
                need(any(not s for s in unforced),'positive relaxed exterior A-star completion')
                unforced_records.append(tuple(len(s) for s in unforced))
                placements+=1
        records.append(dict(canonical_edges=es,rooted_copies=count,placements=placements,**rec))
    return dict(cubic10_profiles=profiles,cubic10_graphs=len(graphs),negative_exact_congruences=negative,
                positive_rank_counts=dict(ranks),positive_classes=records,
                graph_stream_sha256=graph_stream.hexdigest(),negative_witness_stream_sha256=witness_stream.hexdigest(),
                forced_star_cases=len(forced_records)*3,forced_star_candidates=len(forced_records)*3*28,
                forced_survivor_counts=forced_records,forced_survivor_sha256=sha256(json.dumps(forced_records,separators=(',',':')).encode()).hexdigest(),
                relaxed_star_candidates=len(unforced_records)*3*210,
                relaxed_every_placement_has_empty_A_star=all(any(t==0 for t in rec) for rec in unforced_records),
                relaxed_survivor_counts=unforced_records),allgrams
