"""Serial, fresh source-only certificate replay. six-code-2, researcher.

Each ordinary mathematical child retains60s/2M and a60s process bound.
Normal and optimized runs start from separate source copies and fixtures.
Complete packets are hashed and all fields compared. Only measured time,
RSS, and a raw producer-summary hash are normalized; the latter is first
checked against that mode's actual unnormalized summary. No private
generated graph or point-map packet is an input. Incomplete means no bound.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n').encode()


def pin(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            block = f.read(1 << 20)
            if not block:
                break
            digest.update(block)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def read(path):
    return json.loads(path.read_bytes())


def summary(path):
    x = read(path)
    need('seconds' in x and 'peak_RSS_kib' in x, 'exact allowed execution fields')
    return {k: v for k, v in x.items() if k not in ('seconds', 'peak_RSS_kib')}


def physical(path, raw_summary):
    x = read(path)
    need(x['producer_summary_sha256'] == pin(raw_summary)['sha256'], 'actual raw-summary pin before normalization')
    return {k: v for k, v in x.items() if k != 'producer_summary_sha256'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['normal', 'optimized'], required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--normal', type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    need(not work.exists(), 'new source-only replay work directory required')
    source = Path(__file__).resolve().parent
    names = sorted(p.name for p in source.iterdir() if p.is_file() and
                   (p.suffix == '.py' or p.name in ('PARENT.json', 'SPEC.json', 'PRIOR_EXPECTATIONS.json',
                                                  'POSITIVE_WITNESSES.json', 'baseline69.txt', 'DERIVATION.json')))
    frozen = {name: pin(source / name) for name in names}
    if args.mode == 'optimized':
        need(args.normal is not None, 'optimized run requires completed normal replay')
        normal = args.normal.resolve()
        need(read(normal / 'JOURNAL.json')['status'] == 'COMPLETE_SOURCE_ONLY_ALL13_CASES',
             'normal source-only replay not complete')
        need(read(normal / 'FROZEN_PLAN.json')['sources_and_fixtures'] == frozen,
             'normal and optimized source/fixture bytes differ')
    else:
        need(args.normal is None, 'normal run must not seed from another replay')
        normal = None
    work.mkdir(parents=True)
    local_source = work / 'source'
    local_source.mkdir()
    for name in names:
        shutil.copyfile(source / name, local_source / name)
    plan = {'agent': 'six-code-2', 'role': 'researcher', 'mode': args.mode,
            'sources_and_fixtures': frozen, 'original_seconds': 60, 'original_states': 2000000,
            'child_process_seconds': 60, 'native_threads': 1, 'serial_children': True,
            'private_generated_inputs': [],
            'normalization': {'producer_summary': ['seconds', 'peak_RSS_kib'],
                              'physical_result': ['producer_summary_sha256 AFTER actual raw pin verification'],
                              'all_other_fields': 'retain and compare whole',
                              'core_graph_witness_cover_finite_packets': 'compare entire byte hash and size'},
            'prior_new_ordered_trace': 'capture whole normal trace after all prior invariant fields match; optimized whole trace must equal',
            'completeness_on_failure': 'NONE; retain receipts and stop without absence'}
    (work / 'FROZEN_PLAN.json').write_bytes(encoded(plan))
    journal = {'agent': 'six-code-2', 'role': 'researcher', 'mode': args.mode,
               'status': 'RUNNING_SOURCE_ONLY_SERIAL_MATH', 'stages': [], 'completed_cases': []}
    exact = {'agent': 'six-code-2', 'role': 'researcher',
             'status': 'COMPLETE_SOURCE_ONLY_ALL13_CASES', 'cases': []}
    environment = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        environment[name] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    interpreter = [sys.executable, '-B'] + (['-O'] if args.mode == 'optimized' else [])

    def save():
        (work / 'JOURNAL.json').write_bytes(encoded(journal))

    def check_sources():
        need({n: pin(local_source / n) for n in names} == frozen,
             'source-only local copies changed during replay')
        need({n: pin(source / n) for n in names} == frozen,
             'portable original source changed during replay')

    def child(label, script, arguments):
        check_sources()
        if environment.get('DISCOVERY_OPERATIONS_STATE'):
            state = Path(environment['DISCOVERY_OPERATIONS_STATE'])
            need(not any((state / n).exists() for n in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                 'operations pause/handover barrier')
        command = interpreter + [str(local_source / script)] + [str(a) for a in arguments]
        print(json.dumps({'starting': label, 'mode': args.mode}), flush=True)
        start = time.monotonic()
        with (work / (label + '.stdout.txt')).open('wb') as out, (work / (label + '.stderr.txt')).open('wb') as err:
            try:
                result = subprocess.run(command, cwd=local_source, env=environment,
                                        stdout=out, stderr=err, timeout=60)
                code, timed_out = result.returncode, False
            except subprocess.TimeoutExpired:
                code, timed_out = None, True
        row = {'stage': label, 'command': command, 'seconds': time.monotonic() - start,
               'returncode': code, 'timed_out': timed_out,
               'stdout': pin(work / (label + '.stdout.txt')), 'stderr': pin(work / (label + '.stderr.txt'))}
        journal['stages'].append(row)
        save()
        need(code == 0 and not timed_out, 'STOP incomplete source-only child, no absence: ' + label)
        need(row['stderr']['bytes'] == 0, 'unexpected source-only child stderr: ' + label)
        check_sources()
        print(json.dumps({'completed': label, 'seconds': row['seconds']}), flush=True)

    save()
    try:
        child('finite', 'check_ordered_finite.py', ['--work', work / 'finite'])
        exact['finite'] = read(work / 'finite' / 'EXACT_RESULT.json')
        child('cover', 'cover.py', ['--parent', local_source / 'PARENT.json', '--spec', local_source / 'SPEC.json',
                                  '--work', work / 'cover'])
        child('cover-audit', 'audit_cover.py', ['--parent', local_source / 'PARENT.json',
                    '--spec', local_source / 'SPEC.json', '--cover', work / 'cover' / 'COVER.json',
                    '--work', work / 'cover-audit'])
        exact['cover'] = read(work / 'cover' / 'EXACT_RESULT.json')
        exact['cover_packet'] = pin(work / 'cover' / 'COVER.json')
        exact['physical_cover'] = read(work / 'cover-audit' / 'EXACT_RESULT.json')
        spec = read(local_source / 'SPEC.json')
        priors = {c['component']: c for c in read(local_source / 'PRIOR_EXPECTATIONS.json')}
        positives = {c['component']: c for c in read(local_source / 'POSITIVE_WITNESSES.json')}
        for c in spec['cases']:
            key = 'C%03d' % c['component']
            base = work / key
            child(key + '-caps', 'caps.py', ['--parent', local_source / 'PARENT.json', '--holes',
                                           *c['hole_words'], '--work', base / 'carrier'])
            child(key + '-graph', 'graph.py', ['--parent', local_source / 'PARENT.json',
                       '--carrier', base / 'carrier' / 'CORES.json', '--work', base / 'graph'])
            child(key + '-audit', 'audit_ordered.py', ['--carrier', base / 'carrier' / 'CORES.json',
                  '--graph', base / 'graph' / 'GRAPH.json', '--producer-summary', base / 'graph' / 'SUMMARY.json',
                  '--witness-dir', base / 'graph', '--baseline69', local_source / 'baseline69.txt',
                  '--work', base / 'audit'])
            prior = priors[c['component']]
            caps = summary(base / 'carrier' / 'SUMMARY.json')
            graph = summary(base / 'graph' / 'SUMMARY.json')
            audit = physical(base / 'audit' / 'EXACT_RESULT.json', base / 'graph' / 'SUMMARY.json')
            need(caps == prior['cap_summary'], 'whole prior cap mathematical summary differs: ' + key)
            need(graph == prior['graph_summary'], 'whole prior graph mathematical summary differs: ' + key)
            for name, value in prior['physical_invariants'].items():
                need(audit.get(name) == value, 'prior physical invariant differs: ' + key + '/' + name)
            if prior['ordered_trace_prior']:
                need(audit['ordered_edge_neighborhood_trace_sha256'] == prior['ordered_trace_prior'],
                     'entire prior ordered trace differs: ' + key)
            need(audit['five_cliques'] == 0 and audit['max_positive_size'] == c['sharp_size'],
                 'exact noK5/max-positive certificate differs')
            if c['sharp_size'] == 67:
                need(audit['four_cliques'] == 0, 'sharp67 requires exact noK4')
            packets = {}
            for filename, expectation in prior['packet_pins'].items():
                path = base / ('carrier' if filename == 'CORES.json' else 'graph') / filename
                packets[filename] = pin(path)
                need(packets[filename] == expectation, 'whole prior packet differs: ' + key + '/' + filename)
            max_witness = read(base / 'graph' / ('WITNESS%d.json' % c['sharp_size']))
            need(max_witness['words'] == positives[c['component']]['words'] and
                 max_witness['hole_words'] == positives[c['component']]['hole_words'] and
                 max_witness['size'] == positives[c['component']]['size'],
                 'published literal positive fixture differs')
            exact['cases'].append({'component': c['component'], 'caps': caps, 'graph': graph,
                                   'physical': audit, 'packets': packets})
            journal['completed_cases'].append(c['component'])
            (work / 'CHECKED_PREFIX.json').write_bytes(encoded(exact))
            save()
            if normal is not None:
                old = read(normal / 'EXACT_RESULT.json')
                old_case = next(v for v in old['cases'] if v['component'] == c['component'])
                need(exact['cases'][-1] == old_case, 'entire cold normal/O case differs: ' + key)
        need(len(exact['cases']) == 13 and journal['completed_cases'] == [c['component'] for c in spec['cases']],
             'entire thirteen-case completeness')
        if normal is not None:
            need(exact == read(normal / 'EXACT_RESULT.json'), 'entire cold normal/O result differs')
            for sub in ('finite/EXACT_RESULT.json', 'cover/EXACT_RESULT.json', 'cover/COVER.json',
                        'cover-audit/EXACT_RESULT.json'):
                need(pin(work / sub) == pin(normal / sub), 'whole cold normal/O coverage packet differs: ' + sub)
        (work / 'EXACT_RESULT.json').write_bytes(encoded(exact))
        journal['status'] = 'COMPLETE_SOURCE_ONLY_ALL13_CASES'
        journal['exact_result'] = pin(work / 'EXACT_RESULT.json')
        journal['whole_normal_optimized_equal'] = normal is not None
        save()
        print(json.dumps({'status': journal['status'], 'cases': len(exact['cases']),
                          'exact_result': journal['exact_result'],
                          'whole_normal_optimized_equal': normal is not None}), flush=True)
    except Exception as exc:
        journal['status'] = 'STOPPED_INCOMPLETE_OR_DIFFERENT_SOURCE_ONLY_REPLAY_NO_ABSENCE'
        journal['error'] = str(exc)
        save()
        raise


if __name__ == '__main__':
    main()
