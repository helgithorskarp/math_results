"""Whole-domain exact coefficient certificate for the independent lower derivative."""
import json
from pathlib import Path
from sympy import Poly, cancel, symbols, QQ, factor
import original_field as O
P=Path(__file__).resolve().parent
q,k,x,u=symbols('q k x u')
data=json.loads((P/'lower-sectors.json').read_text())

def read(value):
    from sympy import sympify
    return cancel(sympify(value,locals={'q':q}))

nu=read(data['nu']['zero']); nd=read(data['nu']['right_derivative'])
tau=read(data['tau']['zero']); td=read(data['tau']['right_derivative'])
F=cancel(2*nd/nu**2+td/tau**2)
O.require(F==read(data['F']),'entire independently derived F normalization')
a=cancel(q*k*nu*tau/((q-k)*tau+k*nu))
b=2*(3*q+4)*(3*q*q+3*q-2)/(6*q*q+5*q-2)
cert={}
def sign(name,expr,subs,vars,positive=True):
    poly=Poly(expr.subs(subs, simultaneous=True),*vars,domain=QQ)
    O.require(all(c>=0 for c in poly.coeffs()),name+' all shifted coefficients nonnegative')
    O.require(poly.TC()>0 if positive else poly.TC()>=0,name+' strict constant')
    cert[name]={'variables':[str(v) for v in vars], 'coefficients':[[list(e),str(c)] for e,c in poly.terms()],
                'strict_constant':str(poly.TC()),'total_degree':poly.total_degree()}

for name,expr,sgn in [('nu',nu,1),('tau',tau,1),('nu_derivative',nd,-1),('tau_derivative',td,1)]:
    n,d=expr.as_numer_denom()
    sign(name+'_numerator',sgn*n,{q:4+x},[x])
    sign(name+'_denominator',d,{q:4+x},[x])
n,d=F.as_numer_denom()
sign('F_denominator',d,{q:21+x},[x])
sign('F_strict_bound',-2*q**5*n-d,{q:21+x},[x])
n,d=a.as_numer_denom()
quadrant={k:7+x,q:3*(7+x)+u}
sign('a_denominator',d,quadrant,[x,u])
sign('a_gt_q',n-q*d,quadrant,[x,u])
n2,d2=cancel(b/2-a).as_numer_denom()
sign('b_half_minus_a_denominator',d2,quadrant,[x,u])
sign('b_half_minus_a',n2,quadrant,[x,u])
record={'method':'definition-level full original sectors plus canceled rational field; exact shifted coefficient proof',
        'nu0':str(nu),'nu_prime0':str(nd),'tau0':str(tau),'tau_prime0':str(td),'F':str(F),'a0':str(a),
        'certificates':cert,'scope':'q>=4 derivative signs; q>=21 F<-1/(2q^5); integer k>=7,q>=3k gives a>q and a0_prime<-1/(2q^4)',
        'trust':'original zero separation credited9980; exact symbolic computation and ordinary singular Schur bridge unformalized'}
(P/'lower-signs.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'all independent lower signs passed','signs':len(cert),'coefficients':sum(len(c['coefficients']) for c in cert.values()),
                  'degrees_F':[Poly(F.as_numer_denom()[0],q).degree(),Poly(F.as_numer_denom()[1],q).degree()],
                  'a0':str(a),'F_factored':str(factor(F))},indent=2))
