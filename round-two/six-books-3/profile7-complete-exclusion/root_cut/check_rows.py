"""Distinct graph-orbit coverage and literal ordinary22-point spine row checker.

Imports no producer, neighborhood generator, model, or private case inventory.
All nine-bit physical candidates are tested through actual red/blue rows.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import time


TYPES = (2,3,3,4,5,5,6,6,7,8,9,9,10,10,11,12,12,13)
SIGMA = (0,1,4,1,0,16,0,0,0,1,0,64,0,0,0,0,0,0)
REPRESENTATIVES = (
    (276,296,73,134,97,146,148,104,3),
    (400,292,74,148,41,82,164,73,3),
    (386,37,74,148,296,82,164,73,17),
    (268,276,35,193,194,196,56,56,3),
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(path):
    started = time.monotonic()
    work = 0

    def tick():
        nonlocal work
        if work >= 2000000 or time.monotonic() - started >= 40:
            raise ValueError('Operational literal row guard; incomplete coverage')
        work += 1

    originals = set()
    class_sets = []
    for representative in REPRESENTATIVES:
        neighbors = [[j for j in range(9) if row & (1 << j)] for row in representative]
        images = set()
        for permutation in itertools.permutations(range(8)):
            tick()
            phi = permutation + (8,)
            record = [0]*9
            for i in range(9):
                record[phi[i]] = sum(1 << phi[j] for j in neighbors[i])
            images.add(tuple(record))
        require(not images & originals, 'Two asserted distinct shapes overlap')
        originals.update(images)
        class_sets.append(images)
    require(len(originals) == 50400, 'Incomplete marked graph orbit domain')
    original_encoded = json.dumps(sorted(originals), separators=(',',':')).encode()
    original_sha = hashlib.sha256(original_encoded).hexdigest()
    require(original_sha == '57f2a5e464354eb427d1818589988a038335a42ed05709b8f3118d4dd785f4f8',
            'Full literal graph domain differs from cubic/direct baseline')
    A = tuple(x for x in range(18) if TYPES[x] & 1 and x != 1) + (1,)
    B = tuple(x for x in range(18) if not TYPES[x] & 1)
    require(A == (2,4,5,8,10,11,14,17,1) and B == (0,3,6,7,9,12,13,15,16),
            'Wrong literal physical high labels')
    low_rows = tuple(sum(1 << (x+4) for x in range(18) if TYPES[x] & (1 << j))
                     for j in range(4))
    require([row.bit_count() for row in low_rows] == [9]*4, 'Wrong literal low degrees')
    full = (1 << 22)-1
    low_blue = tuple(full ^ (low_rows[j] | (1 << j)) for j in range(4))
    a_lift = tuple(sum(1 << (A[j]+4) for j in range(9) if word & (1 << j))
                   for word in range(512))
    b_lift = tuple(sum(1 << (B[j]+4) for j in range(9) if word & (1 << j))
                   for word in range(512))
    cache = {}

    def literal_domain(i, adjacency_row):
        key = i, adjacency_row
        if key in cache:
            return cache[key]
        x = A[i]
        point = x+4
        known = TYPES[x] | a_lift[adjacency_row]
        require(not known & (1 << point), 'Literal diagonal red edge')
        domain = []
        for word in range(512):
            tick()
            red = known | b_lift[word]
            if red.bit_count() != 10:
                continue
            blue = full ^ (red | (1 << point))
            valid = True
            for j in range(4):
                deficit = (SIGMA[x] >> (2*j)) & 3
                if red & (1 << j):
                    pages = (red & low_rows[j]).bit_count()
                    target = 3-deficit
                else:
                    pages = (blue & low_blue[j]).bit_count()
                    target = 6-deficit
                if pages != target:
                    valid = False
                    break
            if valid:
                domain.append(word)
        cache[key] = domain
        return domain

    seen = set()
    previous = None
    sha = hashlib.sha256()
    count = viable = physical_rows = total_bytes = 0
    sizes = collections.Counter()
    first_empty = collections.Counter()
    viable_classes = [0]*4
    with Path(path).open('rb') as handle:
        for line in handle:
            tick()
            sha.update(line)
            total_bytes += len(line)
            value = json.loads(line)
            require(isinstance(value, list) and len(value) == 2, 'Bad graph/domain record')
            a, domains = value
            require(isinstance(a, list) and len(a) == 9
                    and all(type(row) is int and 0 <= row < 512 for row in a),
                    'Bad actual adjacency rows')
            graph = tuple(a)
            require(graph in originals and graph not in seen
                    and (previous is None or previous < graph), 'Bad graph coverage/order')
            require(isinstance(domains, list) and len(domains) == 9, 'Bad cut-row domains')
            for i, domain in enumerate(domains):
                tick()
                require(isinstance(domain, list)
                        and all(type(word) is int and 0 <= word < 512 for word in domain),
                        'Bad literal nine-bit row word')
                expected = literal_domain(i, graph[i])
                require(domain == expected, 'Whole literal low-spine row domain differs')
                sizes[len(domain)] += 1
                physical_rows += len(domain)
            first = next((i for i, domain in enumerate(domains) if not domain), None)
            if first is None:
                viable += 1
                k = next(k for k, images in enumerate(class_sets) if graph in images)
                viable_classes[k] += 1
            else:
                first_empty[first] += 1
            seen.add(graph)
            previous = graph
            count += 1
    require(seen == originals, 'Omitted original marked neighborhood graph')
    return dict(agent='six-books-3', role='researcher',
        status='COMPLETE_LITERAL_ORDINARY_SPINE_ROW_CHECK', complete_graphs=count,
        original_graph_inventory_sha256=original_sha, orbit_assignments=161280,
        class_sizes=[len(images) for images in class_sets], viable_graphs=viable,
        viable_by_shape=viable_classes, empty_row_excluded_graphs=count-viable,
        whole_records_bytes=total_bytes, whole_records_sha256=sha.hexdigest(),
        exact_row_domain_size_counts=dict(sizes), first_empty_row_counts=dict(first_empty),
        complete_physical_rows=physical_rows, distinct_literal_point_neighbor_patterns=len(cache),
        all_physical_words_checked_per_pattern=512, four_original_low_spines_checked=True,
        imports_producer_or_generator=False, work_units=work, work_guard=2000000,
        internal_seconds_guard=40, simultaneous_column_constraints_checked=False,
        host_realization_claimed=False, whole_profile_excluded=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--records', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.records), sort_keys=True, separators=(',',':')))
