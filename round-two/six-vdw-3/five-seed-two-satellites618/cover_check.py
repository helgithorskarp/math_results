"""Independent literal joint four-head cover; extends source00dd57d6.

Only the complete nine-point premise is used; orientation u6 remains free.
This ordinary cover alone proves no new exclusion.
"""
import copy
import itertools
import json
import sys
import tempfile
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def verify(path):
    proposed = json.loads(path.read_text())
    need(proposed['parent_relative_bits'] == [[0,0],[1,0],[2,0],[3,0],[4,0],[52,1],[54,0],[55,0],[102,1]],
         'Parent counterexample scope changed')
    need([(x['height'],x['reference'],x['source_commit']) for x in proposed['mathematical_dependencies']] == [
        (9457,'bafkreie57fszbji6sez2l42kd53mx2dxs7bsvgnmzpai33lvqig4fmb5k4','00dd57d625b56fd84901cd0a14862b90034ad73f')],
         'Written mathematical premise domain changed')
    need(proposed['field_fixed_zero_points'] == [2, 3, 4, 54, 55] and
         proposed['variable_point_order'] == [28, 29, 80, 81], 'Fixed/variable domain changed')
    need(proposed['holes'] == [5, 53, 101] and len(proposed['actual_interval_APs']) == 4,
         'Hole/AP coverage changed')
    need(len(proposed['heads']) == 4 and
         [h['number'] for h in proposed['heads']] == [1, 2, 3, 4], 'Missing ordered head')
    need(proposed['joint_profile_cover'] == {'free_point':6,'original_masks':[2,3],
         'free_orientations_before_heads':91}, 'Incomplete joint profile domain')
    need(6 not in dict(proposed['parent_relative_bits']), 'u6 must remain free')
    # These actual integer APs independently verify the two forbidden constant
    # triples. Neither the field-ladder generator nor native solver is imported.
    expected = [(570, 180), (414, 129), (210, 180), (54, 129)]
    need([(a['start'], a['step']) for a in proposed['actual_interval_APs']] == expected,
         'Literal seven-AP witness changed')
    fixed_points = {2, 3, 4, 54, 55}
    variable = (28, 29, 80, 81)
    inputs = positives = bad = point_checks = 0
    branch_counts = [0] * 4
    for palette in (0, 1):
        for tail in itertools.product((0, 1), repeat=4):
            values = {x: palette for x in fixed_points}
            values.update({x: b ^ palette for x, b in zip(variable, tail)})
            mixed = True
            for item in proposed['actual_interval_APs']:
                terms = [item['start'] + j * item['step'] for j in range(7)]
                need(all(1 <= t <= 1650 and t % 103 not in (5, 53, 101) for t in terms),
                     'Bad actual domain or hole contact')
                need(all(t % 103 in values for t in terms), 'Unassigned witness column')
                colors = [values[t % 103] ^ int(t % 6 >= 3) for t in terms]
                mixed = mixed and len(set(colors)) > 1
                point_checks += len(terms)
            satisfied = (len({values[x] for x in (28, 29, 80)}) > 1 and
                         len({values[x] for x in (29, 80, 81)}) > 1)
            need(mixed == satisfied, 'Literal subsystem differs from claimed triple condition')
            matches = []
            for head in proposed['heads']:
                need(head['other_orientation_bits_free'] in (87, 89), 'Wrong free-bit count')
                local = dict(head['additional_relative_bits'])
                need(set(local) <= set(variable), 'Head imposes an unrelated orientation')
                need(head['other_orientation_bits_free'] == 91 - len(local),
                     'Hidden restriction or wrong domain count')
                if all(values[x] ^ palette == b for x, b in local.items()):
                    matches.append(head['number'])
            need(bool(matches) == satisfied and len(matches) <= 1,
                 'Incomplete, overlapping or unsound head cover')
            if satisfied:
                positives += 1
                branch_counts[matches[0] - 1] += 1
            else:
                bad += 1
            inputs += 1
    need((inputs, positives, bad, point_checks) == (32, 20, 12, 896) and
         branch_counts == [8, 8, 2, 2], 'Incomplete palette/word/branch coverage')
    need(proposed['harmonic_transports'] == [
        {'field_multiplier':88,'field_shift':75,'CRT_multiplier':397,'CRT_shift':384,
         'holes':[0,1,2],'mono_five_seed':[15,30,45,60,75],
         'forced_opposite_endpoint':90,'opposite_required_at_one_of':[74,89]},
        {'field_multiplier':15,'field_shift':30,'CRT_multiplier':427,'CRT_shift':30,
         'holes':[0,1,2],'mono_five_seed':[30,45,60,75,90],
         'forced_opposite_endpoint':15,'opposite_required_at_one_of':[16,31]}],
         'Harmonic transported claim changed')
    CRT_checks = 0
    for transport in proposed['harmonic_transports']:
        alpha,beta = transport['CRT_multiplier'],transport['CRT_shift']
        a,b = transport['field_multiplier'],transport['field_shift']
        points = [(alpha*t+beta)%618 for t in range(618)]
        need(len(set(points)) == 618 and alpha%6 == 1 and beta%6 == 0,
             'CRT transport is not a phase-preserving unit affine map')
        for t,image in enumerate(points):
            need(image%103 == (a*(t%103)+b)%103 and image%6 == t%6,
                 'Literal CRT field/phase identity failed')
            CRT_checks += 1
        need(sorted((a*x+b)%103 for x in (5,53,101)) == transport['holes'] and
             sorted((a*x+b)%103 for x in range(5)) == transport['mono_five_seed'] and
             (a*102+b)%103 == transport['forced_opposite_endpoint'] and
             sorted((a*x+b)%103 for x in (54,55)) == transport['opposite_required_at_one_of'],
             'Transported hole, seed, endpoint or two-point restriction failed')
    bridge_inputs = after_endpoint = after_old = after_new = 0
    residual_profiles, failing_profiles = [], []
    joint_inputs = []
    satellites = (6,52,54,55,102)
    # Complete two-palette truth-table bridge from committed9457. The new
    # binary conclusion's failure pins52 opposite and54/55 equal to the seed,
    # while BOTH choices for u6 remain covered by the same nine-point parent.
    for palette in (0,1):
        for word in itertools.product((0,1),repeat=5):
            relative = dict(zip(satellites,word))
            bridge_inputs += 1
            endpoint = relative[102] == 1
            prior = endpoint and any(relative[x] for x in (52,54,55))
            new = prior and any(relative[x] for x in (54,55))
            after_endpoint += endpoint
            after_old += prior
            after_new += new
            if prior and not new:
                candidate = {x:0 for x in range(5)}
                candidate.update({x:relative[x] for x in satellites if x != 6})
                need(sorted(candidate.items()) == [tuple(x) for x in proposed['parent_relative_bits']],
                     'Uncovered cited-premise counterexample')
                need(relative[6] in (0,1), 'Wrong free u6 domain')
                joint_inputs.append([palette,relative[6]])
                if palette == 0:
                    oldmask = sum(relative[x] << j for j,x in enumerate((6,52,54,55)))
                    failing_profiles.append(oldmask)
            if palette == 0 and new:
                residual_profiles.append([[x,relative[x]] for x in satellites])
    need((bridge_inputs,after_endpoint,after_old,after_new) == (64,32,28,24),
         'Cited-premise bridge domain changed')
    need(sorted(joint_inputs) == [[0,0],[0,1],[1,0],[1,1]] and
         sorted(failing_profiles) == [2,3], 'Incomplete joint palette/u6 cover')
    need(len(residual_profiles) == 12 and len({str(x) for x in residual_profiles}) == 12,
         'Incomplete twelve-profile continuation')
    return {'agent': 'six-vdw-3', 'role': 'researcher', 'complete_two_palette_inputs': inputs,
            'positive_subsystem_inputs': positives, 'negative_subsystem_inputs': bad,
            'literal_integer_point_checks': point_checks, 'head_input_counts_both_palettes': branch_counts,
            'new_head_free_orientation_bits': [89,89,87,87],
            'u6_fixed':False,'joint_old_masks':failing_profiles,
            'joint_palette_free_u6_inputs':joint_inputs,
            'global_colorings_counted': False, 'full_model_feasibility_claimed': False,
            'complete_two_palette_satellite_bridge_inputs':bridge_inputs,
            'CRT_point_identities_checked':CRT_checks,
            'transported_harmonic_claims':proposed['harmonic_transports'],
            'after_forced_endpoint_local_inputs':after_endpoint,
            'after_committed_ternary_rule_local_inputs':after_old,
            'after_prospective_binary_rule_local_inputs':after_new,
            'remaining_relative_satellite_profiles':residual_profiles,
            'mathematical_premises_reproved':False,
            'literal_cover_alone_refutes_full_models':False}


