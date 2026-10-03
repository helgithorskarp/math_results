"""Complete literal-labeled outside-column patterns for full common size5.

For s=4 all10outside columns are singleton-missing, two per row. For s=5
there are9outside columns, either all singleton-missing (S=9), or eight
singletons plus one double-missing column (S=10). This exhausts S<=10.
Every tail row must have full missing degree>=2, since these are the least5.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def need(ok,why):
    if not ok:raise ValueError(why)


def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":")).encode()


ap=argparse.ArgumentParser()
ap.add_argument("--capacity",type=Path,required=True)
ap.add_argument("--output",type=Path,required=True)
args=ap.parse_args()
need(not args.output.exists(),"preserve previous computation")
capacity=json.loads(args.capacity.read_text())
sq=[q for q in range(1,617) if pow(q,308,617)==1]
ns=[t for t in range(1,617) if pow(t,308,617)==616]
v={((1+j*d)%617) for d in range(1,617) if all(pow((1+k*d)%617,308,617)==616 for k in range(1,7)) for j in range(1,7)}
dd=v|{pow(t,615,617) for t in v}
nb={q:sum(1<<(q*t%617) for t in dd) for q in sq}
records=[];hist=collections.Counter();patterns_hist=collections.Counter()
for row in capacity['records']:
    if len(row['C'])!=5 or not row['surviving_core_sizes']:continue
    a0,c=row['A0'],row['C'];groups=collections.defaultdict(list)
    for t in ns:
        pattern=sum(1<<i for i,q in enumerate(a0) if not nb[q]&(1<<t))
        if pattern:groups[pattern].append(t)
    cases=[]
    def add(b0,choices,kind):
        outside=[t for group in choices for t in group];b=sorted(list(b0)+outside)
        bm=sum(1<<t for t in b)
        need(len(b)==len(set(b))==14,"full physical column choice")
        deficits=[14-(nb[q]&bm).bit_count() for q in a0]
        need(max(deficits)==2 and 6<=sum(deficits)<=10,"least-five admissible deficits")
        costs=sorted((14-(nb[q]&bm).bit_count(),q) for q in sq if q not in a0 and 14-(nb[q]&bm).bit_count()>=2)
        lower=sum(deficits)+sum(cost for cost,q in costs[:5])
        cases.append({'B0':list(b0),'B':b,'first_five_deficits':deficits,'minimum_missing':lower,'best_added_rows':[[cost,q] for cost,q in costs[:5]]})
        hist[lower]+=1;patterns_hist[kind]+=1
    if 4 in row['surviving_core_sizes']:
        for b0 in itertools.combinations(c,4):
            for choices in itertools.product(*(itertools.combinations(groups[1<<i],2) for i in range(5))):add(b0,choices,'ten_singleton')
    if 5 in row['surviving_core_sizes']:
        for lone in range(5):
            counts=[1 if i==lone else 2 for i in range(5)]
            for choices in itertools.product(*(itertools.combinations(groups[1<<i],counts[i]) for i in range(5))):add(c,choices,'nine_singleton')
        for i,j in itertools.combinations(range(5),2):
            counts=[1 if k in (i,j) else 2 for k in range(5)]
            for double in groups[(1<<i)|(1<<j)]:
                for choices in itertools.product(*(itertools.combinations(groups[1<<k],counts[k]) for k in range(5))):add(c,[*choices,(double,)],'eight_singleton_one_double')
    cases.sort(key=lambda r:r['B'])
    need(len({tuple(r['B']) for r in cases})==len(cases),'all labeled columns counted once per prefix')
    records.append({'A0':a0,'C':c,'records':cases})
potential=[{'A0':r['A0'],'C':r['C'],**sub} for r in records for sub in r['records'] if sub['minimum_missing']<=20]
out={'schema':'private-character617-size24-common-five-v1','agent':'six-vdw-3','role':'researcher',
     'part_sizes':[10,14],'missing_budget':20,'full_common_size':5,'cores':len(records),
     'fourteen_column_sets':sum(len(r['records']) for r in records),'missing_histogram':sorted(hist.items()),
     'column_pattern_histogram':sorted(patterns_hist.items()),'minimum_conditional_missing':min(hist),
     'potential_support_cores':len(potential),'potential_supports':potential,'records':records,
     'records_sha256':hashlib.sha256(canon(records)).hexdigest(),
     'status':'COMPLETE_PRIVATE_COMMON_FIVE_PILOT_REQUIRES_INDEPENDENT_CHECK'}
args.output.write_text(json.dumps(out,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','potential_supports')}))
