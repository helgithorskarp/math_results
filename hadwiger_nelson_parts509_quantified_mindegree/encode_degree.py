#!/usr/bin/env python3
"""Family-equivalent degree restriction; skipped selections need not be colourable."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_parts509_quantified_dual'))
import encode_dual as base


def check_inputs():
    for name,digest in json.loads((HERE/'manifest.json').read_text())['inputs'].items():
        base.require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('source hash',name))
    return base.original()


def degrees(n,edges,cross):
    adj=[set() for _ in range(n)]
    fixed=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    for a,v in cross:fixed[v].add(a)
    return adj,list(map(len,fixed))


def serialize(nv,universal,rows):
    used={abs(v) for row in rows for v in row}
    padding=[v for v in range(1,nv+1) if v not in used]
    rows=rows+[[v,-v] for v in padding]
    prefix=([('a',list(range(1,universal+1)))] if universal else [])+[
        ('e',list(range(universal+1,nv+1)))]
    raw=(f'p cnf {nv} {len(rows)}\n'+
         ''.join(q+' '+' '.join(map(str,vs))+' 0\n' for q,vs in prefix)+
         ''.join(' '.join(map(str,row))+(' ' if row else '')+'0\n' for row in rows)).encode('ascii')
    return raw,len(padding),len(rows)


def encode(n,edges,cross,patterns,budget,selection=None):
    old,meta=base.encode(n,edges,cross,patterns,budget,selection)
    adj,fixed=degrees(n,edges,cross)
    rows=[list(map(int,line.split()[:-1])) for line in old.decode('ascii').splitlines()
          if not line.startswith(('p ','a ','e '))]
    nv=meta['variables'];original_nv=nv
    extra=dict(base_qdimacs_sha256=meta['qdimacs_sha256'],base_variables=nv,
               base_clauses=meta['clauses'],degree_witnesses=0,degree_aliases=0,
               degree_counter_variables=0,degree_clauses=0,escape_variable=None,
               fixed_deficient_vertices=None)
    if selection is not None:
        bad=sorted(v for v in selection if fixed[v]+len(adj[v]&selection)<4)
        extra['fixed_deficient_vertices']=bad
        if bad:
            raw,pad,nc=serialize(nv,0,[])
            meta.update(clauses=nc,tautology_padding=pad,qdimacs_sha256=sha256(raw).hexdigest())
        else:
            raw=old
        meta.update(extra)
        return raw,meta

    pad=meta['tautology_padding']
    if pad:rows=rows[:-pad]
    counter=rows[:meta['counter_clauses']]
    colouring=rows[meta['counter_clauses']:]
    guard=meta['overflow']
    if type(guard) is not bool:
        base.require(all(r[0]==guard for r in colouring),'base guard layout')
        colouring=[r[1:] for r in colouring]
    else:
        base.require(guard is False,'universal base overflow')
    card=base.load('degree_cardinality',REPO/'hadwiger_nelson_parts509_pool_shape_closure/cardenc.py')
    witnesses=[];degree_rows=[];counter_vars=0;witness_vars=0
    for v in range(n):
        k=3-fixed[v]
        if k<0:
            continue
        neighbours=[u+1 for u in sorted(adj[v])]
        if len(neighbours)<=k:
            witnesses.append(v+1)
            continue
        nv+=1;w=nv;witness_vars+=1;witnesses.append(w)
        degree_rows.append([-w,v+1])
        begin=nv
        clauses,nv=card.atmost(neighbours,k,nv)
        counter_vars+=nv-begin
        degree_rows.extend([-w]+row for row in clauses)
    if not witnesses:
        meta.update(extra)
        return old,meta
    nv+=1;escape=nv
    # escape can be true only if overflow or an actual selected low-degree witness holds.
    escape_clause=[-escape]+([] if guard is False else [guard])+witnesses
    final=counter+degree_rows+[escape_clause]+[[escape]+row for row in colouring]
    raw,pad,nc=serialize(nv,n,final)
    extra.update(degree_witnesses=witness_vars,degree_aliases=len(witnesses)-witness_vars,
                 degree_counter_variables=counter_vars,degree_clauses=len(degree_rows),escape_variable=escape)
    meta.update(variables=nv,clauses=nc,existential=nv-n,tautology_padding=pad,
                qdimacs_sha256=sha256(raw).hexdigest(),**extra)
    base.require(nv-original_nv==witness_vars+counter_vars+1,'allocation count')
    return raw,meta


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    old=check_inputs();source,U=old.pool_input()
    raw,meta=encode(**source,budget=134)
    args.out.write_bytes(raw)
    print(json.dumps(meta,indent=2,sort_keys=True))


if __name__=='__main__':main()
