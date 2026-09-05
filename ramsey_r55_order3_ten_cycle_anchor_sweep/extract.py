#!/usr/bin/env python3
"""Extract used clause cores and DRAT subproofs, then verify each new pair."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import re
import subprocess

import audit
from sweep import atomic_json, file_info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sweep', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    work, output, drat = args.sweep.resolve(), args.output.resolve(), args.drat_trim.resolve()
    audit.require(not output.is_relative_to(audit.ROOT.parent), 'extract outside Git before reviewing certificate sizes')
    audit.require(1 <= args.workers <= 4, 'invalid worker count')
    report = json.loads((work / 'sweep.json').read_text())
    audit.require(report['complete_bounded_sweep'] and not report['target_graph_found'], 'sweep not complete')
    output.mkdir(parents=True, exist_ok=True)
    certificates = output / 'certificates'
    certificates.mkdir(exist_ok=True)
    audit.require_parent()

    def one(row):
        index = row['index']
        source_cnf = work / f'cube_{index:02}.cnf'
        source_drat = work / f'cube_{index:02}.drat'
        audit.require(audit.check_cube(work / 'base.cnf', source_cnf, index) == row['formula'], 'cube changed')
        audit.require(file_info(source_drat) == row['proof'], 'source proof changed')
        core = certificates / f'case_{index:02}.cnf'
        proof = certificates / f'case_{index:02}.drat'
        extract_log = output / f'extract_{index:02}.log'
        with extract_log.open('w') as log:
            process = subprocess.run([str(drat), str(source_cnf), str(source_drat), '-c', str(core),
                                      '-l', str(proof), '-t', '120'], stdout=log, stderr=subprocess.STDOUT, timeout=180)
        audit.require(process.returncode == 0 and 's VERIFIED' in extract_log.read_text(), 'extraction replay failed')
        check_log = output / f'compact_{index:02}.log'
        with check_log.open('w') as log:
            process = subprocess.run([str(drat), str(core), str(proof), '-t', '120'],
                                     stdout=log, stderr=subprocess.STDOUT, timeout=180)
        text = check_log.read_text()
        audit.require(process.returncode == 0 and 's VERIFIED' in text, 'compact proof failed')
        match = re.search(r'(\d+) RAT lemmas in core', text)
        audit.require(match is not None, 'missing compact RAT count')
        result = {'index': index, 'weights': row['weights'], 'full_formula': row['formula'],
                  'full_proof': row['proof'], 'core': file_info(core), 'proof': file_info(proof),
                  'compact_rat_core_lemmas': int(match.group(1)), 'status': 'excluded'}
        print(json.dumps({'index': index, 'compact_bytes': result['core']['bytes'] + result['proof']['bytes'],
                          'rat_core_lemmas': result['compact_rat_core_lemmas']}, sort_keys=True), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(one, [row for row in report['cases'] if row['status'] == 'excluded']))
    result = {'format': 'r55-order3-k10-anchor-certificates-v1', 'cycle_type': '1^13 3^10', 'red_cycles': 4,
              'parent_source_commit': json.loads((audit.ROOT / 'parent_manifest.json').read_text())['source_commit'],
              'audit': audit.audit(), 'base': report['contract']['base'], 'cases': rows,
              'excluded_indices': report['excluded_indices'], 'open_indices': report['open_indices'],
              'all_98_cubes_excluded': report['all_98_cubes_excluded'], 'target_graph_found': False,
              'tools': {key: report['contract'][key] for key in ('kissat', 'drat_trim', 'python')},
              'sweep': {key: report[key] for key in ('elapsed_seconds', 'largest_child_maxrss_kib')},
              'limits': {key: report['contract'][key] for key in ('workers', 'solver_seconds_per_cube', 'replay_seconds_per_cube')},
              'compact_certificate_bytes': sum(row['core']['bytes'] + row['proof']['bytes'] for row in rows)}
    atomic_json(output / 'result.json', result)
    print('EXTRACTION_COMPLETE ' + str(result['compact_certificate_bytes']), flush=True)


if __name__ == '__main__':
    main()
