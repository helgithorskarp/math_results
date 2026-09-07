"""Bijection between integer intervals and all pair-domain packing survivors."""
from functools import lru_cache
from pathlib import Path
import argparse,json,random
import census,domains,model

@lru_cache(maxsize=1)
def counts():return census.count(domains.certificate())

@lru_cache(maxsize=None)
def positions(left,right,root):return {x:k for k,x in enumerate(domains.root_states(right) if root else domains.states(left,right))}

def unrank(index):
 if type(index) is not int or not 0<=index<counts()['retained_rooted_family']:raise ValueError('index outside complete retained family')
 for row in counts()['branches']:
  if index>=row['count']:index-=row['count'];continue
  packing=model.Packing(row['branch']);matrices=[]
  for i,j in packing.matrix_pairs:
   xs=packing.matrix_domain(i,j);index,k=divmod(index,len(xs));matrices.append(xs[k])
  if index:raise ValueError('mixed-radix overflow')
  return {'branch':row['branch'],'matrices':matrices}
 raise ValueError('missing branch')

def rank(data):
 packing=model.parse(data);index=0;place=1
 for x,(i,j) in zip(data['matrices'],packing.matrix_pairs):
  table=positions(packing.types[i],packing.types[j],i==0);index+=table[x]*place;place*=len(table)
 for row in counts()['branches']:
  if row['branch']==data['branch']:
   if place!=row['count']:raise ValueError('branch cardinality disagreement')
   return index
  index+=row['count']
 raise ValueError('unlisted branch')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--index',type=int);p.add_argument('--seed',type=int);p.add_argument('--data');p.add_argument('--output')
 a=p.parse_args()
 if a.data:print(rank(json.loads(Path(a.data).read_text())))
 else:
  if (a.index is None)==(a.seed is None):p.error('choose exactly one index or seed')
  k=a.index if a.index is not None else random.Random(a.seed).randrange(counts()['retained_rooted_family'])
  data=unrank(k)
  if not a.output:p.error('--output is required when generating')
  out=Path(a.output)
  if out.exists():raise ValueError('output exists')
  out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps({'index':k,'branch':data['branch'],'status':'ROOTED_PACKING_SURVIVOR_ONLY'}))
