#!/usr/bin/env python3
"""No common complex scalar root on the s=0 angular stationary slice.

Actual six-sendov-2, researcher. Standard library only. The same-author9550
arithmetic and proof premise are explicitly reused, not independently reviewed.
All coefficients, fixed Sylvester determinants, entire interpolation identities
and the univariate finite-field unit are regenerated. No CAS output is a premise.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm, isqrt
import argparse, hashlib, importlib.util, json

INPUT_COMMIT = 'cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4'
INPUT_FILES = {
    'verify.py': '793731739751b6aa21213932a371d3985a5b69f010604017d1a1695fce478deb',
    'expected.json': '37efc29f52d2ddb4efb91fcd3f5c9e69a2f4d96a4e12adf797e6bbb74a760f96'}
INPUT_RECORD = 'c808d09b1f60281d10a76384306b974d8bf94d3647fa037fcf01dd23a76c023c'
PRIME = 257


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def same_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_typed(x, y) for x, y in zip(a, b))
    return a == b


class Capture:
    def write_text(self, value):
        self.data = json.loads(value)


def input9550():
    directory = Path(__file__).resolve().parent.parent/'degree-five-triangular'
    for name, digest in INPUT_FILES.items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
                'pinned9550 source '+name)
    spec = importlib.util.spec_from_file_location('quartic9550_input', directory/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    capture = Capture()
    record = module.make_certificate(capture)
    require(same_typed(record, json.loads((directory/'expected.json').read_text())),
            'entire typed9550 fixture')
    require(hashlib.sha256(canonical(record)).hexdigest() == INPUT_RECORD,
            'entire9550 record digest')
    return module, capture.data


def trim(a, prime=None):
    a = [x % prime for x in a] if prime else list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def add(a, b, prime=None):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))], prime)


def scale(c, a, prime=None):
    return trim([c*x for x in a], prime)


def multiply(a, b, prime=None):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out, prime)


def evaluate(a, x, prime=None):
    out = 0
    for c in reversed(a):
        out = out*x+c
        if prime:
            out %= prime
    return out


def divide(a, b, prime=None):
    a, b = trim(a, prime), trim(b, prime)
    require(b != [0], 'nonzero univariate divisor')
    out = [0]*max(1, len(a)-len(b)+1)
    inverse = pow(b[-1], -1, prime) if prime else F(1, b[-1])
    while a != [0] and len(a) >= len(b):
        j, c = len(a)-len(b), a[-1]*inverse
        if prime:
            c %= prime
        out[j] += c
        a = add(a, [0]*j+scale(-c, b, prime), prime)
    return trim(out, prime), a


def integer_primitive(a):
    a = trim([F(x) for x in a])
    den = lcm(*(c.denominator for c in a))
    common = 0
    for c in a:
        common = gcd(common, abs(int(c*den)))
    require(common > 0, 'nonzero integer primitive polynomial')
    if a[-1] < 0:
        common = -common
    content = F(common, den)
    return [int(c/content) for c in a], content


def fixed_sylvester(a, b, x=0):
    """a,b are formal arrays of coefficients, each a univariate integer array.

    Formal dimensions never change when a leading coefficient vanishes at x.
    Rows encode shifted polynomials in descending formal powers.
    """
    m, n = len(a)-1, len(b)-1
    size = m+n
    require(m > 0 and n > 0, 'positive formal Sylvester degrees')
    av, bv = [evaluate(c, x) for c in a], [evaluate(c, x) for c in b]
    rows = []
    for coeff, count in [(av, n), (bv, m)]:
        for j in reversed(range(count)):
            row = [0]*size
            for k, c in enumerate(coeff):
                row[size-1-k-j] = c
            rows.append(row)
    require(len(rows) == size and all(len(row) == size for row in rows),
            'fixed Sylvester dimensions')
    return rows


def determinant_integer(rows):
    a = [list(row) for row in rows]
    n, previous, sign = len(a), 1, 1
    for k in range(n-1):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        value = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*value-a[i][k]*a[k][j]
                quotient, rest = divmod(numerator, previous)
                require(rest == 0, 'every Bareiss division integral')
                a[i][j] = quotient
            a[i][k] = 0
        previous = value
    return sign*a[-1][-1]


def determinant_fraction(rows):
    """Different same-author arithmetic corroboration, not independent review."""
    a = [[F(x) for x in row] for row in rows]
    answer, n = F(1), len(a)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            answer = -answer
        value = a[k][k]
        answer *= value
        for i in range(k+1, n):
            factor = a[i][k]/value
            for j in range(k+1, n):
                a[i][j] -= factor*a[k][j]
            a[i][k] = 0
    return answer


def interpolate_rational(values):
    difference, basis, result = [F(x) for x in values], [F(1)], [F(0)]
    for k in range(len(values)):
        result = add(result, scale(difference[0], basis))
        difference = [difference[i+1]-difference[i] for i in range(len(difference)-1)]
        if k+1 < len(values):
            basis = scale(F(1, k+1), multiply(basis, [-k, 1]))
    require(all(evaluate(result, x) == y for x, y in enumerate(values)),
            'whole exact interpolation values')
    require(all(c.denominator == 1 for c in result), 'whole determinant coefficients integral')
    return [int(c) for c in result]


def finite_unit(a, b, prime):
    require(type(prime) is int and prime >= 2 and
            all(prime % d for d in range(2, isqrt(prime)+1)), 'field characteristic prime')
    require(all(type(c) is int for c in a+b) and a[-1] % prime and b[-1] % prime,
            'both integer leading degrees preserved modulo prime')
    original = [trim(a, prime), trim(b, prime)]
    a0, a1 = original
    u0, u1, v0, v1 = [1], [0], [0], [1]
    while a1 != [0]:
        q, rest = divide(a0, a1, prime)
        a0, a1 = a1, rest
        u0, u1 = u1, add(u0, scale(-1, multiply(q, u1, prime), prime), prime)
        v0, v1 = v1, add(v0, scale(-1, multiply(q, v1, prime), prime), prime)
    require(len(a0) == 1 and a0[0], 'univariate finite gcd is a unit')
    inverse = pow(a0[0], -1, prime)
    u, v = scale(inverse, u0, prime), scale(inverse, v0, prime)
    require(add(multiply(original[0], u, prime), multiply(original[1], v, prime), prime) == [1],
            'ENTIRE finite Bezout unit coefficient identity')
    return {'prime':prime, 'left':original[0], 'right':original[1],
            'left_multiplier':u, 'right_multiplier':v, 'whole_product':[1],
            'integer_degrees_preserved':[len(a)-1, len(b)-1]}


def certificate(export=None):
    k, data = input9550()
    P = k.P
    B,E,r,s,t = [k.variable(i) for i in range(5)]
    v,w = k.variable(5), k.variable(6)
    checks, encoded = {}, {}
    def eq(name, a, b=0):
        require(P(a) == P(b), 'universal '+name)
        checks[name] = True
    def decode(a):
        require(all(len(key)==5 and all(type(e) is int and e>=0 for e in key)
                    and key[4]==0 for key,c in a), 'entire ordinary four-parameter matrix')
        return P({tuple(key+[0]*5):F(c) for key,c in a})
    M = [[k.sub(decode(a),3,0) for a in row] for row in data['matrix_rows_ABC']]
    R = [row[0]*t*t+row[1]*t+row[2] for row in M]
    def det3(rows):
        a,b,c = [M[i] for i in rows]
        return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
    def primitive(a):
        a = P(a)
        require(bool(a.c), 'nonzero multivariate primitive input')
        den = lcm(*(c.denominator for c in a.c.values()))
        common = 0
        for c in a.c.values():
            common = gcd(common, abs(int(c*den)))
        if a.c[max(a.c)] < 0:
            common = -common
        content = F(common,den)
        out = P({key:c/content for key,c in a.c.items()})
        eq('primitive_reconstruction_'+str(len(checks)), content*out, a)
        return out
    def quotient(a,b,index):
        a,b = P(a),P(b)
        require(bool(b.c), 'nonzero polynomial divisor')
        coeff = k.coefficients(b,index)
        leading = k.scalar(coeff[-1])
        require(leading != 0, 'division only by a NONZERO RATIONAL leading coefficient')
        out = P(0)
        while a.c:
            ac = k.coefficients(a,index)
            if len(ac) < len(coeff):
                break
            monomial = ac[-1]*F(1,leading)*k.variable(index)**(len(ac)-len(coeff))
            out += monomial
            a -= monomial*b
        return out,a
    def exact_quotient(a,b,index,name):
        q,rem = quotient(a,b,index)
        eq(name+'_whole_reconstruction', q*b, a)
        require(not rem.c, name+' zero entire remainder')
        return q
    def dense(a,index):
        return [k.scalar(c) for c in k.coefficients(a,index)]
    def array(a,index):
        return integer_primitive(dense(a,index))[0]
    def fixed_nonzero_pair(a,b,index,name):
        aa,bb = array(a,index),array(b,index)
        rows = fixed_sylvester([[c]for c in aa], [[c]for c in bb])
        determinant = determinant_integer(rows)
        require(determinant != 0 and determinant_fraction(rows)==determinant,
                name+' entire nonzero determinant corroborated')
        return {'left':aa,'right':bb,'formal_degrees':[len(aa)-1,len(bb)-1],
                'Sylvester_size':len(rows),'entire_matrix':rows,'determinant':str(determinant),
                'same_author_fraction_determinant_agrees':True}

    H = 2112*E+10976*r*r+7344*r+1143
    K = 14400*E+65856*r*r+38160*r+4725
    W = 5488*r*r+7280*r+1875
    D = (262144*E*E*r+102400*E*E+786432*E*r**3+663552*E*r*r+
         153600*E*r+5760*E+36864*r**4+18432*r**3-1152*r*r-864*r+81)
    eq('t_zero_constant_column',M[0][2]-14*M[4][2],-192)
    eq('complete_scalar_row3',18816*R[3],t*(B*t*K-112*H))
    eq('complete_three_branch_minor023',det3([0,2,3]),F(5,774144)*(7*r+3)*H*D)
    eq('complete_HK_cross',2112*K-14400*H,-3456*W)

    # H=0: since Bt!=0, K=0. Substitute only the constant-pivot E formula.
    minor = det3([0,2,4])
    require(all(key[0]>=1 for key in minor.c), 'minor024 entire B factor')
    divided = P({(key[0]-1,)+key[1:]:c for key,c in minor.c.items()})
    eq('minor024_legal_B_factor',B*divided,minor)
    EH = F(-1,2112)*(10976*r*r+7344*r+1143)
    substituted = k.sub(divided,1,EH)
    q,L = quotient(substituted,W,2)
    eq('H0_entire_W_remainder_identity',substituted,q*W+L)
    require(all(all(e==0 for i,e in enumerate(key)if i!=2)for key in L.c),
            'H0 remainder is ENTIRE univariate r polynomial')
    require(len(k.coefficients(L,2))==2,'H0 linear necessary remainder')
    L = primitive(L)
    HK = fixed_nonzero_pair(W,L,2,'H0_K0_branch')

    # H!=0: R3 supplies the PROVED nonzero K and w=Bt=112H/K.
    # No affine slope in v is divided. The entire multiplication syzygy remains.
    Ys,Ws = {},{}
    for i in [0,1,2,4]:
        power = 1 if i==1 else 2
        terms = {}
        for key,c in R[i].c.items():
            require(all(e==0 for j,e in enumerate(key)if j not in [0,1,2,4]),
                    's0 residual four-variable domain')
            exponent = key[0]+power-key[4]
            require(exponent>=0 and exponent%2==0,'whole scalar transformation parity and clearing')
            new = list(key)
            new[0]=new[4]=0
            new[5]=exponent//2
            new[6]=key[4]
            terms[tuple(new)] = terms.get(tuple(new),F(0))+c
        y = P(terms)
        yc = k.coefficients(y,6)+[P(0)]*3
        require(len(k.coefficients(y,6))<=3,'whole w degree at most2')
        raw = sum((yc[j]*(112*H)**j*K**(2-j)for j in range(3)),P(0))
        eq('whole_K_clearing_syzygy_'+str(i),K*K*y-raw,
           (K*w-112*H)*(yc[2]*(K*w+112*H)+K*yc[1]))
        require(len(k.coefficients(raw,5))==2,'whole cleared equations affine in v')
        Ys[i],Ws[i] = y,primitive(raw)
    A = {}
    for i,hpower in [(1,1),(4,2)]:
        f0,f1 = k.coefficients(Ws[0],5)
        g0,g1 = k.coefficients(Ws[i],5)
        cross = f1*g0-g1*f0
        # Elimination does NOT assume f1 or g1 nonzero.
        eq('entire_zero_slope_affine_cross_'+str(i),f1*Ws[i]-g1*Ws[0],cross)
        reduced = cross
        for j in range(hpower):
            reduced = exact_quotient(reduced,H,1,'H_factor_'+str(i)+'_'+str(j))
        A[i] = primitive(reduced)
        require(all(all(e==0 for j,e in enumerate(key)if j not in [1,2])for key in A[i].c),
                'entire reduced eliminant in QQ[E,r]')
    require(len(k.coefficients(A[1],1))==6 and len(k.coefficients(A[4],1))==5,
            'formal scalar eliminant E degrees5/4')

    # First branch: r=-3/7, H!=0. A5 and A4 have no common complex E.
    one_branch = fixed_nonzero_pair(k.sub(A[1],2,F(-3,7)),k.sub(A[4],2,F(-3,7)),1,
                                   'r_minus3over7_branch')
    # Last branch: D=0, A5=A4=0. Formal determinants retain EVERY degree loss.
    resultants = {}
    quotients = []
    for i in [1,4]:
        def coefficients_r(a):
            out=[]
            for c in k.coefficients(a,1):
                vals=dense(c,2)
                require(all(x.denominator==1 for x in vals),'integer Sylvester coefficients')
                out.append([int(x)for x in vals])
            return out
        da,aa = coefficients_r(D),coefficients_r(A[i])
        m,n = len(da)-1,len(aa)-1
        degree_D=max(len(row)-1 for row in da)
        degree_A=max(len(row)-1 for row in aa)
        bound = n*degree_D+m*degree_A
        values=[]
        for point in range(bound+1):
            rows = fixed_sylvester(da,aa,point)
            val = determinant_integer(rows)
            require(determinant_fraction(rows)==val,'every whole char0 determinant independently recomputed arithmetically')
            values.append(val)
        poly = interpolate_rational(values)
        require(len(poly)-1<=bound,'entire reconstructed determinant degree bound')
        common = multiply(multiply([3,8],[3,8]),[3,8])
        q,rem = divide(poly,common)
        require(rem==[0] and multiply(q,common)==poly,'ENTIRE (8r+3)^3 determinant factor')
        qi,content = integer_primitive(q)
        require(scale(content,multiply(qi,common))==[F(x)for x in poly],
                'ENTIRE normalized resultant reconstruction')
        quotients.append(qi)
        resultants[str(i)] = {'formal_E_degrees':[m,n],'fixed_Sylvester_size':m+n,
             'proved_r_degree_bound':bound,'distinct_exact_evaluations':bound+1,
             'actual_r_degree':len(poly)-1,'entire_determinant':poly,
             'common_factor_ascending':common,'normalized_quotient':qi,'content':str(content),
             'same_author_fraction_comparisons':bound+1,
             'entire_values_sha256':hashlib.sha256(canonical(values)).hexdigest()}
    require([len(q)-1 for q in quotients]==[22,19],'complete residual quotient degrees22/19')
    unit = finite_unit(*quotients,PRIME)
    eq('D_at_remaining_r',k.sub(D,2,F(-3,8)),4096*E*E)
    hpoint = k.scalar(k.sub(k.sub(H,2,F(-3,8)),1,0))
    kpoint = k.scalar(k.sub(k.sub(K,2,F(-3,8)),1,0))
    require(hpoint==F(-135,2) and kpoint==-324,'entire remaining scalar pivot values')
    wpoint=112*hpoint/kpoint
    require(wpoint==F(70,3),'entire remaining w recovery')
    eq('entire_remaining_original_R0_contradiction',
       k.sub(k.sub(k.sub(Ys[0],2,F(-3,8)),1,0),6,wpoint),14*v)

    # Meaningful bridge controls. Literal algebraic data are not angular profiles.
    control=[]
    degree_loss=fixed_sylvester([[0],[0,1]],[[-1],[1]],0)
    require(degree_loss==[[0,0],[1,-1]] and determinant_integer(degree_loss)==0,
            'formal leading-degree loss common-root necessity retained')
    control.append('specialized_leading_coefficient_zero')
    require(determinant_integer([[0,1],[2,3]])==-2 and
            determinant_fraction([[0,1],[2,3]])==-2,'whole pivot row-swap sign')
    control.append('determinant_row_swap')
    require(interpolate_rational([3,10,21])==[3,5,2],'whole rational Newton interpolation')
    control.append('exact_interpolation_entire_polynomial')
    for name,f0,f1,g0,g1 in [('first_slope_zero',0,0,-1,1),
                            ('second_slope_zero',-1,1,0,0),
                            ('both_slopes_zero',0,0,0,0)]:
        require(f1*g0-g1*f0==0 and f0+f1==0 and g0+g1==0,
                'affine elimination retains zero slopes')
        control.append(name)
    damages=[]
    bad=list(unit['left_multiplier']);bad[-1]=(bad[-1]+1)%PRIME
    try:
        require(add(multiply(unit['left'],bad,PRIME),multiply(unit['right'],unit['right_multiplier'],PRIME),PRIME)==[1],
                'damaged whole trailing unit coefficient')
    except ValueError:
        damages.append('trailing_finite_unit_coefficient')
    else:
        raise ValueError('mathematical damage survived unit')
    for name,a,b in [
        ('wrong_scalar_row_sign',18816*R[3],t*(B*t*K+112*H)),
        ('dropped_minor_H_branch',det3([0,2,3]),F(5,774144)*(7*r+3)*D),
        ('remaining_endpoint_misreported_zero',14*v,P(0)),
        ('wrong_clear_multiplier',K*K*Ys[0],Ws[0]),
    ]:
        try:
            require(P(a)==P(b),'damaged '+name)
        except ValueError:
            damages.append(name)
        else:
            raise ValueError('mathematical damage survived '+name)
    encoded={'variable_order':['B','E','r','s','t','v','w','unused7','unused8','unused9'],
             'coefficient_format':'[ten nonnegative integer exponents, exact rational coefficient]',
             'matrix_s0':[[a.encoded()for a in row]for row in M],
             'residuals_s0':[a.encoded()for a in R],
             'H':H.encoded(),'K':K.encoded(),'W':W.encoded(),'D':D.encoded(),
             'HK_linear_remainder':L.encoded(),
             'Y':{str(i):a.encoded()for i,a in Ys.items()},
             'cleared_W':{str(i):a.encoded()for i,a in Ws.items()},
             'A5':A[1].encoded(),'A4':A[4].encoded()}
    record={'actual_agent':'six-sendov-2','role':'researcher',
        'domain':'QQ[B,E,r,t]; s=0; no common finite scalar root over COMPLEX parameters',
        'input9550':{'source_commit':INPUT_COMMIT,'file_sha256':INPUT_FILES,'whole_record_sha256':INPUT_RECORD,
                     'entire_fixture_regenerated':True,'same_author_reuse':True},
        'universal_identities':sorted(checks),'entire_generated_polynomials':encoded,
        'H0_K0_nonzero_resultant':HK,'r_minus3over7_nonzero_resultant':one_branch,
        'D_branch_fixed_resultants':resultants,'D_branch_whole_finite_unit':unit,
        'remaining_point':{'r':'-3/8','E':'0','H':str(hpoint),'K':str(kpoint),'Bt':str(wpoint),'R0':'14'},
        'bridge_controls':control,'rejected_mathematical_damages':damages,
        'original_interpretation':'eight DISTINCT REAL balanced stationary originals: mass interpolant p4!=0; no additional value/variance premise',
        'ordinary_bridges':'9550 complex B=s=0 obstruction and feasible stationarity; legal polynomial clearing; fixed Sylvester evaluation-column necessity, exact degree-bounded interpolation, primitive univariate Gauss, complex algebra; unformalized',
        'global_complex_s_nonzero_rankone_locus_classified':False,
        'ranktwo_feasible_locus_classified':False,'original_collisions_included':False,
        'quantitative_lower_bound_for_abs_p4':False,'complex_first_power_proved':False,
        'global_angular_optimum_proved':False,'independently_reviewed':False}
    if export is not None:
        export.write_text(json.dumps(encoded,indent=2,sort_keys=True)+'\n')
    return record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--export',type=Path)
    args=parser.parse_args()
    record=certificate(args.export)
    if args.emit:
        args.expected.write_text(canonical(record).decode()+'\n')
    else:
        require(same_typed(record,json.loads(args.expected.read_text())),'ENTIRE typed expected record')
    print(json.dumps({'verified':True,'actual_agent':'six-sendov-2','role':'researcher',
        'record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
        'universal_identity_count':len(record['universal_identities']),
        'whole_resultant_degrees':[v['actual_r_degree']for v in record['D_branch_fixed_resultants'].values()],
        'fixed_identity_evaluation_counts':[v['distinct_exact_evaluations']for v in record['D_branch_fixed_resultants'].values()],
        'bridge_control_count':len(record['bridge_controls']),
        'rejected_damage_count':len(record['rejected_mathematical_damages']),
        's0_common_complex_scalar_root_exists':False,
        'complex_first_power_proved':False},sort_keys=True))


if __name__=='__main__':
    main()
