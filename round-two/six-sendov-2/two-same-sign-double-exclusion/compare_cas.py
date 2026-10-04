"""Dense QQ(p,tau)[z] reconstruction and exact tensor interpolation.

SymPy 1.14.0. No private data or native arithmetic is imported. The native
module is loaded only after the dense certificate, all whole intermediates,
both whole Bernstein polynomials and all20 seven-slot cases are rebuilt.
Same author, distinct representations; this is not independent peer review.
"""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,time
import sympy as s

BASE=Path(__file__).resolve().parent
P,TAU,Z,Y,U,B,A=s.symbols('p tau z y u b a')
START=time.monotonic()

def require(ok,message):
    if not ok:raise ValueError(message)

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode('utf-8')

def progress(stage):
    print(json.dumps({'stage':stage,'seconds':time.monotonic()-START}),flush=True)

def terms(expression,variables=(P,TAU)):
    poly=s.Poly(expression,*variables,domain=s.QQ)
    return [{'powers':list(powers),'coefficient':str(c)}
            for powers,c in sorted(poly.terms()) if c]

def outer(poly):
    return [terms(poly.nth(i))for i in range(poly.degree()+1)]

def raw_sturm(poly):
    chain=[poly,poly.diff()]
    while True:
        rem=chain[-2].rem(chain[-1])
        if rem.is_zero:break
        chain.append(-rem)
    def variations(values):
        signs=[s.sign(x)for x in values if x]
        return sum(x!=y for x,y in zip(signs,signs[1:]))
    zero=variations([p.nth(0)for p in chain])
    plus=variations([p.LC()for p in chain])
    minus=variations([p.LC()*(-1)**p.degree()for p in chain])
    return {'positive_distinct':int(zero-plus),'negative_distinct':int(minus-zero),
            'gcd_degree':chain[-1].degree(),
            'entire_sturm_chain':[[str(p.nth(i))for i in range(p.degree()+1)]for p in chain]}

def tensor_interpolation(poly):
    # Exactly reconstruct degree-(n,m) polynomial from distinct rational
    # knots in the Bernstein basis, then compare every symbolic coefficient.
    unit=s.Poly(s.expand(poly.as_expr().subs(U,1+s.Rational(9,40)*A)),A,B,domain=s.QQ)
    n,m=unit.degree_list()
    xs=[s.Rational(i,n)for i in range(n+1)]
    ys=[s.Rational(j,m)for j in range(m+1)]
    left=s.Matrix([[s.binomial(n,k)*x**k*(1-x)**(n-k)for k in range(n+1)]for x in xs])
    right=s.Matrix([[s.binomial(m,l)*y**l*(1-y)**(m-l)for l in range(m+1)]for y in ys])
    samples=s.Matrix([[unit.eval(A,x).eval(B,y)for y in ys]for x in xs])
    coefficients=left.inv()*samples*right.inv().T
    require(left*coefficients*right.T==samples,'whole exact tensor interpolation equations')
    bases_a=[s.Poly(s.binomial(n,k)*A**k*(1-A)**(n-k),A,B,domain=s.QQ)for k in range(n+1)]
    bases_b=[s.Poly(s.binomial(m,l)*B**l*(1-B)**(m-l),A,B,domain=s.QQ)for l in range(m+1)]
    rebuilt=s.Poly(0,A,B,domain=s.QQ)
    for k in range(n+1):
        curve=s.Poly(0,A,B,domain=s.QQ)
        for l in range(m+1):curve+=bases_b[l].mul_ground(coefficients[k,l])
        rebuilt+=bases_a[k]*curve
    require(rebuilt==unit,'ENTIRE reconstructed Bernstein polynomial')
    require(all(c>0 for c in coefficients),'all530 independently reconstructed signs')
    return {'whole_original_terms':terms(poly.as_expr(),(U,B)),
            'whole_unit_terms':terms(unit.as_expr(),(A,B)),
            'complete_tensor_bernstein':[[str(coefficients[k,l])for l in range(m+1)]for k in range(n+1)]}

