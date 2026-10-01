"""Optional independent exact CAS derivation for the all-order extension.

SymPy1.14.0; no floating point. The portable verifier has no CAS dependency.
Author: six-downset-2, researcher.
"""
import json
import sympy as S
assert S.__version__=='1.14.0'
v,l=S.symbols('v l');x,y=S.symbols('x y')
m,b,r,u=v*(v-1)/2,l*v*(v-1)/6,l*(v-1)/2,l*(l-1)/2
s,N=v+r,1+v+m+b
D=l*(v*v-10*v+27)-6;E=3*l*v*v-3*l*v-16*l+6*v
a=-l/3;c=(v*v-(l+3)*v+11*l/3)/((v-2)*(v-3));d=(v*v-v-4)/((v-4)*(v-3))
t=(v-1)*(l*(v-3)-6)/D
alpha1=s-c*(v-3);alpha2=s+c
beta=t-d*d/alpha2
red=t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
mu=s-t-(r-l)*red
A=(r-l)*d*d*(v-4)**2/(v-2)
def cert(expr,v0=7,l0=2,weak=False,fixed_l=None):
    expr=S.cancel(expr)
    if fixed_l is not None:expr=S.cancel(expr.subs(l,fixed_l))
    num,den=S.fraction(expr)
    out={}
    for label,p in [('num',num),('den',den)]:
        p=S.Poly(S.expand(p.subs({v:v0+x,l:l0+y})),x,y)
        co=p.coeffs();constant=p.coeff_monomial(1)
        assert all(z>=0 for z in co),(label,str(expr),p.terms())
        assert constant>0 or(label=='num' and weak and constant==0)
        out[label]={'constant':str(constant),'terms':[[i,j,str(z)] for(i,j),z in sorted(p.terms()) if z]}
    return out
base={
 'D':D,'E':E,'alpha1_gt_lv_over_2':alpha1-l*v/2,
 'A_lt_2lv2':2*l*v*v-A,'t_gt_1':t-1,'d_positive':d,
 'c_legal_lower':(8*v-22)/(3*(v-2)*(v-3)),
 'beta_lower_positive':1-S.Rational(361,36)/(2*v-1)}
out={'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0','domain':'Q(v,l)','base':{k:cert(z) for k,z in base.items()},
 'weak':{'d_le_19_over_6':cert(S.Rational(19,6)-d,weak=True),'s_ge_2v_minus1':cert(s-(2*v-1),weak=True)},
 'l2_mu_gt_1':cert(mu-1,fixed_l=2),'l3plus_mu_gt_1_over_l':cert(mu-1/l,l0=3),'finite':[]}
tau=S.symbols('tau')
w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*tau
eqs=[h+(v-4)*d+(r-3*l)*tau-s,
 1+s+(v-3)*h-3*(l-1)*tau+(v-3)*(v-4)*d/2+(b-3*r+3*l-1)*tau-N,
 w+(v-3)*c+(r-2*l)*d-s,
 1+s+(v-2)*w-l*d+(v-2)*(v-3)*c/2+(b-2*r+l)*d-N,
 a+(v-2)*w-l*d+(r-l)*h-3*u*tau-s,
 1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-(l-1)*r*tau-N,
 s+c-2*c*(v-1)+(c-1)*m-4*l/3,
 l*d-2*d*r+(d-1)*b+2*l/3,
 s+(3*l-1)*tau-3*r*tau+(tau-1)*b-1]
for vv,ll,tt in [(5,3,6),(6,2,2),(6,4,5)]:
    sub={v:vv,l:ll,tau:tt}
    assert all(S.cancel(eq.subs(sub))==0 for eq in eqs),(vv,ll)
    aa1=S.cancel(alpha1.subs(sub));aa2=S.cancel(alpha2.subs(sub));dd=S.cancel(d.subs(sub))
    bb=tt-dd*dd/aa2
    rr=tt*S.Rational(vv-6,vv-2)+dd*dd*(vv-4)**2/((vv-2)*aa1)
    mm=vv+S.Rational(ll*(vv-1),2)-tt-(S.Rational(ll*(vv-1),2)-ll)*rr
    assert bb>0 and rr>0 and mm>S.Rational(1,ll)
    assert aa1>S.Rational(ll*vv,2) and S.cancel(A.subs(sub))<2*ll*vv*vv
    out['finite'].append({'v':vv,'l':ll,'t':tt,'alpha1':str(aa1),'alpha2':str(aa2),'beta':str(bb),'red':str(rr),'mu':str(mm),'A':str(S.cancel(A.subs(sub))),
        'weights':{name:str(S.cancel(z.subs(sub))) for name,z in {'a':a,'w':w,'c':c,'d':d,'h':h,'t':tau}.items()},'zero_identities':len(eqs)})
out['status']='Exact scalar certificates; ordinary PSD/rank interpretation in UNIFORM_LAMBDA_ALL_ORDERS.md.'
print(json.dumps(out,indent=2,sort_keys=True))
