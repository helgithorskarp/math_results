"""Semantic damage controls for hypothesis, weights, completeness and PSD."""
from fractions import Fraction as F
from math import comb
import pins
from variance import require, row_classes, scalar_record
from entries import parameters, certificate
from exact import schur_psd, polynomial_psd
from algebra import positive_shift


def census(state):
    keys, sizes = state['keys'], state['sizes']
    require(len(keys) == len(sizes) == 23 and len(set(keys)) == 23 and sum(sizes) == 445,
            'complete original23 fixed orbits')
    require(all(size == comb(6, key[1])*comb(18, key[2])
                for key, size in zip(keys, sizes)), 'actual binomial orbit norms')
    require(445-len(keys) == 422, 'entire omitted-space dimension')


def star_kernel(G, state):
    require(all(sum(G[i][j]*state['star'][j] for j in range(23)) == 0
                for i in range(23)), 'actual lower greatest-star kernel')


def run(state):
    rejected = []

    def reject(name, call):
        try:
            call()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Damaged mathematical input accepted: '+name)

    census(state)
    star_kernel(state['G'], state)
    reject('boolean ground order', lambda: parameters(True, 5))
    from point import domain
    reject('expanded singleton matrix guard', lambda: domain(25, 6))
    reject('negative sufficient variance promoted to positive cap',
           lambda: parameters(24, 6, variance_only=True))
    p, M = certificate(24, 6)
    reject('deleted triangle supplied as surviving original member', lambda: M(14, 0))
    reject('oversized original member', lambda: M(15, 0))
    damaged = dict(state)
    damaged['keys'], damaged['sizes'] = state['keys'][:-1], state['sizes'][:-1]
    reject('omitted complete fixed-space orbit', lambda: census(damaged))
    damaged = dict(state)
    damaged['sizes'] = state['sizes'][:]
    damaged['sizes'][0] += 1
    damaged['sizes'][1] -= 1
    reject('wrong norm weights with unchanged total dimension', lambda: census(damaged))
    broken = [row[:] for row in state['G']]
    a = state['keys'].index((1, 0, 0))
    b = state['keys'].index((2, 0, 0))
    broken[a][b] -= 10
    broken[b][a] -= 10
    reject('one original repair sign reversed', lambda: star_kernel(broken, state))
    reject('changed all-k coefficient certificate',
           lambda: positive_shift([-479, -4224, -18655, 1600], 19,
                                  [4159209, 1019686, 72545, 1600]))
    reject('changed pinned executable input',
           lambda: pins.setup({next(iter(pins.PINS)): '0'*64}))
    reject('zero diagonal with nonzero row treated as PSD',
           lambda: schur_psd([[0, 1], [1, 0]]))
    reject('negative-root characteristic criterion weakened',
           lambda: polynomial_psd([[0, 1], [1, 0]]))
    require(schur_psd([[1, 1], [1, 1]]) == polynomial_psd([[1, 1], [1, 1]])[0] == 1,
            'positive singular PSD control remains accepted')
    # Wrong slope norm/repair budget cannot justify the claimed positive floor.
    r = scalar_record(19, 5)
    mu = F(r['nonempty_cap_floor_at_zero'])
    reject('arbitrary large parameter asserted within perturbation budget',
           lambda: require(16*(3*19+4)*F(1, 8)+F(1, 96) < mu/4,
                           'claimed perturbation exceeds certified budget'))
    # Verify the scalar failure remains a failure even though another point exists.
    require(F(scalar_record(24, 6)['strict_scalar_margin']) < 0 and
            p['mechanism'] == 'complete23-orbit exceptional point',
            'distinct exceptional certificate, no reinterpretation of failed estimate')
    return {'damage_rejections': len(rejected), 'rejected': rejected,
            'positive_controls': 2, 'scope': 'Same-author controls, not peer review'}
