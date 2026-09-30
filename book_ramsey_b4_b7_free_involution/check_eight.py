"""Sequential exact reduction and local controls for the nine-pair theorem.
Author: six-books-2, role researcher. Python standard library only.
The finite quotient reduction is a theorem premise; controls sample signs.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    require(scratch != HERE and HERE not in scratch.parents,
            'scratch must be outside the contribution directory')
    scratch.mkdir(parents=True, exist_ok=True)
    expected = json.loads((HERE / 'eight_expected.json').read_text())
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    start = time.monotonic()
    measurements = []

    def run(label, script, arguments, reject=False):
        before = time.monotonic()
        result = subprocess.run([sys.executable, '-O', str(HERE / script),
                                 *[str(a) for a in arguments]], env=env,
                                capture_output=True, text=True, timeout=120)
        (scratch / (label + '.stdout')).write_text(result.stdout)
        (scratch / (label + '.stderr')).write_text(result.stderr)
        measurements.append({'step': label, 'returncode': result.returncode,
                             'expected_rejection': reject,
                             'wall_seconds': time.monotonic() - before})
        if reject:
            require(result.returncode != 0 and 'all survivor and flag entries must match' in result.stderr,
                    label + ' must reject the corrupted record for its entry mismatch')
            return None
        require(result.returncode == 0, label + ' failed: ' + result.stderr[-2000:])
        return json.loads(result.stdout)

    records = scratch / 'eight_survivors.json'
    fast = run('fast', 'eight_census.py', ['--records', records])
    fast.pop('wall_seconds')
    require(fast == {k: v for k, v in expected.items()
                     if k not in ('analytic_templates', 'obstruction_controls')},
            'every fast case diagnostic must match')
    separate = run('separate', 'eight_independent.py', ['--compare-records', records])
    for key in ('complete', 'every_case_diagnostic_matches', 'every_survivor_flag_entry_matches',
                'every_red_candidate_position_matches'):
        require(separate[key] is True, 'separate guard: ' + key)
    for key in ('blue_forms', 'red_triples', 'matching_pass', 'necessary_survivors',
                'inside_flag_survivors', 'analytic_templates', 'degree_theorem_used',
                'full_matching_sign_enumeration'):
        require(separate[key] == expected[key], 'separate diagnostic: ' + key)
    require(separate['connected_catalog_sizes_by_edge_count'] == {'1': 1, '2': 1, '3': 3, '4': 5, '5': 12},
            'complete connected catalogs')
    domains = separate['connected_generation_domains']
    require([(c['vertices'], c['edges'], c['edge_sets']) for c in domains]
            == [(2, 1, 1), (3, 2, 3), (3, 3, 1), (4, 3, 20), (4, 4, 15),
                (4, 5, 6), (5, 4, 210), (5, 5, 252), (6, 5, 3003)],
            'all connected generation domains')
    controls = run('controls', 'eight_controls.py', [])
    require(controls == expected['obstruction_controls'], 'every exact local-obstruction control')
    original = json.loads(records.read_text())
    changed = copy.deepcopy(original)
    old = changed[0]['flags'][0]
    replacement = next(old ^ (1 << bit) for bit in range(11)
                       if (old ^ (1 << bit)) not in changed[0]['flags'])
    changed[0]['flags'][0] = replacement
    bad_flag = scratch / 'changed_flag.json'
    bad_flag.write_text(json.dumps(changed) + '\n')
    missing = scratch / 'missing_survivor.json'
    missing.write_text(json.dumps(original[1:]) + '\n')
    for label, path in [('changed_flag', bad_flag), ('missing_survivor', missing)]:
        run(label, 'eight_independent.py', ['--compare-records', path], reject=True)
    summary = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
               'finite_reduction_is_theorem_premise': True,
               'five_blue_augmentations': expected['five_blue_augmentations'],
               'blue_forms': expected['blue_forms'], 'red_triples': expected['red_triples'],
               'matching_pass': expected['matching_pass'],
               'necessary_survivors': expected['necessary_survivors'],
               'inside_flag_survivors': expected['inside_flag_survivors'],
               'all_survivor_flag_entries_match': True,
               'all_red_candidate_positions_match': True,
               'all_case_diagnostics_match': True,
               'separate_connected_labeled_edge_sets': sum(c['edge_sets'] for c in domains),
               'connected_generation_domains': domains,
               'analytic_templates': separate['analytic_templates'],
               'obstruction_controls': controls, 'targeted_corruptions_rejected': 2,
               'threads': 1, 'full_matching_sign_enumeration': False,
               'degree_theorem_used': False, 'wall_seconds': time.monotonic() - start,
               'peak_child_rss_kib_linux': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'measurements': measurements}
    (scratch / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
