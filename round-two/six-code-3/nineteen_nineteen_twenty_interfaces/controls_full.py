"""Meaningful damage controls for core coverage and literal certificates."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import tempfile

from check_witness import controls as witness_controls
from collect_fast import load
from fast_run import digest
from verify_colors import check_record, require


def rejected(call):
    try:
        call()
    except (ValueError, KeyError, FileNotFoundError):
        return
    raise ValueError('damaged proof input accepted')


def run(census_work, color_work, executables, witness):
    cores, manifest = load(census_work, executables)
    mathematical = {k: value for k, value in manifest.items() if k != 'binding'}
    from verify_colors import sha
    domain = sha(mathematical)
    core = cores[0]
    row = json.loads((color_work / 'color-0.json').read_text())
    check_record(core, row, 0, domain)
    color_damages = []
    def change(field, value):
        bad = copy.deepcopy(row); bad[field] = value; color_damages.append((core, bad))
    change('status', 'UNKNOWN')
    change('index', 1)
    change('domain_sha256', '0' * 64)
    change('core_sha256', '0' * 64)
    change('candidate_sha256', '0' * 64)
    change('candidate_count', row['candidate_count'] - 1)
    change('capacity', row['capacity'] - 1)
    change('colors', row['colors'][:-1])
    bad = copy.deepcopy(row); bad['colors'][0] = -1; color_damages.append((core, bad))
    bad = copy.deepcopy(row); bad['colors'][0] = True; color_damages.append((core, bad))
    bad = copy.deepcopy(row); bad['colors'] = [0] * len(row['colors']); bad['capacity'] = 1
    color_damages.append((core, bad))
    bad_core = copy.deepcopy(core); bad_core['blocks'][1] = bad_core['blocks'][0]
    bad_core['core_sha256'] = sha(bad_core['blocks'])
    bad_row = copy.deepcopy(row); bad_row['core_sha256'] = bad_core['core_sha256']
    color_damages.append((bad_core, bad_row))
    for changed_core, changed_row in color_damages:
        rejected(lambda c=changed_core, r=changed_row: check_record(c, r, 0, domain))
    source_result = json.loads((census_work / 'fast-case-1-0.json').read_text())
    source_seal = json.loads((census_work / 'fast-sealed-1-0.json').read_text())
    census_rejections = 0
    with tempfile.TemporaryDirectory(prefix='mixed19-controls-') as folder:
        work = Path(folder)
        result_path, seal_path = work / 'fast-case-1-0.json', work / 'fast-sealed-1-0.json'
        rejected(lambda: load(work, executables, [(1, 0)])); census_rejections += 1
        rejected(lambda: load(work, executables, [(1, 0), (1, 0)])); census_rejections += 1
        def test_mutation(mutate, reseal=True):
            result, seal = copy.deepcopy(source_result), copy.deepcopy(source_seal)
            mutate(result, seal)
            result_path.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
            if reseal:
                seal['result_sha256'] = digest(result_path)
            seal_path.write_text(json.dumps(seal, sort_keys=True, separators=(',', ':')) + '\n')
            rejected(lambda: load(work, executables, [(1, 0)]))
        mutations = [
            lambda r, s: s.update(status='UNKNOWN'),
            lambda r, s: s['binding']['sources'].update({'fast_run.py': '0' * 64}),
            lambda r, s: r.update(status='UNKNOWN'),
            lambda r, s: r.update(case=2),
            lambda r, s: r.update(orientation=1),
            lambda r, s: r['intervals'][0].update(start=1),
            lambda r, s: r['intervals'][1].update(start=0),
            lambda r, s: r.update(z_eleven=r['z_eleven'] + 1),
            lambda r, s: r.update(core_count=r['core_count'] + 1),
            lambda r, s: r['cores'].__setitem__(1, copy.deepcopy(r['cores'][0])),
        ]
        for mutation in mutations:
            test_mutation(mutation); census_rejections += 1
        test_mutation(lambda r, s: r.update(scope='changed'), reseal=False); census_rejections += 1
        result_path.write_bytes((census_work / result_path.name).read_bytes())
        seal_path.write_bytes((census_work / seal_path.name).read_bytes())
        selected, selected_manifest = load(work, executables, [(1, 0)])
        require(len(selected) == 8 and selected_manifest['status'] == 'COMPLETE_EXPLICIT_SELECTED_JOINT_DOMAINS',
                'selected interval confused with whole census')
        rejected(lambda: load(work, executables)); census_rejections += 1
    native_rejections = []
    with tempfile.TemporaryDirectory(prefix='mixed19-native-controls-') as folder:
        work = Path(folder)
        valid = [int(q) for q in (census_work / 'input-1-0.txt').read_text().split()]
        require(len(valid) == 19, 'native control fixture')
        changed = valid[:]; changed[0] = 1 << 18
        wrong_weight = valid[:]; wrong_weight[0] = 1 << 17
        repeated = valid[:]; repeated[1] = repeated[0]
        no_x = valid[:]; no_x[0] ^= 1 << 17
        covered = valid[:]; covered[0] = sum(1 << q for q in (0, 1, 15, 16, 17))
        fixtures = [('missing', None, '1', '0'), ('token', 'bad-token\n', '1', '0'),
                    ('range', changed, '1', '0'), ('weight', wrong_weight, '1', '0'),
                    ('repeat', repeated, '1', '0'), ('order', valid[::-1], '1', '0'),
                    ('short', valid[:-1], '1', '0'), ('no-x', no_x, '1', '0'),
                    ('covered', covered, '1', '0'), ('case', valid, '-1', '0'),
                    ('orientation', valid, '1', '2')]
        for executable in executables:
            count = 0
            for name, values, case, orientation in fixtures:
                path = work / (name + '.txt')
                if values is not None:
                    path.write_text(values if isinstance(values, str) else '\n'.join(map(str, values)) + '\n')
                result = subprocess.run([str(executable.resolve()), case, orientation, str(path)],
                                        capture_output=True, text=True, timeout=5)
                require(result.returncode != 0 and '"status":"COMPLETE"' not in result.stdout,
                        'malformed native census input accepted')
                count += 1
            native_rejections.append(count)
    witness_rejections = witness_controls(witness)
    return {'status': 'PASS_MEANINGFUL_DAMAGE_CONTROLS',
            'literal_color_damages_rejected': len(color_damages),
            'census_completion_damages_rejected': census_rejections,
            'native_input_damages_rejected_per_engine': native_rejections,
            'literal_witness_damages_rejected': witness_rejections,
            'selected_domain_does_not_claim_all92': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--census-work', type=Path, required=True)
    parser.add_argument('--color-work', type=Path, required=True)
    parser.add_argument('--include-executable', type=Path, required=True)
    parser.add_argument('--color-executable', type=Path, required=True)
    parser.add_argument('--witness', type=Path, default=Path(__file__).with_name('witness67.json'))
    args = parser.parse_args()
    print(json.dumps(run(args.census_work, args.color_work,
                         [args.include_executable, args.color_executable],
                         json.loads(args.witness.read_text())), sort_keys=True))
