#!/usr/bin/env python3
"""Definition-level graph checks against the parsed dual matrix."""
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
import encode_dual as enc

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_parts509_quantified_selector'))


def parse(raw):
    lines=raw.decode('ascii').splitlines()
    h=lines.pop(0).split()
    enc.require(len(h)==4 and h[:2]==['p','cnf'],'header')
    nv,nc=map(int,h[2:])
    prefix=[]
    while lines and lines[0].startswith(('a ','e ')):
        r=lines.pop(0).split()
        enc.require(r[-1]=='0','prefix terminator')
        prefix.append((r[0],list(map(int,r[1:-1]))))
    enc.require([q for q,_ in prefix] in [['a','e'],['e']],'prefix order')
    enc.require(sorted(v for _,vs in prefix for v in vs)==list(range(1,nv+1)),'prefix partition')
    rows=[]
    for line in lines:
        r=list(map(int,line.split()))
        enc.require(r and r[-1]==0 and all(1<=abs(v)<=nv for v in r[:-1]),'clause format')
        rows.append(tuple(r[:-1]))
    enc.require(len(rows)==nc,'clause count')
    enc.require({abs(v) for row in rows for v in row}==set(range(1,nv+1)),'atom occurrence')
    return prefix,rows


def colourable(case,selected):
    vertices=sorted(selected)
    for p in case['patterns']:
        for values in itertools.product(range(4),repeat=len(vertices)):
            c=dict(zip(vertices,values))
            if any(a in c and b in c and c[a]==c[b] for a,b in case['edges']):
                continue
            if any(v in c and c[v]==p[a] for a,v in case['cross']):
                continue
            return True
    return False


def check_colouring(source,witness,raw,meta):
    c=list(map(int,witness['colouring']))
    p=witness['class_index']
    enc.require(len(c)==source['n'] and all(0<=v<4 for v in c) and
                type(p) is int and 0<=p<len(source['patterns']),'witness format')
    enc.require(all(c[a]!=c[b] for a,b in source['edges']),'witness pool edge')
    enc.require(all(c[v]!=source['patterns'][p][a] for a,v in source['cross']),'witness cross edge')
    positive={meta['color_variables'][i][c[i]] for i in range(len(c))}|{meta['pattern_variables'][p]}
    _,rows=parse(raw)
    enc.require(all(any((v>0)==(abs(v) in positive) for v in row) for row in rows),'witness matrix')


def decode_native(log,source,raw,meta):
    values=[int(v) for line in log.splitlines() if line.startswith('V ')
            for v in line.split()[1:] if v!='0']
    assignment=set(values)
    enc.require(not any(-v in assignment for v in assignment),'conflicting native literals')
    _,rows=parse(raw)
    enc.require(all(any(v in assignment for v in row) for row in rows),'native matrix witness')
    p=next(j for j,v in enumerate(meta['pattern_variables']) if v in assignment)
    c=''.join(str(next(j for j,v in enumerate(vs) if v in assignment)) for vs in meta['color_variables'])
    witness=dict(class_index=p,colouring=c)
    check_colouring(source,witness,raw,meta)
    return witness


def fixtures():
    old=enc.load('old_controls',REPO/'hadwiger_nelson_parts509_quantified_selector/controls.py')
    result=old.controls()
    pairs=list(itertools.combinations(range(3),2))
    for mask in range(1<<len(pairs)):
        for b in range(4):
            result.append(dict(name=f'all3_edges{mask}_b{b}',n=3,
                edges=[pair for i,pair in enumerate(pairs) if (mask>>i)&1],
                cross=[(a,v) for a in range(3) for v in range(3)],patterns=[[0,1,2]],budget=b))
    for b in range(6):
        result.append(dict(name=f'odd_counter5_b{b}',n=5,edges=[(0,1),(1,2),(2,3),(3,4)],
            cross=[(a,v) for a in range(3) for v in range(5)],patterns=[[0,1,2]],budget=b))
    return result


def abstract_checks():
    audit=enc.load('old_dpll',REPO/'hadwiger_nelson_parts509_quantified_selector/verify_controls.py')
    results=[]
    for case in fixtures():
        args={k:case[k] for k in ['n','edges','cross','patterns','budget']}
        raw,meta=enc.encode(**args)
        prefix,rows=parse(raw)
        u=prefix[0][1] if prefix[0][0]=='a' else []
        enc.require(u==list(range(1,case['n']+1)),'selector order')
        failing=[]
        for mask in range(1<<case['n']):
            selected={i for i in range(case['n']) if (mask>>i)&1}
            expected=len(selected)>case['budget'] or colourable(case,selected)
            assumptions=[v if (v-1) in selected else -v for v in u]
            actual=audit.sat(rows,assumptions)
            enc.require(actual==expected,('dual mismatch',case['name'],mask))
            # Fixed-selection partial evaluation must preserve this same matrix truth.
            fixed,_=enc.encode(**args,selection=selected)
            fixed_prefix,fixed_rows=parse(fixed)
            enc.require([q for q,_ in fixed_prefix]==['e'],'fixed prefix')
            enc.require(audit.sat(fixed_rows,[])==expected,('fixed mismatch',case['name'],mask))
            if not actual:
                failing.append(mask)
        if 'expected' in case:
            enc.require(bool(failing)==case['expected'],'negation of original fixture')
        results.append(dict(name=case['name'],dual_truth=not failing,failing_selection_masks=failing,
            selections_checked=1<<case['n'],qdimacs_sha256=meta['qdimacs_sha256']))
    return results


def compute():
    enc.original()  # Check all pinned dependencies before running the audits.
    checks=abstract_checks()
    old=enc.original()
    source,U=old.pool_input()
    raw,meta=enc.encode(**source,budget=134)
    parse(raw)
    pool_meta={k:v for k,v in meta.items() if k not in ['color_variables','pattern_variables']}
    leak=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/s_vertex_leaks.json').read_text())['leaks']['397'][0]
    indices=[i for i,v in enumerate(U) if v<509 and v!=397]
    H=old.restrict(source,indices)
    c=list(map(int,leak['witness_colouring_S_minus_v']))
    p=leak['class_index']
    enc.require(len(c)==134 and all(c[a]!=c[b] for a,b in H['edges']),'proper S colouring')
    enc.require(all(c[v]!=H['patterns'][p][a] for a,v in H['cross']),'proper cross colouring')
    fixed,fm=enc.encode(**H,budget=134,selection=set(range(134)))
    prefix,rows=parse(fixed)
    positive={fm['color_variables'][i][c[i]] for i in range(134)}|{fm['pattern_variables'][p]}
    enc.require(all(any((v>0)==(abs(v) in positive) for v in row) for row in rows),'real508 matrix witness')
    native=json.loads((HERE/'native_witness.json').read_text())
    check_colouring(H,native,fixed,fm)
    return dict(status='DUAL FINITE CHECKS VERIFIED',abstract_cases=len(checks),
        selector_assignments_checked=sum(r['selections_checked'] for r in checks),
        fixed_specializations_checked=sum(r['selections_checked'] for r in checks),
        abstract_controls=checks,full_instance=pool_meta,
        real508=dict(vertices=508,edges=1860+len(H['edges'])+len(H['cross']),deleted_vertex=397,
            class_index=p,proper_colouring_checked=True,cnf_witness_checked=True,
            native_class_index=native['class_index'],native_colouring_checked=True,
            qdimacs_sha256=fm['qdimacs_sha256'],cnf_sha256=sha256(enc.to_cnf(fixed)).hexdigest()))


def main():
    result=compute()
    enc.require(result==json.loads((HERE/'expected.json').read_text()),'expected results differ')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
