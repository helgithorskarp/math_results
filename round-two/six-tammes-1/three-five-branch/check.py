#!/usr/bin/env python3
"""Necessary three-neighbor, link and original-alias checks.

Actual author six-tammes-1, researcher, 2026-10-01. Standard library only.
Not an enumeration of spherical maps. Written geometry is essential.
"""
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(records):
    raw = json.dumps(sorted(records), separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def canonical_face(face):
    variants = []
    for word in (tuple(face), tuple(reversed(face))):
        variants.extend(word[i:] + word[:i] for i in range(4))
    return min(variants)


def classify_neighbors(rows, ordinary, a, b, deficits):
    n = a + b + len(deficits)
    ns = list(map(set, rows))
    if any(len(ns[i] & ns[j]) > 2 for i, j in combinations(range(3), 2)):
        return 'COMMON_CONTACT', None
    inverse = {s: {i for i in range(3) if s in ns[i]} for s in range(n)}
    if any(len(inverse[s]) > 2 for s in range(a)) or any(
            len(inverse[a + b + j]) > d for j, d in enumerate(deficits)):
        return 'QQ_SUPPLY', None
    faces = set()
    for s in range(n):
        forces = s < a or (s >= a + b and deficits[s - a - b] == 2)
        if not forces or len(inverse[s]) != 2:
            continue
        i, j = sorted(inverse[s])
        other = (ns[i] & ns[j]) - {s}
        if len(other) != 1:
            return 'NO_SHARED_Q_OPPOSITE', None
        w = next(iter(other))
        faces.add(canonical_face((3 + s, i, 3 + w, j)))
    links = {s: set() for s in range(n)}
    for face in faces:
        for k in range(4):
            s = face[k] - 3
            if s >= 0:
                links[s].add(tuple(sorted((face[(k - 1) % 4], face[(k + 1) % 4]))))
    if any(len(edges) == 3 for edges in links.values()):
        return 'SEALED_LINK', None
    if (ordinary, a, b, deficits) == (2, 3, 1, (1,)):
        h = a + b
        singles = [s for s in range(a) if len(inverse[s]) == 1]
        require(len(inverse[h]) == 1 and len(inverse[a]) == 3 and len(singles) == 1,
                'Two-ordinary residual incidence differs')
        c_role = singles[0]
        u, w = next(iter(inverse[h])), next(iter(inverse[c_role]))
        require(u != w, 'H and C sole-U roles coincide')
        v = next(iter({0, 1, 2} - {u, w}))
        left = [s for s in range(a) if inverse[s] == {u, v}]
        right = [s for s in range(a) if inverse[s] == {v, w}]
        require(len(left) == len(right) == 1, 'Shared one-T roles differ')
        names = {left[0]: 3, right[0]: 4, c_role: 5, a: 6, h: 7}
        normal = ((3, 6, 7), (3, 4, 6), (4, 5, 6))
        tag = 'TWO_ORDINARY_NORMAL_FORM'
    elif (ordinary, a, b, deficits) == (1, 2, 1, (1, 1)):
        h1, h2 = a + b, a + b + 1
        require(len(inverse[h1]) == len(inverse[h2]) == 1 and len(inverse[a]) == 3,
                'One-ordinary residual incidence differs')
        u, w = next(iter(inverse[h1])), next(iter(inverse[h2]))
        require(u != w, 'Two deficient fives have the same sole U')
        v = next(iter({0, 1, 2} - {u, w}))
        left = [s for s in range(a) if inverse[s] == {u, v}]
        right = [s for s in range(a) if inverse[s] == {v, w}]
        require(len(left) == len(right) == 1, 'Two shared one-T roles differ')
        names = {left[0]: 3, right[0]: 4, a: 5, h1: 6, h2: 7}
        normal = ((3, 5, 6), (3, 4, 5), (4, 5, 7))
        tag = 'ONE_ORDINARY_NORMAL_FORM'
    else:
        raise ValueError('Unexpected surviving census')
    actual = tuple(tuple(sorted(names[s] for s in ns[i])) for i in (u, v, w))
    require(actual == normal, 'Original incidence normal form differs')
    return tag, actual


def neighbor_cover():
    profiles, all_raw = [], 0
    for ordinary in range(3):
        for f2 in range(4 - ordinary):
            f1 = 3 - ordinary - f2
            deficits = (1,) * f1 + (2,) * f2
            budget = 6 - sum(deficits)
            for b in range(budget // 2 + 1):
                a = budget - 2 * b
                triples = list(combinations(range(a + b + len(deficits)), 3))
                counts = Counter()
                full_records, admitted, terminal, terminal_rows = [], [], [], []
                for rows in product(triples, repeat=3):
                    tag, normal = classify_neighbors(rows, ordinary, a, b, deficits)
                    counts[tag] += 1
                    full_records.append((rows, tag))
                    if tag not in ('COMMON_CONTACT', 'QQ_SUPPLY'):
                        admitted.append((rows, tag))
                    if normal:
                        terminal.append(normal)
                        terminal_rows.append(rows)
                raw = len(triples) ** 3
                require(sum(counts.values()) == raw, 'Incomplete row-triple enumeration')
                all_raw += raw
                profiles.append({'ordinary_fives': ordinary, 'f1': f1, 'f2': f2,
                                 'a': a, 'b': b, 'ordinary_fours': 9 - a - b,
                                 'raw_ordered_three_neighbor_triples': raw,
                                 'classifications': dict(sorted(counts.items())),
                                 'full_row_records_sha256': digest(full_records),
                                 'admitted_records_sha256': digest(admitted),
                                 'terminal_rows_sha256': digest(terminal_rows),
                                 'terminal_normal_forms': sorted(set(terminal))})
    require(len(profiles) == 19 and all_raw == 30451, 'Full census domain changed')
    require(sum(p['classifications'].get('TWO_ORDINARY_NORMAL_FORM', 0)
                for p in profiles) == 36, 'Two-ordinary residual domain changed')
    require(sum(p['classifications'].get('ONE_ORDINARY_NORMAL_FORM', 0)
                for p in profiles) == 12, 'One-ordinary residual domain changed')
    return profiles


def original_alias_cover():
    # Actual original roles: U,V,W=0..2; A,D,C=3..5; B=6; H=7;
    # ordinary fives F,G=8,9; five ordinary fours=10..14.
    records, prefixes = [], []
    counts = Counter()
    for x in range(15):
        if x in (0, 1, 2, 6):
            tag = 'X_SELF_OR_OLD_B_NEIGHBOR'
        elif x in (3, 4):
            tag = 'X_CONTACT_Q_DIAGONAL'
        elif x in (5, 7):
            tag = 'X_REPEATED_Q_VERTEX'
        elif x in (8, 9):
            tag = 'X_FIVE_OPPOSITE_THREE'
        else:
            tag = 'X_ORDINARY_FOUR'
        counts[tag] += 1
        records.append(('X', x, -1, -1, -1, tag))
        if tag != 'X_ORDINARY_FOUR':
            continue
        for r in range(15):
            if r in (2, 4, 5):
                tag = 'R_REPEATED_Q_VERTEX'
            elif r == x:
                tag = 'R_REPEATED_ONE_T_LINK_CORNER'
            elif r in (0, 1):
                tag = 'R_EXTRA_C_THREE_CONTACT'
            elif r in (7, 8, 9):
                tag = 'R_FIVE_OPPOSITE_THREE'
            elif r in (3, 6):
                tag = 'R_DEFICIENT_QQ_DEBT'
            else:
                tag = 'R_ORDINARY_FOUR'
            counts[tag] += 1
            records.append(('R', x, r, -1, -1, tag))
            if tag != 'R_ORDINARY_FOUR':
                continue
            for p in range(15):
                if p in (x, 5, 6, 7):
                    tag = 'P_SELF_OR_OLD_X_NEIGHBOR'
                elif p not in (8, 9):
                    tag = 'P_THREE_TRIANGLES_AT_NONFIVE'
                else:
                    tag = 'P_ORDINARY_FIVE'
                counts[tag] += 1
                records.append(('P', x, r, p, -1, tag))
                if tag != 'P_ORDINARY_FIVE':
                    continue
                prefixes.append((x, r, p))
                for y in range(15):
                    face = (5, p, y, r)
                    if len(set(face)) != 4:
                        tag = 'Y_REPEATED_Q_VERTEX'
                    elif y in (2, x):
                        tag = 'Y_CONTACT_Q_DIAGONAL'
                    else:
                        tag = 'OPPOSITE_ORDINARY_FOUR_FIVE_CORNER'
                    counts[tag] += 1
                    records.append(('Y', x, r, p, y, tag))
    require(len(prefixes) == 40, 'Terminal original alias prefix count changed')
    require(counts['OPPOSITE_ORDINARY_FOUR_FIVE_CORNER'] == 400,
            'Final opposite-corner exclusion domain changed')
    require((10, 11, 8) in prefixes, 'Released terminal-role control missing')
    # Releasing only the last *role test* admits this necessary local prefix.
    # It is not a sphere packing or an angle assignment.
    control = {'x': 10, 'r': 11, 'p': 8, 'y': 12,
               'face': [5, 8, 12, 11]}
    return {'canonical_classifications': dict(sorted(counts.items())),
            'entrywise_sha256': digest(records),
            'prefixes': prefixes,
            'role_labeled_neighbor_normal_form_multiplicity': 36,
            'released_final_role_test_prefix_count': 400,
            'released_final_role_test_example': control}


def one_ordinary_alias_cover():
    # U,V,W=0..2; one-T A,D=3,4; zero-T B=5; three-T H1,H2=6,7;
    # the only ordinary five F=8; ordinary fours=9..14.
    counts, records, prefixes = Counter(), [], []
    for x in range(15):
        if x in (0, 1, 2, 5):
            tag = 'X_SELF_OR_OLD_B_NEIGHBOR'
        elif x in (3, 4):
            tag = 'X_CONTACT_Q_DIAGONAL'
        elif x in (6, 7):
            tag = 'X_REPEATED_Q_VERTEX'
        elif x == 8:
            tag = 'X_FIVE_OPPOSITE_THREE'
        else:
            tag = 'X_ORDINARY_FOUR'
        counts[tag] += 1
        records.append(('X', x, -1, -1, -1, tag))
        if tag != 'X_ORDINARY_FOUR':
            continue
        for p in range(15):
            if p in (x, 5, 6, 7):
                tag = 'P_SELF_OR_OLD_X_NEIGHBOR'
            elif p != 8:
                tag = 'P_AT_LEAST_THREE_T_AT_NONFIVE'
            else:
                tag = 'P_UNIQUE_ORDINARY_FIVE'
            counts[tag] += 1
            records.append(('P', x, p, -1, -1, tag))
        for k in range(15):
            if k == x or k < 9:
                tag = 'K_NOT_DISTINCT_ORDINARY_INTERNAL'
            else:
                tag = 'K_ORDINARY_FOUR'
            counts[tag] += 1
            records.append(('K', x, k, -1, -1, tag))
            if tag != 'K_ORDINARY_FOUR':
                continue
            for z in range(15):
                if z not in (3, 4, 5):
                    tag = 'Z_NOT_DEFICIENT_FOUR_OPPOSITE'
                else:
                    tag = 'Z_DEFICIENT_FOUR'
                counts[tag] += 1
                records.append(('Z', x, k, z, -1, tag))
                if tag != 'Z_DEFICIENT_FOUR':
                    continue
                for r in range(15):
                    if r in (0, 6, 8, x, k):
                        tag = 'R_REPEATED_H1_FAN_OR_CENTER'
                    elif r in (1, 2, 5):
                        tag = 'R_ZERO_T_FAN_ENDPOINT'
                    elif r == 7:
                        tag = 'R_FIVE_FIVE_Q_EDGE'
                    elif r == z:
                        tag = 'SEALED_K_DEGREE_FOUR_LINK'
                    else:
                        qq = {tuple(sorted((5, x))), tuple(sorted((k, z)))}
                        debt = sum(sum(d in e for e in qq) for d in (3, 4, 5))
                        require(len(qq) == 2 and debt == 2, 'K-Z/B-X debt collision')
                        require(debt > 8 - 7, 'Last non-three QQ-end capacity not exceeded')
                        tag = 'TWO_DISTINCT_QQ_ENDS_EXCEED_ONE'
                        prefixes.append((x, k, z, r))
                    counts[tag] += 1
                    records.append(('R', x, k, z, r, tag))
    require(len(prefixes) == 480, 'One-ordinary final alias count changed')
    return {'canonical_classifications': dict(sorted(counts.items())),
            'entrywise_sha256': digest(records),
            'final_QQ_prefixes_sha256': digest(prefixes),
            'role_labeled_neighbor_normal_form_multiplicity': 12,
            'released_non_three_D_four_QQ_capacity2_prefixes': len(prefixes),
            'released_capacity_example': [9, 10, 3, 4]}


def catalogue_corollary():
    fixture = json.loads(Path(__file__).with_name('PROFILE_CONTEXT.json').read_text())
    result = []
    for entry in fixture['catalogues']:
        rows = entry['profiles']
        for row in rows:
            f0, f1, f2 = row['five_counts_f0_f1_f2']
            require(f0+f1+f2 == row['r'] and row['a']+2*row['b']+f1+2*f2 == 6,
                    'Imported catalogue row identity differs')
            require(row['ordinary_fours'] == 15-2*row['r']-row['a']-row['b'],
                    'Imported ordinary-four count differs')
        remaining = [row for row in rows if row['r'] != 3]
        removed = [row for row in rows if row['r'] == 3]
        require(len(removed) == 11 and all(row['r'] == 2 for row in remaining),
                'Imported beta row domain differs')
        require(len(remaining) == (10 if entry['name'] == 'committed_21' else 7),
                'Catalogue consequence count differs')
        result.append({'name':entry['name'],'prior_source_commit':entry['source_commit'],
                       'prior_graph_ref':entry['graph_ref'],'prior_count':len(rows),
                       'removed_r3_rows':removed,'remaining_profiles':remaining,
                       'remaining_counts_r1_r2_r3':[0,len(remaining),0],
                       'prior_derivation_imported_not_regenerated':True})
    return result


def main():
    result = {'actual_agent': 'six-tammes-1', 'role': 'researcher',
              'scope': 'complete connected convex hemispherical T/Q15 contact graph,9Q,n5=3,1/2<c<3/5',
              'status': 'exact necessary incidences; written geometric bridges unformalized',
              'censuses': neighbor_cover(),
              'catalogue_corollaries': catalogue_corollary(),
              'two_ordinary_original_aliases': original_alias_cover(),
              'one_ordinary_original_aliases': one_ordinary_alias_cover(),
              'credited_full_interval_deficit_bound':
                  {'delta3_plus_4_distinct_positive_deficits_exceeds6': 3 + 4 > 6,
                   'delta4_plus_5_distinct_positive_deficits_exceeds6': 4 + 5 > 6},
              'full_global_Tammes15_bounds_unchanged': True}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
