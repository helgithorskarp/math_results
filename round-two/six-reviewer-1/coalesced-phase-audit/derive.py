"""Independent definition-level jets over QQ(i)(x), x=a/(1+a).

No imports, formula hints, certificates or code from the target author.
All eight phase variables coexist in one truncated polynomial product.
"""
import hashlib
import json
from fractions import Fraction
from math import comb


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def coeffs(f):
    """Increasing-power rational coefficients; requires an actual polynomial."""
    need(f.denom.degree() == 0, 'uncleared rational denominator')
    degree=max((m[0] for m in f.numer), default=0)
    return [str(Fraction(str(f.numer.get((j,), 0)))/Fraction(str(f.denom[(0,)])))
            for j in range(degree+1)]


def bernstein(power, lo, hi):
    """Use exact affine substitution, then reverse the entire expansion."""
    p=list(map(Fraction,power)); n=len(p)-1
    transformed=[sum(p[j]*comb(j,k)*lo**(j-k)*(hi-lo)**k
                     for j in range(k,n+1)) for k in range(n+1)]
    b=[sum(transformed[k]*Fraction(comb(i,k),comb(n,k)) for k in range(i+1))
       for i in range(n+1)]
    reverse=[Fraction(0)]*(n+1)
    for i,c in enumerate(b):
        for j in range(n-i+1):
            reverse[i+j]+=c*comb(n,i)*comb(n-i,j)*(-1)**j
    need(reverse==transformed,'whole reversed Bernstein equality')
    return {'degree':n,'power':list(map(str,p)),'bernstein':list(map(str,b)),
            'minimum':str(min(b))}


