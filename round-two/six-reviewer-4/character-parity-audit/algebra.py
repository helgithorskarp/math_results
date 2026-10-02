#!/usr/bin/env python3
"""Independent cyclic-polynomial inverse and complete gap-orbit reduction."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,json,hashlib,math
N=102;ALL=(1<<N)-1;MOD=(1<<N)|1

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def canon(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def pmul(a,b):
 z=0
 while b:
  if b&1:z^=a
  a<<=1;b>>=1
 return z
def pdiv(a,b):
 need(b>0,'nonzero polynomial divisor');q=0
 while a.bit_length()>=b.bit_length():
  j=a.bit_length()-b.bit_length();q^=1<<j;a^=b<<j
 return q,a
def egcd(a,b):
 x0,x1,y0,y1=1,0,0,1;steps=0
 while b:
  q,r=pdiv(a,b);a,b=b,r;x0,x1=x1,x0^pmul(q,x1);y0,y1=y1,y0^pmul(q,y1);steps+=1
 return a,x0,y0,steps
def rot(x,k):
 k%=N
 return ((x<<k)|(x>>(N-k)))&ALL

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 primitive=next(g for g in range(2,103)if len({pow(g,j,103)for j in range(N)})==N)
 powers=[pow(primitive,j,103)for j in range(N)];logs={v:j for j,v in enumerate(powers)}
 support=range(80,87);P=sum(1<<((-logs[v])%N)for v in support)
 gcd,u,v,steps=egcd(P,MOD);need(gcd==1 and pmul(P,u)^pmul(MOD,v)==1,'whole binary polynomial Bezout identity')
 U=pdiv(u,MOD)[1];need(pdiv(pmul(P,U),MOD)[1]==1,'whole cyclic inverse identity')
 columns=[]
 for r in range(1,103):
  logword=rot(U,logs[r]);fieldword=sum(1<<(powers[j]-1)for j in range(N)if logword>>j&1);columns.append(fieldword)
 rows=[sum(1<<((k*s)%103-1)for s in support)for k in range(1,103)]
 products=0
 for k,row in enumerate(rows):
  for j,column in enumerate(columns):need((row&column).bit_count()%2==int(k==j),'every physical right-inverse entry');products+=1
 need(all(r.bit_count()==7 for r in rows)and len(set(rows))==N,'actual102 distinct seven-supports')
 degree=[sum(bool(r>>j&1)for r in rows)for j in range(N)];need(degree==[7]*N,'every physical vertex degree7')
 data=canon({'points':list(range(1,103)),'inverse_columns_hex':[format(c,'x')for c in columns]});(a.work/'INVERSE.json').write_bytes(data)
 # Translation on log indices is actual field multiplication. Circular
 # positive gap triples classify every syndrome triple up to translation.
 gaps={min((i,j,k),(j,k,i),(k,i,j))for i in range(1,101)for j in range(1,102-i)for k in [102-i-j]}
 seen=set();hist=Counter();registry=[];evaluations=0
 one=ALL^U;hist[one.bit_count()]+=N;registry.append({'syndrome_logs':[0],'orbit_size':N,'candidate_weight':one.bit_count()});evaluations+=1
 min_witness=None
 for g in sorted(gaps):
  i,j,k=g;need(i+j+k==N and min(g)>0,'positive circular gaps')
  seed=(0,i,i+j);orbit={tuple(sorted((x+t)%N for x in seed))for t in range(N)}
  need(not seen&orbit,'distinct complete gap orbits');seen|=orbit
  word=ALL^U^rot(U,i)^rot(U,i+j);w=word.bit_count();hist[w]+=len(orbit);evaluations+=1
  registry.append({'gaps':g,'syndrome_logs':seed,'orbit_size':len(orbit),'candidate_weight':w})
  if min_witness is None or w<min_witness['candidate_weight']:
   min_witness={'syndrome_points':[powers[q]for q in seed],'candidate_weight':w,'candidate_points':[powers[q]for q in range(N)if word>>q&1]}
 need(len(seen)==math.comb(N,3) and all(len(t)==3 and len(set(t))==3 and min(t)>=0 and max(t)<N for t in seen),'complete original triple domain')
 need(sum(hist.values())==N+math.comb(N,3),'whole parity catalogue domain')
 need(15 not in hist and min(hist)>15,'no15-column parity candidate')
 special=[r for r in registry if r.get('orbit_size')!=N];need(len(special)==1 and special[0]['gaps']==(34,34,34)and special[0]['orbit_size']==34,'only the actual equispaced short orbit')
 rb=canon(registry);(a.work/'GAP_ORBITS.json').write_bytes(rb);hb=canon({'weight_histogram':dict(sorted(hist.items()))});(a.work/'HISTOGRAM.json').write_bytes(hb)
 (a.work/'MINIMUM_PARITY_WORD.json').write_bytes(canon(min_witness))
 print(json.dumps({'complete':True,'author_code_or_certificate_imported':False,'method':'binary cyclic polynomial extended Euclid, literal field-coordinate right product, complete circular-gap quotient','primitive_field_element':primitive,'cyclic_operator_polynomial_hex':format(P,'x'),'cyclic_inverse_polynomial_hex':format(U,'x'),'Bezout_steps':steps,'every_physical_inverse_entry_checked':products,'regular_supports':N,'every_support_size':7,'every_field_vertex_degree':7,'inverse_bytes':len(data),'inverse_sha256':hashlib.sha256(data).hexdigest(),'singleton_syndrome_orbits':1,'triple_syndrome_orbits':len(gaps),'short_triple_orbit_size':34,'all_full_triples_covered':len(seen),'full_one_triple_catalogue':sum(hist.values()),'quotient_candidate_evaluations':evaluations,'full_weight_histogram':dict(sorted(hist.items())),'minimum_candidate_weight':min(hist),'weight15_candidates':hist[15],'whole_quotient_registry_bytes':len(rb),'whole_quotient_registry_sha256':hashlib.sha256(rb).hexdigest(),'whole_histogram_sha256':hashlib.sha256(hb).hexdigest(),'minimum_witness':min_witness,'original_cover_optimum_claimed':False},sort_keys=True))
if __name__=='__main__':main()
