#!/usr/bin/env python3
"""Focused malformed-formula, graph and model checks; no proof search."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import check
import decode

ROOT=Path(__file__).resolve().parent


def run(work,formulas):
    work.mkdir(parents=True,exist_ok=True)
    rejected=[]
    def reject(name,fn):
        try:
            fn()
        except (ValueError,KeyError,IndexError):
            rejected.append(name)
        else:
            raise ValueError('accepted malformed '+name)
    formula_reports=[]
    for color in ('blue','red'):
        expected=check.expected(color)
        path=formulas/(color+'.cnf')
        formula_reports.append(check.audit(path,color,expected))
        lines=path.read_text().splitlines()
        def save(rows):
            bad=work/'bad.cnf'
            bad.write_text('\n'.join(rows)+'\n')
            check.audit(bad,color,expected)
        for name in ('wrong_header','omitted_row','extra_empty','wrong_core','wrong_pair','opposite_case','new_variable','repeated_literal'):
            altered=lines[:]
            if name=='wrong_header':altered[0]=altered[0].replace('320','321')
            if name=='omitted_row':altered.pop(1);altered[0]='p cnf 320 '+str(len(altered)-1)
            if name=='extra_empty':altered.append('0');altered[0]='p cnf 320 '+str(len(altered)-1)
            if name in ('wrong_core','wrong_pair'):
                ids,_,fixed=check.setup(color)
                x=ids[0,3] if name=='wrong_core' else ids[33,34]
                old=f'{x if fixed[x] else -x} 0';new=f'{-x if fixed[x] else x} 0'
                check.require(old in altered,'unit mutation domain')
                altered[altered.index(old)]=new
            if name=='opposite_case':altered=(formulas/('red.cnf' if color=='blue' else 'blue.cnf')).read_text().splitlines()
            if name=='new_variable':altered[1]='321 0'
            if name=='repeated_literal':altered[1]='1 1 0'
            reject(color+'_'+name,lambda:save(altered))
    fixtures={n:check.graph(ROOT/n) for n in ('blue_pair14.edges','red_pair15.edges')}
    lines=(ROOT/'blue_pair14.edges').read_text().splitlines()
    for name in ('duplicate_edge','bad_vertex','monochromatic_complete'):
        bad=work/'bad.edges'
        data=lines[:]
        if name=='duplicate_edge':data.append(lines[1])
        if name=='bad_vertex':data.append('0 14')
        if name=='monochromatic_complete':data=['5']+[f'{a} {b}' for a,b in combinations(range(5),2)]
        bad.write_text('\n'.join(data)+'\n')
        reject(name,lambda:check.graph(bad))
    # Decode an independently prescribed assignment and compare all903 colors.
    literals=[x if x%7 in (1,2,4) else -x for x in range(1,321)]
    log=work/'model.log';log.write_text('s SATISFIABLE\nv '+' '.join(map(str,literals))+' 0\n')
    graph=work/'model.edges';decode.write(log,graph)
    ids,internal=check.orbits()
    red={tuple(map(int,s.split())) for s in graph.read_text().splitlines()[1:]}
    check.require(all((e in red)==(internal[e] if e in internal else ids[e]%7 in (1,2,4)) for e in combinations(range(43),2)),'independent903-pair decoder check')
    for name in ('incomplete_model','conflicting_model','invalid_model_index','missing_terminator','after_terminator'):
        row=literals[:]
        if name=='incomplete_model':row.pop()
        if name=='conflicting_model':row.append(-literals[0])
        if name=='invalid_model_index':row.append(321)
        suffix='' if name=='missing_terminator' else ' 0'
        if name=='after_terminator':suffix+=' 1'
        log.write_text('v '+' '.join(map(str,row))+suffix+'\n')
        reject(name,lambda:decode.values(log))
    for n in ('bad.cnf','bad.edges','model.log','model.edges'):(work/n).unlink()
    check.require(len(rejected)==24,'all negative controls')
    return dict(formulas=formula_reports,fixtures=fixtures,local_signature_witnesses=check.local_lemma(),
                decoded_physical_pairs=903,rejected=rejected)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--formulas',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    a.report.write_text(json.dumps(run(a.work,a.formulas),indent=2,sort_keys=True)+'\n')
    print('PASS direct formula, local witness and model controls')
