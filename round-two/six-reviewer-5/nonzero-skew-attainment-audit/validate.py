"""Whole-record, cold source-only, semantic-damage and preimport checks."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
NATIVE = ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
          'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']


def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(strict_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def sealed(root):
    records = json.loads((root/'CORE.json').read_text())
    if set(records) != {'algebra.py','check.py'}:
        raise RuntimeError('wrong sealed source set')
    for name, wanted in records.items():
        got = hashlib.sha256((root/name).read_bytes()).hexdigest()
        if got != wanted:
            raise RuntimeError('preimport source mismatch: '+name)


def run(root, args, env):
    start = time.monotonic()
    p = subprocess.run([sys.executable,'-I','-B']+args, cwd=root,
                       env=env, capture_output=True, timeout=45)
    return {'returncode':p.returncode,'stdout':p.stdout.decode(),
            'stderr':p.stderr.decode(),'seconds':time.monotonic()-start}


def validate():
    sealed(ROOT)
    env = dict(os.environ)
    env.update({n:'1' for n in NATIVE})
    fixture_raw = (ROOT/'RECORD.json').read_bytes()
    fixture = json.loads(fixture_raw)
    rows = []
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='nonzero-skew-audit-') as tmp:
        cold = Path(tmp)
        for name in ['algebra.py','check.py','CORE.json','RECORD.json','validate.py']:
            (cold/name).write_bytes((ROOT/name).read_bytes())
        sealed(cold)
        for location, root in [('live',ROOT),('cold-source-only',cold)]:
            for mode in ['normal','optimized']:
                out = cold/(location+'-'+mode+'.json')
                command = ([] if mode == 'normal' else ['-O'])+['check.py','--output',str(out)]
                row = run(root,command,env)
                row.update({'case':location+'-'+mode,'kind':'whole-positive'})
                if row['returncode'] != 0:
                    raise RuntimeError(row)
                raw = out.read_bytes()
                if raw != fixture_raw or not strict_equal(json.loads(raw),fixture):
                    raise RuntimeError('whole field/parameter record differs')
                row['record_sha256'] = hashlib.sha256(raw).hexdigest()
                rows.append(row)
        for mode in ['normal','optimized']:
            for damage in ['mu','nu','sigma','q1','split','anchor','shift','cost-split']:
                row = run(ROOT,([] if mode == 'normal' else ['-O'])+
                          ['check.py','--damage',damage],env)
                row.update({'case':mode+'-'+damage,'kind':'mathematical-rejection'})
                if row['returncode'] != 2 or not row['stderr'].startswith('REJECT: '):
                    raise RuntimeError('damage did not fail mathematically: '+str(row))
                rows.append(row)
        damages = []
        f = copy.deepcopy(fixture); f['all_nine_root_eta_jets'][4][3][0][0][0] += 1
        damages.append(('individual-third-root-coordinate',f))
        f = copy.deepcopy(fixture); f['all_nine_half_normal_eta_jets'][5][3][0][0][0] += 1
        damages.append(('individual-third-normal-coordinate',f))
        f = copy.deepcopy(fixture); f['all_nine_epsilon7_responses'][6]['half_normal'][0][0] += 1
        damages.append(('seventh-normal-coordinate',f))
        f = copy.deepcopy(fixture); f['schema'] = True
        damages.append(('boolean-integer-confusion',f))
        f = copy.deepcopy(fixture); f['schema'] = 1.0
        damages.append(('float-integer-confusion',f))
        f = copy.deepcopy(fixture); del f['all_four_individual_repair_rows']
        damages.append(('missing-entire-repair-map',f))
        f = copy.deepcopy(fixture); f['unclaimed-extra-key'] = 0
        damages.append(('extra-field',f))
        for name, damaged in damages:
            if strict_equal(fixture,damaged):
                raise RuntimeError('whole/type fixture damage accepted: '+name)
        rows.append({'kind':'strict-whole-record-rejections','cases':[n for n, _ in damages]})
        (cold/'algebra.py').write_bytes((cold/'algebra.py').read_bytes()+b'\n# damaged source\n')
        row = run(cold,['validate.py','--seal-only'],env)
        if row['returncode'] != 2 or 'preimport source mismatch' not in row['stderr']:
            raise RuntimeError('source-byte control accepted')
        row.update({'kind':'preimport-source-rejection','case':'cold-algebra-byte-change'})
        rows.append(row)
    return {'schema':1,'agent':'six-reviewer-5','role':'independent reviewer',
            'verdict':'PASS','python':sys.version.split()[0], 'arithmetic':'stdlib Fraction',
            'record_bytes':len(fixture_raw),'record_sha256':hashlib.sha256(fixture_raw).hexdigest(),
            'source_seal':json.loads((ROOT/'CORE.json').read_text()),
            'threads':{n:env[n] for n in NATIVE},'serial_children':True,
            'child_guard_seconds':45,'total_seconds':time.monotonic()-start,
            'children_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'cases':rows, 'timeouts':0,'resource_escalation':False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seal-only',action='store_true')
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    try:
        if args.seal_only:
            sealed(ROOT)
            print('SEALED')
        else:
            report = validate()
            if args.output:
                args.output.write_text(json.dumps(report,indent=2)+'\n')
            print(json.dumps({k:v for k,v in report.items() if k != 'cases'},sort_keys=True))
    except (RuntimeError,subprocess.TimeoutExpired) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(2)
