"""Independent physical-row and exact-coefficient audit of committed9313.
Only literal20-quadruple stars are input; no author executable/expected/certificate.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,json,hashlib,time


def need(ok,message):
 if not ok:raise ValueError(message)


def encoded(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()


def census(stars):
 need(len(stars)==23,'generic star count')
 records=[]
 for fixture,blocks in enumerate(stars):
  need(len(blocks)==20 and len({tuple(sorted(b))for b in blocks})==20,'twenty distinct blocks')
  need(all(len(set(b))==4 and all(type(p)is int and 0<=p<17 for p in b)for b in blocks),'physical block domain')
  pair_owner={}
  for i,b in enumerate(blocks):
   for pair in combinations(sorted(b),2):
    need(pair not in pair_owner,'repeated pair in shortened star');pair_owner[pair]=i
  r=[sum(p in b for b in blocks)for p in range(17)]
  need(all(t<=5 for t in r)and sum(r)==80,'replication scope')
  high=[p for p,t in enumerate(r)if t<5]
  low=set(range(17))-set(high)
  leave=[pair for pair in combinations(range(17),2)if pair not in pair_owner]
  need(len(pair_owner)==120 and len(leave)==16,'complete physical leave')
  need(all(not(set(pair)<=low)for pair in leave),'no-low-low imported premise')
  need(sum(5-r[p]for p in high)==5 and 1<=len(high)<=5,'deficit mass5')
  hh=[pair for pair in leave if set(pair)<=set(high)]
  need(len(hh)==len(high)-1,'high-high edge identity')
  e=5-len(high)
  for k in range(len(high)+1):
   for hubs in combinations(high,k):
    hubset=set(hubs);eligible=[p for p in hubs if not any(p in edge for edge in hh)]
    q=sum(bool(set(edge)&hubset)for edge in hh)
    saturated=set(high)-hubset
    g1=sum(r[p]==4 for p in saturated)
    sigma=sum(4-r[p]for p in saturated)
    unit=(e==0)
    psi=g1 if unit and eligible else -g1 if not unit and not eligible else 0
    a=k-e-q
    records.append({'fixture':fixture,'hubs':list(hubs),'high':high,'replication':r,
      'hh_edges':[list(edge)for edge in hh],'h':len(high),'e':e,'k':k,'q':q,
      'eligible':bool(eligible),'isolated_hubs':eligible,'g1':g1,'sigma':sigma,'psi':psi,
      'a':a,'margin3':psi-3*a,'margin4':psi-4*a,'in_scope':k<=4})
 need(len(records)==sum(2**len([p for p in range(17)if sum(p in b for b in blocks)<5])for blocks in stars),'complete subset carrier')
 need(len({(r['fixture'],tuple(r['hubs']))for r in records})==len(records),'unique physical marked rows')
 return records


def coefficients(rows):
 inside=[r for r in rows if r['in_scope']]
 lower,upper=Fraction(0),None
 lows,ups=[],[]
 for r in inside:
  a,psi=r['a'],r['psi']
  if a==0:need(psi>=0,'no coefficient can satisfy zero-a row')
  elif a>0:
   bound=Fraction(psi,a)
   if upper is None or bound<upper:upper=bound;ups=[r]
   elif bound==upper:ups.append(r)
  else:
   bound=Fraction(psi,a)
   if bound>lower:lower=bound;lows=[r]
   elif bound==lower:lows.append(r)
 need(upper is not None and lower<=upper,'coefficient interval empty')
 for r in inside:
  need(Fraction(r['psi'])>=lower*r['a']and Fraction(r['psi'])>=upper*r['a'],'whole endpoint inequality')
  need(r['psi']>=4*max(r['a'],0)-3*max(-r['a'],0),'signed row refinement')
 return {'interval':[str(lower),str(upper)],'lower_attaining_rows':[[r['fixture'],r['hubs']]for r in lows],
         'upper_attaining_rows':[[r['fixture'],r['hubs']]for r in ups],
         'off_scope_failures':[[r['fixture'],r['hubs'],r['psi'],r['a'],r['margin3']]for r in rows if not r['in_scope']and r['margin3']<0]}


def categories(rows,m):
 fields=['e','k','q','eligible','h','g1','sigma','psi','margin3','a','margin4']
 return sorted({tuple(r[f]for f in fields)for r in rows if r['k']<=m})


def boundary(rows,m,p,q):
 n=18-m;B=4*n-n*(n-1)*(n-2)//6-120*m+740
 E=B+3*p-q;W=20+10*m-5*m*m+2*p;K=W-E;delta=E+q-K
 need(E>=0 and K>=0 and delta>=0,'boundary scalar feasibility')
 types=[t for t in categories(rows,m)if t[2]<=q and t[6]==0 and 0<=t[8]<=3*delta]
 # Complete count-vector multiplication of local types; different order from
 # author recursive category partition. All sums bounded by the exact totals.
 states={(0,0,0,0,0):[()]};expanded=0
 for index,t in enumerate(types):
  e,k,qr,eligible,h,g1,sigma,psi,margin,a,margin4=t
  nxt={}
  for key,compositions in states.items():
   for count in range(n-key[0]+1):
    out=(key[0]+count,key[1]+count*e,key[2]+count*k,key[3]+count*qr,key[4]+count*margin)
    if out[1]>E or out[2]>K or out[3]>q or out[4]>3*delta:continue
    for counts in compositions:nxt.setdefault(out,[]).append(counts+(count,))
    expanded+=1
  states=nxt
  need(expanded<=100000,'fixed category resource guard; incomplete gives no exclusion')
 accepted=[]
 for key,compositions in states.items():
  if key[:4]==(n,E,K,q):
   for counts in compositions:
    psi_sum=sum(c*t[7]for c,t in zip(counts,types))
    if psi_sum<=0:accepted.append({'counts':list(counts),'margin':key[4],'psi_sum':psi_sum})
 accepted.sort(key=lambda r:r['counts'])
 return {'m':m,'P':p,'Q':q,'n':n,'E':E,'K':K,'delta':delta,'types':[list(t)for t in types],
         'compositions':accepted,'expanded':expanded}


def main():
 a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
 start=time.monotonic();stars=json.loads(args.input.read_bytes())['stars'];rows=census(stars);interval=coefficients(rows)
 boundaries=[boundary(rows,*triple)for triple in [(2,3,0),(3,9,0),(3,9,1),(4,19,0)]]
 result={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','rows':rows,'coefficient':interval,
  'boundaries':boundaries,'row_count':len(rows),'in_scope_count':sum(r['in_scope']for r in rows)}
 args.out.write_bytes(encoded(result))
 print(json.dumps({'rows':len(rows),'in_scope':result['in_scope_count'],'coefficient_interval':interval['interval'],
   'off_scope_failures':len(interval['off_scope_failures']),'boundary_compositions':[len(b['compositions'])for b in boundaries],
   'whole_bytes':args.out.stat().st_size,'whole_sha256':hashlib.sha256(args.out.read_bytes()).hexdigest(),'seconds':time.monotonic()-start},sort_keys=True))


if __name__=='__main__':main()
