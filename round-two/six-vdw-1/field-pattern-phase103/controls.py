"""Actual positive witnesses/cores and semantic certificate damage controls."""
from copy import deepcopy
import json
from pathlib import Path

from check import base_check, need


def tiny_core(complement=False):
    # Square-set oracle is separate from Euler producer and Gauss checker.
    q = 7
    squares = {x*x % q for x in range(1,q)}
    roots = [1,2,4]
    types = {x:tuple(int((x-r) % q not in squares) for r in roots)
             for x in range(1,q) if x not in roots}
    sigma = [0,0,0,1,1,1]
    phases = {x: [sigma[(s+x) % 6] ^ int(complement) for s in range(6)] for x in range(1,q)}
    word = [None if n % q == 0 else phases[n % q][n % 6] for n in range(6*q)]
    need(len(set(types.values())) == 3, 'actual three tiny character classes')
    return word


def check_tiny_word(word):
    q, M = 7, 42
    need(len(word) == M, 'entire original42 word required')
    need([i for i,v in enumerate(word) if v is None] == list(range(0,M,q)),
         'only physical pole omitted; every original root is colored')
    need(all(v is None or type(v) is int and v in [0,1] for v in word), 'binary literal word')
    domain = regular = 0
    for a in range(M):
        for d in range(1,M):
            domain += 1
            values = [word[(a+j*d) % M] for j in range(7)]
            if None in values:
                continue
            regular += 1
            need(len(set(values)) != 1, 'actual tiny monochromatic AP: '+str((a,d)))
    need((domain,regular) == (1722,180), 'whole tiny original AP domain')
    return {'domain':domain,'regular':regular,'poles':domain-regular,'roots_colored':18}


def canonical(rows):
    return ''.join(','.join(map(str,row))+'\n' for row in rows).encode()


def run():
    here = Path(__file__).resolve().parent
    raw = (here/'five-packs.csv').read_bytes()
    kernel = json.loads((here/'four-APs.json').read_bytes())
    base_check(raw,kernel)  # all640 actual positive certificates, not a fabricated return.
    rows = [[int(v) for v in line.split(',')] for line in raw.decode().splitlines()]
    damages = []
    def reject(name, data, damaged_kernel):
        try:
            base_check(data,damaged_kernel)
        except (ValueError,KeyError,TypeError) as error:
            damages.append({'damage':name,'error':str(error)})
        else:
            raise ValueError('actual semantic damage accepted: '+name)
    reject('missing actual Boolean case',canonical(rows[:-1]),deepcopy(kernel))
    shifted = deepcopy(rows)
    shifted[0],shifted[1] = shifted[1],shifted[0]
    reject('swapped actual case order',canonical(shifted),deepcopy(kernel))
    duplicate = deepcopy(rows)
    duplicate[1][0] = duplicate[0][0]
    reject('duplicated actual truth state',canonical(duplicate),deepcopy(kernel))
    repeated = deepcopy(rows)
    repeated[0][3:5] = repeated[0][1:3]
    reject('physical supports really overlap',canonical(repeated),deepcopy(kernel))
    root_hit = deepcopy(rows)
    root_hit[0][1:3] = [1,5]
    reject('actual original root hit',canonical(root_hit),deepcopy(kernel))
    pole_hit = deepcopy(rows)
    pole_hit[0][1:3] = [0,5]
    reject('actual physical pole hit',canonical(pole_hit),deepcopy(kernel))
    zero_step = deepcopy(rows)
    zero_step[0][2] = 0
    reject('actual zero progression step',canonical(zero_step),deepcopy(kernel))
    # Find a genuine regular nonmonochromatic witness under table2.
    squares = {x*x % 103 for x in range(1,103)}
    labels = {x:sum(int((x-r) % 103 not in squares) << (2-j) for j,r in enumerate([1,2,4]))
              for x in range(1,103) if x not in [1,2,4]}
    bad_pair = None
    for a in range(103):
        for d in range(1,52):
            xs = [(a+j*d) % 103 for j in range(7)]
            if all(x in labels for x in xs) and len({(2 >> labels[x]) & 1 for x in xs}) > 1:
                bad_pair = [a,d]
                break
        if bad_pair is not None:
            break
    need(bad_pair is not None, 'actual nonmonochromatic damage fixture')
    mixed = deepcopy(rows)
    mixed[1][1:3] = bad_pair
    reject('actual full-table monochromaticity false',canonical(mixed),deepcopy(kernel))
    omitted_root = deepcopy(kernel)
    omitted_root['roots'] = [1,2]
    reject('ignored input root silently removed',raw,omitted_root)
    wrong_pole = deepcopy(kernel)
    wrong_pole['pole'] = 1
    reject('physical pole moved without transport',raw,wrong_pole)
    false_leaf = deepcopy(kernel)
    false_leaf['APs'][0][1] = 18
    reject('actual kernel coordinate changed',raw,false_leaf)
    reject('whole certificate newline missing',raw[:-1],deepcopy(kernel))
    positives = [check_tiny_word(tiny_core()),check_tiny_word(tiny_core(True))]
    tiny_damages = []
    for name,word in [('actual field-constant bad phase word',[None if n%7 == 0 else 0 for n in range(42)]),
                      ('actual root point improperly omitted',tiny_core())]:
        if name.startswith('actual root'):
            word[1] = None
        try:
            check_tiny_word(word)
        except ValueError as error:
            tiny_damages.append({'damage':name,'error':str(error)})
        else:
            raise ValueError('actual bad tiny word accepted')
    need(len(damages) == 12 and len(tiny_damages) == 2, 'all declared actual controls')
    return {'author':'six-vdw-1','role':'researcher','status':'ACTUAL_POSITIVE_AND_SEMANTIC_DAMAGE_CONTROLS_PASS',
            'actual_F103_positive_five_pack_APs':640,'positive_original_q7_cores':positives,
            'semantic_certificate_damages':damages,'actual_tiny_word_damages':tiny_damages,
            'genuine_nonmonochromatic_fixture':bad_pair,'external_review_claimed':False}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True))
