#!/usr/bin/env python3
"""Exact six-case obstruction to the h=15 weight-four-pair carrier."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, separators=(',', ':')) + '\n').encode('ascii')


def mul4(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7  # X^2+X+1 over F2.
    return result


def plane_lines():
    lines = [frozenset(4*x+(mul4(m,x)^c) for x in range(4))
             for m in range(4) for c in range(4)]
    lines += [frozenset(4*x+y for y in range(4)) for x in range(4)]
    counts = Counter(p for line in lines for p in combinations(sorted(line),2))
    require(len(set(lines))==20 and set(counts)==set(combinations(range(16),2))
            and set(counts.values())=={1}, 'wrong field plane')
    return lines


def case_instance(chosen):
    require(tuple(chosen) in tuple(combinations([2,3,8,12],2)), 'unknown case')
    a,b,z,u,v,c,d = 16,0,17,11,4,14,1
    axes = {frozenset([0,1,2,3]),frozenset([0,4,8,12])}
    words = [frozenset((line-{0}) | {a,z}) if line in axes
             else frozenset(line | {z}) for line in plane_lines()]
    require(len(words)==len(set(words))==20 and
            all(len(p&q)<=2 for p,q in combinations(words,2)), 'invalid split star')
    fixed = [word-{a} for word in words if a in word]
    require(len(fixed)==2, 'wrong shared blocks')
    b_side = set(range(1,16))-{1,2,3,4,8,12}
    leave = {tuple(sorted((z,y))) for y in b_side | {b}}
    leave |= {tuple(sorted((u,y))) for y in [c,v,d]}
    leave |= {tuple(sorted((c,y))) for y in chosen}
    matched = tuple(sorted({2,3,8,12}-set(chosen)))
    leave.add(matched)
    degrees = Counter(y for p in leave for y in p)
    require(len(leave)==16 and all(degrees[y]=={z:10,u:4,c:4}.get(y,1)
            for y in set(range(18))-{a}), 'wrong complete leave')
    used = {p for q in fixed for p in combinations(sorted(q),2)}
    conflict = used & leave
    if conflict:
        return {'conflict': sorted(conflict), 'leave':leave,
                'fixed':fixed, 'star':words}
    rows = sorted(set(combinations(sorted(set(range(18))-{a}),2))-leave-used)
    row_set = set(rows)
    columns = []
    for q in combinations(range(16),4):
        if not set(combinations(q,2)) <= row_set:
            continue
        word = frozenset(q) | {a}
        if all(len(word & other)<=2 for other in words):
            columns.append(q)
    require(len(rows)==108, 'wrong uncovered pair universe')
    return {'rows':rows, 'columns':columns, 'leave':leave,
            'fixed':fixed, 'star':words}


def exact_cover(rows, columns, seconds=15, node_limit=200000):
    """Partition all rows; each recursive branch selects its pivot's unique column."""
    index = {p:i for i,p in enumerate(rows)}
    masks = [sum(1 << index[p] for p in combinations(q,2)) for q in columns]
    row_columns = [0]*len(rows)
    for i,m in enumerate(masks):
        bits = m
        while bits:
            bit = bits & -bits
            row_columns[bit.bit_length()-1] |= 1 << i
            bits -= bit
    conflicts = []
    for m in masks:
        bits,conflict = m,0
        while bits:
            bit = bits & -bits
            conflict |= row_columns[bit.bit_length()-1]
            bits -= bit
        conflicts.append(conflict)
    nodes = 0
    start = time.monotonic()
    leaves = sha256()

    def visit(uncovered, active, chosen):
        nonlocal nodes
        nodes += 1
        if nodes>node_limit or (nodes%128==0 and time.monotonic()-start>seconds):
            raise RuntimeError('INCOMPLETE: exact-cover cap reached; no exclusion')
        if not uncovered:
            return chosen
        bits,least,options = uncovered,None,0
        while bits:
            bit = bits & -bits
            j = bit.bit_length()-1
            here = active & row_columns[j]
            count = here.bit_count()
            if not count:
                leaves.update(('dead '+str(j)+' '+','.join(map(str,chosen))+'\n').encode())
                return None
            if least is None or count<least:
                least,options = count,here
                if count==1:
                    break
            bits -= bit
        while options:
            bit = options & -options
            i = bit.bit_length()-1
            require(masks[i] & uncovered == masks[i], 'active column covers a used pair')
            solution = visit(uncovered ^ masks[i], active & ~conflicts[i], chosen+[i])
            if solution is not None:
                return solution
            options -= bit
        return None

    solution = visit((1<<len(rows))-1,(1<<len(columns))-1,[])
    if solution is not None:
        counts = Counter(p for i in solution for p in combinations(columns[i],2))
        require(set(counts)==set(rows) and set(counts.values())<={1}, 'bad cover witness')
    return solution, {'nodes':nodes, 'dead_leaf_stream_sha256':leaves.hexdigest()}


