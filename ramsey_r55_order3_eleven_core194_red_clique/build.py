#!/usr/bin/env python3
"""Three complete exact-cardinality RED extensions; no solver here."""
from itertools import combinations
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import audit

ROOT=Path(__file__).resolve().parent
DIRECT=ROOT.parent/'ramsey_r55_order3_eleven_core194_direct'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


generator=module('red_direct_generator',DIRECT/'generate.py')
checker=module('red_direct_checker',DIRECT/'check.py')
need=audit.need
identity=generator.identity
IDS=('e2','e3','e4')


def atomic(path,data):
    tmp=path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def sources():
    paths=[ROOT/n for n in ('build.py','audit.py','run.py','verify.py','controls.py','PROOF.md')]
    paths += [DIRECT/n for n in ('generate.py','check.py','decode.py','PROOF.md','result.json')]
    paths += [ROOT.parent/'ramsey_r55_order3_eleven_core194_attachments/audit.py']
    for directory in ('ramsey_r55_order3_eleven_core194_direct_review1','ramsey_r55_core194_a4_fixed_review1','ramsey_r55_order3_eleven_core194_multiplicity_review1'):
        paths += [ROOT.parent/directory/n for n in ('README.md','result.json')]
    for directory in ('ramsey_r55_order3_eleven_core194_a4_fixed','ramsey_r55_order3_eleven_core194_multiplicity'):
        paths += [ROOT.parent/directory/n for n in ('PROOF.md','result.json')]
    return {str(p.relative_to(ROOT.parent)):identity(p) for p in paths}


def tail(q):
    rows=[]
    for f in range(35,33+q):
        rows += [[-generator.variable(3*i,f)] for i in range(4)]
    rows += [[generator.variable(u,v)] for u,v in combinations(range(33,33+q),2) if (u,v)!=(33,34)]
    rows += [[generator.variable(3*i,f) for i in range(4)] for f in range(33+q,43)]
    need(rows==list(map(list,audit.expected(q))),'all physical clauses match producer')
    return rows


def write_child(base,path,q):
    rows=tail(q)
    with base.open('rb') as f,path.open('wb') as g:
        need(f.readline()==b'p cnf 320 364095\n','complete RED header')
        g.write(f'p cnf 320 {364095+len(rows)}\n'.encode());shutil.copyfileobj(f,g)
        for row in rows:g.write((' '.join(map(str,row))+' 0\n').encode())


def check_child(base,path,q):
    rows=audit.expected(q)
    with base.open('rb') as f,path.open('rb') as g:
        need(f.readline()==b'p cnf 320 364095\n','RED base header')
        need(g.readline()==f'p cnf 320 {364095+len(rows)}\n'.encode(),'exact child header')
        while block:=f.read(1<<20):need(g.read(len(block))==block,'entire RED base retained')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'exact physical child clause')
        need(not g.read(),'exact EOF')
    return identity(path)


def controls(base,work):
    q=4;path=work/'e4.cnf';data=path.read_bytes();head,body=data.split(b'\n',1)
    rows=tail(q);suffix=b''.join((' '.join(map(str,row))+' 0\n').encode() for row in rows)
    need(data.endswith(suffix),'complete production suffix');prefix=data[:-len(suffix)]
    def with_rows(rs):return prefix+b''.join((' '.join(map(str,row))+' 0\n').encode() for row in rs)
    samples=dict(wrong_header=b'p cnf 320 364113\n'+body,lost_base=head+b'\n'+body[1:],
        missing_nonempty=with_rows(rows[:-1]),missing_empty=with_rows(rows[1:]),
        wrong_empty_sign=with_rows([[-rows[0][0]]]+rows[1:]),
        wrong_clique_sign=with_rows(rows[:8]+[[-rows[8][0]]]+rows[9:]),
        extra_no_BB=data+b'169 177 0\n',missing_clique=with_rows(rows[:8]+rows[9:]))
    bad=work/'bad.cnf';rejected=[]
    for name,b in samples.items():
        bad.write_bytes(b)
        try:check_child(base,bad,q)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    bad.unlink();return rejected


def graph(path,q):
    result=checker.graph(path,'red')
    lines=path.read_text().splitlines();red={tuple(map(int,line.split())) for line in lines[1:]}
    empty=[f for f in range(33,43) if not any((a,f) in red for a in range(12))]
    need(empty==list(range(33,33+q)),'literal exact empty set')
    need(all(e in red for e in combinations(empty,2)),'literal red empty clique')
    return dict(**result,empty_fixed_vertices=empty)


def build(work):
    work.mkdir(parents=True,exist_ok=True);cover=audit.cover()
    base=work/'red.cnf';gen=generator.write('red',base);independent=checker.audit(base,'red')
    pin=dict(bytes=14841387,sha256='2aa575e6b988d788f57f98abaa3728518517adc02c795ef5f75458c459e85a72')
    need(gen['formula']==pin and independent['sha256']==pin['sha256'],'reviewed complete RED identity')
    symmetries=audit.base_symmetries(base);cases=[]
    for q,key in zip((2,3,4),IDS):
        path=work/(key+'.cnf');write_child(base,path,q)
        cases.append(dict(id=key,counts=[q],empty_fixed_vertices=list(range(33,33+q)),
            added_clauses=tail(q),formula=check_child(base,path,q),status='untested'))
    return json.loads(json.dumps(dict(cases=cases,cover=cover,base_generation=gen,base_audit=independent,
        base_symmetries=symmetries,file_controls=controls(base,work))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();w=a.work.resolve()
    need(not w.is_relative_to(ROOT.parent),'external work');answer=build(w);atomic(w/'preparation.json',answer)
    print('PASS complete RED empty-clique cover, literal tails, and full formulas')
