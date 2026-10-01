"""Complete special-circle cohort replay with explicit seven-clique targets.

Exact standard-library Python. Both record streams and every projection row
are compared. Guards/incomplete coverage never establish an exclusion.
Compact generated checkpoints are optional local state, not publication.
"""
from collections import Counter
from pathlib import Path
import argparse
import json
import resource
import time
from common import (ROOT, atomic_json, classical_design, digest, require,
                    source_fingerprint, enumerate_fixed_words, enumerate_sets,
                    project, pair_projection, find_clique, clique_census)
from normalize import normalize
from fixtures import check_fixture
from imports import check_imports


def run_case(circles, case):
    start = time.monotonic()
    records, first = enumerate_fixed_words(circles, case['gaps'], (15,))
    separate, second = enumerate_sets(circles, case['gaps'], (15,))
    require(records == separate, 'record lists differ entrywise')
    require(first['records'] == second['records'] == len(records)
            and first['records_sha256'] == second['records_sha256'], 'record summaries differ')
    adjacency, words, projected = project(records)
    rows, separate_words, separate_projection = pair_projection(separate)
    require(adjacency == rows and words == separate_words, 'projected words or rows differ entrywise')
    # The finder and increasing census now both use seven directly.
    witness, search = find_clique(adjacency, 7)
    require(search['complete'], 'INCOMPLETE: seven-clique decision')
    require(witness is None, 'positive seven-clique; special-cohort exclusion fails')
    census = clique_census(rows, 7)
    counts = census['cliques_by_size']
    require(counts['7'] == 0 and counts['1'] == len(words)
            and counts['2'] == projected['edges'], 'projected census mismatch')
    manifest = {'case': case['case'], 'orbit_size': case['orbit_size'],
                'gaps': case['gaps'], 'fixed_noncontained_words': [15],
                'records': len(records), 'records_sha256': first['records_sha256'],
                'projected_vertices': len(words), 'projected_edges': projected['edges'],
                'projected_graph_sha256': projected['graph_sha256'],
                'cliques_by_size': counts, 'K7_excluded': True}
    return {'complete': True, 'manifest': manifest,
            'manifest_sha256': digest(manifest), 'primary_target': search['target'],
            'separate_forbidden_clique': census['forbidden_clique'],
            'all_records_entrywise': True, 'all_projection_rows_entrywise': True,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def authenticate(case, result, fingerprint, normalization_digest):
    require(result.get('complete') is True
            and result.get('source_fingerprint') == fingerprint
            and result.get('normalization_sha256') == normalization_digest,
            'checkpoint is incomplete or belongs to different source/normalization')
    manifest = result['manifest']
    require(manifest['case'] == case['case'] and manifest['gaps'] == case['gaps']
            and manifest['orbit_size'] == case['orbit_size']
            and manifest['fixed_noncontained_words'] == [15], 'checkpoint inputs differ')
    require(result['manifest_sha256'] == digest(manifest)
            and manifest['K7_excluded'] and manifest['cliques_by_size']['7'] == 0
            and result['primary_target'] == result['separate_forbidden_clique'] == 7
            and result['all_records_entrywise'] and result['all_projection_rows_entrywise'],
            'checkpoint seven-target exclusion is not authenticated')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checks-dir', type=Path, required=True,
                        help='local generated state; keep outside the publication directory')
    parser.add_argument('--from-case', type=int, default=0)
    parser.add_argument('--to-case', type=int)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--normalization-only', action='store_true')
    args = parser.parse_args()
    expected = json.loads((ROOT / 'expected.json').read_text())
    require(expected['schema_version'] == 1, 'unexpected expected schema')
    fingerprint = source_fingerprint()
    circles, _ = classical_design()
    cases, normalization, stabilizer = normalize(circles)
    require(normalization == expected['normalization'], 'normalization differs from expected')
    norm_digest = digest(normalization)
    imported = check_imports(circles, normalization, stabilizer)
    require(imported == expected['imports'], 'imported coverage differs from expected')
    fixtures = json.loads((ROOT / 'fixtures.json').read_text())
    checked_fixtures = [check_fixture(circles, f) for f in fixtures]
    require(checked_fixtures == expected['fixtures'], 'literal fixture summaries differ')
    print(json.dumps({'agent': 'six-code-2', 'role': 'researcher',
                      'normalization': normalization, 'imports': imported,
                      'fixtures_checked': len(checked_fixtures),
                      'source_fingerprint': fingerprint}), flush=True)
    if args.normalization_only:
        require(source_fingerprint() == fingerprint, 'source changed during normalization')
        atomic_json(args.checks_dir / 'normalization-summary.json',
                    {'complete': True, 'scope': 'normalization/import/fixture checks only',
                     'normalization': normalization, 'imports': imported,
                     'fixtures': checked_fixtures, 'source_fingerprint': fingerprint})
        return 0
    end = len(cases) if args.to_case is None else args.to_case
    require(0 <= args.from_case <= end <= len(cases), 'invalid case interval')
    results, incomplete = [], None
    for case in cases[args.from_case:end]:
        path = args.checks_dir / f"{case['case']}.json"
        if args.resume and path.exists():
            result = json.loads(path.read_text())
            authenticate(case, result, fingerprint, norm_digest)
        else:
            try:
                result = run_case(circles, case)
            except ValueError as error:
                if 'INCOMPLETE' not in str(error):
                    raise
                incomplete = {'complete': False, 'case': case['case'], 'gaps': case['gaps'],
                              'limit': str(error), 'mathematical_exclusion': None}
                atomic_json(args.checks_dir / 'incomplete.json', incomplete)
                break
            result.update({'source_fingerprint': fingerprint,
                           'normalization_sha256': norm_digest})
            atomic_json(path, result)
        authenticate(case, result, fingerprint, norm_digest)
        results.append(result)
        if len(results) % 25 == 0 or case['case'] + 1 == end:
            print(json.dumps({'checked_cases': len(results), 'last_case': case['case'],
                              'seconds_sum': sum(r['seconds'] for r in results),
                              'max_RSS_KiB': result['max_RSS_KiB']}), flush=True)
    require(source_fingerprint() == fingerprint, 'source changed during replay')
    full = (args.from_case == 0 and end == len(cases) and incomplete is None
            and len(results) == len(cases))
    manifest = [r['manifest'] for r in results]
    clique_totals = Counter()
    numbers = Counter()
    for m in manifest:
        clique_totals.update(m['cliques_by_size'])
        numbers[str(max((int(k) for k, v in m['cliques_by_size'].items() if v), default=0))] += 1
    mathematical = {'complete_cases': len(results),
                    'labeled_triples': sum(m['orbit_size'] for m in manifest),
                    'records_entrywise': sum(m['records'] for m in manifest),
                    'projected_rows_entrywise': sum(m['projected_vertices'] for m in manifest),
                    'manifest_sha256': digest(manifest),
                    'cliques_by_size': dict(sorted(clique_totals.items())),
                    'clique_number_histogram': dict(sorted(numbers.items()))}
    if full:
        require(mathematical == expected['seven_gap'], 'whole-cohort mathematical summary differs')
    summary = {'agent': 'six-code-2', 'role': 'researcher', 'complete': incomplete is None,
               'whole_cohort_complete': full,
               'scope': 'all1763special-gapclasses' if full else 'specifiedintervalonly',
               'from_case': args.from_case, 'to_case': end,
               'mathematical': mathematical, 'source_fingerprint': fingerprint,
               'normalization_sha256': norm_digest, 'incomplete': incomplete,
               'seconds_sum': sum(r['seconds'] for r in results),
               'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    atomic_json(args.checks_dir / f'summary-{args.from_case}-{end}.json', summary)
    if full:
        atomic_json(args.checks_dir / 'summary.json', summary)
    print(json.dumps(summary), flush=True)
    return 2 if incomplete else 0


if __name__ == '__main__':
    raise SystemExit(main())
