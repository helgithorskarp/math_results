"""Damage actual literal original AP binding images, not an unattached hash."""
from copy import deepcopy
import json
from pathlib import Path

from check_kernel import bind, check, need


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    record = json.loads((here/'kernel.json').read_bytes())
    cnf = (here/'kernel.cnf').read_bytes()
    positive = check(here)
    damages = []

    def reject(name, mutation, reason):
        bad = deepcopy(record)
        image = mutation(bad)
        changed_cnf = image if type(image) is bytes else cnf
        need(bad != record or changed_cnf != cnf, 'actual changed AP image:'+name)
        try:
            bind(bad, changed_cnf)
        except ValueError as error:
            need(str(error) == reason, 'wrong actual kernel rejection:'+name+':'+str(error))
            damages.append({'name': name, 'rejection': str(error)})
        else:
            raise ValueError('damaged actual original AP binding accepted:'+name)

    scope_reason = 'chosen original fixed0,1,4 finite pattern x phase6 family'
    for key, value in [('N', 3703), ('roots', [0, 1, 5]), ('phase_period', 3), ('variables', 67)]:
        reject('wrong_actual_'+key, lambda r, k=key, v=value: r.__setitem__(k, v), scope_reason)
    reject('actual_zero_step', lambda r: r['original_integer_AP_leaves'][0]['original_AP'].__setitem__(1, 0),
           'each actual nonconstant integer AP lies in zero[0,3703]')
    reject('actual_endpoint_outside', lambda r: r['original_integer_AP_leaves'][0]['original_AP'].__setitem__(0, 3704),
           'each actual nonconstant integer AP lies in zero[0,3703]')
    endpoint_index = next(i for i, leaf in enumerate(record['original_integer_AP_leaves'])
                          if leaf['original_AP'] == [1, 617] and leaf['polarity'] == 1)
    reject('actual_endpoint_root_wrong_variable',
           lambda r: r['original_integer_AP_leaves'][endpoint_index]['literals'].__setitem__(-1, 67),
           'literal original seven-point support including every root occurrence and actual phase')
    regular_index = next(i for i, leaf in enumerate(record['original_integer_AP_leaves'])
                         if abs(leaf['literals'][0]) <= 48)
    reject('actual_regular_phase_wrong_variable',
           lambda r: r['original_integer_AP_leaves'][regular_index]['literals'].__setitem__(0, 49),
           'literal original seven-point support including every root occurrence and actual phase')
    reject('actual_monochromatic_polarity_flipped',
           lambda r: r['original_integer_AP_leaves'][0].__setitem__('polarity', -r['original_integer_AP_leaves'][0]['polarity']),
           'literal original seven-point support including every root occurrence and actual phase')
    reject('actual_compact_clause_missing', lambda r: b''.join(cnf.splitlines(keepends=True)[:-1]),
           'whole original signed compact CNF equality')
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'ACTUAL_ORIGINAL_AP_KERNEL_POSITIVE_AND_SEMANTIC_DAMAGE_CONTROLS_PASS',
                      'positive_entire_original_AP_binding_and_proof': positive,
                      'semantic_damage_rejections': len(damages), 'damages': damages,
                      'external_review_claimed': False}, sort_keys=True))
