"""Certificate proof of chi=4, including complete exact unit-edge census."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import json,time
from native_geometry import candidates
from reference_geometry import squared_norm,RAD
ROOT=Path(__file__).resolve().parent

def require(ok,message):
 if not ok:raise ValueError(message)

def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def word_check(word,n,edges):
 require(type(word) is str and len(word)==n and all(c in '0123' for c in word),'Malformed colour word')
 require(all(word[a]!=word[b] for a,b in edges),'Monochromatic unit edge')

def spindle(points,edges):
 # Physical coordinates multiplied by12 in the declared radical basis.
 rows=[]
 for data in ({},{0:12},{0:6,10:6},{0:18,10:6},
              {0:10,12:2},{0:5,6:-1,10:5,12:1},{0:15,6:-1,10:5,12:3}):
  rows.append(tuple(data.get(i,0) for i in range(16)))
 idx={tuple(p):i for i,p in enumerate(points)}
 require(all(p in idx for p in rows),'Missing spindle vertex')
 labels=[idx[p] for p in rows]
 required=[(0,1),(0,2),(1,2),(1,3),(2,3),(0,4),(0,5),(4,5),(4,6),(5,6),(3,6)]
 E=set(map(tuple,edges))
 require(all(tuple(sorted((labels[a],labels[b]))) in E for a,b in required),'Missing spindle edge')
 return labels

def main():
 t=time.monotonic();g=json.loads((ROOT/'out/instance.json').read_text());ps=g['points'];n=len(ps)
 require(g['denominator']==12 and g['radicands']==RAD,'Bad coordinate convention')
 require(all(len(p)==16 and all(type(v) is int for v in p) for p in ps),'Bad point')
 require(len(set(map(tuple,ps)))==n,'Repeated point')
 require(digest(ps)=='ea5f06b01aebb6969de55b9e5a0ed0552d5beae4792bdddee4149d50b5a33c12','Unexpected point set or order')
 near=candidates(ps);es=[]
 for a,b in near:
  if squared_norm([x-y for x,y in zip(ps[a],ps[b])])==[144,0,0,0,0,0,0,0]:es.append([a,b])
 require(es==g['edges'],'Producer edges are not all exact unit pairs')
 require(digest(es)=='c8195c893c8a0d1f4e4bf44fd9ce8e0b68ed9569e5ab360d3568cc85d9d79450','Unexpected edges')
 lines=(ROOT/'colouring.txt').read_text().splitlines();require(len(lines)==1,'Expected one colour word')
 word=lines[0];word_check(word,n,es);labels=spindle(ps,es)
 out={'vertices':n,'unit_edges':len(es),'chromatic_number':4,'all_subgraphs_four_colourable':True,
      'point_sha256':digest(ps),'edge_sha256':digest(es),
      'colouring_sha256':sha256(word.encode()).hexdigest(),'spindle_labels':labels,
      'all_point_pairs':n*(n-1)//2,'interval_candidates':len(near),'false_interval_candidates':len(near)-len(es)}
 print('verified in',time.monotonic()-t,'seconds',flush=True,file=__import__('sys').stderr)
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
