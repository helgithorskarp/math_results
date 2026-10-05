"""PRIVATE exact scalar/stationary support; actual six-sendov-3 researcher.

Characteristic zero Q[w]/(w^6+w^3+1), physical c=-(w^4+w^5)/2.
One exact polynomial variable mu, increasing exponent indices. No expected
record, peer executable, numerical sample or generated mathematics is read.
The analytic globality and second stationary-jet bridges remain external.
"""
from pathlib import Path
from hashlib import sha256
import json, sys

D = Path(__file__).resolve().parent
pins = json.loads((D / 'kernel-pins.json').read_text())
for row in pins:
    b = (D / 'kernel' / row['name']).read_bytes()
    if len(b) != row['bytes'] or sha256(b).hexdigest() != row['sha256']:
        raise RuntimeError('PREIMPORT_KERNEL_PIN ' + row['name'])
sys.path.insert(0, str(D / 'kernel'))
import calculation as calc

j, s, F, need = calc.j, calc.s, calc.F, calc.need
ar = s.ar
ids = []
eq = lambda name, a, b: s.eq(ids, name, a, b)
values = {}


def mean_poly(poly, specialize=False):
    out = s.N0
    for n, coefficient in poly.items():
        need(type(n) is int and n >= 0, 'packed monomial index')
        if n % 32 == 0:
            degree = n // 32
            term = (s.nm({0: coefficient}, s.np(j.m.MUstar, degree))
                    if specialize else {degree: coefficient})
            out = s.na(out, term)
    return out


def initial_parts(specialize=False):
    parts = tuple(s.pa({key: tuple(mean_poly(p, specialize) for p in g)
                   for key, g in factor.items()}) for factor in calc.no_ninth())
    need(all(g[1] == s.N0 for factor in parts[:2] for g in factor.values()),
         'all real A and B coefficients')
    need(all(g[0] == s.N0 for g in parts[2].values()), 'pure imaginary K')
    need(all(e % 2 == 0 and z == 0 for factor in parts for e, z in factor),
         'all factors even in epsilon, original-free')
    return parts


def evaluate(poly):
    return s.na(*(s.nm({0: a}, s.np(j.m.MUstar, n))
                  for n, a in poly.items()))


def differentiate(poly):
    return {n-1: ar.ns(a, n) for n, a in poly.items() if n}


