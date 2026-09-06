#!/usr/bin/env python3
"""Exhaustive small graph/CNF bridge and malformed-input controls."""
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import json
import audit
import generate as gen


def small():
    count = 0
    for t in range(1,4):
        n = 3*t;nv = 3*t*(t-1)//2
        for r in range(t+1):
            clauses = gen.ramsey_clauses(t,r);literal = audit.primary(t,r)
            for values in product((False,True),repeat=nv):
                red = {e for e,c in literal.items() if (c if type(c) is bool else values[c-1])}
                actual = audit.clique_count(n,red,5,True)==0 and audit.clique_count(n,red,4,False)==0
                encoded = all(any(values[abs(v)-1]==(v>0) for v in row) for row in clauses)
                audit.need(actual==encoded, 'small complete coloring/encoding equivalence');count += 1
    audit.need(count==2074, 'complete small domain')
    return count


def run(work):
    work.mkdir(parents=True,exist_ok=True);cases=gen.cases();audit.check_cases(cases);rejected=[]
    for name in ('missing_case','changed_core','wrong_case'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='changed_core':bad[0]['bits']='1'+bad[0]['bits'][1:]
        if name=='wrong_case':bad[0]['index']=109
        try:audit.check_cases(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    path=work/'control.cnf';gen.write(path,cases[0]);formula=audit.check_formula(path,cases[0]);lines=path.read_text().splitlines(keepends=True)
    for name in ('lost_ramsey','changed_sign','lost_core','global_core_variable','extra_normalizer','bad_header'):
        bad=lines[:]
        if name=='lost_ramsey':bad.pop(1)
        if name=='changed_sign':bad[1]=bad[1].replace('-', '',1)
        if name=='lost_core':bad.pop()
        if name=='global_core_variable':bad[-9]='31 0\n'
        if name=='extra_normalizer':bad.append('1 0\n')
        if name=='bad_header':bad[0]='p cnf 85 1\n'
        path.write_text(''.join(bad))
        try:audit.check_formula(path,cases[0])
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    path.unlink()
    return dict(small_graphs=small(), cases=audit.check_cases(cases), formula=formula, rejected=rejected)


def graph_controls(path,case,work):
    work.mkdir(parents=True,exist_ok=True);n,red=audit.read_edges(path);rejected=[]
    def write(edges):
        out=work/'bad.edges';out.write_text(f'24 {len(edges)}\n'+''.join(f'{a} {b}\n' for a,b in sorted(edges)));return out
    for name in ('red_K5','blue_K4','wrong_core','duplicate_edge','bad_order'):
        edges=red.copy()
        if name=='red_K5':edges.update(combinations(range(5),2))
        if name=='blue_K4':edges-=set(combinations(range(4),2))
        if name=='wrong_core':edges.symmetric_difference_update({(0,3)})
        out=write(edges)
        if name=='duplicate_edge':
            rows=out.read_text().splitlines();rows[0]=f'24 {len(edges)+1}';rows.append(rows[1]);out.write_text('\n'.join(rows)+'\n')
        if name=='bad_order':out.write_text(out.read_text().replace('24 ','43 ',1))
        try:audit.check_graph(out,case)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    out.unlink();return rejected


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    a.report.write_text(json.dumps(run(a.work),indent=2,sort_keys=True)+'\n');print('PASS small graphs and nine corruptions')
