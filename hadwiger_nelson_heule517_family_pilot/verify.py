#!/usr/bin/env python3
"""Solver-free exact geometry, positive cuts and residual selection audit.

No producer or earlier field arithmetic is imported. Every positive witness
is checked against the complete graph reconstructed by monomial expansion.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
EXP=[(i&1,(i>>1)&1,(i>>2)&1) for i in range(8)]
INDEX={e:i for i,e in enumerate(EXP)}
PRIMES=(3,5,11)


def require(ok,detail):
    if not ok:raise ValueError(detail)


def multiply(a,b):
    result=[0]*8
    for e,x in zip(EXP,a):
        if not x:continue
        for f,y in zip(EXP,b):
            if not y:continue
            es=tuple(i+j for i,j in zip(e,f));c=x*y
            for p,k in zip(PRIMES,es):c*=p**(k//2)
            result[INDEX[tuple(k%2 for k in es)]]+=c
    return tuple(result)


def distance(a,b):
    d=[tuple(x-y for x,y in zip(a[i],b[i])) for i in (0,1)]
    return tuple(x+y for x,y in zip(multiply(d[0],d[0]),multiply(d[1],d[1])))


def parse(p):
    require(len(p)==2 and all(len(axis)==8 for axis in p),'coordinate shape')
    return tuple(tuple(Fraction(x) for x in axis) for axis in p)


def geometry():
    m=json.loads((HERE/'manifest.json').read_text())
    for name,digest in m['inputs'].items():require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    for name,digest in m['certificates'].items():require(sha256((HERE/name).read_bytes()).hexdigest()==digest,('certificate hash',name))
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    union={int(v):parse(p) for v,p in old['coordinates'].items()};labels=[v for v in range(553) if '510' in old['provenance'][v]]
    H=[union[v] for v in labels];require(len(H)==len(set(H))==510,'base support')
    fresh=json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    seven=[row for row in fresh if row['degree']>=7]
    require([r['centre_index'] for r in seven]==[327,439,671,1040,1074,1377,1383],'complete added stratum')
    points=H+[parse(row['coordinates']) for row in seven]
    require(len(points)==len(set(points))==517,'new graph distinctness')
    integer=[]
    for p in points:
        axes=[]
        for axis in p:
            cs=[96*c for c in axis];require(all(c.denominator==1 for c in cs),'coordinate scale');axes.append(tuple(c.numerator for c in cs))
        integer.append(tuple(axes))
    edges=[(u,v) for u,v in combinations(range(517),2) if distance(integer[u],integer[v])==(96**2,)+(0,)*7]
    require(len(edges)==2555 and sum(v<510 for u,v in edges)==2504 and not any(u>=510 for u,v in edges),'complete unit graph')
    for v,row in enumerate(seven,510):require([u for u in range(510) if (u,v) in edges]==row['neighbors'],'census neighbour labels')
    pool=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    allparts={v:union[v] for v in range(509)}
    allparts.update({509+i:parse([row['x'],row['y']]) for i,row in enumerate(pool)})
    ac=json.loads((REPO/'hadwiger_nelson_parts509_A976_colourability/certificate.json').read_text())
    A1111={allparts[v] for v in ac['vertices']+list(range(374,509))}
    old574=json.loads((REPO/'hadwiger_nelson_parts509_pool_obstruction574/certificate.json').read_text())
    H574={allparts[v] for v in list(range(374))+old574['pool_labels']}
    poolS=json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())
    U677={allparts[v] for v in list(range(374))+poolS['W_S']}
    noncontainment={name:{'missing_count':sum(p not in S for p in points),'first_missing_H517_index':next(v for v,p in enumerate(points) if p not in S)}
                    for name,S in [('U553',set(union.values())),('A1111',A1111),('H574',H574),('U677',U677)]}
    return labels,edges,old,noncontainment


def decode(row,labels,old):
    if row['source']=='native':return row['colouring']
    if row['source']=='forced':
        removed={row['index']};text=old['forced_witness'][str(row['index'])]
    else:
        require(row['source']=='family','source kind');source=old['family'][row['index']];removed=set(source['D']);text=source['witness']
    remaining=sorted(set(range(553))-removed)
    require(len(text)==len(remaining) and set(text)<=set('0123'),'source colouring format')
    colour=dict(zip(remaining,text));require(len(row['extra'])==7,'new colour suffix')
    return ''.join(colour.get(v,'.') for v in labels)+row['extra']


def check(row,labels,edges,old):
    text=decode(row,labels,old);require(len(text)==517 and set(text)<=set('.0123'),'colour domain')
    D=[v for v,c in enumerate(text) if c=='.'];require(D==row['D'],'killing set identity')
    count=0
    for u,v in edges:
        if text[u]!='.' and text[v]!='.':require(text[u]!=text[v],'monochromatic unit edge');count+=1
    return count


def master(rows):
    # Direct closed index formula, independent of the producer dictionary.
    def state(i,j):return 517+sum(min(t,9) for t in range(1,i))+j
    clauses=[]
    for i in range(1,518):
        for j in range(1,min(i,9)+1):
            previous=[state(i-1,j)] if j<i else []
            clauses.append([-state(i,j)]+previous+[i])
            if j>=2:clauses.append([-state(i,j)]+previous+[state(i-1,j-1)])
    clauses.append([state(517,9)])
    clauses += [[-(v+1) for v in row['D']] for row in rows]
    variables=state(517,9)
    raw=(f'p cnf {variables} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    return variables,clauses,raw


def run(work=None):
    start=time.monotonic();labels,edges,old,noncontainment=geometry()
    rows=json.loads((HERE/'certificate.json').read_text())['rows'];native=json.loads((HERE/'native_witnesses.json').read_text())
    require(len(rows)==526 and len(native)==64,'saved row counts')
    edge_checks=sum(check(row,labels,edges,old) for row in rows)
    native_checks=sum(check(row,labels,edges,old) for row in native)
    require(all(1<=len(row['D'])<=9 for row in native),'native positive extensions contain508 vertices')
    require([r['turn'] for r in native]==list(range(64)),'native witness coverage')
    cuts=[frozenset(row['D']) for row in rows]
    require(len(cuts)==len(set(cuts)) and not any(a<b for a in cuts for b in cuts),'minimal cut antichain')
    bad=dict(native[0]);colour=list(bad['colouring']);u,v=next((u,v) for u,v in edges if colour[u]!='.' and colour[v]!='.');colour[v]=colour[u];bad['colouring']=''.join(colour)
    rejected=False
    try:check(bad,labels,edges,old)
    except ValueError as error:require(str(error)=='monochromatic unit edge','wrong rejection');rejected=True
    require(rejected,'invalid colouring accepted')
    residual=json.loads((HERE/'residual_selection.json').read_text());omitted=set(residual['omitted'])
    require(len(omitted)==len(residual['omitted'])==9 and omitted<=set(range(517)),'residual omission domain')
    require(all(not D<=omitted for D in cuts),'residual necessary clauses')
    variables,clauses,raw=master(rows)
    # A direct auxiliary witness uses the actual prefix counts.
    model={v+1:v in omitted for v in range(517)};count=0;index=517
    for i in range(1,518):
        count+=i-1 in omitted
        for j in range(1,min(i,9)+1):index+=1;model[index]=count>=j
    require(index==variables and all(any(model[abs(l)]==(l>0) for l in clause) for clause in clauses),'explicit full residual CNF model')
    if work:
        require(raw==(work/'master_residual.cnf').read_bytes(),'complete master entrywise comparison')
        activation=[[-(2069+v)]+[4*v+c+1 for c in range(4)] for v in range(517)]
        activation += [[-4*u-c-1,-4*v-c-1] for u,v in edges for c in range(4)]
        activation += [[-2069,1]]
        encoded=(f'p cnf 2585 {len(activation)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in activation)).encode()
        require(encoded==(work/'activation.cnf').read_bytes(),'complete native activation comparison')
        inherited=json.loads((work/'inherited.json').read_text());require(len(inherited)==830,'all inherited source rows')
        for row in inherited:check(row,labels,edges,old)
    facts={'status':'POSITIVE HEULE517 CUTS VERIFIED; FULL <=508 FAMILY REMAINS OPEN','vertices':517,'edges':len(edges),'base_to_added_edges':51,'added_edges':0,
           'unordered_pairs_checked':517*516//2,'edge_sha256':sha256(''.join(f'{u},{v}\n' for u,v in edges).encode()).hexdigest(),
           'final_cuts':len(rows),'forced_vertices':sum(len(r['D'])==1 for r in rows),'final_cut_edge_checks':edge_checks,
           'native_positive_witnesses':len(native),'native_witness_edge_checks':native_checks,'improper_witness_rejected':True,
           'residual_selected_vertices':508,'residual_omitted':sorted(omitted),'residual_master_variables':variables,'residual_master_clauses':len(clauses),
           'residual_master_sha256':sha256(raw).hexdigest(),'residual_full_CNF_model_checked':True,
           'noncontainment_in_pinned_coordinates':noncontainment,'family_closed':False,'record_improvement':False,'negative_certificate_used':False,'native_solver_required':False}
    if (HERE/'expected.json').exists():require(facts==json.loads((HERE/'expected.json').read_text()),'expected facts')
    result={'facts':facts,'seconds':time.monotonic()-start,'native_inputs_compared_entrywise':work is not None,'all830_inherited_rows_checked':work is not None}
    print(json.dumps(result,indent=2,sort_keys=True));return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--work',type=Path);ap.add_argument('--report',type=Path);args=ap.parse_args();result=run(args.work)
    if args.report:args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
