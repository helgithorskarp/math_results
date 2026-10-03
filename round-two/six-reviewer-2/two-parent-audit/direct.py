"""Separate reviewer reconstruction: sets, explicit expansion, global subsets.

Imports no incidence.py or physical.py. Whole output rows compared, not maxima only.
"""
from itertools import combinations,product
from collections import Counter
from math import lcm
from functools import lru_cache
import hashlib,json,struct
PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=tuple(d for d in range(2,316)if 315%d==0)
ALLOC=((2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4))
def need(ok,why):
 if not ok:raise ValueError(why)
def wire(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def capacity(outdir,chosen=None):
 banned=set()
 for m,a in PREFIX:banned.update(range(a,2520,m))
 R=tuple(sorted(set(range(2520))-banned));pts={r:tuple(n for n in R if n%8==r)for r in range(1,8)}
 phase={r:{d:[{n for n in pts[r]if n%d==a}for a in range(d)]for d in (1,)+D}for r in range(1,8)}
 pop={r:{d:[len(z)for z in phase[r][d]]for d in (1,)+D}for r in range(1,8)}
 cap={r:{d:max(v)for d,v in pop[r].items()}for r in range(1,8)}
 pairs={};pairhash=hashlib.sha256();paircount=0
 for a,b in combinations(D,2):
  values=[len(x|y)for x,y in product(phase[2][a],phase[2][b])]
  raw=struct.pack('<'+'H'*len(values),*values);pairhash.update(raw);paircount+=len(values);pairs[a,b]=max(values)
  (outdir/('pair-'+str(a)+'-'+str(b)+'.bin')).write_bytes(raw)
 @lru_cache(None)
 def U(hs):
  if not hs:return 0
  if len(hs)==1:return cap[2][hs[0]]
  if len(hs)==2:return pairs[tuple(sorted(hs))]
  need(len(hs)==3,'input126 group bound')
  return min([126,sum(cap[2][d]for d in hs)]+[pairs[tuple(sorted(set(hs)-{d}))]+cap[2][d]for d in hs])
 def B(n,groups):
  if any(not g for g in groups):return 0
  return min([sum(n[d]for d in g)for g in groups]+[sum(n[lcm(*t)]for t in product(*groups))])
 def intersection(n,*groups):
  return sum(n[lcm(*t)]for t in product(*groups))
 @lru_cache(None)
 def local(r,hs,q):
  n=cap[r];raw=[];best=-1;witness=None
  for qs in combinations(D,q):
   for hh,qq in product(product((12,)if r==2 else(3,12),repeat=len(hs)),product((4,8)if r==2 else((2,4,8)if r==6 else(1,2,4,8)),repeat=q)):
    occupied=3 if r==2 else(1 if r==6 else 0)
    for v in hh+qq:occupied|=v
    if occupied!=15:continue
    H1=tuple(d for d,v in zip(hs,hh)if v==3);H2=tuple(d for d,v in zip(hs,hh)if v==12)
    Q={a:tuple(d for d,v in zip(qs,qq)if v==a)for a in(1,2,4,8)}
    if r==2:value=min(len(pts[r]),U(hs)+B(n,(Q[4],Q[8])))
    elif r==6:
     expanded=intersection(n,H2,H1)+intersection(n,H2,Q[2])+intersection(n,H1,Q[4],Q[8])+intersection(n,Q[2],Q[4],Q[8])
     value=min(len(pts[r]),expanded,U(H2)+B(n,(Q[4],Q[8])),U(H1)+sum(n[d]for d in Q[2]))
    else:
     expanded=intersection(n,H1,H2)+intersection(n,H1,Q[4],Q[8])+intersection(n,H2,Q[1],Q[2])+intersection(n,Q[1],Q[2],Q[4],Q[8])
     value=min(len(pts[r]),expanded,sum(n[d]for d in H1)+B(n,(Q[1],Q[2])),sum(n[d]for d in H2)+B(n,(Q[4],Q[8])))
    raw.append(value)
    if value>best:best=value;witness=qs
  packet=struct.pack('<'+'H'*len(raw),*raw)
  return(best if raw else 0,witness,len(raw),hashlib.sha256(packet).hexdigest())
 records=[];grows={};total=0;survivors=[];needed=set()
 for r in (1,4):
  for ns in ALLOC:
   if chosen is not None and chosen!=(r,ns):continue
   values=[];types=[];maximum=0
   for h2 in range(ns[0]):
    q2=ns[0]-1-h2
    if h2==0 and q2<2:continue
    for h6 in range(ns[1]):
     q6=ns[1]-1-h6
     if q6==0 or(h6==0 and q6<3):continue
     for hr in range(ns[2]+1):
      qr=ns[2]-hr
      if not(hr>=2 or(hr>=1 and qr>=2)or qr>=4):continue
      # All used H sets first; then all ordered disjoint splits. Different
      # construction from choosing the three groups from shrinking pools.
      table={}
      for whole in combinations(D,h2+h6+hr):
       for a in combinations(whole,h2):
        rem=tuple(d for d in whole if d not in a)
        for b in combinations(rem,h6):
         c=tuple(d for d in rem if d not in b)
         v=local(2,a,q2)[0]+local(6,b,q6)[0]+local(r,c,qr)[0]
         need((a,b,c)not in table,'distinct ordered split');table[a,b,c]=v
      block=[v for k,v in sorted(table.items())];packet=struct.pack('<'+'H'*len(block),*block)
      typ=[h2,q2,h6,q6,hr,qr];types.append([typ,len(block),max(block),hashlib.sha256(packet).hexdigest()]);values.extend(block);total+=len(block);maximum=max(maximum,max(block))
      for (a,b,c),v in sorted(table.items()):
       if v>=177:survivors.append([r,list(ns),typ,list(a),list(b),list(c),v])
      for parent,h,q in ((2,h2,q2),(6,h6,q6),(r,hr,qr)):
       needed.update((parent,hs,q)for hs in combinations(D,h))
   packet=struct.pack('<'+'H'*len(values),*values);key=str(r)+'-'+''.join(map(str,ns));grows[key]=[len(values),maximum,hashlib.sha256(packet).hexdigest()];(outdir/('global-'+key+'.bin')).write_bytes(packet);records.append([r,list(ns),types])
 locals=[[r,list(hs),q,*local(r,hs,q)]for r,hs,q in sorted(needed)]
 return dict(R=list(R),parent_populations=pop,pair_union=[[list(k),v]for k,v in pairs.items()],pair_phase_count=paircount,pair_phase_sha256=pairhash.hexdigest(),local_rows=locals,types=records,global_rows=grows,total_global_H_allocations=total,survivors=survivors,original_H_globally_distinct=True,cross_parent_Q_collisions_relaxed=True,cross_type_equal_cofactors_legal=True,three_H126_dependency='LEMMA10022 / independently checked new numerical step in REVIEW10066',native_imported=False)

def physical(outdir,span=None):
 banned=set()
 for m,a in PREFIX:banned.update(range(a,2520,m))
 R=tuple(sorted(set(range(2520))-banned));scenarios=((2,(80,144,240),((16,2),),72),(6,(48,96),((32,6),),90),(4,(112,336),(),15));phases=[];goods={}
 for r,ms,fixed,cut in scenarios:
  pts=tuple(n for n in R if n%8==r);universe={n+2520*k for n in pts for k in range(4)}
  pref=set().union(*({x for x in universe if x%m==a}for m,a in fixed))if fixed else set()
  individual={m:{a:{x for x in universe if x%m==a}for a in range(r,m,8)}for m in ms};rows=[];good=[];values=[]
  for aa in product(*(range(r,m,8)for m in ms)):
   cover=pref.copy()
   for m,a in zip(ms,aa):cover.update(individual[m][a])
   hits=[n for n in pts if all(n+2520*k in cover for k in range(4))];values.append(len(hits));rows.append([list(aa),len(hits),hits])
   if len(hits)>=cut:good.append([list(aa),hits])
  packet=struct.pack('<'+'H'*len(values),*values);(outdir/('phases-'+str(r)+'.bin')).write_bytes(packet)
  phases.append(dict(parent=r,moduli=list(ms),threshold=cut,all_rows=rows,qualifying=good,count=len(rows),maximum=max(values),values_sha256=hashlib.sha256(packet).hexdigest()));goods[r]=good
 completions=[[a[0]+b[0]+c[0],sorted(a[1]+b[1]+c[1])]for a,b,c in product(goods[2],goods[6],goods[4])];shapes=sorted({tuple(v[1])for v in completions})
 labels=tuple(m for m in range(8,2521)if 2520%m==0 and m not in {m for m,a in PREFIX});residue_sets={m:[{n for n in R if n%m==a}for a in range(m)]for m in labels};rows=[];stream=hashlib.sha256();phasecount=0
 lo,hi=(0,len(shapes))if span is None else span
 need(0<=lo<hi<=len(shapes),'declared physical shape interval')
 for sid,S in enumerate(shapes[lo:hi],start=lo):
  S=set(S);permod=[]
  for m in labels:
   numbers=[];valid=[]
   # Explicit intersections; no histogram subtraction or bitmap imports.
   for a,rs in enumerate(residue_sets[m]):
    hit=len(rs&S);outside=len(rs-S);numbers.extend((hit,outside));phasecount+=1
    if hit==0:valid.append([a,outside])
   packet=struct.pack('<'+'H'*len(numbers),*numbers);stream.update(packet);(outdir/('base-'+str(sid)+'-'+str(m)+'.bin')).write_bytes(packet)
   permod.append([m,max([0]+[v for a,v in valid]),valid,hashlib.sha256(packet).hexdigest()])
  rows.append([sorted(S),len(R)-len(S),sum(v[1]for v in permod),permod])
 return dict(R=list(R),literal_phases=phases,completions=completions,distinct_shapes=len(shapes),BASE_labels=list(labels),all_BASE_rows=rows,BASE_raw_phases=phasecount,whole_BASE_sha256=stream.hexdigest(),minimum_BASE_capacity=min(v[2]for v in rows),maximum_BASE_capacity=max(v[2]for v in rows),minimum_outside_need=min(v[1]for v in rows),minimum_deficit=min(v[1]-v[2]for v in rows),native_imported=False)
if __name__=='__main__':
 import sys
 from pathlib import Path
 mode=sys.argv[1];dst=Path(sys.argv[2]);dst.mkdir(parents=True,exist_ok=False)
 key=tuple(map(int,sys.argv[3].split(',')))if len(sys.argv)>3 else None
 if mode=='capacity':
  need(key is None or(key[0]in(1,4)and key[1:]in ALLOC),'declared capacity partition')
  x=capacity(dst,None if key is None else(key[0],key[1:]))
 else:x=physical(dst,key)
 x['local_rows']=sorted(x['local_rows'])if mode=='capacity'else None
 if mode!='capacity':del x['local_rows']
 (dst/'record.json').write_bytes(wire(x)+b'\n');print(wire(dict(mode=mode,record_bytes=len(wire(x)),record_sha256=hashlib.sha256(wire(x)).hexdigest())).decode())
