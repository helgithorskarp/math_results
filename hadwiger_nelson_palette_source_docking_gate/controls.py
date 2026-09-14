"""Independent prime-mask norm expansion and certificate fault controls."""
import copy
import json
from itertools import combinations
from math import prod
import verify as v

PRIMES = (3, 5, 7, 11)
RAD = tuple(prod(p for i, p in enumerate(PRIMES) if m >> i & 1) for m in range(16))


def norm(x):
    out = [0] * 16
    for axis in (0, 16):
        for i, a in enumerate(x[axis:axis+16]):
            for j, b in enumerate(x[axis:axis+16]):
                out[i ^ j] += a * b * RAD[i & j]
    return tuple(out)


def run():
    g, f, gd, fd, *rest = v.geometry()
    gg = []
    for row in g:
        q = [0]*32
        for axis in (0, 1):
            for i, radical in enumerate(v.RAD):
                q[16*axis + RAD.index(radical)] = row[8*axis+i]
        gg.append(q)
    ff = []
    for a, b, c, d in f:
        q = [0]*32
        q[0], q[9], q[17], q[24] = a, b, c, d
        ff.append(q)
    for (a, b), want in gd.items():
        got = norm([x-y for x, y in zip(gg[a], gg[b])])
        expected = [0]*16
        for i, radical in enumerate(v.RAD):
            expected[RAD.index(radical)] = want[i]
        v.need(got == tuple(expected), 'independent G norm')
    for (a, b), want in fd.items():
        got = norm([x-y for x, y in zip(ff[a], ff[b])])
        expected = [0]*16
        expected[0], expected[9] = want
        v.need(got == tuple(expected), 'independent F norm')
    # Brute subset clique check, independently of the matching argument.
    compatible = set(rest[2])
    cliques = [s for k in range(9) for s in combinations(v.T, k)
               if all(ab in compatible for ab in combinations(s, 2))]
    v.need(max(map(len, cliques)) == 2, 'all 256 terminal subsets')
    cert = json.loads((v.HERE/'certificate.json').read_text())
    trials = []
    bad = copy.deepcopy(cert); bad['pair_words'].pop(); trials.append(bad)
    bad = copy.deepcopy(cert); bad['pair_words'][0]['word'] = '0'*29; trials.append(bad)
    bad = copy.deepcopy(cert); bad['pair_words'][1]['second_colour'] = 0; trials.append(bad)
    bad = copy.deepcopy(cert); bad['pair_words'][0]['pair'] = [0, 1]; trials.append(bad)
    bad = copy.deepcopy(cert)
    # A proper colour permutation with wrong named pins must also fail.
    bad['pair_words'][0]['word'] = bad['pair_words'][0]['word'].translate(str.maketrans('0123','1230'))
    trials.append(bad)
    for bad in trials:
        try:
            v.verify(bad)
        except ValueError:
            continue
        raise ValueError('accepted corrupted certificate')
    return {'status': 'CONTROLS_PASS', 'independent_norm_vectors': 434,
            'terminal_subsets': 256, 'rejected_corruptions': len(trials)}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
