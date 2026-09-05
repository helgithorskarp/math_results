#!/usr/bin/env python3
"""Reconstruct the parent, verify extracted core membership, and replay proofs."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import subprocess
import sys
import time

import audit
from sweep import atomic_json, file_info


def read_core(path):
    lines = path.read_text().splitlines()
    header = lines[0].split()
    audit.require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'invalid core header')
    variables, count = map(int, header[2:])
    audit.require(variables == 28950 and count == len(lines) - 1, 'wrong core dimensions')
    clauses = []
    for line in lines[1:]:
        tokens = list(map(int, line.split()))
        audit.require(tokens and tokens[-1] == 0 and all(1 <= abs(x) <= variables for x in tokens[:-1]), 'invalid core literal')
        clause = tuple(sorted(set(tokens[:-1])))
        audit.require(len(clause) == len(tokens) - 1 and not any(-x in clause for x in clause), 'noncanonical logical core clause')
        clauses.append(clause)
    return clauses


def membership(base, certificates, rows):
    ids = audit.orbit_edge_ids()
    wanted = set()
    core_count = 0
    for row in rows:
        index = row['index']
        core = certificates / f'case_{index:02}.cnf'
        proof = certificates / f'case_{index:02}.drat'
        audit.require(file_info(core) == row['core'] and file_info(proof) == row['proof'], 'compact certificate hash mismatch')
        weights = audit.load_weights()[index]
        audit.require(row['weights'] == weights, 'wrong case weights')
        units = {(ids[0, 3 * j + t] * (1 if t < weights[j - 1] else -1),)
                 for j in range(1, 10) for t in range(3)}
        clauses = read_core(core)
        core_count += len(clauses)
        wanted.update(clause for clause in clauses if clause not in units)
    obligations = len(wanted)
    with base.open('rb') as stream:
        audit.require(stream.readline() == audit.BASE_HEADER, 'wrong full parent header')
        for raw in stream:
            literals = tuple(map(int, raw.split()))
            audit.require(literals[-1] == 0, 'bad parent clause')
            wanted.discard(literals[:-1])
    audit.require(not wanted, 'compact core contains a clause outside its parent-plus-cube formula')
    return {'core_clauses_with_multiplicity': core_count, 'distinct_nonunit_parent_obligations': obligations}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--certificates', type=Path, required=True, help='extracted certificates outside Git')
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    work, drat = args.work.resolve(), args.drat_trim.resolve()
    audit.require(not work.is_relative_to(audit.ROOT.parent), 'work directory must be outside Git')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    result = json.loads((audit.ROOT / 'result.json').read_text())
    audited = audit.audit()
    audit.require(audited == result['audit'], 'coverage audit mismatch')
    excluded = result['excluded_indices']
    open_ids = result['open_indices']
    audit.require(sorted(excluded + open_ids) == list(range(98)), 'case list does not partition all 98 cubes')
    audit.require([row['index'] for row in result['cases']] == excluded, 'certificate list mismatch')
    audit.require(result['all_98_cubes_excluded'] == (len(excluded) == 98), 'incorrect whole-stratum claim')
    survivors = [audit.load_weights()[i] for i in open_ids]
    normal_form = [[1, 2, 2] + [1] * p + [2] * (6 - p) for p in range(4, 0, -1)]
    audit.require(survivors == normal_form and len(excluded) == 94, 'minority matching interpretation mismatch')
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(audit.PARENT / 'generate.py'), '--red-cycles', '4', '--output', str(base)], check=True)
    audit.require(file_info(base) == result['base'] and file_info(base)['sha256'] == audit.BASE_SHA256, 'wrong parent bytes')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(audit.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    certificates = args.certificates.resolve()
    support = membership(base, certificates, result['cases'])
    verified = []
    for row in result['cases']:
        index = row['index']
        core = certificates / f'case_{index:02}.cnf'
        proof = certificates / f'case_{index:02}.drat'
        log_path = work / f'case_{index:02}.replay.log'
        with log_path.open('w') as log:
            process = subprocess.run([str(drat), str(core), str(proof), '-t', '120'],
                                     stdout=log, stderr=subprocess.STDOUT, timeout=180)
        audit.require(process.returncode == 0 and 's VERIFIED' in log_path.read_text(), 'proof replay failed: ' + str(index))
        verified.append(index)
    report = {'verified_indices': verified, 'open_indices': open_ids, 'membership': support,
              'all_98_cubes_excluded': len(verified) == 98, 'target_graph_found': False,
              'minority_matching_forced': True, 'mixed_weight_one_counts': [1, 2, 3, 4],
              'elapsed_seconds': round(time.monotonic() - start, 6),
              'solver_required_for_existing_certificate_replay': False,
              'solver_required_for_certificate_regeneration': True}
    atomic_json(work / 'verification.json', report)
    print('PASS ' + json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
