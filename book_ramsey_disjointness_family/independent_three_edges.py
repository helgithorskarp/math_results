#!/usr/bin/env python3
"""Independent indexed-domain reconstruction of the three-edge exclusion.

Imports no generator code; reconstructs the core from Steiner triples and
subsets from combinations. Rebuilds each frontier, checks every emitted
domain entry by entry, and validates the twelve literal triangle books.
Assertions must remain enabled.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('run this checker with Python assertions enabled')
Y = [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 23, 24]


def core_from_triples():
    blocks = [frozenset((x+d) % 13 for d in base)
              for base in [(0, 1, 4), (0, 2, 7)] for x in range(13)]
    assert len(set(blocks)) == 26
    assert all(sum(set(p) <= b for b in blocks) == 1
               for p in combinations(range(13), 2))
    triples = [blocks[i] for i in Y]
    return [frozenset(j for j, b in enumerate(triples)
                      if i != j and not a & b)
            for i, a in enumerate(triples)]


def known_adjacency(core, masks, J):
    """Unknown cross edges belong to neither color; all J edges are known."""
    vertices = set(range(16))
    red = [set(s) for s in core]+[set() for _ in range(6)]
    blue = [vertices-{i}-set(s) for i, s in enumerate(core)]+[set() for _ in range(6)]
    for role in range(6):
        red[16+role] = {16+j for j in J[0][role]}
        blue[16+role] = {16+j for j in J[1][role]}
    for role, mask in masks.items():
        for y in range(16):
            adjacency = red if mask >> y & 1 else blue
            adjacency[16+role].add(y)
            adjacency[y].add(16+role)
    return red, blue


def first_book(core, masks, J):
    for color, adjacency in enumerate(known_adjacency(core, masks, J)):
        cap = [3, 6][color]
        for i in range(22):
            for j in range(i):
                if j in adjacency[i]:
                    pages = adjacency[i] & adjacency[j]
                    if len(pages) > cap:
                        return color, j, i, sorted(pages)[:cap+1]
    return None


def compute(trace_directory):
    core = core_from_triples()
    fixture = (HERE/'core16.edges').read_text().splitlines()
    assert fixture[0] == '16'
    fixture_edges = [tuple(map(int, line.split())) for line in fixture[1:]]
    assert len(fixture_edges) == len(set(fixture_edges)) == 48
    assert set(fixture_edges) == {(i, j) for i in range(16) for j in core[i] if j < i}
    vertices = frozenset(range(16))
    blue_core = [vertices-{i}-ns for i, ns in enumerate(core)]
    assert all(len(s) == 6 for s in core)
    spines = [(i, j, color) for color, adjacency in enumerate([core, blue_core])
              for i in range(16) for j in range(i) if j in adjacency[i]]
    capacities = [[3, 6][c]-len([core, blue_core][c][i] & [core, blue_core][c][j])
                  for i, j, c in spines]
    assert Counter(capacities) == {0: 3, 1: 45, 2: 69, 3: 3}
    zero = [(i, j, c) for (i, j, c), cap in zip(spines, capacities) if cap == 0]
    # Combination traversal and literal neighborhoods, rather than mask scan.
    row_sets = {}
    for size in range(17):
        for subset in combinations(range(16), size):
            ns = frozenset(subset)
            if any(len(core[y] & ns) > 3 for y in ns):
                continue
            bs = vertices-ns
            if any(i in [ns, bs][c] and j in [ns, bs][c] for i, j, c in zero):
                continue
            if any(len(blue_core[y] & bs) > 6 for y in bs):
                continue
            row_sets[sum(1 << y for y in ns)] = (ns, bs)
    masks = sorted(row_sets)
    ns = [row_sets[m][0] for m in masks]
    bs = [row_sets[m][1] for m in masks]
    m = len(masks)
    all_rows = (1 << m)-1
    row_id = {mask: i for i, mask in enumerate(masks)}
    ten = [i for i, n in enumerate(ns) if len(n) == 10]
    assert len(ten) == 4
    assert all(len(n) >= 5 and len(b) >= 6 for n, b in zip(ns, bs))
    assert all(len(core[y] & ns[i]) == 3 for i in ten for y in ns[i])
    not_ten = all_rows ^ sum(1 << i for i in ten)
    # Bit sets index rows, not core vertex assignments. All tables below are
    # derived from literal page definitions in this independent reconstruction.
    points = [sum(1 << i for i in range(m) if y in ns[i]) for y in range(16)]
    new_red = [[sum(1 << i for i in range(m)
                    if y not in ns[i] or len(core[y] & ns[i])+k <= 3)
                for k in range(6)] for y in range(16)]
    new_blue = [[sum(1 << i for i in range(m)
                     if y not in bs[i] or len(blue_core[y] & bs[i])+k <= 6)
                 for k in range(6)] for y in range(16)]
    features = [frozenset(k for k, (a, b, c) in enumerate(spines)
                          if a in [ns[i], bs[i]][c] and b in [ns[i], bs[i]][c])
                for i in range(m)]
    spine_rows = [sum(1 << i for i in range(m) if k in features[i])
                  for k in range(len(spines))]
    keys = [(0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (1, 5)]
    compat = {key: [0]*m for key in keys}
    for i in range(m):
        for j in range(i, m):
            common = ((masks[i] & masks[j]).bit_count(),
                      ((65535 ^ masks[i]) & (65535 ^ masks[j])).bit_count())
            for color, cap in keys:
                if common[color] <= cap:
                    compat[color, cap][i] |= 1 << j
                    compat[color, cap][j] |= 1 << i

    def members(bits):
        while bits:
            low = bits & -bits
            yield low.bit_length()-1
            bits ^= low

    def domain(context, role, J, base=all_rows):
        allowed = base
        # First intersect whole indexed pair domains. No branch is dropped
        # by a heuristic; every intersection expresses a spine inequality.
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            cap = [3, 6][color]-len(J[color][role] & J[color][old_role])
            allowed &= compat[color, cap][old_id]
            if not allowed:
                return 0
        used = Counter(k for _, old_id in context for k in features[old_id])
        for k, count in used.items():
            assert count <= capacities[k], 'invalid input context'
            if count == capacities[k]:
                allowed &= all_rows ^ spine_rows[k]
                if not allowed:
                    return 0
        for old_role, old_id in context:
            color = 0 if old_role in J[0][role] else 1
            neighbor_set = [ns, bs][color][old_id]
            for y in neighbor_set:
                pages = len([core, blue_core][color][y] & neighbor_set)
                pages += sum(other_role in J[color][old_role] and
                             y in [ns, bs][color][other_id]
                             for other_role, other_id in context)
                assert pages <= [3, 6][color]
                if pages == [3, 6][color]:
                    allowed &= (all_rows ^ points[y]) if color == 0 else points[y]
                    if not allowed:
                        return 0
        for y in range(16):
            r = sum(old_role in J[0][role] and y in ns[old_id]
                    for old_role, old_id in context)
            b = sum(old_role in J[1][role] and y in bs[old_id]
                    for old_role, old_id in context)
            allowed &= new_red[y][r] & new_blue[y][b]
            if not allowed:
                return 0
        return allowed

    edges_by_pattern = {
        'triangle': [(3,4),(3,5),(4,5)],
        'star': [(2,3),(2,4),(2,5)],
        'p4': [(2,3),(3,4),(4,5)],
        'p3k2': [(1,2),(1,3),(4,5)],
        '3k2': [(0,1),(2,3),(4,5)]}
    # All fifteen possible X edges, exactly three selected, classified
    # independently by their degree multisets. The proof supplies the
    # explicit isomorphism normalization for these five distinct signatures.
    signatures = {(0,0,0,2,2,2): 'triangle', (0,0,1,1,1,3): 'star',
                  (0,0,1,1,2,2): 'p4', (0,1,1,1,1,2): 'p3k2',
                  (1,1,1,1,1,1): '3k2'}
    placements = Counter()
    for edges in combinations(combinations(range(6),2),3):
        degree = Counter(v for edge in edges for v in edge)
        placements[signatures[tuple(sorted(degree[i] for i in range(6)))]] += 1
    expected = json.loads((HERE/'three_edges_expected.json').read_text())
    assert dict(placements) == expected['labeled_placements']
    assert sum(placements.values()) == 455
    results = []
    for pattern in edges_by_pattern:
        red = [set() for _ in range(6)]
        for a,b in edges_by_pattern[pattern]:
            red[a].add(b); red[b].add(a)
        J = (red,[set(range(6))-{i}-red[i] for i in range(6)])
        assert all(len(J[c][i]&J[c][j]) <= [3,6][c]
                   for c in range(2) for i in range(6) for j in J[c][i])
        assert all(J[1][i] & J[1][j] for i in range(6) for j in J[1][i])
        trace_path = Path(trace_directory)/f'{pattern}.trace'
        records, books, observed = {}, [], []
        for line in trace_path.read_text().splitlines():
            tag,*tokens=line.split(); values=list(map(int,tokens))
            if tag=='R':
                assert len(values)==1; observed.append(values[0])
            elif tag=='B':
                books.append(values)
            elif tag in 'TADEFGW':
                n=values[0]; ctx=tuple(zip(values[1:2*n+1:2],values[2:2*n+1:2]))
                count=values[2*n+1]; dom=values[2*n+2:]
                assert count==len(dom) and (tag,ctx) not in records
                records[tag,ctx]=dom
            else:
                raise AssertionError('bad trace tag')
        assert observed==masks
        leaf_sizes = Counter()
        def compare(tag,ctx,bits):
            key=tag,tuple((role,masks[i]) for role,i in ctx)
            assert records.pop(key)==[masks[i] for i in members(bits)],key
        def after(bits,i):
            return bits >> (i+1) << (i+1)
        stats={'complete':True,'pattern':pattern,'rows':m,
               'ordinary_pairs':0,'ordinary_triples':0,'first_domain_sum':0,
               'second_domain_sum':0,'max_first_domain':0,'max_second_domain':0,
               'qualifying_contexts':0,'prefix3_domains':0,'prefix4_domains':0,
               'prefix5_domains':0,'case_checks':0,'full_valid':0}
        if pattern in ['triangle','star','p4']:
            for e in range(m):
                for f in members(after(domain([(0,e)],1,J),e)):
                    stats['ordinary_pairs']+=1; os=[(0,e),(1,f)]
                    if pattern=='triangle':
                        for g in members(after(domain(os,2,J),f)):
                            stats['ordinary_triples']+=1; three=os+[(2,g)]
                            ends=domain(three,3,J,not_ten); compare('T',three,ends)
                            size=ends.bit_count(); stats['first_domain_sum']+=size
                            stats['max_first_domain']=max(stats['max_first_domain'],size)
                            # Transport is checked using independently computed domains.
                            for role in [4,5]:
                                assert domain(three,role,J,not_ten)==ends
                            if size<3: continue
                            stats['qualifying_contexts']+=1
                            for a,b,c in combinations(members(ends),3):
                                full_ctx=three+[(3,a),(4,b),(5,c)]
                                literal=first_book(core,{r:masks[i] for r,i in full_ctx},J)
                                assert literal is not None
                                stats['case_checks']+=1
                                expected_book=[masks[i] for _,i in full_ctx]+[literal[0],literal[1],literal[2]]+literal[3]
                                assert books.pop(0)==expected_book
                    else:
                        first=domain(os,2,J,not_ten if pattern=='star' else all_rows)
                        second=domain(os,3,J,not_ten if pattern=='p4' else all_rows)
                        compare('A',os,first);compare('D',os,second)
                        a_size=first.bit_count(); b_size=second.bit_count()
                        stats['first_domain_sum']+=a_size;stats['second_domain_sum']+=b_size
                        stats['max_first_domain']=max(stats['max_first_domain'],a_size)
                        stats['max_second_domain']=max(stats['max_second_domain'],b_size)
                        if pattern=='star' and b_size<3: continue
                        if pattern=='star' and first:stats['qualifying_contexts']+=1
                        for a in members(first):
                            c3=os+[(2,a)]
                            dom3=domain(c3,3,J,second);compare('E',c3,dom3)
                            if pattern=='star':leaf_sizes[str(dom3.bit_count())]+=1
                            stats['prefix3_domains']+=1
                            if pattern=='star' and dom3.bit_count()<3:continue
                            for b in members(dom3):
                                c4=c3+[(3,b)]
                                dom4=domain(c4,4,J,after(dom3,b) if pattern=='star' else second)
                                compare('F',c4,dom4);stats['prefix4_domains']+=1
                                for c in members(dom4):
                                    c5=c4+[(4,c)]
                                    dom5=domain(c5,5,J,after(dom4,c) if pattern=='star' else after(first,a))
                                    compare('G',c5,dom5);stats['prefix5_domains']+=1
                                    assert not dom5,'a complete candidate requires further research'
        elif pattern=='p3k2':
            for e in range(m):
                os=[(0,e)];leaves=domain(os,2,J)
                size=leaves.bit_count();stats['first_domain_sum']+=size;stats['max_first_domain']=max(stats['max_first_domain'],size)
                for a in members(leaves):
                    c2=os+[(2,a)];seconds=after(domain(c2,3,J,leaves),a)
                    stats['prefix3_domains']+=1;stats['second_domain_sum']+=seconds.bit_count()
                    for b in members(seconds):
                        c3=c2+[(3,b)];centers=domain(c3,1,J,not_ten)
                        compare('F',c3,centers);stats['prefix4_domains']+=1
                        for c in members(centers):
                            c4=c3+[(1,c)];endpoints=domain(c4,4,J)
                            stats['prefix5_domains']+=1
                            for d in members(endpoints):
                                c5=c4+[(4,d)];partners=after(domain(c5,5,J,endpoints),d)
                                stats['case_checks']+=1
                                assert not partners,'a complete candidate requires further research'
        else:
            for e in range(m):
                one=[(0,e)];partners=after(domain(one,1,J),e)
                size=partners.bit_count();stats['first_domain_sum']+=size;stats['max_first_domain']=max(stats['max_first_domain'],size)
                for f in members(partners):
                    c2=one+[(1,f)];seconds=after(domain(c2,2,J),e)
                    stats['prefix3_domains']+=1;stats['second_domain_sum']+=seconds.bit_count()
                    for a in members(seconds):
                        c3=c2+[(2,a)];thirds=after(domain(c3,3,J,seconds),a)
                        compare('F',c3,thirds);stats['prefix4_domains']+=1
                        for b in members(thirds):
                            c4=c3+[(3,b)];last=after(domain(c4,4,J,seconds),a)
                            stats['prefix5_domains']+=1
                            for c in members(last):
                                c5=c4+[(4,c)];finals=after(domain(c5,5,J,last),c)
                                stats['case_checks']+=1
                                assert not finals,'a complete candidate requires further research'
        assert not records and not books,'unverified trace records remain'
        assert stats == expected['patterns'][pattern]['counts']
        if pattern=='star':
            assert dict(leaf_sizes) == expected['patterns'][pattern]['center_leaf_domain_sizes']
        assert sha256(trace_path.read_bytes()).hexdigest() == expected['patterns'][pattern]['trace_sha256']
        results.append(stats)
    return results

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trace_directory')
    args = parser.parse_args()
    results = compute(args.trace_directory)
    print(json.dumps({'agent': 'six-books-2', 'role': 'researcher',
                      'complete': True, 'degree_or_edge_bounds_used': False,
                      'labeled_placements': 455, 'patterns': results},
                     indent=2, sort_keys=True))
