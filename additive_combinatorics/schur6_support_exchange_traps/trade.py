"""Independent point trades with explicit colour-transition lists.

For a selected directed colour cycle, a currently coloured point may keep
its colour or take its successor.  At most one point may remain unfilled;
the old hole must be filled.  Other current classes remain fixed.  This
is a constructive neighbourhood, not a complete Schur search.

The star family lets hub classes use every selected colour; other classes
retain their colour or enter a hub.  The fan family adds arbitrary outgoing
choices at colour6 to a directed cycle.  All choices remain per-position.
"""
import argparse
from collections import Counter,defaultdict
from itertools import combinations,permutations
import json
from pathlib import Path
import random
import time

from pysat.card import CardEnc,EncType
from pysat.solvers import Solver


def check(word):
    defects=[(x,y,x+y) for x in range(1,len(word)+1)
             for y in range(x,len(word)-x+1)
             if word[x-1] and word[x-1]==word[y-1]==word[x+y-1]]
    holes=[x for x,c in enumerate(word,1) if c==0]
    return defects,holes


def potential(word):
    bad,holes=check(word);assert not bad and len(holes)==1
    h=holes[0];scores=[0]*6
    for z in range(2,len(word)+1):
        for x in range(1,z//2+1):
            row=set((x,z-x,z))
            if h not in row:continue
            values={word[v-1] for v in row-{h}}
            if len(values)==1:scores[next(iter(values))-1]+=1
    return scores


def model(word,cycle,family='cycle',hubs=(6,)):
    cycle=tuple(cycle);succ=dict(zip(cycle,cycle[1:]+cycle[:1]))
    points=[x for x,c in enumerate(word,1) if c==0 or c in cycle]
    index=set(points);variables={};domains={};top=0
    old_holes=[]
    for x in points:
        old=word[x-1]
        if not old:
            allowed=list(cycle)
        elif family=='star':
            allowed=list(cycle) if old in hubs else sorted({old,*hubs})
        elif family=='fan' and old==6:
            allowed=list(cycle)
        else:
            allowed=sorted({old,succ[old]})
        if old:allowed=[0]+allowed
        else:old_holes.append(x)
        domains[x]=allowed
        for c in allowed:top+=1;variables[x,c]=top
    clauses=[]
    for x in points:
        choices=[variables[x,c] for c in domains[x]]
        clauses.append(choices)
        clauses.extend([-a,-b] for a,b in combinations(choices,2))
    triples=[]
    for x in points:
        for y in points:
            z=x+y
            if y<x or z not in index:continue
            row=sorted(set((x,y,z)));triples.append((x,y,z))
            for c in set.intersection(*(set(domains[v])-{0} for v in row)):
                clauses.append([-variables[v,c] for v in row])
    holes=[variables[x,0] for x in points if 0 in domains[x]]
    cardinality=CardEnc.atmost(holes,bound=1,top_id=top,encoding=EncType.seqcounter)
    clauses.extend(cardinality.clauses)
    return clauses,domains,variables,triples,holes,cardinality.nv


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--out',required=True)
    p.add_argument('--seconds',type=float,default=90)
    p.add_argument('--budget',type=int,default=3000)
    p.add_argument('--steps',type=int,default=30)
    p.add_argument('--seed',type=int,default=171701)
    p.add_argument('--size',type=int,default=4)
    p.add_argument('--family',choices=['cycle','star','fan'],default='cycle')
    p.add_argument('--hubs',type=int,nargs='+',default=[6])
    p.add_argument('--forbid-holes',type=int,nargs='*',default=[])
    p.add_argument('--mobile',action='store_true')
    args=p.parse_args();rng=random.Random(args.seed)
    word=list(map(int,Path(args.input).read_text().strip()))
    assert len(word)==537 and check(word)==([], [word.index(0)+1])
    result={'settings':vars(args),'initial_word':''.join(map(str,word)),
            'initial_scores':potential(word),'queries':[], 'accepted':[],
            'standalone_UNSAT_certificates':False}
    seen={tuple(word)};start=time.monotonic();stop='step_limit'
    best=min(potential(word));bestword=word[:]
    for step in range(args.steps):
        cycles=[(6,)+p for others in combinations(range(1,6),args.size-1)
                for p in ([others] if args.family=='star' else permutations(others))]
        rng.shuffle(cycles);moved=False
        for cycle in cycles:
            if time.monotonic()-start>args.seconds:stop='time_limit';break
            if not set(args.hubs)<=set(cycle):continue
            clauses,domains,var,triples,holes,top=model(word,cycle,args.family,tuple(args.hubs))
            for x in args.forbid_holes:
                if (x,0) in var:clauses.append([-var[x,0]])
            # Forbid previously accepted words only if representable in this domain.
            blocked=0
            fixed=set(range(1,538))-set(domains)
            for previous in seen:
                if all(previous[x-1]==word[x-1] for x in fixed) and all(previous[x-1] in domains[x] for x in domains):
                    clauses.append([-var[x,previous[x-1]] for x in domains]);blocked+=1
            phases=[v if word[x-1]==c else -v for (x,c),v in var.items()]
            tick=time.monotonic()
            with Solver(name='g3',bootstrap_with=clauses) as solver:
                solver.set_phases(phases);solver.conf_budget(args.budget)
                # Full attempts prohibit all holes.  Mobile attempts use <=1.
                answer=solver.solve_limited(assumptions=[] if args.mobile else [-h for h in holes])
                row={'step':step,'cycle':cycle,'points':len(domains),'clauses':len(clauses),
                     'status':{True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
                     'seconds':time.monotonic()-tick,'stats':solver.accum_stats(),
                     'blocked_previous_words':blocked}
                if answer:
                    m=set(solver.get_model());candidate=word[:]
                    for x,ds in domains.items():
                        cs=[c for c in ds if var[x,c] in m];assert len(cs)==1
                        candidate[x-1]=cs[0]
                    defects,hs=check(candidate)
                    assert not defects and len(hs)<=1 and tuple(candidate) not in seen
                    assert all(candidate[x-1] for x,c in enumerate(word,1) if not c)
                    assert all(candidate[x-1]==word[x-1] for x in fixed)
                    row.update(word=''.join(map(str,candidate)),holes=hs,
                               changed=sum(a!=b for a,b in zip(word,candidate)))
                    if not hs:
                        stop='complete_valid_537';Path(args.out+'.full.txt').write_text(row['word']+'\n')
                    else:
                        row['scores']=potential(candidate)
                        if min(row['scores'])<best:
                            best=min(row['scores']);bestword=candidate[:]
                    result['accepted'].append({key:row[key] for key in row if key not in ['stats']})
                    seen.add(tuple(candidate));word=candidate;moved=True
            result['queries'].append({k:v for k,v in row.items() if k!='word'})
            if answer:
                print(json.dumps({k:row[k] for k in ['step','cycle','holes','changed']}|
                                 {'best_score':best}),flush=True)
                break
        if stop in ['time_limit','complete_valid_537']:break
        if not moved:
            stop='no_accepted_cycle_trade';break
    result.update(stop=stop,seconds=time.monotonic()-start,best_score=best,
                  best_word=''.join(map(str,bestword)),last_word=''.join(map(str,word)))
    Path(args.out+'.json').write_text(json.dumps(result,indent=2)+'\n')
    Path(args.out+'.best.txt').write_text(result['best_word']+'\n')
    print(json.dumps({'stop':stop,'seconds':result['seconds'],'accepted':len(result['accepted']),
                      'best_score':best,'statuses':dict(Counter(q['status'] for q in result['queries']))}),flush=True)


if __name__=='__main__':main()
