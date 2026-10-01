"""Independent literal rational-formula replay of completion-defect Gram caps.

SymPy1.14.0, QQ polynomial arithmetic, no author arithmetic imports.
Checks the algebraic identities, positive h numerator, and all finite scalar
caps independently. Counts/PSD interpretation are outside this CAS layer.
six-downset-2, researcher. Portable cohort/literal checkers need no CAS.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sympy as S
assert S.__version__=='1.14.0'
v,l,x,y=S.symbols('v l x y')
r=l*(v-1)/2;s=v+r;u=l*(l-1)/2
m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b
D=l*(v*v-10*v+27)-6
Cnum=3*v*v-3*(l+3)*v+11*l
c=Cnum/(3*(v-2)*(v-3));d=(v*v-v-4)/((v-4)*(v-3))
t=(v-1)*(l*(v-3)-6)/D
w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*t
Hnum=3*l*l*v*v-12*l*l*v+9*l*l+l*v**3-12*l*v*v+11*l*v+36*l+12*v-24
alpha=(v-5)*r-(v-6)*u+3*l*l-l
beta=(v-6)*u+l*l*(v-4)+l
mu12=w*w*(v-2)+d*d*(r-u)-2*w*d*l
nu12=w*w+d*d*u+2*w*d*l
mu13=h*h*(r-l)-6*h*t*u+t*t*alpha
zcoef13=2*h*t+t*t*(v-6)
nu13=h*h*l+6*h*t*u+t*t*beta


def identities():
    HH_I=(v-4)*(r-u)+l*l-2*(r-u-l*l)+(r-l)
    HH_J=(v-4)*u+l*l*(v-2)-2*(l*l+u)+l
    hshift=(12*(l-1)*(6*l-5)+(10*l*(3*l-1)+12)*x
            +3*l*(l+3)*x*x+l*x**3)
    eqs={'D_shift':D.subs(v,7+x)-(l*(x*x+4*x+6)-6),
        'h_cleared':h*(v-3)*D-Hnum,
        'h_positive_shift':Hnum.subs(v,7+x)-hshift,
        'c_minimum_endpoint':Cnum.subs(l,v-2)-(8*v-22),
        'parent_HB_I':(r-u-l*l)-(r-l)+3*u,
        'parent_HB_J':l*l+u-l-3*u,
        'HH_I_coefficient':HH_I-alpha,'HH_J_coefficient':HH_J-beta,
        'A12_I_coefficient':mu12-(w*w*(v-2)+d*d*(r-u)-2*w*d*l),
        'A12_J_coefficient':nu12-(w*w+d*d*u+2*w*d*l),
        'A13_I_coefficient':mu13-(h*h*(r-l)+2*h*t*(-3*u)+t*t*HH_I),
        'A13_Z_coefficient':zcoef13-(2*h*t+t*t*(v-6)),
        'A13_J_coefficient':nu13-(h*h*l+2*h*t*3*u+t*t*HH_J),
        'A12_constant_eigenvalue':mu12+v*nu12-(w*(v-1)+d*r)*(2*w+d*l),
        'A13_constant_eigenvalue':mu13+v*nu13-t*t*3*l*(v-2-l)*r-3*r*(h+t*(l-1))**2,
        'constant_gap':s-(l*(v+7)/6+1)-(v-1+l*(v-5)/3),
        'density_gap':N-2*s-(v-1)*((v-2)/2+l*(v-6)/6)}
    for name,z in eqs.items():
        assert S.Poly(S.expand(S.fraction(S.together(z))[0]),v,l,x,y,domain=S.QQ).is_zero,name
    return list(eqs)


def h_positive_certificate():
    z=S.Poly(S.expand(Hnum.subs({v:7+x,l:2+y})),x,y,domain=S.QQ)
    table=[[i,j,str(a)]for(i,j),a in sorted(z.terms())if a]
    assert all(S.Rational(a)>=0 for i,j,a in table)
    constant=z.coeff_monomial(1);assert constant>0
    return {'domain':'v=7+x,l=2+y,x,y>=0','constant':str(constant),
        'term_count':len(table),
        'coefficient_sha256':sha256(json.dumps(table,separators=(',',':')).encode()).hexdigest()}


def exact_specialize(z,lam):
    out=S.cancel(z.subs({v:13,l:lam}));assert out.is_Rational
    return out


def scalar_record(lam):
    gamma=S.Integer(28)
    rho=[exact_specialize(mu12+d*d*gamma,lam),
         exact_specialize(mu13+zcoef13*gamma,lam),
         exact_specialize(d*d*(v-4)**2*(2*v-6)/4,lam)]
    roots=[]
    for q in rho:
        z=S.Integer(1)
        while z*z<=q:z+=1
        assert z*z>q>=0;roots.append(z)
    diagonal=[exact_specialize(s+l/3+t*gamma,lam),
              exact_specialize(s+c,lam),exact_specialize(s+t*(v-5),lam)]
    a12,a13,a23=roots
    rows=[diagonal[0]+a12+a13,diagonal[1]+a12+a23,diagonal[2]+a13+a23]
    bound=max(rows);delta=exact_specialize(N,lam)-bound
    g=S.Rational(330,13);assert delta>g
    out={'gamma':gamma,'mu12':exact_specialize(mu12,lam),'nu12':exact_specialize(nu12,lam),
         'alphaH':exact_specialize(alpha,lam),'betaH':exact_specialize(beta,lam),
         'mu13':exact_specialize(mu13,lam),'zcoef13':exact_specialize(zcoef13,lam),
         'nu13':exact_specialize(nu13,lam),'rho':rho,'crosses':roots,
         'root_square_margins':[z*z-q for z,q in zip(roots,rho)],
         'diagonal':diagonal,'rows':rows,'B':bound,'delta':delta,'g':g,
         'delta_minus_g':delta-g,'half_gap_margin':(delta-g)/2}
    return {key:[str(z)for z in a]if isinstance(a,list)else str(a)for key,a in out.items()}


def run():
    names=identities()
    return {'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0 QQ',
        'zero_identities':len(names),'identity_names':names,
        'h_positive_numerator':h_positive_certificate(),
        'cyclic13_common_gamma_scalars':{str(lam):scalar_record(lam)for lam in (4,5,6)},
        'trust_boundary':'Independent algebra only; full incidence/mode and cohort coverage proofs in DEFECT_GRAM_CAP.md. Parent HB identity is credited, not new.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('defect_gram_symbolic.json')
    if args.check:assert out==json.loads(path.read_text()),'symbolic expected output mismatch'
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
