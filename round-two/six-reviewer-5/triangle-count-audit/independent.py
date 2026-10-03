"""Fresh written-formula reconstruction. No producer imports or data input."""
import argparse, hashlib, json
import sympy as S

q, h = S.symbols('q h')
Z = S.Integer(0)

def need(ok, why):
    if not ok:
        raise ValueError(why)

def tidy(x):
    return S.cancel(x)

def enc(x):
    a, b = S.fraction(tidy(x))
    def poly(p):
        return [[list(m), str(c)] for m, c in S.Poly(p, h, q).terms()]
    return {'num': poly(a), 'den': poly(b)}

def vector(n, pairs):
    a = S.zeros(n, 1)
    for i, x in pairs.items():
        a[i] = x
    return a

def dyad(a):
    return a*a.T

def forms(damage=None):
    s = q+3*h; d = 3*h; ell = 3*h+4; H = 2*q+6*h+5
    rho = (q-1)/(s-4)
    e2 = q/(3*h)+rho**2*(s-3)/3
    k2 = ell*q+6*h-16
    c0 = k2/ell**2
    F = (q-8)/(ell*rho*(s-3)); A = F/(2*h)
    cL = -4*(q-8)/(ell*s)
    b = 3*h*(q-ell-1)/(ell*s*(h-1)); a = -b/2
    cH = -9*(q-ell-1)/(2*ell*s)+A*q/(h*s)
    b2 = s*(h-1)/(3*h)
    eHL = s-1-c0-A**2*e2-a**2*b2-2*s*cH**2/3
    eHF = s-1-c0-b**2*b2-2*s*cH**2/(3*(h-1))-2*s*cL**2/(3*h**2)
    eLL = s-1-c0-F**2*e2-2*s*cL**2/3
    eLF = s-1-c0-9*F**2*e2
    rH = -1-c0-a*b*b2; rL = -1-c0+3*F**2*e2
    muH = (2*rH+eHF)/3; muL = (2*rL+eLF)/3
    alphaH = 2*(2*eHL-rH-eHF); betaH = eHF-muH
    alphaL = 2*(2*eLL-rL-eLF); betaL = eLF-muL
    nu = (h*muH-muL/h)/(h-1)
    if damage == 'light-mean':
        muL += 1
    scalars = [alphaH, betaH, alphaL, betaL, nu, muL]
    # Fixed projections of each literal marked/private row, summed as dyads.
    gf = S.diag(q-1, d, d*(q-1), d*(q-1), 6*h*s,
                s*(h-1)/(3*h), 6*s, h*betaH, betaL, muL)
    gf[2,3] = gf[3,2] = -d
    hx = vector(10,{1:1/d,2:1/d}); hy = vector(10,{1:1/d,3:1/d})
    Y = vector(10,{5:1})
    K = vector(10,{0:1,1:1/h,2:1,3:1/h,5:3})
    E = hx-rho*(hy+Y)
    need(tidy((E.T*gf*E)[0]-e2)==0, 'whole E norm')
    need(tidy((K.T*gf*K)[0]-k2)==0, 'whole K norm')
    need(tidy((K.T*gf*E)[0])==0, 'K/E orthogonality')
    old = S.zeros(10)
    old[0,0]=q*q-1; old[0,1]=old[1,0]=d*(q-1); old[1,1]=d*d
    for i in (2,3):
        for j in (2,3):
            old[i,j]=2*d*gf[i,j]
    heavy_marked = [hx+vector(10,{4:c/h}) for c in (S.Rational(1,6),S.Rational(1,6),-S.Rational(1,3))]
    light_marked = [hy+Y+vector(10,{6:c}) for c in (S.Rational(1,6),S.Rational(1,6),-S.Rational(1,3))]
    heavy_leaf = -K/ell+A*E+vector(10,{4:cH/(6*h),9:1/h,7:-1/(2*h)})
    heavy_full = -K/ell+vector(10,{4:-cH/(3*h),6:-cL/(3*h),9:1/h,7:1/h})
    light_leaf = -K/ell+F*E+vector(10,{6:cL/6,9:-1,8:-S.Rational(1,2)})
    light_full = -K/ell-3*F*E+vector(10,{9:-1,8:1})
    cov = h*sum((dyad(v) for v in heavy_marked), S.zeros(10))
    cov += sum((dyad(v) for v in light_marked), S.zeros(10))
    cov += h*(2*dyad(heavy_leaf)+dyad(heavy_full))+2*dyad(light_leaf)+dyad(light_full)
    if damage != 'empty-omission':
        cov += dyad(-K/ell)
    fixed = H*gf-old-gf*cov*gf
    # Heavy standard contrasts have norm squared 2; sum_i a_i^2/4=1/2.
    gs = S.diag(2*s/3,12*s,2*nu,2*betaH)
    stdrows = [vector(4,{0:1,1:c}) for c in (S.Rational(1,6),S.Rational(1,6),-S.Rational(1,3))]
    sl = vector(4,{0:a,1:cH/6,2:1,3:-S.Rational(1,2)})
    sf = vector(4,{0:b,1:cH/(3*(h-1)),2:1,3:1})
    scov = (sum((dyad(v) for v in stdrows),S.zeros(4))+2*dyad(sl)+dyad(sf))/2
    standard = H*gs-gs*scov*gs
    if damage == 'standard-metric':
        standard[0,0] += 1
    anti = []
    for c, alpha in ((cH,alphaH),(cL,alphaL)):
        ga = S.diag(2*s,alpha)
        va=vector(2,{0:S.Rational(1,2)})
        vb=vector(2,{0:-c/2,1:S.Rational(1,2)})
        anti.append(H*ga-ga*(2*dyad(va)+2*dyad(vb))*ga)
    # Written projections must sum to the actual empty complement.
    total = h*sum(heavy_marked,S.zeros(10,1))+sum(light_marked,S.zeros(10,1))
    total += h*(2*heavy_leaf+heavy_full)+2*light_leaf+light_full
    total += vector(10,{0:1,1:-1}) # old G = gp-h0
    need(all(tidy(x)==0 for x in total-K/ell), 'whole row-sum bridge')
    if damage == 'light-mean':
        need(tidy((light_full.T*gf*light_full)[0] + alphaL*Z - (s-1))==0, 'light whole norm')
    return dict(scalars=[enc(x) for x in scalars],
                sectors={name:[[enc(x) for x in row] for row in matrix.tolist()]
                         for name,matrix in [('anti-heavy',anti[0]),('anti-light',anti[1]),('standard',standard),('fixed',fixed)]},
                gram={name:[[enc(x) for x in row] for row in matrix.tolist()] for name,matrix in [('fixed',gf),('standard',gs)]},
                identities=['E norm','K norm','K/E orthogonality','whole row sum'],
                scalar_order=['alphaH','betaH','alphaL','betaL','nu','muL'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--damage');opts=ap.parse_args()
    out=forms(opts.damage)
    print(json.dumps(out,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    main()
