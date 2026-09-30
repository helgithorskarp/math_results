#!/usr/bin/env python3
"""Exact bookkeeping for TOPOLOGY.md; CPython >=3.11, standard library.

The planar realization, geometric reductions and connectedness arguments
are written hand proofs. This is not a spherical embedding enumerator.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, permutations, product
import json
import sys

import check as base
import check_boundary_patch as boundary
import check_two_zeros as previous


def star(degree, triangle_mask, zero_mask):
    """Sector i lies between contact edges i and (i+1) mod degree."""
    base.need(type(degree) is int and 3 <= degree <= 5, 'star degree')
    for mask in (triangle_mask, zero_mask):
        base.need(type(mask) is int and 0 <= mask < 1 << degree, 'star mask')
    T = tuple(bool(triangle_mask >> i & 1) for i in range(degree))
    Z = tuple(bool(zero_mask >> i & 1) for i in range(degree))
    base.need(not any(T[i] and (Z[i] or Z[(i+1) % degree])
                      for i in range(degree)), 'triangle cannot touch zero neighbor')
    Q = tuple(not t for t in T)
    base.need(any(Q), 'selected Q star is nonempty')
    qq = tuple(i for i in range(degree) if Q[i-1] and Q[i])
    free = tuple(i for i in range(degree)
                 if Q[i] and not Z[i] and not Z[(i+1) % degree])
    fans = 1 if all(Q) else sum(Q[i] and not Q[i-1] for i in range(degree))
    return {'Q_fans':fans,'QQ_edges':qq,'W_QQ_edges':tuple(i for i in qq if not Z[i]),
            'free_boundary_Q_sectors':free,'zero_neighbors':sum(Z),
            'triangle_sectors':sum(T),'Q_sectors':sum(Q)}


def enumerate_stars(degree, triangle_count):
    rows = []
    for tm in range(1 << degree):
        if tm.bit_count() != triangle_count:
            continue
        for zm in range(1 << degree):
            if any(tm >> i & 1 and (zm >> i & 1 or zm >> ((i+1) % degree) & 1)
                   for i in range(degree)):
                continue
            rows.append((tm,zm,star(degree,tm,zm)))
    return rows


def local_checks():
    D = enumerate_stars(4,1)
    R = enumerate_stars(4,2)
    F = enumerate_stars(5,4)
    Z3,Z4 = enumerate_stars(3,0),enumerate_stars(4,0)
    base.need([len(x) for x in (D,R,F,Z3,Z4)] == [16,10,5,8,16],
              'complete local mask census')
    for tm,zm,row in D:
        z = row['zero_neighbors']
        base.need(row['Q_fans'] == 1 and len(row['QQ_edges']) == 2
                  and z <= 2 and len(row['W_QQ_edges']) == 2-z,
                  'one-triangle-four local identities')
        base.need(len(row['free_boundary_Q_sectors']) == {0:3,1:1,2:0}[z],
                  'one-triangle-four Q sectors touching Z')
        if z == 1:
            edge, = row['W_QQ_edges']
            sides = {(edge-1) % 4,edge}
            base.need(len(sides & set(row['free_boundary_Q_sectors'])) == 1,
                      'one-Z D free sector shares QQ edge with Z sector')
    for tm,zm,row in R:
        z,s = row['zero_neighbors'],row['Q_fans']-1
        base.need(s in (0,1) and z <= 1 and not (z and s),
                  'ordinary-four capacity/splitting')
        base.need(len(row['QQ_edges']) == 1-s
                  and len(row['W_QQ_edges']) == 1-s-z,
                  'ordinary-four QQ edge counts')
        if z:
            base.need(not row['free_boundary_Q_sectors'], 'attached four Qs touch Z')
    base.need(all(row['Q_fans'] == 1 and not row['QQ_edges']
                  and row['zero_neighbors'] == 0 for _,_,row in F),
              'ordinary-five local identities')
    for degree,rows in ((3,Z3),(4,Z4)):
        base.need(all(row['Q_fans'] == 1 and len(row['QQ_edges']) == degree
                      for _,_,row in rows), 'full zero-triangle link')
    return {'one_triangle_four_masks':len(D),'ordinary_four_masks':len(R),
            'ordinary_five_masks':len(F),'zero_three_masks':len(Z3),
            'zero_four_masks':len(Z4),
            'D_mask_histogram_by_Z_neighbors':dict(sorted(Counter(
                row['zero_neighbors'] for _,_,row in D).items())),
            'ordinary_four_histogram_by_Z_neighbors_and_extra_Q_fans':{
                str(k):v for k,v in sorted(Counter(
                    (row['zero_neighbors'],row['Q_fans']-1) for _,_,row in R).items())},
            'one_Z_D_edge_connection_checked_on_every_local_mask':True}


def edges_of_faces(faces):
    edges = set()
    for face in faces:
        base.need(len(face) == 4 and len(set(face)) == 4, 'simple Q fixture boundary')
        edges.update(tuple(sorted((a,b))) for a,b in zip(face,face[1:]+face[:1]))
    return frozenset(edges)


def components(vertices,edges):
    remaining,parts = set(vertices),[]
    while remaining:
        todo,part = [min(remaining)],set()
        while todo:
            v = todo.pop()
            if v in part:
                continue
            part.add(v)
            todo.extend(b if a == v else a for a,b in edges if a == v or b == v)
        remaining.difference_update(part)
        parts.append(frozenset(part))
    return tuple(parts)


def gf2_rank(rows):
    pivots = {}
    for row in rows:
        base.need(type(row) is int and row >= 0, 'F2 row must be nonnegative integer')
        while row:
            pivot = row.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row ^= pivots[pivot]
    return len(pivots)


def fixture_data(faces):
    edges = sorted(edges_of_faces(faces))
    vertices = set(v for f in faces for v in f)
    positions = {edge:i for i,edge in enumerate(edges)}
    rows = []
    for f in faces:
        rows.append(sum(1 << positions[tuple(sorted((a,b)))]
                        for a,b in zip(f,f[1:]+f[:1])))
    face_edges = [edges_of_faces((f,)) for f in faces]
    adjacency = [(i,j) for i,j in combinations(range(len(faces)),2)
                 if face_edges[i] & face_edges[j]]
    K = len(components(vertices,edges))
    Kfaces = len(components(range(len(faces)),adjacency))
    return {'vertices':len(vertices),'edges':len(edges),'Q_faces':len(faces),
            'edge_graph_components':K,'edge_connected_face_components':Kfaces,
            'Euler_characteristic':len(vertices)-len(edges)+len(faces),
            'graph_cycle_rank':len(edges)-len(vertices)+K,
            'Q_boundary_rank_over_F2':gf2_rank(rows)}


def topology_fixtures():
    cube = ((0,1,2,3),(4,5,6,7),(0,4,5,1),(1,5,6,2),
            (2,6,7,3),(3,7,4,0))
    fixtures = {
        'two_Q_disk':((0,1,2,3),(1,4,5,2)),
        'four_Q_annulus':tuple((i,(i+1)%4,4+(i+1)%4,4+i) for i in range(4)),
        'pinched_two_disks_before_split':((0,1,2,3),(0,4,5,6)),
        'pinched_two_disks_after_split':((0,1,2,3),(7,4,5,6)),
        'five_cube_faces_disk':cube[:-1],
        'six_cube_faces_full_sphere':cube}
    out = {name:fixture_data(faces) for name,faces in fixtures.items()}
    expected = {
        'two_Q_disk':(6,7,2,1,1,1,2,2),
        'four_Q_annulus':(8,12,4,1,1,0,5,4),
        'pinched_two_disks_before_split':(7,8,2,1,2,1,2,2),
        'pinched_two_disks_after_split':(8,8,2,2,2,2,2,2),
        'five_cube_faces_disk':(8,12,5,1,1,1,5,5),
        'six_cube_faces_full_sphere':(8,12,6,1,1,2,5,5)}
    fields = ('vertices','edges','Q_faces','edge_graph_components',
              'edge_connected_face_components','Euler_characteristic',
              'graph_cycle_rank','Q_boundary_rank_over_F2')
    for name,data in out.items():
        base.need(tuple(data[k] for k in fields) == expected[name],
                  'entry-level topology fixture comparison')
    base.need(out['six_cube_faces_full_sphere']['Q_boundary_rank_over_F2'] == 5,
              'proper face selection is necessary for boundary independence')
    return out


@lru_cache(maxsize=None)
def QQ_graphs(degrees):
    """All simple graphs on the labeled vertices having positive QQ degrees."""
    base.need(all(type(d) is int and d > 0 for d in degrees), 'positive QQ degree list')
    pairs = tuple(combinations(range(len(degrees)),2))
    masks = []
    for mask in range(1 << len(pairs)):
        found = [0]*len(degrees)
        for i,(u,v) in enumerate(pairs):
            if mask >> i & 1:
                found[u] += 1
                found[v] += 1
        if tuple(found) == degrees:
            masks.append(mask)
    return tuple(masks)


def slot_allocations(p,r,e,cycle_four):
    a,m = 4-2*p,9-2*r+p
    b = 3*r+4*p-2*e
    cap = 1 if cycle_four else 2
    # A: attached adjacent Qs; J: unattached adjacent Qs; S: separated Qs.
    ordinary = {'A':(1,0,0),'J':(0,0,1),'S':(0,1,0)}
    checked = kept = odd = nongraphical = 0
    patterns = Counter()
    total_graphs = 0
    for Ds in product(range(cap+1),repeat=a):
        for Rs in product(ordinary,repeat=m):
            checked += 1
            if sum(Ds)+sum(ordinary[x][0] for x in Rs) != b:
                continue
            s = sum(ordinary[x][1] for x in Rs)
            stubs = tuple(2-z for z in Ds)+tuple(ordinary[x][2] for x in Rs)
            base.need(sum(stubs) == 17-5*r-7*p+2*e-s,
                      'QQ ends from slots match Z/W identity')
            if sum(stubs) % 2:
                odd += 1
                continue
            positive = tuple(d for d in stubs if d)
            graphs = QQ_graphs(positive)
            if not graphs:
                nongraphical += 1
                continue
            h = sum(stubs)//2
            QQ_from_Z = e+b+h
            QQ_from_vertices = (3*r+4*p+2*a+m-s)//2
            base.need(QQ_from_Z == QQ_from_vertices, 'independent global QQ count')
            V,E = 15+s,32-QQ_from_Z
            base.need(V-E+8 == (r+p+s-1)//2 and (r+p+s-1) % 2 == 0,
                      'normalized component identity')
            kept += 1
            total_graphs += len(graphs)
            patterns[(tuple(sorted(Ds)),tuple(sorted(Rs)),s,h,V,E)] += 1
    rows = [{'D_Z_degrees':list(Ds),'ordinary_four_states':list(Rs),
             'separated_ordinary_fours':s,'W_W_QQ_edges':h,
             'normalized_Q_vertices':V,'Q_edges':E,'Q_faces':8,
             'normalized_Euler_characteristic':V-E+8,
             'minimum_edge_connected_Q_components':V-E+8,
             'labeled_boundary_slot_allocations':count}
            for (Ds,Rs,s,h,V,E),count in sorted(patterns.items())]
    return {'p':p,'n3':r,'internal_Z_edges':e,'Z_W_edges':b,
            'C4_pair_obstruction_caps_each_D_at_one_Z_neighbor':cycle_four,
            'allocation_vectors_checked':checked,'retained_allocation_vectors':kept,
            'boundary_satisfying_vectors_rejected_by_odd_QQ_end_count':odd,
            'even_QQ_vectors_rejected_by_simple_graph_degree_check':nongraphical,
            'simple_QQ_graphs_across_retained_labeled_allocations':total_graphs,
            'necessary_patterns':rows}


def allocation_checks():
    inputs = ((1,4,5,False),(1,3,3,False),(1,3,4,True),
              (0,4,2,False),(0,4,3,False),(0,4,4,True))
    expected = (([2,2],['A','A'],0,0,15,21,1),
                ([2,2],['A','A','A','S'],1,0,16,22,4),
                ([1,1],['A','A','A','S'],1,1,16,22,4),
                ([2,2,2,2],['S'],1,0,16,22,1),
                ([1,1,2,2],['S'],1,1,16,22,6),
                ([1,1,1,1],['S'],1,2,16,22,1))
    out = []
    for args,wanted in zip(inputs,expected):
        row = slot_allocations(*args)
        base.need(len(row['necessary_patterns']) == 1, 'one retained slot pattern per case')
        p = row['necessary_patterns'][0]
        actual = tuple(p[k] for k in ('D_Z_degrees','ordinary_four_states',
                         'separated_ordinary_fours','W_W_QQ_edges',
                         'normalized_Q_vertices','Q_edges','labeled_boundary_slot_allocations'))
        base.need(actual == wanted, 'entry-level hand allocation table comparison')
        base.need(p['normalized_Euler_characteristic'] == 2,
                  'every excluded branch needs at least two Q components')
        out.append(row)
    base.need(sum(row['allocation_vectors_checked'] for row in out) == 1668,
              'complete boundary slot mask total')
    return out


def zero_graph_checks():
    pairs4 = tuple(combinations(range(4),2))
    buckets = {2:set(),3:set(),4:set()}
    for mask in range(1 << len(pairs4)):
        edges = frozenset(edge for i,edge in enumerate(pairs4) if mask >> i & 1)
        if len(edges) in buckets and boundary.zero_graph_allowed(4,edges):
            buckets[len(edges)].add(edges)
    templates = {2:(((0,1),(2,3)),((0,1),(1,2))),
                 3:(((0,1),(1,2),(2,3)),((0,1),(0,2),(0,3))),
                 4:(((0,1),(1,2),(2,3),(3,0)),)}
    for e in buckets:
        relabeled = {base.normalized_edges((p[u],p[v]) for u,v in edges)
                     for edges in templates[e] for p in permutations(range(4))}
        base.need(buckets[e] == relabeled, 'entry-level independent zero graph templates')
    base.need([len(buckets[e]) for e in (2,3,4)] == [15,16,3], 'four-Z graph census')
    counts = Counter()
    pair_vectors_checked = 0
    for edges in buckets[2]:
        neighbors = [{u for edge in edges if v in edge for u in edge if u != v}
                     for v in range(4)]
        options = [(u,v) for u,v in pairs4 if (u,v) not in edges
                   and len(neighbors[u] & neighbors[v]) < 2]
        parts = components(range(4),edges)
        kind = 'two_disjoint_edges' if sorted(map(len,parts)) == [2,2] else 'path_and_isolate'
        for choices in product(options,repeat=4):
            pair_vectors_checked += 1
            degrees = [sum(v in pair for pair in choices) for v in range(4)]
            if degrees != [3-len(neighbors[v]) for v in range(4)]:
                continue
            multiplicities = Counter(choices)
            if any(multiplicities[pair]+len(neighbors[pair[0]] & neighbors[pair[1]]) > 2
                   for pair in choices):
                continue
            # These extra pairs represent connecting two-Z Q sectors, not contact edges.
            base.need(len(components(range(4),edges | frozenset(choices))) == 1,
                      'D two-Z sectors connect both zero components')
            counts[kind] += 1
    base.need(pair_vectors_checked == 3840 and counts ==
              {'two_disjoint_edges':108,'path_and_isolate':288},
              'complete two-edge boundary pair audit')
    for edges in buckets[4]:
        neighbors = [{u for edge in edges if v in edge for u in edge if u != v}
                     for v in range(4)]
        base.need(all((u,v) in edges or len(neighbors[u] & neighbors[v]) == 2
                      for u,v in pairs4), 'every zero-C4 pair forbids a two-Z D')
    return {'four_vertex_masks_checked':64,
            'admitted_Z_graph_counts_by_edges':{str(e):len(buckets[e]) for e in buckets},
            'templates_compared_entry_by_entry':True,
            'two_edge_four_D_pair_vectors_checked':pair_vectors_checked,
            'retained_two_edge_four_D_pair_vectors':dict(sorted(counts.items())),
            'all_retained_two_edge_vectors_join_Z_components_by_Q_sectors':True,
            'C4_two_Z_D_pair_obstruction_checked_for_all_three_labeled_cycles':True,
            'mixed_r4_C5_or_C4_leaf_classification_is_the_unchanged_prior_lemma':True}


def retained_profile(p):
    return p['n3'] <= (2 if p['d42'] else 3)


def cover():
    old = previous.cover()
    retained = [deepcopy(p) for p in old['profiles'] if retained_profile(p)]
    removed = [deepcopy(p) for p in old['profiles'] if not retained_profile(p)]
    direct = []
    for row in old['distributions']:
        codes = row['allowed_H_codes']
        if not codes:
            continue
        for n3,n4,n5 in product(range(16),repeat=3):
            if (n3+n4+n5 == 15 and 3*n3+4*n4+5*n5 == 62
                    and n4 >= row['d41']+row['d42']
                    and n3 <= (2 if row['d42'] else 3)):
                direct.append({'d41':row['d41'],'d42':row['d42'],'d51':row['d51'],
                               'n3':n3,'n4':n4,'n5':n5,'H_codes':codes[:]})
    base.need(retained == direct, 'entry-level independent degree-sum cover')
    base.need([(p['d41'],p['d42'],p['n3']) for p in removed] ==
              [(2,1,3),(2,1,4),(4,0,4)], 'three newly excluded profiles')
    rows = deepcopy(old['distributions'])
    for row in rows:
        row['surviving_degree_profiles'] = sum(
            all(p[k] == row[k] for k in ('d41','d42','d51')) for p in retained)
    base.need(len(retained) == 7 and sum(len(row['allowed_H_codes']) for row in rows) == 11,
              'seven profiles and unchanged eleven H types')
    return {'previous_degree_profiles':10,'remaining_degree_profiles':7,
            'previous_colored_H_types':11,'remaining_colored_H_types':11,
            'remaining_deficit_distributions':2,'removed_profiles':removed,
            'distributions':rows,'profiles':retained,
            'restriction':'Mixed distribution n3<=2; four one-triangle fours n3<=3',
            'component_inequality':'(n3+d42+s-1)/2 <= K_Q',
            's':'ordinary fours with separated Q sectors',
            'K_Q':'components of Q faces joined through QQ edges'}


def selftest():
    controls = 0
    def test(value,message):
        nonlocal controls
        base.need(value,message)
        controls += 1
    for args in ((4,16,0),(4,True,0),(4,1,1),(2,0,0),(5,31,0)):
        try:
            star(*args)
        except ValueError:
            controls += 1
        else:
            raise ValueError('invalid or empty star accepted')
    test(star(4,1,12)['Q_fans'] == 1, 'two-Z D stays one fan')
    test(star(4,5,0)['Q_fans'] == 2, 'separated Qs require two copies')
    test(not QQ_graphs((2,)), 'isolated two-QQ-end vertex rejected')
    test(not QQ_graphs((1,)), 'odd QQ-end vertex rejected')
    test(QQ_graphs((1,1)) == (1,), 'one QQ edge retained')
    test(len(QQ_graphs((1,1,1,1))) == 3, 'three labeled four-D matchings')
    test(gf2_rank((3,5,6)) == 2, 'dependent F2 cycle rows')
    test(gf2_rank((1,2,4)) == 3, 'independent F2 cycle rows')
    before = fixture_data(((0,1,2,3),(0,4,5,6)))
    after = fixture_data(((0,1,2,3),(7,4,5,6)))
    test(before['edge_graph_components'] == 1
         and before['edge_connected_face_components'] == 2,
         'unsplit point connection is insufficient')
    test(after['edge_graph_components'] == 2
         and after['edge_connected_face_components'] == 2,
         'split removes only the point connection')
    test(not retained_profile({'d42':1,'n3':3}), 'mixed three removed')
    test(retained_profile({'d42':1,'n3':2}), 'mixed two retained')
    test(not retained_profile({'d42':0,'n3':4}), 'all-four four removed')
    test(retained_profile({'d42':0,'n3':3}), 'all-four three retained')
    return controls


def main():
    base.need(sys.argv[1:] in ([],['--selftest']), 'usage: check_topology.py [--selftest]')
    local,fixtures,allocations,zeros,remaining = (local_checks(),topology_fixtures(),
                                               allocation_checks(),zero_graph_checks(),cover())
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(),
                          'degree_profiles':7,'colored_H_types':11,
                          'boundary_allocation_vectors':1668},sort_keys=True))
    else:
        print(json.dumps({'agent':'six-tammes-1','role':'researcher',
                          'scope':'exact local/planar bookkeeping; written geometric and topological bridges separate',
                          'local_star_checks':local,'topology_fixtures':fixtures,
                          'boundary_allocations':allocations,'zero_graph_checks':zeros,
                          'cover':remaining},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
