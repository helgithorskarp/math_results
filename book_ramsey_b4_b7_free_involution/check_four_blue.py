"""Sequential validation of the analytic four-blue arbitrary-red-density closure.
Author: six-books-2, role researcher. Python standard library only.
Generated records, controls and logs remain outside the contribution directory.
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
    expected = json.loads((HERE / 'four_blue_expected.json').read_text())
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[name] = '1'
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

    records = scratch / 'four_blue_survivors.json'
    fast = run('fast', 'four_blue_census.py', ['--records', records])
    fast.pop('wall_seconds')
    require(fast == {k: v for k, v in expected.items() if k != 'obstruction_controls'},
            'every fast case diagnostic must match')
    separate = run('separate', 'four_blue_independent.py', ['--compare-records', records])
    require(separate['generated_labeled_four_blue_edge_sets'] == 20475
            and separate['generated_unlabeled_blue_forms'] == 11, 'independent form coverage')
    for key in ('all_survivor_flag_entries_match', 'all_case_diagnostics_match', 'literal_page_tables',
                'validation_not_theorem_premise', 'complete'):
        require(separate[key] is True, 'separate guard: ' + key)
    for key in ('all_red_subsets', 'at_least_three_red_subsets', 'matching_budget_pass',
                'necessary_red_survivors', 'inside_flag_survivors', 'full_matching_sign_enumeration'):
        require(separate[key] == expected[key], 'separate diagnostic: ' + key)
    require(separate['obstruction_controls'] == expected['obstruction_controls'], 'exact obstruction controls')
    original = json.loads(records.read_text())
    changed = copy.deepcopy(original)
    changed[0]['flags'][0] = 1
    bad_flag = scratch / 'changed_flag.json'
    bad_flag.write_text(json.dumps(changed) + '\n')
    missing = scratch / 'missing_survivor.json'
    missing.write_text('[]\n')
    for label, path in [('changed_flag', bad_flag), ('missing_survivor', missing)]:
        run(label, 'four_blue_independent.py', ['--compare-records', path], reject=True)
    summary = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
               'validation_not_theorem_premise': True, 'blue_forms': 11,
               'all_red_candidate_subsets': expected['all_red_subsets'],
               'at_least_three_red_subsets': expected['at_least_three_red_subsets'],
               'necessary_survivors': 1, 'inside_flag_survivors': 128,
               'all_survivor_flag_entries_match': True,
               'independently_generated_labeled_blue_sets': 20475,
               'obstruction_controls': separate['obstruction_controls'],
               'targeted_corruptions_rejected': 2, 'threads': 1,
               'full_matching_sign_enumeration': False,
               'wall_seconds': time.monotonic() - start,
               'peak_child_rss_kib_linux': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'measurements': measurements}
    (scratch / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
