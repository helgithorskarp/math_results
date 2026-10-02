"""Exact corroboration of an independently reconstructed ordinary proof.

The defining graph proof was visible. Target executable/certificate unread
at initial source seal. Explicit exceptions remain live under python -O.
"""
import argparse,hashlib,itertools,json,time
from pathlib import Path
from model import *

def labels(r): return ''.join(map(str,sorted(r)))

def build():
    started=time.monotonic()
    cv=covers(); need(len(cv)==25,'cover count')
    missing=[r for r in subsets(range(6)) if all(not {i,j}<=r for i,j in TIGHT)]
    need({Q-r for r in cv}==set(missing),'cover/complement bijection')
    own=((3,5),(2,4))
    initial=[r for r in cv if all(len(r & set(p))<=1 for p in own)]
    final=[r for r in initial if all(not {i,j}<=r for i,j in TIGHT)]
    need(set(final)=={frozenset((0,1)),frozenset((0,2,3)),frozenset((1,4,5))},'T2 classification')
    budget=[]
    for row in initial:
        if row in final: continue
        edge=next(e for e in TIGHT if set(e)<=row)
        for s0 in cv:
            counts=[]
            for i in edge:
                counts.append(int(i in (2,3,4,5))+int(i in s0)+
                              sum(j in row for a,j in CYCLE if a==i)+
                              sum(a in row for a,j in CYCLE if j==i))
            need(sum(counts)>=4 and sum(3-c for c in counts)<3,'joint union budget')
            budget.append([labels(row),labels(s0),list(edge),counts])
    decks=([frozenset(z) for z in ((0,1),(0,1,4),(0,1,5),(0,1,4,5),(1,4,5))],
           [r for r in cv if {2,3}<=r and 1 not in r],
           [r for r in cv if {1,3}<=r and 2 not in r],
           [r for r in cv if {1,2}<=r and 3 not in r])
    need(all(len(d)==5 for d in decks),'five cover decks')
    scalar=[];physical=[];trans=[];arithmetic=[]
    for s0,s1,t0,t1 in itertools.product(*decks):
        rows=dict(zip(SY+T,(s0,s1,t0,t1,frozenset((0,2,3)))))
        for r in (0,1):
            g,rank,degree=frame(rows,r)
            for which in (0,1):
                dst,rr,perm=transport(rows,r,which)
                gg,rk,dd=frame(dst,rr)
                need(all({perm[b] for b in g[a]}==gg[perm[a]] and
                         rank[a]==rk[perm[a]] and degree[a]==dd[perm[a]] for a in OLD),'literal transport')
                trans.append([r,which,[labels(z) for z in (s0,s1,t0,t1)]])
        g,rank,degree=frame(rows)
        need(sum(degree[z] for z in (V,A)+X+SX)==99,'marked degree sum')
        need(sum(len(g[z]&set((V,A)+X+SX)) for z in (V,A)+X+SX)==26,'root edge count')
        need(rank[SY[0]]==rank[SY[1]]==2,'SY rank')
        # Equations (5),(6) and T cover; no native table or native predicate.
        cond=(s0 in decks[0][:3] and int(4 in s0)+int(4 in s1)+int(4 in t1)>=2 and
              int(5 in s0)+int(5 in s1)+int(5 in t0)>=2 and
              len(s1&t0)<=2 and len(s1&t1)<=2 and len(s0&t1)<=2 and
              {0,4,5}<=t0|t1)
        if cond:
            rec=[labels(z) for z in (s0,s1,t0,t1)]
            scalar.append(rec)
            # Record defining spine counts independently, for the union cut.
            c25=len(g[X[2]]&g[X[5]])
            c15=len(g[X[1]]&g[X[5]])
            arithmetic.append([rec,rank[X[5]],c25,c15,bounds(g,rank,degree,X[2],X[5])[1],bounds(g,rank,degree,X[1],X[5])[1]])
            if rank[X[5]]>bounds(g,rank,degree,X[2],X[5])[1]+bounds(g,rank,degree,X[1],X[5])[1]:
                continue
            physical.append(rec)
    need(len(scalar)==3 and len(physical)==2,'three then two shapes')
    scans=[]
    for rec in physical:
        rows=dict(zip(SY+T,[frozenset(map(int,z)) for z in rec]+[frozenset((0,2,3))]))
        g,rank,degree=frame(rows)
        fixed={U:frozenset(),V:Q,A:frozenset(),X[1]:frozenset((0,1,4,5)),
               X[2]:frozenset((0,2,3)),X[3]:frozenset((1,2,3)),
               SX[0]:frozenset((0,3,4,5)),SX[1]:frozenset((1,3,4,5)),T[2]:frozenset((0,1,2))}
        # Enumerate X4 and SY1 from literal pair spines, rather than importing
        # their final forced values. SY0 remains free in the necessary scan.
        variables=(X[4],SY[1],SY[0],T[0],T[1],X[0],X[5])
        trace=hashlib.sha256();counts=[0]*len(variables);leaves=[];rejections={};full_prefixes=[]
        def visit(k,assigned):
            need(time.monotonic()-started<45,'fixed 45-second phase guard; incomplete')
            if k==len(variables):
                full_prefixes.append({'Q_rows':{z:sorted(assigned[z]) for z in OLD},
                                      'point_failures':{str(q):point_failure(g,rank,assigned,q) for q in Q}})
                if all(point_ok(g,rank,assigned,q) for q in Q):
                    leaves.append({z:sorted(assigned[z]) for z in OLD})
                return
            a=variables[k]
            for qa in subsets(Q,rank[a]):
                witness=next((b for b,qb in assigned.items() if not row_pair_ok(g,rank,degree,a,qa,b,qb)),None)
                trace.update(canonical([k,sorted(qa),witness]).encode())
                if witness is not None:
                    rejections[a+':'+witness]=rejections.get(a+':'+witness,0)+1
                    continue
                counts[k]+=1;assigned[a]=qa;visit(k+1,assigned);del assigned[a]
        need(all(row_pair_ok(g,rank,degree,a,fixed[a],b,fixed[b]) for a,b in itertools.combinations(fixed,2)), 'forced prefix internally consistent')
        visit(0,dict(fixed))
        need(not leaves,'terminal necessary scan not empty')
        scans.append({'endpoint_rows':rec,'degree_SY0':degree[SY[0]],'rank_X0_X5':[rank[X[0]],rank[X[5]]],
                      'prefix_counts':counts,'trace_sha256':trace.hexdigest(),'rejections':rejections,'point_survivors':len(leaves)})
        scans[-1]['all_pair_prefixes']=full_prefixes
    # Positive/checkable primitive controls and known row damage.
    rows=dict(zip(SY+T,[frozenset(map(int,z)) for z in physical[0]]+[frozenset((0,2,3))]))
    g,rank,degree=frame(rows)
    need(row_pair_ok(g,rank,degree,X[1],frozenset((0,1,4,5)),X[2],frozenset((0,2,3))),'positive tight union')
    need(not row_pair_ok(g,rank,degree,X[1],frozenset((0,1,4,5)),X[2],frozenset((0,1,2))),'damaged tight union')
    need(all(0<=max(0,a+b-6)<=min(a,b) for a in range(7) for b in range(7)),'subset lower bound')
    # Exact simultaneous budget with overlap, independently checked on every
    # triple of subsets of a four-point universe (4096 triples).
    budget_control=0
    for p,q,z in itertools.product(subsets(range(4)),repeat=3):
        if p|q==frozenset(range(4)):
            need(len(z)==len(z&p)+len(z&q)-len(z&p&q),'overlap identity')
            budget_control+=1
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','schema':1,
            'cover_rows':[labels(r) for r in cv],'missing_rows':[labels(r) for r in missing],
            'initial_T2':[labels(r) for r in initial],'final_T2':[labels(r) for r in final],
            'union_budget_records':budget,'endpoint_decks':[[labels(r) for r in d] for d in decks],
            'scalar_shapes':scalar,'union_cut_arithmetic':arithmetic,'physical_shapes':physical,
            'endpoint_frames':625,'transport_checks':len(trans),'transport_sha256':hashlib.sha256(canonical(trans).encode()).hexdigest(),
            'terminal_scans':scans,'overlap_positive_controls':budget_control,'controls':'PASS'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--check',type=Path)
    args=ap.parse_args();out=canonical(build()).encode()
    if args.check: need(out==args.check.read_bytes(),'entire mathematical record mismatch')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(out)
    print(json.dumps({'status':'PASS','bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},sort_keys=True))
if __name__=='__main__': main()
