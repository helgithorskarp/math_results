"""derivation over QQ(q,k), characteristic zero.

SymPy 1.14.0 used only for exact expand/cancel/factor. No interpolation,
floating evaluation or modular reconstruction. Integer q>=3k,k>=2 gives
all positive denominators q,q-1,q-2,q-3 and a positive physical frame.
Every exported rational expression is specialized against calibrated
physical actions and ALL first/second/frame entries before use.
"""
from pathlib import Path
import sys
import json
import time
import resource
import residual

import sympy as sp
residual.require(sp.__version__ == '1.14.0', 'optional derivation requires SymPy 1.14.0')

q, k = sp.symbols('q k')


def choose(n, r):
    residual.require(r in (0, 1, 2), 'symbolic binomial degree <=2')
    return (sp.Integer(1), n, n*(n-1)/2)[r]


def base_table():
    o,p,a,b,c,d,e = (0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    out = {}
    def put(x,y,value):
        out[tuple(sorted((x,y)))] = sp.cancel(value)
    s = 3*q+4
    put(o,o,(6/q-q-4)/(q-1))
    put(o,p,q*(q-3)/((q-1)*(q-2)))
    put(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2))
    for leaf,alpha,beta,gamma in (
            (o,1-1/q,1+1/q,1+6/q),
            (p,1,1+2*(q-1)/(q*(q-2)),1+6/q)):
        for core,value in ((a,alpha),(c,alpha),(b,beta),(d,beta),(e,gamma)):
            put(leaf,core,value)
    rr = 3+2/q
    ww = (s-rr)/(q-1)
    for x,y,value in ((a,a,0),(a,b,0),(b,b,0),(a,c,2),
                       (a,d,rr),(b,c,rr),(b,d,ww)):
        put(x,y,value)
    return out


def rational_value(expr, qq, kk):
    value = expr.subs({q:qq, k:kk})
    residual.require(value.is_Rational, 'exact rational symbolic specialization')
    return residual.F(int(value.p), int(value.q))


def derive():
    keys = residual.orbits.forms(6,2)['keys']
    weights = [choose(k,z)*choose(q-k,w) for c,z,w in keys]
    vectors = [[sp.Integer(1),sp.Integer(c==1 and z+w==1),
                sp.Integer(bool(c&6) and not(c in (3,5) and z+w==0))]
               for c,z,w in keys]
    tab = base_table()
    n = (q*q+13*q+16)/2-k
    s, ell = 3*q+4, 5*q+4-k
    gap = n-s
    actions = []
    for i,(c,z,w) in enumerate(keys):
        sums = [gap*vectors[i][a] for a in range(3)]
        for j,(cc,zz,ww) in enumerate(keys):
            if c&cc:
                continue
            count = choose(k-z,zz)*choose(q-k-w,ww)
            entry = tab[tuple(sorted(((c.bit_count(),z+w),(cc.bit_count(),zz+ww))))]
            for a in range(3):
                if vectors[j][a]:
                    sums[a] -= count*entry
        actions.append([sp.cancel(x) for x in sums])
    frame = sp.Matrix(3,3,lambda a,b: sp.cancel(sum(weights[i]*vectors[i][a]*vectors[i][b]
                                                      for i in range(23))))
    first = sp.Matrix(3,3,lambda a,b: sp.cancel(sum(weights[i]*vectors[i][a]*actions[i][b]
                                                      for i in range(23))))
    second = sp.Matrix(3,3,lambda a,b: sp.cancel(sum(weights[i]*actions[i][a]*actions[i][b]
                                                       for i in range(23))))
    residual.require(frame == sp.Matrix([[n-1,q,ell],[q,q,0],[ell,0,ell]]),
                     'symbolic physical frame')
    residual.require(first == first.T and second == second.T, 'symbolic symmetry')
    # Explicit inverse keeps only the known positive frame denominator.
    r = sp.cancel(n-1-q-ell)
    inv = sp.Matrix([[1/r,-1/r,-1/r],[-1/r,1/q+1/r,1/r],[-1/r,1/r,1/ell+1/r]])
    residual.require((frame*inv-sp.eye(3)).applyfunc(sp.cancel) == sp.zeros(3),
                     'symbolic physical inverse')
    cross = (second-first*inv*first).applyfunc(sp.cancel)
    g = sp.cancel(n-2*s)
    sufficient = (first-cross/g).applyfunc(sp.cancel)
    # All functions and identities are calibrated against independently
    # original-validated exact Fraction actions, not floating fits.
    checks = []
    for qq,kk in ((19,5),(24,6),(74,15),(35,8),(46,10),(91,18)):
        data = residual.orbits.forms(qq,kk)
        actual = residual.moments(data)
        for name,value in (('frame',frame),('first',first),('second',second)):
            decoded = [[rational_value(value[a,b],qq,kk) for b in range(3)] for a in range(3)]
            residual.require(decoded == actual[name], 'all specialized moment entries: '+name)
        decoded = [[rational_value(x,qq,kk) for x in row] for row in actions]
        residual.require(decoded == actual['actions'], 'every specialized physical row action')
        record = residual.compare(qq,kk)
        decoded = [[rational_value(sufficient[a,b],qq,kk) for b in range(3)] for a in range(3)]
        residual.require(decoded == record['sufficient'], 'all specialized Schur comparisons')
        checks.append([qq,kk])
    def matrix_strings(m):
        return [[str(sp.factor(m[a,b])) for b in range(m.cols)] for a in range(m.rows)]
    result = {'agent':'six-downset-3','role':'researcher','status':'symbolic identities',
              'coefficient_field':'QQ(q,k), characteristic zero, ordered generators q,k',
              'SymPy_version':sp.__version__,'keys':keys,
              'actions':[[str(sp.factor(x)) for x in row] for row in actions],
              'frame':matrix_strings(frame),'first':matrix_strings(first),
              'second':matrix_strings(second),'residual':matrix_strings(cross),
              'sufficient':matrix_strings(sufficient),'calibrations':checks}
    result['record_sha256'] = residual.digest(result)
    Path(__file__).with_name('SYMBOLIC-MOMENTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result


if __name__=='__main__':
    start = time.perf_counter()
    result = derive()
    print(json.dumps({'digest':result['record_sha256'],'seconds':time.perf_counter()-start,
                      'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'symbolic_actions':result['actions'],'residual':result['residual']}))
