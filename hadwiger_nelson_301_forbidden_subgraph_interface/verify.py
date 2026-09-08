#!/usr/bin/env python3
"""Check a generic odd-wheel/parallelogram/norm certificate and this repair interface.

Core proof checks adapted from the accepted h3981 standard-library verifier.
No FLINT, solver or certificate-production code is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
from math import isqrt
import argparse, copy, hashlib, json
D=Path(__file__).resolve().parent
ORIGINAL=D.parent/'hadwiger_nelson_h516_k23free_edge_repair/graph.json'
ORIGINAL_SHA='7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb'
def need(ok,why):
    if not ok:raise ValueError(why)
def rank_mod(rows,p):
    basis={}
    for row in rows:
        r={j:x%p for j,x in enumerate(row) if x%p}
        while r:
            j=min(r);a=r[j]
            if j not in basis:
                z=pow(a,-1,p);basis[j]={k:v*z%p for k,v in r.items()};break
            for k,v in basis[j].items():
                t=(r.get(k,0)-a*v)%p
                if t:r[k]=t
                elif k in r:del r[k]
    return len(basis)
def audit(graph,cert):
    V=graph['labels'];ix={v:i for i,v in enumerate(V)};n=len(V)
    need(V==sorted(set(V)) and n>0,'graph labels')
    edges=graph['edges'];E={tuple(e) for e in edges}
    need(edges==[list(e) for e in sorted(E)],'edge format')
    need(all(a in ix and b in ix and a<b for a,b in E),'simple graph')
    rows=[];used=set();kinds={'edge':0,'odd_wheel':0};lengths={}
    for cycle in cert['cycles']:
        need(len(cycle)==4 and len(set(cycle))==4 and all(v in ix for v in cycle),'four-cycle vertices')
        need(all(tuple(sorted((a,b))) in E for a,b in zip(cycle,cycle[1:]+cycle[:1])),'four-cycle edge')
        for i in range(2):
            a,b=sorted((cycle[i],cycle[i+2]));key=f'{a},{b}'
            need(key in cert['diagonal_obstructions'],'missing diagonal certificate')
            w=cert['diagonal_obstructions'][key]
            if key in used:continue
            used.add(key);need(w['type'] in kinds,'obstruction type');kinds[w['type']]+=1
            if w['type']=='edge':need((a,b) in E,'diagonal edge')
            else:
                hub=w['hub'];rim=w['rim'];lengths[len(rim)]=lengths.get(len(rim),0)+1
                need(len(rim)>=3 and len(rim)%2==1 and len(set(rim))==len(rim),'odd simple rim')
                need(hub not in rim and all(v in ix and v!=b for v in rim+[hub]),'quotient wheel vertices')
                def qe(x,y):
                    if x==y:return False
                    xx=[a,b] if x==a else [x];yy=[a,b] if y==a else [y]
                    return any(tuple(sorted((u,v))) in E for u in xx for v in yy)
                need(all(qe(hub,v) for v in rim),'wheel spokes')
                need(all(qe(x,y) for x,y in zip(rim,rim[1:]+rim[:1])),'wheel rim edges')
        r=[0]*n
        for j,v in enumerate(cycle):r[ix[v]]=(-1)**j
        rows.append(r)
    need(used==set(cert['diagonal_obstructions']),'unused diagonal certificates')
    anchor=cert['translation_anchor'];need(anchor in ix,'translation anchor')
    rows.append([int(v==anchor) for v in V])
    free=cert['free_labels'];k=len(free)
    need(len(set(free))==k and all(v in ix for v in free),'free labels')
    need(len(cert['parametrization'])==n,'parametrization rows')
    P=[]
    for entries in cert['parametrization']:
        r={}
        for j,num,den in entries:
            need(type(j) is int and 0<=j<k and j not in r,'parameter column')
            need(type(num) is int and type(den) is int and den>0 and num!=0,'rational entry')
            r[j]=Q(num,den)
        P.append(r)
    for j,v in enumerate(free):need(P[ix[v]]=={j:Q(1)},'independent free rows')
    for r in rows:
        out={}
        for i,c in enumerate(r):
            if c:
                for j,z in P[i].items():out[j]=out.get(j,Q(0))+c*z
        need(all(z==0 for z in out.values()),'parametrization violates linear relation')
    p=cert['rank_prime'];need(type(p) is int and 2<=p<=2**31-1,'prime range')
    need(all(p%d for d in range(2,isqrt(p)+1)),'rank modulus not prime')
    rank=rank_mod(rows,p)
    need(rank==cert['affine_rank']==n-k,'rank and nullity')
    quadratic={};weight_sum=0;used_edges=set()
    for u,v,w in cert['norm_weights']:
        need((u,v) in E and (u,v) not in used_edges,'norm edge');used_edges.add((u,v))
        need(type(w) is int and w!=0,'integer norm multiplier');weight_sum+=w
        diff=P[ix[u]].copy()
        for j,z in P[ix[v]].items():diff[j]=diff.get(j,Q(0))-z
        diff={j:z for j,z in diff.items() if z}
        for i,x in diff.items():
            for j,y in diff.items():
                quadratic[i,j]=quadratic.get((i,j),Q(0))+w*x*y
    need(weight_sum==cert['weight_sum'] and weight_sum!=0,'nonzero unit-norm sum')
    need(all(z==0 for z in quadratic.values()),'weighted quadratic identity')
    return {'verified':True,'vertices':n,'edges':len(E),'mandatory_four_cycles':len(rows)-1,
        'diagonal_obstructions':len(used),'obstruction_types':kinds,'odd_wheel_rim_lengths':dict(sorted(lengths.items())),
        'anchored_linear_rank':rank,'coordinate_parameters':k,'norm_identity_edges':len(used_edges),
        'unit_norm_sum':weight_sum,'maps_excluded':'all plane unit-edge maps, including noninjective maps'}
def check_interface(graph, cert, colour, clause, original):
    result=audit(graph,cert)
    V=graph['labels']; E={tuple(e) for e in graph['edges']}
    oldV=set(original['labels']); oldE={tuple(e) for e in original['edges']}
    need(set(V)<=oldV and E<=oldE,'subgraph of original source')
    c=colour['colours']
    need(len(c)==len(V) and all(type(x) is int and 0<=x<4 for x in c),'four-colouring alphabet')
    colours=dict(zip(V,c))
    need(all(colours[u]!=colours[v] for u,v in E),'four-colouring edge')
    need(colour['source_deleted_vertex'] in oldV-set(V),'deleted source vertex is outside witness')
    lines=clause.splitlines()
    need(len(lines)==2 and lines[0]==f"p cnf {len(original['edges'])} 1",'repair clause header')
    literals=list(map(int,lines[1].split()))
    eix={tuple(e):i+1 for i,e in enumerate(original['edges'])}
    expected=sorted(-eix[e] for e in E)+[0]
    need(literals==expected,'exact edge-retention clause')
    neighbors={v:set() for v in V}
    for u,v in E:neighbors[u].add(v);neighbors[v].add(u)
    max_common=max(len(neighbors[u]&neighbors[v]) for u,v in combinations(V,2))
    has_k4=any(tuple(sorted((a,b))) in E for u,v in E for a,b in combinations(neighbors[u]&neighbors[v],2))
    result.update({'four_colourable':True,'source_vertex_subset':True,'source_edge_subset':True,
        'source_vertex_order':len(original['labels']),'source_edge_order':len(original['edges']),
        'retention_clause_literals':len(literals)-1,'maximum_common_neighbors':max_common,'K23_free':max_common<3,'K4_free':not has_k4,
        'status':'FORBIDDEN_SUBGRAPH_AND_NECESSARY_REPAIR_CLAUSE_VERIFIED',
        'graph_minimality_claimed':False,'new_unit_distance_graph_established':False})
    return result

def controls(graph,cert,colour,clause,original):
    cases=[]
    def add(name,g=None,c=None,w=None,q=None):
        cases.append((name,graph if g is None else g,cert if c is None else c,colour if w is None else w,clause if q is None else q))
    c=copy.deepcopy(cert);c['cycles'][0][0]=c['cycles'][0][1];add('degenerate_cycle',c=c)
    c=copy.deepcopy(cert);c['diagonal_obstructions'].pop(next(iter(c['diagonal_obstructions'])));add('missing_diagonal',c=c)
    c=copy.deepcopy(cert);w=next(w for w in c['diagonal_obstructions'].values() if w['type']=='odd_wheel');w['rim'][0]=w['hub'];add('bad_quotient_wheel',c=c)
    c=copy.deepcopy(cert);next(row for row in c['parametrization'] if row)[0][1]+=1;add('bad_kernel_entry',c=c)
    c=copy.deepcopy(cert);c['affine_rank']+=1;add('bad_rank',c=c)
    c=copy.deepcopy(cert);c['norm_weights'][0][2]+=1;c['weight_sum']+=1;add('bad_norm_identity',c=c)
    g=copy.deepcopy(graph);g['edges'].remove(cert['norm_weights'][0][:2]);add('missing_required_edge',g=g)
    w=copy.deepcopy(colour);u,v=graph['edges'][0];w['colours'][graph['labels'].index(u)]=w['colours'][graph['labels'].index(v)];add('bad_four_colouring',w=w)
    lines=clause.splitlines();tokens=lines[1].split();tokens.pop(0);add('missing_repair_literal',q=lines[0]+'\n'+' '.join(tokens)+'\n')
    rejected=[]
    for name,g,c,w,q in cases:
        try:check_interface(g,c,w,q,original)
        except ValueError:rejected.append(name)
        else:raise ValueError('corruption accepted: '+name)
    return rejected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--controls',action='store_true');a=ap.parse_args()
    raw=ORIGINAL.read_bytes();need(hashlib.sha256(raw).hexdigest()==ORIGINAL_SHA,'original graph identity')
    graph_raw=(D/'graph.json').read_bytes();graph=json.loads(graph_raw);cert=json.loads((D/'certificate.json').read_text())
    need(cert['source_sha256']==hashlib.sha256(graph_raw).hexdigest(),'certificate graph identity')
    colour=json.loads((D/'four_colouring.json').read_text());clause=(D/'repair_clause.cnf').read_text();original=json.loads(raw)
    result=check_interface(graph,cert,colour,clause,original)
    if a.controls:result['rejected_controls']=controls(graph,cert,colour,clause,original)
    result['graph_sha256']=hashlib.sha256(graph_raw).hexdigest()
    result['certificate_sha256']=hashlib.sha256((D/'certificate.json').read_bytes()).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
