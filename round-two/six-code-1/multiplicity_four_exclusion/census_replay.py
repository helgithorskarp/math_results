"""Replay exactly the generic-star part of the credited public dependency.
six-code-1, researcher. No involution or completion search is invoked.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import os
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=HERE.parents[2])
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();work=args.work.resolve();repo=args.repository.resolve()
    require(work!=HERE and HERE not in work.parents and not work.exists(),'work must be new and outside source')
    work.mkdir(parents=True);inputs=work/'inputs';inputs.mkdir()
    dep=json.loads((HERE/'DEPENDENCIES.json').read_text())['twenty_star_census']
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        os.environ[key]='1'
    start=time.monotonic()
    for item in dep['runtime_files']:
        data=subprocess.check_output(['git','show',dep['source_commit']+':'+item['path']],cwd=repo,timeout=20)
        require(sha256(data).hexdigest()==item['sha256'],'published dependency bytes differ')
        (inputs/Path(item['path']).name).write_bytes(data)
    sys.path.insert(0,str(inputs))
    spec=importlib.util.spec_from_file_location('credited_census_reproducer',inputs/'reproduce.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    d=json.loads((inputs/'fixtures.json').read_text())
    stars=tuple(tuple(tuple(q) for q in Q) for Q in d['stars'])
    groups=tuple(tuple(tuple(g) for g in G) for G in d['groups'])
    roots,census=module.census_all(work)
    cover=module.cover_by_fixtures(roots,stars,groups,work)
    expected=json.loads((inputs/'expected.json').read_text())
    require(json.loads(json.dumps(census))==expected['census'] and
            json.loads(json.dumps(cover))==expected['fixture_cover'],'complete generic census record differs')
    stable=dict(agent='six-code-1',role='researcher',status='COMPLETE_GENERIC_CENSUS_REPLAY',
                source_commit=dep['source_commit'],census=census,fixture_cover=cover)
    raw=(json.dumps(stable,sort_keys=True,separators=(',',':'))+'\n').encode()
    (work/'result.json').write_bytes(raw)
    metrics=dict(status=stable['status'],manifest_sha256=sha256(raw).hexdigest(),
                 seconds=time.monotonic()-start,peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'metrics.json').write_text(json.dumps(metrics,sort_keys=True)+'\n')
    print(json.dumps(metrics,sort_keys=True),flush=True)


if __name__=='__main__':main()
