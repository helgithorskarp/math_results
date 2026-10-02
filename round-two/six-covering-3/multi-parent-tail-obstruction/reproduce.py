"""Sequential complete new-case reproduction, with unchanged20s child guards."""
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
    root = Path(__file__).resolve().parent
    out = args.scratch.resolve()
    if out == root or root in out.parents:
        raise ValueError('Generated state belongs in workspace/scratch, outside source')
    out.mkdir(parents=True, exist_ok=True)
    c = json.loads((root / 'certificate.json').read_text())
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    children = []

    def child(program, mode, args):
        cmd = [sys.executable, *(['-O'] if mode == 'optimized' else []), '-B',
               str(root / program), *map(str, args)]
        began = time.monotonic()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=20)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError('20s child guard: incomplete, no exclusion certified') from error
        if proc.returncode or proc.stderr:
            raise RuntimeError('Child failed; no exclusion: ' + proc.stderr[-2000:])
        result = json.loads(proc.stdout)
        record = dict(program=program, mode=mode, seconds=time.monotonic() - began,
                      parent=next((int(args[j + 1]) for j, a in enumerate(args)
                                   if a == '--parent'), None),
                      exit_code=0, stderr_empty=True, result=result)
        children.append(record)
        print(json.dumps({k: v for k, v in record.items() if k != 'result'}), flush=True)
        return result

    baseline = {}
    for mode in ('normal', 'optimized'):
        for parent in (1, 2, 3, 5, 6, 7):
            records = out / (f'parent{parent}-{mode}.records')
            summary = out / (f'parent{parent}-{mode}.json')
            produced = child('generate.py', mode,
                             ('--parent', parent, '--records', records, '--output', summary))
            expected = next(case for case in c['cases'] if case['parent'] == parent)
            if produced != expected or json.loads(summary.read_text()) != expected:
                raise ValueError('Complete produced case certificate differs')
            audit = child('check.py', mode, ('--parent', parent, '--records', records))
            if mode == 'normal':
                baseline[parent] = audit
            elif audit != baseline[parent]:
                raise ValueError('Complete normal/optimized AP records differ')
    controls = child('controls.py', 'normal', ('--scratch', out))
    if controls != child('controls.py', 'optimized', ('--scratch', out)):
        raise ValueError('Normal/optimized scope controls differ')
    source = {p.name: sha256(p.read_bytes()).hexdigest() for p in root.iterdir()
              if p.is_file() and (p.suffix == '.py' or p.name == 'certificate.json')}
    for row in children:
        r = row.pop('result')
        keys = ('parent', 'records', 'required', 'total_upper_range', 'all_rows38H_sha256',
                'required_points_sha256', 'universal_outside_holes_at_least',
                'all270_records_entrywise_equal', 'independent_literal_AP_audit',
                'controls', 'definition_level_maximum_rows', 'toy_prefix_upper_bounds',
                'original_BASE_TAIL_partition', 'all_original_BASE_AP_lift_points',
                'all_original_TAIL_AP_parent_points', 'CRT_multipliers', 'parent_orbits')
        row['compact_result'] = {k: r[k] for k in keys if k in r}
    receipt = dict(agent='six-covering-3', role='researcher', utc=datetime.now(timezone.utc).isoformat(),
                   python=platform.python_version(), dependencies='standard library only',
                   child_guard_seconds=20, threads=1, one_CPU_child_at_a_time=True,
                   maximum_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   all_six_new_cases_complete=True, raw_branch_records=1620,
                   original_marginal_entries=55080, phase_intersections=14978520,
                   all_records_entrywise_compared=True, symmetry_reduction=False,
                   native_solver=False, external_independent_review=False,
                   elementary_bridges_unformalized=True,
                   parent4_dependency='Published lemma9709, separately reproducible in parent4-base-obstruction',
                   full_prefix_or_global_Lmin8_exclusion=False,
                   source_sha256=source, children=children)
    (out / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('all_six_new_cases_complete',
                      'raw_branch_records', 'all_records_entrywise_compared',
                      'maximum_child_RSS_KiB')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