def direct_first(parts, order):
    """Binomial positive inverse lengths through epsilon12; all8 slots."""
    need(order in (10, 12), 'exact finite scalar order')
    va, vb, x2 = calc.physical_variances(parts, order)
    need(not x2, 'whole zero cross term for real6+2 family')
    coefficients = [F(1)]
    for n in range(1, order//2 + 1):
        coefficients.append(coefficients[-1] * F(1-2*n, 2*n))
    need(coefficients[5] == F(-63,256), 'fifth binomial coefficient')
    if order == 12:
        need(coefficients[6] == F(231,1024), 'sixth binomial coefficient')
    def inverse_sqrt(v):
        h = s.pa(v, {(0, 0): s.gs(s.G1, -1)})
        need(not h or min(e for e, z in h) >= 2, 'variance valuation')
        return s.pa(*(s.ps(s.pp(h, n, order), a)
                      for n, a in enumerate(coefficients)))
    total = s.pa(s.ps(inverse_sqrt(va), 6), s.ps(inverse_sqrt(vb), 2))
    need(all(z == 0 for e, z in total), 'whole original-free scalar')
    first = [total.get((e, 0), s.G0) for e in range(order+1)]
    eq('WHOLE direct positive FIRST versus independent scalar equations/' + str(order),
       first, calc.scalar_recursion(parts, order, ids))
    return first


def primitive(parts, order, tag):
    p = s.actual_polynomial(*parts, order, 2)
    pn, powers = s.newton_polynomial(*parts, order, 2)
    need(len(powers) == 9, 'all eight critical moments')
    eq('WHOLE all8 Newton versus literal primitive/' + tag,
       [g for row in p for g in row], [g for row in pn for g in row])
    for e in range(1, order+1, 2):
        eq('WHOLE odd primitive/' + tag + '/' + str(e), p[e], [s.G0]*10)
    return p, powers


def normal_controls(roots, order, tag):
    need(len(roots) == 9, 'whole original-root census')
    anchor = [s.G1, s.G0, s.gs(s.G1, -1)] + [s.G0]*(order-2)
    eq('WHOLE actual marked ninth original/' + tag, roots[0]['root'], anchor)
    for label, row in enumerate(roots):
        eq('WHOLE original conjugacy/' + tag + '/' + str(label),
           row['root'], [s.gc(g) for g in roots[(-label) % 9]['root']])
        for e in range(1, order+1, 2):
            eq('WHOLE odd original/' + tag + '/' + str(label) + '/' + str(e),
               [row['root'][e]], [s.G0])


A3, B3 = calc.AB[3]
A4, B4 = calc.AB[4]
h7 = s.ns(s.H, F(1, 7))
det = s.nm(h7, s.na(s.nm(A4, B3), s.ns(s.nm(A3, B4), -1)))
eq('WHOLE even normal determinant', [s.gf(det)],
   [s.gf(s.na(s.ns(s.c, 2), s.ns(s.N1, -1)))])
w4 = s.ni(s.na(s.c, s.ns(s.np(s.c, 2), 2), s.ns(s.N1, -1)))
w3 = s.ns(s.na(s.ns(s.N1, 7), s.ns(s.nm(B4, w4), -1)), F(2, 3))
eq('WHOLE common-center weighted column', [s.gf(s.na(s.nm(w3,A3),s.nm(w4,A4)))],
   [s.gs(s.G1, 8)])
eq('WHOLE imaginary split weighted column', [s.gf(s.na(s.nm(w3,B3),s.nm(w4,B4)))],
   [s.gs(s.G1, 7)])


def repair(parts, p, roots, first, order, tag):
    """Both actual last normal columns, full root equations retained."""
    q3, q4 = (roots[label]['normals'][order][0] for label in (3,4))
    tau = s.nm(s.nm(h7, s.na(s.nm(B3,q4),s.ns(s.nm(B4,q3),-1))),s.ni(det))
    beta = s.nm(s.na(s.nm(A3,q4),s.ns(s.nm(A4,q3),-1)),s.ni(det))
    parts1 = (s.pa(parts[0], {(order,0):s.gf(tau)}),
              s.pa(parts[1], {(order,0):s.gf(tau)}),
              s.pa(parts[2], {(order-2,0):(s.N0,beta)}))
    p1, powers1 = primitive(parts1, order, tag)
    column = [s.G0]*10
    column[0] = s.gf(s.na(s.ns(tau,9),s.ns(s.nm(h7,beta),-9)))
    column[7] = s.gf(s.ns(s.nm(h7,beta),9))
    column[8] = s.gf(s.ns(tau,-9))
    for e in range(order+1):
        eq('WHOLE two-parameter last primitive column/' + tag + '/' + str(e),
           [s.ga(a,s.gs(b,-1)) for a,b in zip(p1[e],p[e])],
           column if e == order else [s.G0]*10)
    newroots = []
    for label, old in enumerate(roots):
        omega = s.np(s.WW,label)
        response = s.gf(s.na(
            s.nm(tau,s.na(s.N1,s.ns(omega,-1))),
            s.nm(s.nm(h7,beta),s.na(omega,s.ns(s.np(omega,8),-1)))))
        root = old['root'][:]
        root[order] = s.ga(root[order], response)
        eq('ALL9 WHOLE independently corrected original equation/' + tag + '/' + str(label),
           s.equation(p1,root,order), [s.G0]*(order+1))
        normals = s.sm(root,[s.gc(a) for a in root],order)
        normals[0] = s.ga(normals[0],s.gs(s.G1,-1))
        normals = [s.gs(a,F(1,2)) for a in normals]
        Aj,Bj = calc.AB[label]
        expected = s.gf(s.na(s.ns(s.nm(Aj,tau),-1),s.nm(s.nm(h7,Bj),beta)))
        eq('ALL9 WHOLE independently recomputed half-normal response/' + tag + '/' + str(label),
           [s.ga(a,s.gs(b,-1)) for a,b in zip(normals,old['normals'])],
           [s.G0]*order+[expected])
        newroots.append({'label':label,'root':root,'normals':normals})
    normal_controls(newroots,order,tag)
    for label in (3,4,5,6):
        eq('ALL4 boundary half-normals through last degree/' + tag + '/' + str(label),
           newroots[label]['normals'],[s.G0]*(order+1))
    first1 = direct_first(parts1,order)
    delta = s.na(s.ns(tau,8),s.ns(s.nm(s.H,beta),-1))
    weighted = s.na(s.nm(w3,q3),s.nm(w4,q4))
    eq('WHOLE last FIRST response equals weighted actual normals/' + tag,
       [s.gf(delta)],[s.gf(weighted)])
    eq('WHOLE last FIRST actual repair/' + tag,
       [s.ga(a,s.gs(b,-1)) for a,b in zip(first1,first)],
       [s.G0]*order+[s.gf(delta)])
    return parts1,p1,powers1,newroots,first1,{'tau':s.rpoly(tau),'beta':s.rpoly(beta),
           'q3':s.rpoly(q3),'q4':s.rpoly(q4),'weighted':s.rpoly(weighted)}


def encode_phase(parts,p,powers,roots,first,controls):
    return {'whole_factors':j.encoded_parts(parts),
            'whole_primitive':[s.encoded_vector(row) for row in p],
            'whole_all8_moments':[s.encoded_vector([power.get((e,0),s.G0)
               for e in range(len(p))]) for power in powers[1:]],
            'whole_all9_originals':s.output_roots(roots),
            'whole_first':s.encoded_vector(first),'repair':controls}


def fifth():
    order = 10
    parts = initial_parts()
    p,powers = primitive(parts,order,'symbolic-mean-baseline')
    roots = s.roots_and_normals(p,order,ids)
    normal_controls(roots,order,'symbolic-mean-baseline')
    for label in (3,4,5,6):
        eq('ALL4 WHOLE symbolic-mean boundary below10/' + str(label),
           roots[label]['normals'][:10],[s.G0]*10)
    first = direct_first(parts,order)
    parts,p,powers,roots,first,controls = repair(parts,p,roots,first,order,'symbolic-mean-fifth')
    lower = [s.G0]*8
    for e,a in ((0,s.ns(s.N1,8)),(2,s.C['C']),(4,s.C['Bstar']),(6,s.Tstar)):
        lower[e] = s.gf(a)
    eq('WHOLE symbolic mean retains complete credited M3',first[:8],lower)
    mu = {1:ar.N1}
    parabola = s.na(j.m.Gmean,s.ns(s.np(s.na(mu,s.ns(j.m.MUstar,-1)),2),F(4,3)))
    eq('WHOLE credited fourth mean parabola', [first[8]], [s.gf(parabola)])
    K = first[10][0]
    need(first[10][1] == s.N0, 'whole real fifth potential')
    J0 = s.const(s.fcf(F(-8304485822364161,181398528),
        F(-6510273073800785,30233088),F(2123849893841477,7558272)))
    eq('WHOLE reproduced public025 global fifth scalar at mu_star',
       [s.gf(evaluate(K))],[s.gf(J0)])
    Kprime = evaluate(differentiate(K))
    need(Kprime != s.N0, 'nonzero fifth derivative at selected mean')
    nu = s.ns(Kprime,F(-3,8))
    correction = s.ns(s.np(Kprime,2),F(-3,16))
    values['Kprime'] = Kprime
    values['K'] = K
    eq('WHOLE second stationary-jet square completion',
       [s.gf(s.na(s.ns(s.np(nu,2),F(4,3)),s.nm(Kprime,nu)))],
       [s.gf(correction)])
    output = encode_phase(parts,p,powers,roots,first,controls)
    output.update({'symbolic_fifth_potential':s.rpoly(K),'Kprime_at_mu_star':s.rpoly(Kprime),
                   'second_mean_displacement_nu':s.rpoly(nu),
                   'global_sixth_stationary_correction':s.rpoly(correction)})
    return output


def sixth():
    # Recompute specialized fifth factors afresh. No phase-five record read.
    parts = initial_parts(True)
    p,powers = primitive(parts,10,'constant-mean-fifth-baseline')
    roots = s.roots_and_normals(p,10,ids)
    for label in (3,4,5,6):
        eq('ALL4 WHOLE constant-mean boundary below10/' + str(label),
           roots[label]['normals'][:10],[s.G0]*10)
    first = direct_first(parts,10)
    parts,p,powers,roots,first,controls5 = repair(parts,p,roots,first,10,'constant-mean-fifth')
    p,powers = primitive(parts,12,'constant-mean-sixth-baseline')
    roots = s.roots_and_normals(p,12,ids)
    for label in (3,4,5,6):
        eq('ALL4 WHOLE constant-mean boundary below12/' + str(label),
           roots[label]['normals'][:12],[s.G0]*12)
    first = direct_first(parts,12)
    baseline = first[12][0]
    parts,p,powers,roots,first,controls6 = repair(parts,p,roots,first,12,'constant-mean-sixth')
    target = [s.G0]*11
    J0 = s.const(s.fcf(F(-8304485822364161,181398528),
        F(-6510273073800785,30233088),F(2123849893841477,7558272)))
    for e,a in ((0,s.ns(s.N1,8)),(2,s.C['C']),(4,s.C['Bstar']),
                (6,s.Tstar),(8,j.m.Gmean),(10,J0)):
        target[e] = s.gf(a)
    eq('WHOLE complete reproduced public025 lower scalar through epsilon10',
       first[:11], target)
    values['sixth_base'] = first[12][0]
    values['small_second_seed'] = parts[0][(6,0)][0]
    values['large_second_seed'] = parts[1][(6,0)][0]
    values['inactive_normals'] = {label: roots[label]['normals'][2][0]
                                 for label in (0,1,2,7,8)}
    output = encode_phase(parts,p,powers,roots,first,controls6)
    output.update({'fifth_repair':controls5,'sixth_unrepaired_scalar':s.rpoly(baseline),
                   'sixth_fixed_mean_boundary_scalar':s.rpoly(first[12][0])})
    return output


def global_support():
    r5, r6 = fifth(), sixth()
    Kprime, base = values['Kprime'], values['sixth_base']
    nu_star = s.ns(Kprime,F(-3,8))
    J6 = s.na(base,s.ns(s.np(Kprime,2),F(-3,16)))
    nu = {1:ar.N1}
    cost = s.na(base,s.nm(Kprime,nu),s.ns(s.np(nu,2),F(4,3)))
    square = s.na(J6,s.ns(s.np(s.na(nu,s.ns(nu_star,-1)),2),F(4,3)))
    eq('WHOLE universal second mean displacement square completion',
       [s.gf(cost)],[s.gf(square)])
    small_second = s.na(values['small_second_seed'],s.ns(nu_star,F(-1,3)))
    large_second = s.na(values['large_second_seed'],nu_star)
    signs = []
    for name, poly in [('minus_global_J6',s.ns(J6,-1)),('even_determinant',det),
                       ('H',s.H),('kappa',s.kappa),('w3',w3),('w4',w4),
                       ('aT',s.const(s.fcf(F(-11564,405),F(-20482,81),F(123284,405)))),
                       *[('minus_inactive_half_normal_'+str(label),s.ns(q,-1))
                         for label,q in values['inactive_normals'].items()]]:
        need(set(poly) == {0}, 'strict constant field sign domain')
        coefficients = list(map(F,s.field_real_form(s.fc,poly[0])))
        low, high, clo, chi = calc.rational_interval(coefficients)
        need(low > 0, 'strict rational physical field sign '+name)
        if name == 'minus_global_J6':
            need(F(65096) < low <= high < F(65097), 'strict whole global J6 integer bracket')
        signs.append({'name':name,'whole_cubic':list(map(str,coefficients)),
                      'strict_rational_interval':[str(low),str(high)],
                      'isolating_cosine_interval':[str(clo),str(chi)]})
    need(J6[0] != ar.N0, 'nonzero global sixth coefficient')
    return {'fifth':r5,'sixth':r6,'global_sixth_scalar':s.rpoly(J6),
            'strict_global_J6_integer_bracket':[-65097,-65096],
            'small_minimizer_second_jet':s.rpoly(small_second),
            'large_minimizer_second_jet':s.rpoly(large_second),
            'whole_second_mean_cost':s.rpoly(cost),'strict_signs':signs,
            'coverage_status':'Global identification is an ordinary written analytic bridge, outside this finite producer.'}


phase = sys.argv[1] if len(sys.argv) == 2 else 'fifth'
need(phase in ('fifth','sixth','global'), 'explicit finite phase')
output = {'fifth':fifth,'sixth':sixth,'global':global_support}[phase]()
output.update({'agent':'six-sendov-3','role':'researcher','phase':phase,
               'coefficient_domain':'Q[w]/(w^6+w^3+1)[mu], c=-(w^4+w^5)/2',
               'generated_mathematical_inputs_read':False,
               'ordinary_globality_and_stationary_bridges_outside_kernel':True,
               'independent_review':False,'identities':ids,
               'kernel_pins':pins})
print(ar.canonical(output).decode())
