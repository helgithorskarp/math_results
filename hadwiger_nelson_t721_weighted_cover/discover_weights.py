#!/usr/bin/env python3
"""Optional untrusted LP producer; every rounded weight is checked as an integer."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
import cover,verify
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args()
    out=a.output.resolve()
    if out.is_relative_to(HERE.parent):raise ValueError('put generated output outside the repository')
    g=cover.geometry(a.input);c=json.loads((HERE/'certificate.json').read_text());report=cover.full_cover(c,g,require_target=False);M=set(report['mandatory_global_vertices']);n=len(g['points'])
    A=lil_matrix((n,n));adj=[set()for _ in range(n)]
    for u,v in g['edges']:adj[u].add(v);adj[v].add(u)
    for v in range(n):
        A[v,v]=4
        for u in adj[v]:A[v,u]=-1
    r=linprog(np.ones(n),A_ub=A.tocsr(),b_ub=np.zeros(n),bounds=[(1,1)if u in M else(0,1)for u in range(n)],method='highs')
    if not r.success:raise ValueError(r.message)
    weights={u:int(round(-2*t))for u,t in enumerate(r.ineqlin.marginals)if int(round(-2*t))}
    incidence=[sum(weights.get(v,0)for v in adj[u])for u in range(n)]
    proof={'version':'t721-weighted-neighbour-v1','minimum_degree':4,'outside_capacity':2,'weights':sorted([u,w]for u,w in weights.items()),'exceptional_outside':[u for u in range(n)if u not in M and incidence[u]>2]}
    result=verify.weighted_bound(proof,g,sorted(M));cover.need(result['minimum_critical_order']>508,'produced weights do not close target')
    data=(json.dumps(proof,separators=(',',':'))+'\n').encode();out.write_bytes(data)
    print(json.dumps({'verified_integer_bound':result['minimum_critical_order'],'byte_identical_to_published':data==(HERE/'weights.json').read_bytes()}))
