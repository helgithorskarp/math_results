"""Exact standalone LOW-hub placement test; fresh direct physical subset oracle.

No author programs/expected imported. Catalogue completeness8933 is credited.
This is local feasibility for the propagation inequalities, not a code.
"""
import collections,itertools as it,math,json,pathlib
import audit as a

def catalog(stars,raw):
    lookup={(r['star'],tuple(r['hubs'])):r for r in raw}
    groups=[];direct_counts=collections.Counter();first_witness={};tested=0
    for index,star in enumerate(stars):
        blocks=[set(w) for w in star]
        pairs={tuple(q) for w in blocks for q in it.combinations(sorted(w),2)}
        deg=[sum(p in w for w in blocks) for p in range(17)]
        delta=[5-v for v in deg];high=[p for p in range(17) if delta[p]];low=[p for p in range(17) if not delta[p]]
        low_friends={p:set() for p in high};hh={p:0 for p in high}
        for x,y in it.combinations(range(17),2):
            if (x,y) in pairs:continue
            if x in low and y in low:a.need(False,'physical no-low-low')
            if x in high and y in high:hh[x]+=1;hh[y]+=1
            elif x in low:low_friends[y].add(x)
            else:low_friends[x].add(y)
        a.need(set().union(*low_friends.values())==set(low),'all LOW leave friends partition')
        a.need(sum(map(len,low_friends.values()))==len(low),'LOW friend buckets disjoint')
        a.need(all(len(low_friends[p])==1+3*delta[p]-hh[p] for p in high),'physical friend-bucket degrees')
        groups.append((high,low,delta,hh,low_friends))
        # Actual complete H placement, no high-mark-only generation.
        for hubtuple in it.combinations(range(17),5):
            tested+=1;H=set(hubtuple)
            good=all(delta[p]+len(low_friends[p]-H)<=5+4*int(p in H) for p in high)
            if good:
                key=(index,tuple(p for p in high if p in H));direct_counts[key]+=1
                first_witness.setdefault(key,list(hubtuple))
    records=[];refined=[];point_rows=[]
    for key,r in sorted(lookup.items()):
        high,low,delta,hh,friends=groups[r['star']];H=set(r['hubs']);N=5-len(H)
        need_by_point={p:max(0,4*delta[p]-hh[p]-4-4*int(p in H)) for p in high}
        demand=sum(need_by_point.values())
        # Coefficient of x^N in independent disjoint-binomial friend factors.
        coeff=[1]+[0]*N
        for p in high:
            size=len(friends[p]);required=need_by_point[p];next_coeff=[0]*(N+1)
            for used,count in enumerate(coeff):
                for j in range(required,min(size,N-used)+1):next_coeff[used+j]+=count*math.comb(size,j)
            coeff=next_coeff
        expected=coeff[N]
        actual=direct_counts.get(key,0)
        a.need(actual==expected,'EVERY raw mark physical subset count equals binomial coefficient')
        a.need(bool(actual)==(demand<=N),'exact standalone local placement criterion')
        rr={'star':key[0],'high_hubs':list(key[1]),'low_hubs_available':N,'required_low_hub_friends':demand,
            'per_high_requirement':[[p,need_by_point[p]] for p in high],
            'exact_feasible_low_hub_placements':actual,'first_actual_full_H':first_witness.get(key)}
        records.append(rr)
        # Individual point inequalities (2), a strictly weaker intermediate.
        if all(4*delta[p]-hh[p]+len(H)<=9+4*int(p in H) for p in high):point_rows.append(r)
        if actual:
            sat=[p for p in high if p not in H]
            a.need(all(delta[p]<=2 for p in sat) and all(delta[p]<=3 for p in H),'improved carrier implies old pair caps')
            refined.append({**r,'c1':sum(delta[p]==1 for p in sat),'c2':sum(delta[p]==2 for p in sat),'mu':r['margin']})
    types=sorted({tuple(r[k] for k in a.FIELDS) for r in refined})
    return {'whole_physical_five_H_placements':tested,'whole_positive_five_H_placements':sum(direct_counts.values()),
            'raw_marks':len(raw),'individual_point_bound_marks':len(point_rows),
            'propagation_feasible_high_marks':len(refined),'propagation_feasible_types':types,
            'whole_mark_records_sha256':a.digest(records),'records':records,
            'boundary':'Exact local placements satisfying only the forced-friend propagation inequalities. Positive placements/types are not actual 71-word packings; complete star coverage8933 remains imported.'},types

def run():
    stars=json.loads((a.P/'fixtures.json').read_text())['stars']
    raw,capped,types=a.raw_and_types(stars)
    record,refined_types=catalog(stars,raw)
    cases=[];counter=collections.Counter();inventory=[]
    for case in a.scalars():
        vectors,states=a.populations(refined_types,case)
        for vector in vectors:
            metrics=a.metrics(refined_types,vector);failed=a.failures(metrics)
            a.need(bool(failed),'propagation survivor must obey original exclusion')
            counter[failed[0]]+=1
            inventory.append([case,[[list(c),n] for c,n in zip(refined_types,vector) if n]])
        cases.append({**case,'vectors':len(vectors),'count_DAG_states':states})
    record.update({'refined27case_counts':cases,'refined_total_vectors':len(inventory),
                   'refined_full_inventory_sha256':a.digest(inventory),'refined_ordered_failures':dict(counter),
                   'ordinary_filter':'sum_high max(0,4delta-4-b_HH-4d_global)<=m-k. Exact local LOW hub placement criterion, not a realizability claim.'})
    return record

if __name__=='__main__':
    record=run();raw=a.encode(record);(a.P/'propagation-record.json').write_bytes(raw)
    print(json.dumps({k:v for k,v in record.items() if k not in ('records','propagation_feasible_types','refined27case_counts')},indent=2))
    print('sha256',a.digest(record))
