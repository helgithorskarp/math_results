#!/usr/bin/env python3
"""Independent Book root-defect-eight audit with relaxed reciprocal domains."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import time

from incidence import (COORDS, DELTA, EXAMPLES, FEATURES, SUPPORTS, digest,
                       incidences, need, root_canonical, root_census,
                       root_matrix, specification)
from reference import formula_domains, replay_rounds
from spines import all_domains, reciprocal


def controls():
    # All two-row multisets in the entire nonnegative-surplus binary domain.
    words = [w for w in range(64) if DELTA[w] >= 0]
    brute = defaultdict(list)
    for first, second in combinations_with_replacement(words, 2):
        feature = tuple(FEATURES[first][i]+FEATURES[second][i] for i in range(21))
        counts = [0]*64
        counts[first] += 1
        counts[second] += 1
        brute[feature].append(counts)
    total = 0
    for feature, full in brute.items():
        G = [[0]*6 for _ in range(6)]
        for (i, j), value in zip(COORDS, feature):
            G[i][j] = G[j][i] = value
        rebuilt, _ = incidences({'G': G}, total_rows=2)
        need(rebuilt == sorted(full), 'complete two-row multiset control')
        total += len(full)
    need(total == 1653, 'complete nonnegative-surplus two-row domain')
    # Repetition controls at all four positive-surplus types, with sixteen rows.
    positive = [[1]*8+[0]*8, [3]*4+[0]*12, [7]*2+[8]*2+[0]*12, [15]*2+[0]*14]
    for row_words in positive:
        G = [[sum(int(i in SUPPORTS[w] and j in SUPPORTS[w]) for w in row_words) for j in range(6)] for i in range(6)]
        rebuilt, _ = incidences({'G': G})
        desired = [row_words.count(w) for w in range(64)]
        need(desired in rebuilt, 'positive repeated-row incidence recovered')
    # Every domain system on three vertices: compare pruning with actual graphs.
    n = 3
    masks = [[m for m in range(1 << n) if not (m >> i & 1)] for i in range(n)]
    systems = 0
    positives = 0
    for choices in product(range(1, 1 << 4), repeat=n):
        domains = [[m for k, m in enumerate(masks[i]) if choices[i] >> k & 1] for i in range(n)]
        result = reciprocal(domains)
        feasible = False
        for rows in product(*domains):
            if all(bool(rows[i] >> j & 1) == bool(rows[j] >> i & 1) for i in range(n) for j in range(n)):
                feasible = True
                break
        need(not feasible or not result['excluded'], 'positive reciprocal solution never deleted')
        replay_rounds(domains, result)
        systems += 1
        positives += feasible
    need(systems == 3375, 'complete three-point domain systems')
    # Explicit malformed / incomplete-domain guards remain active under -O.
    rejected = False
    try:
        incidences(specification(5, 1), state_limit=1)
    except RuntimeError as exc:
        rejected = str(exc).startswith('INCOMPLETE:')
    need(rejected, 'incomplete recursion guard is not a negative theorem')
    return {'two_row_multisets': total, 'distinct_two_row_Grams': len(brute),
            'positive_repeated_row_fixtures': 4, 'three_vertex_domain_systems': systems,
            'positive_three_vertex_systems': positives, 'incomplete_guard_rejected': True}


def run(export=None):
    census = root_census()
    keys = [root_canonical(root_matrix(edges)) for edges in EXAMPLES]
    need(len(set(keys)) == 8 and set(keys) == set(census), 'examples cover literal root orbits')
    copies = [census[key] for key in keys]
    need(copies == [4, 8, 4, 3, 12, 48, 24, 24], 'named root orbit sizes')
    for edges in EXAMPLES[:3]:
        roots = root_matrix(edges)
        leaves = [i for i in range(4) if len(roots[i] & set(range(4))) == 1]
        need(len(leaves) == 3 and all(not (roots[i] & {4, 5}) for i in leaves), 'analytic star obstruction hypotheses')
    cases = []
    all_records = []
    for profile in range(4, 9):
        weights = (0,) if profile == 7 else (0, 1, 2)
        for w in weights:
            start = time.monotonic()
            spec = specification(profile, w)
            need(sum(spec['G'][i][i]*(1 if i < 4 else -1) for i in range(6)) == 8, 'histogram first moment')
            forms, stats = incidences(spec)
            records = []
            for full in forms:
                if time.monotonic()-start > 120:
                    raise RuntimeError('INCOMPLETE: case time guard reached')
                words, domains, literal = all_domains(spec, full, 'relaxed')
                reference = formula_domains(spec, words)
                need(literal == reference, 'every literal/formula labeled star and active defect agrees')
                result = reciprocal(domains)
                need(result['excluded'], 'relaxed reciprocal domain survives; no exclusion proved')
                deleted = replay_rounds(domains, result)
                records.append({'counts': full, 'domain_sizes': list(map(len, domains)),
                                'domains': domains, 'literal_active_defects': literal,
                                'rounds': result['rounds'], 'deleted': deleted})
            summary = {'profile': profile, 'w': w, 'binary_forms': len(forms),
                       'recursion': stats, 'incidence_sha256': digest(forms),
                       'initial_candidate_masks': sum(sum(r['domain_sizes']) for r in records),
                       'forms_requiring_reciprocal_rounds': sum(bool(r['rounds']) for r in records),
                       'batch_rounds': sum(len(r['rounds']) for r in records),
                       'maximum_rounds': max([len(r['rounds']) for r in records]+[0]),
                       'deleted_candidates': sum(r['deleted'] for r in records),
                       'full_record_sha256': digest(records), 'unexcluded_forms': 0}
            cases.append(summary)
            all_records.append({'profile': profile, 'w': w, 'records': records})
    need(len(cases) == 13 and sum(c['binary_forms'] for c in cases) == 199, 'complete relaxed domain census')
    evidence = controls()
    summary = {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
               'root_edge_words': 32768, 'root_labelings': 127, 'root_orbit_sizes': copies,
               'cases': cases, 'binary_forms': 199, 'original_weight_0_1_forms': 143,
               'extra_weight_2_forms': 56, 'all_relaxed_root_spine_domains_excluded': True,
               'active_defect_placement_constraints_used': False,
               'B_pair_page_constraints_used_in_final_filter': False,
               'controls': evidence, 'complete': True}
    if export:
        export.write_text(json.dumps(all_records, separators=(',', ':'))+'\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--export', type=Path, help='Optional private generated domain records')
    args = parser.parse_args()
    summary = run(args.export)
    if args.expected:
        need(summary == json.loads(args.expected.read_text()), 'compact expected output mismatch')
    print(json.dumps(summary, indent=2, sort_keys=True))
