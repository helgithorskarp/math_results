"""Frozen standard-library proof replay; optional bounded LP proposals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).parent
TRIALS = {(1427, 0): 2382, (2132, 1): 1790}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--fresh-guide', action='store_true')
    p.add_argument('--work', type=Path, default=HERE / 'build')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    begin = time.monotonic()
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        sha, name = line.split('  ', 1)
        need(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == sha,
             'Manifest mismatch: ' + name)
    env = dict(os.environ)
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[k] = '1'
    prefix = [sys.executable] + (['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else [])
    steps = []
    for job in (['verify.py', '--expected', 'expected.json'], ['controls.py']):
        r = subprocess.run(prefix + job, cwd=HERE, env=env, text=True,
                           capture_output=True, timeout=30)
        need(r.returncode == 0, 'Exact replay failed: ' + str(job) + '\n' + r.stdout + r.stderr)
        steps.append({'command': job, 'result': json.loads(r.stdout.strip().splitlines()[-1])})
    fresh = []
    if a.fresh_guide:
        import verify
        a.work.mkdir(parents=True, exist_ok=True)
        for root, files in sorted(verify.ROOT_FILES.items()):
            colors, _, vertices, _ = verify.premise(root=root)
            for i, name in enumerate(files):
                frozen_path = HERE / 'certificates' / name
                frozen_data = json.loads(frozen_path.read_text())
                frozen = verify.check_stage(frozen_data, colors, vertices, root=root)
                domain_path = (a.work / (name + '.domain.json')).absolute()
                domain_path.write_text(json.dumps({'permitted_screen': sorted(vertices)}) + '\n')
                target = (a.work / name).absolute()
                summary = (a.work / (name + '.guide.json')).absolute()
                job = ['generate.py', '--root', str(root), '--domain', str(domain_path),
                       '--plans', 'plans.json', '--denominator', str(frozen_data['denominator']),
                       '--output', str(target), '--summary', str(summary)]
                if (root, i) in TRIALS:
                    job += ['--trial-opposite', str(TRIALS[root, i])]
                r = subprocess.run(prefix + job, cwd=HERE, env=env, text=True,
                                   capture_output=True, timeout=30)
                need(r.returncode == 0, 'Optional proposal failed: ' + name + '\n' + r.stdout + r.stderr)
                guide = json.loads(summary.read_text())
                checked = verify.check_stage(json.loads(target.read_text()), colors, vertices, root=root)
                fresh.append({'root': root, 'stage': name, 'guide': guide,
                              'exact_replay_passed': True,
                              'exact_result_matches_frozen': checked == frozen,
                              'certificate_bytes_match_frozen': target.read_bytes() == frozen_path.read_bytes(),
                              'recovered_frozen_exclusion': checked['exclusion'] == frozen['exclusion'],
                              'recovered_frozen_next_domain': checked['next_domain'] == frozen['next_domain'],
                              'fresh_gap_to_cap_numerator': checked['gap_to_cap_numerator']})
                # The next proposal uses the independently proved FROZEN domain.
                # A floating guide is never used to justify that restriction.
                vertices = set(frozen['next_domain'])
    out = {'agent': 'six-vdw-3', 'role': 'researcher', 'success': True,
           'python_version': sys.version.split()[0], 'python_optimization': sys.flags.optimize,
           'steps': steps, 'fresh': fresh, 'solver_threads': 1,
           'native_solve_time_limit_seconds': 15, 'one_CPU_intensive_local_job': True,
           'elapsed_seconds': time.monotonic() - begin,
           'child_peak_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('steps', 'fresh')}, sort_keys=True)
          + '\n' + json.dumps({'exact_steps': len(steps), 'fresh_stages': len(fresh),
                               'all_fresh_results_match_frozen': all(x['exact_result_matches_frozen'] for x in fresh),
                               'all_fresh_bytes_match_frozen': all(x['certificate_bytes_match_frozen'] for x in fresh),
                               'all_fresh_domains_and_exclusions_recovered': all(x['recovered_frozen_exclusion'] and
                                   x['recovered_frozen_next_domain'] for x in fresh)}))


if __name__ == '__main__':
    main()
