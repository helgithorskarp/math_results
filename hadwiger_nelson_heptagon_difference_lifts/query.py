#!/usr/bin/env python3
"""Recreate the two bounded native pilot inputs. No SAT status is inferred here."""
from pathlib import Path
from itertools import combinations
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--encoding',choices=['onehot','alo'],required=True);a=p.parse_args()
x=json.loads((a.work/'graph.json').read_text());n=len(x['points']);edges=x['edges'];left,right=x['sqrt3_pairs'][0];v=lambda i,c:4*i+c+1
if a.encoding=='onehot':
 clauses=[]
 for i in range(n):
  clauses.append([v(i,c) for c in range(4)])
  for c,d in combinations(range(4),2):clauses.append([-v(i,c),-v(i,d)])
 clauses += [[-v(i,c),-v(j,c)] for i,j in edges for c in range(4)]
 # The two unit rows are assumptions in the original incremental call.
 clauses += [[v(left,0)],[v(right,0)]];triangle=None
else:
 adj=[set() for _ in range(n)]
 for i,j in edges:adj[i].add(j);adj[j].add(i)
 triangle=next((left,i,j) for i in sorted(adj[left]) for j in sorted(adj[left]&adj[i]) if i<j)
 clauses=[[v(i,c) for c in range(4)] for i in range(n)]+[[-v(i,c),-v(j,c)] for i,j in edges for c in range(4)]+[[v(left,0)],[v(right,0)],[v(triangle[1],1)],[v(triangle[2],2)]]
text=f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
with a.output.open('x') as f:f.write(text)
print(json.dumps({'encoding':a.encoding,'vertices':n,'pair':[left,right],'triangle':triangle,'variables':4*n,'clauses':len(clauses),'sha256':hashlib.sha256(text.encode()).hexdigest(),'signature_status':'NOT DECIDED'},indent=2))
