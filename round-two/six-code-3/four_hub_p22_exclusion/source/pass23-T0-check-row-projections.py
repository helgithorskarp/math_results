"""Original literal star witnesses and separate exact row-sum audit.

No import from the projection producer or its compiler. Reconstruct every
physical signature witness, then independently select whole admissible
rows and inspect the entire ordered bound prefix for every original case.
Scope remains conditional on the complete star interface and prior cuts.
"""
import argparse,hashlib,itertools,json,time
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch';W=Path('.');WS=S
PAIRS=list(itertools.combinations(range(4),2));TRIPLES=list(itertools.combinations(range(4),3))
FAMILIES=[('deficit',4),('positive_support',4),('deficit_excess',4),('HH_leave',6),('HIGH_pair_overlap',6),('LOW_SAT_friend_degree',4)]
FIELDS=['e','k','q','eligible','h','g1_S','ss_excess','hub_weight','psi','margin','ss_hist']
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(b,m):
 if not b:raise ValueError(m)
def key(r):return tuple(tuple(r[f]) if f=='ss_hist' else r[f] for f in FIELDS)
def literal_features(cat,fixtures,basis):
 compiled={};rebuilt=[];index={key(r):i for i,r in enumerate(basis)}
 for rank,r in enumerate(cat):
  fi=r['witness']['fixture'];roles=r['witness']['hub_roles'];need(len(roles)==len(set(roles))==4 and all(0<=p<17 for p in roles),'original four distinct hub labels')
  if fi not in compiled:
   blocks=[set(b) for b in fixtures[fi]];rho=[sum(p in b for b in blocks) for p in range(17)];delta=[5-v for v in rho];covered={frozenset(e) for b in blocks for e in itertools.combinations(sorted(b),2)};triples={frozenset(t) for b in blocks for t in itertools.combinations(sorted(b),3)};leave=[{q for q in range(17) if q!=p and frozenset((p,q)) not in covered} for p in range(17)];high={p for p,d in enumerate(delta) if d};low=set(range(17))-high
   need(len(blocks)==20 and len(covered)==120 and sum(delta)==5 and min(delta)>=0,'original star ownership/deficit properties')
   compiled[fi]=(blocks,delta,triples,leave,high,low)
  blocks,delta,triples,leave,high,low=compiled[fi];H=set(roles);J=H&high;d=[delta[p] for p in roles];positive=[int(p in high) for p in roles];L=[len(leave[p]&(low-H)) for p in roles];HH=[int(roles[b] in leave[roles[a]]) for a,b in PAIRS];HHH=sum(1<<i for i,t in enumerate(TRIPLES) if frozenset(roles[a] for a in t) in triples);isolated={p for p in high if not leave[p]&high};eligible=sum(1<<a for a,p in enumerate(roles) if p in isolated);counts=[sum(len(b&H)==j for b in blocks) for j in range(5)]
  need(d==r['hub_deficits'] and L==r['low_sat_friend_degrees'] and sum(v<<i for i,v in enumerate(HH))==r['HH_leave_mask'] and HHH==r['HHH_covered_mask'] and eligible==r['eligible_hub_mask'] and counts==r['word_hub_counts'],'entire original physical signature critical fields')
  hist=[sum(delta[p]==v for p in high-H) for v in range(1,6)];h=len(high);e=5-h;k=len(J);q=sum(bool(set((a,b))&J) for a,b in itertools.combinations(sorted(high),2) if b in leave[a]);elig=bool(isolated&J);g1=hist[0];sigma=sum((v-1)*hist[v-1] for v in range(1,6));w=sum(d);psi=g1 if not e and elig else -g1 if e and not elig else 0;row=dict(e=e,k=k,q=q,eligible=elig,h=h,g1_S=g1,ss_excess=sigma,hub_weight=w,psi=psi,margin=psi-3*(k-e-q),ss_hist=hist)
  need(index[key(row)]==r['type_id'],'definition-level physical type identity')
  rebuilt.append(dict(type_id=r['type_id'],HHH=HHH,D=d,N=positive,Z=[x-y for x,y in zip(d,positive)],HH=HH,C=[positive[a]*positive[b] for a,b in PAIRS],LF=L))
 return rebuilt

