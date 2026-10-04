"""All literal coefficients from the written10314 equations, no producer code."""
from fractions import Fraction as Q
from math import comb
from field import E,C,I,need
from constants import constants
from series import *
def family(tau=0,n=10):
    v=constants();c=C;H=v['H'];rho=v['rho'];gamma=v['gamma']
    k=-Q(7,18)*(1+2*c);alpha=-E(Q(527,360))+Q(41,90)*c+Q(13,90)*c*c
    kappa=(k+rho)**2/2+Q(10,27)*alpha
    r=ps(T,1/(3*H));r2=pm(r,r);r3=pm(r2,r);r4=pm(r2,r2);mut=pm(MU,T)
    m2=E(Q(35,81))-Q(2086,81)*c+Q(616,27)*c*c
    b2=E(Q(14537,1512))-Q(3889,756)*c-Q(1661,756)*c*c
    b4=-Q(2,49)*(1+c)**2
    nu1=-E(Q(17983,972))-Q(25711,486)*c+Q(4564,81)*c*c
    nu3=E(Q(28,81))+Q(56,81)*c
    sigma1=-E(Q(1967,81))+Q(5479,432)*c-Q(5375,162)*c*c
    sigma3=-E(Q(55,189))+Q(11,63)*c+Q(88,189)*c*c
    nu4=-E(Q(2424695,13122))-Q(136157,4374)*c+Q(144046,6561)*c*c
    sigma4=-E(Q(536333191,1119744))-Q(805399537,559872)*c+Q(891296017,559872)*c*c
    s7=-Q(2,49)*(1+c)**2
    n9=-E(Q(35,81))-Q(29,27)*c-Q(34,81)*c*c
    s9=-E(Q(34849,42336))-Q(41053,21168)*c-Q(3265,2646)*c*c
    A=[{}]*(n+1);B=[{}]*(n+1);K=[{}]*(n+1);K[0]=pc(I)
    for S,base,mean in [(A,v['uz'],-Q(1,3)),(B,v['up'],Q(1))]:
        S[2]=pc(base);S[3]=ps(r,I*(mean));S[4]=pa(pc(v['w2']),ps(MU,mean))
        S[5]=ps(r,I*3*k*H/7);S[6]=pa(pc(v['m0']),ps(MU,v['m1']))
        S[7]=ps(r,I*nu1);S[8]=pa(pc(v['M0']),ps(MU,v['M1']),ps(r2,m2))
        S[9]=pa(ps(r,I*nu4),ps(r3,I*nu3),ps(mut,I*n9));S[10]=pc(tau)
    K[2]=pc(I*gamma);K[3]=ps(r,3*k+rho)
    K[4]=pa(pc(I*v['b0']),ps(MU,I*v['b1']),ps(r2,-I*4/(3*H)))
    K[5]=pa(ps(r,sigma1),ps(mut,s7))
    K[6]=pa(pc(I*v['beta0']),ps(MU,I*v['beta1']),ps(pp(MU,2),I*v['beta2']),ps(r2,I*b2))
    K[7]=pa(ps(r,sigma4),ps(r3,sigma3),ps(mut,s9));K[8]=ps(r4,I*b4)
    for name,S,sgn in [('A',A,1),('B',B,1),('K',K,-1)]:
        need([{e:(-1)**j*x for e,x in p.items()}for j,p in enumerate(S)]==ss(conj(S),sgn),'whole literal epsilon parity '+name)
        need([{e:(-1)**e[1]*x for e,x in p.items()}for p in S]==ss(conj(S),sgn),'whole literal skew reflection '+name)
        for j,p in enumerate(S):need(all(e[1]<=j for e in p),'all separate monomial grading '+name)
    return v|{'k':k,'kappa':kappa,'s7':s7,'n9':n9,'s9':s9},A,B,K
def primitive(tau=0,n=10):
    v,A,B,K=family(tau,n)
    return from_slots(v,A,B,K,n)
def from_slots(v,A,B,K,n=10):
    H=v['H'];d=sa(A,ss(B,-1),n=n)
    pair=sm(K,K,n);pair=[{},{}]+ss(pair,H/2)[:n-1]
    d2=sa(sm(d,d,n),ss(pair,-1),n=n)
    out=[[{}]*(n+1)for _ in range(10)];minusA=ss(A,-1)
    for power,factor in [(9,sj(1,n)),(8,ss(d,Q(9,4))),(7,ss(d2,Q(9,7)))]:
        for j in range(power+1):out[j]=sa(out[j],ss(sm(factor,sp(minusA,power-j,n),n),comb(power,j)),n=n)
    anchor=sj(1,n);anchor[2]=pc(-1);out[0]=sa(out[0],ss(value(out,anchor,n),-1),n=n)
    need(value(out,anchor,n)==[{}]*(n+1),'entire original marked-root anchor')
    f6=[ss(sp(minusA,6-j,n),comb(6,j))for j in range(7)];minusB=ss(B,-1)
    f2=[sa(sm(minusB,minusB,n),ss(pair,-1),n=n),ss(minusB,2),sj(1,n)];der=[[{}]*(n+1)for _ in range(9)]
    for j,S in enumerate(f6):
        for k,T in enumerate(f2):der[j+k]=sa(der[j+k],sm(S,T,n),n=n)
    need([ss(out[j+1],j+1)for j in range(9)]==[ss(row,9)for row in der],'all original dense derivative vs translated primitive')
    return v,A,B,K,out
