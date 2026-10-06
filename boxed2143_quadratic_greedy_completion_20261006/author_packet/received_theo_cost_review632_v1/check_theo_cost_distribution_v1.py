"""Independent entire finite check of Theo608's new conditional-cost scope.

Every insertion gap is tested by FULL literal occurrence sets, with caching
of immutable words. No author executable, nearest-greater implementation or
third-point-only oracle is imported. Full 147 traces and final words retained.
"""

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(None)
def legal_gaps(word):
    result = []
    for gap in range(len(word) + 1):
        child = word[:gap] + (len(word) + 1,) + word[gap:]
        if not tuple(occurrences(child)):
            result.append(gap)
    return tuple(result)


def complete(source):
    source_position = {value: i for i, value in enumerate(source)}
    word, identities = (), []
    costs, auxiliary_trace = [], []
    stream = hashlib.sha256()
    for rank in range(1, len(source) + 1):
        before_next_original = [i for i, identity in enumerate(identities)
                                if identity is not None and
                                source_position[identity] > source_position[rank]]
        desired = min(before_next_original) if before_next_original else len(word)
        repairs = 0
        while True:
            legal = legal_gaps(word)
            if desired in legal:
                gap = desired
                identity = rank
                auxiliary = False
            else:
                gap = max(g for g in legal if g < desired)
                identity = None
                auxiliary = True
                distance_before = desired - gap
            word = word[:gap] + (len(word) + 1,) + word[gap:]
            identities.insert(gap, identity)
            require(not tuple(occurrences(word)), 'Actual child contains a literal box')
            if auxiliary:
                desired += 1
                repairs += 1
                after = legal_gaps(word)
                distance_after = desired - max(g for g in after if g <= desired)
                if len(source) <= 8:
                    auxiliary_trace.append({'source_rank': rank, 'auxiliary_gap': gap,
                                            'tracked_gap': desired, 'distance_before': distance_before,
                                            'distance_after': distance_after})
            stream.update((json.dumps([word, identities], separators=(',', ':')) + '\n').encode())
            if not auxiliary:
                costs.append(repairs)
                break
    require(tuple(identity for identity in identities if identity is not None) == source,
            'Original identity order is lost')
    kept = tuple(value for value, identity in zip(word, identities) if identity is not None)
    rank = {value: i + 1 for i, value in enumerate(sorted(kept))}
    require(tuple(rank[value] for value in kept) == source, 'Original relative values are lost')
    result = {'input': source, 'output_length': len(word), 'auxiliaries': len(word) - len(source),
              'stage_costs': costs, 'trace_sha256': stream.hexdigest()}
    if len(source) <= 8:
        result.update({'output': word, 'source_identities': identities, 'auxiliary_trace': auxiliary_trace})
    return result, {'source': source, 'final_word': word, 'source_identities': identities,
                    'complete_final_occurrences': tuple(occurrences(word)), 'trace_result': result}


def run():
    began = time.monotonic()
    base = Path(__file__).parent
    root = base / 'received/theo_cost_distribution_v1'
    raw = (root / 'MANIFEST.json').read_bytes()
    for rec in json.loads(raw)['files']:
        data = (root / rec['path']).read_bytes()
        require(len(data) == rec['bytes'] and hashlib.sha256(data).hexdigest() == rec['sha256'],
                'Frozen author file differs: ' + rec['path'])
    author = json.loads((root / 'cost-distribution-objection-controls-v1.json').read_text())
    rows, records = [], []
    digest = hashlib.sha256()
    cases = 0
    for n in range(3, 17):
        parent = tuple(range(n - 1, 0, -1)) + (n,)
        costs = []
        require(not tuple(occurrences(parent)), 'Named parent does not avoid')
        for gap in range(n + 1):
            source = parent[:gap] + (n + 1,) + parent[gap:]
            result, certificate = complete(source)
            expected = gap - 1 if 2 <= gap < n else 0
            require(result['stage_costs'][:-1] == [0] * n and result['stage_costs'][-1] == expected,
                    'Reachable family or next-rank cost differs')
            require(result['output_length'] == n + 1 + expected, 'Exact output length differs')
            costs.append(expected)
            records.append(certificate)
            digest.update((json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n').encode())
            cases += 1
        require(sum(costs) == (n - 2) * (n - 1) // 2, 'Exact row sum differs')
        rows.append({'n': n, 'parent': parent, 'gap_costs': costs, 'sum_cost': sum(costs),
                     'conditional_mean_exact_numerator_denominator': [sum(costs), n + 1]})
    normalized = json.loads(json.dumps(rows))
    require(normalized == author['rows'] and cases == author['case_count'] == 147,
            'Some complete finite table field differs')
    require(digest.hexdigest() == author['ordered_complete_trace_stream_sha256'],
            'Full ordered trace stream differs')
    return {'author': 'literature-researcher-4', 'checker': 'literature-researcher-2',
            'source_message_id': 608, 'decision_message_id': 410, 'full_target_solved': False,
            'transport_manifest_sha256': hashlib.sha256(raw).hexdigest(),
            'independence': __doc__, 'case_count': cases, 'all_complete_deterministic_fields_match': True,
            'ordered_complete_trace_stream_sha256': digest.hexdigest(), 'rows': rows,
            'complete_final_certificates': records, 'cached_full_insertion_parent_words': legal_gaps.cache_info().currsize,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'literal_checker_sha256': hashlib.sha256((base / 'definition_checker.py').read_bytes()).hexdigest(),
            'python': platform.python_version(), 'elapsed_seconds': time.monotonic() - began,
            'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'Preserve prior check output')
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('rows', 'complete_final_certificates')}, indent=2))
