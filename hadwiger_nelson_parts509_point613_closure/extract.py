#!/usr/bin/env python3
"""Extract the compact certificate from the pinned native trace.

The extractor is not trusted: verify its output with VeriPB.
"""
from pathlib import Path
import argparse
from hashlib import sha256
import json

ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
raw=args.input.read_bytes()
if sha256(raw).hexdigest()!='79a0ee677663e2ed78dde76df5704c729fc1995bf7c6aa7b8518ffcdf1f12810':raise ValueError('not the recorded native trace')
lines=raw.decode('ascii').splitlines()
assert lines[:2]==['pseudo-Boolean proof version 2.0','f 341']
nodes=[];owner={};current=342;block=[];depth=0

def references(line,ident):
    tokens=line.split();kind=tokens[0]
    refs=[]
    if kind in ('p','pol'):
        for i,t in enumerate(tokens[1:],1):
            if t.lstrip('-').isdigit() and (i+1==len(tokens) or tokens[i+1] not in ['*','d']):
                v=int(t);refs.append(v if v>0 else ident+v)
    elif kind=='rup':
        refs=[int(x) for x in line.split(';')[1].split()]
    elif kind=='end':refs=[ident+int(tokens[1]) if int(tokens[1])<0 else int(tokens[1])]
    elif kind!='red':raise ValueError(kind)
    return refs

for line in lines[2:]:
    kind=line.split()[0]
    if kind in ['output','conclusion']:break
    assert kind in ['rup','p','pol','red','end']
    block.append((current,line,references(line,current)))
    owner[current]=len(nodes);current+=1
    if kind=='red':depth+=1
    if kind=='end':depth-=1
    if depth==0:nodes.append(block);block=[]
assert not block and current-1==1459
keep=set();pending=[owner[1459]]
while pending:
    i=pending.pop()
    if i in keep:continue
    keep.add(i)
    for ident,line,refs in nodes[i]:
        for r in refs:
            if r>341 and owner[r]!=i:pending.append(owner[r])
mapping={i:i for i in range(1,341)};new=341
for i,node in enumerate(nodes):
    if i in keep:
        for ident,line,refs in node:mapping[ident]=new;new+=1
out=['pseudo-Boolean proof version 2.0','f 340']
for i,node in enumerate(nodes):
    if i not in keep:continue
    for ident,line,refs in node:
        tokens=line.split();kind=tokens[0]
        if kind in ['p','pol']:
            for j,t in enumerate(tokens[1:],1):
                if t.lstrip('-').isdigit() and (j+1==len(tokens) or tokens[j+1] not in ['*','d']):
                    r=int(t);r=r if r>0 else ident+r;tokens[j]=str(mapping[r])
            line=' '.join(tokens)
        elif kind=='rup':line=line.split(';')[0]+'; '+' '.join(str(mapping[r]) for r in refs)
        elif kind=='end':line='end '+str(mapping[refs[0]])
        out.append(line)
out+=['output NONE','conclusion UNSAT : '+str(mapping[1459]),'end pseudo-Boolean proof']
args.output.write_text('\n'.join(line.rstrip() for line in out)+'\n')
print(json.dumps({'blocks':len(nodes),'retained_blocks':len(keep),'original_ids':1118,'retained_ids':new-341,'proof_bytes':args.output.stat().st_size},indent=2))
