"""Sequential exact reduction for the ten-uniform-pair theorem.
Author: six-books-2, role researcher. Python 3.11+ standard library only.
The finite quotient reduction is a theorem premise; see NINE.md.
"""
import argparse
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
    expected = json.loads((HERE / 'nine_expected.json').read_text())
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    start = time.monotonic()
    measurements = []

    def run(label, script, arguments):
        before = time.monotonic()
        result = subprocess.run([sys.executable, '-O', str(HERE / script),
                                 *[str(a) for a in arguments]], env=env,
                                capture_output=True, text=True, timeout=120)
        (scratch / (label + '.stdout')).write_text(result.stdout)
        (scratch / (label + '.stderr')).write_text(result.stderr)
        measurements.append({'step': label, 'returncode': result.returncode,
                             'wall_seconds': time.monotonic() - before})
        require(result.returncode == 0, label + ' failed: ' + result.stderr[-2000:])
        return json.loads(result.stdout)

    records = scratch / 'nine_survivors.json'
    fast = run('fast', 'nine_census.py', ['--records', records])
    fast.pop('wall_seconds')
    require(fast == {k: v for k, v in expected.items()
                     if k not in ('survivors', 'independent_generation')},
            'every fast case diagnostic must match')
    require(json.loads(records.read_text()) == expected['survivors'],
            'every fast survivor and inside flag matches the compact fixture')
    separate = run('separate', 'nine_independent.py', ['--compare-records', records])
    for key in ('complete', 'every_case_diagnostic_matches', 'every_survivor_flag_entry_matches',
                'every_red_candidate_position_matches'):
        require(separate[key] is True, 'separate guard: ' + key)
    for key in ('blue_forms', 'red_triples', 'support_pass', 'matching_pass',
                'necessary_survivors', 'inside_flag_survivors', 'degree_theorem_used',
                'full_matching_sign_enumeration'):
        require(separate[key] == expected[key], 'separate diagnostic: ' + key)
    for key, value in expected['independent_generation'].items():
        require(separate[key] == value, 'independent generation: ' + key)
    require(separate['targeted_corruptions_rejected'] == 2, 'both malformed records rejected')
    summary = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
               'finite_reduction_is_theorem_premise': True,
               'six_blue_augmentations': expected['six_blue_augmentations'],
               'blue_forms': expected['blue_forms'], 'red_triples': expected['red_triples'],
               'support_pass': expected['support_pass'], 'matching_pass': expected['matching_pass'],
               'necessary_survivors': expected['necessary_survivors'],
               'inside_flag_survivors': expected['inside_flag_survivors'],
               'all_survivor_flag_entries_match': True,
               'all_red_candidate_positions_match': True, 'all_case_diagnostics_match': True,
               'connected_labeled_edge_sets': separate['connected_labeled_edge_sets'],
               'connected_catalog_sizes_by_edge_count': separate['connected_catalog_sizes_by_edge_count'],
               'connected_generation_domains': separate['connected_generation_domains'],
               'analytic_templates': separate['analytic_templates'],
               'targeted_corruptions_rejected': 2, 'threads': 1,
               'full_matching_sign_enumeration': False, 'degree_theorem_used': False,
               'wall_seconds': time.monotonic() - start,
               'peak_child_rss_kib_linux': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'measurements': measurements}
    (scratch / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
