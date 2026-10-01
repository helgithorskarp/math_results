"""Semantic damage and relabeling controls, including complete carrier inputs."""
import argparse
import copy
import itertools
import json
import subprocess
import sys
from pathlib import Path
import check_bridge
import verify

def reject(function, value):
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
    seeds = json.loads((here/'seed_certificates.json').read_text())
    damage = []
    def changed():
        value = copy.deepcopy(fixture)
        damage.append(value)
        return value
    changed()['stars'].pop()
    changed()['stars'][0][1] = copy.deepcopy(fixture['stars'][0][0])
    changed()['stars'][0][0][0] = 18
    changed()['stars'][0][0][0] = fixture['stars'][0][0][1]
    changed()['stars'][0][1] = [0, 1, 8, 11]
    changed()['groups'][9][0] = [0]*17
    changed()['groups'][9] = [g for g in fixture['groups'][9] if g != list(range(17))]
    false_map = list(range(17)); false_map[0], false_map[1] = 1, 0
    changed()['groups'][9] = [list(range(17)), false_map]
    generator = next(g for g in fixture['groups'][9] if [g[g[p]] for p in range(17)] != list(range(17)))
    changed()['groups'][9] = [list(range(17)), generator]
    changed()['groups'][9].append(copy.deepcopy(fixture['groups'][9][0]))
    for value in damage:
        reject(verify.inspect, value)
    baseline = verify.inspect(fixture)
    for a, b in ((5, 3), (11, 9), (16, 0)):
        pi = [(a*p+b) % 17 for p in range(17)]
        inverse = [pi.index(p) for p in range(17)]
        transported = copy.deepcopy(fixture)
        transported['stars'] = [[[pi[p] for p in q] for q in Q] for Q in fixture['stars']]
        transported['groups'] = [[[pi[g[inverse[p]]] for p in range(17)] for g in G] for G in fixture['groups']]
        result = verify.inspect(transported)
        verify.need([(len(r['first']), len(r['second']), len(r['first_orbits']), len(r['second_orbits'])) for r in result] ==
                    [(len(r['first']), len(r['second']), len(r['first_orbits']), len(r['second_orbits'])) for r in baseline],
                    'literal relabeling changed marking populations')
    bridge_damage = []
    def change_bridge():
        value = copy.deepcopy(bridge); bridge_damage.append(value); return value
    change_bridge()['raw_positive_maps'].pop()
    change_bridge()['raw_positive_maps'][1] = copy.deepcopy(bridge['raw_positive_maps'][0])
    change_bridge()['raw_positive_maps'][0]['point_map'][0] = bridge['raw_positive_maps'][0]['point_map'][1]
    change_bridge()['raw_positive_maps'][0]['word_masks'][0] |= 1 << 18
    change_bridge()['raw_positive_maps'][0]['triangle_points'] = []
    survivor = next(i for i, r in enumerate(bridge['raw_positive_maps']) if not r['triangle_points'])
    change_bridge()['raw_positive_maps'][survivor]['triangle_points'] = [14]
    change_bridge()['raw_positive_maps'][0]['first'][0] = 17
    for value in bridge_damage:
        reject(lambda item: check_bridge.check(item, fixture, seeds), value)
    seed_damage = []
    def change_seed():
        value = copy.deepcopy(seeds); seed_damage.append(value); return value
    change_seed()['seeds'][0]['candidate_count'] -= 1
    change_seed()['seeds'][0]['candidate_sha256'] = '0'*64
    change_seed()['seeds'][0]['colors'].pop()
    change_seed()['seeds'][0]['saturated_centers'] = [17, 10]
    value = change_seed(); value['seeds'][0]['colors'] = [0]*118
    value['seeds'][0]['capacity'] = 1; value['seeds'][0]['upper_bound'] = 37
    for value in seed_damage:
        reject(lambda item: check_bridge.check(bridge, fixture, item), value)
    target = Path(args.work); target.mkdir(parents=True, exist_ok=True)
    primary = Path(args.primary_work)
    (target/'domains.json').write_bytes((primary/'domains.json').read_bytes())
    positive = json.loads((primary/'product-042.json').read_text())
    mutations = []
    def change_product():
        value = copy.deepcopy(positive); mutations.append(value); return value
    change_product()['status'] = 'INCOMPLETE'
    change_product()['product_index'] = 43
    change_product()['counts']['partial_maps'] -= 1
    change_product()['partial_maps_sha256'] = '0'*64
    change_product()['positives'] = []
    change_product()['positives'][0]['point_map'][0] += 1
    change_product()['positives'][0]['triangle_points'] = [14]
    command = [sys.executable, str(here/'verify.py'), '--fixtures', str(here/'fixtures.json'),
               '--primary-work', str(target), '--output', str(target/'result.json'), '--first', '42', '--finish', '43']
    if sys.flags.optimize:
        command.insert(1, '-O')
    def run(value):
        (target/'product-042.json').write_text(json.dumps(value)+'\n')
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    successful = run(positive)
    verify.need(successful.returncode == 0, 'undamaged carrier control failed')
    for value in mutations:
        result = run(value)
        verify.need(result.returncode == 1 and 'ValueError:' in result.stderr, 'damaged carrier record accepted or operational failure')
    inventory_command = command[:-4]
    # Default whole-domain mode must reject a directory containing only one product.
    result = subprocess.run(inventory_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    verify.need(result.returncode == 1 and 'primary product population gap' in result.stderr, 'whole carrier gap accepted')
    print(json.dumps(dict(status='PASS_SEMANTIC_DAMAGE_AND_RELABEL_CONTROLS', fixture_damages=len(damage),
                         bridge_damages=len(bridge_damage), seed_damages=len(seed_damage),
                         primary_record_damages=len(mutations), product_population_gap=1,
                         relabelings=3, relabeled_stars=69), sort_keys=True))

if __name__ == '__main__':
    main()
