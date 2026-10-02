"""Reviewer-owned complete record. Does not import author executables or data."""
import hashlib
import json
from collections import Counter
from itertools import combinations
from core import (X, RANK, frame, degrees, fixed_pairs, all_columns,
                  role_columns, permutation, transported_word,
                  endpoint_inventory, require)
from separation import TABLE, TARGET, sums, discover, relaxed_certificates


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def run():
    own = frame()
    columns = all_columns(own)
    roles = role_columns(columns)
    domains = {k: sorted(set(tuple(c['missing']) for c in cs)) for k, cs in roles.items()}
    for k in TABLE:
        require(domains[k] == sorted(TABLE[k]), 'ordinary table: ' + k)
    literal = []
    for r in (0, 1):
        for s in (0, 1):
            adj = frame(r, s)
            p = permutation(r, s)
            require([{p[j] for j in row} for row in own] == [adj[p[i]] for i in range(16)],
                    'all prescribed edges transport')
            require(all(degrees(own)[i] == degrees(adj)[p[i]] for i in range(16)),
                    'all actual degrees transport')
            require(all(RANK[i] == RANK[p[i]] for i in range(16)), 'all ranks transport')
            cs = all_columns(adj)
            require(sorted(transported_word(c['word'], p) for c in columns)
                    == sorted(c['word'] for c in cs), 'every column transport')
            relaxed = all_columns(adj, blue_minimum=False)
            require(cs == relaxed, 'entire blue-minimum relaxation domain')
            literal.append({'r': r, 'sy_swap': s, 'adjacency': [sorted(a) for a in adj],
                            'degrees': list(degrees(adj)), 'ranks': list(RANK),
                            'fixed_pairs': fixed_pairs(adj), 'columns': cs,
                            'without_blue_internal_minimum': relaxed})
    endpoints = endpoint_inventory()
    require(Counter(e['case'] for e in endpoints) == {'U': 180, 'V': 360},
            'full actual endpoint coverage')
    q = sums()
    require(all(v['hits'] == 0 for v in q.values()), 'missing row target reached')
    certificates = discover()
    relaxed = relaxed_certificates()
    core = {'literal': literal, 'roles': roles, 'domains': {k: list(map(list,v)) for k,v in domains.items()},
            'endpoint_inventory': endpoints, 'missing_sums': q, 'separators': certificates,
            'relaxed_fractional_separators': relaxed}
    return {'actual_agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'core': core, 'core_sha256': sha(core),
            'summary': {'column_counts': [len(x['columns']) for x in literal],
                        'blue_relaxed_column_counts': [len(x['without_blue_internal_minimum']) for x in literal],
                        'role_counts': {k: len(v) for k,v in roles.items()},
                        'endpoint_counts': dict(Counter(e['case'] for e in endpoints)),
                        'missing_tuple_counts': {k: v['count'] for k,v in q.items()},
                        'separators': certificates,
                        'relaxed_sizes': {k:v['sizes'] for k,v in relaxed.items()}}}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, separators=(',', ':')))
