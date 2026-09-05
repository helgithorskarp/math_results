#!/usr/bin/env python3
"""Extract small clause cores; check their support and replay general DRAT."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys
import time

import audit
import model
from run import atomic


def replay(drat, cnf, proof, log, extra=()):
    with log.open('w') as stream:
        process = subprocess.run([str(drat), str(cnf), str(proof), *map(str, extra), '-t', '120'],
                                 stdout=stream, stderr=subprocess.STDOUT, timeout=180)
    text = log.read_text()
    model.require(process.returncode == 0 and 's VERIFIED' in text, 'DRAT replay failure: '+str(log))
    match = re.search(r'(\d+) RAT lemmas in core', text)
    model.require(match is not None, 'missing RAT count')
    return int(match.group(1))


def check_partition(result):
    rows = result['cases']
    model.require(len(rows) == 24 and [r['index'] for r in rows] == list(range(24)), 'case partition')
    for row, case in zip(rows, model.cases()):
        model.require(all(row[k] == v for k, v in case.items()), 'case meaning changed')
        model.require(row['status'] in ('open', 'excluded'), 'unfinished or unexpected case')
    model.require(result['complete_bounded_sweep'] and not result['target_graph_found'], 'sweep incomplete')
    model.require(result['excluded_indices'] == [r['index'] for r in rows if r['status'] == 'excluded'], 'exclusion summary')
    model.require(result['open_indices'] == [r['index'] for r in rows if r['status'] == 'open'], 'open summary')
    return [r for r in rows if r['status'] == 'excluded']


def extract(sweep, output, drat, workers):
    result = json.loads((sweep / 'result.json').read_text())
    rows = check_partition(result)
    output.mkdir(parents=True, exist_ok=True)
    cert = output / 'certificates'
    cert.mkdir(exist_ok=True)

    def one(row):
        i = row['index']
        cnf, proof = sweep / f'case_{i:02}.cnf', sweep / f'case_{i:02}.drat'
        model.require(audit.check_formula(sweep / 'base.cnf', cnf, model.cases()[i]) == row['formula'], 'formula changed')
        model.require(model.file_info(proof) == row['proof'], 'proof changed')
        core, compact = cert / f'case_{i:02}.cnf', cert / f'case_{i:02}.drat'
        replay(drat, cnf, proof, output / f'extract_{i:02}.log', ('-c', core, '-l', compact))
        rat = replay(drat, core, compact, output / f'compact_{i:02}.log')
        answer = dict(model.cases()[i], core=model.file_info(core), proof=model.file_info(compact), rat_core_lemmas=rat)
        print(json.dumps({'index': i, 'compact_bytes': answer['core']['bytes']+answer['proof']['bytes'], 'rat': rat}), flush=True)
        return answer

    with ThreadPoolExecutor(workers) as pool:
        entries = list(pool.map(one, rows))
    report = {'format': 'r55-k10-phase-certificates-v1', 'sweep': result, 'cases': entries,
              'certificate_bytes': sum(r['core']['bytes']+r['proof']['bytes'] for r in entries)}
    atomic(output / 'manifest.json', report)
    return report


def read_core(path):
    lines = path.read_text().splitlines()
    model.require(bool(lines), 'empty core file')
    head = lines[0].split()
    model.require(len(head) == 4 and head[:3] == ['p', 'cnf', '28974'] and int(head[3]) == len(lines)-1, 'core header')
    result = []
    for line in lines[1:]:
        tokens = list(map(int, line.split()))
        model.require(tokens and tokens[-1] == 0 and all(1 <= abs(v) <= 28974 for v in tokens[:-1]), 'core literal')
        clause = tuple(sorted(tokens[:-1]))
        model.require(len(set(clause)) == len(clause) and not any(-v in clause for v in clause), 'invalid core clause')
        result.append(clause)
    return result


def membership(base, cert, rows):
    wanted = set()
    occurrences = 0
    for row in rows:
        i = row['index']
        case = model.cases()[i]
        model.require(all(row[k] == v for k, v in case.items()), 'wrong certificate case')
        core, proof = cert / f'case_{i:02}.cnf', cert / f'case_{i:02}.drat'
        model.require(model.file_info(core) == row['core'] and model.file_info(proof) == row['proof'], 'certificate hash')
        allowed, _ = audit.semantic_tail(case)
        allowed = set(allowed)
        clauses = read_core(core)
        occurrences += len(clauses)
        wanted.update(c for c in clauses if c not in allowed)
    obligations = len(wanted)
    with base.open('rb') as stream:
        model.require(stream.readline() == model.BASE_HEADER, 'parent membership header')
        for line in stream:
            tokens = tuple(map(int, line.split()))
            model.require(tokens[-1] == 0, 'parent terminator')
            wanted.discard(tokens[:-1])
    model.require(not wanted, 'core clause outside its own formula')
    return {'core_clause_occurrences': occurrences, 'distinct_parent_obligations': obligations}


def verify(work, cert, manifest_path, drat):
    start = time.monotonic()
    manifest = json.loads(manifest_path.read_text())
    excluded = check_partition(manifest['sweep'])
    model.require([r['index'] for r in manifest['cases']] == [r['index'] for r in excluded], 'certificate coverage')
    audit.audit()
    work.mkdir(parents=True, exist_ok=True)
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(model.PARENT / 'generate.py'), '--red-cycles', '4', '--output', str(base)], check=True)
    model.require(model.file_info(base)['sha256'] == model.BASE_SHA, 'base hash')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(model.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    support = membership(base, cert, manifest['cases'])
    verified = []
    for row in manifest['cases']:
        i = row['index']
        rat = replay(drat, cert / f'case_{i:02}.cnf', cert / f'case_{i:02}.drat', work / f'replay_{i:02}.log')
        model.require(rat == row['rat_core_lemmas'], 'RAT statistics mismatch')
        verified.append(i)
    by_phase = []
    for orbit in model.classes():
        group = [r for r in model.cases() if r['phase'] == orbit['phase']]
        opened = [r for r in group if r['index'] not in verified]
        by_phase.append({'phase': orbit['phase'], 'class_size': len(orbit['members']),
                         'excluded': not opened, 'open_anchors': [r['anchor'] for r in opened]})
    report = {'verified_indices': verified, 'open_indices': manifest['sweep']['open_indices'],
              'membership': support, 'phase_classes': by_phase,
              'all_ten_cycle_cases_excluded': len(verified) == 24,
              'target_graph_found': False, 'elapsed_seconds': round(time.monotonic()-start, 6),
              'existing_certificates_require_solver': False}
    atomic(work / 'verification.json', report)
    print(json.dumps(report, sort_keys=True))
    return report


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    e = sub.add_parser('extract')
    e.add_argument('--sweep', required=True, type=Path)
    e.add_argument('--output', required=True, type=Path)
    e.add_argument('--workers', type=int, default=2)
    v = sub.add_parser('verify')
    v.add_argument('--work', required=True, type=Path)
    v.add_argument('--certificates', required=True, type=Path)
    v.add_argument('--manifest', required=True, type=Path)
    for p in (e, v):
        p.add_argument('--drat-trim', required=True, type=Path)
    args = parser.parse_args()
    output = args.output if args.command == 'extract' else args.work
    model.require(not output.resolve().is_relative_to(model.ROOT.parent), 'generated certificates outside Git')
    if args.command == 'extract':
        model.require(1 <= args.workers <= 4, 'worker bounds')
        extract(args.sweep.resolve(), output.resolve(), args.drat_trim.resolve(), args.workers)
    else:
        verify(output.resolve(), args.certificates.resolve(), args.manifest.resolve(), args.drat_trim.resolve())


if __name__ == '__main__':
    main()
