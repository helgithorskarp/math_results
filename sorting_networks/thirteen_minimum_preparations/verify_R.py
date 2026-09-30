"""Scalar audit of the private common maximum-front target and19 control.
Author: six-sorting-1, researcher. Imports no generator or solver.
"""
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def scalar(values, word):
    values = list(values)
    for a, b in word:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def main():
    start = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    packet = fixture['R137']
    B = [(6, 9), (9, 10)]
    word = [tuple(gate) for gate in fixture['known21_suffix']]
    swaps = 0
    for target, gate in enumerate(B):
        position = word.index(gate)
        while position > target:
            assert set(gate).isdisjoint(word[position - 1])
            word[position], word[position - 1] = word[position - 1], word[position]
            position -= 1
            swaps += 1
    assert word[:2] == B and word[2:] == [tuple(gate) for gate in packet['known19_control']]
    assert swaps == packet['disjoint_commutations_checked'] == 14
    checked = 0
    for record in packet['prefixes']:
        case = record['case']
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)] + [list(gate) for gate in B]
        assert prefix == record['prefix26'] and len(prefix) == 26
        image = set()
        for mask in range(8192):
            values = [int(bool(mask & (1 << i))) for i in range(13)]
            out = scalar(values, prefix)
            assert out[10:] == sorted(values)[-3:]
            image.add(sum(out[i] << i for i in range(10)))
            assert scalar(out, packet['known19_control']) == sorted(values)
            checked += 1
        assert image == set(record['states']) == set(packet['states']) and len(image) == 137
    assert checked == 16384
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'Scalar R137 and full45 control audit passed',
              'common_rows': 137, 'original_inputs_checked': checked,
              'known_suffix_size': 19, 'disjoint_commutations': swaps,
              'elapsed_seconds': time.monotonic() - start,
              'scope': 'Checked conditional construction frontier R137=18..19; existence at18 gives global44, exclusion at18 covers only the binary maximum subclass'}
    print(json.dumps(result))


if __name__ == '__main__':
    main()
