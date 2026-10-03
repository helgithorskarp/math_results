"""Bounded serial source-only replay of the complete38 profile3 inventory.

Explicit subsets are useful for complete resumable boundaries. Only all38
complete cases can establish the full conditional profile exclusion.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
try:
    import resource
except ImportError:
    resource=None
import frame

def encode(value): return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def seal(source):
    return [dict(name=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(source.iterdir()) if p.is_file()]

def run(out,optimized,cases,stop_files=()):
    source=Path(__file__).resolve().parent;out=out.resolve()
    if out.exists(): raise ValueError('Preserve prior output; choose a fresh replay directory')
    if not cases or len(cases)!=len(set(cases)) or any(i not in frame.MATRICES for i in cases):
        raise ValueError('A nonempty unique explicit subset of complete38 is required')
    out.mkdir(parents=True);before=seal(source);products={};receipts=[]
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'): env[name]='1'
    result=dict(agent='six-books-3',role='researcher',status='INCOMPLETE_SOURCE_ONLY_NO_VERDICT',
        requested_cases=cases,case_excluded=[],case_methods=[],source_before=before,
        optimized_children=optimized,receipts=receipts,completed_products=[],
        whole_profile_excluded=False,ordinary_bridges_formalized=False,independent_person_review=False,
        native_threads=1,one_mathematical_child_at_a_time=True)
    def save(): (out/'REPLAY.json').write_bytes(encode(result)+b'\n')
    def child(name,module,arguments,file_product=True):
        if any(p.exists() for p in stop_files): raise ValueError('Operations barrier; no new child')
        save();start=time.monotonic()
        command=[sys.executable]+(['-O'] if optimized else [])+[str(source/module)]+arguments
        try:
            process=subprocess.run(command,env=env,capture_output=True,timeout=45)
            stdout,stderr,code=process.stdout,process.stderr,process.returncode
            status='CHILD_COMPLETED' if code==0 else 'CHILD_FAILED_NO_VERDICT'
        except subprocess.TimeoutExpired as error:
            stdout,stderr,code=error.stdout or b'',error.stderr or b'',None
            status='OPERATIONAL_LIMIT_NO_VERDICT'
        (out/(name+'.stdout')).write_bytes(stdout);(out/(name+'.stderr')).write_bytes(stderr)
        receipt=dict(name=name,status=status,exit_code=code,seconds=time.monotonic()-start,
            native_threads=1,child_guard_seconds=45,
            checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        if resource is not None: receipt['maximum_child_rss_kib_so_far']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        receipts.append(receipt);save()
        if code!=0: raise ValueError('Failed/limited child; no exclusion: '+name)
        value=json.loads((out/(name+'.json')).read_bytes()) if file_product else json.loads(stdout)
        canonical=out/(name+'.math.json');canonical.write_bytes(encode(value))
        products[name]=canonical
        result['completed_products'].append(name);save()
        print(json.dumps(dict(completed=name,seconds=receipt['seconds']),sort_keys=True),flush=True)
        return value
    def whole_products():
        digest=hashlib.sha256();size=0
        with (out/'MATHEMATICS.json').open('wb') as stream:
            def append(data):
                nonlocal size
                stream.write(data);digest.update(data);size+=len(data)
            append(b'{')
            for i,key in enumerate(sorted(products)):
                if i: append(b',')
                append(encode(key)+b':')
                with products[key].open('rb') as product:
                    while True:
                        chunk=product.read(1048576)
                        if not chunk: break
                        append(chunk)
            append(b'}');stream.write(b'\n')
        return size,digest.hexdigest()
    def require(ok,message):
        if not ok:
            whole_products();save()
            raise ValueError(message)
    save()
    census=child('census','compare_inventory.py',['--out',str(out/'census.json')])
    require(census['matrices']==[list(frame.MATRICES[k]) for k in range(38)],
            'Entire38 constants differ from the complete two-algorithm census')
    domains={(x,c):stars for x,c,stars in census['domains']}
    for case in cases:
        prefix=f'case_{case}_'
        f=child(prefix+'frame','frame.py',['--case',str(case),'--out',str(out/(prefix+'frame.json'))])
        require(f['columns']==census['matrices'][case] and f['whole_original_indexed_domains']==
            [domains.get((x,c),[]) for x,c in enumerate(f['columns'])],
            'Entire original frame differs from every indexed independent census domain')
        if f['empty_original_high_domains']:
            control=child(prefix+'empty_controls','empty_star_controls.py',
                ['--case',str(case),'--packet',str(out/(prefix+'frame.json'))],False)
            require(f['case_excluded'] and control['case_excluded'] and
                control['entire_empty_original_high_domains']==f['empty_original_high_domains'] and
                len(control['actual_semantic_damages'])==8,'Missing literal empty-star controls')
            method='COMPLETE_LITERAL_EMPTY_ORIGINAL_HIGH_STAR'
        else:
            child(prefix+'cover','neighborhood_cover.py',['--case',str(case),
                '--out',str(out/(prefix+'cover.json')),'--generic-out',str(out/(prefix+'generic.json'))])
            generic=(out/(prefix+'generic.json')).read_bytes().rstrip(b'\n')
            require('generic' not in products or products['generic'].read_bytes()==generic,
                    'Entire generic50400 inventory differs across cases')
            if 'generic' not in products:
                path=out/'generic.math.json';path.write_bytes(generic);products['generic']=path
            rows=child(prefix+'rows','row_domains.py',['--case',str(case),
                '--cover',str(out/(prefix+'cover.json')),'--out',str(out/(prefix+'rows.json'))])
            pairs=child(prefix+'pairs','pair_stage.py',['--case',str(case),
                '--cover',str(out/(prefix+'cover.json')),'--out',str(out/(prefix+'pairs.json'))])
            control=child(prefix+'controls','controls.py',['--case',str(case),
                '--cover',str(out/(prefix+'cover.json')),'--packet',str(out/(prefix+'pairs.json'))],False)
            require(pairs['row_stage_mathematics_sha256']==hashlib.sha256(encode(rows)).hexdigest()
                and not pairs['not_yet_attempted'],'Incomplete/unbound entire cut certificate')
            expected=(10,0) if control['row_only_exclusion'] else (15,2)
            require((len(control['actual_semantic_damages']),control['actual_positive_nonempty_prefixes'])==expected,
                    'Missing actual root-cut semantic or nonempty-prefix controls')
            if pairs['case_excluded']:
                require(not pairs['remaining_graph_indices'],'False pair-stage empty verdict')
                method='COMPLETE_PHYSICAL_ROWS_AND_LITERAL_CURRENT_A_PAIRS'
            else:
                proposed=child(prefix+'outside_proposals','outside_producer.py',['--case',str(case),
                    '--frame',str(out/(prefix+'frame.json')),'--pairs',str(out/(prefix+'pairs.json')),
                    '--out',str(out/(prefix+'outside_proposals.json'))])
                owner=proposed['owner_B_point']
                require(type(owner) is int and 0<=owner<9,'Invalid selected physical outside owner')
                audit=child(prefix+'outside_check','outside_check.py',['--case',str(case),'--owner',str(owner),
                    '--cover',str(out/(prefix+'cover.json')),'--pairs',str(out/(prefix+'pairs.json')),
                    '--frame',str(out/(prefix+'frame.json')),'--packet',str(out/(prefix+'outside_proposals.json')),
                    '--out',str(out/(prefix+'outside_check.json'))])
                require(audit['case_excluded'] and not audit['remaining_graph_indices'],
                    'Nonempty complete selected-owner domain; no exclusion')
                controls=child(prefix+'outside_controls','outside_controls.py',['--case',str(case),'--owner',str(owner),
                    '--cover',str(out/(prefix+'cover.json')),'--pairs',str(out/(prefix+'pairs.json')),
                    '--frame',str(out/(prefix+'frame.json')),'--packet',str(out/(prefix+'outside_proposals.json'))],False)
                require(audit['case_excluded'] and not audit['remaining_graph_indices'] and
                    len(controls['actual_semantic_damages'])==14 and controls['actual_valid_nonempty_prefixes']==2,
                    'Incomplete/nonempty literal full outside-star certificate or semantic controls')
                method='COMPLETE_PHYSICAL_ROWS_A_PAIRS_AND_LITERAL_FULL_SELECTED_OUTSIDE_OWNER_STAR'
        result['case_excluded'].append(case);result['case_methods'].append([case,method]);save()
    after=seal(source);require(after==before,'Source changed during replay')
    size,digest=whole_products()
    complete=sorted(cases)==list(range(38))
    result.update(status='COMPLETE_SOURCE_ONLY_ALL38_PROFILE3_EXCLUSION' if complete else
        'COMPLETE_SOURCE_ONLY_EXPLICIT_SUBSET_EXCLUSIONS',source_after=after,
        mathematical_product_bytes=size,mathematical_product_sha256=digest,
        whole_profile_excluded=complete,unrestricted_Ramsey_endpoint_claimed=False)
    save();print(json.dumps(dict(status=result['status'],case_excluded=result['case_excluded'],
        whole_profile_excluded=complete,mathematical_product_bytes=size,
        mathematical_product_sha256=result['mathematical_product_sha256']),sort_keys=True),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--optimized',action='store_true');p.add_argument('--cases',type=int,nargs='+',default=list(range(38)))
    p.add_argument('--stop-file',type=Path,action='append',default=[])
    a=p.parse_args();run(a.out,a.optimized,a.cases,a.stop_file)
