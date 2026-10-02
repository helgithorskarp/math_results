"""Freeze the complete one-disjoint-route proof premises, with explicit imports.

This validates every bounded checker binding and the exact negative partition.
It does not supply an external-person verdict or make a Git/graph publication.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parent
OUT = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def pair(name):
    normal = json.loads((OUT / (name+'.json')).read_text())
    optimized = json.loads((OUT / (name+'-O.json')).read_text())
    need(normal['finite'] == optimized['finite'] and digest(normal['finite']) ==
         normal['finite_sha256'] == optimized['finite_sha256'], 'Normal/O finite binding differs: '+name)
    return normal


def main():
    start = time.monotonic()
    deadline = start+45
    prep = pair('fresh-prep-checked')
    cuts = pair('fresh-cuts-checked')
    need(prep['finite']['full_functions'] == 6214 and
         cuts['finite']['census']['INHERITED_INDEPENDENTLY_CHECKED_MINIMUM_LOCK'] == 2339 and
         cuts['finite']['census']['NO_CUT_FOUND_RETAINED_WITHOUT_FEASIBILITY_ASSERTION'] == 3875,
         'Complete preparation counts differ')
    catalogue = json.loads((OUT / 'branch01-catalogue.json').read_text())
    checked = pair('branch01-catalogue-checked')
    need(checked['finite']['producer_quotient_sha256'] == catalogue['finite_sha256'] and
         checked['finite']['source_targets_replayed'] == 41562 and checked['finite']['representative_targets'] == 17682 and
         digest(catalogue['representatives']) == catalogue['finite']['representatives_sha256'] and
         digest(catalogue['aliases']) == catalogue['finite']['aliases_sha256'], 'Whole target quotient changed')
    constant = json.loads((OUT / 'branch01-constant-summary.json').read_text())
    expected_slices = [[i, min(i+1000, 17682)] for i in range(0, 17682, 1000)]
    need([r['catalogue_slice'] for r in constant['slices']] == expected_slices and
         constant['catalogue_finite_sha256'] == catalogue['finite_sha256'], 'Constant target partition incomplete')
    counts, metrics, constant_hashes, closed, residual, selected_masses = Counter(), Counter(), [], set(), [], []
    for first, last in expected_slices:
        need(time.monotonic() < deadline, 'Incomplete45s source freeze')
        proposal = json.loads((OUT / f'constant-catalogue01-{first:05}-{last:05}.json').read_text())
        check = pair(f'constant-catalogue-check01-{first:05}-{last:05}-00000-{last-first:05}')
        need([r['front_index'] for r in proposal['cases']] == list(range(first, last)) and
             digest(proposal['cases']) == proposal['cases_sha256'] == check['finite']['complete_case_certificate_sha256'],
             'Constant slice case binding differs')
        for case in proposal['cases']:
            index = case['front_index']
            need(case['prefix_sha256'] == catalogue['representatives'][index]['prefix_sha256'] and
                 case['nine_core_sha256'] == catalogue['representatives'][index]['nine_core_sha256'], 'Wrong representative bound')
            if case['constant16_exceeds44']:
                closed.add(index)
                selected_masses.append(case['selected_mass'])
            else:
                residual.append(index)
        counts.update(check['finite']['census'])
        metrics.update(check['finite']['metrics'])
        constant_hashes.append([first, last, check['finite_sha256']])
    need(residual == constant['inconclusive_catalogue_indices'] and len(residual) == 108,
         'Exact108-case residual complement differs')
    inner = json.loads((OUT / 'branch01-inner-summary.json').read_text())
    need(inner['complete_residual_indices'] == residual and not inner['inconclusive_catalogue_indices'],
         'Inner partition remains incomplete/open')
    inner_counts, inner_metrics, inner_hashes, inner_closed = Counter(), Counter(), [], set()
    for first in range(0, len(residual), 32):
        need(time.monotonic() < deadline, 'Incomplete45s inner source freeze')
        last = min(first+32, len(residual))
        proposal = json.loads((OUT / f'inner01-{first:05}-{last:05}.json').read_text())
        check = pair(f'inner-checked01-{first:05}-{last:05}')
        need([c['catalogue_index'] for c in proposal['cases']] == residual[first:last] and
             digest(proposal['cases']) == proposal['finite']['cases_sha256'] ==
             check['finite']['complete_producer_cases_sha256'] and not check['finite']['inconclusive_catalogue_indices'],
             'Inner slice not fully certified')
        for case in proposal['cases']:
            need(case['producer_exceeds44'] and case['catalogue_index'] not in closed,
                 'Duplicate/unclosed inner representative')
            inner_closed.add(case['catalogue_index'])
            selected_masses.append(case['selected_mass'])
        inner_counts.update(check['finite']['census'])
        inner_metrics.update(check['finite']['metrics'])
        inner_hashes.append([first, last, check['finite_sha256']])
    need(closed.isdisjoint(inner_closed) and closed | inner_closed == set(range(17682)) and
         counts['independently_constant16_excluded_cases'] == len(closed) == 17574 and
         inner_counts['independently_inner_excluded_cases'] == len(inner_closed) == 108,
         'Complete representative negative partition differs')
    damage = json.loads((OUT / 'damage-summary.json').read_text())
    need(damage['restored_byte_for_byte'] and len(damage['controls']) == 8 and
         all(r['returncode'] != 0 for r in damage['controls']), 'Four semantic damage controls incomplete')
    finite = {'schema': 'thirteen-L4-disjoint-route56-79-private-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
              'statement': 'No standard total<=44 sorting completion of literalB23;L4 whose first strict ordinary HIGH mass increase is a singleton preceded by exactly two equal HIGH events with disjoint pairs(5,6) and(7,9), in either commuting order. Arbitrary preparations/interleaving/repeated gates/suffix depth.',
              'HIGH_word': [[5, 6], [7, 9]], 'full_preparation_functions': 6214, 'absorbed_minimum_locks': 2339,
              'retained_preparation_functions': 3875, 'preparation_finite_sha256': prep['finite_sha256'],
              'preparation_cut_finite_sha256': cuts['finite_sha256'],
              'front_census': catalogue['finite']['front_census'], 'front_metrics': catalogue['finite']['front_metrics'],
              'front_interval_bindings_sha256': catalogue['finite']['complete_interval_bindings_sha256'],
              'whole_image_quotient_finite_sha256': catalogue['finite_sha256'],
              'whole_image_quotient_checked_sha256': checked['finite_sha256'], 'original_core_targets': 41562,
              'distinct_maximum_budget_representatives': 17682, 'constant_excluded_representatives': 17574,
              'constant_census': dict(counts), 'constant_metrics': dict(metrics),
              'constant_finite_sha256': digest(constant_hashes), 'inner_excluded_representatives': 108,
              'inner_census': dict(inner_counts), 'inner_metrics': dict(inner_metrics), 'inner_finite_sha256': digest(inner_hashes),
              'minimum_selected_mass': min(selected_masses), 'size44_ceiling': 1 << 44,
              'remaining_gate_budget_range': [3, 12], 'nine_core_image_size_range': [25, 75],
              'four_semantic_damage_controls_reject_normal_O': True, 'normal_O_finite_equal': True,
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False,
              'public_source_published': False, 'new_graph_submission': False,
              'written_bridges_formalized': False, 'imported_lower_bound_corpora_reproved': False,
              'imported_smaller_bounds': {'S11': 35, 'S7': 16, 'S6': 12, 'S5': 9},
              'numeric_primitives_source_commit': 'f47e57677011488966488f68228562643bed2b3c',
              'remaining_scope': 'Other14 disjoint two-prior routes, other event counts/LOW prefixes and unrestricted44..45 remain open. Previously published9699 excludes the10 dependent routes.'}
    private_baseline = digest(finite)
    need(private_baseline == 'd6f14001ab1cd74b61388ed021afc26412a60276552f684600a698003bc43a79',
         'Exact private mathematical baseline changed')
    finite['schema'] = 'thirteen-L4-disjoint-route56-79-v1'
    del finite['public_source_published']
    del finite['new_graph_submission']
    result = {'private_baseline_finite_sha256': private_baseline,
              'portable_reproduction_complete': True,
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'python': sys.version.split()[0], 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (SOURCE / 'certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
