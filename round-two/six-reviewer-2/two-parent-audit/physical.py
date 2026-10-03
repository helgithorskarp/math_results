"""Reviewer six-reviewer-2: whole literal original-phase and BASE census.

Exact bitmaps of actual n+2520*k incidences; all phases and omissions preserved.
"""
from itertools import product
import hashlib,json,struct
PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
def need(ok,why):
 if not ok:raise ValueError(why)
def wire(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def compute(outdir=None,span=None):
 R=tuple(x for x in range(2520)if all(x%m!=a for m,a in PREFIX))
 parents={r:tuple(n for n in R if n%8==r)for r in (2,6,4)}
 scenarios=((2,(80,144,240),((16,2),),72),(6,(48,96),((32,6),),90),(4,(112,336),(),15))
 phases=[];goods={}
 for r,ms,fixed,cut in scenarios:
  pts=parents[r];ones=(1<<len(pts))-1
  def planes(m,a):return tuple(sum(1<<i for i,n in enumerate(pts)if (n+2520*k)%m==a)for k in range(4))
  mark=[0]*4
  for m,a in fixed:
   for k,v in enumerate(planes(m,a)):mark[k]|=v
  raw={m:{a:planes(m,a)for a in range(r,m,8)}for m in ms};rows=[];values=[];good=[]
  for aa in product(*(range(r,m,8)for m in ms)):
   zz=mark.copy()
   for m,a in zip(ms,aa):
    for k,v in enumerate(raw[m][a]):zz[k]|=v
   hit=ones
   for v in zz:hit&=v
   value=hit.bit_count();values.append(value)
   repaired=[n for i,n in enumerate(pts)if hit>>i&1]
   rows.append([list(aa),value,repaired])
   if value>=cut:good.append([list(aa),repaired])
  packet=struct.pack('<'+'H'*len(values),*values)
  if outdir:(outdir/('phases-'+str(r)+'.bin')).write_bytes(packet)
  phases.append(dict(parent=r,moduli=list(ms),threshold=cut,all_rows=rows,qualifying=good,count=len(rows),maximum=max(values),values_sha256=hashlib.sha256(packet).hexdigest()))
  goods[r]=good
 completions=[]
 for a,b,c in product(goods[2],goods[6],goods[4]):
  s=sorted(a[1]+b[1]+c[1]);completions.append([a[0]+b[0]+c[0],s])
 shapes=sorted({tuple(v[1])for v in completions});labels=tuple(m for m in range(8,2521)if 2520%m==0 and m not in {m for m,a in PREFIX})
 base={m:[0]*m for m in labels}
 for m in labels:
  for n in R:base[m][n%m]+=1
 allrows=[];stream=hashlib.sha256();phasecount=0
 lo,hi=(0,len(shapes))if span is None else span
 need(0<=lo<hi<=len(shapes),'declared physical shape interval')
 for sid,S in enumerate(shapes[lo:hi],start=lo):
  permod=[];inside={m:[0]*m for m in labels}
  for m in labels:
   for n in S:inside[m][n%m]+=1
   values=[];valid=[]
   for a in range(m):
    hit=inside[m][a];outside=base[m][a]-hit;values.extend((hit,outside));phasecount+=1
    if hit==0:valid.append([a,outside])
   raw=struct.pack('<'+'H'*len(values),*values);stream.update(raw)
   permod.append([m,max([0]+[b for a,b in valid]),valid,hashlib.sha256(raw).hexdigest()])
   if outdir:(outdir/('base-'+str(sid)+'-'+str(m)+'.bin')).write_bytes(raw)
  allrows.append([list(S),len(R)-len(S),sum(v[1]for v in permod),permod])
 return dict(R=list(R),literal_phases=phases,completions=completions,distinct_shapes=len(shapes),BASE_labels=list(labels),all_BASE_rows=allrows,BASE_raw_phases=phasecount,whole_BASE_sha256=stream.hexdigest(),minimum_BASE_capacity=min(v[2]for v in allrows),maximum_BASE_capacity=max(v[2]for v in allrows),minimum_outside_need=min(v[1]for v in allrows),minimum_deficit=min(v[1]-v[2]for v in allrows),native_imported=False)
if __name__=='__main__':
 import sys
 from pathlib import Path
 dst=Path(sys.argv[1]);dst.mkdir(parents=True,exist_ok=False)
 span=tuple(map(int,sys.argv[2].split(',')))if len(sys.argv)>2 else None
 x=compute(dst,span);(dst/'record.json').write_bytes(wire(x)+b'\n')
 print(wire(dict(phase_counts=[[p['parent'],p['count'],len(p['qualifying']),p['maximum']]for p in x['literal_phases']],completions=len(x['completions']),shapes=x['distinct_shapes'],BASE_raw_phases=x['BASE_raw_phases'],minimum_BASE_capacity=x['minimum_BASE_capacity'],maximum_BASE_capacity=x['maximum_BASE_capacity'],minimum_outside_need=x['minimum_outside_need'],minimum_deficit=x['minimum_deficit'],whole_BASE_sha256=x['whole_BASE_sha256'])).decode())
