"""Strict builds, representative ASan/UBSan and damaged manifest checks.

Run after reproduce.py. Sanitizers cover a2000/1500-case initial interval
and both sharp controls with short500-case intervals. They do not supply
the full census, which is separately replayed by reproduce.py.
"""
import argparse
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import time
import model as m
from reproduce import barrier

HERE = Path(__file__).resolve().parent


def run(args,env,limit=30):
    barrier()
    result = subprocess.run([str(x) for x in args],env=env,capture_output=True,text=True,timeout=limit)
    m.need(result.returncode == 0 and not result.stderr, 'strict/sanitizer run failed: '+result.stderr[-1500:])
    return result.stdout


def records(text,first,count,total):
    items = [json.loads(s) for s in text.splitlines()]
    footer = items.pop()
    m.need(footer['segment'] is True and footer['first'] == first and
           footer['next'] == first+count and footer['total'] == total and len(items) == count,
           'checking interval incomplete')
    m.need([x['index'] for x in items] == list(range(first,first+count)), 'checking interval indices')
    return items


def main(args):
    start = time.monotonic(); work = args.work
    root = args.replay; env = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
        MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',ASAN_OPTIONS='detect_leaks=0:abort_on_error=1',
        UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
    work.mkdir(parents=True,exist_ok=True)
    m.need(not list(work.iterdir()), 'checking work must be empty')
    for name in ('native','produce'):
        run(['g++','-std=c++17','-O1','-g','-fno-omit-frame-pointer','-fno-pie','-no-pie',
             '-fsanitize=address,undefined','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',
             HERE/(name+'.cpp'),'-o',work/name],env)
    joins = list(combinations(range(7),3));promotions = list(combinations(range(35),4))
    recipes = [((0,1,2),(2,25,32,34)),((0,1,6),(1,10,23,25))]
    native_intervals = [(0,2000)]+[(joins.index(J)*52360+promotions.index(P),500) for J,P in recipes]
    manifest = root/'producer/cases.txt'
    cases = [list(map(int,s.split())) for s in manifest.read_text().splitlines()]
    representatives = []
    maps = m.centralizer(m.geometry())
    for J,P in recipes:
        canonical = min((tuple(sorted(v[j] for j in J)),tuple(sorted(b[p] for p in P))) for v,r,b in maps)
        representatives.append(next(c[0] for c in cases if (tuple(c[1:4]),tuple(c[4:8])) == canonical))
    producer_intervals = [(0,1500)]+[(i,500) for i in representatives]
    receipts = []
    for name,intervals,total in (('native',native_intervals,1832600),('produce',producer_intervals,305874)):
        for first,count in intervals:
            results = []
            positive = []
            for mode,binary in (('release',root/('native/native' if name == 'native' else 'producer/produce')),
                                ('sanitized',work/name)):
                command = [binary,'--first',first,'--limit',count,'--seconds','25']
                if name == 'produce':
                    output = work/(mode+'-positive-'+str(first)+'.txt')
                    command += ['--manifest',manifest,'--critical',output]
                results.append(records(run(command,env),first,count,total))
                if name == 'produce':positive.append(output.read_bytes())
            m.need(results[0] == results[1], 'sanitized/release complete case records differ')
            if name == 'produce':m.need(positive[0] == positive[1], 'sanitized positive stream differs')
            receipts.append(dict(algorithm=name,first=first,count=count,all_case_fields_equal=True,
                                 positive_stream_equal=name == 'produce'))
    damages = []
    good = '0 0 1 2 0 1 2 3 6\n'
    bad_inputs = {
        'truncated-final-row':good+'1 0 1 2 0 1',
        'extra-field':good.rstrip()+' 99\n',
        'noninteger-field':good.replace('3 6','x 6'),
        'duplicate-promotion':good.replace('0 1 2 3 6','0 1 2 2 6'),
        'wrong-index':good.replace('0 0 1 2','1 0 1 2'),
        'invalid-orbit-weight':good[:-2]+'5\n'}
    for name,text in bad_inputs.items():
        path = work/(name+'.txt');path.write_text(text)
        barrier()
        result = subprocess.run([str(root/'producer/produce'),'--manifest',str(path),'--critical',
            str(work/(name+'-out.txt')),'--limit','1','--seconds','25'],env=env,capture_output=True,text=True,timeout=30)
        m.need(result.returncode != 0 and result.stderr.strip(), 'damaged manifest accepted: '+name)
        damages.append(name)
    out = dict(status='REPRESENTATIVE_SANITIZERS_AND_PARSER_DAMAGES_PASS',intervals=receipts,
               native_cases=sum(n for i,n in native_intervals),producer_cases=sum(n for i,n in producer_intervals),
               damaged_manifests_rejected=damages,seconds=time.monotonic()-start,
               sanitizer_flags='-O1 -g -fno-omit-frame-pointer -fno-pie -no-pie -fsanitize=address,undefined',
               scope='Representative validation only; full exhaustive release run is separate.')
    (work/'validation.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay',type=Path,required=True)
    ap.add_argument('--work',type=Path,required=True)
    main(ap.parse_args())
