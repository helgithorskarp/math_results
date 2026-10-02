"""Reject semantic damage; transport actual points, cores and color functions."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import subprocess
import sys
import check_colors
import verify

def rejected(function, value):
    try:
        function(value)
    except ValueError:
        return
    raise ValueError('damaged mathematical input accepted')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--primary-work', required=True)
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    here = Path(__file__).absolute().parent
    fixture = json.loads((here/'fixtures.json').read_text())
    bridge = json.loads((here/'BRIDGE.json').read_text())
    cert = json.loads((here/'certificates.json').read_text())
    fixture_damage = []
    def change_fixture():
        value = copy.deepcopy(fixture); fixture_damage.append(value); return value
    change_fixture()['stars'].pop()
    change_fixture()['stars'][0][1] = copy.deepcopy(fixture['stars'][0][0])
    change_fixture()['stars'][0][0][0] = 18
    change_fixture()['stars'][0][0][0] = fixture['stars'][0][0][1]
    change_fixture()['stars'][0][1] = [0, 1, 8, 11]
    change_fixture()['groups'][9][0] = [0]*17
    change_fixture()['groups'][9] = [g for g in fixture['groups'][9] if g != list(range(17))]
    false = list(range(17)); false[0], false[1] = 1, 0
    change_fixture()['groups'][9] = [list(range(17)), false]
    generator = next(g for g in fixture['groups'][9] if [g[g[p]] for p in range(17)] != list(range(17)))
    change_fixture()['groups'][9] = [list(range(17)), generator]
    change_fixture()['groups'][9].append(copy.deepcopy(fixture['groups'][9][0]))
    for value in fixture_damage:
        rejected(verify.inspect, value)
    bridge_damage = []
    def change_bridge():
        value = copy.deepcopy(bridge); bridge_damage.append(value); return value
    change_bridge()['raw_positive_maps'].pop()
    change_bridge()['raw_positive_maps'][1] = copy.deepcopy(bridge['raw_positive_maps'][0])
    change_bridge()['raw_positive_maps'][0]['point_map'][0] = bridge['raw_positive_maps'][0]['point_map'][1]
    change_bridge()['raw_positive_maps'][0]['word_masks'][0] ^= 1 << 18
    change_bridge()['raw_positive_maps'][0]['triangle_points'] = [999]
    change_bridge()['raw_positive_maps'][0]['first'][0] = 23
    change_bridge()['raw_positive_maps'][0]['first'][1][0] = (bridge['raw_positive_maps'][0]['first'][1][0]+1) % 17
    change_bridge()['raw_positive_maps'][0]['second'][1].append(0)
    for value in bridge_damage:
        rejected(lambda b: check_colors.check(b, cert, fixture), value)
    cert_damage = []
    def change_cert():
        value = copy.deepcopy(cert); cert_damage.append(value); return value
    change_cert()['entries'].pop()
    change_cert()['entries'][1] = copy.deepcopy(cert['entries'][0])
    change_cert()['entries'][0]['candidate_count'] -= 1
    change_cert()['entries'][0]['candidate_sha256'] = '0'*64
    change_cert()['entries'][0]['colors'].pop()
    change_cert()['entries'][0]['colors'][0] = True
    change_cert()['entries'][0]['capacity'] = 0
    change_cert()['entries'][0]['edges'] += 1
    change_cert()['entries'][0]['upper_bound'] -= 1
    change_cert()['entries'][0]['first_fixture'] = 7
    change_cert()['entries'][0]['product_index'] += 1
    change_cert()['entries'][0]['triangle_count'] += 1
    candidates, _, _ = check_colors.role_and_domain(bridge['raw_positive_maps'][0], fixture)
    i, j = next((i, j) for i, j in itertools.combinations(range(len(candidates)), 2)
                if len(candidates[i] & candidates[j]) <= 2)
    damaged = change_cert(); damaged['entries'][0]['colors'][j] = damaged['entries'][0]['colors'][i]
    for value in cert_damage:
        rejected(lambda c: check_colors.check(bridge, c, fixture), value)

    baseline_marks = verify.inspect(fixture)
    baseline_colors = check_colors.check(bridge, cert, fixture)
    transported_records = 0
    for a, b in ((5, 3), (11, 9), (16, 0)):
        pi = [(a*p+b) % 17 for p in range(17)]
        pi18 = pi+[17]
        inverse = [pi.index(p) for p in range(17)]
        transported = copy.deepcopy(fixture)
        transported['stars'] = [[[pi[p] for p in q] for q in Q] for Q in fixture['stars']]
        transported['groups'] = [[[pi[g[inverse[p]]] for p in range(17)] for g in G] for G in fixture['groups']]
        rows = verify.inspect(transported)
        verify.need([(len(r['first']), len(r['second']), len(r['first_orbits']), len(r['second_orbits'])) for r in rows] ==
                    [(len(r['first']), len(r['second']), len(r['first_orbits']), len(r['second_orbits'])) for r in baseline_marks],
                    'literal relabeling changed mark/orbit populations')
        for original, changed in zip(baseline_marks, rows):
            verify.need(set(changed['first']) == {tuple(pi[p] for p in m) for m in original['first']}
                        and set(changed['second']) == {tuple(pi[p] for p in m) for m in original['second']},
                        'actual marking transport differs')
        tb, tc = copy.deepcopy(bridge), copy.deepcopy(cert)
        for index, (old, changed) in enumerate(zip(bridge['raw_positive_maps'], tb['raw_positive_maps'])):
            changed['first'][1] = [pi[p] for p in old['first'][1]]
            changed['second'][1] = [pi[p] for p in old['second'][1]]
            changed['point_map'] = [pi18[old['point_map'][inverse[p]]] for p in range(17)]
            changed['word_masks'] = sorted(sum(1 << pi18[p] for p in range(18) if m >> p & 1)
                                           for m in old['word_masks'])
            changed['triangle_points'] = sorted(pi18[p] for p in old['triangle_points'])
            old_domain, _, _ = check_colors.role_and_domain(old, fixture)
            new_domain, new_masks, _ = check_colors.role_and_domain(changed, transported)
            color_by_word = {frozenset(pi18[p] for p in q): c for q, c in zip(old_domain, cert['entries'][index]['colors'])}
            verify.need(set(color_by_word) == set(new_domain), 'actual residual-domain transport differs')
            tc['entries'][index]['colors'] = [color_by_word[q] for q in new_domain]
            tc['entries'][index]['candidate_sha256'] = check_colors.digest(new_masks)
        result = check_colors.check(tb, tc, transported)
        fields = ('candidate_count', 'edges', 'capacity', 'upper_bound',
                  'lambda_xu', 'lambda_yv', 'observed_uv', 'first_deficit_pattern', 'triangle_count')
        verify.need([[r[k] for k in fields] for r in result['records']] ==
                    [[r[k] for k in fields] for r in baseline_colors['records']], 'transported numerical records differ')
        transported_records += len(result['records'])

    target = Path(args.work); target.mkdir(parents=True, exist_ok=True)
    primary = Path(args.primary_work)
    (target/'domains.json').write_bytes((primary/'domains.json').read_bytes())
    positive_index = bridge['raw_positive_maps'][0]['product_index']
    positive_name = f'product-{positive_index:03d}.json'
    positive = json.loads((primary/positive_name).read_text())
    mutations = []
    def change_product():
        value = copy.deepcopy(positive); mutations.append(value); return value
    change_product()['status'] = 'INCOMPLETE'
    change_product()['product_index'] = positive_index+1
    change_product()['counts']['partial_maps'] -= 1
    change_product()['partial_maps_sha256'] = '0'*64
    change_product()['positives'] = []
    change_product()['positives'][0]['point_map'][0] += 1
    change_product()['positives'][0]['triangle_points'] = [999]
    command = [sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(here/'verify.py'),
               '--fixtures', str(here/'fixtures.json'), '--primary-work', str(target),
               '--output', str(target/'result.json'), '--first', str(positive_index),
               '--finish', str(positive_index+1)]
    def run(value):
        (target/positive_name).write_text(json.dumps(value)+'\n')
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    verify.need(run(positive).returncode == 0, 'undamaged product control failed')
    for value in mutations:
        result = run(value)
        verify.need(result.returncode == 1 and 'ValueError:' in result.stderr,
                    'damaged product accepted or operational failure')
    result = subprocess.run(command[:-4], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    verify.need(result.returncode == 1 and 'primary product population gap' in result.stderr,
                'whole-domain product gap accepted')
    # The full carrier retains u-v leave cases even though none is positive.
    # Inject a false positive with consistent15552-map accounting into one.
    ds = json.loads((primary/'domains.json').read_text())
    source_rows = verify.inspect(fixture)
    uv_second = next(i for i, (si, (su, sv, sx)) in enumerate(ds['second'])
                     if sv in source_rows[si]['missing'][su])
    uv_index = uv_second
    uv_name = f'product-{uv_index:03d}.json'
    original_uv = json.loads((primary/uv_name).read_text())
    verify.need(not original_uv['positives'], 'uncovered u-v control unexpectedly positive')
    uv_command = command[:-4]+['--first', str(uv_index), '--finish', str(uv_index+1)]
    (target/uv_name).write_text(json.dumps(original_uv)+'\n')
    result = subprocess.run(uv_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    verify.need(result.returncode == 0, 'complete uncovered-uv negative product control failed')
    false_uv = copy.deepcopy(original_uv)
    fi, (u, v, y) = original_uv['first']
    si, second_mark = original_uv['second']
    partials, _ = verify.point_maps(source_rows[fi], source_rows[si], (u, v, y), second_mark)
    phi = list(partials[0])
    remaining_source = [p for p in range(17) if phi[p] < 0]
    remaining_target = sorted(set(range(18))-{y}-set(phi))
    for p, image in zip(remaining_source, remaining_target):
        phi[p] = image
    literal = set(frozenset(q)|{17} for q in source_rows[fi]['blocks']) | set(
        frozenset(phi[p] for p in q)|{y} for q in source_rows[si]['blocks'])
    verify.need(len(literal) == 36 and any(len(a & b) >= 3 for a, b in itertools.combinations(literal, 2)),
                'invented-positive control must be an actual colliding36-word image')
    triangles = [p for p in range(18) if p not in (17, y, u, v) and
        sum({17, p} <= w for w in literal) == sum({y, p} <= w for w in literal) == 4 and
        not any({17, y, p} <= w for w in literal)]
    fake = dict(point_map=phi, word_masks=sorted(sum(1 << p for p in w) for w in literal),
                triangle_points=triangles)
    false_uv['positives'] = [fake]
    false_uv['positives_sha256'] = verify.sha([fake])
    reason = next(reason for reason, count in false_uv['rejected_full_maps'].items() if count)
    false_uv['rejected_full_maps'][reason] -= 1
    (target/uv_name).write_text(json.dumps(false_uv)+'\n')
    result = subprocess.run(uv_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    verify.need(result.returncode == 1 and 'complete positive maps differ' in result.stderr,
                'account-consistent invented uncovered-uv positive accepted or operational failure')
    domain_damages = []
    wrong = copy.deepcopy(ds); wrong['second'].pop(uv_second); domain_damages.append(wrong)
    wrong = copy.deepcopy(ds); wrong['second'][0][1].append(0); domain_damages.append(wrong)
    low_v = next(i for i, (si, (_, sv, _)) in enumerate(ds['second']) if sv in source_rows[si]['low'])
    wrong = copy.deepcopy(ds); wrong['second'].pop(low_v); domain_damages.append(wrong)
    wrong = copy.deepcopy(ds); wrong['first'].pop(0); domain_damages.append(wrong)
    for wrong in domain_damages:
        (target/'domains.json').write_text(json.dumps(wrong)+'\n')
        result = subprocess.run(uv_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        verify.need(result.returncode == 1 and 'literal mark/orbit domains disagree' in result.stderr,
                    'semantic marked-domain gap or obsolete fourth point accepted or operational failure')

    # Independent literal check of the ordinary automatic-v bridge for all
    # first-star(u,y) pairs, without using v-mark counts as a substitute.
    automatic_v_pairs = 0
    for star in source_rows:
        for u, y in itertools.permutations(sorted(star['high']), 2):
            if star['replication'][y] != 4 or star['missing'][u] & star['high']:
                continue
            choices = star['missing'][y] & star['low']
            verify.need(choices and all(v != u and v != y and v not in star['missing'][u]
                for v in choices), 'automatic low-v neighbor bridge failed literally')
            verify.need(set((u, v, y) for v in choices) <= set(star['first']),
                        'automatic v witness absent from literal marking domain')
            automatic_v_pairs += 1
    print(json.dumps(dict(status='PASS_SEMANTIC_DAMAGE_AND_ACTUAL_TRANSPORT_CONTROLS',
                         fixture_damages=len(fixture_damage), bridge_damages=len(bridge_damage),
                         certificate_damages=len(cert_damage), primary_record_damages=len(mutations),
                         product_population_gap=1, invented_empty_uv_positive=1,
                         semantic_mark_domain_damages=len(domain_damages),
                         actual_empty_uv_product=uv_index, automatic_v_eligible_pairs=automatic_v_pairs,
                         relabelings=3, relabeled_stars=69,
                         transported_interfaces=transported_records), sort_keys=True))

if __name__ == '__main__':
    main()
