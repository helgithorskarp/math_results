"""Independent labelled-cube and entry-level deletion certificate verifier.

Imports no producer module. Graphs use edge sets; the lookup producer uses
catalogue relabellings. This checker exhausts the full labelled Boolean cube.
"""
from array import array
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys
import time

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise ValueError(message)

def graph_lines(cache,n):
    specs = json.loads((HERE / 'INPUTS.json').read_text())
    s = next(x for x in specs if x['n'] == n)
    raw = (Path(cache) / s['name']).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == s['sha256'] and len(raw) == s['bytes'], 'input identity')
    lines=raw.splitlines()
    require(len(lines)==s['count'],'input records')
    return lines

def parse_line(line,n):
    require(line[0] == n+63 and len(line)==1+(n*(n-1)//2+5)//6,'input order/size')
    g = set(); k = 0
    for j in range(1,n):
        for i in range(j):
            if (line[1+k//6]-63) & (1 << (5-k%6)): g.add((i,j))
            k += 1
    return g

def read_graphs(cache,n):
    return [parse_line(line,n) for line in graph_lines(cache,n)]

def exhaustive_lookup(cache, tables, n):
    graphs = read_graphs(cache, n); edges = list(combinations(range(n), 2))
    bit = {e: 1 << k for k,e in enumerate(edges)}
    masks = [sum(bit[e] for e in combinations(s,2)) for s in combinations(range(n),4)]
    owners = array('h'); owners.frombytes((Path(tables)/f'owners{n}.bin').read_bytes())
    ids = array('H'); ids.frombytes((Path(tables)/f'perms{n}.bin').read_bytes())
    require(owners.itemsize == ids.itemsize == 2, 'array ABI')
    if sys.byteorder != 'little': owners.byteswap(); ids.byteswap()
    require(len(owners) == len(ids) == 2**len(edges), 'lookup table size')
    orders = list(permutations(range(n)))
    # Entry-level certificate check, with an independent full-cube classifier.
    transported_bits = [[bit[tuple(sorted((p[i],p[j])))] for i,j in edges] for p in orders]
    target_bits = [[int(e in g) for e in edges] for g in graphs]
    histogram = Counter(); edge_checks = 0
    for word in range(2**len(edges)):
        good = all((word & mask) not in (0, mask) for mask in masks)
        c = owners[word]
        require((c >= 0) == good, 'labelled cube lookup gap or false positive')
        if not good: continue
        require(c < len(graphs) and ids[word] < len(orders), 'lookup range')
        for flag, expected in zip(transported_bits[ids[word]], target_bits[c]):
            require(int(bool(word & flag)) == expected, 'lookup physical edge')
            edge_checks += 1
        histogram[c] += 1
    return {'n': n, 'labelled_inputs': len(owners), 'accepted': sum(histogram.values()),
            'rejected': len(owners)-sum(histogram.values()),
            'catalog_records': len(histogram), 'orbit_sizes': [histogram[i] for i in range(len(graphs))],
            'edge_identities': edge_checks}

def audit_deletions(cache, out, n):
    lines = graph_lines(cache, n); targets = read_graphs(cache, n-4)
    record = struct.Struct('<IBH'+'B'*(n-4)); path = Path(out)/f'deletions{n}.bin'
    require(path.stat().st_size == len(lines)*(6 if n==11 else 1)*record.size, 'deletion length')
    hist = Counter(); matching_hist = Counter(); cardinalities = Counter()
    total = edges_checked = 0; digest = hashlib.sha256()
    with path.open('rb') as f:
        for c, line in enumerate(lines):
            source=parse_line(line,n)
            used = set(); selected = []
            for edge in sorted(source):
                if not used.intersection(edge):
                    selected.append(edge); used.update(edge)
            selected = selected[:4 if n==11 else 2]
            require(len(selected) == (4 if n==11 else 2), 'matching coverage')
            matching_hist[tuple(v for e in selected for v in e)] += 1
            found = set()
            for choice, (e,fourth) in enumerate(combinations(selected,2)):
                raw = f.read(record.size); digest.update(raw)
                source_id, choice_id, target_id, *order = record.unpack(raw)
                require((source_id,choice_id)==(c,choice), 'deletion source indexing')
                require(0<=target_id<len(targets), 'deletion target range')
                require(sorted(order)==[v for v in range(n) if v not in e+fourth], 'deletion permutation')
                for i,j in combinations(range(n-4),2):
                    require((tuple(sorted((order[i],order[j]))) in source)==((i,j) in targets[target_id]), 'deletion physical edge')
                    edges_checked += 1
                hist[target_id] += 1; found.add(target_id); total += 1
            cardinalities[len(found)] += 1
        require(not f.read(1), 'deletion trailing data')
    matching_json = json.dumps(sorted((list(k),v) for k,v in matching_hist.items()), separators=(',', ':')).encode()
    return {'source_order': n, 'destination_order': n-4, 'source_cores': len(lines),
            'deletions': total, 'record_bytes': record.size, 'sha256': digest.hexdigest(),
            'destination_histogram': [hist[i] for i in range(len(targets))],
            'distinct_destination_records': len(hist),
            'destinations_per_source_histogram': [list(x) for x in sorted(cardinalities.items())],
            'distinct_selected_matchings': len(matching_hist),
            'matching_histogram_sha256': hashlib.sha256(matching_json).hexdigest(),
            'edge_identities': edges_checked}

def run(cache, out):
    start = time.monotonic(); out = Path(out)
    lookup = [exhaustive_lookup(cache,out/'tables',n) for n in (3,7)]
    claimed = json.loads((out/'tables'/'LOOKUP.json').read_text())
    for a,b in zip(lookup,claimed):
        for key in a:
            if key != 'edge_identities': require(a[key] == b[key], 'lookup summary '+key)
    deletions = [audit_deletions(cache,out,n) for n in (11,7)]
    claimed = json.loads((out/'CENSUS.json').read_text())
    for a,b in zip(deletions,claimed['core_interfaces']):
        for key in a:
            if key != 'edge_identities': require(a[key] == b[key], 'deletion summary '+key)
    counts = {7:640,8:546356,9:362,10:4}
    rows = [{'q':q,'r':r,'tasks':counts[q],
             'added_clauses_per_task':36*r if q==8 else 6*r if q==9 else 0}
            for q in range(7,11) for r in range(5,q+1)]
    require(rows == claimed['registry'], 'registry interface')
    require(sum(x['tasks'] for x in rows) == claimed['total_tasks'] == 2189178, 'whole registry')
    require(sum(x['tasks'] for x in rows if x['added_clauses_per_task']) == claimed['affected_tasks'] == 2187234, 'affected registry')
    require(sum(x['tasks']*x['added_clauses_per_task'] for x in rows) == claimed['total_added_clauses_over_registry'], 'clause registry total')
    return {'status':'INDEPENDENT_COMPLETE_CORE_BRIDGE_PASS', 'lookup':lookup,
            'deletions':deletions,'seconds':time.monotonic()-start}

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('cache'); p.add_argument('out'); p.add_argument('--receipt'); args=p.parse_args()
    result=run(args.cache,args.out)
    if args.receipt: Path(args.receipt).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['seconds'],
                      'lookup_inputs':sum(x['labelled_inputs'] for x in result['lookup']),
                      'deletions':sum(x['deletions'] for x in result['deletions'])}))