def seven_slot_cases():
    rows=[]
    for r in [s.Rational(101,100),s.Rational(21,20),s.Rational(11,10),s.Rational(10,9)]:
        p=r+r**3;b0=1+2*r*r-r**4-r**6;t=(r*r-1)**2*(r*r+1)
        require(r>1 and b0>0,'dense actual original parameter')
        d2=Z*Z-p*Z+1;gU=d2*d2;q=(Z-p)**2+1
        for fraction in [s.Rational(0),s.Rational(1,4),s.Rational(1,2),s.Rational(3,4),s.Rational(1)]:
            tau=fraction*t;other=s.Poly(gU-tau*q,Z,domain=s.QQ)
            roots=raw_sturm(other);count=2 if fraction==0 else 3 if fraction==1 else 4
            require(roots['positive_distinct']==count and roots['negative_distinct']==0
                    and roots['gcd_degree']==4-count,'dense whole actual root count')
            f=s.Poly(s.expand(gU*other.as_expr().subs(Z,-Z)),Z,domain=s.QQ)
            h=f.diff().mul_ground(s.Rational(1,8));H=s.zeros(7)
            for j in range(6):H[j+1,j]=1
            for j in range(7):H[j,6]=-h.nth(j)
            def evaluate(poly):
                value=s.zeros(7)
                for c in poly.all_coeffs():value=value*H+c*s.eye(7)
                return value
            hp=evaluate(h.diff());inverse=hp.inv()
            require(hp*inverse==s.eye(7),'dense whole seven-slot inverse')
            mass=-8*evaluate(f)*inverse
            N=-2*f.nth(6);X=N*N/2-4*f.nth(4);D=X-N*N/8
            eta=s.trace(mass*mass);C=(N*N-eta)/D
            require(s.trace(mass)==N and D>0 and C<16,'dense actual mass checks')
            moments=[s.Integer(8)]
            for k in range(1,6):
                value=-k*f.nth(8-k)
                for j in range(1,k):value-=f.nth(8-j)*moments[k-j]
                moments.append(value)
            require(moments[1]==moments[3]==moments[5]==0
                    and moments[2]==N and moments[4]==X,'dense whole original powers')
            rows.append({'r':str(r),'p':str(p),'y':str(p*p),'B':str(b0),
                         'fraction_of_T':str(fraction),'tau':str(tau),
                         'actual_companion_root_record':roots,
                         'whole_f':[str(f.nth(i))for i in range(9)],
                         'whole_h':[str(h.nth(i))for i in range(8)],
                         'original_first_five_powers':[str(c)for c in moments[1:]],
                         'N':str(N),'X':str(X),'D':str(D),'raw_eta':str(eta),
                         'angular_C':str(C),'all_seven_slots_accounted_for':True})
    return rows

