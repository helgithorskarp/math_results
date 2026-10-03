"""Different fixed-N coefficient proof of each supplied coupled-column record.

Fresh bounded compositions produce carriers, forward point maps quotient
light labels, complete type factors realize one column at fixed N, and
the whole four-factor product checks simultaneous quotas. No author
executable imports. This remains a necessary candidate-list relaxation.
"""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path

S=Path('round-two/six-code-3/scratch');PAIRS=list(itertools.combinations(range(4),2));TRIPLES=list(itertools.combinations(range(4),3))

def need(test,message):
 if not test:raise ValueError(message)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def compositions(total,n):
 if n==1:
  yield (total,);return
 for k in range(total+1):
  for tail in compositions(total-k,n-1):yield (k,)+tail

def carriers():
 labelled=0;out=[]
 for owned in itertools.combinations(TRIPLES,0):
  mask=sum(1<<TRIPLES.index(t) for t in owned);tab=[sum(set(p)<=set(t) for t in owned) for p in PAIRS]
  upper=[min(5,(14+t)//3) for t in tab];lower=[(t+2)//3 for t in tab]
  for slack in compositions(sum(upper)-22,6):
   lam=tuple(u-d for u,d in zip(upper,slack))
   if any(l<x for l,x in zip(lam,lower)):continue
   D=[sum(l for p,l in zip(PAIRS,lam) if a in p)-(2 if a==0 else 6) for a in range(4)]
   if min(D)<0:continue
   labelled+=1;orbit=[]
   for lights in itertools.permutations((1,2,3)):
    perm=(0,)+lights;edges={tuple(sorted((perm[a],perm[b]))):l for (a,b),l in zip(PAIRS,lam)};ts={tuple(sorted(perm[a] for a in t)) for t in owned}
    mm=sum(1<<i for i,t in enumerate(TRIPLES) if t in ts);orbit.append((mm,tuple(edges[p] for p in PAIRS)))
   if (mask,lam)!=min(orbit):continue
   out.append(dict(T=0,global_HHH_mask=mask,four_hub_words=0,lambda6=list(lam),D4=D,HH_leave_totals=[14+t-3*l for t,l in zip(tab,lam)]))
 return labelled,sorted(out,key=lambda c:(c['global_HHH_mask'],c['lambda6']))

def options(catalogue,mask,zero):
 allowed={0}|{1<<i for i in range(4) if mask>>i&1};out={}
 for r in catalogue:
  if r['HHH_covered_mask'] not in allowed or any(r['HH_leave_mask']>>i&1 for i in zero):continue
  roles=out.setdefault(r['type_id'],[set() for _ in range(4)])
  for a in range(4):
   d=r['hub_deficits'][a];L=r['low_sat_friend_degrees'][a];need(d or not L,'LOW hub friend impossible');roles[a].add((d,L))
 return out

def macro_failure(c):
 owned=[TRIPLES[i] for i in range(4) if c['global_HHH_mask']>>i&1]
 if any(lam<sum(set(pair)<=set(t) for t in owned) for pair,lam in zip(PAIRS,c['lambda6'])):return 'actual_distinct_HHH_owners'
 D=c['D4']
 if D[0]>12 or max(D[0]+D[i] for i in (1,2,3))>16 or any(D[a]+D[b] not in range(8,14) for a,b in [(1,2),(1,3),(2,3)]):return 'complementary_pair_role_bounds'
 return None

def supported_N(population,a,target,ops,tick,factors,polynomials):
 grouped=tuple((count,tuple(sorted(ops.get(tid,[set() for _ in range(4)])[a]))) for tid,count in population);key=(grouped,target)
 if key in polynomials:return polynomials[key]
 answer=[]
 for N in range(min(target,14)+1):
  fs=[];impossible=False
  for count,choices in grouped:
   permitted=tuple(sorted({(d,L%2) for d,L in choices if (d>0 and L<N) or (d==0 and L==0)}))
   if not permitted:impossible=True;break
   fkey=(count,permitted)
   if fkey not in factors:
    factor=set()
    for multiplicities in compositions(count,len(permitted)):
     tick();w=sum(c*d for c,(d,p) in zip(multiplicities,permitted));n=sum(c*bool(d) for c,(d,p) in zip(multiplicities,permitted));p=sum(c*p for c,(d,p) in zip(multiplicities,permitted))%2;factor.add((w,n,p))
    factors[fkey]=factor
   fs.append(factors[fkey])
  if impossible:continue
  states={(0,0,0)}
  for factor in sorted(fs,key=len):
   following=set()
   for w,n,p in states:
    for dw,dn,dp in factor:
     tick()
     if w+dw<=target and n+dn<=N:following.add((w+dw,n+dn,p^dp))
   states=following
   if not states:break
  if (target,N,0) in states:answer.append(N)
 polynomials[key]=answer;return answer

def joint(sets,K,L,tick):
 answer=[]
 for N in itertools.product(*sets):
  tick()
  if sum(N)!=K:continue
  if any(N[a]+N[b]<L[i] for i,(a,b) in enumerate(PAIRS)):continue
  answer.append(list(N))
 return sorted(answer)

def main():
 p=argparse.ArgumentParser();p.add_argument('--author',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);need(not out.exists(),'fresh independent output namespace')
 scope=json.loads((S/'pass23-T0-column-scope.json').read_text());author=json.loads(Path(a.author).read_text());need(author['status']=='PRIVATE_COMPLETE_JOINT_N_SUPPLIED_INTERVAL','author interval incomplete');interval=author['checked_interval'];need(interval in scope['partitions'],'declared interval')
 catpath=S/'pass23-T0-hub-friend-catalogue.json';cat=json.loads(catpath.read_text())['records'];need(hashlib.sha256(catpath.read_bytes()).hexdigest()==author['catalogue_sha256']==scope['catalogue_sha256'],'frozen new physical catalogue bytes')
 labelled,domain=carriers();need(labelled==author['labelled_carriers']==scope['labelled_carriers'] and domain==author['canonical_carriers'] and hashlib.sha256(canonical(domain)).hexdigest()==scope['canonical_carriers_sha256'],'entire independent actualT0 carrier stream')
 censuspath=S/'pass23-T0-producer.json';census=json.loads(censuspath.read_text());other=json.loads((S/'pass23-T0-polynomial.json').read_text());need(hashlib.sha256(censuspath.read_bytes()).hexdigest()==scope['census_sha256'],'frozen census bytes')
 need(canonical(census['inventory'])==canonical(other['inventory']) and len(census['inventory']['branches'])==84,'whole fresh complete two-engine census')
 allsupplied=[dict(survivor_ordinal=i,branch=[b[k] for k in ['Q','T','X','tau']],population=t['population']) for i,(b,t) in enumerate((b,t) for b in census['inventory']['branches'] for t in b['templates'] if not t['failures'])]
 need(len(allsupplied)==11077==scope['preliminary_populations'],'whole preliminary domain')
 need(hashlib.sha256(canonical([dict(branch=r['branch'],population=r['population']) for r in allsupplied])).hexdigest()==author['input_populations_sha256']==scope['input_populations_sha256'],'entire actual preliminary input')
 supplied=allsupplied[interval[0]:interval[1]];need(len(supplied)==len(author['records'])==interval[1]-interval[0],'exact complete supplied interval')
 types=json.loads(Path('round-two/six-code-3/four_hub_p21_endpoint_cut/expected.json').read_text())['types'];opcache={};records=[];total=0
 result=dict(agent='six-code-3',role='researcher',status='PRIVATE_INDEPENDENT_JOINT_N_INTERVAL_IN_PROGRESS',input_scope=author['input_scope'],checked_interval=interval,catalogue_sha256=author['catalogue_sha256'],author_result_sha256=hashlib.sha256(Path(a.author).read_bytes()).hexdigest(),records=records,complete_T0_scalar_census_claimed=True,complete_full_T0_N_classification_claimed=False,packing_realization_claimed=False,ordinary_bridges_formalized=False,external_review=False)
 for given,rec in zip(author['records'],supplied):
  begin=time.monotonic();transitions=0;factors={};polynomials={};stream=[];counts=Counter();complete=True
  need(given['survivor_ordinal']==rec['survivor_ordinal'] and given['branch']==rec['branch'] and given['population']==rec['population'],'same exact named population')
  K=sum(count*types[tid]['k'] for tid,count in rec['population']);need(K==given['K']==6+rec['branch'][0]+2*rec['branch'][2]+2*rec['branch'][3] and rec['branch'][1]==0,'same actualT0 K')
  def tick():
   nonlocal transitions,total
   transitions+=1;total+=1
   if transitions>500000 or time.monotonic()-begin>20:raise TimeoutError('INCOMPLETE unchanged independent joint-N guard')
  try:
   for i,c in enumerate(domain):
    fail=macro_failure(c);sets=[];N4=[]
    if fail is None:
     mask=c['global_HHH_mask'];zero=tuple(i for i,L in enumerate(c['HH_leave_totals']) if L==0);key=(mask,zero)
     if key not in opcache:opcache[key]=options(cat,mask,zero)
     ops=opcache[key];sets=[supported_N(rec['population'],a,target,ops,tick,factors,polynomials) for a,target in enumerate(c['D4'])]
     if any(not x for x in sets):fail='coordinate_friend_support'
     else:
      N4=joint(sets,K,c['HH_leave_totals'],tick)
      if not N4:fail='joint_support_sum_and_all_HH_quotas'
    counts[fail or 'coupled_support_feasible']+=1;stream.append(dict(carrier_index=i,first_failure=fail,coordinate_N_sets=sets,coupled_N4=N4))
  except TimeoutError:complete=False
  if complete:
   need(stream==given['carrier_results'],'every coordinate N set, joint N4 tuple and failure agrees')
   need(dict(counts)==given['failure_counts'],'every carrier failure count')
  record=dict(survivor_ordinal=rec['survivor_ordinal'],branch=rec['branch'],status='COMPLETE' if complete else 'INCOMPLETE',all_carrier_records_match=complete,transitions=transitions,surviving_carriers=sum(bool(x['coupled_N4']) for x in stream),coupled_support_tuples=sum(len(x['coupled_N4']) for x in stream),elapsed_seconds=time.monotonic()-begin);records.append(record)
  out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
  if rec['survivor_ordinal']%16==0 or record['surviving_carriers'] or not complete:print(json.dumps(record),flush=True)
  if not complete:result['status']='PRIVATE_INDEPENDENT_JOINT_N_INTERVAL_INCOMPLETE';break
 else:
  def noop():pass
  need(joint([[3]]*4,12,[6]*6,noop)==[[3,3,3,3]],'independent exact-quota positive control')
  need(not joint([[3]]*4,11,[6]*6,noop) and not joint([[3]]*4,12,[7,6,6,6,6,6],noop),'independent joint negatives')
  ops={999:[{(1,1)}]*4};factors={};polynomials={}
  need(supported_N([(999,2)],0,2,ops,noop,factors,polynomials)==[2],'independent friend-edge positive')
  need(not supported_N([(999,1)],0,1,ops,noop,factors,polynomials) and not supported_N([(999,3)],0,3,ops,noop,factors,polynomials),'independent friend negatives')
  result['status']='PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL';result['abstract_kernel_controls']=dict(positive=2,negative=4)
 result.update(total_transitions=total,surviving_populations=sum(r['surviving_carriers']>0 for r in records),total_coupled_tuples=sum(r['coupled_support_tuples'] for r in records));out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
 if result['status']!='PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL':raise SystemExit(2)

if __name__=='__main__':main()
