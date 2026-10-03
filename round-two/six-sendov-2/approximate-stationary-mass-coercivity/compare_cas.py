"""Whole same-author alternate SymPy corroboration; no independent review."""
from pathlib import Path
import json
import time
import resource
import sympy as S

started=time.monotonic()
fixture=json.loads(Path(__file__).with_name('expected.json').read_text())
robust=fixture['robust_degree_drop_certificate']
variables=S.symbols('B E F G J p0 p1 p2 p3 p4 p5 p6 C')
B,E,F,G,J,p0,p1,p2,p3,p4,p5,p6,C=variables
z,theta=S.symbols('z theta')
ring=S.QQ.poly_ring(*variables)
h=S.Poly(z**7-S.Rational(3,8)*z**5+B*z**4+E*z**3+F*z**2+G*z+J,z,domain=ring)
primitive=S.Poly(sum(8*h.nth(k)*z**(k+1)/S.Integer(k+1) for k in range(8)),z,domain=ring)
x=-S.Rational(3,8)*theta**2+B*theta**3+E*theta**4+F*theta**5+G*theta**6+J*theta**7
minus_log=S.Poly(-x+x*x/2-x*x*x/3,theta,domain=ring)
tau=[S.Integer(7)]+[k*minus_log.nth(k) for k in range(1,7)]
checks={}

def encode_expr(expression):
    return sorted([[list(key),str(coefficient)] for key,coefficient in
                   S.Poly(S.expand(expression),*variables,domain=S.QQ).terms() if coefficient])

def encode_list(polys):
    return [encode_expr(q) for q in polys]

def same(name,left,right):
    if left!=right:raise ValueError('ENTIRE alternate '+name)
    checks[name]=True

def seq(poly,length=None):
    if length is None:length=max(1,poly.degree()+1)
    return [poly.nth(k) for k in range(length)]

def T(poly):
    normal=poly.rem(h)
    result=sum(normal.nth(k)*(sum(tau[j]*z**(k-1-j) for j in range(k))-k*z**(k-1))
               for k in range(1,7))
    return S.Poly(result,z,domain=ring)

def maps(mass):
    Q=(8*primitive+mass*h.diff()).quo(h)
    O=mass*h.diff((z,2))+(mass.diff()-Q)*h.diff()+(64-Q.diff())*h
    ps=(mass*mass).rem(h)
    W=(mass*(Q-mass.diff())).rem(h)
    K=-16*mass-T(T(ps))*S.Rational(1,4)+T(W)*S.Rational(1,4)
    same('whole higher ODE cancellation '+str(len(checks)),O.degree()<=5,True)
    Phi=seq(O,6)+seq(K-S.Poly(4*C*z*z-4,z,domain=ring),7)
    return Q,O,K,ps,W,Phi

mass=S.Poly(sum(variables[5+k]*z**k for k in range(7)),z,domain=ring)
Q,O,K,ps,W,Phi=maps(mass)
full={
    'Q':seq(Q),'ODE':seq(O),'K':seq(K),'Phi':Phi,
    'rho_p_squared':seq(ps),'rho_p_Q_minus_pprime':seq(W),
    'Newton_tau_0_through_6':tau,
    'p6_difference_quotients':[S.cancel((q-q.subs(p6,0))/p6) for q in Phi],
}
for name,polys in full.items():
    same('whole full p6 map '+name,encode_list(polys),fixture['whole_full_maps'][name])

matrix=[[S.Poly(z**(j+l),z,domain=ring).rem(h).nth(6) for l in range(7)] for j in range(7)]
inverse=[[h.nth(l+k+1) if l+k<=6 else S.Integer(0) for k in range(7)] for l in range(7)]
same('ENTIRE monic residue pairing matrix',[encode_list(q) for q in matrix],fixture['whole_residue_pairing_matrix'])
same('ENTIRE polynomial inverse',[encode_list(q) for q in inverse],fixture['whole_polynomial_pairing_inverse'])
same('all49 inverse composition coefficients',
     [[S.expand(sum(inverse[l][k]*matrix[k][j] for k in range(7))) for j in range(7)] for l in range(7)],
     [[S.Integer(l==j) for j in range(7)] for l in range(7)])

cropped=S.Poly(sum(variables[5+k]*z**k for k in range(6)),z,domain=ring)
cQ,cO,cK,cps,cW,cPhi=maps(cropped)
branch=S.Poly(p0+S.Rational(4,5)*B*p4*z+(4-p4/4)*z*z+p4*z**4,z,domain=ring)
bQ,bO,bK,bps,bW,bPhi=maps(branch)
cube=S.Poly((z*z+p0/8)**3,z,domain=ring)
jet=S.Poly(B+E*z+F*z*z+G*z**3+J*z**4+p1*z**5+z**6,z,domain=ring)
known={
    'Q':seq(cQ),'ODE':seq(cO),'Phi':cPhi,
    'rho_p_squared':seq(cps),'rho_p_Q_minus_pprime':seq(cW),
    'Newton_tau_0_through_6':tau,
    'p5_difference_quotients':[S.cancel((q-q.subs(p5,0))/p5) for q in cPhi],
    'projected_quartic_Phi':bPhi,'monic_resonance_cube':seq(cube),
    'resonance_inverse':seq(jet-cube,6),
}
for name,polys in known.items():
    same('whole robust map '+name,encode_list(polys),robust['whole_maps'][name])

def norms(polys):
    return [sum(sum(key)*abs(coefficient) for key,coefficient in
                S.Poly(q,*variables,domain=S.QQ).terms()) for q in polys]
same('all full p6 row gradient norms',[str(q) for q in norms(Phi)],fixture['whole_full_row_gradient_norms'])
same('all cropped row gradient norms',[str(q) for q in norms(cPhi)],robust['whole_row_gradient_norms'])
same('full projected quartic max gradient',str(max(norms(bPhi))),robust['exact_scalar_constants']['whole_branch_max_gradient_norm'])
same('full p6 top kernel',K.nth(6),-16*p6)
same('whole resonance cube ODE',
     (S.Poly(8*z*z+p0,z,domain=ring)*cube.diff()-48*S.Poly(z,z,domain=ring)*cube).as_expr(),S.Integer(0))

print(json.dumps({
    'actual_agent':'six-sendov-2','role':'researcher','same_author_only':True,
    'independent_review':False,'SymPy':S.__version__,'complete':True,
    'all_whole_comparisons':checks,
    'entire_maps_compared':len(full)+len(known)+2,
    'every_coefficient_polynomial_compared':sum(map(len,full.values()))+sum(map(len,known.values()))+98,
    'whole_inverse_composition_coefficients_compared':49,
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}))
