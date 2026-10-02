"""Rational two-triangle/pendant model and sufficient exact cap forms.

This specializes the saved mixed projection construction to r=2. Numeric
values use Fraction; symbolic certificates supply an exact fraction layer.
The complete original-space implications are ordinary mathematics in PROOF.md.
"""
from fractions import Fraction as F


def parameters(q, l, fraction=F, upper_bounds=False):
    if fraction is F:
        if not (type(l) is int and l >= 2 and q >= 4*l):
            raise ValueError('two triangles/l pendants continuous domain')
    q = fraction(q)
    l = fraction(l)
    r = fraction(2)
    s = q+3
    w = q+2
    m = l+6
    ell = l+7
    N = 2*q+12+2*l
    t = l+1
    rho = (q-1)/(q+1)
    d = 3*(q-ell-1)/(ell*q)
    g = (q-ell+1)/(ell*w)
    D = d
    Fp = -g/rho
    A = (-D-l*Fp/2)/2
    a = -d/3
    ast = 2*a-A
    dst = d
    c = (a-d)*q/s
    E2 = q/6+rho*rho*w/l
    Di2 = q/6
    Lj2 = w*(l-1)/l
    K2 = ell*q-10
    common = K2/(ell*ell)
    etaL = w-common-A*A*E2-ast*ast*Di2-2*s*c*c/3
    etaF = w-common-D*D*E2-d*d*Di2-2*s*c*c/(3*t*t)
    etaP = w-common-Fp*Fp*E2-g*g*Lj2-4*s*c*c/(3*t*t)
    pair = -1-common-A*D*E2-ast*d*Di2
    mu = (2*pair+etaF)/3
    alpha = 2*(2*etaL-pair-etaF)
    beta = etaF-mu
    if upper_bounds:
        C = q/(2*m)
        # From mu>q/6 and etaP>2q/3, the harmonic mean satisfies
        # Cactual>Cfloor. Keep this improvement in the triangle sector.
        Cfloor = l*q/(2*(2*l*l+6*l+9))
        # l*Cfloor/3 >= 2*q/87 for l>=2, because
        # 29*l^2-4*(2*l^2+6*l+9)=3*(7*l+6)*(l-2)>=0.
        nuT = 2*mu-fraction(2,87)*q
        nuL = l*etaP/(l-1)
    else:
        C = 1/(2*(l/(6*mu)+6/(l*etaP)+m/q))
        a_mean = (l*C-3*mu)/3
        b_mean = (6*C-etaP)/(l-1)
        nuT = mu-a_mean
        nuL = etaP-b_mean
    anti = [[(N-1)/(2*s)-(1+c*c)/2, c/2],
            [c/2, (N-1)/alpha-fraction(1,2)]]
    B = q/(6*(N-7))+s/(3*(N-1))
    pendant = [[fraction(1,2)-B, -g*B],
               [-g*B, fraction(1,2)-g*g*B-nuL/(2*(N-1))]]
    base = [6*q*(N-q-7), 12*s*(N-q-4),
            2*nuT*(N-1), 2*beta*(N-1)]
    updates = [[ast*q, c*s, nuT, -beta/2],
               [dst*q, 2*c*s/t, nuT, beta]]
    # Cancel the positive Gram norms before expanding rational products.
    # This is exactly U' diag(base)^(-1) U, not a numerical approximation.
    tq, ts, H = N-q-7, N-q-4, N-1
    LL = ast*ast*q/(6*tq)+c*c*s/(12*ts)+nuT/(2*H)+beta/(8*H)
    FF = dst*dst*q/(6*tq)+c*c*s/(3*t*t*ts)+nuT/(2*H)+beta/(2*H)
    LF = ast*dst*q/(6*tq)+c*c*s/(6*t*ts)+nuT/(2*H)-beta/(4*H)
    triangle = [[fraction(1,4)-LL, -LF], [-LF, fraction(1,2)-FF]]
    return locals()


def fixed(q, l, fraction=F, upper_bounds=False):
    p = parameters(q, l, fraction, upper_bounds=upper_bounds)
    q, l, r, s, m, ell, N, t, rho = [p[k] for k in
                                   ('q', 'l', 'r', 's', 'm', 'ell', 'N', 't', 'rho')]
    J = (N-q-2)*(N-4)-3*(q-1)
    D0, H0, A0 = N-7, N-1, N-q-2
    aa = (m-q*(l+r)/D0-2*r*s/H0)/(3*r*l)
    zz = 2*(6*r+2*l-7)/(D0*H0)
    bb = m-m*m*A0/(3*J)-((l+9*r)*q-m*m)/(3*D0)-2*l*s/(3*H0)
    cc = -m*(1-(6*r+2*l-1)/J)
    dd = 2*m+1-((q-1)*(N-10)+3*A0)/J
    arrow = [[aa, zz, fraction(0)], [zz, bb, cc], [fraction(0), cc, dd]]
    cross = [fraction(1,6)+rho/l, 1-rho, rho-1]
    tau_bound = m/(3*r*l)
    augmented = [row+[cross[i]] for i, row in enumerate(arrow)]
    augmented.append(cross+[tau_bound+fraction(1,6)+rho*rho/l])
    aZ = -l*p['Fp']/(3*r)
    bZ = p['c']*l/(9*r*t)
    dE = p['A']-p['D']
    bD = p['c']*(t+2*(r-1))/(6*r*t)
    T = 6*r*s/(N-1-s)
    ZZ = aZ*aZ*tau_bound+bZ*bZ*T+l*p['C']/(3*r*(N-1))
    DD = dE*dE*tau_bound+bD*bD*T+9*p['beta']/(4*r*(N-1))
    ZD = aZ*dE*tau_bound+bZ*bD*T
    final = [[l/(3*r*m)-ZZ, -ZD], [-ZD, fraction(3,2)/r-DD]]
    return augmented, final, p, locals()


def base_pairing(q, l, fraction=F):
    """Before the h,v,K updates: independent closed inverse pairing."""
    q, l = fraction(q), fraction(l)
    N, s, ell, rho = 2*q+12+2*l, q+3, l+7, (q-1)/(q+1)
    J = (N-q-2)*(N-4)-3*(q-1)
    h = [fraction(0), fraction(1,3), fraction(1,6), fraction(0), fraction(0)]
    v = [fraction(0), fraction(1,3), fraction(0), 1/(3*l), 1/l]
    K = [fraction(1), (l+3)/3, fraction(1), fraction(1,3), fraction(1)]
    E = [a-rho*b for a,b in zip(h,v)]
    def inner(x, y):
        return (((q-1)*(N-4)*x[0]*y[0]+3*(q-1)*(x[0]*y[1]+x[1]*y[0])
                 +3*(N-q-2)*x[1]*y[1])/J
                +3*(2*(q-2)*x[2]*y[2]-2*l*(x[2]*y[3]+x[3]*y[2])
                    +l*(q-l)*x[3]*y[3])/(N-7)
                +fraction(2,3)*l*s*x[4]*y[4]/(N-1))
    columns = [h,v,K]
    weights = [fraction(1,6), 1/l, ell]
    S3 = [[weights[i]*(i==j)-inner(a,b) for j,b in enumerate(columns)]
          for i,a in enumerate(columns)]
    b = [inner(a,E) for a in columns]
    EE = inner(E,E)
    return S3, b, EE, locals()
