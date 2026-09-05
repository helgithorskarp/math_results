from pathlib import Path
from itertools import combinations
from collections import Counter
import geometry as G
import json,time
import argparse
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();w=a.work;w.mkdir(parents=True,exist_ok=False);t=time.perf_counter()
h,d=G.integerize(G.host());he=G.edges(h,d)
assert len(h)==len(set(h))==21 and len(he)==42
u={G.sub(h[i],h[j]) for i,j in he}|{G.sub(h[j],h[i]) for i,j in he};assert len(u)==84
D=sorted({G.sub(x,y) for x in h for y in h});ed=[];p3=[];p7=[];pS3=[]
for i,j in combinations(range(len(D)),2):
 n=G.norm(G.sub(D[i],D[j]))
 if n==G.scale(G.ONE,d*d):ed.append((i,j))
 if n==G.scale(G.ONE,9*d*d):p3.append((i,j))
 if n==G.scale(G.ONE,7*d*d):p7.append((i,j))
 if n==G.scale(G.ONE,3*d*d):pS3.append((i,j))
lookup={p:i for i,p in enumerate(D)};alpha=G.sub(G.scale(G.POW[7],2),G.ONE);triples=[]
for i,j in p7:
 for e in [-1,1]:
  key=G.add(G.add(D[i],D[j]),G.scale(G.mul(alpha,G.sub(D[j],D[i])),e))
  if any(x%2 for x in key):continue
  k=lookup.get(tuple(x//2 for x in key))
  if k is not None and k>j:triples.append((i,j,k))
out={'denominator':d,'host':h,'host_edges':he,'points':D,'edges':ed,'distance3_pairs':p3,'sqrt3_pairs':pS3,'sqrt7_triangles':triples}
(w/'graph.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
summary={'host':len(h),'host_edges':len(he),'directions':len(u),'D':len(D),'D_edges':len(ed),'degree_histogram':dict(sorted(Counter(sum(i in edge for edge in ed) for i in range(len(D))).items())),'distance3_pairs':len(p3),'sqrt3_pairs':len(pS3),'sqrt7_triangles':len(triples),'seconds':time.perf_counter()-t}
(w/'build_result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
