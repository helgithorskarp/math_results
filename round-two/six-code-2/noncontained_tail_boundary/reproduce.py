"""Cold, serial, standard-library reconstruction of the complete one-Q result."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    work=args.work.resolve()
    if work.exists():raise ValueError('fresh reconstruction directory required')
    manifest=json.loads((root/'MANIFEST.json').read_bytes())
    for entry in manifest['files']:
        p=root/entry['path']
        if p.stat().st_size!=entry['bytes'] or digest(p)!=entry['sha256']:
            raise ValueError('public source/fixture/certificate pin differs: '+entry['path'])
    work.mkdir(parents=True)
    begin=time.monotonic()
    env=dict(os.environ)
    for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[v]='1'
    flags=['-O','-B'] if sys.flags.optimize else ['-B']
    stages=[('caps.py',['--parent',root/'PARENT.json','--q',15,'--work',work/'carrier']),
            ('graph.py',['--carrier',work/'carrier/CORES.json','--parent',root/'PARENT.json','--work',work/'graph']),
            ('cover.py',['--parent',root/'PARENT.json','--work',work/'cover']),
            ('colors.py',['--graph',work/'graph/GRAPH.json','--work',work/'colors']),
            ('audit.py',['--carrier',work/'carrier/CORES.json','--graph',work/'graph/GRAPH.json',
                '--maps',work/'cover/NONCONTAINED_Q_MAPS.json','--colors',work/'colors/COLORS.json',
                '--witness-dir',work/'graph','--baseline69',root/'baseline69.txt','--work',work/'point-audit'])]
    for index,(program,arguments) in enumerate(stages):
        with (work/f'{index}-{program}.stdout.txt').open('w') as out, (work/f'{index}-{program}.stderr.txt').open('w') as err:
            subprocess.run([sys.executable,*flags,str(root/program),*map(str,arguments)],
                check=True,env=env,stdout=out,stderr=err,timeout=60)
    actual=work/'point-audit/EXACT_RESULT.json'
    if actual.read_bytes()!=(root/'EXPECTED.json').read_bytes():raise ValueError('entire mathematical record differs')
    record=json.loads(actual.read_bytes())
    if any(h==record['known_baseline69_degree_histogram'] for h in record['normalized69_degree_histograms']):
        raise ValueError('literal baseline inequivalence by replication spectrum fails')
    for generated,compact in ((work/'point-audit/NORMAL_FORMS69.json',root/'NORMAL_FORMS69.json'),
                              (work/'colors/COLORS.json',root/'COLORS.json')):
        if generated.read_bytes()!=compact.read_bytes():raise ValueError('positive compact certificate differs')
    for relative,expected in json.loads((root/'GENERATED_HASHES.json').read_bytes()).items():
        if digest(work/relative)!=expected:raise ValueError('generated complete artifact differs: '+relative)
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_COLD_PUBLIC_Q_BOUNDARY_RECONSTRUCTION',
        'python_optimized':bool(sys.flags.optimize),'all_source_fixture_pins':len(manifest['files']),
        'complete_exact_record_sha256':digest(actual),'normalized69_sha256':digest(work/'point-audit/NORMAL_FORMS69.json'),
        'seconds':time.monotonic()-begin,'maximum_child_RSS_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'native_threads':1,'CPU_jobs_at_once':1,'per_stage_guard_seconds':60,
        'proof_scope':'specifiedD, t1,R=a+4, all2040Q: sharp69; all10 normalized69s; ordinary bridges unformalized, external review pending.'}
    (work/'REPRODUCTION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
