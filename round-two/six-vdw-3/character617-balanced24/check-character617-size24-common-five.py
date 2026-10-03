"""Whole physical-column legality plus independently counted completeness.

Input lists are checked against the full column-factor DP from the separate
capacity checker. Degree calculation adds reverse-adjacency columns with
bit-sliced binary counters, instead of per-row intersection population counts.
Every full record and lexicographic five-row minimizer is reconstructed.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def need(ok,why):
    if not ok:raise ValueError(why)


def inv(x):
    a,b,u,v=617,x,0,1
    while b:
        q=a//b;a,b,u,v=b,a-q*b,v,u-q*v
    need(a==1,"field inverse");return u%617


def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":")).encode()


def bit_degrees(column_masks):
    planes=[0,0,0,0]
    for column in column_masks:
        carry=column
        for i in range(4):
            old=planes[i]
            planes[i]^=carry
            carry &= old
        need(carry==0,"at most15selected columns")
    return planes


ap=argparse.ArgumentParser()
ap.add_argument("--input",type=Path,required=True)
ap.add_argument("--capacity-checked",type=Path,required=True)
ap.add_argument("--output",type=Path,required=True)
args=ap.parse_args()
need(not args.output.exists(),"preserve independent result")
data=json.loads(args.input.read_text());cap=json.loads(args.capacity_checked.read_text())
need(cap['status']=='COMPLETE_PRIVATE_ROW_CAPACITY_AUTHOR_CHECKED' and cap['checked_five_sets']==76735,"whole separately checked prefix product")
expected_prefixes=[r for r in cap['records'] if len(r['C'])==5]
need([(r['A0'],r['C']) for r in data['records']]==[(r['A0'],r['C']) for r in expected_prefixes],"entire340-prefix family")
sq=sorted({x*x%617 for x in range(1,617)});ns=sorted(set(range(1,617))-set(sq));nset=set(ns);positions={q:i for i,q in enumerate(sq)}
v=set()
for d in range(1,617):
    current,points=1,[]
    for j in range(6):current=(current+d)%617;points.append(current)
    if set(points)<=nset:v.update(points)
dd=v|{inv(t) for t in v}
reverse={t:sum(1<<positions[q] for q in sq if t*inv(q)%617 in dd) for t in ns}
universe=(1<<308)-1
hist=collections.Counter();patterns_hist=collections.Counter();records=[]
for item,counted in zip(data['records'],expected_prefixes):
    a,c=item['A0'],item['C'];a_mask=sum(1<<positions[q] for q in a)
    need(c==[t for t in ns if reverse[t]&a_mask==a_mask],"complete literal common neighborhood")
    seen=set();counts=collections.Counter();cases=[]
    for sub in item['records']:
        b,b0=sub['B'],sub['B0'];key=tuple(b)
        need(b==sorted(set(b)) and len(b)==14 and set(b)<=nset and key not in seen,"all full labeled column sets distinct and legal")
        seen.add(key)
        need(b0==sorted(set(b)&set(c)) and len(b0) in (4,5),"selected common columns bind to whole C")
        counts[len(b0)]+=1
        planes=bit_degrees([reverse[t] for t in b])
        deficits=[14-sum((1<<i) for i,plane in enumerate(planes) if plane&(1<<positions[q])) for q in a]
        need(max(deficits)==2 and 6<=sum(deficits)<=10,"all five row capacities")
        best=[]
        for cost in range(2,15):
            degree=14-cost
            mask=universe & ~a_mask
            for i,plane in enumerate(planes):mask &= plane if (degree>>i)&1 else ~plane
            while mask and len(best)<5:
                low=mask & -mask
                best.append([cost,sq[low.bit_length()-1]])
                mask^=low
            if len(best)==5:break
        need(len(best)==5,"all303 tail rows considered")
        expected={'B0':b0,'B':b,'first_five_deficits':deficits,
                  'minimum_missing':sum(deficits)+sum(cost for cost,q in best),'best_added_rows':best}
        need(sub==expected,"complete bit-sliced degree/minimizer record")
        hist[expected['minimum_missing']]+=1
        patterns=collections.Counter((a_mask & ~reverse[t]).bit_count() for t in b if t not in c)
        if len(b0)==4:
            need(patterns=={1:10},"ten singleton pattern coverage");patterns_hist['ten_singleton']+=1
        elif patterns=={1:9}:patterns_hist['nine_singleton']+=1
        else:
            need(patterns=={1:8,2:1},"eight singleton and one double pattern coverage")
            patterns_hist['eight_singleton_one_double']+=1
        cases.append(expected)
    need(dict(counts)=={s:total for s,outside,total in counted['selected_column_counts']},"exact coefficient count separately for each common-column size and prefix")
    records.append({'A0':a,'C':c,'records':cases})
potential=[{'A0':r['A0'],'C':r['C'],**sub} for r in records for sub in r['records'] if sub['minimum_missing']<=20]
expected={'schema':'private-character617-size24-common-five-v1','agent':'six-vdw-3','role':'researcher',
          'part_sizes':[10,14],'missing_budget':20,'full_common_size':5,'cores':len(records),
          'fourteen_column_sets':sum(len(r['records']) for r in records),'missing_histogram':sorted(hist.items()),
          'column_pattern_histogram':sorted(patterns_hist.items()),'minimum_conditional_missing':min(hist),
          'potential_support_cores':len(potential),'potential_supports':potential,'records':records,
          'records_sha256':hashlib.sha256(canon(records)).hexdigest(),
          'status':'COMPLETE_PRIVATE_COMMON_FIVE_PILOT_REQUIRES_INDEPENDENT_CHECK'}
need(data==json.loads(json.dumps(expected)),"whole38,020-entry physical/completeness record")
need(len(records)==340 and expected['fourteen_column_sets']==38020 and not potential,"entire full-C5 branch excluded")
fixtures=0
for columns in itertools.product(range(8),repeat=4):
    planes=bit_degrees(columns)
    for row in range(3):
        literal=sum((c>>row)&1 for c in columns)
        binary=sum((1<<i) for i,plane in enumerate(planes) if plane&(1<<row))
        need(literal==binary,"complete small reverse-column adder truth control")
    fixtures+=1
result={'agent':'six-vdw-3','role':'researcher','cores':len(records),'fourteen_column_sets':38020,
        'minimum_conditional_missing':min(hist),'potential_support_cores':0,
        'records_sha256':expected['records_sha256'],'small_exhaustive_bit_counter_fixtures':fixtures,
        'status':'COMPLETE_PRIVATE_COMMON_FIVE_AUTHOR_CHECKED'}
args.output.write_text(json.dumps(result,sort_keys=True)+'\n');print(json.dumps(result))
