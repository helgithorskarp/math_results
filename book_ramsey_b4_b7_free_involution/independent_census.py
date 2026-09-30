"""Separate set-based census of all six-uniform-pair quotient patterns.
Author: six-books-2, role researcher. No generator code is imported.
All possible matching signs are relaxed independently at each spine.
Thus surviving patterns are necessary data, never asserted valid hosts.
"""
from itertools import combinations,product
from pathlib import Path
import argparse,json,time

Q=11;VERTICES=frozenset(range(Q));PAIRS=list(combinations(range(Q),2))
FORMS=[('one',[(0,1)]),('two_adjacent',[(0,1),(0,2)]),('two_disjoint',[(0,1),(2,3)]),('3k2',[(0,1),(2,3),(4,5)]),('p3k2',[(0,1),(1,2),(3,4)]),('p4',[(0,1),(1,2),(2,3)]),('star',[(0,1),(0,2),(0,3)]),('triangle',[(0,1),(0,2),(1,2)])]

def check(ok,message):
    if not ok:raise RuntimeError(message)

# Literal third-orbit page sets determine each relaxed matching cost.
for ri,rj in product(range(3),repeat=2):
    candidates=[]
    for ni in ([frozenset()],[frozenset([0]),frozenset([1])],[frozenset([0,1])])[ri]:
        for nj in ([frozenset()],[frozenset([0]),frozenset([1])],[frozenset([0,1])])[rj]:
            red_pages=len(ni&nj)
            j1_red=frozenset(1-v for v in nj) if rj==1 else nj
            blue_pages=len((frozenset([0,1])-ni)&(frozenset([0,1])-j1_red))
            candidates.append((red_pages,blue_pages))
    expected={(1,0),(0,1)} if ri==rj==1 else {(ri*rj//2,(2-ri)*(2-rj)//2)}
    check(set(candidates)==expected,'literal third-orbit cost table')

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--reference",type=Path,required=True,help="scratch survivor list from census.cpp")
args=parser.parse_args()
start=time.monotonic();cases=[];survivors=[]
for name,edges in FORMS:
    er=frozenset(edges);r=[frozenset(j for a,j in edges if a==i)|frozenset(a for a,j in edges if j==i) for i in range(Q)]
    possible=[p for p in PAIRS if p not in er]
    c={'red_form':name,'all_patterns':0,'three_blue_neighbors_pass':0,'matching_budget_pass':0,'color_pattern_survivors':0,'flag_survivors':0}
    for eb in combinations(possible,6-len(edges)):
        c['all_patterns']+=1;b=[set() for _ in range(Q)]
        for i,j in eb:b[i].add(j);b[j].add(i)
        if any(len(b[i]|b[j])<3 for i,j in edges):continue
        c['three_blue_neighbors_pass']+=1
        m=[VERTICES-{i}-r[i]-b[i] for i in range(Q)]
        okay=True
        for i,j in PAIRS:
            if j not in m[i]:continue
            forced_red=2*len(r[i]&r[j])+len(r[i]&m[j])+len(m[i]&r[j])
            forced_blue=2*len(b[i]&b[j])+len(b[i]&m[j])+len(m[i]&b[j])
            free=len(m[i]&m[j])
            if max(0,forced_blue+free-6)>min(free,3-forced_red):okay=False;break
        if not okay:continue
        c['matching_budget_pass']+=1
        active=sorted({v for e in edges+list(eb) for v in e});inactive=sorted(VERTICES-set(active))
        row_degrees=[[2 if k in r[i] else 0 if k in b[i] else 1 for k in range(Q)] for i in range(Q)]
        budgets=[(i,j,0,sum(row_degrees[i][k]*row_degrees[j][k] for k in VERTICES-{i,j})) for i,j in edges]
        budgets += [(i,j,1,sum((2-row_degrees[i][k])*(2-row_degrees[j][k]) for k in VERTICES-{i,j})) for i,j in eb]
        valid=[]
        for values in product([0,1],repeat=len(active)):
            epsilon=dict(zip(active,values))
            if any((epsilon[i] and 2*len(r[i])>3) or (not epsilon[i] and 2*len(b[i])>6) for i in active):continue
            if any(outside+2*(epsilon[i]+epsilon[j] if color==0 else 2-epsilon[i]-epsilon[j])>[6,12][color] for i,j,color,outside in budgets):continue
            mask=sum(value<<i for i,value in epsilon.items())
            for extras in product([0,1],repeat=len(inactive)):valid.append(mask+sum(value<<i for i,value in zip(inactive,extras)))
        if valid:
            c['color_pattern_survivors']+=1;c['flag_survivors']+=len(valid)
            word=sum(1<<PAIRS.index(p) for p in eb)
            survivors.append({'red_form':name,'blue_mask':word,'flags':sorted(valid)})
    cases.append(c);print(json.dumps(c),flush=True)
reference=[json.loads(line) for line in args.reference.read_text().splitlines()]
check(sorted(survivors,key=lambda x:(x['red_form'],x['blue_mask']))==sorted(reference,key=lambda x:(x['red_form'],x['blue_mask'])),'complete survivor/flag lists differ')
expected=json.loads(Path(__file__).with_name('expected.json').read_text())['census_cases']
for c,e in zip(cases,expected):
    check(c['red_form']==e['red_form'],'form order')
    for key in ['all_patterns','three_blue_neighbors_pass','matching_budget_pass','color_pattern_survivors','flag_survivors']:check(c[key]==e[key],'census count mismatch')
# Explicitly reconstruct all expected normal forms and their allowed flags.
predicted=[]
for k,l in combinations(range(3,Q),2):
    eb=sorted([(0,k),(0,l),(1,2),(k,l)])
    active={0,1,2,k,l};flags=[f for f in range(1<<Q) if all((f>>i&1)==int(i in [k,l]) for i in active)]
    predicted.append({'red_form':'two_adjacent','blue_mask':sum(1<<PAIRS.index(p) for p in eb),'flags':flags})
for k in range(4,Q):
    for ac,bd in [((0,2),(1,3)),((0,3),(1,2))]:
        for a in [0,1]:
            other=bd[1] if ac[0]==a else ac[1]
            eb=sorted([ac,bd,tuple(sorted((a,k))),tuple(sorted((other,k)))])
            active={0,1,2,3,k};flags=[f for f in range(1<<Q) if all((f>>i&1)==int(i==k) for i in active)]
            predicted.append({'red_form':'two_disjoint','blue_mask':sum(1<<PAIRS.index(p) for p in eb),'flags':flags})
check(sorted(predicted,key=lambda x:(x['red_form'],x['blue_mask']))==sorted(survivors,key=lambda x:(x['red_form'],x['blue_mask'])),'analytic two-shape coverage mismatch')
result={'agent':'six-books-2','role':'researcher','complete':True,'cases':cases,'all_patterns':sum(c['all_patterns'] for c in cases),'matching_budget_pass':sum(c['matching_budget_pass'] for c in cases),'color_pattern_survivors':len(survivors),'flag_survivors':sum(c['flag_survivors'] for c in cases),'analytic_shapes':2,'full_survivor_flag_sets_match':True,'wall_seconds':time.monotonic()-start,'full_signing_enumeration':False}
print(json.dumps(result))
