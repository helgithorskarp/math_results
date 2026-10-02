"""Private exact simultaneous-column relaxation of complete preliminary T2 rows.

Physical rows remain independently selectable by hub. Exact global support
sum and all six HH leave inequalities are coupled. The supplied35-branch T2 census is independently complete; this
computation checks every preliminary survivor. Passing a relaxation
would not supply a packing realization.
"""
import argparse,hashlib,itertools,json,time
from collections import Counter
from pathlib import Path

S=Path('round-two/six-code-3/scratch')
PAIRS=list(itertools.combinations(range(4),2));TRIPLES=list(itertools.combinations(range(4),3))
STATE_CAP=500000;TIME_CAP=20

def need(test,message):
 if not test:raise ValueError(message)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def carriers():
 output=[];labelled=0
 for mask in range(16):
  if mask.bit_count()!=2:continue
  covered=[TRIPLES[i] for i in range(4) if mask>>i&1]
  tab=tuple(sum(set(p)<=set(t) for t in covered) for p in PAIRS)
  for first in itertools.product(range(6),repeat=5):
   last=22-sum(first)
   if not 0<=last<=5:continue
   lam=first+(last,);L=tuple(14+t-3*l for t,l in zip(tab,lam))
   if min(L)<0 or max(L)>14:continue
   D=tuple(sum(l for p,l in zip(PAIRS,lam) if a in p)-(2 if a==0 else 6) for a in range(4))
   if min(D)<0:continue
   labelled+=1;orbit=[]
   for lights in itertools.permutations((1,2,3)):
    p=(0,)+lights
    mnew=sum(1<<i for i,t in enumerate(TRIPLES) if tuple(sorted(p[a] for a in t)) in covered)
    lnew=tuple(lam[PAIRS.index(tuple(sorted((p[a],p[b]))))] for a,b in PAIRS)
    orbit.append((mnew,lnew))
   if (mask,lam)!=min(orbit):continue
   output.append(dict(T=2,global_HHH_mask=mask,four_hub_words=0,lambda6=list(lam),D4=list(D),HH_leave_totals=list(L)))
 return labelled,output

def physical_options(catalogue,mask,zero):
 choices={}
 for r in catalogue:
  hhh=r['HHH_covered_mask']
  if hhh and (hhh.bit_count()!=1 or not hhh&mask):continue
  if r['HH_leave_mask']&zero:continue
  tid=r['type_id'];choices.setdefault(tid,[{} for _ in range(4)])
  for a in range(4):
   d=r['hub_deficits'][a];L=r['low_sat_friend_degrees'][a]
   need(d>0 or L==0,'LOW hub has no LOW-SAT friend')
   key=(d,L%2);req=L+1 if d else 0
   choices[tid][a][key]=min(choices[tid][a].get(key,100),req)
 return {tid:[tuple(sorted((d,p,req) for (d,p),req in x.items())) for x in roles] for tid,roles in choices.items()}

def support_sizes(population,role,target,options,tick):
 states={(0,0,0):0}
 for tid,count in population:
  opts=options.get(tid,[(),(),(),()])[role]
  for _ in range(count):
   following={}
   for (w,n,p),req in states.items():
    for d,dp,dr in opts:
     tick();nw=w+d;nn=n+bool(d);nr=max(req,dr)
     if nw>target or nr>target:continue
     key=(nw,nn,p^dp)
     following[key]=min(following.get(key,100),nr)
   states=following
   if not states:break
  if not states:break
 return sorted(n for (w,n,p),r in states.items() if w==target and p==0 and n>=r)

def coupled(sets,K,L,tick):
 answers=[];last=set(sets[3])
 for n0 in sets[0]:
  for n1 in sets[1]:
   if n0+n1<L[0]:continue
   for n2 in sets[2]:
    tick();n3=K-n0-n1-n2
    if n3 not in last:continue
    N=(n0,n1,n2,n3)
    if all(N[a]+N[b]>=l for (a,b),l in zip(PAIRS,L)):answers.append(list(N))
 return sorted(answers)

