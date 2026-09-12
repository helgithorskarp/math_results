"""Bind all 640 actual local refutations to both exact original q7 strata.

The original source core is color-complemented and identified by a checked
literal isomorphism. A signed bijection pulls every proof-input clause back
to an independently grounded no-blue-augmentation formula on B union C.
This is a conditional branch exclusion, never original-task UNSAT.
"""
from pathlib import Path
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
import argparse,hashlib,importlib.util,json,sys
from common import REPO,LOCAL,need,sha,dependencies

def parse(raw):
    n=raw[0]-63;a=[[0]*n for _ in range(n)]
    for k,(i,j) in enumerate((i,j) for j in range(1,n) for i in range(j)):
        a[i][j]=a[j][i]=(raw[1+k//6]-63)>>(5-k%6)&1
    return a

def source_formula(core):
    fixed={(u,v):0 for u,v in combinations(range(4),2)}
    fixed.update({(4+i,4+j):core[i][j] for i,j in combinations(range(15),2)})
    variables={(u,4+v):1+15*u+v for u in range(4) for v in range(15)}
    def guard(S,color):
        edges=list(combinations(S,2))
        if any(e in fixed and fixed[e]!=color for e in edges):return None
        return frozenset(variables[e] for e in edges if e not in fixed)
    clauses=set();blue4=[]
    for S in combinations(range(19),4):
        red=guard(S,1)
        if red is not None:clauses.add(tuple(sorted(-v for v in red)))
        blue=guard(S,0)
        if blue is not None:blue4.append((sum(1<<v for v in S),blue))
    for S in combinations(range(19),5):
        blue=guard(S,0)
        if blue is not None:clauses.add(tuple(sorted(blue)))
    for (S,a),(T,b) in combinations(blue4,2):
        if not S&T:clauses.add(tuple(sorted(a|b)))
    return sorted(clauses)

def one(job):
    i,raw,j,p,archive,row=job;a=parse(raw);source=source_formula(a)
    cnfpath=Path(archive)/f'core{j:03d}.cnf';proofpath=cnfpath.with_suffix('.drat')
    need(sha(cnfpath)==row['cnf_sha256'] and sha(proofpath)==row['proof_sha256'],'actual input/proof binding')
    def image(lit):
        block,v=divmod(abs(lit)-1,15);return (-1 if lit>0 else 1)*(1+15*block+p[v])
    lines=cnfpath.read_text().splitlines();header=lines[0].split();need(header[:3]==['p','cnf','60'],'local header')
    rows=[list(map(int,x.split())) for x in lines[1:]];need(len(rows)==int(header[3]) and all(x[-1]==0 and all(1<=abs(v)<=60 for v in x[:-1]) for x in rows),'local DIMACS')
    mapped=sorted(set(tuple(sorted(image(v) for v in row[:-1])) for row in rows))
    need(mapped==source,'signed physical pullback differs from literal source branch')
    digest=hashlib.sha256(''.join(' '.join(map(str,c))+' 0\n' for c in source).encode()).hexdigest()
    return {'source_core':i,'certificate_core':j,'certificate_to_source_core':p,'clauses':len(source),
            'source_clause_sha256':digest,'proof_sha256':row['proof_sha256'],
            'original_tasks':[f'bo1-q7-r{r}-c{i:06d}' for r in (5,6)]}

def run(data,archive):
    dependencies();raw=(Path(data)/'r44_15.g6').read_bytes();need(hashlib.sha256(raw).hexdigest()=='53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1','640-core catalog')
    records=raw.splitlines();need(len(records)==640,'core coverage');certs=json.loads((LOCAL/'CERTIFICATES.json').read_text())
    # This search is used only to find bijections. Every returned bijection is
    # checked literally below, so its exhaustiveness is not a proof premise.
    sys.path.insert(0,str(REPO/'ramsey_r55_core_exchange_normal_form'))
    from catalog import isomorphism
    matrices=[parse(x) for x in records];jobs=[]
    for i,a in enumerate(matrices):
        opposite=[[0 if u==v else 1-a[u][v] for v in range(15)] for u in range(15)];found=None
        for j,b in enumerate(matrices):
            if sorted(map(sum,opposite))!=sorted(map(sum,b)):continue
            p=isomorphism(opposite,b)
            if p is not None:found=(j,p);break
        need(found is not None,'color-complement catalog image');j,p=found
        need(sorted(p)==list(range(15)) and all(a[p[u]][p[v]]==1-matrices[j][u][v] for u,v in combinations(range(15),2)),'all 105 signed core edges')
        jobs.append((i,records[i],j,p,str(archive),certs[j]))
    with ProcessPoolExecutor(max_workers=2) as pool:rows=list(pool.map(one,jobs))
    # Physical variable identities of both original h3887 formulas. The core
    # record changes values, not the free-edge numbering.
    fixed={e for b in range(7) for e in combinations(range(4*b,4*b+4),2)}|set(combinations(range(28,43),2))
    variables={e:k+2 for k,e in enumerate(e for e in combinations(range(43),2) if e not in fixed)}
    edge_maps={str(r):[{'local':1+15*u+v,'physical_edge':[4*r+u,28+v],'original_variable':variables[4*r+u,28+v]} for u in range(4) for v in range(15)] for r in (5,6)}
    need([x['source_core'] for x in rows]==list(range(640)),'complete original source cover')
    return {'status':'ALL_1280_ORIGINAL_NO_AUGMENTATION_BRANCH_PULLBACKS_VERIFIED','source_cores':640,'original_task_branches':1280,
            'unique_source_clauses':sum(x['clauses'] for x in rows),'core_edge_equalities':640*105,
            'physical_variable_maps':edge_maps,'rows':rows,'original_task_exclusions':0,
            'branch_condition':'No two disjoint blue K4s in the first blue block plus the original 15-vertex core',
            'trust':'Actual DRAT checks are supplied by local19 audit; this checks its complete signed input bridge.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('archive');s=p.parse_args()
    print(json.dumps(run(s.catalog,s.archive),indent=2,sort_keys=True))
