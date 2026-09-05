#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations
import argparse,json
import geometry as G
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();x=json.loads((a.work/'graph.json').read_text())
assert G.POW[0]==G.ONE and G.mul(G.POW[1],G.POW[41])==G.ONE
for d in [1,2,3,6,7,14,21]:assert G.POW[d]!=G.ONE
for n in range(42):assert G.norm(G.POW[n])==G.ONE and G.conj(G.POW[n])==G.POW[-n%42]
for value in [G.ONE,G.add(G.ONE,G.POW[1]),G.sub(G.POW[6],G.POW[36])]:assert G.mul(value,G.inv(value))==G.ONE
try:G.inv(G.ZERO)
except ZeroDivisionError:pass
else:raise AssertionError('zero inverse accepted')
# Tiny explicit non-lift colouring. This is a control for the restricted scope,
# not a claim of a non-lift colouring of the421-point graph.
S=[G.ZERO,G.ONE,G.POW[7]];tiny=sorted({G.sub(a,b) for a in S for b in S});edges=G.edges(tiny,1);idx={p:i for i,p in enumerate(tiny)}
assert len(tiny)==7 and len(edges)==12
col=[0]*7
for k,c in enumerate([1,2,1,2,1,3]):col[idx[G.POW[7*k]]]=c
assert all(col[i]!=col[j] for i,j in edges)
assert col[idx[G.ONE]]!=col[idx[G.POW[21]]]
# Every potential lift is antipodally symmetric, so the preceding row cannot be one.
H=list(map(tuple,x['host']));D=list(map(tuple,x['points']));lookup={p:i for i,p in enumerate(D)};potential=json.loads((Path(__file__).resolve().parent/'potentials.json').read_text())[0];color=[0]*421
for i,j in combinations(range(21),2):
 color[lookup[G.sub(H[i],H[j])]]=color[lookup[G.sub(H[j],H[i])]]=potential[i]^potential[j]
def check(c):
 if len(c)!=421 or any(a not in range(4) for a in c) or any(c[i]==c[j] for i,j in x['edges']):raise ValueError('not a proper four-colouring')
check(color);i,j=x['edges'][0];bad=color.copy();bad[j]=bad[i]
rejections=0
for c in [bad,color[:-1],[4]+color[1:]]:
 try:check(c)
 except ValueError:rejections+=1
 else:raise AssertionError('corruption accepted')
result={'exact_unit_roots_checked':42,'proper_divisors_excluded':7,'nonzero_inverse_controls':3,'zero_inverse_rejected':True,'tiny_nonlift_control':{'vertices':7,'edges':12},'corrupt_colourings_rejected':rejections}
(a.work/'controls_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
