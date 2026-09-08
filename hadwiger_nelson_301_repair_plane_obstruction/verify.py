#!/usr/bin/env python3
"""Exact certificate checker; Python standard library, no solver or CAS."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
from math import isqrt
import argparse,copy,hashlib,json
D=Path(__file__).resolve().parent
SOURCE=D.parent/'hadwiger_nelson_h516_k23free_edge_repair'
GRAPH_SHA='7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb'
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
    need(V==sorted(set(V)) and n==301,'graph labels')
    edges=graph['edges'];E={tuple(e) for e in edges}
    need(edges==[list(e) for e in sorted(E)] and len(E)==1452,'edge format')
    need(all(a in ix and b in ix and a<b for a,b in E),'simple graph')
    need(cert['source_sha256']==GRAPH_SHA,'certificate source identity')
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
def positive_audit(graph):
    V=graph['labels'];E=graph['edges'];ix={v:i for i,v in enumerate(V)}
    five=json.loads((SOURCE/'five_colouring.json').read_text())['colours']
    need(set(five)==set(map(str,V)) and set(five.values())==set(range(5)),'five word domain')
    need(all(five[str(u)]!=five[str(v)] for u,v in E),'five word edges')
    words=json.loads((SOURCE/'vertex_deletion_colours.json').read_text())['colourings']
    need(set(words)==set(map(str,V)),'deletion words domain')
    for v in V:
        order=[u for u in V if u!=v];word=words[str(v)]
        need(len(word)==len(order) and all(type(c) is int and 0<=c<4 for c in word),'deletion word alphabet')
        colour=dict(zip(order,word));need(all(v in (a,b) or colour[a]!=colour[b] for a,b in E),'deletion word edge')
    tri=graph['triangle'];need(len(set(tri))==3 and all(sorted(e) in E for e in combinations(tri,2)),'colour pin triangle')
    lines=[f'p cnf {4*len(V)} {len(V)+4*len(E)+3}\n']
    lines += [' '.join(str(4*i+c+1) for c in range(4))+' 0\n' for i in range(len(V))]
    lines += [f'{-4*ix[u]-c-1} {-4*ix[v]-c-1} 0\n' for u,v in E for c in range(4)]
    lines += [f'{4*ix[v]+c+1} 0\n' for c,v in enumerate(tri)]
    need(''.join(lines).encode()==(SOURCE/'four_colour.cnf').read_bytes(),'positive CNF identity')
    return {'proper_five_colouring':True,'deletion_four_colourings':len(V),'CNF_reconstructed':True,
        'lower_bound_trust':'requires separate strict LRAT replay; not inferred from this audit'}
def controls(graph,cert):
    cases=[]
    x=copy.deepcopy(cert);x['cycles'][0][0]=x['cycles'][0][1];cases.append(('degenerate_cycle',graph,x))
    x=copy.deepcopy(cert);x['diagonal_obstructions'].pop(next(iter(x['diagonal_obstructions'])));cases.append(('missing_diagonal',graph,x))
    x=copy.deepcopy(cert)
    w=next(w for w in x['diagonal_obstructions'].values() if w['type']=='odd_wheel');w['rim'][0]=w['hub'];cases.append(('bad_wheel',graph,x))
    x=copy.deepcopy(cert);r=next(r for r in x['parametrization'] if r);r[0][1]+=1;cases.append(('bad_parametrization',graph,x))
    x=copy.deepcopy(cert);x['affine_rank']+=1;cases.append(('bad_rank',graph,x))
    x=copy.deepcopy(cert);x['norm_weights'][0][2]+=1;x['weight_sum']+=1;cases.append(('bad_quadratic_identity',graph,x))
    g=copy.deepcopy(graph);g['edges'].pop();cases.append(('missing_source_edge',g,cert))
    rejected=[]
    for name,g,c in cases:
        try:audit(g,c)
        except ValueError:rejected.append(name)
        else:raise ValueError('bad certificate accepted: '+name)
    return rejected
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=D/'certificate.json');ap.add_argument('--controls',action='store_true');ap.add_argument('--positive',action='store_true');a=ap.parse_args()
    raw=(SOURCE/'graph.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==GRAPH_SHA,'named source graph hash')
    graph=json.loads(raw);cert=json.loads(a.certificate.read_text());r=audit(graph,cert)
    if a.controls:r['rejected_controls']=controls(graph,cert)
    if a.positive:r['positive_audit']=positive_audit(graph)
    r['certificate_sha256']=hashlib.sha256(a.certificate.read_bytes()).hexdigest();print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
