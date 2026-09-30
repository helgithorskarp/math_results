"""Optional exact discovery algebra, rechecked without CAS by threefold_identities.

SymPy1.14.0 over Q(v), characteristic zero. Select the remaining affine
parameter by setting the constant triple block to one. Denominators are
interpreted only for v>=13. This calculation alone is not an H proof.
Redirect stdout to threefold_symbolic.json to reproduce the compact output.
Author: six-downset-2, researcher.
"""
import json
import sympy as S

assert S.__version__ == '1.14.0'
v = S.symbols('v', integer=True, positive=True)
a, w, c, h, d, t = S.symbols('a w c h d t')
r, m, b, s, N = 3*(v-1)/2, v*(v-1)/2, v*(v-1)/2, (5*v-3)/2, v*v+1
equations = [h+(v-4)*d+(r-9)*t-s,
             1+s+(v-3)*h-6*t+(v-3)*(v-4)*d/2+(b-3*r+8)*t-N,
             w+(v-3)*c+(r-6)*d-s,
             1+s+(v-2)*w-3*d+(v-2)*(v-3)*c/2+(b-2*r+3)*d-N,
             a+(v-2)*w-3*d+(r-3)*h-9*t-s]
affine = S.solve(equations, [a, w, c, h, d], dict=True)
assert len(affine) == 1
constant_triple = s+8*t-3*r*t+(t-1)*b
selected = S.factor(S.solve(constant_triple-1, t)[0])
solution = {key: S.factor(value.subs(t, selected)) for key, value in affine[0].items()}
solution[t] = selected
equations.append(1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-2*r*t-N)
assert all(S.cancel(eq.subs(solution)) == 0 for eq in equations)
cc, dd, tt = solution[c], solution[d], solution[t]
constant_pair = S.factor(s+cc-2*cc*(v-1)+(cc-1)*m)
constant_cross = S.factor(3*dd-2*dd*r+(dd-1)*b)
assert constant_pair == 4 and constant_cross == -2
alpha1, alpha2 = S.factor(s-cc*(v-3)), S.factor(s+cc)
beta = S.factor(tt-dd**2/alpha2)
mu = S.factor(s-tt-(r-3)*(tt*(v-6)/(v-2)+dd**2*(v-4)**2/((v-2)*alpha1)))
out = {'agent': 'six-downset-2', 'role': 'researcher', 'CAS': 'SymPy '+S.__version__,
       'domain': 'Q(v)', 'weights': {str(k): str(value) for k, value in solution.items()},
       'constant_K': [[4, -2], [-2, 1]],
       'pair_eigenvalues': {'point_standard': str(alpha1), 'point_kernel': str(alpha2)},
       'Schur_R_coefficient': str(beta), 'Schur_lower_bound': str(mu),
       'Schur_margin_above_half': str(S.factor(mu-S.Rational(1,2))),
       'exceptional_denominators': 'v-2,v-3,v-4,v-5; pair Schur eigenvalues; positive atv>=13',
       'status': 'Exact discovery algebra; complete incidence/sign/cap/rank proof in UNIFORM_THREEFOLD_PROOF.md'}
print(json.dumps(out, indent=2, sort_keys=True))
