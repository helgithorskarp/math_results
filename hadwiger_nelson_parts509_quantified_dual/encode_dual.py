#!/usr/bin/env python3
"""Universal pool selection, existential four-colouring; true means closure."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(test,message):
    if not test:
        raise RuntimeError(message)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def original():
    pins=json.loads((HERE/'manifest.json').read_text())['inputs']
    for name,digest in pins.items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('source hash',name))
    return load('prior_pool_encoder',REPO/'hadwiger_nelson_parts509_quantified_selector/encode.py')


def encode(n,edges,cross,patterns,budget,selection=None):
    require(type(n) is int and n>=0 and type(budget) is int and 0<=budget<=n,'domain')
    require(patterns and all(len(p)==len(patterns[0]) and
            all(type(c) is int and 0<=c<4 for c in p) for p in patterns),'patterns')
    require(edges==sorted(set(edges)) and all(0<=a<b<n for a,b in edges),'edges')
    require(cross==sorted(set(cross)) and all(0<=a<len(patterns[0]) and 0<=v<n for a,v in cross),'cross')
    if selection is not None:
        require(type(selection) in [set,frozenset] and selection<=set(range(n)),'selection')
    selectors=list(range(1,n+1)) if selection is None else []
    x=selectors if selection is None else [i in selection for i in range(n)]
    nv=len(selectors)
    clauses=[]
    overflow=False
    if selection is not None:
        overflow=len(selection)>budget
    elif budget<n:
        card=load('dual_cardinality',REPO/'hadwiger_nelson_parts509_pool_shape_closure/cardenc.py')
        clauses,out,nv=card.totalizer(selectors,nv,kmax=budget+1)
        overflow=out[budget]
    counter_variables=nv-len(selectors)
    counter_clauses=len(clauses)
    colors=[]
    for _ in range(n):
        colors.append(list(range(nv+1,nv+5)))
        nv+=4
    classes=list(range(nv+1,nv+len(patterns)+1))
    nv+=len(patterns)

    def neg(lit):
        return not lit if type(lit) is bool else -lit

    def guarded(row):
        row=[overflow]+row
        if any(type(v) is bool and v for v in row):
            return
        row=[v for v in row if type(v) is not bool]
        clauses.append(row)

    guarded(classes)
    for i in range(n):
        guarded([neg(x[i])]+colors[i])
    for a,b in edges:
        for c in range(4):
            guarded([neg(x[a]),neg(x[b]),-colors[a][c],-colors[b][c]])
    for a,v in cross:
        for j,p in enumerate(patterns):
            guarded([-classes[j],neg(x[v]),-colors[v][p[a]]])
    used={abs(v) for row in clauses for v in row}
    padding=[v for v in range(1,nv+1) if v not in used]
    clauses.extend([v,-v] for v in padding)
    prefix=[('a',selectors),('e',list(range(len(selectors)+1,nv+1)))]
    prefix=[(q,vs) for q,vs in prefix if vs]
    raw=(f'p cnf {nv} {len(clauses)}\n'+
         ''.join(q+' '+' '.join(map(str,vs))+' 0\n' for q,vs in prefix)+
         ''.join(' '.join(map(str,row))+(' ' if row else '')+'0\n' for row in clauses)).encode('ascii')
    meta=dict(variables=nv,clauses=len(clauses),universal=len(selectors),existential=nv-len(selectors),
              counter_variables=counter_variables,counter_clauses=counter_clauses,pool_vertices=n,
              pool_edges=len(edges),cross_edges=len(cross),patterns=len(patterns),budget=budget,
              fixed_selection=sorted(selection) if selection is not None else None,
              overflow=overflow,color_variables=colors,pattern_variables=classes,
              tautology_padding=len(padding),qdimacs_sha256=sha256(raw).hexdigest())
    return raw,meta


def real_case(case):
    old=original()
    source,U=old.pool_input()
    if case=='pool508':
        return encode(**source,budget=134)
    indices=[i for i,v in enumerate(U) if v<509 and (case!='delete397' or v!=397)]
    source=old.restrict(source,indices)
    return encode(**source,budget=source['n'],selection=set(range(source['n'])))


def to_cnf(raw):
    require(not any(line.startswith(b'a ') for line in raw.splitlines()),'SAT export requires no universal variables')
    return b'\n'.join(line for line in raw.splitlines() if not line.startswith((b'a ',b'e ')))+b'\n'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--case',choices=['pool508','record509','delete397'],default='pool508')
    args=ap.parse_args()
    raw,meta=real_case(args.case)
    args.out.write_bytes(raw)
    print(json.dumps(meta,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
