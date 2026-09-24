"""Complete exact twenty-block exclusion, using either proof implementation."""
from collections import Counter,defaultdict
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

from catalogue import validate
import primary_model
import audit_model
import profiles
from row_maps import pointed_templates

ROOT=Path(__file__).resolve().parent
PROFILE_NAMES=('twelve','eleven','balanced')
ROOT_COUNTS={'primary':(954,8451,12819),'audit':(1284,14124,23540)}
ROW_SCHEMA=['root','design','excess','second_point','shared_blocks','compatible_joins',
            'configurations_sha256','search_states','largest_primary_search','bundle_states']
DESIGN_SCHEMA=['profile','design','roots','empty_roots','compatible_joins',
               'search_states','bundle_states','root_records_sha256']

def digest(value):
    return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def root_list(profile,method):
    if profile=='balanced':
        roots=(primary_model if method=='primary' else audit_model).prepare()[0]
        for root in roots:root['extra']=tuple((p,1) for p in root['high'])
        return roots
    return profiles.prepare(profile,method)

def run_range(task):
    profile,method,lo,hi,python_audit=task
    roots=root_list(profile,method)
    expected=ROOT_COUNTS[method][PROFILE_NAMES.index(profile)]
    if len(roots)!=expected or not 0<=lo<=hi<=expected:raise ValueError('incomplete root domain')
    if method=='primary':
        from residual import Space,solve
        templates=pointed_templates()
    else:
        if python_audit:from reference_star import Space,solve
        else:from native_star import Space,solve
        templates=audit_model.prepare()[1]
    spaces={};records=[]
    for root in roots[lo:hi]:
        if profile=='balanced':
            if method=='primary':configurations=primary_model.joined(root,templates)[0]
            else:configurations=audit_model.join(root,templates)[1]
            target=[10 if p in root['high'] else 9 for p in range(13)]
        else:configurations,target,_=profiles.join(root,templates,method)
        high=set(root['high'])
        bounds={sum(1<<p for p in pair):(20 if set(pair)<=high else 5) for pair in combinations(range(13),2)}
        if root['r'] not in spaces:spaces[root['r']]=Space(12,root['r'])
        h=root['high'][0];q=root['high'][1] if len(root['high'])>1 else h
        nodes=largest=bundles=0
        for fixed in configurations:
            answer=solve(spaces[root['r']],fixed,h,q,target_degrees=target,pair_bounds=bounds)
            if answer['status']!='UNSAT':
                raise ValueError(('unexpected twenty-block completion',profile,root,fixed,answer))
            if method=='primary':
                nodes+=answer['nodes'];largest=max(largest,answer['nodes'])
            else:nodes+=answer['point_states'];bundles+=answer['bundle_states']
        records.append([root['id'],root['design'],[list(x) for x in root['extra']],root['r'],root['k'],
                        len(configurations),digest(configurations),nodes,largest,bundles])
    if [r[0] for r in records]!=list(range(lo,hi)):raise ValueError('missing worker result')
    return profile,records

def summarize(method,records,inputs):
    totals={};design_rows=[]
    for profile in PROFILE_NAMES:
        rows=sorted(records[profile],key=lambda r:r[0])
        expected=ROOT_COUNTS[method][PROFILE_NAMES.index(profile)]
        if [r[0] for r in rows]!=list(range(expected)):raise ValueError('missing or duplicate root')
        totals[profile]=dict(roots=len(rows),compatible_joins=sum(r[5] for r in rows),
                            empty_roots=sum(not r[5] for r in rows),search_states=sum(r[7] for r in rows),
                            largest_primary_search=max(r[8] for r in rows),bundle_states=sum(r[9] for r in rows),
                            root_records_sha256=digest(rows))
        by_design=defaultdict(list)
        for row in rows:by_design[row[1]].append(row)
        if set(by_design)!=set(range(107)):raise ValueError('missing catalogue design')
        for design in range(107):
            part=by_design[design]
            design_rows.append([profile,design,len(part),sum(not r[5] for r in part),sum(r[5] for r in part),
                                sum(r[7] for r in part),sum(r[9] for r in part),digest(part)])
    return dict(status='NO_TWENTY_BLOCK_C13_6_3_COVER',method=method,inputs=inputs,profiles=totals,
                total_roots=sum(x['roots'] for x in totals.values()),
                compatible_joins=sum(x['compatible_joins'] for x in totals.values()),
                search_states=sum(x['search_states'] for x in totals.values()),
                bundle_states=sum(x['bundle_states'] for x in totals.values()),
                links_file_sha256=sha256((ROOT/'LINKS.json').read_bytes()).hexdigest(),
                root_row_schema=ROW_SCHEMA,design_row_schema=DESIGN_SCHEMA,design_rows=design_rows)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--method',choices=['primary','audit'],default='primary')
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--python-audit',action='store_true')
    parser.add_argument('--write-reference',action='store_true')
    args=parser.parse_args()
    if not 1<=args.workers<=64:parser.error('workers must be in 1..64')
    if args.python_audit and args.method!='audit':parser.error('--python-audit requires --method audit')
    inputs=validate();tasks=[]
    for profile,n in zip(PROFILE_NAMES,ROOT_COUNTS[args.method]):
        for i in range(args.workers):tasks.append((profile,args.method,n*i//args.workers,n*(i+1)//args.workers,args.python_audit))
    records=defaultdict(list)
    if args.workers==1:parts=map(run_range,tasks)
    else:
        pool=ProcessPoolExecutor(max_workers=args.workers)
        parts=pool.map(run_range,tasks)
    try:
        for profile,rows in parts:records[profile].extend(rows)
    finally:
        if args.workers!=1:pool.shutdown(wait=True,cancel_futures=True)
    summary=summarize(args.method,records,inputs)
    reference=ROOT/('EXPECTED.json' if args.method=='primary' else 'AUDIT_EXPECTED.json')
    if args.write_reference:
        body=json.dumps({k:v for k,v in summary.items() if k!='design_rows'},indent=2)
        body=body[:-2]+',\n  "design_rows": [\n'
        body+=',\n'.join('    '+json.dumps(row) for row in summary['design_rows'])
        reference.write_text(body+'\n  ]\n}\n')
    elif summary!=json.loads(reference.read_text()):raise ValueError('reference mismatch')
    display={key:value for key,value in summary.items() if key!='design_rows'}
    print(json.dumps(display,indent=2))

if __name__=='__main__':main()
