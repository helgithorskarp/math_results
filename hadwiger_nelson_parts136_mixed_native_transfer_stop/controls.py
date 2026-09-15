#!/usr/bin/env python3
import copy,json
from pathlib import Path
import verify
p=Path(__file__).resolve().parent;c=json.loads((p/'certificate.json').read_text())
verify.verify(c)
_,edges,_,bm,_=verify.graph();e=next(e for e in edges if e[0] in bm and e[1] in bm)
cases=[]
b=copy.deepcopy(c);w=list(b['colour4']);w[e[1]]=w[e[0]];b['colour4']=''.join(w);cases.append(('bad_private_B_edge',b))
b=copy.deepcopy(c);b['boundary_word']='1'+b['boundary_word'][1:];cases.append(('wrong_host_projection',b))
b=copy.deepcopy(c);w=list(b['colour5']);w[e[1]]=w[e[0]];b['colour5']=''.join(w);cases.append(('bad_five_word',b))
b=copy.deepcopy(c);b['moser_vertices'][-1]=b['moser_vertices'][0];cases.append(('repeated_lower_bound_vertex',b))
for name,b in cases:
    try:verify.verify(b)
    except ValueError:continue
    raise ValueError('accepted corrupt certificate '+name)
for i,rad in enumerate(verify.RAD):
    v=[0]*16;v[i]=1
    verify.need(verify.norm(v)==(rad,0,0,0,0,0,0,0),'pure radical norm')
v=[0]*16;v[0]=v[9]=48;verify.need(verify.norm(v)==(9216,0,0,0,0,0,0,0),'equilateral unit direction')
print(json.dumps({'valid_certificate_accepted':True,'corruptions_rejected':[name for name,_ in cases],'hand_norm_controls':9},indent=2))
