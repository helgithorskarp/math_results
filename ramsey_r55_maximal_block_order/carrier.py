"""Exact multiset root coordinates and full physical carrier indexing."""
from pathlib import Path
from math import comb,prod
import argparse,json
import dependencies

def multiset_count(m,k):return comb(m+k-1,k)
def unrank_multiset(index,m,k):
 if type(index) is not int or not 0<=index<multiset_count(m,k):raise ValueError('multiset rank')
 # Combinatorial-number-system order on y_i=x_i+i (strictly increasing).
 ys=[];ceiling=m+k-2
 for i in range(k,0,-1):
  lo=i-1;hi=ceiling
  while lo<hi:
   mid=(lo+hi+1)//2
   if comb(mid,i)<=index:lo=mid
   else:hi=mid-1
  ys.append(lo);index-=comb(lo,i);ceiling=lo-1
 ys.reverse();xs=[y-i for i,y in enumerate(ys)]
 return list(reversed(xs))
def rank_multiset(xs,m):
 if not isinstance(xs,list) or any(type(x) is not int or not 0<=x<m for x in xs) or xs!=sorted(xs,reverse=True):raise ValueError('ordered multiset')
 return sum(comb(x+i,i+1) for i,x in enumerate(reversed(xs)))

def count(q,r):
 family=dependencies.load()['family'];family.validate(q,r);a=r-1;b=q-r;n=43-4*q
 return comb(1998+a-1,a)*comb(1931+b-1,b)*37823**(comb(a,2)+comb(b,2))*35714**(a*b)*15**(q*n)

def registry():
 old=dependencies.load()['family'].registry();rows=[];offset=0
 for row in old['classes']:
  q,r=row['q'],row['r'];size=count(q,r);total=size*row['core_stop']
  rows.append(dict(q=q,r=r,n=row['n'],core_start=0,core_stop=row['core_stop'],first_task=row['first_task'].replace('mp1','bo1'),last_task=row['last_task'].replace('mp1','bo1'),per_task=size,code_start=offset,code_stop=offset+total,physical_variables=row['physical_variables'],input_sha256=row['input_sha256']))
  offset+=total
 return dict(format='bo1',macro_classes=18,tasks=old['tasks'],P=offset,parent_N=old['carrier_count'],classes=rows)

def parent_name(name):
 if not isinstance(name,str) or not name.startswith('bo1-'):raise ValueError('bo1 task ID')
 old='mp1-'+name[4:];dependencies.load()['family'].parameters(old);return old

def locate(index):
 reg=registry()
 if type(index) is not int or not 0<=index<reg['P']:raise ValueError('global index')
 for row in reg['classes']:
  if row['code_start']<=index<row['code_stop']:
   core,local=divmod(index-row['code_start'],row['per_task'])
   return f"bo1-q{row['q']}-r{row['r']}-c{core:06d}",local
 raise ValueError('gap')

def global_index(name,local):
 family=dependencies.load()['family'];q,r,c=family.parameters(parent_name(name));row=next(x for x in registry()['classes'] if (x['q'],x['r'])==(q,r))
 if type(local) is not int or not 0<=local<row['per_task']:raise ValueError('local index')
 return row['code_start']+c*row['per_task']+local

class Carrier:
 def __init__(self,name,cache):
  self.name=name;family=dependencies.load()['family'];self.old=family.Task(parent_name(name),cache);self.q=self.old.q;self.r=self.old.r;self.a=self.r-1;self.b=self.q-self.r;self.size=count(self.q,self.r)
  self.rest=[(i,j) for i,j in self.old.pairs if i>0]
 def radices(self):return [multiset_count(1998,self.a),multiset_count(1931,self.b)]+[len(self.old.domain(i,j)) for i,j in self.rest]+[15]*len(self.old.stars)
 def unrank(self,index):
  if type(index) is not int or not 0<=index<self.size:raise ValueError('carrier index')
  digits=[]
  for radix in reversed(self.radices()):index,d=divmod(index,radix);digits.append(d)
  digits.reverse();root=unrank_multiset(digits[0],1998,self.a)+unrank_multiset(digits[1],1931,self.b)
  old_digits=root+digits[2:];old_rank=0
  for d,radix in zip(old_digits,self.old.radices()):old_rank=old_rank*radix+d
  return self.old.unrank(old_rank)
 def rank(self,graph):
  index=self.old.rank(graph);digits=[]
  for radix in reversed(self.old.radices()):index,d=divmod(index,radix);digits.append(d)
  digits.reverse();root=digits[:self.q-1];new=[rank_multiset(root[:self.a],1998),rank_multiset(root[self.a:],1931)]+digits[self.q-1:];answer=0
  for d,radix in zip(new,self.radices()):answer=answer*radix+d
  return answer
 def normalize(self,graph):
  family=dependencies.load()['family'];self.old.rank(graph);a=family.matrix(graph)
  def key(i):return sum(a[u][4*i+v]<<(4*u+v) for u in range(4) for v in range(4))
  blocks=[0]+sorted(range(1,self.r),key=key,reverse=True)+sorted(range(self.r,self.q),key=key,reverse=True)
  permutation=[4*i+j for i in blocks for j in range(4)]+list(range(4*self.q,43))
  out=family.graph([[a[u][v] for v in permutation] for u in permutation]);code=self.rank(out)
  if self.old.closure(out)!=self.old.closure(graph):raise ValueError('closure transport')
  return dict(task=self.name,code=code,graph=out,new_to_old=permutation)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--task');p.add_argument('--code',type=int);p.add_argument('--registry',action='store_true');a=p.parse_args()
 out=registry() if a.registry else dict(status='ORDERED_CARRIER_ONLY_NOT_A_TARGET',graph=Carrier(a.task,a.cache).unrank(a.code))
 print(json.dumps(out,indent=2))
