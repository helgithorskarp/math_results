"""Serial guarded cold proof replay; full records stay in caller-selected scratch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    dest = args.scratch.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    seal = json.loads((source/'PRIMARY_SEAL.json').read_text())
    for name, digest in seal['files'].items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest() != digest:
            raise ValueError('primary seal '+name)
    env = os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key] = '1'
    receipts = []
    def run(directory, optimize, arguments, reject=False):
        command = [sys.executable,'-I','-B']+(['-O'] if optimize else [])
        command += [str(directory/'check.py')]+arguments
        start = time.monotonic()
        child = subprocess.run(command,capture_output=True,text=True,env=env,cwd=dest,timeout=45)
        if (child.returncode != 0) != reject:
            raise ValueError('unexpected child outcome '+str(arguments)+'\n'+child.stderr)
        receipt = {'optimized':optimize,'arguments':arguments,'exit':child.returncode,
                   'seconds':round(time.monotonic()-start,6),
                   'cumulative_peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        if not reject:
            receipt['result'] = json.loads(child.stdout)
        receipts.append(receipt)
        print(json.dumps({'exit':child.returncode,'optimized':optimize,
                         'seconds':receipt['seconds'],'arguments':arguments}),flush=True)
        return child
    for label in ['primary','literal']:
        records = []
        for optimize in [False,True]:
            path = dest/(label+('-O' if optimize else '-normal')+'.json')
            arguments = (['--literal'] if label == 'literal' else [])+['--record',str(path)]
            arguments += ['--check',str(source/('expected-literal.json' if label == 'literal' else 'expected.json'))]
            run(source,optimize,arguments)
            records.append(path.read_bytes())
        if records[0] != records[1]:
            raise ValueError('whole normal/O bytes '+label)
    cold = dest/'cold-source'
    cold.mkdir(exist_ok=True)
    for name in list(seal['files'])+['PRIMARY_SEAL.json','expected.json','expected-literal.json']:
        shutil.copy2(source/name,cold/name)
    for label in ['primary','literal']:
        path = dest/(label+'-cold.json')
        run(cold,False,(['--literal'] if label == 'literal' else [])+['--record',str(path)])
        if path.read_bytes() != (dest/(label+'-normal.json')).read_bytes():
            raise ValueError('whole cold bytes '+label)
    damages = ['missing','duplicate','float','negative-deficit','oversized-floor',
               'omitted-highest','physical-cross','wrong-kernel','wrong-mean-metric','wrong-multiplicity']
    for damage in damages:
        for optimize in [False,True]:
            run(source,optimize,['--damage',damage],True)
    fixture = json.loads((source/'expected.json').read_text())
    for label in ['wrong-hash','wrong-type','missing-rank','malformed']:
        value = json.loads(json.dumps(fixture))
        if label == 'wrong-hash':
            value['record_sha256'] = '0'*64
        elif label == 'wrong-type':
            value['N'] = str(value['N'])
        elif label == 'missing-rank':
            del value['original_lower_rank']
        path = dest/('damaged-'+label+'.json')
        path.write_text('{' if label == 'malformed' else json.dumps(value))
        for optimize in [False,True]:
            run(source,optimize,['--check',str(path)],True)
    result = {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
              'python':sys.version,'native_threads':1,'serial_children':True,
              'unchanged_child_guard_seconds':45,'primary_source_seals_match':True,
              'complete_primary_literal_normal_O_cold_bytes_match':True,
              'positive_children':6,'mathematical_damages':20,'fixture_damages':8,
              'rss_is_cumulative_maximum_not_per_child':True,'receipts':receipts}
    (dest/'validation.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
