"""Complete necessary root0 attachment rows; no simultaneous completion claim."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import time

import neighborhoods

COUNTS = (0,1,2,1,2,2,1,1,2,2,1,2,1,0,0)
COLUMNS = (0,1,4,1,0,16,0,0,0,1,0,64,0,0,0,0,0,0)
EXPECTED_NEIGHBORHOODS = '57f2a5e464354eb427d1818589988a038335a42ed05709b8f3118d4dd785f4f8'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(out):
    started = time.monotonic()
    baseline, graphs, classes = neighborhoods.run(return_inventory=True)
    require(baseline['complete_labelled_graphs'] == 50400
            and baseline['whole_inventory_sha256'] == EXPECTED_NEIGHBORHOODS,
            'The complete original neighborhood baseline changed')
    work = baseline['work_units']

    def tick():
        nonlocal work
        if work >= 2000000 or time.monotonic() - started >= 40:
            raise ValueError('Operational attachment-row guard; incomplete domain')
        work += 1

    types = tuple(t for t, count in enumerate(COUNTS, 1) for _ in range(count))
    require(len(types) == 18 and len(COLUMNS) == 18, 'Wrong high population')
    marked = [x for x, t in enumerate(types) if t & 1 and COLUMNS[x] & 3]
    require(marked == [1], 'Wrong unique degree2 point')
    A = tuple(x for x, t in enumerate(types) if t & 1 and x != marked[0]) + tuple(marked)
    B = tuple(x for x, t in enumerate(types) if not t & 1)
    require(len(A) == len(B) == 9 and [COLUMNS[x] & 3 for x in A] == [0]*8+[1],
            'Wrong root0 tagged-neighborhood ordering')
    a_slices = tuple(sum(1 << i for i, x in enumerate(A) if types[x] & (1 << j))
                     for j in (1,2,3))
    b_slices = tuple(sum(1 << i for i, x in enumerate(B) if types[x] & (1 << j))
                     for j in (1,2,3))
    by_signature = collections.defaultdict(list)
    for word in range(512):
        tick()
        key = (word.bit_count(),) + tuple((word & s).bit_count() for s in b_slices)
        by_signature[key].append(word)
    require(sum(map(len, by_signature.values())) == 512, 'Incomplete physical row domain')
    sha = hashlib.sha256()
    total_bytes = 0
    viable = collections.Counter()
    excluded = collections.Counter()
    empty_vertices = collections.Counter()
    row_sizes = collections.Counter()
    samples = []
    signature_count = set()
    total_rows = 0
    with Path(out).open('wb') as handle:
        for graph in graphs:
            domains = []
            for i, x in enumerate(A):
                tick()
                cardinality = 10 - types[x].bit_count() - graph[i].bit_count()
                targets = tuple((3 if types[x] & (1 << j) else 5)
                    - ((COLUMNS[x] >> (2*j)) & 3)
                    - (graph[i] & a_slices[j-1]).bit_count() for j in (1,2,3))
                key = (cardinality,) + targets
                signature_count.add(key)
                domain = by_signature.get(key, [])
                domains.append(domain)
                row_sizes[len(domain)] += 1
                total_rows += len(domain)
            first = next((i for i, domain in enumerate(domains) if not domain), None)
            if first is None:
                viable[classes[graph]] += 1
                if len(samples) < 3:
                    samples.append([list(graph), domains])
            else:
                excluded[classes[graph]] += 1
                empty_vertices[first] += 1
            encoded = json.dumps([graph, domains], separators=(',',':')).encode() + b'\n'
            handle.write(encoded)
            sha.update(encoded)
            total_bytes += len(encoded)
    return dict(agent='six-books-3', role='researcher',
        status='COMPLETE_EXACT_NECESSARY_ROOT0_ROW_DOMAINS',
        counts=list(COUNTS), columns=list(COLUMNS), A_high_labels=list(A), B_high_labels=list(B),
        A_tags=[[types[x], COLUMNS[x]] for x in A],
        B_tags=[[types[x], COLUMNS[x]] for x in B],
        A_slice_masks=list(a_slices), B_slice_masks=list(b_slices),
        complete_local_baseline=baseline, original_graphs=len(graphs),
        viable_graphs=sum(viable.values()), empty_row_excluded_graphs=sum(excluded.values()),
        viable_by_shape=dict(viable), empty_row_excluded_by_shape=dict(excluded),
        first_empty_row_counts=dict(empty_vertices),
        exact_row_domain_size_counts=dict(row_sizes), complete_physical_rows=total_rows,
        distinct_requested_signatures=len(signature_count),
        whole_records_bytes=total_bytes, whole_records_sha256=sha.hexdigest(),
        first_viable_records=samples, work_units=work, work_guard=2000000,
        internal_seconds_guard=40, ordinary_host_bridge_formalized=False,
        simultaneous_column_constraints_checked=False, B_high_graphs_completed=False,
        host_realization_claimed=False, whole_profile_excluded=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.out), sort_keys=True, separators=(',',':')))
