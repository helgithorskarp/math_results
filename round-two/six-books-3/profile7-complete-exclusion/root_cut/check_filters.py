"""Literal certificate verifier for column separations and ordered pair cuts.

Imports no proposal code. The full cut-row domain is bound to its independently
verified record digest. Prefixes, empty domains, and fixed points stay distinct.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import time

TYPES = (2,3,3,4,5,5,6,6,7,8,9,9,10,10,11,12,12,13)
A = (2,4,5,8,10,11,14,17,1)
B = (0,3,6,7,9,12,13,15,16)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(records, columns, packets, fixed_out):
    begun = time.monotonic()
    work = 0

    def tick():
        nonlocal work
        if work >= 2000000 or time.monotonic()-begun >= 40:
            raise ValueError('Operational filter checker guard; incomplete verdict')
        work += 1

    row_bytes = Path(records).read_bytes()
    row_sha = hashlib.sha256(row_bytes).hexdigest()
    require(row_sha == '8ac8cfc8cd19e3123a9c85f1e87c94af8846ea06d2418d853e67b206353a8e7b',
            'Different fully verified cut-row data')
    originals = [json.loads(line) for line in row_bytes.splitlines()]
    require(len(originals) == 50400, 'Incomplete original graph domain')
    active = [i for i, (graph, domains) in enumerate(originals) if all(domains)]
    require(len(active) == 2908, 'Wrong original nonempty row population')
    column_bytes = Path(columns).read_bytes()
    column_sha = hashlib.sha256(column_bytes).hexdigest()
    column_packet = [json.loads(line) for line in column_bytes.splitlines()]
    require([entry[0] for entry in column_packet] == active, 'Column coverage/order differs')
    require(column_sha == 'a3c000a32e69e0a49ef9d7231ebe3d7f6a29277479ecf62dce816b8d1290c0c6',
            'Different column packet')
    degree = (5,4,5,5,4,5,5,5,5)
    extrema = {}
    target = [sum(degree[j] for j in range(9) if mask & (1 << j)) for mask in range(512)]

    def score(domain):
        key = tuple(domain)
        if key in extrema:
            return extrema[key]
        # Literal candidate bits, with the score table built by subset recurrence.
        bits = [[(word >> j) & 1 for j in range(9)] for word in domain]
        values = [[0]*512 for word in domain]
        low = [0]*512
        high = [0]*512
        for mask in range(1,512):
            tick()
            bit = mask & -mask
            j = bit.bit_length()-1
            for r, literal in enumerate(bits):
                values[r][mask] = values[r][mask ^ bit] + literal[j]
            low[mask] = min(row[mask] for row in values)
            high[mask] = max(row[mask] for row in values)
        extrema[key] = low, high
        return extrema[key]

    column_excluded = 0
    remaining = []
    tested_scores = 0
    for index, proposed in column_packet:
        graph, domains = originals[index]
        tables = [score(domain) for domain in domains]
        found = None
        for mask in range(1,512):
            tick()
            tested_scores += 1
            lower = sum(table[0][mask] for table in tables)
            upper = sum(table[1][mask] for table in tables)
            if lower > target[mask]:
                found = ['lower', mask, lower, target[mask]]
                break
            if upper < target[mask]:
                found = ['upper', mask, upper, target[mask]]
                break
        require(proposed == found, 'Actual full subset-score separation differs')
        if found is None:
            remaining.append(index)
        else:
            column_excluded += 1

    low_rows = [sum(1 << (h+4) for h in range(18) if TYPES[h] & (1 << low))
                for low in range(4)]
    B_points = sum(1 << (h+4) for h in B)
    full = (1 << 22)-1
    b_lifts = [sum(1 << (B[j]+4) for j in range(9) if word & (1 << j))
               for word in range(512)]
    a_lifts = [sum(1 << (A[j]+4) for j in range(9) if word & (1 << j))
               for word in range(512)]
    colors = {}

    def row(i, word, graph):
        key = i,word,graph[i]
        if key not in colors:
            red = TYPES[A[i]] | a_lifts[graph[i]] | b_lifts[word]
            require(red.bit_count() == 10 and not red & (1 << (A[i]+4)),
                    'Wrong literal high red row')
            colors[key] = red, full ^ (red | (1 << (A[i]+4)))
        return colors[key]

    def allowed(i, word, j, other, graph):
        tick()
        left_red, left_blue = row(i,word,graph)
        right_red, right_blue = row(j,other,graph)
        red_edge = bool(left_red & (1 << (A[j]+4)))
        require(red_edge == bool(right_red & (1 << (A[i]+4))), 'Reciprocal edge mismatch')
        if red_edge:
            common = left_red & right_red
            if common.bit_count() > 3:
                return False
            # Any such actually present four-clique contradicts the written
            # ordinary K4-free carrier lemma under the full profile hypotheses.
            for low in range(4):
                if common & (1 << low) and common & B_points & low_rows[low]:
                    return False
        elif (left_blue & right_blue).bit_count() > 6:
            return False
        return True

    checked_cases = []
    fixed = []
    previous_stop = 0
    actual_pair_exclusions = checked_cuts = 0
    packet_refs = []
    for path in packets:
        raw = Path(path).read_bytes()
        packet = json.loads(raw)
        require(packet['start'] == previous_stop
                and packet['requested_graph_indices'] == remaining[packet['start']:packet['stop']]
                and packet['whole_requested_interval_processed']
                and packet['limited_graph_index'] is None and packet['unvisited_requested_graphs'] == 0,
                'Incomplete, overlapping or mislabelled pair interval')
        require(packet['original_rows_sha256'] == row_sha
                and packet['original_columns_sha256'] == column_sha,
                'Pair original-domain binding differs')
        require([case['graph_index'] for case in packet['cases']] == packet['requested_graph_indices'],
                'Pair case coverage/order differs')
        packet_refs.append(dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest()))
        for case in packet['cases']:
            index = case['graph_index']
            graph, domains = originals[index]
            current = [list(domain) for domain in domains]
            for cut in case['cuts']:
                require(isinstance(cut,list) and len(cut)==3
                        and all(type(value) is int for value in cut), 'Malformed ordered cut')
                i, word, j = cut
                require(0 <= i < 9 and 0 <= j < 9 and i != j
                        and word in current[i] and all(current), 'Invalid, duplicate or post-empty cut')
                require(not any(allowed(i,word,j,other,graph) for other in current[j]),
                        'Deleted word has a literal ordinary compatible partner')
                current[i].remove(word)
                checked_cuts += 1
            require(case['final_sizes'] == list(map(len,current)), 'Final literal domain sizes differ')
            if any(not domain for domain in current):
                require(case['status'] == 'PROPOSED_PAIR_EMPTY_DOMAIN_EXCLUSION',
                        'Wrong actual empty-domain status')
                actual_pair_exclusions += 1
            else:
                require(case['status'] == 'PAIR_FIXED_POINT_NO_EXCLUSION', 'Wrong nonempty status')
                for i, domain in enumerate(current):
                    for word in domain:
                        for j in range(9):
                            if i != j:
                                require(any(allowed(i,word,j,other,graph) for other in current[j]),
                                        'Unfinished claimed nonempty fixed point')
                fixed.append(dict(graph_index=index, graph=graph, original_domains=domains,
                                  current_domains=current, cuts=case['cuts'],
                                  status='LITERAL_CHECKED_NONEMPTY_PAIR_FIXED_POINT'))
            checked_cases.append(index)
        previous_stop = packet['stop']
    require(checked_cases == remaining and previous_stop == len(remaining),
            'Incomplete full pair-frontier coverage')
    fixed_packet = dict(agent='six-books-3',role='researcher',source_rows_sha256=row_sha,
        source_columns_sha256=column_sha,source_pair_packets=packet_refs,cases=fixed,
        pair_cuts_verified=True,full_column_completion_unproved=True,
        host_realization_claimed=False,whole_profile_excluded=False)
    Path(fixed_out).write_text(json.dumps(fixed_packet,sort_keys=True,separators=(',',':'))+'\n')
    return dict(agent='six-books-3',role='researcher',status='COMPLETE_LITERAL_NECESSARY_ROOT_CUT_FILTER_CHECK',
        original_graphs=50400,empty_row_exclusions=47492,column_bound_exclusions=column_excluded,
        tested_column_subset_bounds=tested_scores,original_column_frontier=len(remaining),
        checked_pair_cases=len(checked_cases),literal_pair_empty_exclusions=actual_pair_exclusions,
        literal_checked_cuts=checked_cuts,remaining_fixed_points=len(fixed),
        remaining_graph_indices=[case['graph_index'] for case in fixed],
        fixed_packet_sha256=hashlib.sha256(Path(fixed_out).read_bytes()).hexdigest(),
        original_rows_sha256=row_sha,original_columns_sha256=column_sha,
        original_pair_packet_sha256=[record['sha256'] for record in packet_refs],
        imports_proposal_code=False,literal_22_point_colors_used=True,
        work_units=work,work_guard=2000000,internal_seconds_guard=40,
        host_realization_claimed=False,whole_profile_excluded=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--records',required=True)
    parser.add_argument('--columns',required=True)
    parser.add_argument('--packets',nargs='+',required=True)
    parser.add_argument('--fixed-out',required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.records,args.columns,args.packets,args.fixed_out),
                     sort_keys=True,separators=(',',':')))
