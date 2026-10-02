"""New9594 audit; explicitly owned prior raw/DAG engines reused.
All complete records rebuilt before access to target executable or EXPECTED.
"""
import collections,hashlib,itertools as it,json,math,pathlib,time
import census as c
P=pathlib.Path(__file__).resolve().parent
need=c.need;encode=c.encode;digest=c.digest
F20=(1,1,0,True,4,3,0,0,0,0)
F22=(1,1,1,False,4,3,0,-3,0,0)

def independent_scalars():
    rows=[]
    for T in range(1,6):
      for X in range(5):
       for tau in range(3):
        for N5 in range(4):
         slack=11-2*T-2*X-4*tau-3*N5
         for surplus in range(max(0,slack+1)):
          Q=4*N5+surplus;E=14-T-2*tau-Q;K=17-E+2*X
          margin=3*(E+Q+N5-K)
          if E>=0 and K>=0 and margin>=0:
           rows.append(dict(N5=N5,T=T,X=X,tau=tau,Q=Q,E=E,K=K,margin_budget=margin))
    return sorted(rows,key=lambda x:(x['N5'],x['T'],x['X'],x['tau'],x['Q']))

def local_quotas(raw):
    # Reproved prior joint LOW-hub filter. Full independent direct placement
    # comparison is part of the already sufficient owned9527 evidence.
    good=[];records=[]
    for r in raw:
      H=set(r['hubs']);d=r['delta'];adj=collections.Counter(p for edge in r['high_edges'] for p in edge)
      quotas=[max(0,4*d[p]-4-adj[p]-4*int(p in H)) for p in r['high']]
      valid=sum(quotas)<=5-r['k'];records.append([r['star'],r['hubs'],quotas,valid])
      if valid:
       sat=[p for p in r['high'] if p not in H]
       good.append(tuple([r[k] for k in c.FIELDS[:5]]+[sum(d[p]==1 for p in sat),sum(d[p]==2 for p in sat),r['psi'],r['I5'],r['margin']]))
    return sorted(set(good)),records

def enhanced_metrics(types,v):
    r=c.metrics(types,v);r['DV']=sum(n*t[5] for n,t in zip(v,types) if t[0]==0 and t[3])
    r['DA']=r['D']-r['DV'];r['I_even']=r['I']-r['I']%2
    r['n20']=sum(n for n,t in zip(v,types) if t==F20)
    r['n22']=sum(n for n,t in zip(v,types) if t==F22)
    r['hub3']=sum(n for n,t in zip(v,types) if 5-t[5]-2*t[6]>2*t[1])
    return r

def all_cuts(case,r):
    out=c.failures(r)
    if case['N5']:out.append('isolated_exception_radius')
    if r['n20']>3:out.append('complement_triangle_n20')
    if case['T']==1:
      if r['n20']>1:out.append('T1_n20')
      if r['n22']>4:out.append('T1_n22')
      if r['hub3']:out.append('T1_hub_weight')
      if r['R'] and (r['B'] or r['DV']) and r['C1']<r['DV']+r['R']:out.append('eligible_unit_plus_root')
    return out

def compositions(n,k):
    for cuts in it.combinations(range(n+k-1),k-1):
      a=(-1,)+cuts+(n+k-1,);yield tuple(a[j+1]-a[j]-1 for j in range(k))

