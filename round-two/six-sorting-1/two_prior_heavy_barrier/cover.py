"""Private complete two-equal-event cover plus one bounded six-port pilot.
Full six-input functions; exact original39 activity/minimum image predicates.
Pilot is a producer proposal, not an independently checked branch exclusion.
"""
from collections import Counter, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent


def need(test,message):
    if not test:raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def stopped():
    from controls import operations_blocked
    return operations_blocked()


def table(word,ports):
    index={p:i for i,p in enumerate(ports)};rows=[]
    for x in range(1<<len(ports)):
        for a,b in word:
            a,b=index[a],index[b]
            if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
        rows.append(x)
    return tuple(rows)


def main():
    start=time.monotonic();need(not stopped(),'Operations barrier: no new pilot')
    units=(5,6,7,9,10);leaves=units+(11,);canonical=[]
    for leftover in units:
        rest=[p for p in units if p!=leftover]
        for mate in rest[1:]:
            first=sorted([rest[0],mate]);second=[p for p in rest if p not in first]
            canonical.append([first,second])
    for a,b in combinations(units,2):canonical.append([[a,b],[b,11]])
    canonical.sort();need(len(canonical)==25,'Canonical two-merge tree count differs')
    initial=tuple([(p,6) for p in units]+[(11,7)])
    ordered=[]
    for i,j in combinations(range(6),2):
        a,da=initial[i];b,db=initial[j]
        if da!=db:continue
        state=tuple(sorted([r for k,r in enumerate(initial) if k not in (i,j)]+[(max(a,b),da+1)]))
        for u,v in combinations(range(5),2):
            p,d=state[u];q,e=state[v]
            if d==e:ordered.append([sorted([a,b]),sorted([p,q])])
    actual={table(w,leaves) for w in ordered};proposed={table(w,leaves) for w in canonical}
    need(len(ordered)==40 and actual==proposed and len(actual)==25,'Whole64-row event cover differs')
    cover={'agent':'six-sorting-1','role':'researcher','status':'PRIVATE_COMPLETE40_EVENT_ORDERS_MATCH25_FULL64_ROW_FUNCTIONS',
           'canonical_words':canonical,'event_orders':40,'distinct_full_six_input_functions':25,
           'full_function_set_sha256':digest(sorted(actual)),'source_dependency':'f47e57677011488966488f68228562643bed2b3c',
           'scope':'Exactly two prior equal HIGH merges after literal B23;L4; no preparation or singleton exclusion.'}
    (ROOT/'work/two-prior-high-complete-cover.json').write_text(json.dumps(cover,indent=2)+'\n')
    base=json.loads((ROOT/'prior/work/low26-partner4-construction-pilot.json').read_text())['core_states']
    domains=json.loads((ROOT/'prior/work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    need(len(base)==157 and len(domains)==39,'Prior checked exact original images differ')
    prefix=canonical[0];columns=[sum((x>>j&1)<<i for i,x in enumerate(base)) for j in range(10)]
    live=dict(initial)
    for a,b in prefix:
        d=live[a];need(d==live[b],'Not an equal HIGH merge');del live[a];live[b]=d+1
        columns[a-2],columns[b-2]=columns[a-2]&columns[b-2],columns[a-2]|columns[b-2]
    dead=tuple(p for p in range(2,12) if p not in live);need(len(dead)==6 and dead[0]==2,'Six dead-port map differs')
    patterns=[sum((columns[p-2]>>i&1)<<j for j,p in enumerate(dead)) for i in range(157)]
    bins=[sum(1<<i for i,x in enumerate(patterns) if x==k) for k in range(64)]
    minimum=sum(1<<i for i,x in enumerate(base) if x==1023)
    init=tuple(sum((x>>j&1)<<x for x in range(64)) for j in range(6))
    queue=deque([init]);words={init:()};locks=[];counts=Counter();deadline=time.monotonic()+5
    status='COMPLETE_PRIVATE_MINIMUM_ABSORBING_SIX_VARIABLE_ACTIVITY_CLOSURE_PRODUCER_ONLY'
    while queue:
        if time.monotonic()>deadline or len(words)>=20000 or stopped():
            status='INCOMPLETE_OPERATIONAL_TIME_STATE_OR_PAUSE_GUARD_NOT_AN_EXCLUSION';break
        f=queue.popleft();counts['expanded_full_functions']+=1
        image=[sum(bins[k] for k in range(64) if c>>k&1) for c in f]
        wrong=image[0]^minimum
        lock=next((r['original_LOW_mask'] for r in domains if not wrong&r['core_image_index_mask']),None)
        if wrong and lock is not None:
            locks.append({'full_function_sha256':digest(f),'word':words[f],'original_LOW_mask':lock});counts['minimum_lock_absorbed']+=1;continue
        for i,j in combinations(range(6),2):
            active=image[i]&~image[j]
            if not all(active&r['core_image_index_mask'] for r in domains):
                counts['inactive_original_domain_edges']+=1;continue
            fresh=list(f);fresh[i],fresh[j]=f[i]&f[j],f[i]|f[j];fresh=tuple(fresh)
            need(fresh!=f,'Admissible next comparison is an identity');counts['admissible_edges']+=1
            if fresh not in words:
                words[fresh]=words[f]+((dead[i],dead[j]),);queue.append(fresh)
    rows=[{'full_six_variable_columns':f,'shortest_word':w} for f,w in sorted(words.items())]
    out={'agent':'six-sorting-1','role':'researcher','status':status,'HIGH_word':prefix,'HIGH_live_costs':sorted(live.items()),
         'dead_preparation_ports':dead,'complete_full_functions_seen':len(words),'queue_unexpanded':len(queue),'census':dict(counts),
         'shortest_lengths':dict(Counter(map(len,words.values()))),'functions':rows,'minimum_lock_proposals':locks,
         'full_functions_sha256':digest(rows),'cover_sha256':digest(cover),'pilot_seconds':time.monotonic()-start,
         'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'independent_pilot_replay_complete':False,
         'scope':'ONE of25 exact-two-prior-HIGH routes only, producer necessary six-port closure with proposed minimum-lock absorption; no singleton/tail/branch/global exclusion.'}
    (ROOT/'work/two-prior-high-six-port-pilot.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('functions','minimum_lock_proposals')},sort_keys=True))


if __name__=='__main__':main()
