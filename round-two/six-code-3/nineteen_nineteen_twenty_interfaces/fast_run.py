"""Whole-case dual-engine census with independently decoded full universes.

The new scheduling removes per-query Python IPC. Sources are SHA-bound.
The same-author include/exclude and colored executions do not constitute
a new independent peer review of the mixed19/19/20 theorem.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import time

from bindings import HERE, PRIOR, v, verifier
from verify import input_case, joint


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(executables):
    sources = {name: digest(HERE / name) for name in
               ('bindings.py', 'verify.py', 'reviewer_kernel.hpp', 'fast_census.cpp', 'fast_run.py')}
    sources['prior_color_server.cpp'] = digest(PRIOR / 'color_server.cpp')
    sources['prior_verify.py'] = digest(PRIOR / 'verify.py')
    return {'sources': sources, 'executables': [digest(exe) for exe in executables],
            'native_node_guard': 2000000, 'query_seconds': 20, 'whole_case_seconds': 60,
            'wrapper_seconds': 65}


def literal(case, orientation):
    star, rows, cols, fixed = input_case(case, orientation)
    ts, covers, nodes = verifier.covers(fixed)
    yw, ya = v.base(rows, fixed, 15)
    zw, za = v.base(cols, fixed, 16)
    universe = {'triples': [v.bits(t) for t in ts],
                'y_words': [v.bits(w) for w in yw], 'z_words': [v.bits(w) for w in zw],
                'covers_sha256': v.sha(covers),
                'y_adjacency_sha256': v.sha([sorted(row) for row in ya]),
                'z_adjacency_sha256': v.sha([sorted(row) for row in za]),
                'tail_y_sha256': v.sha([[i for i, w in enumerate(yw) if len(w & (t | {15, 16})) <= 2] for t in ts]),
                'tail_z_sha256': v.sha([[i for i, w in enumerate(zw) if len(w & (t | {15, 16})) <= 2] for t in ts]),
                'z_to_y_sha256': v.sha([[i for i, w in enumerate(yw) if len(w & z) <= 2] for z in zw])}
    return star, sorted(v.bits(w) for w in fixed), len(covers), universe, nodes


def run_case(case, orientation, work, executables, slow_work=None, resume=False):
    begun = time.monotonic();work.mkdir(parents=True, exist_ok=True)
    source_binding = fingerprint(executables)
    seal_path = work / f'fast-sealed-{case}-{orientation}.json'
    result_path = work / f'fast-case-{case}-{orientation}.json'
    if resume and seal_path.exists():
        seal = json.loads(seal_path.read_text())
        v.check(seal['status'] == 'COMPLETE_LOCAL_DUAL_ENGINE_EXECUTION', 'fast resume status')
        v.compare(seal['binding'], source_binding, 'fast resume source/executable mismatch')
        v.check(seal['result_sha256'] == digest(result_path), 'fast resume result byte mismatch')
        result = json.loads(result_path.read_text())
        v.check(result['status'] == 'COMPLETE_SELECTED_DUAL_ENGINE_ORIENTATION' and
                result['case'] == case and result['orientation'] == orientation, 'fast resume completed domain')
        return result
    star, fixed, cover_count, expected_universe, cover_nodes = literal(case, orientation)
    input_path = work / f'input-{case}-{orientation}.txt'
    input_path.write_text('\n'.join(map(str, fixed)) + '\n')
    outputs = []
    for engine, executable in enumerate(executables):
        done = subprocess.run([str(executable.resolve()), str(case), str(orientation), str(input_path)],
                              capture_output=True, text=True, timeout=65)
        v.check(done.returncode == 0, 'INCOMPLETE fast engine: ' + done.stderr[-2000:])
        output = json.loads(done.stdout)
        v.check(output['status'] == 'COMPLETE' and output['case'] == case and
                output['orientation'] == orientation and output['engine'] == engine and
                output['covers'] == cover_count, 'fast engine complete/domain binding')
        v.compare(output['universes'], expected_universe, 'fast/literal full candidate/edge/cover universes')
        (work / f'native-{engine}-{case}-{orientation}.json').write_bytes(v.encode(output))
        outputs.append(output)
    exact_keys = ('case', 'orientation', 'covers', 'z_eleven', 'y_ten', 'carrier_sha256', 'universes', 'intervals', 'cores')
    v.compare({k: outputs[0][k] for k in exact_keys}, {k: outputs[1][k] for k in exact_keys},
              'dual-engine full transcript/core mismatch')
    intervals = outputs[0]['intervals']
    v.check(intervals[0]['start'] == 0 and intervals[-1]['finish'] == cover_count and
            all(a['finish'] == b['start'] for a, b in zip(intervals, intervals[1:])),
            'fast full-case interval gap/overlap')
    for record in outputs[0]['cores']:
        words = [v.points(mask) for mask in record['blocks']]
        joint(words)
        v.check(record['core_sha256'] == v.sha(sorted(record['blocks'])), 'fast literal core hash')
        v.check(record['y_m'] == v.stats(words, 15)['m'], 'fast literal nineteen-star statistic')
        v.check(record['case'] == case and record['orientation'] == orientation and
                0 <= record['cover'] < cover_count and
                sorted(record['blocks']) == record['blocks'], 'fast literal core metadata')
    v.check(len(outputs[0]['cores']) == outputs[0]['y_ten'] and
            len({r['core_sha256'] for r in outputs[0]['cores']}) == outputs[0]['y_ten'],
            'fast complete distinct core count')
    slow_comparison = None
    if slow_work is not None and (slow_work / f'census-case-{case}-{orientation}.json').exists():
        slow = json.loads((slow_work / f'census-case-{case}-{orientation}.json').read_text())
        v.check(slow['status'] == 'COMPLETE_SELECTED_MARKED_ORIENTATION_ONLY', 'incomplete slow regression')
        prior = []
        for old, native in zip(slow['intervals'], intervals):
            v.check(old['start'] == native['start'] and old['finish'] == native['finish'] and
                    old['primary']['carrier_sha256'] == native['carrier_sha256'] and
                    old['primary']['counts']['z_eleven'] == native['z_eleven'] and
                    old['primary']['counts']['y_ten'] == native['y_ten'], 'entrywise slow/fast interval regression')
            path = slow_work / f"saturated-joints-{case}-{orientation}-{old['start']}-{old['finish']}.json"
            v.check(digest(path) == old['checked']['joints_sha256'], 'changed slow regression cores')
            prior.extend(json.loads(path.read_text()))
        v.check(len(slow['intervals']) == len(intervals), 'slow regression interval coverage')
        v.compare(prior, outputs[0]['cores'], 'entrywise slow/fast all literal cores')
        slow_comparison = {'status': 'COMPLETE_ENTRYWISE_SLOW_FAST_REGRESSION', 'covers': cover_count,
                           'cores': len(prior), 'intervals': len(intervals)}
    v.compare(fingerprint(executables), source_binding, 'fast execution source/executable mutation')
    result = {'status': 'COMPLETE_SELECTED_DUAL_ENGINE_ORIENTATION', 'case': case, 'orientation': orientation,
              'input_m': star['m'], 'input_model': star['model'], 'covers': cover_count,
              'z_eleven': outputs[0]['z_eleven'], 'core_count': outputs[0]['y_ten'],
              'carrier_sha256': outputs[0]['carrier_sha256'], 'universes': expected_universe,
              'intervals': intervals, 'cores': outputs[0]['cores'], 'binding': source_binding,
              'literal_cover_nodes': cover_nodes, 'slow_regression': slow_comparison,
              'measurements': [{'engine': out['engine'], 'seconds': out['seconds'],
                               'z_nodes': out['z_nodes'], 'y_nodes': out['y_nodes'],
                               'peak_query_nodes': out['peak_query_nodes']} for out in outputs],
              'seconds': time.monotonic() - begun}
    result_path.write_bytes(v.encode(result))
    seal_path.write_bytes(v.encode({'status': 'COMPLETE_LOCAL_DUAL_ENGINE_EXECUTION',
                                  'binding': source_binding, 'result_sha256': digest(result_path)}))
    print(json.dumps({k: result[k] for k in ('status', 'case', 'orientation', 'covers', 'core_count', 'z_eleven', 'seconds', 'slow_regression')}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', type=int, nargs='+', required=True)
    parser.add_argument('--orientations', type=int, choices=(0, 1), nargs='+', default=[0, 1])
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--include-executable', type=Path, required=True)
    parser.add_argument('--color-executable', type=Path, required=True)
    parser.add_argument('--slow-work', type=Path)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    v.check(len(args.cases) == len(set(args.cases)) and all(0 <= case < 46 for case in args.cases), 'fast cases domain')
    v.check(len(args.orientations) == len(set(args.orientations)), 'fast orientations domain')
    outputs = [run_case(case, orientation, args.work, [args.include_executable, args.color_executable],
                        args.slow_work, args.resume) for case in args.cases for orientation in args.orientations]
    print(json.dumps({'status': 'COMPLETE_ALL92_JOINT_ORIENTATIONS' if set(args.cases) == set(range(46))
                      and set(args.orientations) == {0, 1} else 'COMPLETE_SELECTED_JOINT_ORIENTATIONS',
                      'orientations': len(outputs), 'covers': sum(r['covers'] for r in outputs),
                      'cores': sum(r['core_count'] for r in outputs),
                      'scope': 'Joint-star census only; residual certificates remain separate.'}), flush=True)
