"""complete sectors; ordinary original completeness proof in PROOF.md.

Integer h>l>=2,q>=4. Physical q=2^(n-1). These new ten aggregate
directions retain the light B mean; no mark-exchange quotient is used.
"""
from fractions import Fraction as F
from exact import require


def parameters(q, h, l):
    if type(q) is int: q = F(q)
    if type(h) is int: h = F(h)
    require(not isinstance(q, float) and not isinstance(h, float), 'exact parameters')
    if type(l) is int: l = F(l)
    s = q+3*h
    N = 2*q+6*(h+l)
    ell = 3*(h+l)+1
    c0 = (q*ell+9*l*(h-l)-3*h-6*l-1)/ell**2
    groups = []
    for k, v in ((h, -(q-1)/ell), (l, -(q+3*(h-l)-1)/ell)):
        B2 = s*(k-1)/(3*k)
        a = (1+v)/(2*B2)
        b = -2*a
        c = 9*(1+v)/(2*s)
        etaL = s-1-c0-a*a*B2-2*s*c*c/3
        etaF = s-1-c0-b*b*B2-2*s*c*c/(3*(k-1))
        pair = -1-c0-a*b*B2
        mu = (2*pair+etaF)/3
        alpha = 2*(2*etaL-pair-etaF)
        beta = etaF-mu
        require(mu+alpha/4+beta/4 == etaL and mu+beta == etaF
                and mu-beta/2 == pair, 'ALL exact residual norm/support identities')
        groups.append(dict(k=k,v=v,B2=B2,a=a,b=b,c=c,mu=mu,
                           alpha=alpha,beta=beta,etaL=etaL,etaF=etaF,pair=pair))
    mux,muy=groups[0]['mu'],groups[1]['mu']
    tau=mux*muy/(h*mux+l*muy)
    nus=[(h*mux-l*tau)/(h-1),(l*muy-h*tau)/(l-1)]
    for g,nu in zip(groups,nus): g['nu']=nu
    return dict(q=q,h=h,l=l,s=s,D=3*h,N=N,ell=ell,c0=c0,groups=groups,tau=tau)


def diag(values):
    return [[v if i == j else F(0) for j in range(len(values))]
            for i,v in enumerate(values)]


def frame(G, rows):
    n=len(G)
    out=[[F(0) for _ in range(n)] for _ in range(n)]
    for row,mult in rows:
        require(len(row)==n, 'complete sector coordinate count')
        image=[sum((v*x for v,x in zip(g,row)),F(0)) for g in G]
        for i in range(n):
            for j in range(n): out[i][j]+=mult*image[i]*image[j]
    return out


def sectors(q,h,l):
    p=parameters(q,h,l)
    q,h,l,s,D,N,ell,tau=[p[z] for z in ('q','h','l','s','D','N','ell','tau')]
    grams,frames,rows_by_group={},{},{}
    for label,g in zip(('x','y'),p['groups']):
        k,a,b,c,alpha,beta,nu=[g[z] for z in ('k','a','b','c','alpha','beta','nu')]
        G=diag([2*s,alpha])
        rows=[([F(1,2),0],1),([F(-1,2),0],1),
              ([-c/2,F(1,2)],1),([c/2,F(-1,2)],1)]
        name='anti-'+label
        grams[name]=G;frames[name]=frame(G,rows);rows_by_group[name]=rows
        G=diag([2*s/3,12*s,2*beta,2*nu])
        rows=[([F(1,2),F(1,12),0,0],4),
              ([F(1,2),F(-1,6),0,0],2),
              ([a/2,c/12,F(-1,4),F(1,2)],4),
              ([b/2,c/(6*(k-1)),F(1,2),F(1,2)],2)]
        name='standard-'+label
        grams[name]=G;frames[name]=frame(G,rows);rows_by_group[name]=rows
    gx,gy=p['groups']
    G=diag([4*(q-1),4*D,2*D*(q-2),2*q*D,
            s*(h-l)/(3*h*l),6*h*s,6*l*s,h*gx['beta'],l*gy['beta'],h*l*tau])
    rows=[]
    for ix,iy,count in ((0,0,q/2-1),(1,0,q/2),(0,1,q/2),(1,1,q/2-1)):
        rows.append(([1/(2*(q-1)),0,(1-ix-iy)/(q-2),(iy-ix)/q]+[0]*6,count))
    rows.append(([F(-1,2),F(1,2)]+[0]*8,1))
    z=[-1/(2*ell),l/(2*h*ell),-(h+l)/(2*h*ell),-(h-l)/(2*h*ell),-3*l/ell]+[0]*5
    for group,g in enumerate(p['groups']):
        k,c,beta=[g[key] for key in ('k','c','beta')]
        mark=[0,-1/(2*D),1/(2*D),(1 if group==0 else -1)/(2*D),group]+[0]*5
        leaf=mark[:];full=mark[:]
        leaf[5+group]=1/(6*k);full[5+group]=-1/(3*k)
        rows.extend([(leaf,2*k),(full,k)])
        leaf=z[:];full=z[:]
        leaf[5+group]=c/(6*k);full[5+group]=-c/(3*k)
        leaf[7+group]=-1/(2*k);full[7+group]=1/k
        leaf[9]=full[9]=1/h if group==0 else -1/l
        rows.extend([(leaf,2*k),(full,k)])
    rows.append((z,1))
    grams['aggregate']=G;frames['aggregate']=frame(G,rows);rows_by_group['aggregate']=rows
    grams['untouched-even']=[[8*q]];frames['untouched-even']=[[16*q*q]]
    grams['untouched-odd']=[[4*D]];frames['untouched-odd']=[[8*D*D]]
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))]
                for i in range(len(G))] for name,G in grams.items()}
    return p,grams,frames,caps,rows_by_group
