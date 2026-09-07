"""Fresh census, independent certificate check, and physical interface audit.

No target completion solver is invoked. Build products and four generated CNFs
live in a fresh temporary directory and are removed after verification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time
import audit
import burnside

HERE=Path(__file__).resolve().parent


def run(args,valid=True):
    p=subprocess.run([str(x) for x in args],text=True,capture_output=True)
    if (p.returncode==0)!=valid:raise RuntimeError(f'Unexpected exit {p.returncode}: {args}\n{p.stdout}\n{p.stderr}')
    return p.stdout


def compare(actual,filename):
    expected=json.loads((HERE/filename).read_text())
    # JSON object keys (including clause lengths) are strings on disk.
    if json.loads(json.dumps(actual))!=expected:raise ValueError(f'Expected certificate mismatch: {filename}')


def reproduce(work):
    started=time.monotonic();binaries={}
    for name in ['cover','check_cover']:
        dest=work/name
        run(['g++','-std=c++17','-Wall','-Wextra','-Wpedantic','-O3','-mpopcnt',HERE/f'{name}.cpp','-o',dest])
        binaries[name]=dest
    print('Regenerating complete row cover',file=sys.stderr,flush=True)
    table=work/'row_cover.tsv'
    generator=json.loads(run([binaries['cover'],4,19,20,table]))
    if table.read_bytes()!=(HERE/'row_cover.tsv').read_bytes():raise ValueError('Canonical cover byte mismatch')
    checker=json.loads(run([binaries['check_cover'],4,19,20,table]))
    compare({'generator':generator,'checker':checker},'EXPECTED_COVER.json')
    compare(burnside.census(),'burnside.json')
    negative=0
    for rank,lo,hi in [(2,4,5),(3,9,10)]:
        small=work/f'small{rank}.tsv'
        run([binaries['cover'],rank,lo,hi,small])
        run([binaries['check_cover'],rank,lo,hi,small])
        lines=small.read_text().splitlines()
        bads=[lines[:-1],lines+[lines[-1]]]
        fields=lines[1].split('\t');fields[2]='0'
        bads.append([lines[0],'\t'.join(fields)]+lines[2:])
        for k,bad in enumerate(bads):
            path=work/f'bad{rank}-{k}.tsv';path.write_text('\n'.join(bad)+'\n')
            run([binaries['check_cover'],rank,lo,hi,path],False);negative+=1
    print('Checking exhaustive small graphs and full43 normalization',file=sys.stderr,flush=True)
    controls=audit.controls();instances=[]
    for category,code in sorted(controls['representative_codes'].items()):
        print(f'Checking every full43 clause: {category}',file=sys.stderr,flush=True)
        record=audit.full_instance(code,work/f'{category}.cnf');record['category']=category;instances.append(record)
    result={'controls':controls,'instances':instances,'status':'VERIFIED_ALL_PATTERN_RANK4_TASK_HANDOFF'}
    compare(result,'EXPECTED_AUDIT.json')
    encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    return {'status':result['status'],'audit_sha256':hashlib.sha256(encoded).hexdigest(),
            'row_cover_sha256':hashlib.sha256(table.read_bytes()).hexdigest(),
            'tasks':sum(checker['spanning_orbits']),'certificate_negative_controls':negative,
            'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'python_optimization':sys.flags.optimize}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work-root');parser.add_argument('--output')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='r55-row-cover-',dir=args.work_root) as directory:
        result=reproduce(Path(directory))
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
