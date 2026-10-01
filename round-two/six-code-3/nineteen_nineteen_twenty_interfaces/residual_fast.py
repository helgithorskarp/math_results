"""Solver-free proper-color certificates for the full92-orientation census.

This stage needs every completed joint orientation. Each graph is built
both by masks and by literal triples. It makes only the numerical bound
that the checked color capacities actually support.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from residual_geometry import literal_graph, residual
from bindings import HERE, v
from collect_fast import load
from verify_colors import check_record


def run(census_work, work, executables, first, count):
    begun = time.monotonic()
    cores, manifest = load(census_work, executables)
    v.check(manifest['status'] == 'COMPLETE_ALL92_JOINT_CENSUS', 'incomplete residual full domain')
    mathematical = {k: value for k, value in manifest.items() if k != 'binding'}
    domain_hash = v.sha(mathematical)
    v.check(type(first) is int and 0 <= first < len(cores) and type(count) is int and
            0 < count <= 100, 'bounded full residual batch')
    finish = min(first + count, len(cores))
    work.mkdir(parents=True, exist_ok=True)
    record_path = work / 'mathematical-census.json'
    if record_path.exists():
        v.compare(json.loads(record_path.read_text()), mathematical, 'full residual domain changed')
    else:
        record_path.write_bytes(v.encode(mathematical))
    records = []
    for index in range(first, finish):
        if time.monotonic() - begun > 60:
            raise RuntimeError('INCOMPLETE residual batch guard; no exclusion')
        core = cores[index]
        words, literal, adjacent = literal_graph(core)
        candidates, mask_graph = residual.graph(core)
        v.compare([word for word, mask in candidates], literal, 'full residual candidate mask/literal mismatch')
        v.check(mask_graph == adjacent, 'full residual mask/triple adjacency mismatch')
        colors = residual.color(mask_graph)
        v.check(len(colors) == len(literal) and all(type(c) is int and c >= 0 for c in colors),
                'full residual color domain/coverage')
        v.check(not any(colors[i] == colors[j] for i, row in enumerate(adjacent) for j in row),
                'full residual improper literal coloring')
        record = {'status': 'COMPLETE_EXACT_PROPER_COLOR', 'index': index,
                  'domain_sha256': domain_hash, 'core_sha256': core['core_sha256'],
                  'candidate_sha256': v.sha(literal), 'candidate_count': len(literal),
                  'colors': colors, 'capacity': max(colors, default=-1) + 1}
        (work / f'color-{index}.json').write_bytes(v.encode(record))
        records.append(record)
    result = {'status': 'COMPLETE_FULL_DOMAIN_COLOR_BATCH_ONLY', 'first': first, 'finish': finish,
              'domain_sha256': domain_hash, 'total_cores': len(cores),
              'capacity_census': dict(sorted(Counter(row['capacity'] for row in records).items())),
              'candidate_range': [min(row['candidate_count'] for row in records),
                                  max(row['candidate_count'] for row in records)],
              'seconds': time.monotonic() - begun}
    (work / f'batch-{first}-{finish}.json').write_bytes(v.encode(result))
    (work / 'progress.json').write_bytes(v.encode(result))
    print(json.dumps(result), flush=True)
    return result


def collect(census_work, work, executables):
    cores, manifest = load(census_work, executables)
    mathematical = {k: value for k, value in manifest.items() if k != 'binding'}
    domain_hash = v.sha(mathematical)
    records = []
    for index, core in enumerate(cores):
        path = work / f'color-{index}.json'
        v.check(path.exists(), 'missing residual graph; no numerical bound')
        row = json.loads(path.read_text())
        v.check(row['status'] == 'COMPLETE_EXACT_PROPER_COLOR' and type(row['index']) is int
                and row['index'] == index and row['domain_sha256'] == domain_hash and
                row['core_sha256'] == core['core_sha256'], 'residual complete record/domain binding')
        v.check(len(row['colors']) == row['candidate_count'] and
                all(type(c) is int and c >= 0 for c in row['colors']) and
                row['capacity'] == max(row['colors'], default=-1) + 1,
                'residual complete color coverage/domain')
        check_record(core, row, index, domain_hash)
        records.append(row)
    certificate = {'status': 'COMPLETE_ALL_CORE_PROPER_COLOR_RECORDS', 'domain_sha256': domain_hash,
                   'core_count': len(cores), 'records': records}
    (work / 'all-color-certificates.json').write_bytes(v.encode(certificate))
    result = {'status': 'COMPLETE_ALL92_AND_ALL_RESIDUAL_PROPER_COLORS', 'core_count': len(cores),
              'orientation_count': 92, 'domain_sha256': domain_hash,
              'certificate_sha256': v.sha(certificate),
              'capacity_census': dict(sorted(Counter(row['capacity'] for row in records).items())),
              'candidate_range': [min(row['candidate_count'] for row in records),
                                  max(row['candidate_count'] for row in records)],
              'maximum_capacity': max(row['capacity'] for row in records),
              'certified_total_upper_bound': 44 + max(row['capacity'] for row in records),
              'scope': 'Uncovered19/19/20, pair5/5/4, first19 opposite4; all marked inputs and both orientations.'}
    (work / 'complete-color-summary.json').write_bytes(v.encode(result))
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--census-work', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--include-executable', type=Path, required=True)
    parser.add_argument('--color-executable', type=Path, required=True)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--collect', action='store_true')
    args = parser.parse_args()
    executables = [args.include_executable, args.color_executable]
    if args.collect:
        collect(args.census_work, args.work, executables)
    else:
        run(args.census_work, args.work, executables, args.first, args.count)
