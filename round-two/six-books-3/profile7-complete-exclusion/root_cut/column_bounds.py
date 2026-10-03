"""Exact subset-score necessary column bounds, with literal separating witnesses."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(records, out):
    started = time.monotonic()
    work = 0

    def tick():
        nonlocal work
        if work >= 2000000 or time.monotonic() - started >= 40:
            raise ValueError('Operational column-score guard; incomplete domain')
        work += 1

    columns = (5,4,5,5,4,5,5,5,5)
    targets = [sum(columns[j] for j in range(9) if mask & (1 << j))
               for mask in range(512)]
    score_cache = {}

    def scores(domain):
        key = tuple(domain)
        if key in score_cache:
            return score_cache[key]
        require(domain, 'Subset score of an empty row domain')
        lower = [0]*512
        upper = [0]*512
        for mask in range(1,512):
            tick()
            values = [(word & mask).bit_count() for word in domain]
            lower[mask], upper[mask] = min(values), max(values)
        result = lower, upper
        score_cache[key] = result
        return result

    original_sha = hashlib.sha256()
    certificate_sha = hashlib.sha256()
    viable = eliminated = remaining = tested_masks = 0
    failures = collections.Counter()
    original_count = 0
    original_bytes = certificate_bytes = 0
    survivors = []
    with Path(records).open('rb') as source, Path(out).open('wb') as certificate:
        for index, line in enumerate(source):
            tick()
            original_sha.update(line)
            original_bytes += len(line)
            graph, domains = json.loads(line)
            original_count += 1
            if any(not domain for domain in domains):
                continue
            viable += 1
            tables = [scores(domain) for domain in domains]
            witness = None
            for mask in range(1,512):
                tick()
                tested_masks += 1
                minimum = sum(lower[mask] for lower, upper in tables)
                maximum = sum(upper[mask] for lower, upper in tables)
                target = targets[mask]
                if minimum > target:
                    witness = ['lower', mask, minimum, target]
                    failures['lower'] += 1
                    break
                if maximum < target:
                    witness = ['upper', mask, maximum, target]
                    failures['upper'] += 1
                    break
            if witness is None:
                remaining += 1
                survivors.append(index)
            else:
                eliminated += 1
            encoded = json.dumps([index,witness], separators=(',',':')).encode() + b'\n'
            certificate.write(encoded)
            certificate_sha.update(encoded)
            certificate_bytes += len(encoded)
    require(original_count == 50400 and viable == 2908,
            'Wrong complete original row domain')
    require(original_sha.hexdigest() == '8ac8cfc8cd19e3123a9c85f1e87c94af8846ea06d2418d853e67b206353a8e7b',
            'Different original row domains')
    return dict(agent='six-books-3', role='researcher',
        status='COMPLETE_SUBSET_SCORE_NECESSARY_COLUMN_BOUND_FILTER',
        original_graphs=original_count, original_rows_bytes=original_bytes,
        original_rows_sha256=original_sha.hexdigest(), column_degrees=list(columns),
        original_nonempty_row_graphs=viable, column_bound_excluded_graphs=eliminated,
        graphs_surviving_all511_subset_bounds=remaining, survivor_graph_indices=survivors,
        actual_failures=dict(failures), tested_subset_bounds=tested_masks,
        distinct_row_score_tables=len(score_cache),
        certificate_bytes=certificate_bytes, certificate_sha256=certificate_sha.hexdigest(),
        work_units=work, work_guard=2000000, internal_seconds_guard=40,
        simultaneous_matrix_existence_claimed=False, page_compatibility_checked=False,
        B_high_completion_checked=False, whole_profile_excluded=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--records', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.records, args.out), sort_keys=True, separators=(',',':')))
