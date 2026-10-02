"""Independent finite full-undeleted harmonic forms at actual endpoint orders.

Credited complete incidence formula8757. Reconstructed here without its code.
These finite checks replace reliance on infinite spectral-floor premises for
the new five positive fixtures; the infinite adaptive tail remains imported.
"""
from fractions import Fraction as F
from math import comb
from affine import table
from linear import need,psd,digest,mv

def choose(n,r):return comb(n,r)if 0<=r<=n else 0
def inverse(A):
    n=len(A);B=[[F(x)for x in r]+[F(i==j)for j in range(n)]for i,r in enumerate(A)]
    for j in range(n):
        p=next((i for i in range(j,n)if B[i][j]),None);need(p is not None,'kernel metric invertible')
        B[j],B[p]=B[p],B[j];pivot=B[j][j];B[j]=[x/pivot for x in B[j]]
        for i in range(n):
            if i==j:continue
            z=B[i][j];B[i]=[x-z*y for x,y in zip(B[i],B[j])]
    return [r[n:]for r in B]
def full_sectors(q,kap):
    need((q==4 or 19<=q<=23)and kap in [0,F(1,4096),F(1,1024)],'finite undeleted parameter controls')
    types=[(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)];Q=table(q,kap);s=3*q+4;records=[];dimension=0;nullity=0
    for j,l,copies in [(0,0,1),(1,0,2),(0,1,q-1),(1,1,2*(q-1)),(0,2,q*(q-3)//2)]:
        kept=[t for t in types if j<=t[0]<=3-j and l<=t[1]<=q-l]
        weights=[choose(3-2*j,a-j)*choose(q-2*l,b-l)for a,b in kept];need(all(w>0 for w in weights),'positive harmonic norms')
        G=[]
        for i,(a,b)in enumerate(kept):
            row=[]
            for m,(c,d)in enumerate(kept):
                number=choose(3-a-j,c-j)*choose(q-b-l,d-l)
                disjoint=Q.get(tuple(sorted(((a,b),(c,d)))),F(0))
                z=F(s*weights[i]*(i==m))+weights[i]*disjoint*((-1)**(j+l))*number
                if j==l==0:z-=weights[i]*weights[m]
                row.append(z)
            G.append(row)
        need(all(G[i][m]==G[m][i]for i in range(len(G))for m in range(len(G))),'full harmonic symmetry')
        kernels=[]
        if j==l==0:
            kernels=[[F(a)for a,b in kept],[F(a>=2)for a,b in kept]]
            if kap==0:kernels.append([F(1)]*len(kept))
        elif j==1 and l==0:kernels=[[F(1)]*len(kept)]
        need(all(not any(mv(G,k))for k in kernels),'all actual harmonic family kernels')
        n=len(G);P=[[F(weights[i]*(i==m))for m in range(n)]for i in range(n)]
        if kernels:
            metric=[[sum(weights[i]*x[i]*y[i]for i in range(n))for y in kernels]for x in kernels];inv=inverse(metric)
            for i in range(n):
                for m in range(n):P[i][m]-=weights[i]*weights[m]*sum(kernels[a][i]*inv[a][b]*kernels[b][m]for a in range(len(kernels))for b in range(len(kernels)))
        lower=[[G[i][m]-kap*P[i][m]/2 for m in range(n)]for i in range(n)]
        upper=[[2*s*weights[i]*(i==m)-G[i][m]for m in range(n)]for i in range(n)]
        rank=psd(G)['rank'];need(rank==n-len(kernels),'exact full harmonic nullity')
        # These bounds are nonstrict; equality at an endpoint is permitted.
        shifted_lower=psd(lower)['rank'];shifted_upper=psd(upper)['rank']
        dimension+=copies*n;nullity+=copies*len(kernels)
        records.append({'core_degree':j,'outside_degree':l,'copies':copies,'types':kept,'weights':weights,'lower_rank':rank,'lower_floor':kap/2,'upper_bound':2*s,'shifted_lower_rank':shifted_lower,'shifted_upper_rank':shifted_upper,'Gram_sha256':digest(G),'shifted_lower_sha256':digest(lower),'shifted_upper_sha256':digest(upper)})
    need(dimension==(q*q+13*q+16)//2-1 and nullity==(5 if kap==0 else 4),'full undeleted dimension and nullity census')
    return {'q':q,'kappa':kap,'dimension':dimension,'nullity':nullity,'records':records,'trust':'finite exact harmonic PSD/rank/floors plus ordinary complete layer decomposition; no inference of all-q signs from these points'}
