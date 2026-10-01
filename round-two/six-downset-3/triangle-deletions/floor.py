"""Exact unbounded floor C>=P/4, plus the single-deletion cap sign."""
import bootstrap
from fractions import Fraction as F
from pathlib import Path
import json
from poly import R, mul, exact_divide
from model import model, formula
from signs import determinant, lower_sign
from exact import require, digest


def inverse(matrix):
    n=len(matrix)
    a=[[R(x) for x in row]+[R(int(i==j)) for j in range(n)] for i,row in enumerate(matrix)]
    for k in range(n):
        p=next((i for i in range(k,n) if a[i][k]!=0),None)
        require(p is not None,'singular symbolic Gram')
        a[k],a[p]=a[p],a[k]
        scale=a[k][k];a[k]=[x/scale for x in a[k]]
        for i in range(n):
            if i!=k and a[i][k]!=0:
                scale=a[i][k];a[i]=[x-scale*y for x,y in zip(a[i],a[k])]
    return [row[n:] for row in a]


def run(floor=F(1,4)):
    q=R((4,1));data=model(q,formula(q));signs=[]
    clear=2*q*(q-1)*(q-2)*(q-3)*(3*q+5)*(q+1)
    for sector in data:
        degree,levels,norms=sector['degree'],sector['levels'],sector['norms']
        g=sector['lower'];ks=sector['kernel'];size=len(levels)
        proj=[[R(norms[i]*int(i==j)) for j in range(size)] for i in range(size)]
        if ks:
            gram=[[sum(norms[k]*v[k]*w[k] for k in range(size)) for w in ks] for v in ks]
            inv=inverse(gram)
            for i in range(size):
                for j in range(size):
                    proj[i][j]-=norms[i]*norms[j]*sum(ks[a][i]*inv[a][b]*ks[b][j] for a in range(len(ks)) for b in range(len(ks)))
        shifted=[[g[i][j]-floor*proj[i][j] for j in range(size)] for i in range(size)]
        require(all(sum(shifted[i][j]*v[j] for j in range(size))==0 for i in range(size) for v in ks),'shifted kernel differs')
        anchors=[(1,0),(2,0)] if degree==(0,0) else [(1,0)] if degree==(1,0) else []
        keep=[i for i,t in enumerate(levels) if t not in anchors]
        scaled=[[exact_divide(mul(clear.n,shifted[i][j].n),mul(clear.d,shifted[i][j].d)) for j in keep] for i in keep]
        for k in range(1,len(keep)+1):
            p=determinant([row[:k] for row in scaled[:k]])
            lower_sign(p)
            signs.append({'sector':list(degree),'size':k,'coefficients':[str(v) for v in p]})
    return {'scope':'all q=4+u,u>=0','spectral_floor':str(floor),'common_denominator':'2q(q-1)(q-2)(q-3)(3q+5)(q+1)','sign_count':len(signs),'signs':signs,'signs_sha256':digest(signs)}


def cap_parameters(q, k):
    c = F(1, 2)
    n = (q*q+13*q+16)/2-k
    s, g = 3*q+4, n-2*(3*q+4)
    alpha = q*(q+1)/2+3*(q+1)/(3*q+5)
    h = 1/(3*q+5)
    chi = k*g*(n-c+c*h)**2-((k-1)*(n-c)+c*alpha)*(n-c)*(n-s-k)
    gamma = g*chi/(n*(n-c)**2*(n-s-k))
    return n, s, chi, gamma


def regenerate():
    result = run()
    q = R((4, 1))
    chi = cap_parameters(q, 1)[2]
    chi.coefficients_positive()
    result['single_deletion_cap_sign'] = chi.record()
    result['certificate_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    print(json.dumps(regenerate(), indent=2))