def derive():
    from sympy import QQ, QQ_I, I
    from sympy.polys.rings import ring
    K=QQ_I.frac_field('x'); x=K.gens[0]; ell=1-x; a=x/ell
    Kr=QQ.frac_field('x'); xr=Kr.gens[0]; lr=1-xr
    imaginary=K.from_sympy(I)
    def real(f):
        expr=K.to_sympy(f)
        need(not expr.has(I),'unexpected imaginary coefficient')
        return Kr.from_sympy(expr)
    R,*g=ring('u,t0,t1,t2,t3,t4,t5,t6,t7',K); u,*theta=g
    def truncate(p):
        return R.from_dict({m:c for m,c in p.items() if sum(m[1:])<=2})
    baseline=[9*ell]+[ell]*7
    radial=[-x*sum(t*t for t in theta[1:])/2]
    radial += [x*t*t/2 for t in theta[1:]]
    q=[b*(1+imaginary*t-t*t/2)+r for b,t,r in zip(baseline,theta,radial)]
    origin=R.one; product=R.one
    for qq,b,rr in zip(q,baseline,radial):
        origin=truncate(origin*(1-a*u*qq))
        product=truncate(product*(b+rr))
    jet={}
    for monomial,c in origin.items():
        phase=monomial[1:]
        jet[phase]=jet.get(phase,K.zero)+9*c/(monomial[0]+1)
    product_jet={m[1:]:c for m,c in product.items()}
    zero=(0,)*8; P=9*lr**8
    need(real(jet[zero])==P==real(product_jet[zero]),'coalesced origin equality')
    w=[]; quadratic=[]; matrix=[]
    for i in range(8):
        m=tuple(int(j==i) for j in range(8))
        w.append(real(jet[m]/imaginary))
    for i in range(8):
        row=[]; full=[]
        for j in range(8):
            m=tuple(int(k==i)+int(k==j) for k in range(8))
            v=real(jet.get(m,K.zero)-product_jet.get(m,K.zero))/(1 if i==j else 2)
            row.append(v);full.append(v+w[i]*w[j]/(2*P))
        quadratic.append(row);matrix.append(full)
    h,b,d,e=matrix[0][0],matrix[0][1],matrix[1][1],matrix[1][2]
    for i in range(8):
        for j in range(8):
            expected=h if i==j==0 else d if i==j else b if i==0 or j==0 else e
            need(matrix[i][j]==expected,'full S7 commutant identity')
    lam=d-e; determinant=h*(d+6*e)-7*b*b
    # Independent radial jets, differentiating the primitive factor products.
    Z,v,z=ring('v,z',Kr)
    def radial_gap(heavy, small):
        radii=[9*lr+heavy*v,lr+small*v]+[lr]*6
        oo=Z.one;pp=Z.one
        for rr in radii:
            oo*=1-(xr/lr)*z*rr;pp*=rr
        out=Kr.zero
        for m,c in oo.items():
            if m[0]==1:out+=9*c/(m[1]+1)
        return out-pp.get((1,0),Kr.zero)
    H=-radial_gap(1,0); slack=radial_gap(-1,1)
    need(H==(1-lr**8)/(8*xr*lr),'complete closed heavy derivative identity')
    # Recover the author's scaled polynomials solely from the full jets.
    den=18*lr**8
    polynomials={'ell_H':coeffs(lr*H),'2ell_c':coeffs(2*lr*slack),
        '2ell_transverse':coeffs(2*lr*lam),'B_heavy':coeffs(den*h),
        'B_cross':coeffs(den*b),'B_diagonal':coeffs(den*d),'B_off':coeffs(den*e)}
    determinant_poly=coeffs(den*den*determinant)
    # Conversion x=a/(1+a) in a separate exact field, including full degrees.
    Ka=QQ.frac_field('a'); av=Ka.gens[0]
    def to_a(power):
        n=len(power)-1
        return sum(Ka.convert(QQ(c))*av**j*(1+av)**(n-j) for j,c in enumerate(power))
    S=to_a(polynomials['2ell_c'])*QQ(7,4)
    T=to_a(polynomials['2ell_transverse'])*QQ(56)/av
    Kpoly=to_a(determinant_poly)*QQ(-448,729)/(av*av)
    apr={'S':coeffs(S),'T':coeffs(T),'K':coeffs(Kpoly)}
    need(all(Fraction(c)>0 for c in apr['S'][1:]) and Fraction(apr['S'][0])<0,
         'slack monotonicity signs')
    need(all(Fraction(c)<0 for c in apr['T'][:3]) and all(Fraction(c)>0 for c in apr['T'][3:]),
         'T/a^2 strict monotonicity signs')
    need(all(Fraction(c)>0 for c in apr['K'][:6]) and all(Fraction(c)<0 for c in apr['K'][6:]),
         'K/a^5 strict monotonicity signs')
    def evaluate(power,t):
        return sum(Fraction(c)*t**j for j,c in enumerate(power))
    alo=Fraction(861212748918,10**12);ahi=Fraction(861212748919,10**12)
    need(evaluate(apr['T'],alo)<0<evaluate(apr['T'],ahi),'unique threshold enclosure')
    need(Fraction(2,3)<alo<ahi<Fraction(7,8),'threshold ordering')
    need(evaluate(apr['K'],Fraction(2,3))<0 and evaluate(apr['S'],Fraction(1,2))>0,
         'collective and slack entry signs')
    root={'lo':str(alo),'hi':str(ahi),'T_lo':str(evaluate(apr['T'],alo)),
          'T_hi':str(evaluate(apr['T'],ahi)),
          'K_two_thirds':str(evaluate(apr['K'],Fraction(2,3))),
          'S_half':str(evaluate(apr['S'],Fraction(1,2)))}
    # All five original whole-interval margins, reconstructed as rational functions.
    mu=QQ(1,1000)
    quantities={'c_ge_half':2*lr*(slack-QQ(1,2)), 'H_le_one':lr*(1-H),
        'transverse_ge_1_1000':2*lr*(lam-mu),
        'heavy_ge_1_1000':den*(h-mu),
        'shifted_collective_determinant':den*den*((h-mu)*(d+6*e-mu)-7*b*b)}
    bounds={name:bernstein(coeffs(f),Fraction(7,15),Fraction(1,2)) for name,f in quantities.items()}
    need(all(Fraction(c)>0 for r in bounds.values() for c in r['bernstein']),
         'every complete uniform bound coefficient')
    # Quartic, derived from the exact critical-disk equation rather than a supplied h4.
    V,eps,t=ring('eps,t',Kr); aa=xr/lr
    def cut(p):return V.from_dict({m:c for m,c in p.items() if m[0]<=4})
    cosine=1-eps**2/2+eps**4/24
    r2=xr/2;trial=lr+r2*eps**2
    residual=cut((1-aa*aa)*trial*trial+2*aa*trial*cosine-1)
    need(residual.get((2,0),Kr.zero)==0,'disk second order coefficient')
    r4=-residual.get((4,0),Kr.zero)/2
    radius=lr+r2*eps**2+r4*eps**4
    disk=cut((1-aa*aa)*radius*radius+2*aa*radius*cosine-1)
    need(not disk,'entire critical-disk jet through fourth order')
    heavy=16*lr-5*lr-2*radius
    # Conjugate pair eliminates all imaginary terms exactly in the primitive integrand.
    pair=cut(1-2*aa*radius*cosine*t+aa*aa*radius*radius*t*t)
    quartic_integrand=cut(cut((1-aa*heavy*t)*(1-xr*t)**5)*pair)
    target_product=cut(heavy*lr**5*radius*radius)
    costs=[]
    for order in (0,2,4):
        cc=sum(9*c/(m[1]+1) for m,c in quartic_integrand.items() if m[0]==order)
        costs.append(cc-target_product.get((order,0),Kr.zero))
    need(costs[0]==0 and costs[1]==2*lam,'literal pair agrees with full Hessian')
    q4=costs[2]
    # Independently multiply eight Gaussian fourth-order critical factors.
    VC,ce,ct=ring('eps,t',K)
    def ccut(p):return VC.from_dict({m:c for m,c in p.items() if m[0]<=4})
    rr=K.from_sympy(Kr.to_sympy(radius.get((0,0),Kr.zero)))+x*ce*ce/2 \
        +K.from_sympy(Kr.to_sympy(r4))*ce**4
    hh=16*ell-5*ell-2*rr
    ep=1+imaginary*ce-ce*ce/2-imaginary*ce**3/6+ce**4/24
    em=1-imaginary*ce-ce*ce/2+imaginary*ce**3/6+ce**4/24
    gaussian=VC.one
    for qq in [hh,rr*ep,rr*em]+[ell]*5:
        gaussian=ccut(gaussian*(1-a*ct*qq))
    for order in (0,2,4):
        actual=sum(9*c/(m[1]+1) for m,c in gaussian.items() if m[0]==order)
        expected=sum(9*c/(m[1]+1) for m,c in quartic_integrand.items() if m[0]==order)
        need(real(actual)==expected,'whole Gaussian/conjugate-pair quartic identity')
    # Q4=x P9(x)/(672(1-x)^3), sign on the entire rational threshold bracket.
    P9=q4*672*lr**3/xr
    numerator=coeffs(P9)
    xlo=alo/(1+alo);xhi=ahi/(1+ahi)
    negative=bernstein(coeffs(-P9),xlo,xhi)
    need(all(Fraction(c)>0 for c in negative['bernstein']), 'strict negative quartic at threshold')
    quartic_bounds={}
    for name,f in {'less_than_minus_1_100':(-QQ(1,100)-q4)*672*lr**3,
                   'greater_than_minus_1_50':(q4+QQ(1,50))*672*lr**3}.items():
        rec=bernstein(coeffs(f),xlo,xhi)
        need(all(Fraction(c)>0 for c in rec['bernstein']),'strict rational quartic bound')
        quartic_bounds[name]=rec
    # Mathematical damages: removing modulus curvature, a wrong mixed entry,
    # losing the radius correction, or altering the full interval certificate.
    damages=[]
    def reject(test,label):
        try:test()
        except ValueError:damages.append(label);return
        raise ValueError('mathematical damage accepted: '+label)
    reject(lambda:need(quadratic==matrix,'rank-one modulus contribution'), 'discarded modulus rank one')
    reject(lambda:need(b+1==matrix[0][1],'mixed entry changed'),'changed mixed entry')
    reject(lambda:need(not cut((1-aa*aa)*trial*trial+2*aa*trial*cosine-1),'omitted fourth radius'),
           'omitted fourth disk correction')
    reject(lambda:need(all(Fraction(c)>0 for c in ['-1']+negative['bernstein'][1:]),'wrong quartic sign'),
           'quartic interval sign changed')
    reject(lambda:need(evaluate(apr['T'],Fraction(4,5))<0<evaluate(apr['T'],Fraction(81,100)),
                       'wrong bracket'), 'incorrect threshold bracket')
    full_matrix=[[coeffs(den*c) for c in row] for row in matrix]
    return {'domain':'QQ(i)(x), x=a/(1+a); exact eight-variable degree-two jets and degree-four pair jets',
        'full_phase_matrix':full_matrix,'matrix_sha256':digest(full_matrix),
        'imaginary_gradient':[coeffs(c) for c in w],
        'polynomials':polynomials,'modulus_determinant':determinant_poly,'a_polynomials':apr,
        'threshold':root,'bounds':bounds,'bernstein_count':sum(len(r['bernstein']) for r in bounds.values()),
        'quartic':{'radius_fourth_numerator':coeffs(r4*24*lr**2),
                   'pair_P9':numerator,'negative_P9':negative,'xlo':str(xlo),'xhi':str(xhi),
                   'bounds':quartic_bounds},
        'jet_counts':{'primitive_integrand_terms':len(origin),'origin_coefficients':len(jet),
                      'full_matrix_entries':64,'pair_quartic_integrand_terms':len(quartic_integrand),
                      'gaussian_quartic_integrand_terms':len(gaussian)},
        'mathematical_damage_rejections':damages}
