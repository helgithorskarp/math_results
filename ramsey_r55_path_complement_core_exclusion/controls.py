"""Full physical-interface controls; zero target search or solver calls."""
from itertools import combinations
import copy
import json
from pathlib import Path
from interface import inspect
from verify_certificate import verify


def candidate(mode, reverse=False, permute=False):
    # Modes 0/1: complete/empty core. Mode 2: C5[C5] joined to a
    # universal vertex. Mode 3: an explicitly ordered path in the core.
    labels = [(7*i+11) % 43 if permute else i for i in range(43)]
    edges = set()
    for i, j in combinations(range(43), 2):
        if j < 26:
            if mode in (0, 1):
                bit = 1-mode
            elif mode == 2:
                bit = (j == 25 or (i//5 == j//5 and (i-j) % 5 in (1, 4)) or
                       (i//5 != j//5 and (i//5-j//5) % 5 in (1, 4)))
            else:
                bit = j < 5 and j == i+1
        else:
            # Arbitrary deterministic outside incidences do not enter the proof.
            bit = (i*i+3*i*j+7*j+mode) % 11 < 5
        if bool(bit) != reverse:
            edges.add(tuple(sorted((labels[i], labels[j]))))
    word = sum(1 << k for k, uv in enumerate(combinations(range(43), 2)) if uv in edges)
    return {'n': 43, 'red_bits_hex': format(word, '0226x'),
            'core': sorted(labels[:26])}


def main():
    counts = {}
    for mode in range(4):
        for reverse in (False, True):
            for permute in (False, True):
                g = candidate(mode, reverse, permute)
                answer = inspect(g)
                verify(g, answer['certificate'])
                key = answer['status']
                counts[key] = counts.get(key, 0)+1
                if (key.startswith('EXCLUDED_')) != (mode != 3):
                    raise ValueError('wrong classification')
                if mode != 3 and answer['core_five_sets_checked'] != 65780:
                    raise ValueError('incomplete family-membership check')
    rejected = []
    g = candidate(2)
    for name, mutate in [
        ('wrong_order', lambda x: x.__setitem__('n', 42)),
        ('short_core', lambda x: x['core'].pop()),
        ('duplicate_label', lambda x: x['core'].__setitem__(1, 0)),
        ('unsorted_core', lambda x: x['core'].reverse()),
        ('unused_high_bit', lambda x: x.__setitem__('red_bits_hex', format(2**903, '0226x'))),
        ('boolean_label', lambda x: x['core'].__setitem__(0, False)),
    ]:
        bad = copy.deepcopy(g)
        mutate(bad)
        try:
            inspect(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted malformed input')
    for mode in (2, 3):
        g = candidate(mode)
        cert = inspect(g)['certificate']
        for name, mutate in [
            ('color', lambda c: c.__setitem__('color', 1-c['color'])),
            ('duplicate', lambda c: c['vertices'].__setitem__(0, c['vertices'][1])),
            ('kind', lambda c: c.__setitem__('kind', 'unverified')),
        ]:
            bad = copy.deepcopy(cert)
            mutate(bad)
            try:
                verify(g, bad)
            except ValueError:
                rejected.append(str(mode)+'_'+name)
            else:
                raise ValueError('accepted corrupt certificate')
    return {'status': 'VERIFIED_PHYSICAL_CLASS_INTERFACE', 'full_graph_controls': 16,
            'outcomes': counts, 'rejected_inputs_or_certificates': rejected,
            'target_searches': 0, 'solver_calls': 0}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
