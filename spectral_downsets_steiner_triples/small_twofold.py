"""Compact deterministic validation inputs, not a twofold-design census.

At nine points retain the two old two-STS fixtures. At even orders develop
three displayed seeds over Z_(v-1), then add {i,i+1,infinity}. These simple
inputs are checked from their literal pair counts before any matrix is used.
The designs are validation inputs, not claimed new design constructions.
Author: six-downset-2, researcher.
"""
import json
from pathlib import Path
from certificates import mask
from uniform_twofold import design_data


def fixtures():
    old = json.loads(Path(__file__).with_name('two9_certificates.json').read_text())
    for index, case in enumerate(old['cases']):
        blocks = sorted(old['first_blocks']+case['second_blocks'])
        design_data(9, blocks)
        yield 'two_STS9_case_'+str(index), 9, blocks, {
            'kind': 'existing two-STS9 fixture', 'case_index': index,
            'first_blocks': old['first_blocks'], 'second_blocks': case['second_blocks']}
    for v, seeds in ((10, ((0, 1, 4), (0, 2, 4), (0, 3, 6))),
                     (12, ((0, 1, 4), (0, 2, 5), (0, 2, 6)))):
        modulus = v-1
        blocks = {mask((x+j) % modulus for x in seed)
                  for seed in seeds for j in range(modulus)}
        blocks.update(mask((i, (i+1) % modulus, modulus)) for i in range(modulus))
        blocks = sorted(blocks)
        design_data(v, blocks)
        yield 'rotational_'+str(v), v, blocks, {
            'kind': 'three developed finite seeds and infinity cycle',
            'finite_modulus': modulus, 'infinity_label': modulus,
            'seeds': [list(seed) for seed in seeds], 'infinity_pair_step': 1}
