#!/usr/bin/env python3
"""Corroborate the ordinary proof with two separate exact small encodings.

The written proof, rather than an enumeration output, is the mathematical
argument. These checks test its correspondence to the literal stated graph.
No earlier candidate generator, finite join census, or solver is imported.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import platform
import resource
import time

import literal
import missing

THREAD_VARIABLES=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                  'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
TARGET=(3,3,2,2,2,2)
TABLE={
    'A0':((0,1),(0,3),(3,5),(0,2,3)),
    'A1U':((0,2),(0,3)),
    'A1V':((0,3),),
    'B':((1,),(0,1),(1,4),(2,4)),
    'C':((0,1),(1,4,5)),
    'D':((0,1),(2,4),(0,2,3)),
}

def require(test,message):
    if not test:
        raise RuntimeError(message)

def canonical(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()

def signature(column):
    return (tuple(column['incidence']),column['internal_degree'],column['actual_degree'])

def role_projection(columns,role):
    s,t=missing.roles[role]
    answer=[]
    for column in columns:
        inc=column['incidence']
        if tuple(inc[8:10])==s and tuple(inc[10:13])==t:
            answer.append((tuple(i for i in range(6) if not inc[i]),tuple(inc[6:8]),
                           column['internal_degree'],column['actual_degree']))
    return sorted(answer)

def formula_projection(table,role):
    s,t=missing.roles[role]
    h=4-sum(s)-sum(t)
    return sorted((tuple(r['M']),tuple(r['SX']),h,11+sum(r['SX'])-len(r['M']))
                  for r in table[role]['records'])

def check_projection(columns,table):
    for role in TABLE:
        actual=role_projection(columns,role)
        require(actual==formula_projection(table,role),
                'whole literal/formula role mismatch: '+role)
        require(sorted({r[0] for r in actual})==sorted(TABLE[role]),
                'written missing-set table mismatch: '+role)

def transport(domains,source,target,permutation):
    source_red,source_degree,source_q=literal.build(*source)
    target_red,target_degree,target_q=literal.build(*target)
    require(sorted(permutation)==list(range(16)) and
            sorted(permutation.values())==list(range(16)), 'not a vertex bijection')
    for i in range(16):
        j=permutation[i]
        require({permutation[k] for k in source_red[i]}==target_red[j],
                'transport fails prescribed adjacency')
        require(source_degree[i]==target_degree[j] and source_q[i]==target_q[j],
                'transport fails actual degrees or Q ranks')
    mapped=[]
    for col in domains[source]['columns']:
        adjacent={permutation[literal.VAR[k]] for k,b in enumerate(col['incidence']) if b}
        mapped.append((tuple(int(i in adjacent) for i in literal.VAR),
                       col['internal_degree'],col['actual_degree']))
    require(sorted(mapped)==sorted(signature(c) for c in domains[target]['columns']),
            'transport fails whole column domain')
    def mapped_rules(rules):
        return sorted((min(permutation[i],permutation[j]),
                       max(permutation[i],permutation[j]),rule) for i,j,rule in rules)
    require(mapped_rules(domains[source]['tight_pair_column_rules'])==
            sorted(tuple(r) for r in domains[target]['tight_pair_column_rules']),
            'transport fails whole tight-pair rules')
    return {'source':list(source),'target':list(target),
            'vertex_permutation':[permutation[i] for i in range(16)],
            'all_prescribed_pairs_degrees_rows_and_columns_match':True}

def integer_cases(table):
    answer={}
    for name,roles in (('U',('A0','A1U','B','B','C','C')),
                       ('V',('A0','A1V','B','B','C','D'))):
        candidates=[sorted({tuple(r['M']) for r in table[role]['records']}) for role in roles]
        checked=0;survivors=[];first_failure=Counter()
        for chosen in product(*candidates):
            checked+=1
            counts=tuple(sum(i in M for M in chosen) for i in range(6))
            if counts==TARGET:
                survivors.append(chosen)
            else:
                first_failure[next(i for i in range(6) if counts[i]!=TARGET[i])]+=1
        require(not survivors,'missing-row integer contradiction failed: '+name)
        answer[name]={'roles':list(roles),'tuples_checked':checked,'survivors':survivors,
                      'first_failed_row_histogram':dict(sorted(first_failure.items()))}
    require(answer['U']['tuples_checked']==512 and answer['V']['tuples_checked']==384,
            'incomplete Cartesian missing-set check')
    return answer

def point(M,p,s,t):
    neighbors={1}|{i+3 for i in range(6) if i not in M}
    neighbors|={9+i for i,b in enumerate(p) if b}
    neighbors|={11+i for i,b in enumerate(s) if b}
    neighbors|={13+i for i,b in enumerate(t) if b}
    h=4-sum(s)-sum(t)
    degree=len(neighbors)+h
    require(degree==11+sum(p)-len(M),'point actual-degree bridge')
    return neighbors,h,degree

def spine(i,M,p,s,t):
    red,degrees,ranks=literal.build(0,False)
    neighbors,h,degree=point(M,p,s,t)
    edge=i in neighbors
    pages=sorted(red[i]&neighbors)
    # A red Qi includes q; a blue Qi lies in the other five Q points.
    lower=max(0,ranks[i]+h-(6 if edge else 5))
    cap=3 if edge else degrees[i]+degree-14
    return {'spine':[i,16],'red_edge':edge,'known_common_red':pages,
            'Q_minimum':lower,'actual_degrees':[degrees[i],degree],
            'red_codegree_cap':cap,'violates':len(pages)+lower>cap}

def known_spines():
    """Verify the written fixed-core page lists without enumerating columns."""
    red,degrees,q=literal.build(0,False)
    # The final column is the exact upper bound on the Q-row intersection.
    expected=(
        (3,7,(0,14),1),(7,6,(0,),2),(6,4,(0,13),1),
        (4,5,(0,14),1),(5,8,(0,),2),(8,3,(0,13),1),
        (9,6,(0,),2),(9,8,(0,),2),(10,5,(0,),2),(10,7,(0,),2),
        (8,13,(3,12),1),
        (12,13,(2,4,8),0),(12,14,(2,4,7),0),(11,14,(2,3,5),0),
        (14,15,(2,3,4,9,11),0),
    )
    records=[]
    for i,j,pages,limit in expected:
        actual=tuple(sorted(red[i]&red[j]))
        edge=j in red[i]
        cap=3 if edge else degrees[i]+degrees[j]-14
        require(actual==pages and cap-len(pages)==limit,
                'ordinary fixed-core spine/page bridge')
        records.append({'spine':[i,j],'red_edge':edge,
                        'known_common_red':pages,'Q_ranks':[q[i],q[j]],
                        'Q_intersection_upper':limit,
                        'Q_intersection_lower':max(0,q[i]+q[j]-6)})
    return {'spines':records,'actual_known_degrees':list(degrees),'Q_ranks':list(q),
            'outside_degrees_derived_from_Bu_four_regularity':True}

def expect_reject(callback,name):
    try:
        callback()
    except RuntimeError:
        return {'control':name,'rejected':True}
    raise RuntimeError('negative control was accepted: '+name)

def controls(domains,table):
    answer=[]
    # This is the discarded prototype mapping: the literal-cycle guard must fail.
    wrong=(2,1,3,4,7,8,6,5,10,9)
    answer.append(expect_reject(lambda:literal.build(0,False,wrong),
                               'wrong old-label/X-cycle map'))
    damaged=deepcopy(table)
    damaged['A1V']['records']=[]
    answer.append(expect_reject(lambda:check_projection(domains[0,False]['columns'],damaged),
                               'missing formula role record'))
    damaged_columns=deepcopy(domains[0,False]['columns'])
    for col in damaged_columns:
        if tuple(col['incidence'][8:])==(1,0,1,0,1):
            col['actual_degree']+=1
            break
    else:
        raise RuntimeError('no A1V literal column for actual-degree control')
    answer.append(expect_reject(lambda:check_projection(damaged_columns,table),
                               'incorrect unrestricted outside actual degree'))
    specimens=(
        ('A0 singleton0',6,{0},(0,0),(1,0),(1,0,0),4,0,3),
        ('A0 singleton3',3,{3},(1,0),(1,0),(1,0,0),4,0,3),
        ('B singleton4',4,{4},(0,1),(0,1),(0,0,1),4,0,3),
        ('C missing P blue SY1',12,{0,2,3},(1,1),(0,0),(1,1,0),6,0,5),
        ('D singleton1 needs internal-Q minimum',7,{1},(0,0),(0,0),(0,1,0),3,1,3),
    )
    for name,i,M,p,s,t,known,lower,cap in specimens:
        record=spine(i,M,p,s,t)
        require(record['violates'] and len(record['known_common_red'])==known and
                record['Q_minimum']==lower and record['red_codegree_cap']==cap,
                'literal page-control mismatch: '+name)
        answer.append({'control':name,'rejected':True,**record})
    wrong_tag=spine(12,{0,2,3},(1,1),(0,0),(1,1,0))
    require(wrong_tag['actual_degrees']==[9,10] and
            len(wrong_tag['known_common_red'])==6 and
            10+10-14==6 and wrong_tag['violates'],
            'derived degree-nine tag must be retained')
    answer.append({'control':'SY1 degree-ten tag would erase the C/P violation',
                   'rejected':True,'derived_SY1_degree':9,'incorrect_tag':10})
    # An allowed D=01 point saturates the relevant bounds; rejecting everything
    # is not a successful checker. Full local acceptance is also checked below.
    neighbors,h,degree=point({0,1},(0,0),(0,0),(0,1,0))
    allowed=(tuple(int(i in neighbors) for i in literal.VAR),h,degree)
    require(allowed in {signature(c) for c in domains[0,False]['columns']},
            'positive D=01 local column rejected')
    require(not spine(7,{0,1},(0,0),(0,0),(0,1,0))['violates'],
            'positive tight red-spine control rejected')
    answer.append({'control':'D=01 necessary local column','accepted':True,
                   'not_a_completed_graph':True})
    return answer

def reproduce():
    for variable in THREAD_VARIABLES:
        require(os.environ.get(variable,'1')=='1',variable+' must be one')
    domains={(r,s):literal.columns(r,s) for r in (0,1) for s in (False,True)}
    require(all(d['count']==43 for d in domains.values()),'literal column count drift')
    table=missing.classify()
    check_projection(domains[0,False]['columns'],table)
    sy={i:i for i in range(16)}
    for a,b in ((3,4),(5,7),(6,8)):
        sy[a],sy[b]=b,a
    rs={i:i for i in range(16)}
    for a,b in ((5,6),(7,8),(9,10)):
        rs[a],rs[b]=b,a
    transports=[transport(domains,(r,False),(r,True),sy) for r in (0,1)]
    transports += [transport(domains,(0,s),(1,s),rs) for s in (False,True)]
    control_records=controls(domains,table)
    integer=integer_cases(table)
    return {
        'schema':'six-books-1 ordinary terminal cross corroboration v1',
        'scope':'only the four specified terminal X16 configurations, E<=108',
        'proof':'PROOF.md ordinary missing-set argument; enumeration is corroboration',
        'outside_global_degree_input':'none',
        'endpoint_cases':['U','V'],'missing_row_target':list(TARGET),
        'literal_masks_examined_per_configuration':8192,
        'literal_domains':[domains[r,s] for r in (0,1) for s in (False,True)],
        'ordinary_fixed_core_spines':known_spines(),
        'formula_role_table':table,
        'whole_literal_formula_role_agreement':True,
        'transports':transports,'integer_checks':integer,
        'controls':control_records,'complete':True,
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--receipt',type=Path)
    parser.add_argument('--check',type=Path,help='require whole-byte match to this mathematical record')
    args=parser.parse_args()
    started=time.monotonic()
    record=reproduce()
    data=canonical(record)
    if args.check:
        require(data==args.check.read_bytes(),'whole mathematical record mismatch')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_bytes(data)
    else:
        print(data.decode(),end='')
    receipt={'mathematical_sha256':hashlib.sha256(data).hexdigest(),
             'mathematical_bytes':len(data),'wall_seconds':time.monotonic()-started,
             'reported_maxrss_KiB_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'python':platform.python_version(),'optimized':not __debug__,
             'thread_variables':{v:os.environ.get(v,'1') for v in THREAD_VARIABLES},
             'complete':True}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_bytes(canonical(receipt))
    if args.output:
        print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':
    main()