def new_macro_failure(c):
 mask=c['global_HHH_mask'];owned=[TRIPLES[i] for i in range(4) if mask>>i&1]
 tab=[sum(set(p)<=set(t) for t in owned) for p in PAIRS]
 if any(l<t for l,t in zip(c['lambda6'],tab)):return 'actual_distinct_HHH_owners'
 D=c['D4']
 if D[0]>12 or any(D[0]+D[a]>16 for a in (1,2,3)) or any(not 8<=D[a]+D[b]<=13 for a,b in [(1,2),(1,3),(2,3)]):return 'complementary_pair_role_bounds'
 return None

def inspect(rec,domain,catalogue,types,optioncache):
 begin=time.monotonic();visited=0;coordinate_cache={};results=[];counts=Counter()
 K=sum(count*types[tid]['k'] for tid,count in rec['population'])
 Q,T,X,tau=rec['branch'];need(T==2 and K==8+Q+2*X+2*tau,'same scalar K')
 def tick():
  nonlocal visited
  visited+=1
  if visited>STATE_CAP or time.monotonic()-begin>TIME_CAP:raise TimeoutError('INCOMPLETE unchanged joint-N guard')
 try:
  for index,c in enumerate(domain):
   failure=new_macro_failure(c);sets=[];answers=[]
   if failure is None:
    M=c['global_HHH_mask'];zero=sum(1<<i for i,L in enumerate(c['HH_leave_totals']) if L==0);okey=(M,zero)
    if okey not in optioncache:optioncache[okey]=physical_options(catalogue,M,zero)
    options=optioncache[okey]
    for a,target in enumerate(c['D4']):
     grouped=tuple((count,options.get(tid,[(),(),(),()])[a]) for tid,count in rec['population']);key=(grouped,target)
     if key not in coordinate_cache:coordinate_cache[key]=support_sizes(rec['population'],a,target,options,tick)
     sizes=coordinate_cache[key];sets.append(sizes)
    if any(not x for x in sets):failure='coordinate_friend_support'
    else:
     answers=coupled(sets,K,c['HH_leave_totals'],tick)
     if not answers:failure='joint_support_sum_and_all_HH_quotas'
   counts[failure or 'coupled_support_feasible']+=1
   results.append(dict(carrier_index=index,first_failure=failure,coordinate_N_sets=sets,coupled_N4=answers))
  status='COMPLETE_SUPPLIED_POPULATION_JOINT_N_RELAXATION'
 except TimeoutError:status='INCOMPLETE_SUPPLIED_POPULATION_JOINT_N_RELAXATION'
 return dict(status=status,survivor_ordinal=rec['survivor_ordinal'],branch=rec['branch'],population=rec['population'],K=K,visited_transitions=visited,carrier_results=results,failure_counts=dict(counts),surviving_carriers=sum(bool(x['coupled_N4']) for x in results),coupled_support_tuples=sum(len(x['coupled_N4']) for x in results),elapsed_seconds=time.monotonic()-begin)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=Path(args.output);need(not out.exists(),'fresh output namespace')
 prefix=out.with_suffix(out.suffix+'.cases');progress=out.with_suffix(out.suffix+'.progress.json')
 need(not prefix.exists() and not progress.exists(),'fresh resumable case namespace');prefix.mkdir()
 catpath=S/'pass18-hub-friend-catalogue.json';cat=json.loads(catpath.read_text());audit=json.loads((S/'pass18-independent-friend-catalogue.json').read_text());types=json.loads(Path('round-two/six-code-3/four_hub_p21_endpoint_cut/expected.json').read_text())['types']
 need(hashlib.sha256(catpath.read_bytes()).hexdigest()=='e6c013d3b32257181d6b880e1ef1a79154eab8d3a036cf0d1d1ac62de37b0fd8','literal catalogue SHA')
 need(audit['status']=='PRIVATE_COMPLETE_TWO_ENGINE_FRIEND_SIGNATURE_AGREEMENT' and audit['records_sha256']==hashlib.sha256(canonical(cat['records'])).hexdigest(),'complete prior physical catalogue record agreement')
 labelled,domain=carriers();need(labelled==3996 and len(domain)==696,'complete carrier counts; second generator checks every record')
 censuspath=S/'pass20-T2-producer.json'
 census=json.loads(censuspath.read_text());other=json.loads((censuspath.parent/'pass20-T2-polynomial.json').read_text())
 need(canonical(census['inventory'])==canonical(other['inventory']),'entire fresh two-engine T2 census')
 need(len(census['inventory']['branches'])==35,'all35 scalar branches')
 supplied=[dict(survivor_ordinal=i,branch=[b[k] for k in ['Q','T','X','tau']],population=t['population']) for i,(b,t) in enumerate((b,t) for b in census['inventory']['branches'] for t in b['templates'] if not t['failures'])]
 need(len(supplied)==266,'fixed complete preliminary T2 scope')
 need({tid for r in supplied for tid,count in r['population']}<=set(cat['relevant_type_ids']),'every preliminary type has complete physical catalogue coverage')
 output=dict(agent='six-code-3',role='researcher',status='PRIVATE_JOINT_N_CANDIDATE_LIST_IN_PROGRESS',input_scope='All266 preliminary survivors of the complete fresh35-branch1373-vector T2 census',catalogue_sha256=hashlib.sha256(catpath.read_bytes()).hexdigest(),input_populations_sha256=hashlib.sha256(canonical([dict(branch=r['branch'],population=r['population']) for r in supplied])).hexdigest(),canonical_carriers=domain,labelled_carriers=labelled,state_guard_per_population=STATE_CAP,time_guard_seconds_per_population=TIME_CAP,hubs_still_choose_physical_rows_independently=True,support_sum_and_all_six_HH_quotas_coupled=True,complete_T2_census_claimed=True,packing_realization_claimed=False,ordinary_bridges_formalized=False,external_review=False,records=[])
 optioncache={}
 for rec in supplied:
  result=inspect(rec,domain,cat['records'],types,optioncache);output['records'].append(result)
  casefile=prefix/(str(result['survivor_ordinal'])+'.json');casefile.write_bytes(canonical(result)+b'\n')
  progress.write_bytes(canonical(dict(agent='six-code-3',role='researcher',status='RESUMABLE_FULL_T2_N_PREFIX',completed_records=len(output['records']),last_record_status=result['status'],last_record_sha256=hashlib.sha256(casefile.read_bytes()).hexdigest(),case_directory=str(prefix),final_output=str(out),final_output_ready=False))+b'\n')
  print(json.dumps({k:v for k,v in result.items() if k!='carrier_results'}),flush=True)
  if result['status'].startswith('INCOMPLETE'):output['status']='PRIVATE_JOINT_N_CANDIDATE_LIST_INCOMPLETE';break
 else:
  def noop():pass
  need(coupled([[3]]*4,12,[6]*6,noop)==[[3,3,3,3]],'abstract exact-quota positive control')
  need(not coupled([[3]]*4,11,[6]*6,noop),'abstract support-sum negative control')
  need(not coupled([[3]]*4,12,[7,6,6,6,6,6],noop),'abstract one-HH-quota negative control')
  op={999:[((1,1,2),)]*4}
  need(support_sizes([(999,2)],0,2,op,noop)==[2],'abstract friend-edge positive control')
  need(not support_sizes([(999,1)],0,1,op,noop),'abstract friend support negative')
  need(not support_sizes([(999,3)],0,3,op,noop),'abstract friend parity negative')
  output['status']='PRIVATE_COMPLETE_JOINT_N_CANDIDATE_LIST';output['abstract_kernel_controls']=dict(positive=2,negative=4)
 output['surviving_populations']=sum(r['surviving_carriers']>0 for r in output['records']);output['total_coupled_tuples']=sum(r['coupled_support_tuples'] for r in output['records']);out.write_bytes(canonical(output)+b'\n')
 print(json.dumps(dict(status=output['status'],input_populations=len(supplied),completed_populations=len(output['records']),surviving_populations=output['surviving_populations'],total_coupled_tuples=output['total_coupled_tuples'],canonical_carriers=len(domain))),flush=True)

if __name__=='__main__':main()
