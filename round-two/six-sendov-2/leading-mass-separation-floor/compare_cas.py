"""Whole same-author alternate SymPy corroboration, not independent review."""
from pathlib import Path
import json
import time
import resource
import sympy as S

started = time.monotonic()
fixture = json.loads(Path(__file__).with_name('expected.json').read_text())
variables = S.symbols('B E F G J p0 p1 p2 p3 p4 p5 C')
B,E,F,G,J,p0,p1,p2,p3,p4,p5,C = variables
z,theta = S.symbols('z theta')
ring = S.QQ.poly_ring(*variables)
h = S.Poly(z**7-S.Rational(3,8)*z**5+B*z**4+E*z**3+F*z**2+G*z+J,z,domain=ring)
primitive = S.Poly(sum(8*h.nth(k)*z**(k+1)/S.Integer(k+1) for k in range(8)),z,domain=ring)
x = -S.Rational(3,8)*theta**2+B*theta**3+E*theta**4+F*theta**5+G*theta**6+J*theta**7
log_series = S.Poly(-x+x*x/2-x*x*x/3,theta,domain=ring)
tau = [S.Integer(7)]+[k*log_series.nth(k) for k in range(1,7)]
checks = {}

def encode_expr(expression):
    return sorted([[list(key),str(coefficient)] for key,coefficient in
                   S.Poly(S.expand(expression),*variables,domain=S.QQ).terms() if coefficient])

def encode_list(polys):
    return [encode_expr(poly) for poly in polys]

def same(name,left,right):
    if left != right:
        raise ValueError('ENTIRE alternate '+name)
    checks[name] = True

def seq(poly, length=None):
    if length is None:
        length = max(1,poly.degree()+1)
    return [poly.nth(k) for k in range(length)]

def T(poly):
    normal = poly.rem(h)
    result = sum(normal.nth(k)*(sum(tau[j]*z**(k-1-j) for j in range(k))-k*z**(k-1))
                 for k in range(1,7))
    return S.Poly(result,z,domain=ring)

def maps(mass):
    Q = (8*primitive+mass*h.diff()).quo(h)
    O = mass*h.diff((z,2))+(mass.diff()-Q)*h.diff()+(64-Q.diff())*h
    p_squared = (mass*mass).rem(h)
    W = (mass*(Q-mass.diff())).rem(h)
    K = -16*mass-T(T(p_squared))*S.Rational(1,4)+T(W)*S.Rational(1,4)
    same('full higher ODE vanishing '+str(len(checks)), O.degree() <= 5, True)
    Phi = seq(O,6)+seq(K-S.Poly(4*C*z*z-4,z,domain=ring),7)
    return Q,O,p_squared,W,Phi

mass = S.Poly(sum(variables[5+k]*z**k for k in range(6)),z,domain=ring)
Q,O,ps,W,Phi = maps(mass)
branch = S.Poly(p0+S.Rational(4,5)*B*p4*z+(4-p4/4)*z*z+p4*z**4,z,domain=ring)
branch_Q,branch_O,branch_ps,branch_W,branch_Phi = maps(branch)
cube = S.Poly((z*z+p0/8)**3,z,domain=ring)
jet = S.Poly(B+E*z+F*z*z+G*z**3+J*z**4+p1*z**5+z**6,z,domain=ring)
known = {
    'Q':seq(Q), 'ODE':seq(O), 'Phi':Phi,
    'rho_p_squared':seq(ps), 'rho_p_Q_minus_pprime':seq(W),
    'Newton_tau_0_through_6':tau,
    'p5_difference_quotients':[S.cancel((q-q.subs(p5,0))/p5) for q in Phi],
    'projected_quartic_Phi':branch_Phi,
    'monic_resonance_cube':seq(cube),
    'resonance_inverse':seq(jet-cube,6),
}
for name,polys in known.items():
    same('whole map '+name,encode_list(polys),fixture['whole_maps'][name])

gradients = []
for polys in [Phi,branch_Phi]:
    norms = []
    for q in polys:
        norms.append(sum(sum(key)*abs(coefficient)
                         for key,coefficient in S.Poly(q,*variables,domain=S.QQ).terms()))
    gradients.append(norms)
same('all whole row gradient norms',[str(q) for q in gradients[0]],fixture['whole_row_gradient_norms'])
same('full input max gradient',str(max(gradients[0])),fixture['exact_scalar_constants']['whole_input_max_gradient_norm'])
same('full branch max gradient',str(max(gradients[1])),fixture['exact_scalar_constants']['whole_branch_max_gradient_norm'])
same('entire monic sextic cube ODE',(S.Poly(8*z*z+p0,z,domain=ring)*cube.diff()-48*S.Poly(z,z,domain=ring)*cube).as_expr(),S.Integer(0))

result = {
    'actual_agent':'six-sendov-2', 'role':'researcher', 'same_author_only':True,
    'independent_review':False, 'SymPy':S.__version__, 'complete':True,
    'all_whole_comparisons':checks,
    'entire_maps_compared':len(known),
    'every_coefficient_polynomial_compared':sum(len(q) for q in known.values()),
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}

print(json.dumps(result))
