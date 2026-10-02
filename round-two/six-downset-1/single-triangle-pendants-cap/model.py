"""Rational one-triangle/pendant model and exact small Schur forms.

The complete original-space implication is ordinary mathematics in PROOF.md.
"""
from fractions import Fraction as F
from exact import require,matvec,dot,vecadd,scale,unit,zero

def parameters(q,l,fraction=F):
    if fraction is F:
        require(type(l) is int and l>=2 and q>=4*l-4,'one triangle/l pendants continuous sign domain')
    q=fraction(q);l=fraction(l);s=q+3;w=q+2;m=l+3;ell=l+4;N=2*q+6+2*l
    rho=(q-1)/(q+1);d=3*(q-ell-1)/(ell*q);g=(q-ell+1)/(ell*w)
    Fp=-g/rho;A=(-d-l*Fp)/2;c=(A-d)*q/s
    E2=q/3+rho*rho*w/l;common=(ell*q-4)/(ell*ell)
    etaL=w-common-A*A*E2-2*s*c*c/3
    etaF=w-common-d*d*E2
    etaP=w-common-Fp*Fp*E2-g*g*w*(l-1)/l-2*s*c*c/(3*l*l)
    pair=-1-common-A*d*E2;mu=(2*pair+etaF)/3
    alpha=2*(2*etaL-pair-etaF);beta=etaF-mu;C=3*mu/l
    nuL=(l*etaP-3*C)/(l-1)
    # Anti2 is congruent via its positive Gram to this matrix.
    anti=[[(N-1)/(2*s)-(1+c*c)/2,c/2],
          [c/2,(N-1)/alpha-fraction(1,2)]]
    # Standard3: positive diagonal D minus TWO actual update columns,
    # b=(q,2s/3,0),p=(gq,2sg/3,nuL). The2x2 Schur test is equivalent.
    B=q/(6*(N-7))+s/(3*(N-1))
    standard=[[fraction(1,2)-B,-g*B],
              [-g*B,fraction(1,2)-g*g*B-nuL/(2*(N-1))]]
    return locals()


def determinant3(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
            -A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
            +A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))

def inverse_quad3(A,b):
    adj=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rows=[a for a in range(3) if a!=j];cols=[a for a in range(3) if a!=i]
            row.append((-1)**(i+j)*(A[rows[0]][cols[0]]*A[rows[1]][cols[1]]-A[rows[0]][cols[1]]*A[rows[1]][cols[0]]))
        adj.append(row)
    return dot(b,matvec(adj,b))/determinant3(A)

def fixed(q,l,fraction=F,compute_tau=True):
    p=parameters(q,l,fraction);q=p['q'];l=p['l'];N=p['N'];s=p['s'];ell=p['ell'];rho=p['rho'];m=p['m']
    h=[fraction(0),fraction(1,3),fraction(1,3),fraction(0),fraction(0)]
    v=[fraction(0),fraction(1,3),fraction(0),1/(3*l),1/l]
    K=[fraction(1),l/3,fraction(1),fraction(1,3),fraction(1)]
    E=vecadd(h,scale(-rho,v))
    J=(N-q-2)*(N-4)-3*(q-1)
    def inner(x,y):
        small=((q-1)*(N-4)*x[0]*y[0]+3*(q-1)*(x[0]*y[1]+x[1]*y[0])
               +3*(N-q-2)*x[1]*y[1])/J
        oldA=3*((q-1)*x[2]*y[2]-l*(x[2]*y[3]+x[3]*y[2])+l*(q-l)*x[3]*y[3])/(N-7)
        light=fraction(2,3)*l*s*x[4]*y[4]/(N-1)
        return small+oldA+light
    columns=[h,v,K];weights=[fraction(1,3),1/l,ell]
    S3=[[weights[i]*(i==j)-inner(a,b) for j,b in enumerate(columns)] for i,a in enumerate(columns)]
    b=[inner(a,E) for a in columns]
    tau=inner(E,E)+inverse_quad3(S3,b) if compute_tau else (l+3)/(3*l)
    T=6*s/(N-1-s);a=-l*p['Fp']/3;d=p['A']-p['d'];c=p['c']
    ZZ=a*a*tau+c*c*T/81+p['mu']/(N-1)
    DD=d*d*tau+c*c*T/36+fraction(9,4)*p['beta']/(N-1)
    ZD=a*d*tau+c*c*T/54
    S2=[[l/(3*m)-ZZ,-ZD],[-ZD,fraction(3,2)-DD]]
    return S3,S2,p,{'tau':tau,'base_J':J,'pre_E_inverse':inner(E,E),
                   'inverse_pairings':b,'tau_bound':(l+3)/(3*l)}

def frame(G,updates,old=None):
    S=zero(len(G)) if old is None else [row[:] for row in old]
    for count,v in updates:
        image=matvec(G,v)
        for i in range(len(G)):
            for j in range(len(G)):S[i][j]+=count*image[i]*image[j]
    return S

def reduced(q,l):
    """Closed Gram and complete-frame bilinears, including actual empty."""
    p=parameters(q,l);q=p['q'];l=int(p['l']);s=p['s'];N=p['N'];rho=p['rho'];ell=p['ell']
    G=zero(8)
    for i,z in enumerate([q-1,F(3),3*(q-1),3*l*(q-l),6*s,F(2*l,3)*s,
                          p['beta'],p['mu']]):G[i][i]=z
    G[2][3]=G[3][2]=F(-3*l)
    h=scale(F(1,3),vecadd(unit(8,1),unit(8,2)))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    E=vecadd(h,scale(-rho,v))
    K=vecadd(unit(8,0),scale(F(l,3),unit(8,1)),unit(8,2),scale(F(1,3),unit(8,3)),unit(8,5))
    common=scale(-1/ell,K)
    vmL=vecadd(h,scale(F(1,6),unit(8,4)))
    vmF=vecadd(h,scale(F(-1,3),unit(8,4)))
    upL=vecadd(common,scale(p['A'],E),scale(p['c']/6,unit(8,4)),unit(8,7),scale(F(-1,2),unit(8,6)))
    upF=vecadd(common,scale(p['d'],E),unit(8,7),unit(8,6))
    upP=vecadd(common,scale(p['Fp'],E),scale(-p['c']/(3*l),unit(8,4)),scale(F(-3,l),unit(8,7)))
    old=zero(8);old[0][0]=q*q-1;old[0][1]=old[1][0]=3*(q-1);old[1][1]=F(9)
    for i in (2,3):
        for j in (2,3):old[i][j]=6*G[i][j]
    S=frame(G,[(2,vmL),(1,vmF),(l,v),(2,upL),(1,upF),(l,upP),(1,common)],old)
    out={'fixed':(G,S)}
    G=zero(2);G[0][0]=2*s;G[1][1]=p['alpha']
    S=frame(G,[(F(1,2),[F(1),F(0)]),(F(1,2),[-p['c'],F(1)])])
    out['anti']=(G,S)
    G=zero(3)
    for i,z in enumerate([6*q,F(4,3)*s,2*p['nuL']]):G[i][i]=z
    old=zero(3);old[0][0]=6*G[0][0]
    S=frame(G,[(2,[F(1,6),F(1,2),F(0)]),(2,[p['g']/6,p['g']/2,F(1,2)])],old)
    out['standard']=(G,S)
    return out,p
