"""Whole literal owner37 model; inputs retain original rows and point maps."""
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


class Guard(RuntimeError):
    pass


class Budget:
    def __init__(self, name):
        self.name, self.states, self.start = name, 0, time.monotonic()

    def tick(self, n=1):
        self.states += n
        if self.states > 100000 or time.monotonic() - self.start > 10:
            raise Guard('original100000-state/10s whole case: ' + self.name)

    def receipt(self):
        return {'case': self.name, 'states': self.states,
                'elapsed_seconds': time.monotonic() - self.start}


def load(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    need(data['actual_agent'] == 'six-code-1' and data['role'] == 'researcher', 'actual author/role')
    rows = data['owner_row_indices']
    need(rows == sorted(set(rows)) and rows, 'all original named rows distinct')
    need(data['source_root_orientations'] == [[13, 14], [14, 13]], 'both original Q4 rooted views')
    need(data['free_case_count_per_owner_orientation'] == 1296 and
         data['six_hole_bijections_per_free_case'] == 720, 'whole literal map domain')
    need(data['original_guards'] == {'states': 100000, 'case_seconds': 10, 'child_seconds': 60,
         'operational_timeout_seconds': 65, 'native_threads': 1, 'serial_CPU_intensive_jobs': 1},
         'unchanged original resource guards')
    return data, hashlib.sha256(raw).hexdigest()


def validate(data, budget):
    Q = data['whole_original_Q4_quadruples']
    need(len(Q) == len({tuple(q) for q in Q}) == 20 and
         all(len(set(q)) == 4 and set(q) <= set(range(17)) for q in Q), 'whole literal source Q20')
    for a, b in combinations(Q, 2):
        budget.tick()
        need(len(set(a) & set(b)) <= 1, 'original Q20 pair-simple')
    F = sorted(tuple(sorted(f)) for f in data['target_free_triples'])
    M = sorted(tuple(sorted(m)) for m in data['target_mate_triples'])
    need(len(F) == 3 and all(len(f) == 3 for f in F) and
         len(set().union(*(set(f) for f in F))) == 9, 'three disjoint whole free triples')
    need(len(M) == 5 and all(len(m) == 3 for m in M) and
         set().union(*(set(m) for m in M)) == set(range(15)), 'whole five mate triple partition')
    groups = {}
    rows = data['all_original_owner_rows']
    need([r['original_named_record_index'] for r in rows] == data['owner_row_indices'], 'entire declared owner list')
    for row in rows:
        values = row['original17_point_map']
        quads = row['whole_original20_quadruples']
        record = row['complete_original_decorated_owner_record']
        need(len(record) == 12 and record[7] == data['complete_original_colored_key'] and
             record[8] == values, 'whole original decorated row and point map')
        fixture, hubs, mate, roles = record[0]
        need(len(roles) == 5 and set(roles) == set(hubs) and
             [values[h] for h in roles] == list(range(5)) and
             values[record[1]] == 15 and values[mate] == 17,
             'all actual named Hub/free/mate roles')
        need(len(values) == 17 and sorted(values) == list(range(16)) + [17], 'whole original owner map')
        need(len(quads) == len({tuple(q) for q in quads}) == 20 and
             all(len(set(q)) == 4 and set(q) <= set(range(17)) for q in quads), 'all original owner quadruples')
        for a, b in combinations(quads, 2):
            budget.tick()
            need(len(set(a) & set(b)) <= 1, 'original whole owner pair-simple')
        star = sorted(tuple(sorted([16] + [values[p] for p in q])) for q in quads)
        need(len(star) == len(set(star)) == 20, 'whole owner star')
        for a, b in combinations(star, 2):
            budget.tick()
            need(len(set(a) & set(b)) <= 2, 'literal whole owner20 packing')
        actualF = sorted(tuple(sorted(set(w) - {15, 16})) for w in star if 15 in w)
        actualM = sorted(tuple(sorted(set(w) - {16, 17})) for w in star if 17 in w)
        need(actualF == F == sorted(tuple(sorted(f)) for f in record[10]) and
             actualM == M == sorted(tuple(sorted(m)) for m in record[9]), 'actual three free/five mate words')
        groups.setdefault(tuple(star), []).append(row['original_named_record_index'])
    owners = {min(indices): star for star, indices in groups.items()}
    actual_groups = sorted(sorted(indices) for indices in groups.values())
    need(actual_groups == data['literal_owner_groups'] and
         sorted(owners) == data['literal_distinct_owner_representatives'],
         'whole actual20 word equality is the only owner quotient')
    need(data['representative_whole_case_count'] == len(owners) * 2592 and
         data['all_original_owner_whole_case_count'] == len(rows) * 2592, 'whole rooted case coverage')
    for u, v in data['source_root_orientations']:
        tails = sorted(tuple(sorted(set(q) - {u})) for q in Q if u in q)
        need(len(tails) == 3 and all(v not in t for t in tails) and
             len(set().union(*(set(t) for t in tails))) == 9, 'three disjoint root-free triples')
    return owners


def source_cells(Q, u, v):
    cells = sorted(tuple(sorted(set(q) - {u})) for q in Q if u in q)
    holes = sorted(set(range(17)) - {u, v} - set().union(*(set(c) for c in cells)))
    need(len(holes) == 6, 'six source holes')
    return cells, holes


def literal37(Q, owner, image, u, v, budget):
    budget.tick()
    need(len(image) == 17 and sorted(image) == list(range(15)) + [16, 17], 'entire17 source image')
    need(image[u] == 16 and image[v] == 17, 'actual fixed original-root images')
    tstar = sorted(tuple(sorted([15] + [image[a] for a in q])) for q in Q)
    need(len(tstar) == len(set(tstar)) == 20, 'whole actual t-star')
    union = sorted(set(tstar) | set(owner))
    need(len(union) == 37 and len(set(tstar) & set(owner)) == 3, 'whole37 and all three xt overlaps')
    for a, b in combinations(union, 2):
        budget.tick()
        need(len(set(a) & set(b)) <= 2, 'all666 actual37 pairs')
    return {'point_map': list(image), 'whole37_union': [list(w) for w in union]}
