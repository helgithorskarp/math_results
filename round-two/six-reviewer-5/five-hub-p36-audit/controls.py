"""Semantic controls and whole marking transports; no author imports."""
import collections,itertools as it,json
import audit as a
import propagation as p
import graph_checks as g

def run(core,placement):
    # A separate weak-composition oracle exercises exact charge totals and
    # an unused inequality margin, rather than comparing a canned digest.
    toy=[(0,0,0,False,5,5,0,0,0,0),(0,1,0,True,5,4,0,4,0,1),
         (1,0,1,False,4,3,1,-3,0,0),(1,1,0,True,4,3,0,0,0,0)]
    checked=0
    for n in range(1,5):
        for counts in it.product(range(n+1),repeat=4):
            if sum(counts)!=n:continue
            E,K,Q,X,I,margin=(sum(v*t[j] for v,t in zip(counts,toy)) for j in (0,1,2,6,8,9))
            case={'E':E,'K':K,'Q':Q,'X':X//2,'N5':I,'margin_budget':margin+2}
            if X%2:continue
            # The real routine fixes thirteen rows; pad with its neutral unit.
            expected=[]
            for u1,q,ek in it.product(range(n+1),repeat=3):
                u0=13-u1-q-ek
                if u0<0:continue
                v=(u0,u1,q,ek)
                charges=tuple(sum(m*t[j] for m,t in zip(v,toy)) for j in (0,1,2,6,8,9))
                if charges[:5]==(E,K,Q,X,I) and charges[5]<=case['margin_budget']:expected.append(v)
            actual,_=a.populations(toy,case)
            a.need(actual==sorted(expected),'independent tiny weak-composition coefficient coverage and slack')
            checked+=1
    stars=json.loads((a.P/'fixtures.json').read_text())['stars']
    raw,capped,types=a.raw_and_types(stars)
    exceptions=[r for r in raw if r['I5']]
    a.need(len(exceptions)==8 and all(r['old_margin']==-3 and r['margin']==0 for r in exceptions),'all eight exceptional physical marks retained')
    physical={(r['star'],tuple(r['high_hubs'])):r for r in placement['records']}
    a.need(all(physical[r['star'],tuple(r['hubs'])]['exact_feasible_low_hub_placements']==1 for r in exceptions),'joint LOW filter retains every physical exceptional mark')
    a.need(sum(c['N5']==1 for c in core['all_scalar_cases'])==5 and core['N5_vector_counts'][1]==10,'all five exceptional scalar branches and ten vectors retained')
    case=next(c for c in core['all_scalar_cases'] if (c['T'],c['X'],c['tau'],c['Q'],c['N5'])==(1,0,0,3,0))
    closure=[r for r in case['vectors'] if r['all_original_cut_failures'][0]=='all_color_closure']
    a.need(len(closure)==1 and closure[0]['metrics']=={'U':6,'A':5,'C':3,'B':4,'D':29,'I':20,'C1':9,'C2':0,'B2':0,'R':5,'closed_root':5},'corrected first ordered closure case exact roles')
    wrongly_described=[r for r in case['vectors'] if r['metrics']['U']==6 and r['metrics']['C']==0 and r['metrics']['B']==7 and r['metrics']['D']==r['metrics']['I']==29]
    a.need(len(wrongly_described)==1 and wrongly_described[0]['all_original_cut_failures'][0]=='distinct_crossing','printed first bullet is a different earlier-excluded actual vector')
    demand_only=[r for r in placement['records'] if not r['exact_feasible_low_hub_placements'] and r['required_low_hub_friends']>r['low_hubs_available'] and all(v<=r['low_hubs_available'] for _,v in r['per_high_requirement'])]
    a.need(len(demand_only)==4,'four simultaneous bucket obstructions that individual inequalities miss')
    path=g.inspect(('A','C','B'),[(0,1,1),(1,2,2)])
    a.need(path['C2']==path['B2']==1 and not a.failures(path),'positive heavy crossing survives guarded cut')
    a.need(path['C1']+path['C2']<path['R']+path['D']-path['I']+path['B'],'incorrect summed demands would reject positive path')
    a.need(not a.failures({'D':0,'I':0,'C1':0,'C2':0,'B2':0,'R':0,'B':1,'closed_root':0}),'closure requires an actual radius root')
    return {'coefficient_weak_composition_cases':checked,'all8physical_exceptions_and5scalar_exception_branches_retained':True,
            'exact_printed_residual_correction_checked':True,'joint_LOW_budget_counterexamples':demand_only,
            'heavy_crossing_maximum_and_actual_root_positive_controls':True}

def transports(original):
    stars=json.loads((a.P/'fixtures.json').read_text())['stars']
    baseline={(r['star'],tuple(r['high_hubs'])):r for r in original['records']}
    records=[]
    for perm in ([16-x for x in range(17)],[(5*x+3)%17 for x in range(17)],[(7*x+11)%17 for x in range(17)]):
        inv={b:i for i,b in enumerate(perm)}
        renamed=[[sorted(perm[x] for x in word) for word in star] for star in stars]
        raw,_,_=a.raw_and_types(renamed);transformed,types=p.catalog(renamed,raw)
        a.need([list(t) for t in types]==[list(t) for t in original['propagation_feasible_types']],'complete refined type carrier invariant')
        for r in transformed['records']:
            key=r['star'],tuple(sorted(inv[x] for x in r['high_hubs']))
            old=baseline[key]
            a.need((r['low_hubs_available'],r['required_low_hub_friends'],r['exact_feasible_low_hub_placements'])==(old['low_hubs_available'],old['required_low_hub_friends'],old['exact_feasible_low_hub_placements']),'every actual transported marking exact placement count')
            a.need(sorted([inv[x],v] for x,v in r['per_high_requirement'])==old['per_high_requirement'],'every actual point role and friend quota transports')
        records.append({'permutation':perm,'all426marks_matched':True,'actual5Hplacements_checked':transformed['whole_physical_five_H_placements']})
    return records
