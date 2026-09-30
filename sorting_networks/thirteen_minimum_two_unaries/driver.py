"""Only batching, expected-output comparisons and private scratch progress.
Author: six-sorting-1, researcher. Contains no comparator mathematics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent


def canonical(result):
    r=json.loads(json.dumps(result))
    if 'coarse_state_sha256' in r:r['state_sha256']=r.pop('coarse_state_sha256')
    if r['status']=='independent_complete_empty_coarse_closure':r['status']='complete_empty_closure'
    keys=('catalog_index','kernel','status','states','processed','queue','edges',
          'maximum_cuts','weight_cuts','terminals','state_sha256')
    return {k:r[k] for k in keys if k in r}


def run(mode,catalog,close,controls):
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    start=time.monotonic();deadline=start+45
    cert=json.loads((HERE/'certificate.json').read_text())
    fixture_hash=hashlib.sha256((HERE/'fixture.json').read_bytes()).hexdigest()
    assert fixture_hash==cert['fixture_sha256']
    assert json.loads(json.dumps(catalog))==cert['catalog'] and len(catalog)==59
    certificate_hash=hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()
    scratch=HERE/'scratch';scratch.mkdir(exist_ok=True)
    path=scratch/(mode+'-progress.json')
    results=[];status='all_cases_complete';partial=None
    if args.resume:
        old=json.loads(path.read_text())
        assert old['fixture_sha256']==fixture_hash and old['certificate_sha256']==certificate_hash
        results=old['results']
    assert [r['catalog_index'] for r in results]==list(range(len(results)))
    assert results==cert['cases'][:len(results)],'Saved progress differs from the pinned certificate'
    for i,word in enumerate(catalog):
        if i<len(results):continue
        if time.monotonic()>=deadline:status='incomplete_batch';break
        r=close(word,deadline);r['catalog_index']=i
        if r['status']=='operational_limit_incomplete':
            status='incomplete_batch';partial=r;break
        r=canonical(r)
        assert r==cert['cases'][i],(i,r,cert['cases'][i])
        results.append(r)
    result={'agent':'six-sorting-1','role':'researcher','mode':mode,'status':status,
            'fixture_sha256':fixture_hash,'certificate_sha256':certificate_hash,
            'results':results,'completed_cases':len(results),'partial':partial,
            'controls':controls,'elapsed_seconds':time.monotonic()-start,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'per_closure_state_limit':50000,'batch_seconds_limit':45}
    if status=='all_cases_complete':
        assert len(results)==59
        assert sum(r.get('states',0) for r in results)==cert['total_states']==932386
        assert sum(r.get('edges',0) for r in results)==cert['total_edges']==21793023
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('results','partial','controls')}))
