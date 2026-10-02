"""Independent bit-mask oracle: every actual hub placement, transports, damages."""
import argparse,copy,hashlib,json,math
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import importlib.util
s=importlib.util.spec_from_file_location('own_census',Path(__file__).with_name('census.py'))
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
need=c.need
FIELDS=['e','k','q','eligible','h','g1','sigma','psi','margin3','a','margin4']
ALL=(1<<17)-1

def physical(blocks):
 masks=[sum(1<<p for p in b)for b in blocks]
 r=[sum(bool(b>>p&1)for b in masks)for p in range(17)]
 covered=[]
 for p in range(17):
  neighbors=0
  for b in masks:
   if b>>p&1:neighbors|=b
  covered.append(neighbors&~(1<<p))
 adj=[ALL&~covered[p]&~(1<<p)for p in range(17)]
 high=sum(1<<p for p,t in enumerate(r)if t<5)
 hh=[adj[p]&high for p in range(17)]
 return r,adj,high,hh

def row_oracle(f,blocks,hubs):
 r,adj,high,hh=physical(blocks)
 hm=sum(1<<p for p in hubs);J=hm&high
 hp=[p for p in range(17)if high>>p&1];h=len(hp);e=5-h;k=J.bit_count()
 edges=[[p,q]for p in hp for q in hp if p<q and hh[p]>>q&1]
 q=sum(bool(hm&((1<<p)|(1<<q)))for p,q in edges)
 isolated=[p for p in hp if J>>p&1 and hh[p]==0]
 g1=sum(r[p]==4 and not hm>>p&1 for p in range(17))
 sigma=sum(4-r[p]for p in hp if not hm>>p&1)
 eligible=bool(isolated)
 psi=g1 if e==0 and eligible else -g1 if e>0 and not eligible else 0
 a=k-e-q
 return {'fixture':f,'hubs':[p for p in hp if J>>p&1],'high':hp,'replication':r,'hh_edges':edges,
  'h':h,'e':e,'k':k,'q':q,'eligible':eligible,'isolated_hubs':isolated,'g1':g1,'sigma':sigma,
  'psi':psi,'a':a,'margin3':psi-3*a,'margin4':psi-4*a,'in_scope':k<=4}

def oracle_rows(stars):
 return [row_oracle(f,b,J)for f,b in enumerate(stars)for k in range(physical(b)[2].bit_count()+1)
         for J in combinations([p for p in range(17)if physical(b)[2]>>p&1],k)]

def match_rows(rows,reference):
 def mapping(v):
  need(len(v)==426,'complete426 physical records')
  d={(r['fixture'],tuple(r['hubs'])):r for r in v};need(len(d)==426,'no duplicated mark');return d
 need(mapping(rows)==mapping(reference),'every physical point/leave/statistic equality')

