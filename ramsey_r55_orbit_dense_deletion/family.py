#!/usr/bin/env python3
"""Two completely specified physical 43-vertex deletion families."""
from itertools import combinations
from math import comb


def need(ok, message):
    if not ok:
        raise ValueError(message)


def two_orbit_index(u, v):
    need(0 <= u < v < 53, 'template edge')
    if v == 52:
        return 52 + (u // 26)
    if u // 26 == v // 26:
        d = min(v-u, 26-(v-u))
        return 13*(u//26)+d-1
    return 26+(v-26-u) % 26


def two_orbit(word, deleted_a, deleted_b):
    need(type(word) is int and 0 <= word < 1 << 54, '54-bit word')
    for deletion in (deleted_a, deleted_b):
        need(len(deletion) == 5 and len(set(deletion)) == 5 and
             all(type(x) is int and 0 <= x < 26 for x in deletion), 'five deleted positions')
    deleted = set(deleted_a) | {26+x for x in deleted_b}
    return {'n': 53, 'red_edges': [[u,v] for u,v in combinations(range(53),2)
                                  if word >> two_orbit_index(u,v) & 1],
            'generators': [[(v//26)*26+(v+1)%26 if v < 52 else 52 for v in range(53)]],
            'selected': [v for v in range(53) if v not in deleted]}


def paley53(deleted):
    need(len(deleted) == 10 and len(set(deleted)) == 10 and
         all(type(x) is int and 0 <= x < 53 for x in deleted), 'ten deleted positions')
    residues = {x*x % 53 for x in range(1,53)}
    return {'n': 53, 'red_edges': [[u,v] for u,v in combinations(range(53),2)
                                  if (v-u) % 53 in residues],
            'generators': [[(v+1) % 53 for v in range(53)]],
            'selected': [v for v in range(53) if v not in set(deleted)]}


def instantiate(row):
    if row['family'] == 'paley53':
        return paley53(row['deleted'])
    need(row['family'] == 'two_orbit53', 'fixture family')
    return two_orbit(row['word'], row['deleted_a'], row['deleted_b'])


def inventory():
    return {'paley53': {'ambient_order': 53, 'deleted': 10,
                        'physical_subset_jobs': comb(53,10), 'surviving_good43_jobs': 0},
            'two_orbit53': {'ambient_order': 53, 'ambient_edge_orbit_bits': 54,
                            'deletion_pairs': comb(26,5)**2,
                            'physical_parameter_jobs': (1 << 54)*comb(26,5)**2,
                            'surviving_good43_jobs': 0,
                            'count_convention': 'parameter jobs; resulting labeled or unlabeled graphs can coincide'},
            'not_multiplied_by_h3887': True, 'whole_q10_task_decided': False,
            'target43_found': False}
