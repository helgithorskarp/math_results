"""Reproduce the exact C3 108-edge exclusion, with independent checking."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from controls import check
from incidence import enumerate_incidences
from local_roots import enumerate_roots

HERE = Path(__file__).resolve().parent


def compact(roots,cases,completion,controls,verification):
    keep = ('placement','code','incidence_representatives','completions_tested','completions_rejected','completion_sha256')
    return dict(status='EXACT_C3_108_EXCLUSION',
        root_counts={placement:{k:data[k] for k in ('raw_survivors','canonical_roots','reduced_raw_survivors','reduced_canonical_roots')}
                     | {'reduced_representatives':list(map(int,data['reduced_groups']))}
                     for placement,data in roots.items()},
        incidence_counts=[dict(placement=case['placement'],code=case['code'],
            high_domains=case['high_domains'],low_domains=case['low_domains'],representatives=case['representatives']) for case in cases],
        incidence_sha256=hashlib.sha256(json.dumps([case['incidence_representatives'] for case in cases],
            separators=(',',':')).encode()).hexdigest(),
        outside_profiles=completion['outside_profiles'],
        completion_counts=[{k:case[k] for k in keep} for case in completion['cases']],
        total_incidences=sum(case['representatives'] for case in cases),
        total_completions=sum(case['completions_tested'] for case in completion['cases']),
        valid_completions=len(completion['valid_completions']),
        independent_status=verification['status'],controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    if work==HERE or HERE in work.parents:
        raise ValueError('generated state must be outside the source directory')
    work.mkdir(parents=True,exist_ok=True)
    started = time.monotonic()
    roots = enumerate_roots()
    (work/'roots.json').write_text(json.dumps(roots,indent=2)+'\n')
    print('complete root classes', {k:list(data['reduced_groups']) for k,data in roots.items()},flush=True)
    cases = []
    for placement,data in roots.items():
        for code in sorted(map(int,data['reduced_groups'])):
            record = enumerate_incidences(code,placement=='inside',time.monotonic()+30)
            if record['status']!='COMPLETE':
                (work/'incomplete-incidences.json').write_text(json.dumps(cases+[record],indent=2)+'\n')
                raise RuntimeError('bounded incidence enumeration incomplete; no exclusion')
            cases.append(record)
            print('complete incidence',placement,code,record['representatives'],flush=True)
    incidences = work/'incidences.json'
    incidences.write_text(json.dumps(cases,indent=2)+'\n')
    control_result = check(cases)
    (work/'controls.json').write_text(json.dumps(control_result,indent=2)+'\n')
    print('literal positive/damage controls pass',control_result['damages_rejected'],flush=True)
    completion_path = work/'completions.json'
    command = [sys.executable]+(['-O'] if sys.flags.optimize else [])
    subprocess.run(command+[str(HERE/'complete.py'),'--incidences',str(incidences),
        '--output',str(completion_path),'--seconds','30'],check=True)
    completion = json.loads(completion_path.read_text())
    if completion['status']!='COMPLETE' or completion['valid_completions']:
        raise RuntimeError('no complete zero-survivor exclusion')
    # The independent child always runs with -O; all checks must survive it.
    independent_path = work/'independent.json'
    subprocess.run([sys.executable,'-O',str(HERE/'independent.py'),'--incidences',str(incidences),
        '--expected',str(completion_path),'--output',str(independent_path)],check=True)
    verification = json.loads(independent_path.read_text())
    summary = compact(roots,cases,completion,control_result,verification)
    (work/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    expected_path = HERE/'expected.json'
    if not expected_path.exists():
        raise RuntimeError('expected.json missing; generated summary preserved for author inspection')
    if summary != json.loads(expected_path.read_text()):
        raise ValueError('complete result differs from expected.json')
    print('EXACT_C3_108_EXCLUSION',summary['total_incidences'],'incidences',
          summary['total_completions'],'completions; zero survivors; seconds',time.monotonic()-started,flush=True)


if __name__ == '__main__':
    main()
