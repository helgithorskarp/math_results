"""Separate literal column tuples and full degree checker for every C4 case."""
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path


def need(ok,why):
    if not ok:raise ValueError(why)


def inv(x):
    a,b,u,v=617,x,0,1
    while b:
        q=a//b;a,b,u,v=b,a-q*b,v,u-q*v
    need(a==1,"field inverse");return u%617


def canon(x):return json.dumps(x,sort_keys=True,separators=(",",":")).encode()


ap=argparse.ArgumentParser()
ap.add_argument("--input",type=Path,required=True)
ap.add_argument("--capacity",type=Path,required=True)
ap.add_argument("--output",type=Path,required=True)
args=ap.parse_args()
need(not args.output.exists(),"preserve literal check")
data=json.loads(args.input.read_text());cap=json.loads(args.capacity.read_text())
sq=sorted({x*x%617 for x in range(1,617)});ns=sorted(set(range(1,617))-set(sq));nset=set(ns)
v=set()
for d in range(1,617):
    now,points=1,[]
    for j in range(6):now=(now+d)%617;points.append(now)
    if set(points)<=nset:v.update(points)
dd=v|{inv(x) for x in v}
nb={q:{t for t in ns if t*inv(q)%617 in dd} for q in sq}
records=[];hist=collections.Counter()
for row in cap['records']:
    if len(row['C'])!=4 or not row['surviving_core_sizes']:continue
    a,c=row['A0'],row['C'];single=[]
    need(set(c)=={t for t in ns if all(t in nb[q] for q in a)},"full common neighborhood")
    for i in range(5):
        single.append([t for t in ns if t not in nb[a[i]] and all(t in nb[q] for j,q in enumerate(a) if i!=j)])
    cases=[]
    # Increasing physical ten-column tuples grouped by the unique missed row.
    def visit(i,chosen):
        if i==5:
            b=sorted(c+chosen)
            need(len(b)==len(set(b))==14,"all labeled columns retained")
            need(all(len(set(b)-nb[q])==2 for q in a),"five exact row deficits")
            extra=[q for q in sq if q not in a and sum(t not in nb[q] for t in b)==2]
            cases.append({'B':b,'cost_two_added_rows':extra});hist[len(extra)]+=1
            return
        for x,y in itertools.combinations(single[i],2):visit(i+1,chosen+[x,y])
    visit(0,[])
    need(len(cases)==math.prod(math.comb(len(s),2) for s in single),"whole disjoint singleton product coverage")
    cases.sort(key=lambda r:r['B'])
    records.append({'A0':a,'C':c,'singleton_columns':single,'records':cases})
potential=[{'A0':r['A0'],**sub} for r in records for sub in r['records'] if len(sub['cost_two_added_rows'])>=5]
expected={'schema':'private-character617-size24-common-four-v1','agent':'six-vdw-3','role':'researcher',
          'part_sizes':[10,14],'missing_budget':20,'first_five_common':4,'cores':len(records),
          'fourteen_column_sets':sum(len(r['records']) for r in records),'extra_cost_two_histogram':sorted(hist.items()),
          'potential_support_cores':len(potential),'potential_supports':potential,
          'records_sha256':hashlib.sha256(canon(records)).hexdigest(),'records':records,
          'status':'COMPLETE_PRIVATE_COMMON_FOUR_PILOT_REQUIRES_INDEPENDENT_CHECK'}
need(data==json.loads(json.dumps(expected)),"every full original column/row record")
result={'agent':'six-vdw-3','role':'researcher','cores':len(records),'fourteen_column_sets':expected['fourteen_column_sets'],
        'potential_support_cores':len(potential),'records_sha256':expected['records_sha256'],
        'status':'COMPLETE_PRIVATE_COMMON_FOUR_CHECK_PASSED'}
args.output.write_text(json.dumps(result,sort_keys=True)+"\n");print(json.dumps(result))
