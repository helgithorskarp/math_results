"""Separate literal-page/set-based audit of the two-red quotient reduction.
Author: six-books-2, role researcher. Imports no researcher program.
The matching relaxation and Boolean flag search assert no valid witness.
"""
import argparse
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import time

Q=11
VERTICES=set(range(Q))
PAIRS=list(combinations(range(Q),2))


def require(ok,message):
    if not ok:raise RuntimeError(message)


# Derive the two-point tables from literal neighbor sets, not degree formulas.
CHOICES=[(frozenset(),),(frozenset([0]),frozenset([1])),(frozenset([0,1]),)]
TWO=frozenset([0,1]);MATCH_COST={};UNIFORM_COST={}
for ti,tj in product(range(3),repeat=2):
    matching=set();uniform=set()
    for ni,nj0 in product(CHOICES[ti],CHOICES[tj]):
        nj1=frozenset(1-v for v in nj0) if tj==1 else nj0
        matching.add((len(ni&nj0),len((TWO-ni)&(TWO-nj1))))
        uniform.add((len(ni&nj0)+len(ni&nj1),
                     len((TWO-ni)&(TWO-nj0))+len((TWO-ni)&(TWO-nj1))))
    require(len(uniform)==1,'uniform literal cost is sign-independent')
    UNIFORM_COST[ti,tj]=next(iter(uniform));MATCH_COST[ti,tj]=matching
    require(matching=={(0,1),(1,0)} if ti==tj==1 else len(matching)==1,
            'matching literal relaxed cost table')


def low_partitions(n,first):
    shapes=[]
    for length in range(n+1):
        for sizes in combinations_with_replacement([1,2,3],length):
            if sum(sizes)==n:shapes.append(sizes)
    shapes.sort(key=lambda sizes:(sizes.count(3),sizes.count(2)))
    for sizes in shapes:
        start=first;blocks=[]
        for size in sizes:
            blocks.append(tuple(range(start,start+size)));start+=size
        yield tuple(sizes.count(i) for i in [1,2,3]),blocks


def neighbors(edges):
    ans=[set() for _ in range(Q)]
    for i,j in edges:ans[i].add(j);ans[j].add(i)
    return ans


def flags_by_constraints(red,blue,types):
    domains=[{0,1} for _ in range(Q)]
    for i in range(Q):
        if 2*len(red[i])>3:domains[i].discard(1)
        if 2*len(blue[i])>6:domains[i].discard(0)
    constraints=[]
    for i,j in PAIRS:
        if j not in red[i] and j not in blue[i]:continue
        color=int(j in blue[i]);outside=sum(UNIFORM_COST[types[i][k],types[j][k]][color] for k in VERTICES-{i,j})
        allowed={(a,b) for a,b in product([0,1],repeat=2)
                 if outside+2*(a+b if color==0 else 2-a-b)<=(6 if color==0 else 12)}
        if not allowed:return []
        constraints.append((i,j,allowed))
    answer=[]

    def visit(ds):
        changed=True
        while changed:
            changed=False
            for i,j,allowed in constraints:
                di={a for a in ds[i] if any((a,b) in allowed for b in ds[j])}
                dj={b for b in ds[j] if any((a,b) in allowed for a in ds[i])}
                if not di or not dj:return
                if di!=ds[i] or dj!=ds[j]:ds[i]=di;ds[j]=dj;changed=True
        if any(not d for d in ds):return
        free=next((i for i in range(Q) if len(ds[i])==2),None)
        if free is None:
            answer.append(sum(next(iter(ds[i]))<<i for i in range(Q)));return
        for bit in [0,1]:
            branch=[d.copy() for d in ds];branch[free]={bit};visit(branch)
    visit(domains)
    return sorted(answer)


def record_key(record):
    return record['form'],tuple(record['low_cliques']),record['blue_mask']


def expected_flags(active,blocks,fixed):
    options=[]
    for block in blocks:
        if all(i in fixed for i in block):options.append([tuple(fixed[i] for i in block)])
        elif len(block)==1:options.append([(0,),(1,)])
        elif len(block)==2:options.append([(0,1),(1,0),(1,1)])
        else:options.append([(1,1,1)])
    flags=[]
    for pieces in product(*options):
        bits=dict(fixed)
        for block,piece in zip(blocks,pieces):bits.update(zip(block,piece))
        require(all(i in bits for i in range(Q)),'predicted complete flag')
        flags.append(sum(bits[i]<<i for i in range(Q)))
    return sorted(flags)


