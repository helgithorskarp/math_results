"""Optional discovery algebra, independently rechecked by twofold_identities.

Requires SymPy==1.14.0; exact domain Q(v), characteristic zero. All theorem
specializations use v>=13. v-2,v-3,v-4 and pair Schur eigenvalues are divided
out and are positive there. No CAS is needed for the proof verifier.
Run this script and redirect stdout to twofold_symbolic.json to reproduce it.
"""
import json
import sympy as S

assert S.__version__ == '1.14.0'
v = S.symbols('v', integer=True, positive=True)
a, w, c, h, d, t = S.symbols('a w c h d t')
s, N = 2*v-1, (5*v*v+v+6)/6
equations = [h+(v-4)*d+(v-7)*t-s,
             1+s+(v-3)*h-3*t+(v-3)*(v-4)*d/2+(v-4)*(v-6)*t/3-N,
             w+(v-3)*c+(v-5)*d-s,
             1+s+(v-2)*w-2*d+(v-2)*(v-3)*c/2+(v-3)*(v-4)*d/3-N,
             a+(v-2)*w-2*d+(v-3)*h-3*t-s]
solution = S.solve(equations, [a, w, c, h, d], dict=True)[0]
solution = {k: S.factor(value.subs(t, (v-1)/(v-4))) for k, value in solution.items()}
solution[t] = (v-1)/(v-4)
equations.append(1+s+(v-1)*a+(v-1)*(v-2)*w/2-(v-1)*d+
                 (v-1)*(v-3)*h/3-(v-1)*t-N)
assert all(S.cancel(eq.subs(solution)) == 0 for eq in equations)
cc, dd, tt = solution[c], solution[d], solution[t]
alpha0 = S.factor(s+cc-2*(v-1)*cc+(cc-1)*v*(v-1)/2)
alpha1, alpha2 = S.factor(s-cc*(v-3)), S.factor(s+cc)
beta = S.factor(tt-dd**2/alpha2)
mu = S.factor(s-tt-(v-3)/(v-2)*(tt*(v-6)+dd**2*(v-4)**2/alpha1))
out = {'CAS': 'SymPy '+S.__version__, 'domain': 'Q(v)',
       'weights': {str(k): str(value) for k, value in solution.items()},
       'pair_eigenvalues': {'constant': str(alpha0), 'point_standard': str(alpha1),
                            'point_kernel': str(alpha2)},
       'Schur_R_coefficient': str(beta), 'Schur_lower_bound': str(mu),
       'exceptional_denominators': 'v-2,v-3,v-4; pair Schur eigenvalues; positive for v>=13',
       'status': 'Exact algebra only; incidence, positivity and cap interpreted in the written proof'}
print(json.dumps(out, indent=2, sort_keys=True))