def brute_boundary(rows,m,P,Q):
 n=18-m;B=4*n-math.comb(n,3)-120*m+740;E=B+3*P-Q;K=20+10*m-5*m*m+2*P-E;D=E+Q-K
 types=sorted({tuple(r[k]for k in FIELDS)for r in rows if r['k']<=m and r['q']<=Q and r['sigma']==0 and 0<=r['margin3']<=3*D})
 def weak(total,length):
  if length==1:yield(total,);return
  for j in range(total+1):
   for tail in weak(total-j,length-1):yield(j,)+tail
 accepted=[];visited=0
 for counts in weak(n,len(types)):
  visited+=1
  if sum(c*t[0]for c,t in zip(counts,types))!=E:continue
  if sum(c*t[1]for c,t in zip(counts,types))!=K:continue
  if sum(c*t[2]for c,t in zip(counts,types))!=Q:continue
  psi=sum(c*t[7]for c,t in zip(counts,types));margin=sum(c*t[8]for c,t in zip(counts,types))
  if psi<=0 and margin<=3*D:accepted.append({'counts':list(counts),'margin':margin,'psi_sum':psi})
 return {'m':m,'P':P,'Q':Q,'n':n,'E':E,'K':K,'delta':D,'types':[list(t)for t in types],
         'compositions':sorted(accepted,key=lambda x:x['counts'])},visited

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--record',type=Path,required=True);a=p.parse_args()
 stars=json.loads(a.input.read_bytes())['stars'];record=json.loads(a.record.read_bytes());oracle=oracle_rows(stars);match_rows(record['rows'],oracle)
 lookup={(r['fixture'],tuple(r['hubs'])):r for r in oracle}
 placements=0;by_m={m:0 for m in range(5)}
 # Physical hub placements: the mask is NOT assumed contained in the high set.
 # Compare all whole row fields after actual low hubs have been removed.
 for f,b in enumerate(stars):
  for m in range(5):
   for H in combinations(range(17),m):
    row=row_oracle(f,b,H);need(row==lookup[(f,tuple(row['hubs']))],'actual low/high hub role projection')
    placements+=1;by_m[m]+=1
 need(placements==23*sum(math.comb(17,m)for m in range(5)),'complete literal placement universe')
 for m,t in by_m.items():need(t==23*math.comb(17,m),'placement cardinality')
 boundary_visited=[]
 for got in record['boundaries']:
  ref,visited=brute_boundary(oracle,got['m'],got['P'],got['Q']);g={k:v for k,v in got.items()if k!='expanded'}
  need(g==ref,'whole boundary categories/compositions independent weak-count product');boundary_visited.append(visited)
 damages=[]
 def reject(label,fn):
  try:fn()
  except (ValueError,KeyError):damages.append(label);return
  raise ValueError('damage accepted: '+label)
 for field in ['e','k','q','eligible','g1','sigma','psi','margin3','a','margin4','in_scope']:
  broken=copy.deepcopy(oracle);old=broken[0][field];broken[0][field]=not old if type(old)is bool else old+1
  reject('wrong '+field,lambda x=broken:match_rows(x,oracle))
 reject('deleted e4 mark',lambda:match_rows([r for r in oracle if r['e']!=4],oracle))
 reject('deleted five-hub failures',lambda:match_rows([r for r in oracle if r['in_scope']],oracle))
 broken=copy.deepcopy(oracle);broken[1]=broken[0]
 reject('duplicated marked row',lambda:match_rows(broken,oracle))
 for i,got in enumerate(record['boundaries']):
  ref,_=brute_boundary(oracle,got['m'],got['P'],got['Q'])
  broken=copy.deepcopy(ref)
  if broken['compositions']:broken['compositions'][0]['counts'][0]+=1
  else:broken['compositions']=[{'counts':[1]*len(broken['types']),'margin':0,'psi_sum':0}]
  reject('fabricated boundary composition '+str(i),lambda x=broken,y=ref:need(x==y,'full independent boundary mismatch'))
 for name,mutate in [
  ('missing star',lambda z:z.pop()),('missing block',lambda z:z[0].pop()),
  ('duplicated block',lambda z:z[0].__setitem__(1,z[0][0][:])),
  ('boolean point',lambda z:z[0][0].__setitem__(0,True)),
  ('out-of-domain point',lambda z:z[0][0].__setitem__(0,17)),
  ('repeated point',lambda z:z[0][0].__setitem__(1,z[0][0][0]))]:
  bad=copy.deepcopy(stars);mutate(bad);reject(name,lambda z=bad:c.census(z))
 transported=0
 for perm in [[(p+3)%17 for p in range(17)],[16-p for p in range(17)],[1,0]+list(range(2,17))]:
  moved=[[[perm[p]for p in b]for b in star]for star in stars]
  actual=c.census(moved);expected=oracle_rows(moved);match_rows(actual,expected)
  for old in oracle:
   key=(old['fixture'],tuple(sorted(perm[p]for p in old['hubs'])))
   now={(r['fixture'],tuple(r['hubs'])):r for r in actual}[key]
   need(all(now[f]==old[f]for f in FIELDS),'all row statistics survive literal coordinate transport');transported+=1
 # Algebra/ordinary-proof calibrations; neither proves ambient existence.
 need([20+10*m-5*m*m-2*(4*(18-m)-math.comb(18-m,3)-120*m+740)for m in range(1,5)]==[9,12,35,76],'incidence constants')
 for j in range(6):need((math.comb(5-j,3)if 5-j>=3 else 0)==10-6*j+3*math.comb(j,2)-(math.comb(j,3)if j>=3 else 0),'word triple identity')
 need([3*n%2 for n in [11,9,13]]==[1,1,1],'odd simple cubic blocks')
 # Both local coefficient endpoints are attained by literal physical marks.
 ratio=[Fraction(r['psi'],r['a'])for r in oracle if r['in_scope']and r['a']>0]
 negative=[Fraction(r['psi'],r['a'])for r in oracle if r['in_scope']and r['a']<0]
 need(min(ratio)==4 and max(negative)==3,'optimal full coefficient interval')
 print(json.dumps({'actual_hub_placements':placements,'by_m':by_m,'complete_marked_rows':len(oracle),
  'weak_compositions_visited':boundary_visited,'damage_rejections':len(damages),'damage_names':damages,
  'transported_stars':69,'transported_marked_rows':transported,'coefficient_interval':['3','4']},sort_keys=True))
if __name__=='__main__':main()
