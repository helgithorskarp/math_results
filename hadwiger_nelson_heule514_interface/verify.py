#!/usr/bin/env python3
"""Exact support, positive witnesses, and complete residual six-omission family."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import comb
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
N=514
SCALE=288

def need(ok,message):
    if not ok:raise ValueError(message)
def load(path):return json.loads(path.read_text())
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def point(raw):
    q=[[Fraction(x)*SCALE for x in a] for a in raw]
    need(len(q)==2 and all(len(a)==8 for a in q) and all(x.denominator==1 for a in q for x in a),'coordinate scale')
    return tuple(tuple(int(x) for x in a) for a in q)
def check(c,D,edges):
    need(len(c)==N and set(c)<=set('.0123'),'colour domain')
    need(D==[i for i,x in enumerate(c) if x=='.'] and D,'exact omissions')
    need(all(c[u]=='.' or c[v]=='.' or c[u]!=c[v] for u,v in edges),'unit edge inequality')
    return sum(c[u]!='.' and c[v]!='.' for u,v in edges)
def minimal(ds):return {d for d in ds if not any(e<d for e in ds)}

def avoiding(vertices,cuts,size):
    """Separate bit-mask backtracking; prune forbidden partial selections."""
    index={v:i for i,v in enumerate(vertices)}
    masks=[sum(1<<index[v] for v in d) for d in cuts]
    def visit(start,chosen,mask):
        if any(mask&d==d for d in masks):return
        if len(chosen)==size:
            yield chosen;return
        for i in range(start,len(vertices)-(size-len(chosen))+1):
            yield from visit(i+1,chosen+(vertices[i],),mask|(1<<i))
    yield from visit(0,(),0)

def controls():
    vertices=(0,1,2);subsets=[frozenset(s) for k in range(4) for s in combinations(vertices,k)];count=0
    for bits in range(256):
        cuts=[d for i,d in enumerate(subsets) if bits&(1<<i)]
        for size in range(4):
            direct=[s for s in combinations(vertices,size) if not any(d<=set(s) for d in cuts)]
            need(list(avoiding(vertices,cuts,size))==direct,'recursive enumeration control');count+=1
    return count

def decode(recipe,source):
    index,tail,fills=recipe
    need(type(index) is int and 0<=index<963 and len(tail)==4 and set(tail)<=set('.0123'),'transport recipe')
    c=list(source[index][:510]+tail);seen=set()
    for v,x in fills:
        need(type(v) is int and 0<=v<510 and v not in seen and c[v]=='.' and x in '0123','restored old vertex')
        c[v]=x;seen.add(v)
    return ''.join(c)

def master_bytes(rows):
    clauses=[];variables=N;prefix={}
    for i in range(1,N+1):
        for j in range(1,min(i,6)+1):
            variables+=1;prefix[i,j]=variables;previous=prefix.get((i-1,j))
            clauses.append([-variables]+([previous] if previous else [])+[i])
            if j>1:clauses.append([-variables]+([previous] if previous else [])+[prefix[i-1,j-1]])
    clauses.append([prefix[N,6]])
    clauses += [[-v-1 for v in sorted(d)] for d in sorted(rows,key=lambda d:(len(d),sorted(d)))]
    return raw(variables,clauses)
def raw(n,clauses):return (f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')

def verify(work=None,out=None):
    start=time.monotonic()
    for name,digest in load(HERE/'manifest.json').items():need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    R=module('reviewed_ring_and_decoder',REPO/'hadwiger_nelson_heule517_whole_decision_review1/independent_check.py')
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels=[v for v in range(553) if '510' in old['provenance'][v]];H=[point(old['coordinates'][str(v)]) for v in labels]
    L={i for i,p in enumerate(H) if all(p[a][k]==0 for a in(0,1) for k in(2,3,6,7))};need(len(H)==510 and len(L)==375,'base blocks')
    pool=load(REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json');need(len(pool)==122,'fixed input frontier')
    unit=(SCALE*SCALE,)+(0,)*7;chosen=[];classification=Counter();mixed_neighbours=[]
    for row in pool:
        q=point(row['coordinates']);neighbours=[i for i,h in enumerate(H) if R.exact_squared_distance(q,h)==unit]
        need(neighbours==row['neighbors'] and len(neighbours)==row['degree']>=4,'exact complete centre neighbours')
        dl=len(set(neighbours)&L);ds=len(neighbours)-dl;classification[dl,ds]+=1
        if dl and ds:chosen.append(row);mixed_neighbours.append(neighbours)
    need([r['centre_index'] for r in chosen]==[170,436,1239,1527],'complete mixed selection')
    points=H+[point(r['coordinates']) for r in chosen]
    need(points[0]==((0,)*8,(0,)*8),'origin label')
    union={point(p) for p in old['coordinates'].values()};need(len(set(points))==N and all(p not in union for p in points[510:]),'distinct new support outside U553')
    # Ambient exclusion comes from the pinned published census. It is not
    # needed to define or prove the finite graph/certificate statement.
    edges=[(u,v) for u,v in combinations(range(N),2) if R.exact_squared_distance(points[u],points[v])==unit]
    cross=[e for e in edges if (e[0] in L)!=(e[1] in L)]
    need(len(edges)==2526 and len(cross)==34,'full graph counts')
    need([e for e in edges if min(e)>=510]==[(510,511),(511,512),(512,513)],'new path')
    need([e for e in cross if max(e)>=510]==[(0,i) for i in range(510,514)],'origin-only new cross edges')
    groups=R.inherited_witnesses(REPO,old,labels,L,set(range(517))-L)
    source=[c for name in ['prior','small','large2','large3','large4'] for row,c in groups[name]]
    source += [r['colouring'] for r in load(REPO/'hadwiger_nelson_heule517_whole_decision/certificate.json')['rows']]
    need(len(source)==963,'source indexing')
    cert=load(HERE/'certificate.json');colours=[decode(r,source) for r in cert['transport']]+[r['colouring'] for r in cert['native']]
    cuts=[frozenset(i for i,x in enumerate(c) if x=='.') for c in colours]
    edge_checks=sum(check(c,sorted(d),edges) for c,d in zip(colours,cuts))
    need(len(colours)==516 and len(cert['transport'])==491 and len(cert['native'])==25,'retained row counts')
    for row in cert['native']:need(row['D']==[i for i,x in enumerate(row['colouring']) if x=='.'],'native exact D')
    need(len(set(cuts))==len(cuts) and minimal(set(cuts))==set(cuts),'full public antichain')
    forced=set().union(*(d for d in cuts if len(d)==1));free=sorted(set(range(N))-forced)
    bad=[d for d in cuts if len(d)>1]
    need(len(forced)==484 and len(forced&L)==358 and len(free)==30 and len(bad)==32,'forced/free partition')
    control_count=controls();other=iter(avoiding(tuple(free),bad,6))
    stream=sha256();residual=0;hist=Counter();examples=[];tested=0;covered=0
    fp=(out/'frontier.txt').open('wb') if out else None;t=time.monotonic()
    try:
        for O in combinations(free,6):
            tested+=1;s=set(O)
            if any(d<=s for d in bad):covered+=1;continue
            need(next(other,None)==O,'entrywise recursive frontier comparison')
            residual+=1;hist[len(s&L)]+=1
            line=(','.join(map(str,O))+'\n').encode('ascii');stream.update(line)
            if fp:fp.write(line)
            if len(examples)<3:examples.append(list(O))
    finally:
        if fp:fp.close()
    need(tested==comb(30,6)==593775 and tested==covered+residual,'complete six-subset census')
    need(next(other,None) is None,'no extra recursive frontier entries')
    census=dict(total_six_sets=tested,covered=covered,residual=residual,residual_by_large_omissions={str(k):v for k,v in sorted(hist.items())},frontier_sha256=stream.hexdigest(),first_residuals=examples)
    expected=HERE/'census.json'
    if expected.exists():need(census==load(expected),'published census')
    census_seconds=time.monotonic()-t;native_checks=initial_checks=0
    if work:
        g=load(work/'graph.json');need([point(p) for p in g['coordinates']]==points and g['edges']==[list(e) for e in edges],'entrywise native graph')
        initial=load(work/'initial_rows.json');need(len(initial)==963,'all transported rows')
        for row in initial:
            c=decode([row['source_index'],row['tail'],row['fills']],source)
            need(c==row['colouring'],'native transported colouring');initial_checks+=check(c,row['D'],edges)
        native=load(work/'native_witnesses.json');native_checks=sum(check(r['colouring'],r['D'],edges) for r in native)
        need(len(native)==64 and all(any(d<=set(r['D']) for d in cuts) for r in initial+native),'all discovered rows subsumed')
        for row in cert['native']:
            n=native[row['native_index']];need(row['D']==n['D'] and row['colouring']==n['colouring'],'retained native provenance')
        result=load(work/'result.json');history=result['history'];need(result['status']=='BOUND_REACHED' and len(history)==len(native)==64,'bounded discovery result')
        current=minimal({frozenset(r['D']) for r in initial})
        for i,(rec,row) in enumerate(zip(history,native)):
            O=set(rec['omitted']);need(len(O)==6 and rec['turn']==i and rec['answer'] is True and all(not d<=O for d in current),'uncovered queried support')
            need(set(row['D'])<=O and row['D']==rec['D'],'checked query extension')
            current=minimal(current|{frozenset(row['D'])});need(rec['cut_count']==len(current),'actual cut count')
        need(current==set(cuts) and all(not d<=set(result['target_omitted']) for d in cuts),'final unresolved selector')
        clauses=[[-2057-v]+[4*v+j+1 for j in range(4)] for v in range(N)]
        clauses += [[-4*u-j-1,-4*v-j-1] for u,v in edges for j in range(4)];clauses.append([-2057,1])
        need((work/'activation.cnf').read_bytes()==raw(2570,clauses),'actual activation CNF')
        need((work/'master.cnf').read_bytes()==master_bytes(set(cuts)),'actual residual omission formula')
    return dict(status='EXACT H514 SUPPORT AND POSITIVE RESIDUAL FAMILY VERIFIED',record_improvement=False,family_closed=(residual==0),
                centre_neighbour_pairs_checked=122*510,graph_pairs_checked=comb(N,2),vertices=N,unit_edges=len(edges),large_vertices=len(L),small_vertices=N-len(L),
                within_large=sum(u in L and v in L for u,v in edges),within_small=sum(u not in L and v not in L for u,v in edges),cross_edges=len(cross),
                selected_centres=[r['centre_index'] for r in chosen],selected_H_neighbours=mixed_neighbours,origin_only_new_cross_edges=True,
                centre_classification=[dict(large=k[0],small=k[1],centres=v) for k,v in sorted(classification.items())],
                public_colourings=516,public_edge_checks=edge_checks,forced_vertices=484,forced_large=358,forced_small=126,
                free_vertices=free,non_singleton_cuts=32,census=census,all_initial_edge_checks=initial_checks,all_native_edge_checks=native_checks,
                actual_native_graph_and_formulas_checked=bool(work),independent_frontier_entrywise_comparison=True,control_rank_families=control_count,
                native_solver_used=False,negative_proof_required=False,census_seconds=census_seconds,seconds=time.monotonic()-start)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path);parser.add_argument('--out',type=Path);parser.add_argument('--report',type=Path);args=parser.parse_args()
    if args.out:args.out.mkdir(exist_ok=False)
    result=verify(args.work,args.out)
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
