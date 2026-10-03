"""Complete new physical factors, closed signs and original basis coverage.

Native target factor tables and expected results remain unopened at creation.
"""
import json
from fractions import Fraction as F
from itertools import combinations
from derive import rebuild, rows_text
from signs import complete_sign
from census import classify, PLANES, LABELS

ORIGINAL = ('14/25', '593/1000', '6/5', '7/5')
LARGER = ('14/25', '3/5', '6/5', '7/5')
NAMED = ('B067', 'H067', 'B579', 'H579', 'A6911', 'B6911')
EXCLUDED = ((0,6,7),(1,4,12),(2,8,10),(5,7,9),(6,9,11))
A = frozenset((0,5,6,7,9,11))
B = frozenset((1,2,4,8,10,12))


def check():
    m, derived, identities = rebuild()
    signs = {}
    for label, box in [('original', ORIGINAL), ('larger_local', LARGER)]:
        signs[label] = {}
        for name in NAMED:
            signs[label][name] = complete_sign(derived[name], box, 1)
    census = classify()
    parent = [tuple(r['triple']) for r in census if r['case']=='residual']
    pure = [r for r in census if set(r['triple'])<=A or set(r['triple'])<=B]
    pure_parent = tuple(p for p in parent if set(p)<=A or set(p)<=B)
    if len(census)!=364 or len(parent)!=260 or len(pure)!=40 or pure_parent!=EXCLUDED:
        raise ValueError('entire original case domain or pure-component basis changed')
    survivors = [list(p) for p in parent if p not in EXCLUDED]
    if len(survivors)!=255 or any(set(p)<=A or set(p)<=B for p in survivors):
        raise ValueError('whole survivor literal list changed')
    # Strict factors used for clearing/Gram/longness hold on the LARGER box.
    low, high = F(LARGER[0]), F(LARGER[1])
    auxiliary = {
        'J_at_lower': (1+low)**2+low*(9*low**2-2*low-3),
        'J_derivative_lower': 27*low**2-2*high-1,
        'h_lower': 9*low**2-1,
        '3t_minus1_lower': 3*low-1,
        '5t_squared_minus1_lower': 5*low**2-1,
        'b_lower': 1-high,
        '29t_minus15_lower': 29*low-15,
        '25t_minus9_lower': 25*low-9}
    if any(v<=0 for v in auxiliary.values()):
        raise ValueError('nonpositive auxiliary strict bound')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'whole_original_coordinate_identities':identities,
            'derived_entire_primitive_rows':{k:rows_text(v) for k,v in derived.items()},
            'all_complete_closed_sign_records':signs,
            'larger_local_auxiliary_strict_bounds':{k:str(v) for k,v in auxiliary.items()},
            'whole364_original_case_rows':census,
            'whole40_pure_component_case_rows':pure,
            'whole260_parent_literal_triples':[list(p) for p in parent],
            'exactly5_excluded_literal_triples':[list(p) for p in EXCLUDED],
            'whole255_unchanged_survivor_literal_triples':survivors,
            'not_blind_written_math_and_own_backend_exposed':True,
            'new_target_native_factor_program_expected_input':False,
            'larger_local_rectangle_only_not_extended_geometric_normalization':True,
            'local_cuts_do_not_use_strict_2G_a4C2_or_other66_core_packing_predicates':True,
            'signed_positive_root_retained':True,
            'all255_feasibility_or_global_Tammes_claim':False}


if __name__ == '__main__':
    print(json.dumps(check(),sort_keys=True,separators=(',',':')))