def predicted_records():
    predicted={}
    for form,active in [('adjacent',3),('disjoint',4)]:
        for shape,blocks in low_partitions(Q-active,active):
            low_blue=set(e for block in blocks for e in combinations(block,2))
            if form=='adjacent':
                for block in blocks:
                    if len(block)!=2:continue
                    blue=low_blue|{(1,2)}|{(0,k) for k in block}
                    fixed={0:0,1:0,2:0,**{k:1 for k in block}}
                    mask=sum(1<<PAIRS.index(e) for e in blue)
                    predicted[form,shape,mask]=expected_flags(active,blocks,fixed)
            else:
                cross=set(product(range(2),range(2,4)))
                variants=[]
                for bridges in [{(0,2),(1,3)},{(0,3),(1,2)}]:
                    for nonedge in cross-bridges:variants.append((bridges,nonedge))
                for nonedge in cross:variants.append((cross-{nonedge},nonedge))
                for block in blocks:
                    if len(block)!=1:continue
                    k=block[0]
                    for bridges,(a,d) in variants:
                        blue=low_blue|bridges|{(a,k),(d,k)}
                        fixed={0:0,1:0,2:0,3:0,k:1}
                        mask=sum(1<<PAIRS.index(e) for e in blue)
                        predicted[form,shape,mask]=expected_flags(active,blocks,fixed)
    return predicted


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-records',type=Path,required=True)
    parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();start=time.monotonic();cases=[];survivors={}
    for form,edges,active in [('adjacent',[(0,1),(0,2)],3),('disjoint',[(0,1),(2,3)],4)]:
        red=neighbors(edges);er=set(edges)
        cross=sorted(set(combinations(range(active),2))-er)
        active_options=[{(1,2)}] if active==3 else [set(e for e,bit in zip(cross,bits) if bit) for bits in product([0,1],repeat=4)]
        partitions=list(low_partitions(Q-active,active))
        require(len(partitions)==(10 if active==3 else 8),'complete low partitions')
        for shape,blocks in partitions:
            count={'form':form,'low_cliques':list(shape),'raw_patterns':0,'red_F_pass':0,'matching_budget_pass':0,'color_survivors':0,'inside_flag_survivors':0}
            low_blue=set(e for block in blocks for e in combinations(block,2))
            possible=[()]+[p for block in blocks if len(block)<=2 for n in range(1,len(block)+1) for p in combinations(block,n)]
            for active_blue in active_options:
                for attach in product(possible,repeat=active):
                    count['raw_patterns']+=1
                    eb=low_blue|active_blue|{(i,k) for i,subset in enumerate(attach) for k in subset}
                    blue=neighbors(eb)
                    if any(len(blue[i]|blue[j])<3 for i,j in er):continue
                    count['red_F_pass']+=1
                    types=[[2 if k in red[i] else 0 if k in blue[i] else 1 for k in range(Q)] for i in range(Q)]
                    okay=True
                    for i,j in PAIRS:
                        if (i,j) in er or (i,j) in eb:continue
                        forced_red=forced_blue=free=0
                        for k in VERTICES-{i,j}:
                            costs=MATCH_COST[types[i][k],types[j][k]]
                            if len(costs)==2:free+=1
                            else:
                                a,b=next(iter(costs));forced_red+=a;forced_blue+=b
                        if max(0,forced_blue+free-6)>min(free,3-forced_red):okay=False;break
                    if not okay:continue
                    count['matching_budget_pass']+=1
                    flags=flags_by_constraints(red,blue,types)
                    if not flags:continue
                    count['color_survivors']+=1;count['inside_flag_survivors']+=len(flags)
                    mask=sum(1<<PAIRS.index(e) for e in eb)
                    key=form,shape,mask
                    require(key not in survivors,'duplicate normalized quotient');survivors[key]=flags
            cases.append(count)
            if args.progress:print(json.dumps(count),flush=True)
    reference=json.loads(args.compare_records.read_text())
    ref={record_key(r):r['flags'] for r in reference}
    require(len(ref)==len(reference),'duplicate reference quotient')
    require(survivors==ref,'every survivor and flag entry comparison')
    require(survivors==predicted_records(),'complete analytic A/B/C normal-form and flag prediction')
    expected=json.loads(Path(__file__).with_name('two_red_expected.json').read_text())
    require(cases==expected['cases'],'every independent case diagnostic')
    summary={'agent':'six-books-2','role':'researcher','complete':True,
             'raw_patterns':sum(c['raw_patterns'] for c in cases),
             'color_survivors':len(survivors),'inside_flag_survivors':sum(len(v) for v in survivors.values()),
             'cases':cases,'all_survivor_flag_entries_match':True,'analytic_forms_match':True,
             'literal_page_cost_tables':True,'Boolean_flag_constraint_search':True,
             'full_matching_sign_enumeration':False,'wall_seconds':time.monotonic()-start}
    print(json.dumps(summary))


if __name__=='__main__':main()
