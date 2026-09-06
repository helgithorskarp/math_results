#!/usr/bin/env python3
"""Truth tables, small literal graphs, and deliberate malformed certificates."""
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import json
import audit
import generate as gen


def sat(rows,values):return all(any(values[abs(v)]==(v>0) for v in row) for row in rows)


def logical():
    rows,top=gen.order_rows();need=audit.need;gate_cases=0
    # Extract each actual q definition, excluding q's use by its successor.
    for pair in range(3):
        a,b=gen.columns()[pair:pair+2]
        for k in range(11):
            q=85+11*pair+k;previous=q-1 if k else None
            ids={q,a[k],b[k]}|({previous} if previous else set())
            group=[r for r in rows if q in map(abs,r) and set(map(abs,r))<=ids]
            need(len(group)==(5 if previous else 4),'complete gate clause group')
            for bits in product((False,True),repeat=len(ids)):
                values=dict(zip(sorted(ids),bits));expected=values[q]==((values[previous] if previous else True) and values[a[k]]==values[b[k]])
                need(sat(group,values)==expected,'gate biconditional truth table');gate_cases+=1
    first=rows[:66];a,b=gen.columns()[:2];comparisons=0
    for left in product((0,1),repeat=6):
        for right in product((0,1),repeat=6):
            x=left+(0,)*6;y=right+(0,)*6;values=dict(zip(a,x));values.update(zip(b,y))
            values.update({85+k:x[:k+1]==y[:k+1] for k in range(11)})
            need(sat(first,values)==(left<=right),'lex comparator canonical extension');comparisons+=1
    phases=gen.phase_rows();forbidden={tuple(int(v<0) for v in row) for row in phases[:2720]}
    need(len(forbidden)==2720,'distinct phase assignments');phase_cases=0
    for w in product((0,1),repeat=12):
        minimum=min(audit.shifted(w,s) for s in range(3))
        need((w not in forbidden)==(w==minimum),'phase clause truth table');phase_cases+=1
    small=0
    for triangles in (1,2,3):
        for red in range(triangles+1):
            keys=[(i,j,d) for i,j in combinations(range(triangles),2) for d in range(3)];ids={k:v+1 for v,k in enumerate(keys)}
            def edge(a,b):
                i,s=divmod(a,3);j,t=divmod(b,3)
                return i<red if i==j else ids[i,j,(t-s)%3]
            n=3*triangles;edges={e:edge(*e) for e in combinations(range(n),2)}
            rows=gen.forbid(n,edge,((5,True),(4,False)))
            independent=sorted(audit.clique_rows(n,edges,5,True)[0]|audit.clique_rows(n,edges,4,False)[0])
            need(rows==independent,'small recursion formula')
            for bits in product((False,True),repeat=len(keys)):
                values=dict(enumerate(bits,1));colors={e:(v if type(v)is bool else values[v]) for e,v in edges.items()}
                literal=not any(all(colors[e]==color for e in combinations(vs,2)) for size,color in ((5,True),(4,False)) for vs in combinations(range(n),size))
                need(sat(rows,values)==literal,'small literal clique semantics');small+=1
    return dict(gate_truth_rows=gate_cases,lex_pairs=comparisons,phase_words=phase_cases,small_invariant_graphs=small)


def corruptions(work,reps,local_path,full_path):
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,IndexError,KeyError):rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    for name,change in [
        ('nonpermutation',lambda r:r['representatives'][0]['pullback_permutation'].__setitem__(0,r['representatives'][0]['pullback_permutation'][1])),
        ('wrong_image',lambda r:r['representatives'][0].__setitem__('word','0'*21)),
        ('missing_image',lambda r:r['representatives'].pop()),
        ('duplicate_image',lambda r:r['representatives'].__setitem__(1,copy.deepcopy(r['representatives'][0]))),
        ('wrong_stabilizer',lambda r:r.__setitem__('red_stabilizer',25))]:
        r=copy.deepcopy(reps);change(r);reject(name,lambda:audit.check_representatives(r))
    local_lines=local_path.read_text().splitlines();full_lines=full_path.read_text().splitlines()
    mutations=[('wrong_local_header','classification',['p cnf 84 22666']+local_lines[1:]),
        ('drop_blocker','classification',local_lines[:-1]),
        ('drop_phase_clause','classification',local_lines[:11585]+local_lines[11586:]),
        ('wrong_gate','classification',local_lines[:22465]+['1 0']+local_lines[22466:]),
        ('extra_local_unit','classification',local_lines+['1 0']),
        ('wrong_full_header','extension',['p cnf 215 131652']+full_lines[1:]),
        ('drop_full_clause','extension',full_lines[:-1]),
        ('extra_full_unit','extension',full_lines+['1 0']),
        ('local_as_full','extension',local_lines)]
    for name,kind,lines in mutations:
        bad=work/(name+'.cnf');bad.write_text('\n'.join(lines)+'\n');reject(name,lambda:audit.check_formula(bad,kind,reps))
    return rejected


def run(work):
    work.mkdir(parents=True,exist_ok=True);reps=gen.representatives();out=logical()
    for kind in ('classification','extension'):gen.write(work/(kind+'.cnf'),kind)
    out['formulas']={kind:audit.check_formula(work/(kind+'.cnf'),kind,reps) for kind in ('classification','extension')}
    out['representatives']=audit.check_representatives(reps)
    out['rejected']=corruptions(work,reps,work/'classification.cnf',work/'extension.cnf')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    a.report.write_text(json.dumps(run(a.work),indent=2,sort_keys=True)+'\n')
