"""Fresh prefix-product audit. Defining mathematics visible; no target imports.
Local rows credited to this reviewer's previous sealed physical census.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,time
from rows import census,need,encoded

FIELDS=('e','k','q','eligible','colors','psi','margin')
def project(rows):
 out=[]
 for r in rows:
  sat=set(r['high'])-set(r['hubs'])
  colors=[sum(5-r['replication'][v]==a for v in sat)for a in range(1,6)]
  need(sum(colors)==r['h']-r['k'],'physical degree')
  need(sum((a-1)*x for a,x in enumerate(colors,1))==r['sigma'],'physical excess')
  out.append({**r,'colors':colors})
 return out

def types_of(rows):
 return sorted({(r['e'],r['k'],r['q'],r['eligible'],tuple(r['colors']),r['psi'],r['margin3'])for r in rows if r['k']<=4})

def weights(t):
 return (1,t[0],t[1],t[2],sum((a-1)*v for a,v in enumerate(t[4],1)),t[6])

def prefix_product(types,E,K,Q,X,budget):
 """Multiply uniform bounded local generating factors, retaining exact coefficients.
 Forward prefix tables followed by subtraction recover EVERY count vector.
 No special q split, prescribed unit types, or solved unit completion.
 """
 cap=(14,E,K,Q,2*X,budget)
 ids=[i for i,t in enumerate(types)if all(0<=v<=c for v,c in zip(weights(t),cap))]
 wt=[weights(types[i])for i in ids]
 suffix=[]
 for j in range(len(wt)+1):
  rem=wt[j:]
  suffix.append(([min(w[c]for w in rem)for c in range(1,6)],
                 [max(w[c]for w in rem)for c in range(1,6)])if rem else None)
 tables=[{(0,0,0,0,0,0):1}];updates=0;start=time.monotonic()
 for j,w in enumerate(wt):
  new={}
  for state,multiplicity in tables[-1].items():
   for c in range(15-state[0]):
    key=tuple(v+c*a for v,a in zip(state,w))
    if any(v>limit for v,limit in zip(key,cap)):break
    remaining=14-key[0]
    if j+1<len(wt):
     lo,hi=suffix[j+1]
     if any(not remaining*lo[d-1]<=cap[d]-key[d]<=remaining*hi[d-1]for d in range(1,5)):continue
     if remaining*lo[4]>cap[5]-key[5]:continue
    elif key[:5]!=cap[:5]:continue
    new[key]=new.get(key,0)+multiplicity;updates+=1
    need(updates<=500000,'incomplete prefix enumeration: fixed500000-update guard')
    need(time.monotonic()-start<=20,'incomplete prefix enumeration: fixed20-second branch guard')
  tables.append(new)
 vectors=[]
 def recover(j,key,counts):
  if j==0:
   need(key==(0,0,0,0,0,0),'prefix recovery base')
   full=[0]*len(types)
   for i,c in zip(ids,reversed(counts)):full[i]=c
   vectors.append(full);return
  w=wt[j-1]
  for c in range(key[0]+1):
   prev=tuple(v-c*a for v,a in zip(key,w))
   if prev in tables[j-1]:recover(j-1,prev,counts+[c])
 for key,multiplicity in sorted(tables[-1].items()):
  if key[:5]==cap[:5]:
   before=len(vectors);recover(len(wt),key,[])
   need(len(vectors)-before==multiplicity,'full coefficient/recovery agreement')
 return sorted(vectors),{'updates':updates,'peak_states':max(map(len,tables)),'active_types':len(ids)}

def endpoints(types,counts,use_radius=True):
 vertices=[i for i,c in enumerate(counts)for _ in range(c)]
 for a in range(5):
  if sum(types[i][4][a]for i in vertices)%2:return {'reason':'odd-color','color':a+1}
 for s,i in enumerate(vertices):
  row=types[i];radius=0
  for a,wanted in enumerate(row[4]):
   allowed=[v for v,j in enumerate(vertices)if v!=s and types[j][4][a]>0
       and not((row[0]==0 and types[j][3])or(types[j][0]==0 and row[3]))]
   if len(allowed)<wanted:return {'reason':'distinct-endpoints','row':i,'color':a+1,'required':wanted,'available':len(allowed)}
   radius+=sum(sorted((sum(types[vertices[v]][4])for v in allowed),reverse=True)[:wanted])
  if use_radius and row[1]==0 and radius<13:return {'reason':'radius-two','row':i,'upper_sum_degrees':radius,'needed':13}
 return None
