from pathlib import Path
import json,itertools
import argparse
W=Path(__file__).resolve().parent

def profiles(n):
 def rec(w):
  if len(w)==n:yield tuple(w);return
  for c in range(min(3,max(w,default=-1)+1)+1):yield from rec(w+[c])
 yield from rec([])

def extension(n,edges,masks,w):
 adj=[set()for _ in range(n)];dom=[set(range(4))for _ in range(n)]
 for i,j in edges:adj[i].add(j);adj[j].add(i)
 for m,c in zip(masks,w):
  for j in range(n):
   if m>>j&1:dom[j].discard(c)
 cc=[-1]*n
 def rec():
  left=[j for j in range(n)if cc[j]<0]
  if not left:return ''.join(map(str,cc))
  choices={j:dom[j]-{cc[i]for i in adj[j]}for j in left}
  j=min(left,key=lambda j:(len(choices[j]),-len(adj[j]),j))
  for c in sorted(choices[j]):
   cc[j]=c;z=rec()
   if z is not None:return z
  cc[j]=-1;return None
 return rec()

def templates(g):
 out={}
 for v in g['outside_groups']:
  old=sorted({r for r,j in v['cross']});masks=tuple(sorted(sum(1<<(j-1)for r0,j in v['cross']if r0==r)for r in old));edges=tuple(sorted((i-1,j-1)for i,j in v['inside']));out[(edges,masks)]=None
 return sorted(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--work',required=True,type=Path);args=ap.parse_args();out={}
 for name,sub,n in [('M','',6),('G','golomb',9)]:
  g=json.loads((args.work/(name+'_census.json')).read_text());tt=[]
  for edges,masks in templates(g):
   words=[]
   for w in profiles(len(masks)):
    c=extension(n,edges,masks,w)
    if c is None:raise ValueError('no extension')
    words.append(c)
   tt.append({'new_vertices':n,'new_edges':edges,'old_neighbour_masks':masks,'words':words})
  out[name]=tt;print(name,'templates',len(tt),'words',sum(len(x['words'])for x in tt),'labelled',sum(4**len(x['old_neighbour_masks'])for x in tt))
 (args.work/'certificate.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
