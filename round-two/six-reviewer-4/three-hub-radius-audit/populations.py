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
 return sorted({(r['e'],r['k'],r['q'],r['eligible'],tuple(r['colors']),r['psi'],r['margin3'])for r in rows if r['k']<=3})

def weights(t):
 return (1,t[0],t[1],t[2],sum((a-1)*v for a,v in enumerate(t[4],1)),t[6])

def prefix_product(types,E,K,Q,X,budget):
 """Multiply uniform bounded local generating factors, retaining exact coefficients.
 Forward prefix tables followed by subtraction recover EVERY count vector.
 No special q split, prescribed unit types, or solved unit completion.
 """
 cap=(15,E,K,Q,2*X,budget)
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
   for c in range(16-state[0]):
    key=tuple(v+c*a for v,a in zip(state,w))
    if any(v>limit for v,limit in zip(key,cap)):break
    remaining=15-key[0]
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
  if use_radius and row[1]==0 and radius<14:return {'reason':'radius-two','row':i,'upper_sum_degrees':radius,'needed':14}
 return None

def run(stars):
 physical=project(census(stars));types=types_of(physical)
 need(len(physical)==426 and len(types)==56,'complete carriers')
 branches=[]
 for Q in range(6):
  for T in range(2):
   for X in range(3):
    for tau in range(2):
     slack=5-2*T-2*X-4*tau-Q
     if slack<0:continue
     E=15-T-2*tau-Q;K=25-E+2*X
     vectors,cost=prefix_product(types,E,K,Q,X,3*slack)
     records=[]
     for v in vectors:
      # All original equalities rechecked independently from the recovered vector.
      got=[sum(c*w[d]for c,t in zip(v,types)for w in [weights(t)])for d in range(6)]
      need(got[:5]==[15,E,K,Q,2*X]and got[5]<=3*slack,'recovered complete budget')
      need(sum(c*t[5]for c,t in zip(v,types))<=0,'selector capacity budget')
      records.append({'counts':v,'old_failure':endpoints(types,v,False),'failure':endpoints(types,v)})
     branches.append({'Q':Q,'T':T,'X':X,'tau':tau,'E':E,'K':K,'margin_budget':3*slack,'records':records,'enumeration':cost})
 need(len(branches)==20,'all admissible branch coverage')
 survivors=[(b,r)for b in branches for r in b['records']if r['failure']is None]
 need(len(survivors)==1,'complete necessary survivor count')
 b,r=survivors[0]
 need((b['Q'],b['T'],b['X'],b['tau'])==(5,0,0,0),'final actual branch')
 support=[{'type':list(types[i][:4])+[list(types[i][4]),*types[i][5:]],'count':c}for i,c in enumerate(r['counts'])if c]
 need(sorted((v['count'],*v['type'][:4],tuple(v['type'][4]))for v in support)==[(5,0,1,1,False,(4,0,0,0,0)),(10,1,1,0,True,(3,0,0,0,0))],'final physical population hypotheses')
 return {'physical':physical,'types':[list(t[:4])+[list(t[4]),*t[5:]]for t in types],'branches':branches,'final_support':support}

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 z=run(json.loads(a.input.read_bytes())['stars']);a.out.write_bytes(encoded(z))
 print(json.dumps({'rows':len(z['physical']),'types':len(z['types']),'branches':len(z['branches']),
 'populations':sum(len(b['records'])for b in z['branches']),'raw_by_branch':[[b[k]for k in ('Q','T','X','tau')]+[len(b['records'])]for b in z['branches']],
 'survivors':sum(r['failure']is None for b in z['branches']for r in b['records']),
 'bytes':a.out.stat().st_size,'sha256':hashlib.sha256(a.out.read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
