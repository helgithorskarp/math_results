"""One bounded joint footprint/outside-edge model over the critical path core."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import time

from encoding import CounterEncoder, add_lex
CELLS=((2,9),(3,4),(4,9),(5,4),(6,4),(7,2))


def need(ok,msg):
    if not ok:raise ValueError(msg)


def fixed_edges():
    core={(0,v) for v in range(1,11)}
    core|={e for bit,e in enumerate(it.combinations(range(3,11),2)) if not(5388912>>bit&1)}
    fixed={e:e in core for e in it.combinations(range(11),2)}
    groups=[];v=11
    for mask,size in CELLS:
        group=list(range(v,v+size));groups.append(group);v+=size
        for w in group:
            for u in range(3):fixed[u,w]=bool(mask>>u&1)
    need(v==43,'outside count')
    return fixed,groups


def build():
    fixed,groups=fixed_edges()
    edges=[e for e in it.combinations(range(43),2) if e not in fixed]
    index={e:i+1 for i,e in enumerate(edges)};clauses=set();census={}
    for k in range(4):
        count=0
        for core in it.combinations(range(11),5-k):
            for outside in it.combinations(range(11,43),k):
                five=core+outside;pairs=list(it.combinations(five,2))
                for color in (False,True):
                    if any(fixed[e]!=color for e in pairs if e in fixed):continue
                    clauses.add(tuple(sorted((-1 if color else 1)*index[e] for e in pairs if e in index)))
                    count+=1
        census[k]=count
    enc=CounterEncoder(len(edges),sorted(clauses,key=lambda row:(len(row),row)))
    base=len(enc.clauses);cardinality=[]
    def interval(vs,lo,hi,label):
        enc.interval(vs,lo,hi);cardinality.append({'label':label,'literals':vs,'lower':lo,'upper':hi})
    for v in range(43):
        debt=(20 if v<3 else 21)-sum(c for e,c in fixed.items() if v in e)
        interval([index[e] for e in edges if v in e],debt,debt,['degree',v])
    degree_end=len(enc.clauses)
    # These are linear because every incidence of the three roots is fixed.
    # The cap-equivalent red ranges are 92..93 at the path centre, 93 at leaves.
    for u in range(3):
        N=[v for v in range(43) if v!=u and fixed[tuple(sorted((u,v)))]]
        const=sum(fixed[e] for e in it.combinations(N,2) if e in fixed)
        free=[index[e] for e in it.combinations(N,2) if e in index]
        interval(free,(92 if u==0 else 93)-const,93-const,['root_red_density',u])
    density_end=len(enc.clauses)
    # Keep the former root-union interface, now on variable footprints. Each
    # predicate is reified exactly, so all rows use the same contact variables.
    U=[[1]*6 for _ in range(6)]
    for a in range(2,6):
        for b in range(2,6):
            x,y=U[a-1][b],U[a][b-1];U[a][b]=x+y-int(x%2==y%2==0)
    cliques={c:[s for k in range(4) for s in it.combinations(range(11),k)
                if all(fixed[e]==c for e in it.combinations(s,2))] for c in (False,True)}
    predicates={};union_rows={};root_rows=0
    for A in cliques[True]:
        for B in cliques[False]:
            if not(A or B) or set(A)&set(B):continue
            root_rows+=1;upper=U[5-len(A)][5-len(B)]-1;terms=[]
            for v in range(43):
                if v in A+B:continue
                signed=[];impossible=False
                for u,c in [(u,True) for u in A]+[(u,False) for u in B]:
                    e=tuple(sorted((u,v)))
                    if e in fixed:
                        if fixed[e]!=c:impossible=True;break
                    else:signed.append(index[e] if c else -index[e])
                if impossible:continue
                term=tuple(sorted(signed))
                if not term:upper-=1
                else:terms.append(term)
            key=tuple(sorted(terms))
            if upper>=len(terms):continue
            if key not in union_rows or upper<union_rows[key][0]:union_rows[key]=(upper,[list(A),list(B)])
    # Canonical terms/rows ensure reproducible identifiers independent of
    # which root description realizes a repeated predicate.
    for term in sorted({t for terms in union_rows for t in terms}):
        if len(term)==1:predicates[term]=term[0]
        else:
            enc.variables+=1;z=enc.variables;predicates[term]=z
            for lit in term:enc.add(-z,lit)
            enc.add(z,*[-lit for lit in term])
    predicate_end=len(enc.clauses)
    for terms,(bound,label) in sorted(union_rows.items()):
        interval([predicates[t] for t in terms],0,bound,['root_union',*label])
    union_end=len(enc.clauses)
    # Identical root-signature cells may be permuted. Sort only their W-contact
    # strings, allowing equal strings and arbitrary shared outside edges.
    for group in groups:
        for u,v in zip(group,group[1:]):
            add_lex(enc,[index[w,u] for w in range(10,2,-1)],
                        [index[w,v] for w in range(10,2,-1)])
    return fixed,edges,enc,{'five_set_clauses_before_dedup':census,'base_clauses':base,
                          'degree_clause_end':degree_end,'density_clause_end':density_end,
                          'root_pairs':root_rows,'nontrivial_merged_root_rows':len(union_rows),
                          'root_predicate_count':len(predicates),'predicate_clause_end':predicate_end,
                          'union_clause_end':union_end,
                          'cardinality':cardinality,'groups':groups}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--seconds',type=int,default=120)
    p.add_argument('--emit-only',action='store_true');a=p.parse_args();need(a.seconds>0,'positive cap')
    a.work.mkdir(exist_ok=False);start=time.monotonic();fixed,edges,enc,meta=build()
    cnf=a.work/'case.cnf'
    with cnf.open('x') as f:
        f.write(f'p cnf {enc.variables} {len(enc.clauses)}\n')
        for row in enc.clauses:f.write(' '.join(map(str,row))+' 0\n')
    (a.work/'interface.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    report={'status':'EMITTED','scope':'variable 32 footprints and shared outside edges; fixed K11/cells/degrees/root density/all 3140 root-union bounds; K5 outside <=3',
            'primary_variables':len(edges),'variables':enc.variables,'clauses':len(enc.clauses),
            'fixed_pairs':len(fixed),'fixed_red':sum(fixed.values()),'solver_cap_seconds':a.seconds,
            'base_clauses':meta['base_clauses'],'formula_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'build_seconds':time.monotonic()-start}
    def save():
        (a.work/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report),flush=True)
    save()
    if a.emit_only:return
    t=time.monotonic();log=a.work/'solver.log';proof=a.work/'proof.drat'
    with log.open('x') as out:
        try:
            code=subprocess.run([str(a.kissat),f'--time={a.seconds}',str(cnf),str(proof)],
                                stdout=out,stderr=subprocess.STDOUT,timeout=a.seconds+30).returncode
        except subprocess.TimeoutExpired:code=None
    report.update(solver_exit=code,solve_seconds=time.monotonic()-t,
                  status={10:'SAT_UNCHECKED',20:'UNSAT_UNCHECKED',0:'UNKNOWN'}.get(code,'ERROR'),
                  solver_sha256=hashlib.sha256(a.kissat.read_bytes()).hexdigest(),
                  max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    if code==10:
        values={}
        for line in log.read_text().splitlines():
            if line.startswith('v '):
                for token in line.split()[1:]:
                    lit=int(token)
                    if lit:
                        need(abs(lit) not in values or values[abs(lit)]==(lit>0),'model consistency')
                        values[abs(lit)]=lit>0
        need(set(values)==set(range(1,enc.variables+1)),'complete model')
        need(all(any(values[abs(l)]==(l>0) for l in row) for row in enc.clauses),'all model clauses')
        red={e for e,c in fixed.items() if c}|{e for e,i in zip(edges,range(1,len(edges)+1)) if values[i]}
        graph=a.work/'graph.json';graph.write_text(json.dumps({'n':43,'red_edges':sorted(red)},indent=2,sort_keys=True)+'\n')
        report.update(status='SAT_MODEL_CHECKED_GRAPH_PENDING_LITERAL_AUDIT',graph_sha256=hashlib.sha256(graph.read_bytes()).hexdigest())
    report['elapsed_seconds']=time.monotonic()-start;save()


if __name__=='__main__':main()
