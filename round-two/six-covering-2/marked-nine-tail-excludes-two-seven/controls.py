"""Typed fresh-record checks and semantic damage controls, not a third kernel.

The reference records/raw streams must have just been rebuilt by the separate
audit algorithms. No expected digest is consulted in this module. These checks
validate the interface and reject damaged evidence; the proof's arithmetic
independence comes from the seven other source files, not this comparison code.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

LITERAL = [[8, 0], [9, 0], [10, 1], [14, 0], [12, 10], [16, 2], [28, 4], [32, 6]]
D = (3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def reject_number(token):
    raise ValueError('Noninteger JSON number: ' + token)


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def loads(data):
    return json.loads(data, object_pairs_hook=object_pairs,
                      parse_float=reject_number, parse_constant=reject_number)


def typed_equal(actual, rebuilt):
    """Complete structural comparison, with bool/int and list order distinct."""
    if type(actual) is not type(rebuilt):
        return False
    if isinstance(actual, dict):
        return actual.keys() == rebuilt.keys() and all(
            typed_equal(actual[k], rebuilt[k]) for k in actual)
    if isinstance(actual, list):
        return len(actual) == len(rebuilt) and all(
            typed_equal(a, b) for a, b in zip(actual, rebuilt))
    return actual == rebuilt


def inventory(H, Q):
    require(type(H) in (list, tuple) and type(Q) in (list, tuple), 'Inventory sequence required')
    require(len(H) + len(Q) == 6, 'Six productive extras required')
    for group, pool in ((H, set(D) - {3}), (Q, set(D))):
        require(all(type(d) is int and d in pool for d in group), 'Spent or invalid original label')
        require(len(set(group)) == len(group), 'Repeated original modulus')
    originals = [16*d for d in H] + [32*d for d in Q]
    require(len(set(originals)) == 6, 'Original labels were merged or reused')


def domain(record, physical=False):
    require(type(record) is dict, 'Record object required')
    require(record.get('agent') == 'six-covering-2' and record.get('role') == 'researcher', 'Author/role mismatch')
    require(type(record.get('schema')) is int and record['schema'] == 1, 'Integer schema required')
    d = record if physical else record['domain']
    common = {'minimum_exactly': 8, 'original_moduli_divide': 10080,
              'literal_prefix': LITERAL, 'productive_TAILs_exactly': 9,
              'unproductive_selected_tails_allowed': True,
              'actual_LCM_may_be_proper_divisor': True, 'global_bound_changed': False}
    common['essential_originals_explicit' if physical else 'essential_originals'] = [16, 32]
    common['actual_hole_parent_counts' if physical else 'counts_in_actual_hole_parents2_6'] = [2, 7]
    if not physical:
        common['BASE_lower_bound_imported'] = 177
    for key, value in common.items():
        require(key in d and typed_equal(d[key], value), 'Literal theorem domain mismatch: ' + key)
    require(record.get('ordinary_proof_formalized', d.get('ordinary_proof_formalized')) is False,
            'Unformalized ordinary bridges must be disclosed')
    require(record.get('independent_person_reviewed', d.get('independent_person_reviewed')) is False,
            'Person-independent review is pending')


def record_equal(actual, rebuilt, stage):
    domain(actual, stage == 'physical')
    require(typed_equal(actual, rebuilt), 'Evidence differs from fresh separate reconstruction: ' + stage)


def controls(work):
    records = {s: loads((work/(s+'.json')).read_text()) for s in ('small', 'capacity', 'projection', 'physical')}
    rebuilt = {s: loads((work/('audit-'+s+'.json')).read_text()) for s in records}
    for stage, record in records.items():
        record_equal(record, rebuilt[stage], stage)
    small, capacity, projection, physical = (records[s] for s in records)
    require(capacity['domain']['H_pool'] == list(D[1:]), 'H48 must be spent, without removing Q96')
    require(capacity['domain']['Q_pool'] == list(D), 'Q96 must remain available')
    require(capacity['domain']['cross_H_Q_equal_cofactors_legal'] is True, 'Cross-type equality is legal')
    require(capacity['domain']['essential32_forces_nonempty_missing_same_half_Q_arm'] is True,
            'Actual-hole essential32 bridge required')
    for H, Q, _, _ in capacity['survivors_ge87']:
        inventory(H, Q)
    require(projection['inventory_count'] == len(capacity['survivors_ge87']), 'Projection lineage incomplete')
    for block, predecessor in zip(projection['original_six_extra_inventories'], capacity['survivors_ge87']):
        require([block['H'], block['Q']] == predecessor[:2], 'Original inventory lineage/order differs')
        inventory(block['H'], block['Q'])
    for name in ('small.raw', 'physical.raw'):
        raw = (work/name).read_bytes()
        require(raw == (work/('audit-'+name)).read_bytes(), 'Whole fresh raw stream mismatch')
    rejected = []

    def reject(label, action):
        try:
            action()
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('Damaged evidence accepted: ' + label)

    def damage(stage, label, change):
        altered = deepcopy(records[stage])
        change(altered)
        reject(label, lambda: record_equal(altered, rebuilt[stage], stage))

    changes = [
        ('minimum_exactly', 9, 'at-least-eight cannot replace exactly-eight'),
        ('essential_originals', [16], 'essential32 cannot be omitted'),
        ('counts_in_actual_hole_parents2_6', [3, 6], 'count cannot migrate to another allocation'),
        ('productive_TAILs_exactly', 10, 'productive count cannot be increased'),
        ('BASE_lower_bound_imported', 176, 'imported BASE177 cannot be weakened silently'),
        ('unproductive_selected_tails_allowed', False, 'unproductive selected tails stay allowed'),
        ('actual_LCM_may_be_proper_divisor', False, 'proper-divisor LCM must stay allowed'),
        ('minimum_exactly', 8.0, 'float and integer domains differ'),
        ('global_bound_changed', 0, 'integer zero cannot impersonate False'),
    ]
    for key, value, label in changes:
        damage('small', label, lambda r, k=key, v=value: r['domain'].__setitem__(k, v))
    damage('small', 'prefix phase cannot be quotient-normalized', lambda r: r['domain']['literal_prefix'][6].__setitem__(1, 2))
    damage('small', 'all free omissions must be retained', lambda r: r['domain'].__setitem__('all_other_original_labels_phases_omissions_free', False))
    damage('small', 'one unused BASE original cannot be dropped', lambda r: r['all_unused_BASE_originals'].pop())
    damage('small', 'protected shadow budget cannot be reversed', lambda r: r['mirrored_small_shadows'][0].__setitem__('protected_budget', 177-r['mirrored_small_shadows'][0]['shadow_size']))
    damage('capacity', 'spent H48 cannot return', lambda r: r['domain']['H_pool'].insert(0, 3))
    damage('capacity', 'Q96 cannot be merged with H48', lambda r: r['domain']['Q_pool'].remove(3))
    damage('capacity', 'legal cross-type equal cofactors cannot be suppressed', lambda r: r['domain'].__setitem__('cross_H_Q_equal_cofactors_legal', False))
    damage('capacity', 'missing same-half Q arm cannot be assumed empty', lambda r: r['domain'].__setitem__('essential32_forces_nonempty_missing_same_half_Q_arm', False))
    damage('capacity', 'one complete original inventory cannot be dropped', lambda r: r['all_types'][0]['all_caps'].pop())
    damage('capacity', 'coarse capacity cannot be understated', lambda r: r.__setitem__('uniform_parent6_upper', 93))
    damage('projection', 'one physical quarter role cannot be dropped', lambda r: r['original_six_extra_inventories'][0]['all_role_rows'].pop())
    damage('projection', 'coarse surviving inventory cannot be omitted', lambda r: r['original_six_extra_inventories'].pop())
    damage('projection', 'mod3 branch1 cannot replace branch2', lambda r: r['domain'].__setitem__('cofactor_divisible_by3_productive_branch_choices', [0, 1]))
    damage('projection', 'projected support cannot be understated', lambda r: r.__setitem__('uniform_role_branch_upper', 83))
    damage('projection', 'unrecognized keys cannot be added', lambda r: r.__setitem__('undocumented_phase_quotient', True))
    damage('physical', 'binary quarter order cannot be swapped', lambda r: r['quarter_bit_order'].__setitem__(1, 22))
    damage('physical', 'one original phase mask cannot be dropped', lambda r: r['all_original_phase_masks'].pop())
    duplicate_row = next(i for i, row in enumerate(projection['all_projection_union_values'])
                         if len(row[0]) != len(set(row[0])))
    damage('projection', 'repeated LCM rows cannot be collapsed',
           lambda r: r['all_projection_union_values'][duplicate_row].__setitem__(0,
               sorted(set(r['all_projection_union_values'][duplicate_row][0]))))
    for name, key in (('small.raw', 'raw_stream_sha256'), ('physical.raw', 'raw_sha256')):
        altered = bytearray((work/name).read_bytes()); altered[0] ^= 1
        stage = name.split('.')[0]
        fake = deepcopy(records[stage]); fake[key] = sha256(altered).hexdigest()
        # The attacker recomputes the declared digest. Fresh raw equality rejects
        # the damage regardless of the expected.json pins or declared digest.
        reject('rehashed first-byte damage in '+name,
               lambda b=bytes(altered), n=name: require(b == (work/('audit-'+n)).read_bytes(), 'Fresh raw mismatch'))
        reject('rehashed raw metadata damage in '+name,
               lambda r=fake, s=stage: record_equal(r, rebuilt[s], s))
    reject('duplicate JSON keys', lambda: loads('{"schema":1,"schema":1}'))
    reject('floating JSON integer', lambda: loads('{"schema":1.0}'))
    reject('nonfinite JSON value', lambda: loads('{"schema":NaN}'))
    for H, Q, label in [([3, 5, 7], [3, 5, 7], 'reuse of original48'),
                        ([5, 5, 7], [3, 5, 7], 'same H original reused'),
                        ([5, 7, 9], [3, 3, 7], 'same Q original reused'),
                        ([5, 7], [3, 5, 7], 'wrong number of extras'),
                        ([True, 7, 9], [3, 5, 7], 'boolean cofactor')]:
        reject(label, lambda h=H, q=Q: inventory(h, q))
    # Positive controls deliberately retain the freedoms that would strengthen
    # a false exclusion if accidentally removed.
    inventory([5, 7, 9], [3, 5, 7])
    equal_cross = sum(bool(set(H) & set(Q)) for H, Q, _, _ in capacity['survivors_ge87'])
    require(equal_cross > 0, 'No positive cross-type equality witness retained')
    require(small['domain']['unproductive_selected_tails_allowed'] is True and
            small['domain']['actual_LCM_may_be_proper_divisor'] is True, 'Freedoms omitted')
    return {'semantic_record_damages_rejected': rejected,
            'negative_count': len(rejected),
            'positive_controls': ['all four fresh whole records and both raw streams accepted',
                'cross-type equal cofactors remain distinct originals', 'Q96 allowed while H48 spent',
                'unproductive selected tails allowed', 'actual LCM may be proper divisor',
                'repeated projected LCM rows preserved'],
            'positive_cross_type_inventory_count': equal_cross,
            'repeated_projection_multiset_witness_index': duplicate_row,
            'fresh_audit_comparison_not_expected_hash': True,
            'new_arithmetic_kernel_claimed': False,
            'independent_person_reviewed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = controls(args.work)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'negative_count': result['negative_count'],
                     'positive_count': len(result['positive_controls']),
                     'fresh_audit_comparison_not_expected_hash': True}))
