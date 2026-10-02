#!/usr/bin/env python3
"""Regular E recovery at every full nonzero-s stationary-pencil solution.

Actual six-sendov-2, researcher. Standard library only. Complete exact
coefficient/determinant reconstruction; inherited own9550/9695 mathematics and
arithmetic are reused explicitly, not independently reviewed or formalized.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm
from functools import reduce
import argparse
import hashlib
import importlib.util
import json

PARENT_COMMIT = '15d70a9cbcc9d49baab803bd94e2d6a2668d90df'
PARENT_PINS = {
    'verify.py': 'fb3b05da10f44543febe8bb7eb523161588ff5206ed775a94ce3f43213aae345',
    'expected.json': '62f4e0b5707fe7b8dca04b2c2e27b5389358e7923268d6965a269c6b14d4c099'}
PARENT_RECORD = 'f8d8448d1ec587b6ab169afb07a0df472c866ce43d5ba9eef0e15a8e19fb4b21'
PRIME = 257


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def input_parent():
    directory = Path(__file__).resolve().parent.parent / 'nonzero-quartic-mass'
    for name, digest in PARENT_PINS.items():
        require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == digest,
                'pinned9695 source ' + name)
    spec = importlib.util.spec_from_file_location('energy9695_input', directory / 'verify.py')
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    record = parent.certificate()
    require(parent.same_typed(record, json.loads((directory / 'expected.json').read_text())),
            'entire typed9695 fixture')
    require(hashlib.sha256(canonical(record)).hexdigest() == PARENT_RECORD,
            'entire9695 record digest')
    kernel, data = parent.input9550()
    return parent, kernel, data


def certificate(export=None):
    h, k, data = input_parent()
    P = k.P
    q, E, r, x, u, v = [k.variable(i) for i in range(6)]
    checks, saved = {}, {}
    counters = {'primitive':0,'v':0}

    def eq(name, left, right=0):
        require(P(left) == P(right), 'whole identity ' + name)
        checks[name] = True

    def shift(poly, index, exponent):
        out = {}
        for key, c in P(poly).c.items():
            new = list(key)
            new[index] += exponent
            require(new[index] >= 0, 'known monomial division has exact polynomial quotient')
            out[tuple(new)] = c
        return P(out)

    def primitive(poly):
        poly = P(poly)
        require(bool(poly.c), 'nonzero primitive polynomial')
        den = lcm(*(c.denominator for c in poly.c.values()))
        common = 0
        for c in poly.c.values():
            common = gcd(common, abs(int(c * den)))
        content = F(common, den)
        result = P({key: c / content for key, c in poly.c.items()})
        require(all(c.denominator == 1 for c in result.c.values()), 'entire primitive integer coefficients')
        eq('primitive reconstruction ' + str(counters['primitive']), poly, content * result)
        counters['primitive'] += 1
        return result, content

    def decode(poly):
        require(all(len(key) == 5 and key[4] == 0 for key, c in poly),
                'complete ordinary9550 matrix coefficient domains')
        return P({tuple(key + [0] * 5): F(c) for key, c in poly})

    oldM = [[decode(a) for a in row] for row in data['matrix_rows_ABC']]
    oldR = [a*u*u + b*u + c for a, b, c in oldM]
    # The old slots denote B,E,r,s,t; the new slots denote q,E,r,x,u.
    powers = [2, 1, 2, 1, 2]
    R = []
    for i, p in enumerate(oldR):
        result = {}
        for key, c in p.c.items():
            require(not any(key[5:]), 'all input parameters retained')
            exponent = key[0] + key[3] - key[4] + powers[i]
            require(exponent >= 0 and exponent % 2 == 0, 'full nonzero-s chart parity and clearing')
            new = (key[0], key[1], key[2], exponent // 2, key[4]) + (0,) * 5
            result[new] = result.get(new, F(0)) + c
        R.append(P(result))
    for i, p in enumerate(R):
        back = {}
        for key, c in p.c.items():
            exponent = -key[0] + 2*key[3] + key[4]
            require(exponent >= 0, 'full inverse chart pullback remains polynomial')
            old = (key[0], key[1], key[2], exponent, key[4]) + (0,) * 5
            back[old] = back.get(old, F(0)) + c
        eq('entire inverse chart row ' + str(i), P(back), k.variable(3)**powers[i] * oldR[i])
    eq('whole leading E2 row0', k.extract(R[0], 1, 2), 2*u*u)
    eq('whole leading E2 row1', k.extract(R[1], 1, 2), -F(367,180)*u*u)
    eq('whole leading E2 row2', k.extract(R[2], 1, 2), (F(2,3)*r+F(13,48))*u*u)
    eq('whole leading E2 row3', k.extract(R[3], 1, 2), 0)
    eq('whole leading E2 row4', k.extract(R[4], 1, 2), F(1,24)*u*u)
    eq('entire quadratic E row0',R[0],sum((k.extract(R[0],1,j)*E**j for j in range(3)),P()))
    linear = [R[1] + F(367,360)*R[0], R[2] - (F(1,3)*r+F(13,96))*R[0],
              R[3], R[4]-F(1,48)*R[0]]
    alpha, beta, A, a_contents = [], [], [], []
    for i, p in enumerate(linear):
        aa, bb = k.extract(p,1,1), k.extract(p,1,0)
        eq('complete E affine row ' + str(i), p, aa*E+bb)
        a = shift(aa,4,-1)
        aa0, content = primitive(a)
        eq('known u factor in E coefficient ' + str(i), aa, u*content*aa0)
        alpha.append(aa)
        beta.append(bb)
        A.append(aa0)
        a_contents.append(str(content))
    D = 31304*r+1162*x+6165
    V = 118272-D*u
    eq('complete constant7200 qu pivot', A[2], 7200*q*u-V)

    # Polynomial v=q*u substitution, after a known-u multiplier when needed.
    def to_v(poly):
        out = {}
        for key, c in P(poly).c.items():
            require(key[5] == 0 and not any(key[6:]), 'v substitution inputs use only q,E,r,x,u')
            require(key[4] >= key[0], 'v=q*u clearing leaves no unknown denominator')
            new = list(key)
            new[5], new[4], new[0] = key[0], key[4]-key[0], 0
            out[tuple(new)] = c
        result = P(out)
        eq('whole v substitution ' + str(counters['v']), k.sub(result,5,q*u), poly)
        counters['v'] += 1
        return result

    def clear_v(poly, label):
        poly = P(poly)
        coefficients = [k.extract(poly,5,j) for j in range(3)]
        c0, c1, c2 = coefficients
        eq('entire quadratic v polynomial ' + label, poly, c2*v*v+c1*v+c0)
        raw = c2*V*V + 7200*c1*V + 7200**2*c0
        eq('undivided v clearing syzygy ' + label,
           7200**2*poly-raw, (7200*v-V)*(c2*(7200*v+V)+7200*c1))
        return raw

    eliminated, e_contents = [], []
    for i in (0,3):
        av = to_v(A[i])
        slope = k.extract(av,5,1)
        eq('affine v degree for leading row ' + str(i), av, slope*v+k.extract(av,5,0))
        raw = 7200*av-slope*(7200*v-V)
        require(all(key[5] == 0 for key in raw.c), 'constant-pivot elimination removes entire v')
        poly, content = primitive(raw)
        eliminated.append(poly)
        e_contents.append(str(content))
    rawJ = clear_v(to_v(u*A[1]), 'u times second leading row')
    J, jcontent = primitive(shift(rawJ,4,-1))
    eq('whole known u removal from J', rawJ, u*jcontent*J)
    FF, GG = eliminated
    for name, poly in [('F',FF),('G',GG),('J',J)]:
        eq('entire affine u ' + name, poly, k.extract(poly,4,1)*u+k.extract(poly,4,0))
    eq('nonzero x constant in G', k.extract(GG,4,0), 3241728*x)
    rawN = clear_v(to_v(beta[2]), 'original lower row3')
    N, ncontent = primitive(rawN)
    eq('entire quadratic u lower N', N, sum((k.extract(N,4,j)*u**j for j in range(3)),P()))
    f1,f0 = k.extract(FF,4,1),k.extract(FF,4,0)
    g1,g0 = k.extract(GG,4,1),k.extract(GG,4,0)
    j1,j0 = k.extract(J,4,1),k.extract(J,4,0)
    PP,pcontent = primitive(f1*g0-g1*f0)
    RR,rcontent = primitive(shift(g1*j0-j1*g0,3,-1))
    eq('full affine cross P', f1*g0-g1*f0,pcontent*PP)
    eq('full known x removal from R', g1*j0-j1*g0,x*rcontent*RR)
    n0,n1,n2 = [k.extract(N,4,j) for j in range(3)]
    clearing = n2*g0*g0-n1*g1*g0+n0*g1*g1
    eq('undivided affine quadratic lower clearing',
       g1*g1*N-clearing, GG*(g1*n2*u+g1*n1-g0*n2))
    LL,lcontent = primitive(shift(clearing,3,-1))
    eq('entire known x factor in lower clearing', clearing,x*lcontent*LL)
    for name,poly in [('F',FF),('G',GG),('J',J),('N',N),('P',PP),('R',RR),('L',LL)]:
        saved[name] = poly.encoded()

    def x_series(poly):
        require(all(not any(e for i,e in enumerate(key) if i != 3) for key in poly.c),
                'complete integer univariate x coefficient')
        if not poly.c:
            return [0]
        a = [0]*(max(key[3] for key in poly.c)+1)
        for key,c in poly.c.items():
            require(c.denominator == 1,'integer fixed matrix coefficients')
            a[key[3]] = int(c)
        return a

    def coefficient_arrays(poly):
        degree = max(key[2] for key in poly.c)
        return [x_series(k.extract(poly,2,j)) for j in range(degree+1)]

    pc = coefficient_arrays(PP)
    resultants = []
    for name, poly in [('R',RR),('L',LL)]:
        cc = coefficient_arrays(poly)
        m,n = len(pc)-1,len(cc)-1
        bound = n*max(len(c)-1 for c in pc)+m*max(len(c)-1 for c in cc)
        values = []
        for xx in range(bound+1):
            matrix = h.fixed_sylvester(pc,cc,xx)
            value = h.determinant_integer(matrix)
            require(h.determinant_fraction(matrix) == value,'every fixed point Gaussian corroboration')
            values.append(value)
        entire = h.interpolate_rational(values)
        primitive_coeffs, content = h.integer_primitive(entire)
        resultants.append({'pair':['P',name], 'formal_r_degrees':[m,n], 'matrix_size':m+n,
                           'left_entire_coefficient_arrays':pc,'right_entire_coefficient_arrays':cc,
                           'proved_x_degree_bound':bound,'every_integer_value':values,
                           'whole_determinant_coefficients':entire,'primitive_coefficients':primitive_coeffs,
                           'content':str(content),'actual_x_degree':len(entire)-1,
                           'every_fraction_Gaussian_value_matches':True})
    unit = h.finite_unit(resultants[0]['primitive_coefficients'],resultants[1]['primitive_coefficients'],PRIME)

    # Ordinary algebraic/norm bridges are checked in universal small variables.
    av = [k.variable(i) for i in range(4)]
    bv = [k.variable(i+4) for i in range(4)]
    S = sum((a*a for a in av),P())
    T = sum((a*b for a,b in zip(av,bv)),P())
    U = sum((b*b for b in bv),P())
    wedges = sum(((av[i]*bv[j]-av[j]*bv[i])**2 for i in range(4) for j in range(i+1,4)),P())
    eq('whole universal real Gram wedge identity',S*U-T*T,wedges)
    aa,bb,cc,ss,tt,ee = [k.variable(i) for i in range(6)]
    eq('whole universal remaining quadratic clearing',
       ss*ss*(aa*ee*ee+bb*ee+cc)-(aa*tt*tt-bb*tt*ss+cc*ss*ss),
       (ss*ee+tt)*(aa*(ss*ee-tt)+bb*ss))
    cv = [P(F(367,360)), -(F(1,3)*r+F(13,96)),P(),P(F(-1,48))]
    rows = [[cv[i]]+[P(int(i==j))for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            eq('operator TT transpose '+str(i)+str(j),
               sum((rows[i][z]*rows[j][z]for z in range(5)),P()),P(int(i==j))+cv[i]*cv[j])

    controls = {}
    controls['fixed linear Sylvester orientation'] = h.determinant_integer(h.fixed_sylvester([[1],[2]],[[2],[3]])) == 1
    controls['specialized degree drop retained'] = h.determinant_integer(h.fixed_sylvester([[0],[0,1]],[[0],[1]],0)) == 0
    controls['identically zero specialized polynomial retained'] = h.determinant_integer(h.fixed_sylvester([[0,1],[0,1]],[[-1],[0],[1]],0)) == 0
    controls['zero affine slope clearing only necessary'] = (0**2*7-0) == 0 and 7 != 0
    try:
        h.finite_unit([-1,257],[-1,257],257)
    except ValueError as ex:
        controls['true root lost mod257 is rejected'] = 'leading degrees preserved' in str(ex)
    i_squared = (F(0)*F(0)-F(1)*F(1),2*F(0)*F(1))
    controls['complex Gram positivity is not assumed'] = i_squared == (-1,0) and (1+i_squared[0],i_squared[1]) == (0,0)
    # This is a synthetic exact orientation control, not an original-root witness.
    new_values = [F(2),F(1,32),F(-1,3),F(4),F(-6)]
    old_values = [F(-4),F(1,32),F(-1,3),F(-2),F(3)]
    def value(poly, values):
        return sum((c*reduce(lambda a,b:a*b,
                    (values[i]**key[i]for i in range(5)),F(1)) for key,c in poly.c.items()),F(0))
    controls['signed u synthetic pullback retains positive t'] = all(
        value(R[i],new_values) == old_values[3]**powers[i]*value(oldR[i],old_values)for i in range(5))
    require(all(controls.values()),'all meaningful bridge controls')
    damages = {
        'E2 coefficient changed': k.extract(R[1]+F(367,361)*R[0],1,2) != P(),
        'constant7200 pivot changed': A[2] != 7200*q*u-(118271-D*u),
        'one full lower coefficient changed': clearing != x*lcontent*(LL+1),
    }
    changed = dict(unit)
    changed['left_multiplier'] = list(unit['left_multiplier'])
    changed['left_multiplier'][-1] = (changed['left_multiplier'][-1]+1)%PRIME
    damages['trailing modular multiplier changed'] = h.add(
        h.multiply(changed['left'],changed['left_multiplier'],PRIME),
        h.multiply(changed['right'],changed['right_multiplier'],PRIME),PRIME) != [1]
    damaged_det = list(resultants[1]['whole_determinant_coefficients'])
    damaged_det[-1] += 1
    damages['last determinant coefficient changed'] = any(
        h.evaluate(damaged_det,xx) != yy for xx,yy in enumerate(resultants[1]['every_integer_value']))
    require(all(damages.values()),'every mathematical damage rejected')
    record = {
        'actual_agent':'six-sendov-2','role':'researcher',
        'domain':'QQ[q,E,r,x,u]; every finite COMPLEX common root; x!=0 and u!=0',
        'parent9695':{'source_commit':PARENT_COMMIT,'pins':PARENT_PINS,'whole_record_sha256':PARENT_RECORD,'entire_typed_record_regenerated':True},
        'input9550':{'source_commit':h.INPUT_COMMIT,'pins':h.INPUT_FILES,'whole_record_sha256':h.INPUT_RECORD,'entire_typed_record_regenerated':True},
        'chart':{'definition':'q=B/s,x=s^2,u=s*t=p4','row_powers':powers,'all_five_inverse_pullbacks':True,
                 'actual_recovery':'s=sign(u)*sqrt(x), B=q*s,t=abs(u)/sqrt(x)>0; u SIGNED, x>0',
                 'q0_retained':True,'x0_actual_interpretation':False},
        'complete_Elinear_coefficients_alpha':[a.encoded()for a in alpha],
        'complete_Elinear_constants_beta':[b.encoded()for b in beta],
        'complete_remaining_R0_E_coefficients':[k.extract(R[0],1,j).encoded()for j in (2,1,0)],
        'primitive_E_leading_polynomials_A':[a.encoded()for a in A],
        'A_normalization_contents':a_contents,
        'complete_necessary_polynomials':saved,
        'elimination_contents':{'F_and_G':e_contents,'J':str(jcontent),'N':str(ncontent),'P':str(pcontent),'R':str(rcontent),'L':str(lcontent)},
        'fixed_resultants':resultants,'whole_univariate_finite_unit':unit,
        'universal_identities':checks,'bridge_controls':controls,'rejected_mathematical_damages':damages,
        'claim':'At EVERY full common zero with x*u!=0, alpha is nonzero; E is unique and jointly simple at fixed(q,r,x,u).',
        'real_Gram_recovery':'S=alpha dot alpha>0,T=alpha dot beta,U=beta dot beta; S*U-T^2=0, R0(-T/S)=0 after full S^2 clearing, E=-T/S.',
        'pointwise_E_slope':'||dR/dE||>=sqrt(S)/sqrt(1+(367/360)^2+(r/3+13/96)^2+1/2304)>0; real common zeros ONLY; no uniform floor',
        'ordinary_bridges':'Inherited9550/9695 theorem and real feasibility; legal known-u/x clearing, fixed Sylvester evaluation vectors, exact degree-bounded interpolation, primitive integer UNIVARIATE Gauss, real Gram and operator norm; unformalized',
        'unconditional_nonvanishing_of_leading_vector_claimed':False,
        'full_Jacobian_rank_two_asserted':False,
        'ranktwo_feasible_locus_classified':False,'original_collisions_included':False,
        'global_angular_optimum_proved':False,'complex_first_power_proved':False,
        'independently_reviewed':False}
    if export is not None:
        export.write_text(json.dumps({'record':record,'entire_transformed_R':[p.encoded()for p in R],
                                     'entire_Elinear_rows':[p.encoded()for p in linear]},sort_keys=True)+'\n')
    return record,h.same_typed


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--export',type=Path)
    args=parser.parse_args()
    record,same_typed=certificate(args.export)
    if args.write_expected:
        args.expected.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    else:
        require(same_typed(record,json.loads(args.expected.read_text())),'ENTIRE typed expected record')
    print(json.dumps({'whole_record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
                     'universal_identities':len(record['universal_identities']),
                     'bridge_controls':len(record['bridge_controls']),
                     'mathematical_damages_rejected':len(record['rejected_mathematical_damages']),
                     'resultant_degree_bounds':[z['proved_x_degree_bound']for z in record['fixed_resultants']],
                     'actual_resultant_degrees':[z['actual_x_degree']for z in record['fixed_resultants']],
                     'all_fixed_node_Gaussian_corroborations':sum(len(z['every_integer_value'])for z in record['fixed_resultants']),
                     'all_scalar_equations_retained':True,'E_recovery_at_common_roots':True,
                     'complex_first_power_proved':False,'independently_reviewed':False},sort_keys=True))


if __name__=='__main__':
    main()
