#!/usr/bin/env python3
"""Exact finite corroboration of low-energy coefficient entry.

All universal polynomial comparisons use every coefficient. Analytic/norm
inequalities, root-disk positivity and imported theorems remain written proof.
No floats, external packages, solvers, grids, or author/reviewer fixtures.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys

N = 18
ZERO = (0,) * N

def need(condition, message):
    if not condition:
        raise ValueError(message)

def const(value):
    value = Q(value)
    return {ZERO: value} if value else {}

def var(axis):
    mon = list(ZERO); mon[axis] = 1
    return {tuple(mon): Q(1)}

def add(*items):
    out = {}
    for p in items:
        for mon, value in p.items():
            v = out.get(mon, Q(0)) + value
            if v: out[mon] = v
            else: out.pop(mon, None)
    return out

def scale(p, value):
    value = Q(value)
    return {m: v * value for m, v in p.items() if v * value}

def mul(p, q):
    out = {}
    for m, v in p.items():
        for n, w in q.items():
            mon = tuple(a + b for a, b in zip(m, n))
            value = out.get(mon, Q(0)) + v * w
            if value: out[mon] = value
            else: out.pop(mon, None)
    return out

def power(p, n):
    out = const(1)
    for _ in range(n): out = mul(out, p)
    return out

def subst(p, axis, replacement):
    out = {}; cache = {0: const(1)}
    for mon, value in p.items():
        k = mon[axis]
        if k not in cache: cache[k] = power(replacement, k)
        rem = list(mon); rem[axis] = 0
        for a, b in mul({tuple(rem): value}, cache[k]).items():
            v = out.get(a, Q(0)) + b
            if v: out[a] = v
            else: out.pop(a, None)
    return out

def gc(value=0, imag=0): return const(value), const(imag)
def gv(axis): return var(axis), var(axis + 1)
def ga(*gs): return add(*(g[0] for g in gs)), add(*(g[1] for g in gs))
def gs(g, value): return scale(g[0], value), scale(g[1], value)
def gj(g): return g[0], scale(g[1], -1)
def gm(g, h):
    return (add(mul(g[0], h[0]), scale(mul(g[1], h[1]), -1)),
            add(mul(g[0], h[1]), mul(g[1], h[0])))
def gn(g): return add(power(g[0], 2), power(g[1], 2))
def gp(g, n):
    out = gc(1)
    for _ in range(n): out = gm(out, g)
    return out
def gsubst(g, axis, p): return subst(g[0], axis, p), subst(g[1], axis, p)

def ca(*arrays): return [ga(*(a[k] for a in arrays)) for k in range(9)]
def cs(a, value): return [gs(g, value) for g in a]
def cj(a): return [gj(a[-k % 9]) for k in range(9)]
def cm(a, b):
    out = [gc() for _ in range(9)]
    for i in range(9):
        for j in range(9): out[(i + j) % 9] = ga(out[(i + j) % 9], gm(a[i], b[j]))
    return out

def weight(d):
    b = [gc(9)] + [gs(d[k], k) for k in range(1, 9)]
    return ca(cm(b, cj(d)), cm(cj(b), d), cs(cm(d, cj(d)), -9))

def scalar(q):
    need(isinstance(q, Q), 'nonrational record')
    return [q.numerator, q.denominator]

def poly_record(p):
    values = [[list(m), scalar(v)] for m, v in sorted(p.items())]
    text = json.dumps(values, separators=(',', ':'))
    return {'terms': len(values), 'entire_coefficients_sha256': sha256(text.encode()).hexdigest()}

def typed_equal(a, b):
    if type(a) is not type(b): return False
    if isinstance(a, dict): return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in a)
    if isinstance(a, list): return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b

def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate fixture field')
        out[key] = value
    return out

def reject_float(value): raise ValueError('noninteger fixture number: ' + value)

def generate():
    controls = []; margins = []; damages = []
    def pid(name, p, q):
        need(p == q, 'whole polynomial differs: ' + name)
        controls.append({'name': name, **poly_record(p)})
    def gid(name, g, h):
        need(g == h, 'whole Gaussian polynomial differs: ' + name)
        controls.append({'name': name, 'real': poly_record(g[0]), 'imag': poly_record(g[1])})
    def positive(name, value):
        need(value > 0, 'nonpositive full-window budget: ' + name)
        margins.append({'name': name, 'value': scalar(value)})
    def damaged(name, accepted):
        need(not accepted, 'mathematical damage accepted: ' + name)
        damages.append(name)

    # Nine free complex d coefficients; no conjugation symmetry is imposed.
    d = [gv(2 * k) for k in range(9)]
    w = weight(d)
    alt = cs(ca(d, cj(d)), 9)
    for i in range(9):
        for j in range(9):
            k = (i - j) % 9
            alt[k] = ga(alt[k], gs(gm(d[i], gj(d[j])), i + j - 9))
    for k in range(9): gid('full cyclic weight frequency ' + str(k), w[k], alt[k])
    mean = add(scale(d[0][0], 18),
               *(scale(gn(d[k]), 2 * k - 9) for k in range(9)))
    gid('full cyclic mean including negative constant norm', w[0], (mean, {}))
    q1 = ga(*(gs(gm(d[j + 1], gj(d[j])), 2 * j - 8) for j in range(8)),
            gs(gm(d[0], gj(d[8])), -1))
    q2 = ga(*(gs(gm(d[j + 2], gj(d[j])), 2 * j - 7) for j in range(7)),
            gs(gm(d[0], gj(d[7])), -2))
    gid('full first Fourier row with wrap', w[1], ga(gs(ga(d[1], gj(d[8])), 9), q1))
    gid('full second Fourier row with zero extra wrap', w[2], ga(gs(ga(d[2], gj(d[7])), 9), q2))
    for k in range(1, 5): gid('whole real weight conjugacy ' + str(k), w[k], gj(w[9-k]))

    # Independent literal actual-root construction: entire nine cyclic
    # coefficients of the division-free positivity product identity.
    def ordinary_product(roots):
        coef = [gc(1)]
        for root in roots:
            out = [gc() for _ in range(len(coef) + 1)]
            for k, ck in enumerate(coef):
                out[k] = ga(out[k], gs(gm(ck, root), -1))
                out[k+1] = ga(out[k+1], ck)
            coef = out
        return coef
    e = Q(1, 65536); E = Q(1, 256); delta = Q(1, 1000)
    marked = gc(1-e)
    literal_cases = [
        ('eight_originals_at_zero', [marked] + [gc()] * 8),
        ('all_originals_coalesced_interior', [gc(Q(1,2),Q(1,3))] * 9),
        ('boundary_zero_at_sample', [marked,gc(1),gc(-1),gc(0,1),gc(0,-1),
             gc(Q(1,2)),gc(Q(1,2)),gc(0,Q(1,2)),gc(Q(1,2),Q(1,2))]),
        ('asymmetric_complex_repeated_originals', [marked,gc(Q(1,3),Q(1,4)),
             gc(Q(1,3),Q(1,4)),gc(Q(-1,2),Q(1,3)),gc(Q(1,4),Q(-1,3)),
             gc(Q(1,2)),gc(Q(-1,2)),gc(),gc(0,Q(1,2))]),
    ]
    for name, roots in literal_cases:
        coef = ordinary_product(roots)
        need(coef[-1] == gc(1), 'literal original not monic')
        ds = coef[:9]; ds[0] = ga(ds[0], gc(1))
        wc = weight(ds)
        factors = []
        for root in roots:
            norm = gn(root).get(ZERO, Q(0))
            need(norm <= 1, 'literal original outside disk')
            f = [gc() for _ in range(9)]
            f[0] = gc(1+norm); f[1] = gs(gj(root), -1); f[8] = gs(root, -1)
            factors.append((norm, f))
        rhs = [gc() for _ in range(9)]
        for j in range(9):
            product = [gc(1)] + [gc() for _ in range(8)]
            for k in range(9):
                if k != j: product = cm(product, factors[k][1])
            rhs = ca(rhs, cs(product, 1-factors[j][0]))
        for k in range(9):
            need(wc[k] == rhs[k], 'entire literal positivity product differs')
        controls.append({'name': 'complete actual-original positivity ' + name,
                         'all_original_coefficients': [
                             {'real': scalar(g[0].get(ZERO,Q(0))),
                              'imag': scalar(g[1].get(ZERO,Q(0)))} for g in coef],
                         'all_cyclic_weight_coefficients': [
                             {'real': scalar(g[0].get(ZERO,Q(0))),
                              'imag': scalar(g[1].get(ZERO,Q(0)))} for g in wc]})

    # Eight free complex criticals; every full coefficient of Newton2/3.
    crit = [gv(2*j) for j in range(8)]
    u = ga(*crit); t2 = ga(*(gp(g, 2) for g in crit)); t3 = ga(*(gp(g, 3) for g in crit))
    es2 = ga(*(gm(crit[j],crit[k]) for j,k in combinations(range(8),2)))
    es3 = ga(*(gm(gm(crit[j],crit[k]),crit[l]) for j,k,l in combinations(range(8),3)))
    gid('entire complex seventh coefficient Newton identity',
        gs(es2,Q(9,7)),gs(ga(gp(u,2),gs(t2,-1)),Q(9,14)))
    gid('entire complex sixth coefficient Newton identity',gs(es3,Q(-3,2)),
        ga(gs(gp(u,3),Q(-1,4)),gs(gm(u,t2),Q(3,4)),gs(t3,Q(-1,2))))
    pid('whole first critical mean norm scale',gn(u),scale(gn(gs(u,Q(-9,8))),Q(64,81)))

    # Eight free complex original coefficients with eta/z as axes16/17.
    eta = var(16); z = var(17); a = add(const(1),scale(eta,-1))
    ck = [None] + [gv(2*(k-1)) for k in range(1,9)]
    anchor = ga(gs((power(a,9),{}),-1),
                *(gs(gm(ck[k],(power(a,k),{})),-1) for k in range(1,9)))
    original = ga((power(z,9),{}),anchor,
                  *(gm(ck[k],(power(z,k),{})) for k in range(1,9)))
    gid('entire actual anchored original evaluated at marked root',gsubst(original,17,a),gc())
    for m in (7,8,9):
        pid('entire geometric anchor difference ' + str(m),
            add(const(1),scale(power(a,m),-1)),
            mul(eta,add(*(power(a,j) for j in range(m)))))
    numerator = add(scale(power(a,2),8),
                    scale(mul(add(const(8),scale(eta,3)),power(a,3)),-1))
    pid('entire cleared low-sublevel numerator',numerator,
        add(scale(eta,5),scale(power(eta,2),-7),
            scale(power(eta,3),-1),scale(power(eta,4),3)))

    # Full phase comparison, scalar majorants, and both bootstrap costs.
    eta,x,y,L,c1,c2,A,B = [var(j) for j in range(8)]
    aa = add(const(1),scale(eta,-1)); kap=Q(113,512); beta=Q(151,2304)
    left = add(scale(mul(aa,A),Q(8,9)),scale(B,Q(7,6)),scale(y,-Q(14,9)*kap))
    comparison = add(scale(add(A,B),Q(8,9)),scale(y,-beta),scale(mul(eta,x),Q(8,9)))
    pid('whole phase comparison nonnegative decomposition',
        add(comparison,scale(left,-1)),
        add(scale(add(y,scale(B,-1)),Q(5,18)),
            scale(mul(eta,add(x,A)),Q(8,9))))
    slow = add(scale(eta,Q(45,8)),scale(y,Q(151,2048)),scale(power(eta,2),-9),
               scale(power(x,2),Q(-8,9)),scale(mul(eta,x),-1))
    dmean = add(scale(add(scale(eta,9),scale(slow,-1),scale(mul(eta,x),8),
                         scale(mul(eta,y),7),L),2),
                scale(power(x,2),Q(7,9)),scale(power(y,2),Q(5,9)),scale(power(L,2),Q(1,3)))
    dfinal = add(scale(eta,Q(27,4)),scale(y,Q(-151,1024)),scale(power(eta,2),18),
                 scale(mul(eta,x),18),scale(mul(eta,y),14),scale(L,2),
                 scale(power(x,2),Q(23,9)),scale(power(y,2),Q(5,9)),scale(power(L,2),Q(1,3)))
    pid('whole retained mean upper bound',dmean,dfinal)
    D0=add(scale(eta,9),x,y,L)
    xp=add(dfinal,c1,scale(add(mul(D0,x),scale(mul(x,y),6),
                 scale(mul(D0,c1),8),scale(power(L,2),8),scale(mul(y,L),4)),Q(1,9)))
    yp=add(dfinal,c2,scale(add(scale(mul(D0,y),2),scale(mul(D0,c2),7),
                 scale(power(L,2),7),scale(mul(y,L),3),scale(mul(x,L),5)),Q(1,9)))
    expanded_x=add(scale(eta,Q(27,4)),scale(y,Q(-151,1024)),scale(power(eta,2),18),
        scale(mul(eta,x),19),scale(mul(eta,y),14),scale(L,2),
        scale(power(x,2),Q(8,3)),scale(power(y,2),Q(5,9)),scale(mul(x,y),Q(7,9)),
        scale(mul(L,x),Q(1,9)),scale(power(L,2),Q(11,9)),scale(mul(y,L),Q(4,9)),
        mul(c1,add(const(1),scale(D0,Q(8,9)))))
    pid('whole first Fourier majorant',xp,expanded_x)
    xdrop=add(xp,scale(y,Q(151,1024))); ydrop=add(yp,scale(y,Q(151,1024)))
    K0=18+14*135+Q(5,9)*135**2+Q(11,9)*9+Q(4,9)*135*3+Q(8,9)*147*delta
    lam=Q(8,3)*18*E+(19+Q(7,9)*135+Q(3,9)+Q(8,9)*delta)*e
    first_poly=xdrop
    for axis,value in [(2,scale(eta,135)),(3,scale(eta,3)),(4,scale(eta,delta))]:
        first_poly=subst(first_poly,axis,value)
    pid('entire first mean bootstrap before monotone endpoints',first_poly,
        add(scale(eta,Q(27,4)+6+delta),scale(power(eta,2),K0),
            scale(mul(eta,x),19+Q(7,9)*135+Q(3,9)+Q(8,9)*delta),scale(power(x,2),Q(8,3))))
    X=Q(17);Y=Q(20);C=Q(3,8)
    Kx=18+19*X+14*Y+Q(8,3)*X**2+Q(5,9)*Y**2+Q(7,9)*X*Y+C*X/9+Q(11,9)*C**2+Q(4,9)*Y*C+Q(8,9)*(9+X+Y+C)*delta
    Ky=18+18*X+14*Y+Q(23,9)*X**2+Q(5,9)*Y**2+C**2/3+Q(2,9)*(9+X+Y+C)*Y+Q(7,9)*(9+X+Y+C)*delta+Q(7,9)*C**2+Y*C/3+Q(5,9)*X*C
    for name,p,cost in [('x',xdrop,Kx),('y',ydrop,Ky)]:
        for axis,value in [(1,scale(eta,X)),(2,scale(eta,Y)),(3,scale(eta,C)),
                           (4,scale(eta,delta)),(5,scale(eta,delta))]:
            p=subst(p,axis,value)
        pid('entire final ' + name + ' majorant with both phases',p,
            add(scale(eta,Q(27,4)+2*C+delta),scale(power(eta,2),cost)))

    low=[Q(9,k)*comb(8,9-k)*2**(9-k)*E**(7-k) for k in range(1,7)]
    improved=1024*e**2+360*e+Q(165,2)*E+sum(low[:5])
    final=Q(15,2)+delta+2000*e
    budgets={
      'critical_ratio_six':6-Q(11,2)*Q(256,255),
      'whole_low_sum_three':3-sum(low),'c1_small':delta-low[0],'c2_small':delta-low[1],
      'mean_absorption_one_fifth':Q(1,5)-lam,
      'mean_rhs_thirteen':13-(Q(27,4)+6+delta+e*K0),
      'mean_seventeen':17-Q(65,4),
      'c7_twenty':20-Q(9,14)*(30+Q(64,81)*17**2*e),
      'first_trace_sixteen':16-Q(8,9)*17,'sqrt30_five_halves_plus_three':Q(121,4)-30,
      'lower_tail_three_eighths':Q(3,8)-improved,
      'final_x_quadratic_cost2000':2000-Kx,'final_y_quadratic_cost2000':2000-Ky,
      'strict_entry31_4':Q(31,4)-final,'cap8_gap':Q(1,4),
      'signed_complex_y_coefficient':beta,
    }
    for name,value in budgets.items():positive(name,value)
    damaged('omit negative original-value norm in weight',
        ca(w,cs(cm(d,cj(d)),9))==w)
    damaged('omit first wrapped Fourier term',
        ga(q1,gm(d[0],gj(d[8])))==q1)
    damaged('invent nonzero second extra wrapped term',
        ga(q2,gm(d[1],gj(d[8])))==q2)
    damaged('remove complex conjugate from first wrap',
        gm(d[0],d[8])==gm(d[0],gj(d[8])))
    damaged('omit complete U squared in seventh Newton identity',
        gs(es2,Q(9,7))==gs(t2,Q(-9,14)))
    damaged('omit U cubed in sixth Newton identity',
        gs(es3,Q(-3,2))==ga(gs(gm(u,t2),Q(3,4)),gs(t3,Q(-1,2))))
    damaged('omit actual original anchor',gsubst(ga(original,gs(anchor,-1)),17,a)==gc())
    damaged('claim coefficient8 already after first bootstrap',Q(8)>=Q(65,4))
    damaged('underbound initial lower sum by5_2',sum(low)<=Q(5,2))
    damaged('underbound sqrt30 by5',30<=25)
    damaged('claim final cap15_2 from displayed budgets',final<Q(15,2))
    damaged('enlarge full window to2^-8 with unchanged final budget',
            Q(15,2)+delta+2000*Q(1,256)<Q(31,4))
    return {'schema':1,'agent':'six-sendov-1','role':'researcher',
       'representation':'entire Gaussian Fraction polynomials and all nine cyclic frequencies',
       'complete_controls':controls,'strict_whole_window_margins':margins,
       'initial_lower_coefficient_bounds':[scalar(v) for v in low],
       'refined_lower_sum':scalar(improved),'first_mean_lambda':scalar(lam),
       'final_majorant_costs':[scalar(Kx),scalar(Ky)],'final_coefficient_cap':scalar(final),
       'mathematical_damage_rejections':damages,
       'finite_evidence_not_formal_analytic_proof':True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'))
    parser.add_argument('--emit',type=Path)
    args=parser.parse_args()
    record=generate()
    canonical=json.dumps(record,sort_keys=True,separators=(',',':'))
    if args.emit:
        args.emit.write_text(canonical+'\n')
    else:
        expected=json.loads(args.expected.read_text(),object_pairs_hook=pairs,
                            parse_float=reject_float,parse_constant=reject_float)
        need(typed_equal(record,expected),'entire typed fixture differs')
    print(json.dumps({'status':'PASS','complete_controls':len(record['complete_controls']),
       'strict_margins':len(record['strict_whole_window_margins']),
       'mathematical_damage_rejections':len(record['mathematical_damage_rejections']),
       'whole_record_sha256':sha256(canonical.encode()).hexdigest(),
       'analytic_proof_formalized':False},sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
