#!/usr/bin/env python3
"""Complementary same-author bit-incidence and cyclic-link audit.

Imports no primary code. The continuous geometry and raw-to-local coverage
remain written proof, not an independent researcher verdict.
Actual author six-tammes-1, researcher, 2026-10-01.
"""
from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path


def ensure(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def checksum(entries):
    return hashlib.sha256(json.dumps(sorted(entries), separators=(',', ':')).encode()).hexdigest()


def cyclic_link_completion(known, degree, required):
    # Local unnamed slots are distinct remaining actual neighbors, not new
    # code points. Only U-neighbor corners are fixed at this stage.
    vertices = sorted(known) + list(range(3, 3 + degree - len(known)))
    ensure(len(set(vertices)) == degree, 'Link slot collision')
    if not vertices:
        return False
    start, rest = vertices[0], vertices[1:]
    for tail in permutations(rest):
        word = (start,) + tail
        edges = {frozenset((word[i], word[(i + 1) % degree]))
                 for i in range(degree)}
        if required <= edges:
            return True
    return False


def incidence_cover():
    # Literal full census, independent of the primary census generator.
    census = ((0,3,0,3,0),(0,3,0,1,1),(0,2,1,2,0),(0,2,1,0,1),
              (0,1,2,1,0),(0,0,3,0,0),
              (1,2,0,4,0),(1,2,0,2,1),(1,2,0,0,2),
              (1,1,1,3,0),(1,1,1,1,1),(1,0,2,2,0),(1,0,2,0,1),
              (2,1,0,5,0),(2,1,0,3,1),(2,1,0,1,2),
              (2,0,1,4,0),(2,0,1,2,1),(2,0,1,0,2))
    summaries = []
    for ordinary, f1, f2, a, b in census:
        ensure(ordinary+f1+f2 == 3 and a+2*b+f1+2*f2 == 6, 'Census identity differs')
        deficits = [1]*f1 + [2]*f2
        caps = [2]*a + [3]*b + deficits
        choices = [[mask for mask in range(8) if mask.bit_count() <= cap]
                   for cap in caps]
        entries, terminals = [], []
        counts = Counter()
        column_words = 0
        for columns in product(*choices):
            column_words += 1
            row_bits = [sum(1 << q for q, mask in enumerate(columns)
                            if mask & (1 << u)) for u in range(3)]
            if any(row.bit_count() != 3 for row in row_bits):
                continue
            if any((row_bits[u] & row_bits[v]).bit_count() > 2
                   for u, v in combinations(range(3), 2)):
                continue
            rows = tuple(tuple(q for q in range(len(columns)) if row & (1 << q))
                         for row in row_bits)
            requirements = [set() for _ in columns]
            missing = False
            for q, mask in enumerate(columns):
                paired = q < a or (q >= a+b and deficits[q-a-b] == 2)
                if mask.bit_count() != 2 or not paired:
                    continue
                us = [u for u in range(3) if mask & (1 << u)]
                other = (row_bits[us[0]] & row_bits[us[1]]) & ~(1 << q)
                if other.bit_count() != 1:
                    missing = True
                    break
                opposite = other.bit_length()-1
                requirements[q].add(frozenset(us))
                requirements[opposite].add(frozenset(us))
            if missing:
                tag = 'NO_SHARED_Q_OPPOSITE'
            elif any(not cyclic_link_completion(
                    {u for u in range(3) if mask & (1 << u)},
                    4 if q < a+b else 5, requirements[q])
                    for q, mask in enumerate(columns)):
                tag = 'SEALED_LINK'
            else:
                if (ordinary,a,b,deficits) == (2,3,1,[1]):
                    tag = 'TWO_ORDINARY_NORMAL_FORM'
                elif (ordinary,a,b,deficits) == (1,2,1,[1,1]):
                    tag = 'ONE_ORDINARY_NORMAL_FORM'
                else:
                    raise RuntimeError('Unexpected residual incidence')
                terminals.append(rows)
            counts[tag] += 1
            entries.append((rows,tag))
        summaries.append({'ordinary_fives':ordinary,'f1':f1,'f2':f2,'a':a,'b':b,
                          'raw_supplier_subset_words':column_words,
                          'admitted_classifications':dict(sorted(counts.items())),
                          'admitted_records_sha256':checksum(entries),
                          'terminal_rows_sha256':checksum(terminals),
                          'terminal_rows':sorted(terminals)})
    ensure(sum(len(x['terminal_rows']) for x in summaries) == 48,
           'Full residual incidence domain differs')
    return summaries


def four_cycles(neighbors, corners):
    neighbors = set(neighbors)
    ensure(len(neighbors) == 4, 'Not four distinct original contacts')
    first = min(neighbors)
    words = []
    for tail in permutations(sorted(neighbors - {first})):
        word = (first,) + tail
        edges = {frozenset((word[i], word[(i + 1) % 4])) for i in range(4)}
        if set(corners) <= edges:
            words.append((word, edges))
    return words


def p_quota_cover(x, relax_ordinary=False):
    # Every M,K assignment is to the original fifteen points. No extra point
    # is used to represent a full consecutive three-T H fan.
    ceiling = [0, 0, 0, 1, 1, 1, 0, 3, 4, 4, 2, 2, 2, 2, 2]
    allowed, records = set(), []
    for p, m, k in product(range(15), repeat=3):
        fan = (x, p, m, k, 0)
        if len(set(fan)) != 5 or 7 in fan or p in (5, 6, 7, x):
            continue
        triangles = {tuple(sorted((7, fan[j], fan[j + 1]))) for j in range(3)}
        triangles.add(tuple(sorted((5, x, p))))
        incidence = Counter(v for tri in triangles for v in tri)
        ensure(incidence[p] == 3, 'P three-distinct-T bridge failed')
        bounds = ceiling[:]
        if relax_ordinary and p >= 10:
            bounds[p] = 3
        valid = all(incidence[v] <= bounds[v] for v in incidence)
        records.append((p, m, k, valid))
        if valid:
            allowed.add(p)
    if not relax_ordinary:
        ensure(allowed == {8, 9}, 'Full H-fan quota audit differs')
    else:
        ensure(any(p >= 10 for p in allowed), 'Released P quota control empty')
    return allowed, {'x': x, 'proper_original_H_fan_assignments': len(records),
                     'entrywise_sha256': checksum(records),
                     'allowed_P_originals': sorted(allowed)}


def terminal_cover():
    ceiling = [0, 0, 0, 1, 1, 1, 0, 3, 4, 4, 2, 2, 2, 2, 2]
    deficient = {3, 4, 5, 6}
    records, prefixes, quota = [], [], []
    counts = Counter()
    for x in range(15):
        if x in {0, 1, 2, 6}:
            tag = 'X_SELF_OR_OLD_B_NEIGHBOR'
        elif frozenset((6, x)) in {frozenset((6, 3)), frozenset((6, 4))}:
            tag = 'X_CONTACT_Q_DIAGONAL'
        elif any(len(set(q)) != 4 for q in [(6, 0, 7, x), (6, 2, 5, x)]):
            tag = 'X_REPEATED_Q_VERTEX'
        elif ceiling[x] == 4:
            tag = 'X_FIVE_OPPOSITE_THREE'
        else:
            tag = 'X_ORDINARY_FOUR'
        counts[tag] += 1
        records.append(('X', x, -1, -1, -1, tag))
        if tag != 'X_ORDINARY_FOUR':
            continue
        p_allowed, qr = p_quota_cover(x)
        quota.append(qr)
        for r in range(15):
            quad = (2, 4, r, 5)
            if len(set(quad)) < 4:
                tag = 'R_REPEATED_Q_VERTEX'
            elif frozenset((2, r)) == frozenset((2, x)):
                tag = 'R_REPEATED_ONE_T_LINK_CORNER'
            elif ceiling[r] == 0 and r != 6:
                tag = 'R_EXTRA_C_THREE_CONTACT'
            elif ceiling[r] >= 3:
                tag = 'R_FIVE_OPPOSITE_THREE'
            elif r in deficient:
                qq = {frozenset((6, x)), frozenset((5, r))}
                debt = sum(sum(v in edge for edge in qq) for v in deficient)
                ensure(debt > 2, 'Deficient R incidence debt not excluded')
                tag = 'R_DEFICIENT_QQ_DEBT'
            else:
                tag = 'R_ORDINARY_FOUR'
            counts[tag] += 1
            records.append(('R', x, r, -1, -1, tag))
            if tag != 'R_ORDINARY_FOUR':
                continue
            for p in range(15):
                if p in {x, 5, 6, 7}:
                    tag = 'P_SELF_OR_OLD_X_NEIGHBOR'
                elif p not in p_allowed:
                    tag = 'P_THREE_TRIANGLES_AT_NONFIVE'
                else:
                    cycles = four_cycles({2, x, r, p},
                              {frozenset((2, x)), frozenset((2, r)), frozenset((x, p))})
                    ensure(cycles and all(frozenset((r, p)) in edges for _, edges in cycles),
                           'Full C link did not force R-P Q corner')
                    tag = 'P_ORDINARY_FIVE'
                counts[tag] += 1
                records.append(('P', x, r, p, -1, tag))
                if tag != 'P_ORDINARY_FIVE':
                    continue
                prefixes.append((x, r, p))
                for y in range(15):
                    face = (5, p, y, r)
                    if len(set(face)) < 4:
                        tag = 'Y_REPEATED_Q_VERTEX'
                    elif y in ({2, x, r, p} - {r, p}):
                        tag = 'Y_CONTACT_Q_DIAGONAL'
                    else:
                        ensure(ceiling[r] == 2 and ceiling[p] == 4,
                               'Final Q opposite roles differ')
                        tag = 'OPPOSITE_ORDINARY_FOUR_FIVE_CORNER'
                    counts[tag] += 1
                    records.append(('Y', x, r, p, y, tag))
    ensure(len(prefixes) == 40, 'Final incidence prefixes differ')
    released, control = p_quota_cover(10, relax_ordinary=True)
    return {'canonical_classifications': dict(sorted(counts.items())),
            'entrywise_sha256': checksum(records), 'prefixes': prefixes,
            'full_original_H_fan_quota_audits': quota,
            'released_ordinary_P_ceiling3_control': control,
            'released_final_role_test_prefix_count': counts['OPPOSITE_ORDINARY_FOUR_FIVE_CORNER']}


def two_fan_P_quota(x):
    ceiling = [0, 0, 0, 1, 1, 0, 3, 3, 4] + [2] * 6
    possible, records = set(), []
    for p, m1, m2 in product(range(15), repeat=3):
        if p in (x, 5, 6, 7):
            continue
        left, right = (x, p, m1, 0), (x, p, m2, 2)
        if len(set(left)) != 4 or len(set(right)) != 4 or 6 in left or 7 in right:
            continue
        triangles = {tuple(sorted(t)) for t in
                     [(6, x, p), (6, p, m1), (7, x, p), (7, p, m2)]}
        incidence = Counter(v for tri in triangles for v in tri)
        ensure(incidence[p] >= 3, 'Two internal fans gave fewer than three Ts')
        valid = all(incidence[v] <= ceiling[v] for v in incidence)
        records.append((p, m1, m2, valid))
        if valid:
            possible.add(p)
    ensure(possible == {8}, 'Two-fan P quota cover differs')
    return possible, {'x': x, 'proper_original_partial_fan_assignments': len(records),
                      'entrywise_sha256': checksum(records), 'allowed_P_originals': sorted(possible)}


def five_fan_alignment():
    words = []
    for word in permutations(('K', 'H1', 'X', 'H2', 'L')):
        j = word.index('X')
        if j not in (1, 2, 3) or {word[j-1], word[j+1]} != {'H1', 'H2'}:
            continue
        if word.index('H1') not in (1, 2, 3) or word.index('H2') not in (1, 2, 3):
            continue
        words.append(word)
    ensure(len(words) == 4, 'Complete five-fan alignment cover differs')
    return sorted(words)


def one_ordinary_terminal_cover():
    ceiling = [0, 0, 0, 1, 1, 0, 3, 3, 4] + [2] * 6
    counts, records, prefixes, quota = Counter(), [], [], []
    for x in range(15):
        if x in (0, 1, 2, 5):
            tag = 'X_SELF_OR_OLD_B_NEIGHBOR'
        elif frozenset((5, x)) in {frozenset((5, 3)), frozenset((5, 4))}:
            tag = 'X_CONTACT_Q_DIAGONAL'
        elif any(len(set(q)) < 4 for q in [(5, 0, 6, x), (5, 2, 7, x)]):
            tag = 'X_REPEATED_Q_VERTEX'
        elif ceiling[x] >= 3:
            tag = 'X_FIVE_OPPOSITE_THREE'
        else:
            tag = 'X_ORDINARY_FOUR'
        counts[tag] += 1
        records.append(('X', x, -1, -1, -1, tag))
        if tag != 'X_ORDINARY_FOUR':
            continue
        possible_p, details = two_fan_P_quota(x)
        quota.append(details)
        for p in range(15):
            if p in {x, 5, 6, 7}:
                tag = 'P_SELF_OR_OLD_X_NEIGHBOR'
            elif p not in possible_p:
                tag = 'P_AT_LEAST_THREE_T_AT_NONFIVE'
            else:
                tag = 'P_UNIQUE_ORDINARY_FIVE'
            counts[tag] += 1
            records.append(('P', x, p, -1, -1, tag))
        for k in range(15):
            if k == x or ceiling[k] != 2:
                tag = 'K_NOT_DISTINCT_ORDINARY_INTERNAL'
            else:
                tag = 'K_ORDINARY_FOUR'
            counts[tag] += 1
            records.append(('K', x, k, -1, -1, tag))
            if tag != 'K_ORDINARY_FOUR':
                continue
            for z in range(15):
                if z not in {3, 4, 5}:
                    tag = 'Z_NOT_DEFICIENT_FOUR_OPPOSITE'
                else:
                    tag = 'Z_DEFICIENT_FOUR'
                counts[tag] += 1
                records.append(('Z', x, k, z, -1, tag))
                if tag != 'Z_DEFICIENT_FOUR':
                    continue
                for r in range(15):
                    if len({x, 8, k, r, 0}) != 5 or r == 6:
                        tag = 'R_REPEATED_H1_FAN_OR_CENTER'
                    elif ceiling[r] == 0:
                        tag = 'R_ZERO_T_FAN_ENDPOINT'
                    elif r == 7:
                        tag = 'R_FIVE_FIVE_Q_EDGE'
                    elif r == z:
                        required = {frozenset((8, 6)), frozenset((6, r)), frozenset((8, z))}
                        for fourth in set(range(15)) - {8, 6, r, k}:
                            ensure(not four_cycles({8, 6, r, fourth}, required),
                                   'Sealed K link completed with an original fourth point')
                        tag = 'SEALED_K_DEGREE_FOUR_LINK'
                    else:
                        cycles = four_cycles({8, 6, r, z},
                                 {frozenset((8, 6)), frozenset((6, r)), frozenset((8, z))})
                        ensure(cycles and all(frozenset((r, z)) in edges for _, edges in cycles),
                               'Last K sector not forced')
                        binary = [0] * 15
                        for u, v in ((5, x), (k, z)):
                            binary[u] |= 1 << v
                            binary[v] |= 1 << u
                        ends = sum(binary[v].bit_count() for v in (3, 4, 5))
                        ensure(ends == 2 and ends > 1, 'B-X/K-Z QQ debt not excluded')
                        tag = 'TWO_DISTINCT_QQ_ENDS_EXCEED_ONE'
                        prefixes.append((x, k, z, r))
                    counts[tag] += 1
                    records.append(('R', x, k, z, r, tag))
    ensure(len(prefixes) == 480, 'Final one-ordinary alias domain differs')
    return {'canonical_classifications': dict(sorted(counts.items())),
            'entrywise_sha256': checksum(records),
            'final_QQ_prefixes_sha256': checksum(prefixes),
            'two_original_fan_quota_audits': quota,
            'full_F_fan_alignment_words': five_fan_alignment(),
            'released_non_three_D_four_QQ_capacity2_prefixes': len(prefixes)}


def imported_census_audit():
    fixture = json.loads(Path(__file__).with_name('PROFILE_CONTEXT.json').read_text())
    results = []
    for entry in fixture['catalogues']:
        rows = entry['profiles']
        grouped = {r:[] for r in (1,2,3)}
        for row in rows:
            grouped[row['r']].append(row)
        ensure(len(grouped[3]) == 11 and not grouped[1], 'Imported degree domains differ')
        results.append({'name':entry['name'],'remaining_profiles':grouped[2],
                        'removed_r3_rows':grouped[3],
                        'remaining_counts_r1_r2_r3':[0,len(grouped[2]),0],
                        'prior_derivation_imported_not_regenerated':True})
    return results


def main():
    print(json.dumps({'actual_agent': 'six-tammes-1', 'role': 'researcher',
                      'trust': 'same-author bit-incidence/link audit; written geometry unformalized',
                      'censuses': incidence_cover(),
                      'catalogue_corollaries': imported_census_audit(),
                      'two_ordinary_original_aliases': terminal_cover(),
                      'one_ordinary_original_aliases': one_ordinary_terminal_cover()}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
