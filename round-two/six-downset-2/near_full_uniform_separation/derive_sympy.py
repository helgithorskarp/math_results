"""Optional independent CAS derivation, SymPy1.14.0, characteristic0 Q(n,x,T).

No solver, inequality inference, interpolation or reconstruction. The portable
checker verifies all cleared coefficient identities without this dependency.
"""
import json
import sympy as S
from verify import symbolic

n,x,T = S.symbols('n x T')
c,eta,k = 3*n*n/S.Integer(8),2+6/n**2,2+3/n
p = (n*n-x)/4
D,E = n*c*c+p*(n-4*c),c*c-n*c+p
X = (eta*p*x+(12*p/n**2+2*n)*E)/D
H = 2*((n-2)*c+n-2*p)-6*E/n**2
F = S.factor(S.cancel((n-1)*(X*X+p*x*H*H/D**2)-2*(n-2)*x*H/D-2*k*X+k*k))
A,B = n*n*(3*n-4)**2,8*(3*n-2)
numerator = S.Poly(S.cancel(((n-2)*k*k-F)*n**4*(A+B*x)),x)
if numerator.degree() != 2 or numerator.nth(0) != 0:
    raise ValueError('Unexpected CAS numerator')
a1,a2 = numerator.nth(1),numerator.nth(2)
mu = [S.Integer(1),n,3*n*n-2*n,15*n**3-30*n*n+16*n]
bulk = [2*T*M-2*n**(2*j)-2*n*(n-2)**(2*j)-n*(n-1)*(n-4)**(2*j) for j,M in enumerate(mu)]
K0 = n*(-T*n+2*T+5*n*n-9*n+3)
K1 = 2*(n-2)*(2*T*n-4*T+2*n**3-9*n*n+7*n+4)
low = eta*eta*K0+K1-2*k*n*(2*n-1)*eta+k*k*n*n
upper = S.cancel(low+(n-2)*k*k*bulk[0]-(a1*bulk[1]+a2*bulk[2])/(n**4*A)+B*(a1*bulk[2]+a2*bulk[3])/(n**4*A*A))
denom = n**7*(3*n-4)**4
P = S.Poly(S.cancel(-S.diff(upper,T)*denom/2),n)
Q = S.Poly(S.cancel(upper.subs(T,0)*denom),n)
observed = symbolic()
if list(map(int,reversed(P.all_coeffs()))) != observed['P'] or list(map(int,reversed(Q.all_coeffs()))) != observed['Q']:
    raise ValueError('CAS differs from portable exact arithmetic')
print(json.dumps({'sympy':S.__version__,'domain':'Characteristic0 Q(n,x,T)',
                  'F':str(F),'a1':str(S.factor(a1)),'a2':str(S.factor(a2)),
                  'P_Q_match_portable_coefficients':True},sort_keys=True))
