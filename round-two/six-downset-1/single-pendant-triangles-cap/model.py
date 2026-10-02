"""All-count fixed-arrow and exact sufficient cap forms.

The reduction is ordinary mathematics in PROOF.md. All arithmetic is
Fraction unless an exact rational-function layer is explicitly supplied.
"""
from fractions import Fraction as F
from sectors import parameters

def arrow(q,r,l,fraction=F):
    q,r,l=map(fraction,(q,r,l))
    m=3*r+l;N=2*q+2*m;H=N-1;D=N-7;s=q+3;A=N-q-2
    J=A*(N-4)-3*(q-1);rho=(q-1)/(q+1)
    aa=(m-q*(l+r)/D-2*r*s/H)/(3*r*l)
    zz=2*(2*m-7)/(D*H)
    bb=m-m*m*A/(3*J)-((l+9*r)*q-m*m)/(3*D)-2*l*s/(3*H)
    cc=-m*(1-(2*m-1)/J)
    dd=2*m+1-((q-1)*(N-10)+3*A)/J
    cross=[1/(3*r)+rho/l,1-rho,rho-1]
    tauhat=m/(3*r*l)
    aug=[[aa,zz,fraction(0),cross[0]], [zz,bb,cc,cross[1]],
         [fraction(0),cc,dd,cross[2]],
         cross+[tauhat+1/(3*r)+rho*rho/l]]
    return aug,locals()

def base_pairing(q,r,l,fraction=F):
    q,r,l=map(fraction,(q,r,l))
    m=3*r+l;N=2*q+2*m;H=N-1;D=N-7;s=q+3;A=N-q-2
    J=A*(N-4)-3*(q-1);rho=(q-1)/(q+1);ell=m+1
    h=[fraction(0),fraction(1)/3,1/(3*r),fraction(0),fraction(0)]
    v=[fraction(0),fraction(1)/3,fraction(0),1/(3*l),1/l]
    K=[fraction(1),(m-3)/3,fraction(1),fraction(1)/3,fraction(1)]
    E=[a-rho*b for a,b in zip(h,v)]
    def inner(a,b):
        return (((q-1)*(N-4)*a[0]*b[0]+3*(q-1)*(a[0]*b[1]+a[1]*b[0])
                 +3*A*a[1]*b[1])/J
                +3*(r*(q-r)*a[2]*b[2]-r*l*(a[2]*b[3]+a[3]*b[2])
                    +l*(q-l)*a[3]*b[3])/D+2*l*s*a[4]*b[4]/(3*H))
    columns=[h,v,K];weights=[1/(3*r),1/l,ell]
    S3=[[weights[i]*(i==j)-inner(a,b) for j,b in enumerate(columns)]
        for i,a in enumerate(columns)]
    b=[inner(a,E) for a in columns];EE=inner(E,E)
    return S3,b,EE,locals()

def single_parameters(q,r,fraction=F):
    q,r=map(fraction,(q,r));l=fraction(1);s=q+3;w=q+2;m=3*r+1;ell=m+1;t=r
    N=2*q+2*m;H=N-1;rho=(q-1)/(q+1)
    d=3*(q-ell-1)/(ell*q);g=(q-ell+1)/(ell*w);Fp=-g/rho
    A=(-d-Fp/r)/2;ast=(-r*d/3-A)/(r-1);c=-4*(q-ell-1)/(ell*s)
    E2=q/(3*r)+rho*rho*w;Di2=q*(r-1)/(3*r);common=(ell*q+2-6*r)/(ell*ell)
    etaL=w-common-A*A*E2-ast*ast*Di2-2*s*c*c/3
    etaF=w-common-d*d*(E2+Di2)-2*s*c*c*(r-1)/(3*t*t)
    etaP=w-common-Fp*Fp*E2-2*s*c*c*r/(3*t*t)
    pair=-1-common-A*d*E2-ast*d*Di2
    mu=(2*pair+etaF)/3;alpha=2*(2*etaL-pair-etaF);beta=etaF-mu
    C=etaP/(3*r);nuT=(r*mu-C/3)/(r-1)
    return locals()

def forms(q,r,l=1,fraction=F):
    if l!=1:raise ValueError('single-pendant form domain l1')
    p=single_parameters(q,r,fraction);q,r=p['q'],p['r']
    s,t,N,H,m,ell=[p[z] for z in ('s','t','N','H','m','ell')]
    c,d,ast,alpha,beta,nuT=[p[z] for z in ('c','d','ast','alpha','beta','nuT')]
    half=fraction(1)/2
    anti=[[H/(2*s)-(1+c*c)/2,c/2],[c/2,H/alpha-half]]
    Tq,Ts=H-q-6,H-q-3
    base=[6*q*Tq,12*s*Ts,2*nuT*H,2*beta*H]
    updates=[[ast*q,c*s,nuT,-beta/2],[d*q,2*c*s/t,nuT,beta]]
    LL=ast*ast*q/(6*Tq)+c*c*s/(12*Ts)+nuT/(2*H)+beta/(8*H)
    FF=d*d*q/(6*Tq)+c*c*s/(3*t*t*Ts)+nuT/(2*H)+beta/(2*H)
    LF=ast*d*q/(6*Tq)+c*c*s/(6*t*Ts)+nuT/(2*H)-beta/(4*H)
    triangle=[[fraction(1)/4-LL,-LF],[-LF,half-FF]]
    augmented,info=arrow(q,r,l,fraction);tauhat=info['tauhat']
    aZ=-p['Fp']/(3*r);bZ=c/(9*r*t);dE=p['A']-d
    bD=c*(t+2*(r-1))/(6*r*t);T=6*r*s/(H-s)
    j,k=1/(3*r*m),3/(2*r)
    ZZ=aZ*aZ*tauhat+bZ*bZ*T+p['C']/(3*r*H)
    DD=dE*dE*tauhat+bD*bD*T+9*beta/(4*r*H)
    ZD=aZ*dE*tauhat+bZ*bD*T
    final=[[j-ZZ,-ZD],[-ZD,k-DD]]
    return locals()
