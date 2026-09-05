#!/usr/bin/env python3
"""Solver-free audit of a 26-vertex typed-extension bound and its M=217 use."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
W_EDGES = frozenset(((0,2),(0,3),(1,2),(1,3),(0,4),(1,5),(2,6),(3,7),(4,5),(6,7)))
WEIGHTS = {(0,4):1, (1,5):1, (2,6):1, (3,7):1, (4,5):2, (6,7):2}
BLUE_PAIRS = tuple((a,b) for a in (4,5) for b in (6,7))
CELLS = (5,6,9,10,17,18)
PARENT_HASH = '518a05072a726287628c57e8c9d9bc16aac4380dd800b4d807d00208b6b6e624'


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a,b in edges:
        require(0 <= a < b < n, 'simple labeled edge')
        adj[a].add(b)
        adj[b].add(a)
    return adj


def clique(adj, vertices, red):
    return all((b in adj[a]) == red for a,b in combinations(vertices,2))


def code(adj):
    return sum(1 << k for k,(a,b) in enumerate(combinations(range(len(adj)),2)) if b in adj[a])


def from_code(n, mask):
    return adjacency(n, [e for k,e in enumerate(combinations(range(n),2)) if mask >> k & 1])


def augment(n):
    """Every labeled triangle-free graph of order n with independence <4."""
    if n == 0:
        yield ()
        return
    for old in augment(n-1):
        triples = [sum(1 << v for v in t) for t in combinations(range(n-1),3)
                   if all(not(old[a] >> b & 1) for a,b in combinations(t,2))]
        # In a triangle-free graph, a neighborhood is independent, hence has
        # size at most three when no independent four-set is allowed.
        for size in range(min(3,n-1)+1):
            for vs in combinations(range(n-1),size):
                mask = sum(1 << v for v in vs)
                if any(old[v] & mask for v in vs):
                    continue
                if any(not(mask & t) for t in triples):
                    continue
                yield tuple(old[v] | (((mask >> v) & 1) << (n-1)) for v in range(n-1)) + (mask,)


def bit_code(adj):
    return sum(1 << k for k,(a,b) in enumerate(combinations(range(len(adj)),2)) if adj[a] >> b & 1)


def orbit(adj):
    edges = [(a,b) for a,b in combinations(range(len(adj)),2) if b in adj[a]]
    ranks = {e:k for k,e in enumerate(combinations(range(len(adj)),2))}
    images = set()
    for perm in permutations(range(len(adj))):
        images.add(sum(1 << ranks[tuple(sorted((perm[a],perm[b])))] for a,b in edges))
    return images


def decode_g6(line):
    require(len(line) == 6 and line[0] == 'G', 'eight-vertex graph6 record')
    bits = []
    for char in line[1:]:
        value = ord(char)-63
        require(0 <= value < 64, 'graph6 character')
        bits.extend((value >> shift) & 1 for shift in range(5,-1,-1))
    require(not any(bits[28:]), 'graph6 padding')
    pairs = [(i,j) for j in range(1,8) for i in range(j)]
    return adjacency(8, [e for e,bit in zip(pairs,bits) if bit])


def classify_w():
    generated = {}
    counts = []
    for n in range(9):
        masks = [bit_code(g) for g in augment(n)]
        require(len(masks) == len(set(masks)), 'augmentation label uniqueness')
        generated[n] = set(masks)
        counts.append(len(masks))
    # Different reference algorithm: inspect all edge-bit assignments through
    # order six and compare complete sets, not just totals.
    reference_graphs = 0
    for n in range(7):
        good = set()
        for mask in range(1 << (n*(n-1)//2)):
            adj = from_code(n,mask)
            reference_graphs += 1
            if any(clique(adj,t,True) for t in combinations(range(n),3)):
                continue
            if any(clique(adj,t,False) for t in combinations(range(n),4)):
                continue
            good.add(mask)
        require(good == generated[n], 'entry-level brute/augmentation agreement')
    remaining = set(generated[8])
    classes = []
    orbits = {}
    while remaining:
        mask = min(remaining)
        adj = from_code(8,mask)
        images = orbit(adj)
        require(images <= remaining, 'complete disjoint labeled orbit')
        remaining -= images
        edges = sum(len(a) for a in adj)//2
        classes.append({'lex_mask':mask, 'edges':edges, 'labeled_graphs':len(images),
                        'automorphisms':40320//len(images), 'degrees':sorted(map(len,adj))})
        orbits[edges] = images
    require([c['edges'] for c in classes] == [10,11,12], 'three critical classes')
    require(code(adjacency(8,W_EDGES)) in orbits[10], 'natural ten-edge labeling')
    catalog = [decode_g6(line) for line in (HERE/'r34_8.g6').read_text().splitlines()]
    require(len(catalog) == 3, 'catalog comparison length')
    catalog_types = [sum(map(len,g))//2 for g in catalog]
    require(set(catalog_types) == {10,11,12}, 'catalog class coverage')
    require(all(code(g) in orbits[e] for g,e in zip(catalog,catalog_types)), 'literal external catalog comparison')
    return {'labeled_counts_orders_0_to_8':counts, 'classes':classes,
            'reference_edge_assignments_orders_0_to_6':reference_graphs,
            'external_catalog_edge_order':catalog_types}


def admissible(T):
    W = adjacency(8,W_EDGES)
    return not any(clique(W,s,False) for s in combinations(set(range(8))-T,3))


def score(T, weights=WEIGHTS):
    return (sum(weight for pair,weight in weights.items() if set(pair) <= T)
            + sum(not (set(pair) & T) for pair in BLUE_PAIRS))


def pointwise(weights=WEIGHTS):
    valid = []
    by_case = {}
    for mask in range(256):
        T = {i for i in range(8) if mask >> i & 1}
        if not admissible(T):
            continue
        value = score(T,weights)
        require(value >= 3, ('pointwise inequality',mask,value))
        case = (len(T & {4,5}), len(T & {6,7}))
        if case not in by_case:
            by_case[case] = []
        by_case[case].append(value)
        valid.append(mask)
    require(len(valid) == 113, 'all admissible eight-bit neighborhoods')
    return valid, [{'low_counts':list(c), 'patterns':len(v), 'minimum_score':min(v)}
                   for c,v in sorted(by_case.items())]


def core(cross_mask):
    edges = [(0,1),(2,3),(2,4)]
    edges += [(a,b) for k,(a,b) in enumerate((a,b) for a in (0,1) for b in (2,3,4)) if cross_mask >> k & 1]
    edges += [(a+5,b+5) for a,b in W_EDGES]
    edges += [(e,w+5) for e in (2,3,4) for w in range(8)]
    return adjacency(13,edges)


def rooted_cap(adj, root, red):
    require(len(root) == 3 and clique(adj,root,red), 'monochromatic root triangle')
    fixed = {v for v in range(13) if v not in root
             and all((v in adj[r]) == red for r in root)}
    # The full common neighborhood of a monochromatic triangle has at most
    # four vertices: its edges must be the opposite color to avoid a K5.
    return 4-len(fixed), fixed


def roots():
    return ([(False, (r,a+5,b+5), 1) for r in (0,1) for a,b in BLUE_PAIRS]
            + [(True, (e,a+5,b+5), weight) for e in (2,3,4) for (a,b),weight in WEIGHTS.items()])


def root_audit(valid):
    records = []
    extension_tests = 0
    for cross in range(64):
        adj = core(cross)
        require(not any(clique(adj,f,red) for f in combinations(range(13),5) for red in (True,False)), 'literal core is Ramsey')
        total = 0
        for red,root,weight in roots():
            cap,fixed = rooted_cap(adj,root,red)
            require(cap == (2 if not red or root[0] == 2 else 3), 'root capacity')
            total += weight*cap
            if cross == 0:
                records.append({'color':'red' if red else 'blue', 'root':list(root),
                                'weight':weight, 'fixed_common':sorted(fixed), 'outside_cap':cap})
        require(total == 80, 'weighted root capacities')
        fours = {red:[sum(1 << i for i in t) for t in combinations(range(13),4) if clique(adj,t,red)]
                 for red in (True,False)}
        for cell in CELLS:
            survivors = []
            for mask in range(256):
                x = cell | (mask << 5)
                if any(x & t == t for t in fours[True]) or any(not (x & t) for t in fours[False]):
                    continue
                survivors.append(mask)
                # Independent interpretation: membership in each literal
                # root's common neighborhood, not the hand score formula.
                actual = 0
                for red,root,weight in roots():
                    if all(bool(x >> r & 1) == red for r in root):
                        actual += weight
                require(actual == score({i for i in range(8) if mask >> i & 1}) and actual >= 3,
                        'literal typed-extension coverage')
                extension_tests += 1
            require(survivors == valid, 'exact typed single-vertex extension domain')
    require(len(records) == 26, '26 literal root inequalities')
    return records, extension_tests


def parent_audit(witness_path):
    path = HERE.parent/'ramsey_r55_paired_neighborhood_budget/verify.py'
    require(sha256(path.read_bytes()).hexdigest() == PARENT_HASH, 'pinned paired checker')
    replay = subprocess.run([sys.executable,'-O',str(path)],check=True,capture_output=True,text=True)
    require(replay.stdout == (path.parent/'EXPECTED_OUTPUT.txt').read_text(), 'parent complete replay')
    spec = importlib.util.spec_from_file_location('ten_edge_parent',path)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    old,union = parent.inputs()
    near = parent.adjacency(443,5)
    records = json.loads(witness_path.read_text())
    expected = [(a,b) for a in range(3,6) for b in range(2,5) if 6 <= a+b <= 8]
    require(len(records) == len(expected) == 7, 'seven adjusted witnesses')
    output = []
    for record,(a,b) in zip(records,expected):
        y = parent.normal_form(a,b)
        require(record['a'] == [a,b,14-a-b], 'ordered pattern coverage')
        require(sum(y[x] for x in CELLS) == 28 and y[28] == 8, '28 typed extensions and W8')
        parent.check_edge_witness(y,record['edge_counts'],near,union)
        pairs,_,rows = parent.edge_rows(y,near,union)
        ww = record['edge_counts'][pairs.index((28,28))]
        require(11 <= ww <= 12, 'new W edge bound')
        output.append({'a':record['a'], 'aggregate_rows':len(rows)+1, 'W_edges':ww})
    previous = json.loads((path.parent/'EDGE_WITNESSES.json').read_text())
    invalidated = [r['a'] for r in previous if r['edge_counts'][-1] == 10]
    require(invalidated == [[4,2,8],[5,2,7]], 'exact scope of old witness invalidation')
    return output, invalidated


def mutation_tests():
    changed = dict(WEIGHTS)
    changed[(0,4)] = 0
    tests = [lambda: pointwise(changed),
             lambda: rooted_cap(core(0),(0,9,10),False),
             lambda: require(admissible({4}), 'forbidden blue triple'),
             lambda: require(not any(clique(adjacency(8,W_EDGES-{(4,5)}),s,False)
                                     for s in combinations(range(8),4)), 'altered critical graph')]
    for test in tests:
        try:
            test()
        except ValueError:
            continue
        raise ValueError('corrupt evidence was accepted')
    return len(tests)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--edge-witnesses', type=Path, default=HERE/'EDGE_WITNESSES.json')
    args = parser.parse_args()
    classification = classify_w()
    print('PASS complete W8 classification: 17640 labeled graphs, three types with 10/11/12 edges',flush=True)
    valid,cases = pointwise()
    root_records,extensions = root_audit(valid)
    print('PASS 113 neighborhoods, 64 arbitrary cross-link cores, 43392 literal typed extensions',flush=True)
    print('PASS 26 root inequalities: 3|X|<=80, hence |X|<=26; target |X|=28 is impossible',flush=True)
    witnesses,invalidated = parent_audit(args.edge_witnesses)
    mutations = mutation_tests()
    print('PASS parent seven-pattern replay; ten-edge W excluded for all seven patterns',flush=True)
    print('PASS seven exact aggregate witnesses with W edges 11 or 12; two old witnesses invalidated',flush=True)
    print('PASS four negative tests; solver-free verifier',flush=True)
    print('SCOPE W has one of two remaining types; no profile exclusion or target graph; totals 67/273 unchanged',flush=True)
    report = {'classification':classification, 'pointwise_cases':cases, 'root_inequalities':root_records,
              'literal_extension_tests':extensions, 'arbitrary_cross_link_cores':64,
              'weighted_bound':{'left_coefficient':3,'right_side':80,'integer_limit':26,'required':28},
              'adjusted_edge_witnesses':witnesses, 'invalidated_parent_witnesses':invalidated,
              'negative_tests':mutations, 'scope':'Only the ten-edge critical W type is excluded; no Ramsey graph or profile exclusion.'}
    if args.report:
        args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