def main():
 p=argparse.ArgumentParser();p.add_argument('--author',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);need(not out.exists(),'fresh independent row audit')
 ap=Path(a.author);given=json.loads(ap.read_text());need(given['status']=='PRIVATE_COMPLETE_T0_SAME_ROW_PROJECTION_IMAGE' and given['universal_C_refinement'] is False,'complete base image only; optional unneeded refinement not a premise')
 livepath=S/'pass23-T0-live-column-cases.json';cappath=S/'pass23-T0-capacity-producer.json';catpath=WS/'pass23-T0-hub-friend-catalogue.json';fixturepath=R/'four_hub_p21_endpoint_cut/fixtures.json';basispath=R/'four_hub_p21_endpoint_cut/expected.json'
 need(given['input_live_sha256']==hashlib.sha256(livepath.read_bytes()).hexdigest() and given['input_capacity_sha256']==hashlib.sha256(cappath.read_bytes()).hexdigest() and given['catalogue_sha256']==hashlib.sha256(catpath.read_bytes()).hexdigest(),'all complete raw original input provenance')
 need(hashlib.sha256(fixturepath.read_bytes()).hexdigest()=='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7','original generic23 fixture pin')
 cat=json.loads(catpath.read_text())['records'];fixtures=json.loads(fixturepath.read_text())['stars'];basis=json.loads(basispath.read_text())['types'];rows=literal_features(cat,fixtures,basis)
 definitions=[(f,m) for f,n in FAMILIES for m in range(1,2**n)];need(given['definitions']==[list(x) for x in definitions],'entire declared mathematical projection domain')
 mapping=dict(deficit='D',positive_support='N',deficit_excess='Z',HH_leave='HH',HIGH_pair_overlap='C',LOW_SAT_friend_degree='LF')
 live=json.loads(livepath.read_text())['live_cases'];cap=json.loads(cappath.read_text())['records'];cases=[c for c,r in zip(live,cap) if not r['excluded_by_weighted_capacity']];need(len(cases)==len(given['records'])==377,'entire actual377-case remainder')
 groups={}
 for i,r in enumerate(rows):
  if r['HHH']==0:groups.setdefault(r['type_id'],[]).append(i)
 cache={};records=[];survivors=[]
 for case,original in zip(cases,given['records']):
  start=time.monotonic();visited=0;N=case['N4'];D=case['carrier']['D4'];HHL=case['carrier']['HH_leave_totals'];selected=[];failure=None;bounds=[]
  for tid,count in case['population']:
   ck=(tuple(N),tid)
   if ck not in cache:
    allowed=[]
    for i in groups.get(tid,[]):
     r=rows[i];ok=True
     for role in range(4):
      if r['D'][role]==0:
       if r['LF'][role]!=0:ok=False
      elif r['LF'][role]>=N[role]:ok=False
     if ok:allowed.append(i)
    extrema=[]
    if allowed:
     for family,mask in definitions:
      coords=[j for j in range(len(rows[allowed[0]][mapping[family]])) if mask&(2**j)];values={i:sum(rows[i][mapping[family]][j] for j in coords) for i in allowed};lo=min(values.values());hi=max(values.values());extrema.append((lo,hi,min(i for i in allowed if values[i]==lo),min(i for i in allowed if values[i]==hi)))
    cache[ck]=(allowed,extrema)
   allowed,extrema=cache[ck];selected.append(dict(type_id=tid,multiplicity=count,actual_catalogue_indices=allowed));visited+=len(groups.get(tid,[]))*len(definitions)
   if visited>500000 or time.monotonic()-start>20:raise RuntimeError('INCOMPLETE original500000state/20s case guard; no absence')
   if not allowed:failure=dict(reason='no_common_admissible_physical_row',type_id=tid);break
  if failure is None:
   targets=dict(deficit=D,positive_support=N,deficit_excess=[D[j]-N[j] for j in range(4)],HH_leave=HHL,HIGH_pair_overlap=[N[x]+N[y]-HHL[j] for j,(x,y) in enumerate(PAIRS)],LOW_SAT_friend_degree=[n*(n-1) for n in N])
   for j,(family,mask) in enumerate(definitions):
    cells=[]
    for entry in selected:
     lo,hi,li,hi_i=cache[tuple(N),entry['type_id']][1][j];cells.append([entry['type_id'],entry['multiplicity'],lo,hi,li,hi_i])
    lower=sum(c*x for tid,c,x,y,li,hi in cells);upper=sum(c*y for tid,c,x,y,li,hi in cells);target=sum(targets[family][k] for k in range(len(targets[family])) if (2**k)&mask);uonly=family in ['HIGH_pair_overlap','LOW_SAT_friend_degree'];passes=not lower>target and (uonly or not upper<target);bounds.append(dict(family=family,subset_mask=mask,upper_only=uonly,target=target,minimum=lower,maximum=upper,original_row_extrema=cells,passes=passes))
    if not passes:failure=dict(reason='ordinary_same_row_sum_bound',bound_index=j);break
  expected=dict(live_case_ordinal=case['live_case_ordinal'],survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],carrier_index=case['carrier_index'],carrier=case['carrier'],N4=N,mandatory_universal_C_by_role=[0]*4,admissible_original_rows=selected,bounds=bounds,first_failure=failure,complete=True,packing_realization_claimed=False)
  need(canon(expected)==canon(original),'every original physical choice, entire ordered bound prefix and first failure agrees')
  records.append(expected)
  if failure is None:survivors.append(case['live_case_ordinal'])
 need(given['complete_supplied_case_order']==[r['live_case_ordinal'] for r in records] and given['surviving_case_ordinals']==survivors,'entire original case order/surviving list')
 result=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_T0_LITERAL_ROW_PROJECTION_AUDIT',author_sha256=hashlib.sha256(ap.read_bytes()).hexdigest(),all_entire_records_match=True,records=records,original_physical_witnesses_checked=len(rows),original_literal_features_sha256=hashlib.sha256(canon(rows)).hexdigest(),checked_cases=len(records),excluded_cases=len(records)-len(survivors),surviving_cases=len(survivors),surviving_case_ordinals=survivors,ordinary_bridges_formalized=False,independent_person_review=False,optional_universal_C_bridge_used=False,packing_realization_claimed=False)
 out.write_bytes(canon(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('records','surviving_case_ordinals')},sort_keys=True))
if __name__=='__main__':main()