def controls(path):
    original = json.loads(path.read_text())
    verify(path)
    damages = []
    a = copy.deepcopy(original); a['heads'].pop(); damages.append(a)
    a = copy.deepcopy(original); a['heads'][2]['additional_relative_bits'][-1][1] = 0; damages.append(a)
    a = copy.deepcopy(original); a['heads'][0]['additional_relative_bits'].pop(); damages.append(a)
    a = copy.deepcopy(original); a['heads'][0]['other_orientation_bits_free'] = 88; damages.append(a)
    a = copy.deepcopy(original); a['actual_interval_APs'][0]['step'] += 1; damages.append(a)
    a = copy.deepcopy(original); a['field_fixed_zero_points'].pop(); damages.append(a)
    a=copy.deepcopy(original);a['parent_relative_bits'][5][1]=0;damages.append(a)
    a=copy.deepcopy(original);a['mathematical_dependencies'].pop();damages.append(a)
    a=copy.deepcopy(original);a['harmonic_transports'][0]['CRT_multiplier']+=1;damages.append(a)
    a=copy.deepcopy(original);a['harmonic_transports'][1]['opposite_required_at_one_of'].pop();damages.append(a)
    a=copy.deepcopy(original);a['parent_relative_bits'].insert(5,[6,0]);damages.append(a)
    a=copy.deepcopy(original);a['joint_profile_cover']['original_masks'].pop();damages.append(a)
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / 'bad.json'
        for item in damages:
            target.write_text(json.dumps(item))
            try:
                verify(target)
            except ValueError:
                pass
            else:
                raise ValueError('Damaged head/proof/scope certificate accepted')
    return {'positive_control': True, 'damaged_certificates_rejected': len(damages)}


if __name__ == '__main__':
    p = Path(sys.argv[1])
    print(json.dumps({'verification': verify(p), 'controls': controls(p)}))
