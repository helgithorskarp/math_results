"""Exact covering counts from ordered independent triple partitions; no quotient."""
from functools import lru_cache
from itertools import combinations,permutations
from pathlib import Path
import json,hashlib,time
HERE=Path(__file__).resolve().parent

def graph6(line):
 if not isinstance(line,str) or not line or any(ord(c)<63 or ord(c)>126 for c in line):raise ValueError('graph6 alphabet')
 n=ord(line[0])-63
 if n not in (3,6,9,12):raise ValueError('catalog graph order')
 stream=''.join(format(ord(c)-63,'06b') for c in line[1:]);m=n*(n-1)//2
 if len(stream)!=(m+5)//6*6 or any(c!='0' for c in stream[m:]):raise ValueError('graph6 length/padding')
 rows=[0]*n
 for bit,(i,j) in zip(stream,((i,j) for j in range(1,n) for i in range(j))):
  if bit=='1':rows[i]|=1<<j;rows[j]|=1<<i
 return rows

class PartitionCover:
 def __init__(self,rows):
  self.rows=rows;self.n=len(rows);self.k=self.n//3-1;self.full=(1<<self.n)-1
  self.triples=sorted(sum(1<<v for v in q) for q in combinations(range(self.n),3) if self.edge_count(sum(1<<v for v in q))==0)
  self.counts=lru_cache(None)(self._counts)
 def edge_count(self,mask):return sum((row&mask).bit_count() for v,row in enumerate(self.rows) if mask>>v&1)//2
 def _counts(self,mask):
  if mask.bit_count()==3:
   edges=self.edge_count(mask);return tuple(int(t==edges) for t in range(4))
  totals=[0]*4
  for triple in self.triples:
   if triple&mask==triple:
    for t,count in enumerate(self.counts(mask^triple)):totals[t]+=count
  return tuple(totals)
 def unrank_partition(self,t,index):
  if type(t) is not int or t not in range(4) or type(index) is not int or not 0<=index<self.counts(self.full)[t]:raise ValueError('partition code')
  mask=self.full;blocks=[]
  while mask.bit_count()>3:
   for triple in self.triples:
    if triple&mask!=triple:continue
    size=self.counts(mask^triple)[t]
    if index<size:blocks.append(triple);mask^=triple;break
    index-=size
   else:raise ValueError('partition decoding')
  return blocks+[mask]
 def rank_partition(self,t,blocks):
  if len(blocks)!=self.k+1:raise ValueError('partition block count')
  mask=self.full;index=0
  for chosen in blocks[:-1]:
   if chosen not in self.triples or chosen&mask!=chosen:raise ValueError('nonindependent or overlapping block')
   for triple in self.triples:
    if triple>=chosen:break
    if triple&mask==triple:index+=self.counts(mask^triple)[t]
   mask^=chosen
  if mask!=blocks[-1] or self.edge_count(mask)!=t:raise ValueError('last shape')
  return index
 def embeddings(self,t):return self.counts(self.full)[t]*6**self.k*(6 if t in (0,3) else 2)
 def unrank_embedding(self,t,index):
  width=6**self.k*(6 if t in (0,3) else 2)
  if type(index) is not int or not 0<=index<self.embeddings(t):raise ValueError('embedding code')
  pindex,local=divmod(index,width);blocks=self.unrank_partition(t,pindex);order=[]
  for mask in blocks[:-1]:
   local,digit=divmod(local,6);vertices=[v for v in range(self.n) if mask>>v&1];order.extend(list(permutations(vertices))[digit])
  last=[v for v in range(self.n) if blocks[-1]>>v&1];wanted=(0,1,3,7)[t]
  options=[p for p in permutations(last) if sum(((self.rows[p[i]]>>p[j])&1)<<k for k,(i,j) in enumerate(combinations(range(3),2)))==wanted]
  if len(options)!=(6 if t in (0,3) else 2) or local>=len(options):raise ValueError('local transport')
  return order+list(options[local])
 def rank_embedding(self,t,order):
  if not isinstance(order,list) or any(type(v) is not int for v in order) or sorted(order)!=list(range(self.n)):raise ValueError('vertex bijection')
  blocks=[sum(1<<v for v in order[i:i+3]) for i in range(0,self.n,3)];partition=self.rank_partition(t,blocks);local=0
  for j,mask in enumerate(blocks[:-1]):
   vertices=[v for v in range(self.n) if mask>>v&1]
   local+=6**j*list(permutations(vertices)).index(tuple(order[3*j:3*j+3]))
  last=sorted(order[-3:]);wanted=(0,1,3,7)[t]
  options=[p for p in permutations(last) if sum(((self.rows[p[i]]>>p[j])&1)<<k for k,(i,j) in enumerate(combinations(range(3),2)))==wanted]
  if tuple(order[-3:]) not in options:raise ValueError('last triple transport')
  local+=6**self.k*options.index(tuple(order[-3:]))
  return partition*6**self.k*len(options)+local

def census():
 result=[]
 for n,wanted in [(6,32),(9,290),(12,12)]:
  data=(HERE/f'r35_{n}.g6').read_bytes();lines=data.decode().splitlines()
  if len(lines)!=wanted:raise ValueError('catalog cardinality')
  entries=[]
  for i,line in enumerate(lines):
   cover=PartitionCover(graph6(line))
   if cover.n!=n:raise ValueError('wrong catalog order')
   entries.append({'index':i,'graph6':line,'independent_triples':len(cover.triples),'partitions_by_last_red_edges':list(cover.counts(cover.full)),'embedding_covers_by_last_red_edges':[cover.embeddings(t) for t in range(4)]})
  totals=[sum(x['embedding_covers_by_last_red_edges'][t] for x in entries) for t in range(4)]
  result.append({'n':n,'catalog_sha256':hashlib.sha256(data).hexdigest(),'graphs':len(entries),'entries':entries,'embedding_cover_totals':totals})
 return {'status':'EXACT_CATALOG_EMBEDDING_COVER_COUNTS','no_automorphism_quotient':True,'physical_duplicates_allowed':True,'catalogs':result}

if __name__=='__main__':
 start=time.monotonic();d=census();(HERE/'TAIL_COVERS.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'seconds':time.monotonic()-start,'totals':[(c['n'],c['embedding_cover_totals']) for c in d['catalogs']]}))
