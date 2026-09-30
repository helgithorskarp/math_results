"""Sequential, resumable source regeneration and independent exact checks."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--begin', type=int, default=0)
    p.add_argument('--end', type=int, default=617)
    p.add_argument('--seconds', type=float, default=15)
    p.add_argument('--budget', type=float)
    a = p.parse_args()
    if not (0 <= a.begin < a.end <= 617 and 0 < a.seconds <= 60):
        raise ValueError('Phase range or guidance time')
    a.work.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    env = os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[key] = '1'
    started = time.monotonic()
    results = []
    hashes = {name:hashlib.sha256((source/name).read_bytes()).hexdigest()
              for name in ['generate.py','verify.py','reproduce.py']}
    for phase in range(a.begin,a.end):
        if a.budget is not None and time.monotonic()-started >= a.budget:
            break
        certificate = a.work/f'phase-{phase:03d}.json'
        if not certificate.exists():
            run = subprocess.run([sys.executable,str(source/'generate.py'),str(phase),str(certificate),
                                  '--seconds',str(a.seconds),'--guidance',str(a.work/f'guidance-{phase:03d}.json')],
                                 env=env,capture_output=True,text=True,timeout=a.seconds+15)
            if run.returncode:
                raise RuntimeError(f'Phase{phase} guidance failed; no exclusion: {run.stderr}')
        run = subprocess.run([sys.executable,str(source/'verify.py'),str(certificate),
                              '--output',str(a.work/f'check-{phase:03d}.json')],
                             env=env,capture_output=True,text=True,timeout=10)
        if run.returncode:
            raise RuntimeError(f'Phase{phase} exact check failed: {run.stderr}')
        out = json.loads(run.stdout)
        if out['phase'] != phase:
            raise ValueError('Requested phase/certificate mismatch')
        results.append(out)
        guidance_path = a.work/f'guidance-{phase:03d}.json'
        if guidance_path.exists() and json.loads(guidance_path.read_text())['status'] != 'Optimal':
            raise RuntimeError(f'Non-optimal guidance at phase{phase}; positive certificate saved. Expensive sweep paused; no exclusion.')
        lower = min(v['required_edits_per_reference_color'] for v in results)
        checkpoint = {'agent':'six-vdw-3','role':'researcher','saved_at':datetime.now(timezone.utc).isoformat(),
                      'requested_range':[a.begin,a.end],'checked_in_invocation':len(results),
                      'last_phase':phase,'partial_minimum_per_color':lower,
                      'seconds':time.monotonic()-started,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      'source_sha256':hashes,'threads':1,
                      'status':'POSITIVE_PHASE_CERTIFICATES; COMPLETE_FAMILY_CHECK_PENDING'}
        (a.work/'checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
        if len(results) == 1 or (phase+1)%25 == 0:
            print(json.dumps({k:v for k,v in checkpoint.items() if k != 'source_sha256'}),flush=True)
    command = [sys.executable,str(source/'verify.py'),str(a.work),'--output',str(a.work/'verification.json')]
    completed_requested = len(results) == a.end-a.begin
    if a.begin == 0 and a.end == 617 and completed_requested:
        command.append('--require-complete')
    run = subprocess.run(command,env=env,capture_output=True,text=True,timeout=45)
    if run.returncode:
        raise RuntimeError('Directory/coverage check failed: '+run.stderr)
    print(run.stdout.strip(),flush=True)
    verified = json.loads((a.work/'verification.json').read_text())
    expected_path = source/'expected.json'
    if verified['complete'] and expected_path.exists():
        expected = json.loads(expected_path.read_text())
        for item in verified['cases']:
            target = expected['per_phase_lower_bound_each_color'][item['phase']]
            if item['required_edits_per_reference_color'] < target:
                raise RuntimeError('Regenerated positive weights miss a published phase bound; no negative conclusion')
    final = {'agent':'six-vdw-3','role':'researcher','requested_range':[a.begin,a.end],
             'completed_requested_range':completed_requested,'seconds':time.monotonic()-started,
             'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
             'source_sha256':hashes,'threads':1,'sequential_math_jobs':True,
             'published_bounds_compared':verified['complete'] and expected_path.exists(),
             'verification':json.loads(run.stdout)}
    (a.work/'reproduction.json').write_text(json.dumps(final,indent=2)+'\n')
    print(json.dumps({k:v for k,v in final.items() if k not in ['verification','source_sha256']}),flush=True)


if __name__ == '__main__':
    main()
