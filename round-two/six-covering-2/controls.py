"""Definition-level positive-cover and malformed-certificate controls."""
from copy import deepcopy
import json
from pathlib import Path
from check import capacities,check_tree,divisors,transport

HERE=Path(__file__).resolve().parent
A=((8,0),(9,0),(10,1),(14,1),(12,3))
expected={0:[0,8],1:[1,5,9,13],2:[2,6,10,14],3:[3,7,11,15],4:[4,12]}
actual={b:[a for a in range(16) if transport(10080,A,16,a,b) is not None] for b in expected}
if actual!=expected:raise ValueError('Wrong whole-phase classification')

cover=((2,1),(4,2),(3,0),(6,4),(12,8));positive=0
if any(not any(x%m==a for m,a in cover) for x in range(12)):raise ValueError('Invalid known cover')
for length in range(len(cover)):
    prefix=cover[:length];B=[m for m in divisors(12) if m>=2 and m not in dict(prefix)]
    W=[(1+x%5) if all(x%m!=a for m,a in prefix) else 0 for x in range(12)]
    groups=[]
    if len(B)>=3:
        a,b,c=B[:3];groups=[[[a,b],1],[[a,c],1],[[b,c],1]]
    cap2,*_=capacities(W,B,groups)
    if cap2<2*sum(W):raise ValueError('A genuine cover was incorrectly excluded')
    positive+=1

good=json.loads((HERE/'odd-cycle.json').read_text());check_tree(good)
bad=[]
x=deepcopy(good);x['complete']=False;bad.append(x)
x=deepcopy(good);x['nodes'][0]['type']='open';bad.append(x)
x=deepcopy(good);x['vectors'][0]['gap2']+=1;bad.append(x)
x=deepcopy(good);x['vectors'][0]['boxes'][0][-1]=0;bad.append(x)
x=deepcopy(good);x['vectors'][0]['boxes'][0][0]=0;bad.append(x)
x=deepcopy(good);x['vectors'][0]['boxes'][0][0]=1<<32;bad.append(x)
x=deepcopy(good);x['vectors'][0]['boxes'].append(x['vectors'][0]['boxes'][0]);bad.append(x)
x=deepcopy(good);x['vectors'][0]['boxes'].append([1,1,1,1,1]);bad.append(x)
x=deepcopy(good);x['vectors'][0]['pairs2'][0][1]=3;bad.append(x)
x=deepcopy(good);x['vectors'][0]['pairs2'].append(x['vectors'][0]['pairs2'][0]);bad.append(x)
x=deepcopy(good);x['vectors'][0]['pairs2'][0][0]=[8,20];bad.append(x)
x=deepcopy(good);x['vectors'][0]['pairs2'][0][1]=1.5;bad.append(x)
x=deepcopy(good);x['nodes'].append(x['nodes'][0]);bad.append(x)
x=deepcopy(good);x['root_anchors'].append(x['root_anchors'][0]);bad.append(x)
rejected=0
for fixture in bad:
    try:check_tree(fixture)
    except (ValueError,TypeError,IndexError,KeyError):rejected+=1
    else:raise ValueError('A damaged certificate was accepted')
print(json.dumps({'phase_classes':actual,'genuine_cover_prefixes':positive,'malformed_rejected':rejected},sort_keys=True))
