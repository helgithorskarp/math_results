"""Guarded serial necessary pair cover on a deterministic cut-frontier interval.

The producer only proposes deletions. A separate literal checker must check them.
No limit or nonempty fixed point implies nonexistence or a realized full host.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

AT = (3,5,5,7,9,9,11,13,3)
BT = (2,4,6,6,8,10,10,12,12)


class Limit(Exception):
    pass


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run(records, columns, start, stop, out):
    begun = time.monotonic()
    work = 0

    def tick():
        nonlocal work
        if work >= 2000000 or time.monotonic()-begun >= 40:
            raise Limit()
        work += 1

    column_packet = [json.loads(line) for line in Path(columns).read_text().splitlines()]
    wanted = [index for index, witness in column_packet if witness is None]
    require(0 <= start < stop <= len(wanted), 'Bad deterministic frontier interval')
    selected = set(wanted[start:stop])
    originals = []
    rows_sha = hashlib.sha256()
    for index, line in enumerate(Path(records).read_bytes().splitlines(keepends=True)):
        rows_sha.update(line)
        if index in selected:
            graph, domains = json.loads(line)
            originals.append((index, graph, domains))
    require(rows_sha.hexdigest() == '8ac8cfc8cd19e3123a9c85f1e87c94af8846ea06d2418d853e67b206353a8e7b',
            'Wrong original row-domain input')
    require(hashlib.sha256(Path(columns).read_bytes()).hexdigest() ==
            'a3c000a32e69e0a49ef9d7231ebe3d7f6a29277479ecf62dce816b8d1290c0c6',
            'Wrong original column certificate')
    b_slices = tuple(sum(1 << k for k, t in enumerate(BT) if t & (1 << low))
                     for low in range(4))
    cache = {}

    def compatible(i, a, j, b, graph):
        tick()
        if i > j:
            i, a, j, b = j, b, i, a
        red = bool(graph[i] & (1 << j))
        local = (graph[i] & graph[j]).bit_count()
        key = i,a,j,b,red,local
        if key in cache:
            return cache[key]
        shared_types = AT[i] & AT[j]
        shared_cut = a & b
        cap = 3 if red else 6
        valid = shared_types.bit_count() + local + shared_cut.bit_count() <= cap
        if valid and red:
            valid = all(not (shared_cut & b_slices[low])
                        for low in range(4) if shared_types & (1 << low))
        cache[key] = valid
        return valid

    cases = []
    limit = None
    for index, graph, domains in originals:
        current = [list(domain) for domain in domains]
        cuts = []
        before = work
        status = 'PAIR_FIXED_POINT_NO_EXCLUSION'
        try:
            while True:
                changed = False
                for i in range(9):
                    for word in tuple(current[i]):
                        for j in range(9):
                            if i == j:
                                continue
                            if not any(compatible(i,word,j,other,graph) for other in current[j]):
                                cuts.append([i,word,j])
                                current[i].remove(word)
                                changed = True
                                break
                        if not current[i]:
                            status = 'PROPOSED_PAIR_EMPTY_DOMAIN_EXCLUSION'
                            break
                    if status == 'PROPOSED_PAIR_EMPTY_DOMAIN_EXCLUSION':
                        break
                if status == 'PROPOSED_PAIR_EMPTY_DOMAIN_EXCLUSION' or not changed:
                    break
        except Limit:
            status = 'OPERATIONAL_LIMIT_NONEMPTY_CHECKABLE_PREFIX'
            limit = index
        cases.append(dict(graph_index=index, cuts=cuts, final_sizes=list(map(len,current)),
                          status=status, work_units=work-before))
        if limit is not None:
            break
    packet = dict(agent='six-books-3',role='researcher',start=start,stop=stop,
        requested_graph_indices=wanted[start:stop],original_rows_sha256=rows_sha.hexdigest(),
        original_columns_sha256=hashlib.sha256(Path(columns).read_bytes()).hexdigest(),
        cases=cases,work_units=work,limited_graph_index=limit,
        unvisited_requested_graphs=len(originals)-len(cases),
        work_guard=2000000,internal_seconds_guard=40,
        whole_requested_interval_processed=limit is None and len(cases)==stop-start,
        producer_is_untrusted=True,host_realization_claimed=False,whole_profile_excluded=False)
    Path(out).write_text(json.dumps(packet,sort_keys=True,separators=(',',':'))+'\n')
    return dict(agent='six-books-3',role='researcher',start=start,stop=stop,
        processed_cases=len(cases),proposed_exclusions=sum(c['status']=='PROPOSED_PAIR_EMPTY_DOMAIN_EXCLUSION' for c in cases),
        nonempty_fixed_points=sum(c['status']=='PAIR_FIXED_POINT_NO_EXCLUSION' for c in cases),
        proposed_cuts=sum(len(c['cuts']) for c in cases),limited_graph_index=limit,
        work_units=work,unique_cached_pair_predicates=len(cache),
        whole_requested_interval_processed=packet['whole_requested_interval_processed'],
        packet_sha256=hashlib.sha256(Path(out).read_bytes()).hexdigest(),
        producer_is_untrusted=True,whole_profile_excluded=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--records',required=True)
    parser.add_argument('--columns',required=True)
    parser.add_argument('--start',type=int,required=True)
    parser.add_argument('--stop',type=int,required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.records,args.columns,args.start,args.stop,args.out),
                     sort_keys=True,separators=(',',':')))
