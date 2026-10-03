"""Exact ordinary row-sum projections of the complete377-case T0 remainder.

Same actual row options serve every hub simultaneously. Different linear
projections may still pick different rows, so passing is not realization.
Credited9797 supplies C_ab<=N_a+N_b-L_ab and simple friend-graph capacity.
No optional universal-C refinement is used. No method-priority claim.
"""
import argparse,hashlib,itertools,json,time
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch';W=Path('.');WS=S
PAIRS=list(itertools.combinations(range(4),2))
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(b,m):
 if not b:raise ValueError(m)
def features(r):
 d=r['hub_deficits'];p=[int(x>0) for x in d]
 return dict(deficit=d,positive_support=p,deficit_excess=[x-y for x,y in zip(d,p)],HH_leave=[(r['HH_leave_mask']>>i)&1 for i in range(6)],HIGH_pair_overlap=[p[a]*p[b] for a,b in PAIRS],LOW_SAT_friend_degree=r['low_sat_friend_degrees'])
DEFINITIONS=[(f,mask) for f,n in [('deficit',4),('positive_support',4),('deficit_excess',4),('HH_leave',6),('HIGH_pair_overlap',6),('LOW_SAT_friend_degree',4)] for mask in range(1,1<<n)]
def target_features(case):
 D=case['carrier']['D4'];N=case['N4'];L=case['carrier']['HH_leave_totals']
 return dict(deficit=D,positive_support=N,deficit_excess=[d-n for d,n in zip(D,N)],HH_leave=L,HIGH_pair_overlap=[N[a]+N[b]-L[i] for i,(a,b) in enumerate(PAIRS)],LOW_SAT_friend_degree=[n*(n-1) for n in N])
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();out=Path(args.output);need(not out.exists(),'fresh entire row-projection image')
 livepath=S/'pass23-T0-live-column-cases.json';cappath=S/'pass23-T0-capacity-producer.json';catpath=WS/'pass23-T0-hub-friend-catalogue.json'
 live=json.loads(livepath.read_text())['live_cases'];cap=json.loads(cappath.read_text());cat=json.loads(catpath.read_text())['records'];need(len(live)==len(cap['records'])==969,'full actual capacity image')
 need(cap['input_live_cases_sha256']==hashlib.sha256(livepath.read_bytes()).hexdigest() and cap['catalogue_sha256']==hashlib.sha256(catpath.read_bytes()).hexdigest(),'whole raw input provenance')
 supplied=[c for c,r in zip(live,cap['records']) if not r['excluded_by_weighted_capacity']];need(len(supplied)==377,'entire remaining377 candidates')
 grouped={}
 for i,r in enumerate(cat):
  if r['HHH_covered_mask']==0:grouped.setdefault(r['type_id'],[]).append((i,r,features(r)))
 result=dict(agent='six-code-3',role='researcher',status='PRIVATE_T0_ROW_PROJECTION_IMAGE_IN_PROGRESS',input_live_sha256=hashlib.sha256(livepath.read_bytes()).hexdigest(),input_capacity_sha256=hashlib.sha256(cappath.read_bytes()).hexdigest(),catalogue_sha256=hashlib.sha256(catpath.read_bytes()).hexdigest(),universal_C_refinement=False,definitions=[list(x) for x in DEFINITIONS],original_cases=969,input_cases=377,records=[],ordinary_bridges_formalized=False,independent_person_review=False,packing_realization_claimed=False)
 cache={};survivors=[]
 try:
  for case in supplied:
   start=time.monotonic();visited=0;N=case['N4'];cmin=[0]*4;ckey=(tuple(N),tuple(cmin));selected=[];bounds=[];failure=None
   for tid,count in case['population']:
    key=(ckey,tid)
    if key not in cache:
     allowed=[(i,r,f) for i,r,f in grouped.get(tid,[]) if all((d>0 and L<N[a]) or (d==0 and L==0) for a,(d,L) in enumerate(zip(r['hub_deficits'],r['low_sat_friend_degrees'])))]
     extrema=[]
     if allowed:
      for family,mask in DEFINITIONS:
       scores=[(sum(x for a,x in enumerate(f[family]) if mask>>a&1),i) for i,r,f in allowed];lo=min(scores);mx=max(v for v,i in scores);hi=min(i for v,i in scores if v==mx);extrema.append((lo[0],mx,lo[1],hi))
     cache[key]=(allowed,extrema)
    allowed,extrema=cache[key];selected.append(dict(type_id=tid,multiplicity=count,actual_catalogue_indices=[i for i,r,f in allowed]));visited+=len(grouped.get(tid,[]))*len(DEFINITIONS)
    if visited>500000 or time.monotonic()-start>20:raise RuntimeError('INCOMPLETE original500000state/20s case guard; no absence')
    if not allowed:failure=dict(reason='no_common_admissible_physical_row',type_id=tid);break
   if failure is None:
    targets=target_features(case)
    for j,(family,mask) in enumerate(DEFINITIONS):
     cells=[]
     for r in selected:
      lo,hi,li,hi_i=cache[ckey,r['type_id']][1][j];cells.append([r['type_id'],r['multiplicity'],lo,hi,li,hi_i])
     low=sum(c*lo for tid,c,lo,hi,li,hi_i in cells);high=sum(c*hi for tid,c,lo,hi,li,hi_i in cells);target=sum(x for a,x in enumerate(targets[family]) if mask>>a&1);upper_only=family in ['HIGH_pair_overlap','LOW_SAT_friend_degree'];ok=low<=target and (upper_only or target<=high)
     b=dict(family=family,subset_mask=mask,upper_only=upper_only,target=target,minimum=low,maximum=high,original_row_extrema=cells,passes=ok);bounds.append(b)
     if not ok:failure=dict(reason='ordinary_same_row_sum_bound',bound_index=j);break
   r=dict(live_case_ordinal=case['live_case_ordinal'],survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],carrier_index=case['carrier_index'],carrier=case['carrier'],N4=N,mandatory_universal_C_by_role=cmin,admissible_original_rows=selected,bounds=bounds,first_failure=failure,complete=True,packing_realization_claimed=False)
   result['records'].append(r)
   if failure is None:survivors.append(case['live_case_ordinal'])
   prefix=out.with_suffix(out.suffix+'.cases');prefix.mkdir(exist_ok=True);casefile=prefix/(str(case['live_case_ordinal'])+'.json');casefile.write_bytes(canonical(r)+b'\n')
   out.with_suffix(out.suffix+'.progress.json').write_bytes(canonical(dict(agent='six-code-3',role='researcher',status='RESUMABLE_T0_SAME_ROW_PROJECTION_PREFIX_NO_ABSENCE',completed_cases=len(result['records']),last_case_ordinal=case['live_case_ordinal'],last_case_sha256=hashlib.sha256(casefile.read_bytes()).hexdigest(),case_directory=str(prefix),whole_output_ready=False))+b'\n')
   if len(result['records'])%64==0:print(json.dumps(dict(checked=len(result['records']),surviving=len(survivors))),flush=True)
  result.update(status='PRIVATE_COMPLETE_T0_SAME_ROW_PROJECTION_IMAGE',checked_cases=len(result['records']),surviving_case_ordinals=survivors,surviving_cases=len(survivors),excluded_cases=len(supplied)-len(survivors),complete_supplied_case_order=[r['live_case_ordinal'] for r in result['records']])
 except BaseException as exc:
  result.update(status='INCOMPLETE_OR_FAILED_NO_MATHEMATICAL_ABSENCE',failure=type(exc).__name__+': '+str(exc));raise
 finally:
  out.write_bytes(canonical(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('records','definitions','complete_supplied_case_order','surviving_case_ordinals')},sort_keys=True),flush=True)
if __name__=='__main__':main()