def ordered_controls():
    # ALL labelled nonnegative column totals of mass17 with pair sums<=10.
    # Check exact extrema and enumerate eligible heavy column demands.
    totals=[];records=[]
    for D in compositions(17,5):
      if any(D[a]+D[b]>10 for a,b in it.combinations(range(5),2)):continue
      max_n=0;witness=None
      for n in it.product(*(range(min(3,D[a]//2)+1) for a in range(5))):
       if all(not n[a] or D[a]>=max(2*n[a],4+n[a]) for a in range(5)):
        if sum(n)>max_n:max_n=sum(n);witness=n
      need(max_n<=3,'abstract complete eligible-two population bound')
      totals.append(D);records.append([D,max_n,witness])
    need(max(map(max,totals))==7,'exact abstract individual-column maximum7')
    # Complete ordered HH pattern atT1: actual single covered HHH triple.
    pairs=list(it.combinations(range(5),2));triples=list(it.combinations(range(5),3));t1=[]
    for shortages in compositions(4,10):
      f=[sum(shortages[i] for i,e in enumerate(pairs) if a in e) for a in range(5)]
      D=tuple(5-x for x in f)
      for tri in triples:
       tt=[int(set(e)<=set(tri)) for e in pairs]
       if any(1+3*shortages[i]+tt[i]>D[a]+D[b] for i,(a,b) in enumerate(pairs)):continue
       need(min(D)>=1 and max(D)<=5 and D.count(5)<=1,'T1 exact ordinary shortage consequences')
       best20=best22=0
       for n in it.product(*(range(D[a]//2+1) for a in range(5))):
        if all(not n[a] or D[a]>=max(2*n[a],4+n[a]) for a in range(5)):best20=max(best20,sum(n))
        if all(not n[a] or D[a]>=max(2*n[a],3+n[a]) for a in range(5)):best22=max(best22,sum(n))
       need(best20<=1 and best22<=4,'T1 complete support-demand consequences')
       t1.append([shortages,tri,D,best20,best22])
    need(bool(t1),'positive abstract T1 controls do not prove physical realization')
    return dict(all_mass17_totals=math.comb(21,4),pair_sum10_totals=len(totals),full_eligible_demand_records_sha256=digest(records),max_eligible_n20=max(r[1] for r in records),
      all_ordered_T1_carriers=math.comb(13,9)*10,T1_quota_admissible_carriers=len(t1),full_T1_records_sha256=digest(t1),T1_max_n20=max(r[3] for r in t1),T1_max_n22=max(r[4] for r in t1),
      T1_extremal_abstract_n22=[r for r in t1 if r[4]==4][:1])

def compute():
    stars=json.loads((P/'fixtures.json').read_text())['stars'];raw,capped,types=c.raw_and_types(stars)
    cases=c.scalars();need(cases==independent_scalars(),'whole rectangular/slack scalar inventory')
    need(F20 in types and F22 in types,'actual heavy role coordinates20/22')
    refined,qrecords=local_quotas(raw);out=[];inventory=[];order=collections.Counter();refine_order=collections.Counter();refine_total=0
    t1_residuals=[]
    for case in cases:
      vectors,states=c.populations(types,case);records=[]
      for v in vectors:
       r=enhanced_metrics(types,v);bad=all_cuts(case,r);need(bool(bad),'complete P36 vector not excluded')
       sparse=[[list(t),n] for t,n in zip(types,v) if n];record=dict(population=sparse,metrics=r,all_failures=bad)
       records.append(record);inventory.append([case,record]);order[bad[0]]+=1
       if case['T']==1 and bad==['eligible_unit_plus_root']:t1_residuals.append([case,record])
       if all(t in refined for t,n in zip(types,v) if n):refine_total+=1;refine_order[bad[0]]+=1
      out.append({**case,'states':states,'vectors':records})
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',new_author_executable_expected_unread_at_core_seal=True,
      credited_owned_helpers='9422 literal set/bit marks and9527 coefficient DAG; generic8933/imported8323/9249/9367/9476 remain explicit premises',
      raw_marks=len(raw),raw_sha256=digest(raw),capped_marks=len(capped),types=types,all_cases=out,total_vectors=len(inventory),
      whole_inventory_sha256=digest(inventory),ordered_failures=dict(order),simple_endpoint_only_residuals=t1_residuals,
      joint_local_filter_types=refined,full_426_quota_sha256=digest(qrecords),joint_local_filter_vectors=refine_total,joint_local_filter_ordered_failures=dict(refine_order),
      ordered_column_controls=ordered_controls())

if __name__=='__main__':
    r=compute();b=encode(r);(P/'core-record.json').write_bytes(b)
    print(json.dumps(dict(sha256=hashlib.sha256(b).hexdigest(),cases=len(r['all_cases']),vectors=r['total_vectors'],failures=r['ordered_failures'],
      states=sum(x['states'] for x in r['all_cases']),simple_last=len(r['simple_endpoint_only_residuals']),quota_vectors=r['joint_local_filter_vectors'],column_controls=r['ordered_column_controls']),indent=2))
