#!/usr/bin/env python3
"""Exact bounded selector QBF; generated instances are not solver certificates."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(value, message):
    if not value:
        raise RuntimeError(message)


def encode(n, edges, cross, patterns, budget, fixed=None):
    require(type(n) is int and n >= 0 and type(budget) is int and 0 <= budget <= n,
            'selection domain')
    require(patterns and all(len(r) == len(patterns[0]) and
            all(type(c) is int and 0 <= c < 4 for c in r) for r in patterns), 'patterns')
    require(edges == sorted(set(edges)) and all(0 <= a < b < n for a,b in edges), 'pool edges')
    require(cross == sorted(set(cross)) and all(0 <= a < len(patterns[0]) and
                                              0 <= v < n for a,v in cross), 'cross edges')
    card = load('selector_cardinality', REPO / 'hadwiger_nelson_parts509_pool_shape_closure/cardenc.py')
    clauses, nv = card.atmost_tot(list(range(1,n+1)), budget, n)
    outer = list(range(1,nv+1))
    if fixed is not None:
        require(set(fixed) <= set(range(n)), 'fixed selection')
        clauses.extend([i+1 if i in fixed else -i-1] for i in range(n))
    outer_clauses = len(clauses)
    bits = max(1, (len(patterns)-1).bit_length())
    p = list(range(nv+1,nv+bits+1))
    colors = [[nv+bits+2*i+1,nv+bits+2*i+2] for i in range(n)]
    universal = p + [v for pair in colors for v in pair]
    nv += bits+2*n
    inner_first = nv+1

    def fresh():
        nonlocal nv
        nv += 1
        return nv

    def gate(inputs, conjunction):
        z = fresh()
        if conjunction:
            clauses.extend([-z, v] for v in inputs)
            clauses.append([z]+[-v for v in inputs])
        else:
            clauses.extend([z,-v] for v in inputs)
            clauses.append([-z]+list(inputs))
        return z

    matches = [gate([v if (j >> bit)&1 else -v for bit,v in enumerate(p)],True)
               for j in range(len(patterns))]
    boundary = [[gate([matches[j] for j,r in enumerate(patterns) if (r[a] >> bit)&1],False)
                 for bit in range(2)] for a in range(len(patterns[0]))]
    valid = gate(matches,False)
    witnesses = []

    def witness(a,b,selected):
        w = fresh()
        witnesses.append(w)
        clauses.extend([-w,x] for x in selected)
        for x,y in zip(a,b):
            clauses.extend([[-w,-x,y],[-w,x,-y]])

    for a,b in edges:
        witness(colors[a],colors[b],[a+1,b+1])
    for a,v in cross:
        witness(boundary[a],colors[v],[v+1])
    clauses.append([-valid]+witnesses)
    # Strict QDIMACS requires every quantified atom to occur in the matrix.
    # Tiny controls may have irrelevant selectors or colour bits.
    used={abs(v) for row in clauses for v in row}
    padding=[v for v in range(1,nv+1) if v not in used]
    clauses.extend([v,-v] for v in padding)
    prefix = [('e',outer),('a',universal),('e',list(range(inner_first,nv+1)))]
    prefix = [(q,vs) for q,vs in prefix if vs]
    require(sorted(v for _,vs in prefix for v in vs)==list(range(1,nv+1)), 'prefix partition')
    require(all(all(type(v) is int and 1 <= abs(v) <= nv for v in row) for row in clauses), 'literal range')
    data = (f'p cnf {nv} {len(clauses)}\n' +
            ''.join(q+' '+' '.join(map(str,vs))+' 0\n' for q,vs in prefix)+
            ''.join(' '.join(map(str,row))+(' ' if row else '')+'0\n' for row in clauses)).encode('ascii')
    meta = dict(variables=nv,clauses=len(clauses),outer=len(outer),universal=len(universal),
                inner=nv-inner_first+1,pool_vertices=n,pool_edges=len(edges),cross_edges=len(cross),
                patterns=len(patterns),class_bits=bits,unused_class_codes=(1<<bits)-len(patterns),
                budget=budget,outer_clauses=outer_clauses,tautology_padding=len(padding),pattern_variables=p,color_variables=colors,
                witnesses=len(witnesses),qdimacs_sha256=sha256(data).hexdigest())
    return data,meta


def pool_input():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for name,h in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==h, ('source hash',name))
    geom = load('reviewed_geometry',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    den,points,vertices,U,edges = geom.read_geometry()
    table = json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    interface = table['interface_L']
    pos = {v:i for i,v in enumerate(U)}
    ipos = {v:i for i,v in enumerate(interface)}
    cross = [(a,v) for a,v in edges if a < 374 <= v]
    require(len(cross)==36 and {a for a,v in cross} <= set(interface),'sealed interface')
    require(len(table['classes'])==20,'class count')
    for r in table['classes']:
        c=r['witness_colouring_L']
        require(len(c)==374 and set(c)<=set('0123') and c[0]=='0','L witness format')
        require(all(c[a]!=c[v] for a,v in edges if v<374),'L witness colouring')
    patterns = [[int(r['witness_colouring_L'][a]) for a in interface] for r in table['classes']]
    return dict(n=len(U),edges=sorted((pos[a],pos[v]) for a,v in edges if a in pos and v in pos),
                cross=sorted((ipos[a],pos[v]) for a,v in cross),patterns=patterns),list(U)


def restrict(source, indices):
    indices = sorted(indices)
    pos = {v:i for i,v in enumerate(indices)}
    return dict(n=len(indices),edges=sorted((pos[a],pos[b]) for a,b in source['edges'] if a in pos and b in pos),
                cross=sorted((a,pos[v]) for a,v in source['cross'] if v in pos),patterns=source['patterns'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--case',choices=['pool508','record509','delete397'],default='pool508')
    args=ap.parse_args()
    source,U=pool_input()
    if args.case=='pool508':
        data,meta=encode(**source,budget=134)
    else:
        indices=[i for i,v in enumerate(U) if v<509 and (args.case!='delete397' or v!=397)]
        source=restrict(source,indices)
        data,meta=encode(**source,budget=source['n'],fixed=set(range(source['n'])))
    args.out.write_bytes(data)
    print(json.dumps(meta,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
