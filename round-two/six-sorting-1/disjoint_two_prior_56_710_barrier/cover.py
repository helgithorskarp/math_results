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
    print(json.dumps(cover,sort_keys=True))


if __name__=='__main__':main()
