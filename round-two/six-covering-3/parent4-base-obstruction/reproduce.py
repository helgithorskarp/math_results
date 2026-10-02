"""Bounded sequential source reproduction; no solver and no live-job pools."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import platform
import resource
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    out = args.scratch.resolve()
    root = Path(__file__).resolve().parent
    if out == root or root in out.parents:
        raise ValueError('Generated receipts belong in workspace/scratch, outside source')
    out.mkdir(parents=True, exist_ok=True)
    c = json.loads((root / 'certificate.json').read_text())
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    receipts = []

    def child(program, flags=(), arguments=()):
        before = time.monotonic()
        cmd = [sys.executable, *flags, '-B', str(root / program), *map(str, arguments)]
        try:
            proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=20)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError('20s child guard: incomplete; no exclusion certified') from error
        if proc.returncode or proc.stderr:
            raise RuntimeError('Child failed; no exclusion certified: ' + proc.stderr[-2000:])
        result = json.loads(proc.stdout)
        receipts.append(dict(program=program, flags=list(flags),
                             stage=next((int(arguments[i + 1]) for i, a in enumerate(arguments)
                                         if a == '--stage'), None),
                             seconds=time.monotonic() - before, exit_code=proc.returncode,
                             stderr_empty=True, result=result))
        print(json.dumps({k: v for k, v in receipts[-1].items() if k != 'result'}), flush=True)
        return result

    a = child('check_affine.py')
    if a != child('check_affine.py', ('-O',)):
        raise ValueError('Normal/optimized affine outputs differ')
    for stage in (1, 2, 3, 4):
        path = out / ('produced-stage' + str(stage) + '.json')
        child('generate.py', arguments=('--stage', stage, '--output', path))
        if json.loads(path.read_text()) != c['stages'][stage - 1]:
            raise ValueError('Full produced stage certificate differs')
    normal = [child('check_stage.py', arguments=('--stage', stage)) for stage in (1, 2, 3, 4)]
    optimized = [child('check_stage.py', ('-O',), ('--stage', stage)) for stage in (1, 2, 3, 4)]
    if normal != optimized:
        raise ValueError('Complete normal/optimized AP stage outputs differ')
    controls = child('controls.py')
    if controls != child('controls.py', ('-O',)):
        raise ValueError('Normal/optimized controls differ')
    if c['stages'][-1]['retained_vectors'] != 0 or c['stages'][-1]['total_upper_range'][1] >= 1118:
        raise ValueError('Complete frontier is nonempty; no exclusion')
    source = {p.name: sha256(p.read_bytes()).hexdigest() for p in root.iterdir()
              if p.is_file() and (p.suffix == '.py' or p.name == 'certificate.json')}
    summaries = []
    for receipt in receipts:
        r = receipt['result']
        keys = ('stage', 'records', 'retained_vectors', 'total_upper_range',
                'all_rows38H_sha256', 'required_points_sha256', 'independent_literal_AP_audit',
                'all_raw_original_phase_actions', 'complete_prefix_group', 'pair_orbits',
                'all_phase_permutations_sha256', 'all_pair_normalizers_sha256',
                'all_physical_point_transports', 'all_original_phase_permutations',
                'controls', 'toy_full_distinct_cover', 'toy_prefix_upper_bounds',
                'literal_final_gain', 'literal_remaining_capacity')
        summaries.append({k: v for k, v in receipt.items() if k != 'result'} | {
            'compact_result': {k: r[k] for k in keys if k in r}})
    result = dict(agent='six-covering-3', role='researcher', utc=datetime.now(timezone.utc).isoformat(),
                  python=platform.python_version(), dependencies='standard library only',
                  native_solver=False, child_guard_seconds=20, threads=1,
                  one_CPU_child_at_a_time=True, retained_frontier_limit=300,
                  maximum_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  all_stages_complete=True, complete_branch_records=4644,
                  retained_frontiers=[s['retained_vectors'] for s in c['stages']],
                  one_parent4_BASE_route_excluded=True, A4_assumed=False,
                  final_deficit2_conditional=True, universal_outside_holes_at_least=1,
                  allP_or_global_Lmin8_exclusion=False, ordinary_bridges_unformalized=True,
                  independent_external_review=False, source_sha256=source, children=summaries)
    (out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verification_receipt': str(out / 'verification.json'),
                      'all_stages_complete': True, 'retained_frontiers': result['retained_frontiers'],
                      'one_parent4_BASE_route_excluded': True,
                      'maximum_child_RSS_KiB': result['maximum_child_RSS_KiB']}), flush=True)


if __name__ == '__main__':
    main()
