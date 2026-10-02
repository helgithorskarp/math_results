"""Exact uniform r=2 quadrant certificates; ordinary original-space proof separate."""
from pathlib import Path
import sys, signal, time, json, resource
from fractions import Fraction as F
from model import parameters, fixed
from bivariate import P, R, ATOMS, PROBES, DEN_CACHE, atom, rational_value
from polynomial import clear_rows, bareiss_minors, identity
from exact import require


def sign_certificate(stage):
    def alarm(*_):
        raise TimeoutError('unchanged fixed60s two-heavy stage')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(60)
    ATOMS.clear(); PROBES.clear(); DEN_CACHE.clear()
    u, v = R(P({(1,0):1})), R(P({(0,1):1}))
    l, q = 2+u, 8+4*u+v
    N, J = 2*q+12+2*l, (q+10+2*l)*(2*q+8+2*l)-3*(q-1)
    for z in (l, l-1, l+1, l+7, q, q-1, q+1, q+2, q+3,
              N-1, N-7, N-q-7, N-q-4, N-1-(q+3), J, 2*l*l+6*l+9):
        atom(z.num)
    p = parameters(q, l, fraction=lambda a,b=1:R(a)/b, upper_bounds=True)
    rows = []
    if stage == 'norms':
        p['mu_floor_margin'] = p['mu']-q/6
        p['etaP_floor_margin'] = p['etaP']-2*q/3
        names = ('etaL','etaF','etaP','mu','alpha','beta','mu_floor_margin','etaP_floor_margin')
        for name in names:
            z = p[name]
            require(all(ATOMS[a].positive() for a in z.den), 'positive denominator '+name)
            require(z.num.positive(), 'uniform residual numerator '+name)
            atom(z.num)
            rows.append({'name':name, 'terms':len(z.num.a), 'degree':z.num.degree(),
                         'fingerprint':z.num.fingerprint(),
                         'positive_denominator_factors':[[ATOMS[a].fingerprint(),e] for a,e in sorted(z.den.items())],
                         'polynomial':[[list(ex),str(co)] for ex,co in sorted(z.num.a.items())],
                         'coefficient_denominator':z.num.den})
    else:
        for name in ('mu','alpha','beta','etaP','C','nuT','nuL'):
            require(p[name].num.positive(), 'positive norm reused '+name)
            atom(p[name].num)
        aug, tail, _, _ = fixed(q, l, fraction=lambda a,b=1:R(a)/b, upper_bounds=True)
        matrix = {'anti':p['anti'], 'pendant':p['pendant'], 'triangle':p['triangle'],
                  'augmented':aug, 'final':tail}[stage]
        A, domains, removals, constants = clear_rows(matrix)
        clearing = {'positive_row_denominator_factors':[[[ATOMS[a].fingerprint(),e] for a,e in sorted(d.items())] for d in domains],
                    'removed_positive_row_factors':[[[ATOMS[a].fingerprint(),e] for a,e in sorted(d.items())] for d in removals],
                    'primitive_positive_row_multipliers':constants}
        minors = bareiss_minors(A)
        for order, minor in enumerate(minors,1):
            negatives = sum(z<0 for z in minor.a.values())
            require(minor.positive(), 'positive uniform Schur '+stage+'/'+str(order))
            bounds, count = identity([row[:order] for row in A[:order]], minor)
            rows.append({'order':order,'terms':len(minor.a),'degree':minor.degree(),
                         'bounds':bounds,'full_grid_points':count,'fingerprint':minor.fingerprint(),
                         'polynomial':[[list(ex),str(co)] for ex,co in sorted(minor.a.items())],
                         'coefficient_denominator':minor.den})
    scalar_checks = 0
    for L,Q in ((2,8),(2,9),(3,12),(3,16),(4,16),(5,32),(10,100)):
        direct = parameters(Q,L,upper_bounds=True)
        for name in ('etaL','etaF','etaP','mu','alpha','beta','C','nuT','nuL','c','d','g','A','ast','Fp'):
            require(rational_value(p[name],(L-2,Q-4*L))==direct[name], 'scalar identity '+name)
            scalar_checks += 1
    signal.alarm(0)
    result = {'agent':'six-downset-1','role':'researcher','stage':stage,'domain':'l=2+u,q=4l+v,u,v>=0',
              'rows':rows, 'scalar_checks':scalar_checks,
              'status':'exact reduced signs; original-space bridge ordinary in PROOF.md'}
    if stage != 'norms': result['row_clearing'] = clearing
    return result
