"""Integral homogeneous coordinates of the DERIVED thirteen-label G24.

Actual author six-tammes-2, researcher. Label13 here means the fresh x
of the new motif, not the label13 of the older fixed-incumbent G24.
The graph masks are different. No actual extra label is initially fixed
when the motif is applied through the geometric degree theorem.
"""
from polynomials import dot

LABELS=(0,1,2,4,5,6,7,8,9,10,11,12,13)
CONTACTS=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
          (2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),
          (7,12),(9,10),(9,11),(10,12),(5,12),(2,13),(9,13),(10,13))
NORMAL=(-5,-14,20)
CUT=15

def make(t):
    """Ring operations only; no sample, radical, or branch selection."""
    a=1+t; zero=t*0
    Q4=(1-t*t)*(1+3*t)+8*t**4
    L=1+2*t-t*t
    B={1:[a*a,zero,zero],2:[zero,a*a,zero],4:[zero,zero,a*a],
       8:[-a*a,2*t*a,2*t*a],10:[2*t*a,2*t*a,-a*a],
       12:[2*t*(1+3*t),3*t*t-2*t-1,-2*t*a]}
    X=[3*t*t-2*t-1,2*t*(1+3*t),-2*t*a]
    V=[2*t*(5*t*t-1),(3*t+1)*(5*t*t-1),-2*t*a*(3*t+1)]
    Five=[t*a*a*(V[j]+a*B[12][j])-Q4*B[10][j] for j in range(3)]
    W=[1+6*t+5*t*t-28*t**3-29*t**4+94*t**5+103*t**6-56*t**7,
       -2*t*t*(1-t)*(3*t+1)*(3+13*t+11*t*t-7*t**3),
       2*t*a*(3*t+1)*(1+3*t-3*t*t-9*t**3+4*t**4)]
    Zero=[2*t*(L*Five[j]+a*W[j])-a*Q4*L*B[12][j] for j in range(3)]
    Eleven=[2*t*(Zero[j]+a*L*Five[j])-a**3*W[j] for j in range(3)]
    Six=[2*t*(a*Zero[j]+Eleven[j])-a**3*L*Five[j] for j in range(3)]
    Omega=a**5*Q4*L
    Y={i:[a**3*Q4*L*x for x in row] for i,row in B.items()}
    Y[13]=[a**3*Q4*L*x for x in X]
    Y[9]=[a*a*Q4*L*x for x in V]
    Y[5]=[a**3*L*x for x in Five]
    Y[7]=[a**4*x for x in W]
    Y[0]=[a*a*x for x in Zero]
    Y[11]=[a*x for x in Eleven]
    Y[6]=Six
    return Y,Omega,{'Q4':Q4,'L':L,'Five':Five,'W':W,'V':V,'B':B}

def positive_factors(t):
    return (t,1+t,1-t,1+2*t,3*t-1,3*t+1,
            (1-t*t)*(1+3*t)+8*t**4,1+2*t-t*t)
