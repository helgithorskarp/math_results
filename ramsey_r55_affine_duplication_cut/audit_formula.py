#!/usr/bin/env python3
"""Independent dense physical projection and truth-functional gate audit."""
import hashlib,itertools,json,sys
from pathlib import Path

def need(x,msg):
 if not x:raise ValueError(msg)
def dot(x,y):return sum(a*b for a,b in zip(x,y))%2

def audit(path,D,mode):
 lines=Path(path).read_text().splitlines();head=lines[0].split();need(head[:2]==['p','cnf'],'header')
 n,number=map(int,head[2:]);cs=[]
 for line in lines[1:]:
  lits=list(map(int,line.split()));need(lits and lits[-1]==0,'clause terminator');c=lits[:-1]
  need(all(1<=abs(x)<=n for x in c) and len(c)==len(set(c)),'clause domain');cs.append(c)
 need(number==len(cs),'count')
 B=list(range(1,16))+list(range(1,16,2));A=list(range(1,16))+list(D)
 bits={x:[int(t) for t in format(x,'04b')] for x in range(16)}
 cross=[[dot(bits[x],bits[y]) for y in B] for x in A]
 pairs={};v=0
 for a in range(23):
  for b in range(a+1,23):v+=1;pairs[a,b]=v
 expected=set()
 for size in (3,4,5):
  for q in itertools.combinations(range(23),size):
   for color in (0,1):
    admitted=size==5
    if size==4:admitted=any(all(row[j]==color for j in q) for row in cross)
    if size==3:
     admitted=any((0 if x==1 else mode)==color and all(cross[x-1][j]==color for j in q) for x in D)
    if admitted:expected.add(frozenset((1-2*color)*pairs[a,b] for a,b in itertools.combinations(q,2)))
 k=next(i for i,c in enumerate(cs) if max(map(abs,c),default=0)>253)
 need(len(expected)==k and set(map(frozenset,cs[:k]))==expected,'every physical projection clause')
 nextvar=253;truths=0;gates=0
 def value(lit,ass):return lit if type(lit) is bool else ass[lit]
 for col in range(23):
  red_cross=sum(row[col] for row in cross);lo=18-red_cross;hi=24-red_cross
  inputs=[pairs[tuple(sorted((row,col)))] for row in range(23) if row!=col]
  old={0:True}
  for i,x in enumerate(inputs,1):
   new={0:True}
   for j in range(1,min(i,hi+1)+1):
    nextvar+=1;s=nextvar;a=old.get(j,False);b=old.get(j-1,False);new[j]=s
    arity=2 if i==1 else 3 if j==1 or j==i else 4
    block=cs[k:k+arity];k+=arity
    local=sorted(set([s,x]+[y for y in (a,b) if type(y) is not bool]))
    need(all(abs(y) in local for c in block for y in c),'threshold local inputs')
    for word in itertools.product((False,True),repeat=len(local)):
     ass=dict(zip(local,word));got=all(any(ass[abs(y)]==(y>0) for y in c) for c in block)
     wanted=ass[s]==(value(a,ass) or ass[x] and value(b,ass))
     need(got==wanted,'exact threshold equivalence');truths+=1
    gates+=1
   old=new
  need(cs[k:k+2]==[[old[lo]],[-old[hi+1]]],'physical degree bounds');k+=2
 need(k==len(cs) and nextvar==n,'no omitted or extra formula')
 return {'status':'COMPLETE_PHYSICAL_PROJECTION_AND_AUXILIARY_AUDIT','D':D,'mode':mode,'clauses':len(cs),'physical_clauses':len(expected),'threshold_gates':gates,'local_gate_truth_assignments':truths,'cnf_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}
if __name__=='__main__':
 p=Path(sys.argv[1]);meta=json.loads((p.parent/'contract.json').read_text())['formula']
 print(json.dumps(audit(p,meta['D'],meta['mode']),sort_keys=True))
