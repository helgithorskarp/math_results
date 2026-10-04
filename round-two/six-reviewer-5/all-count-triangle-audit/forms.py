"""Written-definition reconstruction for arbitrary unequal counts.

Actual independent reviewer six-reviewer-5. Current author native code and
certificate unread. The generic sector framework is credited to own REVIEW10237;
the independent retained mean, arbitrary l, and spread dual are recomputed here.
Accept either exact Fractions or rational-function-field elements.
"""
def need(t,why):
    if not t: raise ValueError(why)

def build(h,l,q):
    s=q+3*h; d=h-l; ell=3*(h+l)+1; N=2*q+6*(h+l)
    zero=0*h
    def matrix(n):return [[zero for _ in range(n)] for _ in range(n)]
    def add_outer(A,v,c=1):
        for i in range(len(v)):
            for j in range(len(v)): A[i][j]+=c*v[i]*v[j]
    c0=(q*ell+9*l*d-3*h-6*l-1)/ell**2
    gs=[]
    for k,v in ((h,-(q-1)/ell),(l,-(q+3*d-1)/ell)):
        B2=s*(k-1)/(3*k);r=1+v;a=r/(2*B2);b=-2*a;c=9*r/(2*s)
        etaL=s-1-c0-a*a*B2-2*s*c*c/3
        etaF=s-1-c0-b*b*B2-2*s*c*c/(3*(k-1))
        p=-1-c0-a*b*B2
        mu=(2*p+etaF)/3;alpha=2*(2*etaL-p-etaF);beta=etaF-mu
        need(mu==(s-3)/3-c0-9*r*r/(2*s*(k-1)),'expanded mu')
        need(alpha==2*s-27*(2*k-3)*r*r/(s*(k-1)),'expanded alpha')
        need(beta==2*s/3-3*(k+3)*r*r/(s*(k-1)),'expanded beta')
        gs.append(dict(k=k,v=v,r=r,B2=B2,a=a,b=b,c=c,mu=mu,alpha=alpha,beta=beta))
    tau=gs[0]['mu']*gs[1]['mu']/(h*gs[0]['mu']+l*gs[1]['mu'])
    gs[0]['nu']=(h*gs[0]['mu']-l*tau)/(h-1)
    gs[1]['nu']=(l*gs[1]['mu']-h*tau)/(l-1)
    forms={}
    for gi,g in enumerate(gs):
        k,a,b,c,alpha,beta,nu=[g[key] for key in ('k','a','b','c','alpha','beta','nu')]
        forms[str(gi)+'-odd']=([2*s,alpha],[[2*s*s*(1+c*c),-s*c*alpha],[-s*c*alpha,alpha*alpha/2]])
        G=[2*s/3,12*s,2*beta,2*nu]; S=matrix(4)
        for v,w in (([s/3,s,0,0],4),([s/3,-2*s,0,0],2),([a*s/3,c*s,-beta/2,nu],4),([b*s/3,2*c*s/(k-1),beta,nu],2)):
            add_outer(S,v,w)
        forms[str(gi)+'-standard']=(G,S)
        forms[str(gi)+'-trace']=([6*k*s,k*beta],[[6*k*s*s*(1+c*c),-3*k*s*c*beta],[-3*k*s*c*beta,3*k*beta*beta/2]])
    D=3*h; Bbar=s*d/(3*h*l)
    G=[4*(q-1),4*D,2*D*(q-2),2*q*D,Bbar];S=matrix(5)
    # Separately sum literal row-type scores, including the actual empty.
    for ix,iy,count in ((0,0,q/2-1),(1,0,q/2),(0,1,q/2),(1,1,q/2-1)):
        coord=[1/(2*(q-1)),zero,(1-ix-iy)/(q-2),(iy-ix)/q,zero]
        add_outer(S,[G[i]*coord[i] for i in range(5)],count)
    add_outer(S,[-G[0]/2,G[1]/2,zero,zero,zero])
    for v,count in (([zero,-2,q-2,q,zero],3*h),([zero,-2,q-2,-q,Bbar],3*l)):
        add_outer(S,v,count)
    zimage=[-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q*d,-s*d/h]
    add_outer(S,zimage,1/ell)
    forms['five']=(G,S)
    forms['mean']=([h*l*tau],[[3*(h+l)*h*l*tau*tau]])
    kappa=1/(h*l*tau)+4/(l*gs[1]['beta'])
    need(kappa==1/(h*gs[0]['mu'])+1/(l*gs[1]['mu'])+4/(l*gs[1]['beta']),'full harmonic dual identity')
    return dict(h=h,l=l,q=q,s=s,N=N,ell=ell,c0=c0,groups=gs,tau=tau,kappa=kappa,physical=forms)
