#!/usr/bin/env python3
"""Literal colored graphs calibrate the scalar and capacity bridges.
All arbitrary22 fixtures may violate page caps; they are not witnesses.
"""
from itertools import combinations
from math import comb
import hashlib,json

def need(ok,message):
 if not ok:raise RuntimeError(message)
def rows(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 return a
def spines(a):
 n=len(a);univ=set(range(n));out=[]
 for u,v in combinations(range(n),2):
  red=v in a[u]
  pages=len(a[u]&a[v]) if red else len(univ-{u,v}-a[u]-a[v])
  out.append([u,v,red,pages,(3 if red else 6)-pages])
 return out
def main():
 # Rotation of the original21 nonfixed vertices, root21 fixed.
 def rot(u):return 21 if u==21 else 3*(u//3)+(u%3+1)%3
 def orbit(u,v):
  s=set()
  for _ in range(3):s.add(tuple(sorted((u,v))));u,v=rot(u),rot(v)
  return tuple(sorted(s))
 orbits=sorted({orbit(u,v) for u,v in combinations(range(22),2)})
 need(len(orbits)==77 and all(len(o)==3 for o in orbits),'whole original22 C3 partition')
 rootorbits=[o for o in orbits if any(21 in e for e in o)]
 ordinary=[o for o in orbits if o not in rootorbits]
 need(len(rootorbits)==7 and len(ordinary)==70,'root orbit partition')
 digest=hashlib.sha256();physical=[];pairs=0;AA=0
 for seed in range(64):
  # Fixed SHA256 bits, different fixture generation from the author.
  bits=int.from_bytes(hashlib.sha256(('reviewer4-literal22-'+str(seed)).encode()).digest(),'big')
  chosen=rootorbits[:3]+[o for k,o in enumerate(ordinary) if bits>>k&1]
  edges={e for o in chosen for e in o};a=rows(22,edges);d=list(map(len,a));e=len(edges)
  ss=spines(a);W=sum(r[4] for r in ss)
  need(2*W==-6468+120*e-3*sum(x*x for x in d),'literal whole deficit identity')
  A=sorted(a[21]);B=set(range(21))-set(A);h=sum(v in a[u] for u,v in combinations(A,2))
  k=sum(v in a[u] for u,v in combinations(sorted(B),2));DA=sum(d[u] for u in A)
  Dx=sum(r[4] for r in ss if 21 in r[:2])
  need(len(A)==9 and e==DA-h+k and Dx==2*e-33-2*DA,'literal root cut and root deficit')
  caps=[];actual=[]
  bypair={tuple(r[:2]):r[4] for r in ss}
  for u,v in combinations(A,2):
   common=len(a[u]&a[v]&set(A))
   lam=2-common if v in a[u] else d[u]+d[v]-15-common
   overlap=len(a[u]&a[v]&B)
   need(lam-overlap==bypair[u,v],'actual AA spine deficit equals capacity slack')
   caps.append(lam);actual.append(overlap)
  need(sum(actual)==sum(comb(len(a[v]&set(A)),2) for v in B),'physical Gram overlap identity')
  record=[seed,e,d,W,DA,h,k,Dx,caps,actual]
  digest.update((json.dumps(record,separators=(',',':'))+'\n').encode())
  physical.append(record);pairs+=len(ss);AA+=len(caps)
 # Actual positive and forbidden-page boundary controls with known colors.
 fixtures=[('valid_empty4',rows(4,set()),True),('red_B4',rows(6,{(0,1)}|{(u,v) for u in (0,1) for v in range(2,6)}),False),('blue_B7',rows(9,set()),False)]
 boundaries=[]
 for label,a,expected in fixtures:
  ss=spines(a);valid=all(r[4]>=0 for r in ss)
  need(valid==expected,'actual colored book boundary control')
  boundaries.append({'label':label,'valid':valid,'spines':len(ss),'minimum_deficit':min(r[4] for r in ss)})
 # Each wrong physical identity is actually contradicted on a fixed fixture.
 rejected=[]
 for label,predicate in [
 ('wrong_quadratic_degree_coefficient',lambda r:2*r[3]==-6468+120*r[1]-sum(x*x for x in r[2])),
 ('omit_root_constant',lambda r:r[7]==2*r[1]-2*r[4])]:
  need(any(not predicate(r) for r in physical),'damaged identity was not detected');rejected.append(label)
 print(json.dumps({'complete':True,'arbitrary_C3_graphs':64,'original22_edge_orbits':77,'literal22_spines':pairs,'literal_AA_capacity_slacks':AA,'entire_physical_records_sha256':digest.hexdigest(),'actual_colored_boundary_controls':boundaries,'rejected_physical_identity_damages':rejected,'arbitrary22_fixtures_are_witnesses':False},sort_keys=True))
if __name__=='__main__':main()
