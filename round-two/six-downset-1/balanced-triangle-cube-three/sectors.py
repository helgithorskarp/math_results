"""Complete q4 physical forms: fixed5/4 and three untouched old modes.

Row projections include every original row and the actual empty. All
interpretation/completeness bridges are ordinary unformalized mathematics.
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

def sectors(h):
    if type(h) is int:h=F(h)
    p=recipe(h);s,alpha,beta,nu,N,a,b,c,ell=[p[z] for z in ('s','alpha','beta','nu','N','a','b','c','ell')]
    grams={};frames={}
    G=diag([2*s,alpha])
    grams['anti']=G;frames['anti']=frame(G,[([F(1,2),0],1),([F(-1,2),0],1),([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)])
    G=diag([2*s/3,12*s,2*beta,2*nu])
    rows=[([F(1,2),F(1,12),0,0],4),([F(1,2),F(-1,6),0,0],2),([a/2,c/12,F(-1,4),F(1,2)],4),([b/2,c/(6*(h-1)),F(1,2),F(1,2)],2)]
    grams['standard']=G;frames['standard']=frame(G,rows)
    G=diag([12,12*h,12*h,12*h*s,2*h*beta])
    z=[-1/(2*ell),1/(2*ell),-1/ell]
    rows=[([F(1,6),0,F(1,2),0,0],1),([F(1,6),0,0,0,0],4),([F(1,6),0,F(-1,2),0,0],1),([F(-1,2),F(1,2),0,0,0],1),
          ([0,-1/(6*h),1/(6*h),1/(12*h),0],4*h),([0,-1/(6*h),1/(6*h),-1/(6*h),0],2*h),
          (z+[c/(12*h),-1/(4*h)],4*h),(z+[-c/(6*h),1/(2*h)],2*h),(z+[0,0],1)]
    grams['fixed-even']=G;frames['fixed-even']=frame(G,rows)
    G=diag([24*h,12*h*s,2*h*beta,2*h*nu])
    rows=[([F(1,4),0,0,0],4),([1/(6*h),1/(12*h),0,0],4*h),([1/(6*h),-1/(6*h),0,0],2*h),
          ([0,c/(12*h),-1/(4*h),1/(2*h)],4*h),([0,-c/(6*h),1/(2*h),1/(2*h)],2*h)]
    grams['fixed-odd']=G;frames['fixed-odd']=frame(G,rows)
    grams['untouched-even']=[[F(32)]];frames['untouched-even']=[[F(256)]]
    grams['untouched-odd']=[[24*h]];frames['untouched-odd']=[[144*h*h]]
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return p,grams,frames,caps