def controls():
    # Full brute-force cover comparison on every simple graph of order <=5.
    checked = 0
    for n in range(6):
        pairs = tuple(combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            rows = tuple(p for i,p in enumerate(pairs) if bits>>i&1)
            row_set = set(rows)
            columns = [q for q in combinations(range(n),4)
                       if set(combinations(q,2))<=row_set]
            brute = False
            for subset in range(1<<len(columns)):
                counts = Counter(p for i,q in enumerate(columns) if subset>>i&1
                                 for p in combinations(q,2))
                if set(counts)==row_set and set(counts.values())<={1}:
                    brute = True
                    break
            solution,_ = exact_cover(rows,columns)
            require((solution is not None)==brute, 'small-graph cover mismatch')
            checked += 1
    require(checked==1100, 'incomplete small-graph audit')
    # Two directly known positive twenty-quadruple instances.
    positives = []
    for label,vertices,leave in [
        ('affine_plane_unused_point',set(range(17)),{(y,16) for y in range(16)}),
        ('actual_incumbent_point_0',set(range(1,18)),None)
    ]:
        if leave is None:
            words = (HERE/'baseline69.txt').read_text().splitlines()
            blocks = [frozenset(i for i,b in enumerate(word) if b=='1') for word in words]
            star = [b-{0} for b in blocks if 0 in b]
            require(len(star)==20 and all(len(q)==4 for q in star), 'bad incumbent star')
            counts = Counter(p for q in star for p in combinations(sorted(q),2))
            require(len(counts)==120 and set(counts.values())=={1}, 'incumbent star invalid')
            leave = set(combinations(sorted(vertices),2))-set(counts)
        rows = sorted(set(combinations(sorted(vertices),2))-leave)
        columns = [q for q in combinations(sorted(vertices),4)
                   if set(combinations(q,2))<=set(rows)]
        solution,stats = exact_cover(rows,columns)
        require(solution is not None and len(solution)==20, 'known positive fixture rejected')
        positives.append({'fixture':label,'quadruples':len(solution),'nodes':stats['nodes']})
    return {'all_simple_graphs_order_at_most_5':checked,'positive_controls':positives}


def normalization_checks():
    perms = list(permutations(range(4)))
    even = {p for p in perms if sum(p[i]>p[j] for i in range(4)
            for j in range(i+1,4))%2==0}
    adjacent = {p:{q for q in perms if sum(x!=y for x,y in zip(p,q))==2} for p in perms}
    require(all(len(neighbors)==6 for neighbors in adjacent.values()), 'bad transposition graph')
    reached,stack = set(),[perms[0]]
    while stack:
        p = stack.pop()
        if p not in reached:
            reached.add(p)
            stack.extend(adjacent[p]-reached)
    require(len(reached)==24 and len(even)==12, 'wrong Cayley graph coverage')
    require(all(q not in even for p in even for q in adjacent[p]), 'bad parity bipartition')
    graph_lines = [frozenset(4*x+p[x] for x in range(4)) for p in even]
    graph_lines += [frozenset(4*x+y for y in range(4)) for x in range(4)]
    graph_lines += [frozenset(4*x+y for x in range(4)) for y in range(4)]
    require(set(graph_lines)==set(plane_lines()), 'A4 and F4 planes differ entry by entry')
    return {'permutations':24,'transposition_edges':72,'connected':True,
            'even_permutations':12,'A4_and_F4_lines_match':True}


def report():
    cases = []
    for chosen in combinations([2,3,8,12],2):
        instance = case_instance(chosen)
        row = {'case':list(chosen)}
        if 'conflict' in instance:
            row.update({'status':'fixed_block_leave_conflict',
                        'conflicting_pairs':[list(p) for p in instance['conflict']]})
        else:
            rows,columns = instance['rows'],instance['columns']
            solution,stats = exact_cover(rows,columns)
            require(solution is None, 'compatible twenty-quadruple packing found; obstruction false')
            row.update({'status':'complete_no_cover','remaining_pairs':len(rows),
                        'candidate_quads':len(columns),**stats,
                        'candidate_quads_sha256':sha256(encoded(columns)).hexdigest()})
        cases.append(row)
    return {'cases':cases,'normalization_checks':normalization_checks(),
            'controls':controls(),'weighted_cases_covered':6,
            'global_72_word_exclusion':False,'theorem_depends_on_computation':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    result = report()
    path = HERE/'support16_expected.json'
    if args.write_expected:
        expected = json.loads(path.read_text()) if path.exists() else {}
        expected['primary'] = result
        path.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        require(json.loads(path.read_text())['primary']==result, 'primary expected report differs')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
