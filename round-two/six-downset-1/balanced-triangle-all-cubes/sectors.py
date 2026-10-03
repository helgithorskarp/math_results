"""PRIVATE complete variable-q forms, including all untouched old spaces.

Actual physical multiplicities require q=2^(n-1), n>=3 and integerh>=2.
The changed rational forms are defined on auxiliary realq>=4,h>=2.
"""
from fractions import Fraction as F
from recipe import recipe

def diag(values):return [[v if i==j else F(0) for j in range(len(values))] for i,v in enumerate(values)]
def frame(G,rows):
    n=len(G);out=[[F(0) for j in range(n)] for i in range(n)]
    for row,mult in rows:
        paired=[sum((v*e for v,e in zip(g,row)),F(0)) for g in G]
        for i in range(n):
            for j in range(n):out[i][j]+=mult*paired[i]*paired[j]
    return out

def sectors(q,h):
    if type(q) is int:q=F(q)
    if type(h) is int:h=F(h)
    p=recipe(q,h);s,alpha,beta,nu,N,a,b,c,ell,D=[p[z] for z in ('s','alpha','beta','nu','N','a','b','c','ell','D')]
    grams={};frames={}
    G=diag([2*s,alpha]);grams['anti']=G
    frames['anti']=frame(G,[([F(1,2),0],1),([F(-1,2),0],1),([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)])
    G=diag([2*s/3,12*s,2*beta,2*nu]);grams['standard']=G
    rows=[([F(1,2),F(1,12),0,0],4),([F(1,2),F(-1,6),0,0],2),([a/2,c/12,F(-1,4),F(1,2)],4),([b/2,c/(6*(h-1)),F(1,2),F(1,2)],2)]
    frames['standard']=frame(G,rows)
    G=diag([4*(q-1),4*D,2*D*(q-2),12*h*s,2*h*beta]);grams['fixed-even']=G
    z=[-1/(2*ell),1/(2*ell),-1/ell]
    rows=[([1/(2*(q-1)),0,1/(q-2),0,0],q/2-1),([1/(2*(q-1)),0,0,0,0],q),([1/(2*(q-1)),0,-1/(q-2),0,0],q/2-1),([F(-1,2),F(1,2),0,0,0],1),
          ([0,-1/(2*D),1/(2*D),1/(12*h),0],4*h),([0,-1/(2*D),1/(2*D),-1/(6*h),0],2*h),
          (z+[c/(12*h),-1/(4*h)],4*h),(z+[-c/(6*h),1/(2*h)],2*h),(z+[0,0],1)]
    frames['fixed-even']=frame(G,rows)
    G=diag([2*q*D,12*h*s,2*h*beta,2*h*nu]);grams['fixed-odd']=G
    rows=[([1/q,0,0,0],q),([1/(2*D),1/(12*h),0,0],4*h),([1/(2*D),-1/(6*h),0,0],2*h),
          ([0,c/(12*h),-1/(4*h),1/(2*h)],4*h),([0,-c/(6*h),1/(2*h),1/(2*h)],2*h)]
    frames['fixed-odd']=frame(G,rows)
    # Pair-constant contrast representative has coefficient norm^2=2.
    grams['untouched-even']=[[8*q]];frames['untouched-even']=[[16*q*q]]
    # Pair-antisymmetric representative has coefficient norm^2=1.
    grams['untouched-odd']=[[4*D]];frames['untouched-odd']=[[8*D*D]]
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return p,grams,frames,caps
