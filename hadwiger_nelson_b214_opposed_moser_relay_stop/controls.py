"""Author-side comparison and semantic controls; not independent peer review."""
from pathlib import Path
from itertools import combinations
import copy,json,hashlib
import verify as v
p=Path(__file__).resolve().parent
pts,edges,maps,norms=v.build(p)
# Independently specialized complex-coordinate norm, compared entry by entry.
rows=[]
for z in pts:
    v.need(z[1]==z[2]==z[4]==z[7]==0,'E coordinate layout')
    rows.append((z[0],z[3],z[5],z[6]))
other=[];ee=[]
for i,j in combinations(range(len(rows)),2):
    a,b,c,d=(x-y for x,y in zip(rows[i],rows[j]));n=(a*a+33*b*b+3*c*c+11*d*d,0,0,2*(a*b+c*d))
    other.append([i,j,*n])
    if n==(144,0,0,0):ee.append([i,j])
v.need(other==norms and ee==edges,'entrywise geometry mismatch')
cert=json.loads((p/'certificate.json').read_text());v.verify(p,cert)
wrong=[]
x=copy.deepcopy(cert);s=list(x['proper4_different_centres']);s[edges[0][1]]=s[edges[0][0]];x['proper4_different_centres']=''.join(s);wrong.append(x)
x=copy.deepcopy(cert);s=list(x['proper4_equal_centres']);s[216]=str((int(s[89])+1)%4);x['proper4_equal_centres']=''.join(s);wrong.append(x)
x=copy.deepcopy(cert);x['proper4_different_centres']=x['proper4_equal_centres'];wrong.append(x)
x=copy.deepcopy(cert);x['source214_sha256']='0'*64;wrong.append(x)
for x in wrong:
    try:v.verify(p,x)
    except ValueError:continue
    raise ValueError('bad certificate accepted')
print(json.dumps({'all_pair_norms_compared':len(norms),'entrywise_match':True,'semantic_corruptions_rejected':len(wrong),'no_solver':True},sort_keys=True))
