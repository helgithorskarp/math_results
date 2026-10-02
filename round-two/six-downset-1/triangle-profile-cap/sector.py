"""Fixed-dimensional physical sectors for distinct-mark triangle facets.

Actual author six-downset-1, researcher. All-n complete-space and actual-empty
bridges are in PROOF.md. Exact arithmetic code is credited to the earlier
own engine; this is not an independently reviewed implementation.
"""
from fractions import Fraction as F
from exact import require,psd_rank

def reduced(q, k, fraction=F):
    f = fraction
    q, k = f(q), f(k)
    s, w, N, ell = q+3, q+2, 2*q+6*k, 3*k+1
    K2 = ell*q+2-6*k
    D2 = q*k/(3*(k-1))
    d = 3*(q-3*k-2)/(ell*q)
    a = -d/3
    c = (a-d)*q/s
    etaL = w-K2/ell**2-a*a*D2-2*s*c*c/3
    etaF = w-K2/ell**2-d*d*D2-2*s*c*c/(3*(k-1))
    r = -1-K2/ell**2-a*d*D2
    mu = (2*r+etaF)/3
    nu = k*mu/(k-1)
    full = etaF-mu
    anti = 2*(2*etaL-r-etaF)
    def zero(n):
        return [[f(0) for _ in range(n)] for _ in range(n)]
    def diagonal(values):
        M=zero(len(values))
        for i, value in enumerate(values):M[i][i]=value
        return M
    def update(M, vector, count):
        for i in range(len(vector)):
            for j in range(len(vector)):
                M[i][j] += count*vector[i]*vector[j]
    def cap(G, S):
        return [[(N-1)*G[i][j]-S[i][j] for j in range(len(G))] for i in range(len(G))]
    Ga = diagonal([2*s, anti])
    Sa = zero(2)
    update(Sa, [s,f(0)], 2)
    update(Sa, [-c*s,anti/2], 2)

    # Fixed vectors: gplus,h0,sum(A_i),sum(tS_i),sum(wF_i).
    Ge = diagonal([q-1,f(3),3*k*(q-k),6*k*s,k*full])
    Se = zero(5)
    Se[0][0]=q*q-1
    Se[0][1]=Se[1][0]=3*(q-1)
    Se[1][1]=f(9)
    Se[2][2]=6*Ge[2][2]
    update(Se,[f(0),f(1),q-k,s,f(0)],2*k)
    update(Se,[f(0),f(1),q-k,-2*s,f(0)],k)
    common=[-(q-1)/ell,-3*(k-1)/ell,-3*k*(q-k)/ell,f(0),f(0)]
    leaf=common[:]
    leaf[3]=c*s;leaf[4]=-full/2
    whole=common[:]
    whole[3]=-2*c*s;whole[4]=full
    update(Se,leaf,2*k)
    update(Se,whole,k)
    update(Se,common,1) # The ACTUAL empty seed vector -K/ell.

    # Zero-sum alpha with sum(alpha_i^2)=2:
    # A_alpha,tS_alpha,mean_alpha,wF_alpha.
    Go=diagonal([6*q,12*s,2*nu,2*full])
    So=zero(4)
    So[0][0]=6*Go[0][0]
    update(So,[q,s,f(0),f(0)],4)
    update(So,[q,-2*s,f(0),f(0)],2)
    update(So,[a*k*q/(k-1),c*s,nu,-full/2],4)
    update(So,[d*k*q/(k-1),2*c*s/(k-1),nu,full],2)
    return {'anti':(Ga,Sa,cap(Ga,Sa)), 'fixed':(Ge,Se,cap(Ge,Se)),
            'standard':(Go,So,cap(Go,So)),
            'residual':diagonal([mu,anti,full]),
            'parameters':{'q':q,'k':k,'s':s,'N':N,'ell':ell,'K2':K2,
                          'd':d,'a':a,'c':c,'etaL':etaL,'etaF':etaF,
                          'r':r,'mean_norm':mu,'anti_norm':anti,'full_norm':full}}
