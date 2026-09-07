"""Exact mixed palette, complete declared finite support and discovery edges."""
from pathlib import Path
from collections import Counter
import json,time
from build import palette,add,PZERO,unit_edges,norm,RAD
from reference_geometry import interval,Q,square_bounds
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'out'

def main():
 t=time.monotonic();A,B=palette();U=sorted(set(A+B));U0=U+[PZERO]
 P2=sorted({add(p,q) for p in U0 for q in U0});P2set=set(P2)
 count=Counter(add(p,u) for p in P2 for u in U)
 C8=P2set|{p for p,c in count.items() if c>=8};clip=[]
 for p in P2:
  a,b=interval(p[:8]);c,d=interval(p[8:]);xl,xh=square_bounds(a,b);yl,yh=square_bounds(c,d)
  if xh+yh<(12*Q)**2:clip.append(p)
  elif xl+yl<=(12*Q)**2:
   if norm(p)!=(144,0,0,0,0,0,0,0):raise ValueError('Unresolved clipping')
   clip.append(p)
 M3=sorted({add(p,u) for p in clip for u in U0});M3set=set(M3)
 ps=M3+sorted(C8-M3set);ix={p:i for i,p in enumerate(ps)};es=unit_edges(ps,U)
 P2ids={ix[p] for p in P2};C8ids={ix[p] for p in C8}
 counts={'P2':[len(P2),sum(a in P2ids and b in P2ids for a,b in es)],
         'C8':[len(C8),sum(a in C8ids and b in C8ids for a,b in es)],
         'M3':[len(M3),sum(a<len(M3) and b<len(M3) for a,b in es)],
         'union':[len(ps),len(es)]}
 out={'denominator':12,'radicands':RAD,'points':ps,'edges':es,'directions':U,
      'counts':counts,'clip_vertices':len(clip),'palette_sizes':[len(A),len(B),len(set(A)&set(B)),len(U)],
      'label_order':'lexicographic M3 then lexicographic C8 minus M3',
      'edge_scope':'declared96 unit directions; independent verifier checks all unit pairs'}
 OUT.mkdir(exist_ok=True);(OUT/'instance.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 print(json.dumps({'counts':counts,'clip_vertices':len(clip),'seconds':time.monotonic()-t},sort_keys=True))
if __name__=='__main__':main()
