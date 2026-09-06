#!/usr/bin/env python3
"""Independent standard-library checker; imports no producer or SAT solver."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

DISTANCES = (1,2,7,10,12,13,14,16,18,20,21)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x, low, high):
    return type(x) is int and low <= x <= high


def monochromatic(matrix, q):
    c = matrix[q[0]][q[1]]
    return c if all(matrix[u][v] == c for u,v in it.combinations(q,2)) else None


def enumerate_models(clauses, n):
    """Complete binary branching with unit propagation, exact integer masks."""
    models, nodes = [], [0]
    def walk(cs, one, zero):
        nodes[0] += 1
        while True:
            positive = negative = 0
            reduced = []
            for a,b in cs:
                if a & one or b & zero:
                    continue
                a &= ~zero
                b &= ~one
                if not (a | b):
                    return
                if (a | b).bit_count() == 1:
                    positive |= a
                    negative |= b
                reduced.append((a,b))
            if positive & negative:
                return
            cs = reduced
            if not (positive | negative):
                break
            one |= positive
            zero |= negative
        if not cs:
            free = ((1 << n)-1) ^ one ^ zero
            sub = free
            while True:
                models.append(one | sub)
                if not sub:
                    break
                sub = (sub-1) & free
            return
        weights = {}
        for a,b in cs:
            mask = a | b
            weight = 1 << (8-min(8,mask.bit_count()))
            while mask:
                bit = mask & -mask
                mask ^= bit
                weights[bit] = weights.get(bit,0)+weight
        bit = max(weights, key=lambda b:(weights[b],-b))
        walk(cs, one | bit, zero)
        walk(cs, one, zero | bit)
    walk(clauses,0,0)
    return sorted(models), nodes[0]


def cyclic_covers():
    # Enumerate circular43-bit hitting words with nine1s and no five0s.
    # Start with bit0=1; all other covers are translations of these words.
    anchored = []
    def visit(word, ones, run):
        remaining = 43-len(word)
        ones_left = 9-ones
        if not 0 <= ones_left <= remaining:
            return
        if remaining-ones_left > 4*(ones_left+1)-run:
            return
        if not remaining:
            anchored.append(tuple(22*i % 43 for i,x in enumerate(word) if x))
            return
        if run < 4:
            visit(word+[0],ones,run+1)
        if ones < 9:
            visit(word+[1],ones+1,0)
    visit([1],1,0)
    covers = {tuple(sorted((v+a) % 43 for v in ds)) for ds in anchored for a in range(43)}
    return covers, len(anchored)


def literal_graph(obj):
    need(type(obj) is dict and set(obj) == {'n','red_edges','star_ids'}, 'witness fields')
    n = obj['n']
    need(integer(n,34,42), 'witness order')
    need(type(obj['red_edges']) is list, 'witness edge list')
    matrix, previous = [[0]*n for _ in range(n)], (-1,-1)
    for pair in obj['red_edges']:
        need(type(pair) is list and len(pair) == 2 and
             all(integer(v,0,n-1) for v in pair), 'witness edge labels')
        u,v = pair
        need(u < v and (u,v) > previous, 'witness canonical edges')
        matrix[u][v] = matrix[v][u] = 1
        previous = (u,v)
    return matrix


def verify(certificate):
    need(type(certificate) is dict and set(certificate) == {'schema','red_distances',
         'minimum_deletions','minimum_deletion_sets','dihedral_classes','records'}, 'certificate fields')
    need(integer(certificate['schema'],1,1) and certificate['red_distances'] == list(DISTANCES)
         and all(type(x) is int for x in certificate['red_distances']), 'seed definition')
    seed = [[int(a != b and min((a-b)%43,(b-a)%43) in DISTANCES)
             for b in range(43)] for a in range(43)]
    defects = [q for q in it.combinations(range(43),5) if monochromatic(seed,q) is not None]
    expected = {tuple(sorted(22*(a+j)%43 for j in range(5))) for a in range(43)}
    need(set(defects) == expected and len(defects) == 43, 'physical defect windows')
    need(all(monochromatic(seed,q) == 1 for q in defects), 'seed defect colors')
    need(all(sum(v in q for q in defects) == 5 for v in range(43)), 'incidence lower bound')
    covers, anchored = cyclic_covers()
    need(anchored == 45 and len(covers) == 215, 'complete minimum covers')
    need(all(all(set(ds) & set(q) for q in defects) for ds in covers), 'literal deletion cover')
    need(integer(certificate['minimum_deletions'],9,9) and integer(certificate['minimum_deletion_sets'],215,215),
         'cover claims')
    def orbit(ds):
        return {tuple(sorted((a+s*v)%43 for v in ds)) for a in range(43) for s in (-1,1)}
    representatives = sorted({min(orbit(ds)) for ds in covers})
    need(len(representatives) == 5 and integer(certificate['dihedral_classes'],5,5), 'dihedral count')
    need(all(seed[u][v] == seed[(a+s*u)%43][(a+s*v)%43]
             for a in range(43) for s in (-1,1) for u,v in it.combinations(range(43),2)),
         'seed symmetries')
    records = certificate['records']
    need(type(records) is list and len(records) == 5, 'five records required')
    summary, total_cohorts = [], 0
    for index,(rec,deleted) in enumerate(zip(records,representatives)):
        need(type(rec) is dict and set(rec) == {'class','deleted','stars','pair_cap',
             'maximum_added','terminal','maximal_witness'}, 'record fields')
        need(integer(rec['class'],index,index) and rec['deleted'] == list(deleted)
             and all(type(v) is int for v in rec['deleted']), 'representative alignment')
        old = [v for v in range(43) if v not in deleted]
        matrix = [[seed[u][v] for v in old] for u in old]
        clauses, fours = [], [0,0]
        for q in it.combinations(range(34),4):
            c = monochromatic(matrix,q)
            if c is not None:
                fours[c] += 1
                mask = sum(1 << v for v in q)
                clauses.append((mask,0) if c == 0 else (0,mask))
        stars = rec['stars']
        need(type(stars) is list and all(integer(s,0,(1 << 34)-1) for s in stars), 'star masks')
        need(stars == sorted(set(stars)), 'distinct sorted star list')
        models, nodes = enumerate_models(clauses,34)
        need(models == stars, 'incomplete or incorrect attachment domain')
        triples = [[],[]]
        for q in it.combinations(range(34),3):
            c = monochromatic(matrix,q)
            if c is not None:
                triples[c].append(sum(1 << v for v in q))
        n = len(stars)
        allowed = {}
        for a in range(n):
            for b in range(a,n):
                common = [((1 << 34)-1) ^ (stars[a] | stars[b]), stars[a] & stars[b]]
                colors = tuple(c for c in (0,1)
                               if not any(t & common[c] == t for t in triples[c]))
                if a == b:
                    need(not colors, 'duplicate star not excluded')
                elif colors:
                    allowed[a,b] = colors
        cap, maximum = rec['pair_cap'], rec['maximum_added']
        need(integer(cap,1,n) and integer(maximum,1,cap) and cap-maximum <= 1, 'capacity claims')
        cohorts_checked = 0
        for q in it.combinations(range(n),cap+1):
            need(not all(pair in allowed for pair in it.combinations(q,2)), 'pair upper bound false')
            cohorts_checked += 1
        total_cohorts += cohorts_checked
        terminals = rec['terminal']
        need(type(terminals) is list, 'terminal list')
        cases = {}
        for t in terminals:
            need(type(t) is dict and set(t) == {'star_ids','colors','five'}, 'terminal fields')
            need(type(t['star_ids']) is list and all(integer(s,0,n-1) for s in t['star_ids'])
                 and type(t['colors']) is list and all(integer(c,0,1) for c in t['colors']), 'terminal labels')
            key = (tuple(t['star_ids']),tuple(t['colors']))
            need(key not in cases, 'duplicate terminal')
            cases[key] = t['five']
        expected_cases = set()
        if maximum < cap:
            for chosen in it.combinations(range(n),cap):
                pairs = list(it.combinations(chosen,2))
                if not all(pair in allowed for pair in pairs):
                    continue
                for colors in it.product(*(allowed[pair] for pair in pairs)):
                    key = (chosen,colors)
                    expected_cases.add(key)
                    need(key in cases, 'uncovered terminal completion')
                    five = cases[key]
                    need(type(five) is dict and set(five) == {'vertices','color'}, 'five-set fields')
                    q,c = five['vertices'],five['color']
                    need(type(q) is list and len(q) == 5 and
                         all(integer(v,0,34+cap-1) for v in q) and q == sorted(set(q)), 'five-set labels')
                    need(integer(c,0,1), 'five-set color')
                    new_colors = dict(zip(it.combinations(range(cap),2),colors))
                    for u,v in it.combinations(q,2):
                        actual = (matrix[u][v] if v < 34 else
                                  (stars[chosen[v-34]] >> u & 1) if u < 34 else
                                  new_colors[u-34,v-34])
                        need(actual == c, 'terminal physical pair failure')
        need(set(cases) == expected_cases, 'extraneous terminal cases')
        witness = rec['maximal_witness']
        physical = literal_graph(witness)
        need(len(physical) == 34+maximum, 'lower witness order')
        chosen = witness['star_ids']
        need(type(chosen) is list and len(chosen) == maximum and
             all(integer(s,0,n-1) for s in chosen) and chosen == sorted(set(chosen)), 'witness star labels')
        need(all(physical[u][v] == matrix[u][v] for u,v in it.combinations(range(34),2)), 'witness core')
        need(all(physical[u][34+j] == (stars[s] >> u & 1)
                 for j,s in enumerate(chosen) for u in range(34)), 'witness attachments')
        need(all(monochromatic(physical,q) is None for q in it.combinations(range(len(physical)),5)),
             'lower witness has a monochromatic five-set')
        summary.append({'class':index,'deleted':list(deleted),'stars':n,'four_counts_blue_red':fours,
                        'dpll_nodes':nodes,'pair_compatible_edges':len(allowed),'pair_cap':cap,
                        'forbidden_cohorts_checked':cohorts_checked,'terminal_completions':len(cases),
                        'maximum_extension_order':len(physical)})
    return {'status':'VERIFIED_COMPLETE_MINIMUM_PUNCTURE_EXTENSION_SPECTRUM',
            'minimum_deletions':9,'minimum_deletion_sets':215,'dihedral_classes':5,
            'forbidden_cohorts_checked':total_cohorts,'records':summary,
            'ramsey43_constructed':False,'ramsey_bound_improved':False}


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
    result = verify(json.loads(path.read_text()))
    result['certificate_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(result,sort_keys=True,indent=2))
