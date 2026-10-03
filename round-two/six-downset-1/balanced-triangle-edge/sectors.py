"""Complete physical symmetry forms for balanced n2 private triangles."""
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

def sectors(h):
    if type(h) is int:h=F(h)
    p=recipe(h);s,alpha,beta,nu,N,a,b,c,ell=[p[z] for z in ('s','alpha','beta','nu','N','a','b','c','ell')]
    grams={};frames={}
    G=diag([2*s,alpha])
    S=frame(G,[([F(1,2),0],1),([F(-1,2),0],1),([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)])
    grams['anti']=G;frames['anti']=S
    G=diag([2*s/3,12*s,2*beta,2*nu])
    rows=[([F(1,2),F(1,12),0,0],4),([F(1,2),F(-1,6),0,0],2),([a/2,c/12,F(-1,4),F(1,2)],4),([b/2,c/(6*(h-1)),F(1,2),F(1,2)],2)]
    grams['standard']=G;frames['standard']=frame(G,rows)
    G=diag([F(1),3*h,12*h*s,2*h*beta])
    rows=[([1,0,0,0],2),([-1,-1,0,0],1),([0,1/(3*h),1/(12*h),0],4*h),([0,1/(3*h),-1/(6*h),0],2*h),([-1/ell,-1/ell,c/(12*h),-1/(4*h)],4*h),([-1/ell,-1/ell,-c/(6*h),1/(2*h)],2*h),([-1/ell,-1/ell,0,0],1)]
    grams['fixed-even']=G;frames['fixed-even']=frame(G,rows)
    G=diag([3*h,12*h*s,2*h*beta,2*h*nu])
    rows=[([1,0,0,0],2),([1/(3*h),1/(12*h),0,0],4*h),([1/(3*h),-1/(6*h),0,0],2*h),([0,c/(12*h),-1/(4*h),1/(2*h)],4*h),([0,-c/(6*h),1/(2*h),1/(2*h)],2*h)]
    grams['fixed-odd']=G;frames['fixed-odd']=frame(G,rows)
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return p,grams,frames,caps
