#!/usr/bin/env python3
"""Deterministic certificate extraction over Q. Discovery only; verify.py is the proof check."""
from pathlib import Path
from flint import fmpq_mat
import json, time, hashlib
import argparse
D=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description='Regenerate the fixed forbidden-subgraph interface; python-flint 0.8.0')
ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
SRC=D.parent/'hadwiger_nelson_301_repair_plane_obstruction'
GRAPH=D.parent/'hadwiger_nelson_h516_k23free_edge_repair/graph.json'
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
if hashlib.sha256(GRAPH.read_bytes()).hexdigest()!='7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb':raise RuntimeError('Source graph changed')
if hashlib.sha256((SRC/'certificate.json').read_bytes()).hexdigest()!='728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42':raise RuntimeError('Source certificate changed')
G=json.loads(GRAPH.read_text()); C=json.loads((SRC/'certificate.json').read_text())
V=G['labels']; ix={v:i for i,v in enumerate(V)}; E={tuple(e) for e in G['edges']}; cycles=C['cycles']; n=len(V)
rows=[]
for q in cycles:
    r=[0]*n
    for i,v in enumerate(q):r[ix[v]]=(-1)**i
    rows.append(r)
anchor=[int(v==C['translation_anchor']) for v in V]
W=C['norm_weights']
def check(selected, details=False):
    R, rank=fmpq_mat([rows[i] for i in selected]+[anchor]).rref()
    piv=[next(j for j in range(n) if R[i,j]) for i in range(rank)]
    free=[j for j in range(n) if j not in piv]; k=len(free)
    P={j:[int(j==h) for h in free] for j in free}
    for i,j in enumerate(piv):P[j]=[-R[i,h] for h in free]
    diffs=[[a-b for a,b in zip(P[ix[u]],P[ix[v]])] for u,v,w in W]
    D=fmpq_mat(diffs); WD=fmpq_mat([[w*x for x in row] for row,(_,_,w) in zip(diffs,W)])
    gram=D.transpose()*WD
    zero=all(not gram[i,j] for i in range(k) for j in range(i,k))
    return (zero,P,free,rank,gram) if details else zero
start=time.monotonic(); selected=list(range(len(rows))); log=[]
if not check(selected):raise RuntimeError('Initial norm identity invalid')
for i in reversed(range(len(rows))):
    candidate=[j for j in selected if j!=i]
    good=check(candidate)
    if good:selected=candidate
    log.append({'removed_cycle':i,'accepted':good,'remaining_cycles':len(selected)})
    if (len(rows)-i)%20==0 or i==0:print(json.dumps({'trials':len(rows)-i,'cycles':len(selected),'seconds':time.monotonic()-start}),flush=True)
zero,P,free,rank,gram=check(selected,True)
used={','.join(map(str,sorted((cycles[i][j],cycles[i][j+2])))) for i in selected for j in range(2)}
required={tuple(sorted((u,v))) for u,v,w in W}
for i in selected:
    q=cycles[i]
    required.update(tuple(sorted((u,v))) for u,v in zip(q,q[1:]+q[:1]))
for key in sorted(used):
    a,b=map(int,key.split(','));w=C['diagonal_obstructions'][key]
    if w['type']=='edge':required.add((a,b));continue
    rim=w['rim'];hub=w['hub']
    for u,v in [(hub,x) for x in rim]+list(zip(rim,rim[1:]+rim[:1])):
        candidates=sorted({tuple(sorted((x,y))) for x in ([a,b] if u==a else [u]) for y in ([a,b] if v==a else [v]) if tuple(sorted((x,y))) in E})
        if not candidates:raise RuntimeError('Missing wheel preimage')
        required.add(min(candidates,key=lambda e:(e not in required,e)))
labels=sorted({v for e in required for v in e}); subgraph={'labels':labels,'edges':[list(e) for e in sorted(required)]}
# Recompute the complete rational kernel on only the retained physical labels.
n2=len(labels); jx={v:i for i,v in enumerate(labels)}; rows2=[]
for i in selected:
    row=[0]*n2
    for j,v in enumerate(cycles[i]):row[jx[v]]=(-1)**j
    rows2.append(row)
rows2.append([int(v==C['translation_anchor']) for v in labels]); R,rk=fmpq_mat(rows2).rref()
piv=[next(j for j in range(n2) if R[i,j]) for i in range(rk)]; free2=[j for j in range(n2) if j not in piv]
P2={j:[int(j==h) for h in free2] for j in free2}
for i,j in enumerate(piv):P2[j]=[-R[i,h] for h in free2]
def serialize(x):
    return [int(x.numerator),int(x.denominator)] if hasattr(x,'denominator') else [int(x),1]
cert={k:v for k,v in C.items() if k not in ['source_sha256','cycles','diagonal_obstructions','affine_rank','free_labels','parametrization']}
cert.update({'cycles':[cycles[i] for i in selected],'diagonal_obstructions':{key:C['diagonal_obstructions'][key] for key in sorted(used)},'affine_rank':rk,'free_labels':[labels[j] for j in free2], 'parametrization':[[[j,*serialize(x)] for j,x in enumerate(P2[i]) if x] for i in range(n2)]})
graph_bytes=(json.dumps(subgraph,separators=(',',':'),sort_keys=True)+'\n').encode();(OUT/'graph.json').write_bytes(graph_bytes)
cert['source_sha256']=hashlib.sha256(graph_bytes).hexdigest();(OUT/'certificate.json').write_text(json.dumps(cert,separators=(',',':'),sort_keys=True)+'\n')
words=json.loads((GRAPH.parent/'vertex_deletion_colours.json').read_text())['colourings']
deleted=min(set(V)-set(labels)); word=dict(zip([v for v in V if v!=deleted],words[str(deleted)]))
colour={'source_deleted_vertex':deleted,'colours':[word[v] for v in labels]}
(OUT/'four_colouring.json').write_text(json.dumps(colour,separators=(',',':'),sort_keys=True)+'\n')
eix={tuple(e):i+1 for i,e in enumerate(G['edges'])};clause=sorted(-eix[e] for e in required)
(OUT/'repair_clause.cnf').write_text(f"p cnf {len(G['edges'])} 1\n"+' '.join(map(str,clause))+' 0\n')
provenance={'original_graph_sha256':hashlib.sha256(GRAPH.read_bytes()).hexdigest(),'original_certificate_sha256':hashlib.sha256((SRC/'certificate.json').read_bytes()).hexdigest(),'graph_sha256':hashlib.sha256(graph_bytes).hexdigest(),'certificate_sha256':hashlib.sha256((OUT/'certificate.json').read_bytes()).hexdigest(),'selected_cycle_indices':selected,'selection':'One deterministic reverse-order greedy pass, preserving original 18-edge norm weights.','edge_preimages':'Prefer already retained edges, then lexicographically first available wheel-edge preimage.','source_deleted_vertex_for_four_colouring':deleted}
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'FIXED_NORM_IDENTITY_SUPPORT_EXTRACTED','vertices':len(labels),'edges':len(required),'cycles':len(selected),'diagonals':len(used),'rank':rk,'parameters':len(free2),'seconds':time.monotonic()-start},sort_keys=True))
