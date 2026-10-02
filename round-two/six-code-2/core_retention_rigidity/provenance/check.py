"""Check the actual point identification with the previously published ACL core.

six-code-2, researcher. The small ACL69 fixture is a credited byte copy of
the existing publication. This checks positive transports, not novelty.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def point_set(word):
    return frozenset(p for p in range(18) if word >> p & 1)


def verify(identification, seed_raw, instance, states):
    need(hashlib.sha256(seed_raw).hexdigest() == identification['prior_seed_sha256'], 'credited seed bytes changed')
    lines = seed_raw.decode().splitlines()
    need(len(lines) == 69 and all(len(s) == 18 and set(s) <= {'0', '1'} and s.count('1') == 5 for s in lines),
         'bad literal ACL69 rows')
    seed = tuple(frozenset(p for p, bit in enumerate(row) if bit == '1') for row in lines)
    mapping = identification['old_to_new_point_mapping']
    need(len(mapping) == 18 and sorted(mapping) == list(range(18)), 'nonbijective point transport')
    removed = identification['prior_removed_seed_rows']
    need(removed == [6, 9, 14, 17, 22, 27, 30, 32, 37, 54, 55, 58], 'wrong earlier source row definition')
    old_core = tuple(w for i, w in enumerate(seed, 1) if i not in removed)
    new_core = {point_set(w) for w in instance['core_words']}
    need(len(old_core) == len(new_core) == 57, 'wrong literal core count')
    images = {frozenset(mapping[p] for p in word) for word in old_core}
    need(images == new_core, 'literal old-to-new core transport fails')
    seed_image = frozenset(frozenset(mapping[p] for p in word) for word in seed)
    state_sets = tuple(frozenset(point_set(w) for w in state) for state in states)
    need(len(seed_image) == 69 and seed_image in state_sets, 'mapped ACL69 is not a literal present maximum')
    return state_sets.index(seed_image)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--states', type=Path, required=True)
    args = parser.parse_args()
    identification = json.loads((HERE / 'IDENTIFICATION.json').read_bytes())
    seed_raw = (HERE / 'acl69.txt').read_bytes()
    instance = json.loads((HERE.parent / 'INSTANCE.json').read_bytes())
    states = json.loads(args.states.read_bytes())
    index = verify(identification, seed_raw, instance, states)
    damages = []
    def rejects(label, data, seed_bytes):
        try:
            verify(data, seed_bytes, instance, states)
        except ValueError:
            damages.append({'label': label, 'rejected': True})
            return
        raise ValueError('damaged provenance accepted: ' + label)
    damaged = deepcopy(identification)
    damaged['old_to_new_point_mapping'][0] = damaged['old_to_new_point_mapping'][1]
    rejects('nonbijective actual transport', damaged, seed_raw)
    damaged = deepcopy(identification)
    damaged['old_to_new_point_mapping'][0], damaged['old_to_new_point_mapping'][1] = (
        damaged['old_to_new_point_mapping'][1], damaged['old_to_new_point_mapping'][0])
    rejects('bijective but false core transport', damaged, seed_raw)
    damaged = deepcopy(identification)
    damaged['prior_removed_seed_rows'][0] += 1
    rejects('altered prior source row definition', damaged, seed_raw)
    rejects('changed credited seed bytes', identification, seed_raw + b'\n')
    print(json.dumps({'agent': 'six-code-2', 'role': 'researcher',
                      'status': 'COMPLETE_POSITIVE_PRIOR_CORE_IDENTIFICATION',
                      'prior_graph_height': identification['prior_graph_height'],
                      'prior_graph_ref': identification['prior_graph_ref'],
                      'prior_source_commit': identification['prior_source_commit'],
                      'old_to_new_point_mapping': identification['old_to_new_point_mapping'],
                      'all57_core_word_images_exact': True,
                      'mapped_acl69_present_maximum_state_index': index, 'damage_controls': damages,
                      'scope': 'Prior retained55 upper69 and fixed57 maximum/component results are identified and credited; only equality rigidity at retained55 is a refinement.'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
