"""Separate closed forms; no producer, sector or polynomial-field import.

Anti/contrast forms are expanded explicitly. The aggregate is reconstructed
as one five-dimensional block, two trace blocks and its exact mean mode.
Only conservative degree propagation is reused from credited source2252.
"""
from fractions import Fraction as F
from degree_bounds import Degree,require,add_degree,max_degree


def zeros(n):return [[F(0) for _ in range(n)] for _ in range(n)]


def forms(q,h):
    if type(q) is int:q=F(q)
    if type(h) is int:h=F(h)
    l=h-1;s=q+3*h;D=3*h;N=2*q+12*h-6;ell=6*h-2
    c0=q/(2*(3*h-1))-1/(3*h-1)**2
    group=[]
    for k,r in ((h,(ell-q+1)/ell),(l,(ell-q-2)/ell)):
        c=9*r/(2*s);a=3*k*r/(2*s*(k-1))
        alpha=2*s-27*(2*k-3)*r*r/(s*(k-1))
        beta=2*s/3-3*(k+3)*r*r/(s*(k-1))
        mu=(s-3)/3-c0-9*r*r/(2*s*(k-1))
        group.append(dict(k=k,c=c,a=a,alpha=alpha,beta=beta,mu=mu))
    mx,my=group[0]['mu'],group[1]['mu']
    tau=mx*my/(h*mx+l*my)
    group[0]['nu']=(h*mx-l*tau)/(h-1)
    group[1]['nu']=(l*my-h*tau)/(l-1)
    out={}
    for name,g in zip(('x','y'),group):
        for key in ('alpha','beta','mu','nu'):out[name+'-'+key]=[[g[key]]]
    out['tau']=[[tau]]
    for name,g in zip(('x','y'),group):
        k,c,a,alpha,beta,nu=[g[z] for z in ('k','c','a','alpha','beta','nu')]
        out['anti-'+name]=[[N-1-s*(1+c*c),c*alpha/2],
                          [s*c,N-1-alpha/2]]
        zz=(k-3)/(k-1)
        out['standard-'+name]=[
            [N-1-s*(1+2*a*a),-2*s*a*c*zz,3*a*beta,0],
            [-s*a*c*zz/9,N-1-s-s*c*c/3-2*s*c*c/(3*(k-1)**2),
             beta*c*zz/6,-nu*c*k/(3*(k-1))],
            [s*a,s*c*zz,N-1-3*beta/2,0],
            [0,-2*s*c*k/(k-1),0,N-1-3*nu]]
    G=[4*(q-1),4*D,2*D*(q-2),2*q*D,s/(3*h*l)]
    S=zeros(5)
    S[0][0]=4*(q*q-1);S[0][1]=S[1][0]=-4*D*(q-1)
    S[1][1]=4*D*D;S[2][2]=4*D*D*(q-2);S[3][3]=4*D*D*q
    jx=[0,-2,q-2,q,0];jy=[0,-2,q-2,-q,s/(3*h*l)]
    zimage=[-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q,-s/h]
    for i in range(5):
        for j in range(5):
            S[i][j]+=3*h*jx[i]*jx[j]+3*l*jy[i]*jy[j]+zimage[i]*zimage[j]/ell
    A=zeros(10)
    for i in range(5):
        for j in range(5):A[i][j]=(N-1)*F(i==j)-S[i][j]/G[i]
    for g,(i,j) in zip(group,((5,7),(6,8))):
        c,beta=g['c'],g['beta']
        A[i][i]=N-1-s*(1+c*c);A[i][j]=beta*c/2
        A[j][i]=3*s*c;A[j][j]=N-1-3*beta/2
    A[9][9]=N-1-3*(h+l)*tau
    out['aggregate']=A
    out['untouched-even']=[[12*h-7]]
    out['untouched-odd']=[[2*q+6*h-7]]
    return out
