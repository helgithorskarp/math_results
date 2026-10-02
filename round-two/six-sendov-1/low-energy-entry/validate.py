#!/usr/bin/env python3
"""Serial source-only normal/optimized complete-record and bad-fixture checks."""
import copy
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
ENV = os.environ.copy()
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    ENV[key] = '1'

def need(condition, text):
    if not condition: raise ValueError(text)

def run(mode, expected=None):
    command = [sys.executable, '-I', '-B']
    if mode == 'optimized': command.append('-O')
    command.append(str(ROOT/'verify.py'))
    if expected is not None: command += ['--expected', str(expected)]
    started = time.monotonic()
    result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=45)
    return result, time.monotonic()-started

def generate():
    baseline = json.loads((ROOT/'EXPECTED.json').read_text())
    canonical = json.dumps(baseline,sort_keys=True,separators=(',',':'))
    digest = sha256(canonical.encode()).hexdigest()
    positive = []
    for mode in ('normal','optimized'):
        result, elapsed = run(mode)
        need(result.returncode == 0, mode+' positive run failed: '+result.stderr[:500])
        summary = json.loads(result.stdout)
        need(summary['status'] == 'PASS' and summary['whole_record_sha256'] == digest,
             'positive entire record mismatch')
        positive.append({'mode':mode,'seconds':elapsed,'summary':summary})
    fixtures = []
    def mutate(name, function):
        record = copy.deepcopy(baseline); function(record)
        fixtures.append((name,json.dumps(record,sort_keys=True,separators=(',',':'))))
    def original_damage(record):
        item = next(x for x in record['complete_controls']
                    if x['name'].startswith('complete actual-original positivity '))
        item['all_original_coefficients'][0]['real'][0] += 1
    mutate('actual anchored original coefficient changed',original_damage)
    mutate('wrapped first Fourier row missing',lambda r:r['complete_controls'].__setitem__(
           slice(None),[c for c in r['complete_controls'] if c['name']!='full first Fourier row with wrap']))
    mutate('strict endpoint margin changed',lambda r:r['strict_whole_window_margins'][0]['value'].__setitem__(0,-1))
    mutate('integer schema replaced by bool',lambda r:r.__setitem__('schema',True))
    mutate('extra unproved global concentration field',lambda r:r.__setitem__('global_H30',True))
    mutate('integer schema replaced by float',lambda r:r.__setitem__('schema',1.0))
    fixtures.append(('duplicate schema field','{"schema":1,'+canonical[1:]))
    fixtures.append(('nonfinite NaN field',canonical.replace('"schema":1','"schema":NaN',1)))
    fixtures.append(('nonfinite Infinity field',canonical.replace('"schema":1','"schema":Infinity',1)))
    rejections = []
    with tempfile.TemporaryDirectory(prefix='entry-fixtures-', dir=ROOT) as td:
        for index,(name,text) in enumerate(fixtures):
            path=Path(td)/('bad'+str(index)+'.json');path.write_text(text)
            for mode in ('normal','optimized'):
                result,elapsed=run(mode,path)
                need(result.returncode==1,'bad fixture not rejected with explicit failure: '+name)
                need(result.stderr.startswith('FAIL: ') and not result.stdout,
                     'unexpected rejection path: '+name)
                if name.startswith('duplicate'): marker='duplicate fixture field'
                elif name.startswith('nonfinite') or name.endswith('float'):marker='noninteger fixture number'
                else: marker='entire typed fixture differs'
                need(marker in result.stderr,'wrong failure reason: '+name)
                rejections.append({'name':name,'mode':mode,'reason':result.stderr.strip()})
    return {'agent':'six-sendov-1','role':'researcher','status':'PASS',
       'python_version':sys.version.split()[0],'standard_library_only':True,
       'native_threads':1,'serial_children':True,'per_child_guard_seconds':45,
       'whole_record_sha256':digest,'positive_runs':positive,
       'external_fixture_rejections':rejections,
       'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
       'trust_boundary':'ordinary analytic/norm/disk-root inequalities and imported9533/9572 remain written, unformalized; finite records do not prove those steps'}

if __name__=='__main__':
    try:
        record=generate()
        if len(sys.argv)==3 and sys.argv[1]=='--emit':
            Path(sys.argv[2]).write_text(json.dumps(record,indent=2)+'\n')
        elif len(sys.argv)!=1:raise ValueError('usage: validate.py [--emit PATH]')
        print(json.dumps({'status':'PASS','whole_record_sha256':record['whole_record_sha256'],
                          'positive_modes':2,'fixture_rejections':len(record['external_fixture_rejections']),
                          'peak_child_rss_kib':record['peak_child_rss_kib']}))
    except (ValueError,OSError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('VALIDATION INCOMPLETE OR REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
