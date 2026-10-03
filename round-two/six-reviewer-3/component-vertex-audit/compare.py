"""Optional late comparison of three author JSON files; never proof input.

Arguments: FACTORS.json SYSTEM.json PARENT_SYSTEM.json prior-parent SYSTEM.json.
The primary reconstruction and source-only replay precede this comparison.
"""
import hashlib
import json
import sys
from pathlib import Path
from check import check
from derive import rebuild, rows_text
from digit import coefficients
from geometry import LABELS, CONTACTS


def compare(paths):
    if len(paths) != 4:
        raise ValueError('four explicit data files required')
    raw = [Path(p).read_bytes() for p in paths]
    factors, system, parent, old = [json.loads(r) for r in raw]
    if raw[2] != raw[3] or parent != old:
        raise ValueError('entire immutable original parent changed')
    result = check()
    model, _, _ = rebuild()
    fresh = result['derived_entire_primitive_rows']
    reconstructed = {}
    for name in ('067', '579', '6911'):
        reconstructed['excess' + name] = sorted(
            [i, j, w, v] for w, letter in enumerate(('A', 'B'))
            for i, j, v in fresh[letter + name])
    for name in ('067', '579'):
        reconstructed['excess' + name + '_square'] = [
            [i, j, 0, v] for i, j, v in fresh['H' + name]]
    reconstructed['R'] = [[i, j, 0, v] for i, j, v in rows_text(coefficients(model['R']))]
    if (set(factors) != {'schema_version', 'variable_order', 'coefficient_domain', 'rows'}
            or factors['schema_version'] != 1 or factors['variable_order'] != ['t', 'z', 'w']
            or factors['coefficient_domain'] != 'Z' or factors['rows'] != reconstructed):
        raise ValueError('entire literal factor table differs from reconstruction')
    if parent['residual_triples'] != result['whole260_parent_literal_triples']:
        raise ValueError('entire original parent case list differs')
    expected = {
        'schema_version': 1, 'actual_agent': 'six-tammes-2', 'role': 'researcher',
        't_interval': ['14/25', '593/1000'], 'z_interval': ['6/5', '7/5'],
        'intervals_closed': True, 'original_required_labels': list(LABELS),
        'original_contacts': [list(p) for p in CONTACTS], 'extra_contacts_allowed': True,
        'additional_hypotheses': [], 'logical_imports': [9774, 9912, 10109],
        'root': 'w>0; w*w=R', 'regularity': '2G-a^4 C^2>0',
        'selected_Gram_rank': 'strict_positive; zero_rank_is_only_an_ineligible_basis',
        'parent_system_sha256': hashlib.sha256(raw[3]).hexdigest(),
        'new_excluded_triples': result['exactly5_excluded_literal_triples'],
        'remaining_regular_triples': result['whole255_unchanged_survivor_literal_triples'],
        'all_remaining_feasibility': 'UNRESOLVED',
        'three_arbitrary_packing_additions': 'force_one_of255_necessary_parent_vertex_systems',
        'structural_conclusion': 'every_long_vertex_uses_both_core_components_or_a_cap_plane',
        'capacity_claimed': False, 'global_Tammes15_bound_claimed': False,
        'positive_factor_recipes': {
            'excess067': ['a']*6 + ['b']*2 + ['c']*2 + ['3t-1', 'bz+1'],
            'excess579': ['t'] + ['a']*10 + ['b']*2 + ['c']*2 + ['3t-1', 'bz+1', 'bz+1', 'Q'],
            'excess6911': ['a']*5 + ['b']*2 + ['c']*2 + ['3t-1', 'bz+1'],
            'excess067_square': ['a'] + ['b']*4 + ['c']*2 + ['J', 'Q'],
            'excess579_square': ['a']*2 + ['b']*4 + ['c']*2 + ['J']},
        'square_integer_multipliers': {'excess067_square': 1, 'excess579_square': 4},
        'strict_sign_obligations': [['excess067', 'B'], ['excess067_square', 'A'],
                                    ['excess579', 'B'], ['excess579_square', 'A'],
                                    ['excess6911', 'A'], ['excess6911', 'B']]}
    if system != expected:
        raise ValueError('entire system metadata, recipes or survivor list differs')
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'optional_late_comparison_not_primary_input': True,
            'entire_author_factor_rows_matched': sum(map(len, reconstructed.values())),
            'entire_author_system_all_keys_matched': len(expected),
            'entire_parent_bytes_unchanged': True,
            'all260_parent_and255_survivor_literal_lists_matched': True,
            'author_data': [{'bytes': len(r), 'sha256': hashlib.sha256(r).hexdigest()} for r in raw],
            'native_author_executables_certificates_expected_or_controls_run': False}


if __name__ == '__main__':
    print(json.dumps(compare(sys.argv[1:]), sort_keys=True, separators=(',', ':')))