def main():
    require(s.__version__=='1.14.0','pinned SymPy version')
    cert=json.loads((BASE/'CERTIFICATE.json').read_text())
    d2=Z*Z-P*Z+1;q=(Z-P)**2+1;other=d2*d2-TAU*q
    ring=s.QQ.poly_ring(P,TAU);field=s.QQ.frac_field(P,TAU)
    f=s.Poly(s.expand(d2*d2*other.subs(Z,-Z)),Z,domain=ring)
    h=f.diff().mul_ground(s.Rational(1,8))
    H5,rem=h.div(s.Poly(d2,Z,domain=ring))
    require(rem.is_zero and H5.LC()==1,'dense whole canceled quintic')
    H=s.Poly(H5.as_expr(),Z,domain=field);inverse=s.invert(H.diff(),H)
    Delta=s.Poly(1,P,TAU,domain=s.QQ)
    for i in range(5):
        Delta=s.lcm(Delta,s.Poly(s.fraction(s.cancel(inverse.nth(i)))[1],P,TAU,domain=s.QQ))
    Delta=Delta.monic()
    nums=[s.cancel(inverse.nth(i)*Delta.as_expr())for i in range(5)]
    I=s.Poly(sum(c*Z**i for i,c in enumerate(nums)),Z,domain=ring)
    inv_quotient,inv_remainder=(H5.diff()*I).div(H5)
    require(inv_remainder==s.Poly(Delta.as_expr(),Z,domain=ring),'dense whole derivative inverse')
    disc=s.Poly(s.discriminant(H5.as_expr(),Z),P,TAU,domain=s.QQ)
    disc_quotient,rem=disc.div(Delta);require(rem.is_zero,'dense entire discriminant divisor')
    progress('dense quintic inverse and full discriminant rebuilt')
    mass=(s.Poly(-8*d2*other.subs(Z,-Z),Z,domain=field)*inverse).rem(H)
    mass_num=s.Poly(s.cancel(mass.as_expr()*Delta.as_expr()),Z,domain=ring)
    mass2_num=(mass_num*mass_num).rem(H5)
    powers=[s.Integer(5)]
    for k in range(1,5):
        value=-k*H5.nth(5-k)
        for j in range(1,k):value-=H5.nth(5-j)*powers[k-j]
        powers.append(s.expand(value))
    def trace(poly):return s.expand(sum(poly.nth(i)*powers[i]for i in range(5)))
    N=s.expand(-2*f.nth(6));X=s.expand(N*N/2-4*f.nth(4));D=s.expand(X-N*N/8)
    require(trace(mass_num)==s.expand(N*Delta.as_expr()),'dense whole mass normalization')
    eta_num=trace(mass2_num)
    C=s.cancel((N*N-s.cancel(eta_num/Delta.as_expr()**2))/D)
    num,den=s.fraction(C)
    def even_conversion(expr):
        result=0
        for (i,j),c in s.Poly(expr,P,TAU,domain=s.QQ).terms():
            require(i%2==0,'dense reflection-even power')
            result+=c*Y**(i//2)*TAU**j
        return s.Poly(result,Y,TAU,domain=s.QQ)
    num_y,den_y=map(even_conversion,(num,den))
    rebuilt_cert={'domain':cert['domain'],'critical_quintic':outer(H5),
                  'inverse_common_denominator':terms(Delta.as_expr()),
                  'inverse_numerators':[terms(a)for a in nums],
                  'discriminant':terms(disc.as_expr()),
                  'discriminant_divided_by_inverse_denominator':terms(disc_quotient.as_expr()),
                  'angular_numerator_y_tau':terms(num_y.as_expr(),(Y,TAU)),
                  'angular_denominator_y_tau':terms(den_y.as_expr(),(Y,TAU))}
    require(rebuilt_cert==cert,'ENTIRE dense defining certificate agrees')
    substitution={Y:U*(1+U)**2,TAU:(U-1)**2*(U+1)*B}
    common=s.Poly((U-1)**4*(U+1)**6,U,B,domain=s.QQ)
    normalized_num=s.Poly(s.expand(num_y.as_expr().subs(substitution)),U,B,domain=s.QQ).exquo(common)
    normalized_den=s.Poly(s.expand(den_y.as_expr().subs(substitution)),U,B,domain=s.QQ).exquo(common)
    gap=(16*normalized_den-normalized_num).exquo(s.Poly(U-1,U,B,domain=s.QQ))
    fields={'denominator':tensor_interpolation(normalized_den),
            'divided_gap16':tensor_interpolation(gap)}
    progress('all530 tensor coefficients independently interpolated; both entire polynomials verified')
    raw_num=s.expand(N*N*Delta.as_expr()**2-eta_num)
    cleared=s.expand(raw_num*den_y.as_expr().subs(Y,P*P))
    other_side=s.expand(D*Delta.as_expr()**2*num_y.as_expr().subs(Y,P*P))
    require(cleared==other_side,'dense entire cleared angular identity')
    complete={'whole_f':outer(f),'whole_H5':outer(H5),'whole_discriminant':terms(disc.as_expr()),
              'whole_inverse_identity_quotient':outer(inv_quotient),
              'whole_mass_remainders':outer(mass_num),'whole_squared_mass_remainders':outer(mass2_num),
              'whole_mass_trace':terms(trace(mass_num)),'whole_eta_numerator':terms(eta_num),
              'whole_cleared_angular_identity':terms(cleared),
              'whole_transformed_numerator':terms(normalized_num.as_expr(),(U,B)),
              'fields':fields}
    cases=seven_slot_cases()
    progress('all20 dense actual Sturm/seven-slot profiles independently rebuilt')
    # Native arithmetic was not used to obtain any preceding result.
    spec=importlib.util.spec_from_file_location('native_final_comparison',BASE/'verify.py')
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    native_record,native_complete=native.build(native.load_json(BASE/'CERTIFICATE.json'))
    native.typed_equal(complete,native_complete)
    native.typed_equal(cases,native_record['actual_seven_slot_cases'])
    native.typed_equal(native_record,native.load_json(BASE/'EXPECTED.json'))
    print(json.dumps({'status':'entire dense certificate, all whole intermediates, all530tensor entries and20actual cases agree',
                      'record_sha256':sha256(canonical(native_record)).hexdigest(),
                      'same_author_not_peer_review':True,'seconds':time.monotonic()-START}))

if __name__=='__main__':main()
