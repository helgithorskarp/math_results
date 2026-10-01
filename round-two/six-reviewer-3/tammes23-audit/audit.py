"""Independent Gram completion and whole-interval Sturm audit of lemma 8835.

Run with --certificate PATH to the pinned author's certificate. No author code
is imported. All arithmetic, including every interval sign, is exact.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from fractions import Fraction as Q
from rational import (R, need, value, solve, sqrt_rational, sign_certificate,
                      sturm, variations, mul, division, positive_remainder)

LEFT, RIGHT = Q(14, 25), Q(593, 1000)
F = (-1, -3, 2, 6, -1, 13)
EDGES = ((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
         (2,4),(2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),
         (6,11),(7,12),(8,13),(9,10),(9,11),(9,13),(10,12))
LABELS = (0,1,2,4,5,6,7,8,9,10,11,12,13)
NONCOLLISIONS = ((5,6),(7,11),(0,9),(1,8),(4,10),(2,12),(4,13),(2,9))
PINNED_SHA = 'b555b32ac80329e2aaca19ce6053f2a967279c7acf6fb447bbb013d2dfe03d0e'
BOUNDS = {
    'kappa':('-3/10','-1/5'), 'mu':('-3/5','-11/20'),
    'common_w':('1/3','2/5'), 'common_height2':('49/100','3/5'),
    'plane_gram':('9/10','1'), 'normal_squared_norm':('2','3'),
    'rho':('9/50','23/100'), 'detH':('3/10','1/2'),
    'reflection_determinant':('1','2'), 'Fprime':('10','14'),
    '-1_-1_1_7_a':('-1/10','-1/50'), '-1_-1_1_7_b':('9/10','6/5'),
    '-1_-1_1_7_square':('-1/4','-1/5'),
    '1_1_10_11_a':('1/10','3/20'), '1_1_10_11_b':('1/2','2/3'),
    '1_-1_6_8_a':('-3/4','-2/5'), '1_-1_6_8_b':('4/3','8/5'),
    'packing_threshold_factor':('1/2','4/5')}


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


class E:
    """Quadratic algebra a+b*theta; theta^2=rho, without field division."""
    rho = None

    def __init__(self, a=0, b=0):
        if isinstance(a, E):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = R(a), R(b)

    def __add__(self, other):
        other = E(other)
        return E(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return E(-self.a, -self.b)

    def __sub__(self, other):
        return self+-E(other)

    def __rsub__(self, other):
        return E(other)+-self

    def __mul__(self, other):
        other = E(other)
        return E(self.a*other.a+self.rho*self.b*other.b,
                 self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        need(not isinstance(other, E), 'division only by rational functions')
        return E(self.a/R(other), self.b/R(other))

    def __eq__(self, other):
        other = E(other)
        return self.a == other.a and self.b == other.b

    def manifest(self):
        return {'a':self.a.manifest(), 'b':self.b.manifest()}


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]


def mv(matrix, vector):
    return [sum((E(x)*y for x, y in zip(vector, row)), E())
            if any(isinstance(x, E) for x in vector)
            else sum((x*y for x, y in zip(vector, row)), R()) for row in matrix]


def dot(a, b, h):
    if any(isinstance(x, E) for x in a+b):
        return sum((E(a[i])*h[i][j]*E(b[j]) for i in range(3)
                    for j in range(3)), E())
    return sum((a[i]*h[i][j]*b[j] for i in range(3) for j in range(3)), R())


def derive():
    t, one = R((0,1)), R(1)
    h = [[one if i == j else t for j in range(3)] for i in range(3)]
    deth = (one-t)**2*(one+2*t)
    r = 2*t/(one+t)
    b = {label:[one if i == j else R() for i in range(3)]
         for j, label in enumerate((1,2,4))}
    for new, first, second, old in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        b[new] = [r*(x+y)-z for x,y,z in zip(b[first], b[second], b[old])]
    k = t*(9*t*t-2*t-3)/(one+t)**2
    common = dot(b[10], b[13], h)
    v = [2*t/(one+common)*(x+y)-z for x,y,z in zip(b[10], b[13], b[2])]

    # Bordered Gram minimization, rather than the author's 2x2 closed formula.
    hv, hb = mv(h, v), mv(h, b[12])
    bordered = [h[i]+[hv[i], hb[i]] for i in range(3)]
    bordered += [hv+[R(),R()], hb+[R(),R()]]
    center = solve(bordered, [R(),R(),R(),k,t])[:3]
    normal = solve(h, cross(v, b[12]))
    dn = dot(normal, normal, h)
    rho = (one-dot(center, center, h))/dn
    E.rho = rho
    z = dot(v, b[12], h)
    g = one-z*z
    need(dn*deth == g, 'normal determinant identity')

    # Extract a polynomial square instead of adopting the author's mu formula.
    mu = sqrt_rational(deth*(one+2*k)/(one+k)**2)
    coeff = solve([[one,k],[k,one]], [k,k])
    need(coeff[0] == coeff[1] == k/(one+k), 'equilateral center')
    rotation = [[r,r,-one],[-one,r,r],[r,-one,r]]
    rt = [list(x) for x in zip(*rotation)]
    detrot = (3*t-one)*(3*t+one)**2/(one+t)**3
    actual_det = sum((rotation[0][i]*cross(rotation[1],rotation[2])[i]
                      for i in range(3)), R())
    need(actual_det == detrot, 'actual reflection determinant')
    for i in range(3):
        for j in range(3):
            need(dot(rt[i],rt[j],h) == (one if i == j else k),
                 'reflected A common-neighbor Gram identity')
    antecedents = set(itertools.combinations((0,5,11),2))
    antecedents.update(itertools.combinations((1,2,4),2))
    for new, first, second, old in ((6,0,11,5),(7,0,5,11),(9,5,11,0),
                                   (8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        need(all(tuple(sorted(pair)) in antecedents for pair in
                 ((first,second),(first,old),(second,old))),
             'every old-triangle antecedent retained')
        antecedents.update((tuple(sorted((new,first))),tuple(sorted((new,second)))))
    antecedents.update(((7,12),(9,10),(9,13)))
    need(antecedents == set(EDGES), 'reflection construction equals literal graph')
    functions = {'kappa':k,'gamma':coeff[0],'mu':mu,'common_w':common,
                 'z':z,'plane_gram':g,'normal_squared_norm':dn,'rho':rho,
                 'detH':deth,'reflection_determinant':detrot,
                 'common_height2':one-2*t*t/(one+common),
                 'Fprime':R(tuple(i*F[i] for i in range(1,len(F))))}
    models, gaps = {}, {}
    for eps, sigma in itertools.product((-1,1), repeat=2):
        w = [E(x,eps*y) for x,y in zip(center,normal)]
        need(dot(w,w,h) == one and dot(w,v,h) == k and dot(w,b[12],h) == t,
             'both W completions')
        u_normal = solve(h, cross(list(map(E,v)), w))
        u = [(E(x)+y)*coeff[0]+n*(sigma*mu) for x,y,n in zip(v,w,u_normal)]
        need(dot(u,u,h) == one and dot(u,v,h) == k and dot(u,w,h) == k,
             'both U completions')
        p = {i:list(map(E,x)) for i,x in b.items()}
        for coordinate in range(3):
            anchors = solve(rt,[u[coordinate],w[coordinate],E(v[coordinate])])
            for label, x in zip((0,5,11), anchors):
                p.setdefault(label, [None]*3)[coordinate] = x
        p.update({6:u,7:w,9:list(map(E,v))})
        need(tuple(sorted(p)) == LABELS, 'complete thirteen-point labels')
        for i in LABELS:
            need(dot(p[i],p[i],h) == one, 'unit identity')
        for i,j in EDGES:
            need(dot(p[i],p[j],h) == t, 'contact identity')
        key = f'{eps}_{sigma}'
        models[key] = p
        gaps[key] = {f'{i}_{j}':dot(p[i],p[j],h)-t
                     for i,j in ((1,7),(10,11),(6,8))}
        for pair, gap in gaps[key].items():
            functions[f'{key}_{pair}_a'] = gap.a
            functions[f'{key}_{pair}_b'] = gap.b
            functions[f'{key}_{pair}_square'] = gap.a*gap.a-rho*gap.b*gap.b
        if key == '1_-1':
            for i,j in itertools.combinations(LABELS,2):
                if (i,j) in EDGES or (i,j) == (6,8):
                    continue
                d = dot(p[i],p[j],h)
                functions[f'noncontact_{i}_{j}_a'] = d.a
                functions[f'noncontact_{i}_{j}_b'] = d.b
    need(gaps['-1_-1']['1_7'] == gaps['-1_1']['1_7'], 'same two W selectors')
    functions['packing_threshold_factor'] = functions['1_-1_6_8_square']/R(F)
    return functions, models, gaps, h


def sign(f, left=LEFT, right=RIGHT):
    n, nc = sign_certificate(f.n, left, right)
    d, dc = sign_certificate(f.d, left, right)
    need(d != 0, 'denominator strictly nonzero on closed interval')
    return n*d, {'numerator':nc, 'denominator':dc}


def below_radical(a, b, rho, ceiling):
    c = R(ceiling)
    # Each successful route is sufficient on the entire closed interval.
    attempts = (
        ('negative-radical', (c-a, -b)),
        ('positive-center-squared', (c-a, (c-a)**2-rho*b*b)),
        ('negative-coefficient-squared', (-b, rho*b*b-(a-c)**2)))
    for name, tests in attempts:
        try:
            signs = [sign(x)[0] for x in tests]
        except ValueError:
            continue
        if (name == 'negative-radical' and signs[0] > 0 and signs[1] >= 0
                or name != 'negative-radical' and all(x > 0 for x in signs)):
            return name
    raise ValueError('no complete-interval radical exclusion')


def polynomial_interval(p, lo, hi):
    a = b = Q(0)
    for x in reversed(p):
        candidates = (a*lo,a*hi,b*lo,b*hi)
        a,b = min(candidates)+x,max(candidates)+x
    return a,b


def rational_interval(f, lo, hi):
    a,b = polynomial_interval(f.n,lo,hi)
    c,d = polynomial_interval(f.d,lo,hi)
    need(not c <= 0 <= d, 'interval denominator nonzero')
    ratios = (a/c,a/d,b/c,b/d)
    return min(ratios),max(ratios)


def rounded_interval(interval, scale):
    a,b = interval
    lower = a.numerator*scale//a.denominator
    upper = -((-b.numerator*scale)//b.denominator)
    need(Q(lower,scale) <= a <= b <= Q(upper,scale), 'outward rational rounding')
    return [str(Q(lower,scale)),str(Q(upper,scale))]


def arithmetic_controls():
    # Sturm root counting independently cross-checks repeated and endpoint roots.
    cases = ((mul((-1,1),(-1,1)),Q(0),Q(2),1),
             (mul((-1,1),(1,1)),Q(-2),Q(2),2),
             ((1,0,1),Q(-2),Q(2),0),
             ((0,1),Q(0),Q(1),0))
    for p,lo,hi,want in cases:
        s = sturm(p)
        need(variations(s,lo)-variations(s,hi) == want, 'Sturm root-count control')
    for a,b in (((2,-3,5,7),(-1,2)), ((-3,2,1,4),(2,-3)),
                ((1,0,-2,0,1),(1,0,1))):
        actual = positive_remainder(a,b)
        expected = division(a,b)[1]
        if expected:
            scale = Q(actual[-1])/expected[-1]
            need(scale > 0 and tuple(scale*x for x in expected) == actual,
                 'positive pseudoremainder compared with rational division')
        else:
            need(not actual, 'zero pseudoremainder')
    failures = 0
    for task in (lambda:sign_certificate((-1,1),Q(0),Q(2)),
                 lambda:sign_certificate((0,1),Q(0),Q(1)),
                 lambda:sqrt_rational(R((1,0,2))),
                 lambda:R(1,(0,)),
                 lambda:solve([[R(1),R(1)],[R(1),R(1)]],[R(),R()])):
        try:
            task()
        except ValueError:
            failures += 1
    need(failures == 5, 'all five arithmetic damages rejected')
    need(sqrt_rational(R(mul((-2,1),(-2,1)))) == R((-2,1)), 'exact square extraction')
    return {'known_root_counts':len(cases),'pseudoremainder_comparisons':3,
            'rejected_arithmetic_damages':failures}


def check_table(c, functions):
    need(c['format'] == 1 and c['interval'] == [[14,25],[593,1000]], 'fixed domain')
    need(c['edges'] == [list(e) for e in EDGES], 'literal G23 edge list')
    need(set(c['functions']) == set(functions), 'complete rational-function labels')
    for name,f in functions.items():
        raw = c['functions'][name]
        need(set(raw) == {'n','d'} and all(type(x) is int for x in raw['n']+raw['d']),
             'integer-polynomial input shape')
        need(R(raw['n'],raw['d']) == f, 'independently regenerated function '+name)


def audit(c):
    controls = arithmetic_controls()
    functions, models, gaps, h = derive()
    check_table(c, functions)
    bounds = {}
    for name,(a,b) in BOUNDS.items():
        lo,lc = sign(functions[name]-R(Q(a)))
        hi,hc = sign(R(Q(b))-functions[name])
        need(lo > 0 and hi > 0, 'strict whole-interval bound '+name)
        bounds[name] = {'lower':a,'upper':b,'lower_sign':lc,'upper_sign':hc}
    denominators = {}
    for f in functions.values():
        denominators.setdefault(f.d, sign_certificate(f.d,LEFT,RIGHT))
    coordinate_denominators = {coefficient.d for p in models.values()
        for vector in p.values() for x in vector for coefficient in (x.a,x.b)}
    for denominator in coordinate_denominators:
        need(sign_certificate(denominator,LEFT,RIGHT)[0] != 0,
             'every reconstructed coordinate denominator nonzero')
    noncontacts = [pair for pair in itertools.combinations(LABELS,2)
                   if pair not in EDGES and pair != (6,8)]
    need(len(noncontacts) == 54, 'complete noncontact pair coverage')
    routes = {}
    for i,j in noncontacts:
        stem = f'noncontact_{i}_{j}_'
        routes[f'{i}_{j}'] = below_radical(functions[stem+'a'],functions[stem+'b'],
                                           functions['rho'],Q(23,50))
    a,z = map(Q,c['root_bracket'])
    need(LEFT < a < z < RIGHT and value(F,a) < 0 < value(F,z), 'isolated incumbent root')
    need(sign_certificate(F,LEFT,a)[0] == -1 and sign_certificate(F,z,RIGHT)[0] == 1,
         'threshold polynomial has no other root outside bracket')
    # Bound the rational first-order coefficient, after eliminating theta at tau.
    sharp = -functions['packing_threshold_factor']*functions['Fprime']/(2*functions['1_-1_6_8_a'])
    sharp_raw = rational_interval(sharp,a,z)
    sharp_interval = rounded_interval(sharp_raw,10**8)
    need(Q(sharp_interval[0]) < sharp_raw[0] and sharp_raw[1] < Q(sharp_interval[1]),
         'strict outer enclosure of the sharp coefficient')
    need(Q(sharp_interval[0]) > 0, 'positive sharp defect coefficient')
    need(Q(21,50)**2 < Q(9,50) and Q(23,100) < Q(12,25)**2,
         'outward square-root constants')
    need(Q(2,5)+Q(4,3)*Q(21,50) == Q(24,25), 'defect denominator lower bound')
    need(Q(3,4)+Q(8,5)*Q(12,25) == Q(759,500), 'defect denominator upper bound')
    need(Q(1,2)*10/Q(759,500) == Q(2500,759), 'global defect lower factor')
    need(Q(4,5)*14/Q(24,25) == Q(35,3), 'global defect upper factor')
    quartic = (-1,0,3,-2,4)
    need(value(quartic,LEFT) < 0, 'N14 optimum exceeds the interval lower bound')
    # Its derivative is s*(16*s*s-6*s+6), whose quadratic has negative
    # discriminant and positive leading coefficient.
    need((-6)**2-4*16*6 < 0, 'positive N14 quartic derivative for s>0')
    damages = []
    for name in ('rho','mu','packing_threshold_factor','1_-1_6_8_a'):
        copy = json.loads(json.dumps(c))
        copy['functions'][name]['n'][0] += 1
        try:
            check_table(copy,functions)
        except ValueError:
            damages.append(name)
    for name in ('missing-edge','missing-pair'):
        copy = json.loads(json.dumps(c))
        if name == 'missing-edge':
            copy['edges'].pop()
        else:
            copy['functions'].pop('noncontact_0_1_a')
        try:
            check_table(copy,functions)
        except ValueError:
            damages.append(name)
    need(len(damages) == 6, 'all six certificate damages rejected')
    return {'status':'VERIFIED','author_certificate_sha256':PINNED_SHA,
            'canonical_input_sha256':digest(c),'independent_functions':len(functions),
            'branches':4,'unit_identities':52,'contact_identities':92,
            'surviving_branch':[1,-1],'noncontact_pairs':54,'noncontact_upper':'23/50',
            'noncontact_routes':routes,'whole_interval_rational_bounds':bounds,
            'distinct_function_denominators':len(denominators),
            'distinct_coordinate_denominators':len(coordinate_denominators),
            'maximum_denominator_degree':max(len(d)-1 for d in denominators),
            'branch_gram_sha256':{key:digest({f'{i}_{j}':dot(p[i],p[j],h).manifest()
                for i,j in itertools.combinations(LABELS,2)}) for key,p in models.items()},
            'root_bracket':[str(a),str(z)],'sharp_defect_coefficient_interval':sharp_interval,
            'global_absolute_defect_factors':['2500/759','35/3'],
            'one_relaxed_inequality_parameter_loss':'759/2500',
            'noncollisions':[list(x) for x in NONCOLLISIONS],
            'packing_selectors':[[1,7],[10,11],[6,8]],
            'arithmetic_controls':controls,'rejected_certificate_damages':damages}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINNED_SHA, 'pinned author artifact bytes')
    result = audit(json.loads(raw))
    rendered = json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(json.dumps({k:v for k,v in result.items() if k not in
                      ('whole_interval_rational_bounds','noncontact_routes')},sort_keys=True))
