"""six-reviewer-2: independently written quarter-incidence capacity audit.

Written theorem exposed. Target executable and fixture not used.
Full original labels, no quotient of phase or global allocation domains.
"""
from itertools import combinations,product
from math import lcm
from functools import lru_cache
import hashlib,json,struct

PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=tuple(d for d in range(2,316)if 315%d==0)
ALLOC=((2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4))
def need(ok,why):
 if not ok:raise ValueError(why)
def wire(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def masks(points,m):
 out=[0]*m
 for i,x in enumerate(points):out[x%m]|=1<<i
 return out

def compute(outdir=None):
 R=tuple(x for x in range(2520)if all(x%m!=a for m,a in PREFIX))
 pts={r:tuple(x for x in R if x%8==r)for r in range(8)}
 pools={r:{d:masks(pts[r],d)for d in (1,)+D}for r in range(1,8)}
 populations={r:{d:[v.bit_count()for v in pools[r][d]]for d in (1,)+D}for r in range(1,8)}
 C={d:max(populations[2][d])for d in (1,)+D}
 need(C=={d:max(populations[6][d])for d in (1,)+D},'mandatory parent capacities')
 for r in (3,5,7):need({d:max(populations[r][d])for d in C}=={d:max(populations[1][d])for d in C},'all four odd parents independently rebuilt')
 pairs={};pair_sha=hashlib.sha256();pair_phases=0
 for ds in combinations(D,2):
  values=[]
  for a,b in product(*(range(d)for d in ds)):
   values.append((pools[2][ds[0]][a]|pools[2][ds[1]][b]).bit_count())
  raw=struct.pack('<'+'H'*len(values),*values);pair_sha.update(raw);pair_phases+=len(values)
  pairs[ds]=max(values)
  if outdir:(outdir/('pair-'+str(ds[0])+'-'+str(ds[1])+'.bin')).write_bytes(raw)
 @lru_cache(None)
 def union(parent,ds):
  if not ds:return 0
  n={d:max(populations[parent][d])for d in C}
  if parent in (2,6):
   if len(ds)==1:return C[ds[0]]
   if len(ds)==2:return pairs[tuple(sorted(ds))]
   need(len(ds)==3,'mandatory union group at most three')
   return min(126,sum(C[d]for d in ds),min(pairs[tuple(sorted(e for e in ds if e!=d))]+C[d]for d in ds))
  return sum(n[d]for d in ds)
 # Templates are derived from literal four-quarter incidences, not imported DNF.
 @lru_cache(None)
 def templates(parent,h,q):
  hc=(12,)if parent==2 else (3,12)
  qc=(4,8)if parent==2 else ((2,4,8)if parent==6 else(1,2,4,8))
  placed=3 if parent==2 else (1 if parent==6 else 0)
  rows=[]
  for hs,qs in product(product(hc,repeat=h),product(qc,repeat=q)):
   arms=hs+qs
   active=placed
   for arm in arms:active|=arm
   if active!=15:continue
   covers=[]
   for bits in range(1,1<<(h+q)):
    z=placed
    for i,v in enumerate(arms):
     if bits>>i&1:z|=v
    if z==15 and not any((s&bits)==s for s in covers):covers.append(bits)
   mins=tuple(tuple(i for i in range(h+q)if s>>i&1)for s in covers if not any(t!=s and(t&s)==t for t in covers))
   halfs=[]
   for half in (3,12):
    missing=half&~placed
    if not missing:continue
    hh=tuple(i for i in range(h)if arms[i]&half)
    qq=tuple(tuple(i for i in range(h,h+q)if arms[i]&bit)for bit in (1,2,4,8)if missing&bit)
    halfs.append((hh,qq))
   rows.append((mins,tuple(halfs)))
  return rows
 @lru_cache(None)
 def local(parent,hs,q):
  n={d:max(populations[parent][d])for d in C};h=len(hs)
  rows=templates(parent,h,q);raw=[];best=-1;witness=None
  for qs in combinations(D,q):
   ds=hs+qs
   for monomials,halfs in rows:
    bounds=[sum(n[lcm(*(ds[i]for i in mono))]for mono in monomials)]
    for hh,qq in halfs:
     H=union(parent,tuple(ds[i]for i in hh))
     sums=[sum(n[ds[i]]for i in arm)for arm in qq]
     crossing=sum(n[lcm(*(ds[i]for i in term))]for term in product(*qq))
     bounds.append(H+min(sums+[crossing]))
    v=min(bounds+[len(pts[parent])]);raw.append(v)
    if v>best:best=v;witness=qs
  if not rows:return(0,None,0,hashlib.sha256(b'').hexdigest())
  packet=struct.pack('<'+'H'*len(raw),*raw)
  return(best,witness,len(raw),hashlib.sha256(packet).hexdigest())
 type_records=[];global_rows={};total=0;survivors=[]
 for r in (1,4):
  for ns in ALLOC:
   aggregate=[];types=[];maximum=0
   for h2 in range(ns[0]):
    q2=ns[0]-1-h2
    if not templates(2,h2,q2):continue
    for h6 in range(ns[1]):
     q6=ns[1]-1-h6
     if q6<1 or not templates(6,h6,q6):continue
     for hr in range(ns[2]+1):
      qr=ns[2]-hr
      if not templates(r,hr,qr):continue
      ct=0;top=0;type_sha=hashlib.sha256()
      for a in combinations(D,h2):
       rem=tuple(d for d in D if d not in a)
       for b in combinations(rem,h6):
        left=tuple(d for d in rem if d not in b)
        for c in combinations(left,hr):
         z=local(2,a,q2)[0]+local(6,b,q6)[0]+local(r,c,qr)[0]
         top=max(top,z);ct+=1;total+=1;aggregate.append(z);type_sha.update(struct.pack('<H',z))
         if z>=177:survivors.append([r,list(ns),[h2,q2,h6,q6,hr,qr],list(a),list(b),list(c),z])
      types.append([[h2,q2,h6,q6,hr,qr],ct,top,type_sha.hexdigest()]);maximum=max(maximum,top)
   raw=struct.pack('<'+'H'*len(aggregate),*aggregate);key=str(r)+'-'+''.join(map(str,ns));global_rows[key]=[len(aggregate),maximum,hashlib.sha256(raw).hexdigest()]
   if outdir:(outdir/('global-'+key+'.bin')).write_bytes(raw)
   type_records.append([r,list(ns),types])
 locals=[]
 # Materialize every memoized primitive local group used in every global row.
 for r,ns,types in type_records:
  for typ,count,top,sha in types:
   for parent,h,q in ((2,typ[0],typ[1]),(6,typ[2],typ[3]),(r,typ[4],typ[5])):
    for hs in combinations(D,h):
     row=[parent,list(hs),q,*local(parent,hs,q)]
     if row not in locals:locals.append(row)
 return dict(R=list(R),parent_populations=populations,pair_union=[[list(k),v]for k,v in pairs.items()],pair_phase_count=pair_phases,pair_phase_sha256=pair_sha.hexdigest(),local_rows=sorted(locals),types=type_records,global_rows=global_rows,total_global_H_allocations=total,survivors=survivors,original_H_globally_distinct=True,cross_parent_Q_collisions_relaxed=True,cross_type_equal_cofactors_legal=True,three_H126_dependency='LEMMA10022 / independently checked new numerical step in REVIEW10066',native_imported=False)

if __name__=='__main__':
 import sys
 from pathlib import Path
 dst=Path(sys.argv[1]);dst.mkdir(parents=True,exist_ok=False)
 result=compute(dst);(dst/'record.json').write_bytes(wire(result)+b'\n');print(wire({k:result[k]for k in ('global_rows','total_global_H_allocations','survivors','pair_phase_count')} ).decode())
