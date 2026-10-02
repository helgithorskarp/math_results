"""Complete10-coordinate Gram and full frame, including actual empty.

The fixed antisymmetric2 and symmetric8 sectors and complete untouched
space are justified for every n>=3 in PROOF.md.
"""
from fractions import Fraction as F
from exact import require

def model(q, fraction=F):
    s=q+3; N=2*q+8; w=q+2; G=[[fraction(0)]*10 for _ in range(10)]
    d=fraction(3,5)*(q-6)/q
    g=fraction(1,5)*(q-4)/w
    b=(d*(q-1)/(q+1)-g)/2
    a=-b*(q+1)/(q-1);f=-2*a-d;e=-g-2*b;c=(a-d)*q/s
    G[0][0]=q-1;G[1][1]=3
    for i in [2,3]:G[i][i]=3*(q-1)
    G[2][3]=G[3][2]=-3;G[4][4]=fraction(2,3)*s
    G[5][5]=2*s;G[6][6]=6*s
    def zeros():return [fraction(0)]*10
    def add(*x):return [sum(z) for z in zip(*x)]
    def mul(k,x):return [k*z for z in x]
    def unit(j):
        z=zeros();z[j]=fraction(1);return z
    def inner(x,y):return sum(x[i]*G[i][j]*y[j] for i in range(10) for j in range(10) if x[i] and y[j] and G[i][j])
    h=mul(fraction(1,3),add(unit(1),unit(2)))
    Vz=add(mul(fraction(1,3),add(unit(1),unit(3))),unit(4))
    K=add(unit(0),unit(2),mul(fraction(1,3),add(unit(1),unit(3))),unit(4))
    common=add(mul(fraction(-1,5),K),mul(a,h),mul(b,Vz))
    P=[add(common,mul(-c/2,unit(5)),mul(c/6,unit(6))),
       add(common,mul(c/2,unit(5)),mul(c/6,unit(6))),
       add(mul(fraction(-1,5),K),mul(d,h),mul(e,Vz)),
       add(mul(fraction(-1,5),K),mul(f,h),mul(g,Vz),mul(-c/3,unit(6)))]
    eta=[w-inner(p,p) for p in P]
    r=-1-inner(P[0],P[2]);t=(eta[2]+2*r-eta[3])/2
    W12=-eta[0]-r-t;W34=-eta[2]-2*r
    G[7][7]=2*(eta[0]-W12);G[8][8]=eta[2];G[9][9]=eta[3];G[8][9]=G[9][8]=W34
    W=[mul(fraction(1,2),add(unit(7),mul(-1,unit(8)),mul(-1,unit(9)))),
       mul(fraction(1,2),add(mul(-1,unit(7)),mul(-1,unit(8)),mul(-1,unit(9)))),unit(8),unit(9)]
    T=[add(mul(fraction(1,2),unit(5)),mul(fraction(1,6),unit(6))),
       add(mul(fraction(-1,2),unit(5)),mul(fraction(1,6),unit(6))),mul(fraction(-1,3),unit(6))]
    updates=[add(h,tv) for tv in T]+[Vz]+[add(p,wr) for p,wr in zip(P,W)]+[mul(fraction(-1,5),K)]
    frame=[[fraction(0)]*10 for _ in range(10)]
    frame[0][0]=q*q-1;frame[0][1]=frame[1][0]=3*(q-1);frame[1][1]=9
    for i in [2,3]:
        for j in [2,3]:frame[i][j]=6*G[i][j]
    for v in updates:
        products=[sum(G[i][j]*v[j] for j in range(10) if G[i][j] and v[j]) for i in range(10)]
        for i in range(10):
            for j in range(10):frame[i][j]+=products[i]*products[j]
    return G,frame,{'d':d,'a':a,'b':b,'c':c,'f':f,'g':g,'e':e,'eta':eta,'r':r,'t':t,'W12':W12,'W34':W34}
