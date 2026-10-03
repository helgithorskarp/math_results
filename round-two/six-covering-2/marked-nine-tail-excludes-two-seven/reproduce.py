"""Fresh exact arithmetic/audits/controls: serialized20s children,55s parent."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('normal', 'optimized'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    expected = json.loads((source/'expected.json').read_text())
    work = args.out.resolve()
    require(not work.exists(), 'Fresh output directory required')
    work.mkdir(parents=True)
    threads = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'NUMEXPR_NUM_THREADS', 'NUMEXPR_MAX_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
    env = {'PATH': os.defpath, 'PYTHONDONTWRITEBYTECODE': '1', **{k: '1' for k in threads}}
    flags = ['-I', '-B'] + (['-O'] if args.mode == 'optimized' else [])
    target = lambda name: str(work/name)
    plan = [
        ['small.py', '--out', target('small.json'), '--raw', target('small.raw')],
        ['small_audit.py', '--reference', target('small.json'), '--reference-raw', target('small.raw'),
         '--out', target('audit-small.json'), '--raw', target('audit-small.raw')],
        ['capacity.py', '--out', target('capacity.json')],
        ['capacity_audit.py', '--reference', target('capacity.json'), '--out', target('audit-capacity.json')],
        ['projection.py', '--capacity', target('capacity.json'), '--out', target('projection.json')],
        ['projection_audit.py', '--capacity', target('audit-capacity.json'), '--reference', target('projection.json'),
         '--out', target('audit-projection.json')],
        ['physical.py', '--out', target('physical.json'), '--raw', target('physical.raw')],
        ['physical.py', '--audit', '--reference', target('physical.json'), '--reference-raw', target('physical.raw'),
         '--out', target('audit-physical.json'), '--raw', target('audit-physical.raw')],
        ['controls.py', '--work', str(work), '--out', target('controls.json')],
    ]
    receipts = []
    start = time.monotonic()
    failed = False
    for stage in plan:
        remaining = 55 - (time.monotonic()-start)
        if remaining <= 0:
            receipts.append({'stage': stage[0], 'status': 'INCOMPLETE parent55s; no exclusion'})
            failed = True
            break
        began = time.monotonic()
        try:
            result = subprocess.run([sys.executable, *flags, str(source/stage[0]), *stage[1:]],
                                    cwd=work, env=env, capture_output=True, text=True, timeout=min(20, remaining))
            row = {'stage': stage[0], 'status': 'COMPLETE' if result.returncode == 0 else 'ERROR',
                   'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
            failed = result.returncode != 0
        except subprocess.TimeoutExpired:
            row = {'stage': stage[0], 'status': 'INCOMPLETE20s or remaining parent55s; no exclusion'}
            failed = True
        row['seconds'] = time.monotonic()-began
        receipts.append(row)
        (work/'completed-stages.json').write_text(json.dumps(receipts, sort_keys=True, indent=2)+'\n')
        if failed:
            break
    record = {'agent': 'six-covering-2', 'role': 'researcher', 'mode': args.mode,
              'python': sys.version, 'seconds': time.monotonic()-start, 'stages': receipts,
              'child_guard_seconds': 20, 'parent_budget_seconds': 55, 'all_threads': 1,
              'one_intensive_child_at_a_time': True, 'source_only_fresh_arithmetic_inputs': True,
              'peak_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'ordinary_proof_formalized': False, 'independent_person_reviewed': False,
              'global_bound_changed': False, 'new_tenth_tail_bound_claimed': False}
    if failed:
        record['status'] = 'INCOMPLETE; no exclusion established by this run'
        (work/'verification.json').write_text(json.dumps(record, sort_keys=True, indent=2)+'\n')
        raise SystemExit(2)
    pins = []
    for pin in expected['mathematical_records']:
        raw = (work/pin['name']).read_bytes()
        require(raw == (work/('audit-'+pin['name'])).read_bytes(), 'Entire freshly rebuilt evidence differs')
        actual = {'name': pin['name'], 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}
        require(actual == pin, 'Expected reproducibility pin differs: '+pin['name'])
        pins.append(actual)
    small = json.loads((work/'small.json').read_text())
    capacity = json.loads((work/'capacity.json').read_text())
    projection = json.loads((work/'projection.json').read_text())
    physical = json.loads((work/'physical.json').read_text())
    checks = json.loads((work/'controls.json').read_text())
    other_upper = max(c for t in capacity['all_types'] for c in t['all_caps'] if c < 87)
    census = {'initial_R': len(small['initial_R']), 'initial_R2': len(small['initial_R2']),
              'initial_R6': len(small['initial_R6']), 'unused_BASE_originals': len(small['all_unused_BASE_originals']),
              'unused_BASE_phases': small['all_BASE_phase_count'],
              'shadow_phase_entries': sum(len(f[1]) for s in small['mirrored_small_shadows'] for f in s.get('all_BASE_phase_rows', [])),
              'inventories': capacity['original_inventory_count'],
              'inventory_cuts': capacity['binary_H_missing_Q_arm_cuts_checked'],
              'phase42_parent6_upper': capacity['uniform_parent6_upper'],
              'remaining_inventories': projection['inventory_count'], 'role_cases': projection['all_role_assignments'],
              'coupled_mod3_cases': projection['all_unpruned_mod3_phase_cases'],
              'remaining_inventory_upper': projection['uniform_role_branch_upper'],
              'other_inventory_upper': other_upper, 'BASE_hole_upper': 90 + max(other_upper, projection['uniform_role_branch_upper']),
              'imported_BASE_hole_lower': 177, 'survivors': projection['survivor_count'],
              'original_phase_rows': len(physical['all_original_phase_masks']),
              'physical_membership_checks': physical['physical_n_phase_membership_checks'],
              'semantic_negative_controls': checks['negative_count'], 'semantic_positive_controls': len(checks['positive_controls'])}
    require(census == expected['complete_census'], 'Complete census differs')
    require(small['small_cofactors_excluded'] == [5, 9] and
            small['remaining_parent2_H_phases_ge27'] == [[48, 26, 90], [48, 42, 60]], 'Parent2 reduction missing')
    require(capacity['phase42_excluded_by_uniform_capacity'] and census['phase42_parent6_upper'] < 117,
            'Phase42 exclusion missing')
    require(census['survivors'] == 0 and census['BASE_hole_upper'] < census['imported_BASE_hole_lower'],
            'No BASE177 contradiction')
    record['seconds'] = time.monotonic()-start
    require(record['seconds'] <= 55, 'INCOMPLETE parent55s; no exclusion established by this run')
    record.update({'status': 'COMPLETE AUTHOR-CHECKED CONDITIONAL TWO/SEVEN EXCLUSION; independent review pending',
                   'mathematical_records': pins, 'complete_census': census,
                   'semantic_controls_complete': True, 'all_whole_records_and_raw_bytes_agree': True,
                   'remaining_two_parent_counts': [[3, 6], [4, 5], [5, 4]]})
    (work/'verification.json').write_text(json.dumps(record, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: record[k] for k in ('status', 'mode', 'seconds', 'peak_child_RSS_KiB', 'complete_census')}))


if __name__ == '__main__':
    main()
