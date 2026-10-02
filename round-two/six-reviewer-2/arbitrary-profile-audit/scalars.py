"""Definition-derived rational budgets, independent of any author executable."""
from linear import F,need,psd,digest,canonical

def profile(q,loads):
    need(type(q) is int and q>=8,'q>=8')
    need(type(loads) in [list,tuple] and 4<=len(loads)<=20,'4..20 audit marks')
    need(all(type(d) is int and d>0 for d in loads),'positive integer loads')
    R=len(loads);D=max(loads);m=sum(loads);S=m-D;w=q+D-1;h=2*q+2*m-1;s=w+1
    need(q>R and D>=3 and m>=7 and S>=4 and len(set(loads))>=3,'new branch hypotheses')
    c=[F(m*(w-d-m-1),(m+1)*((m-1)*w-1+d)) for d in loads]
    B0=w+m*s-sum(d*d for d in loads)
    B0-=2*m
    C2=sum(d*x*x*(s-d) for d,x in zip(loads,c));KC=sum(d*x*(w-d) for d,x in zip(loads,c))
    eta=[w-F(B0,(m+1)**2)-x*x*w+2*x*x*F(s-d,m)-C2/m**2+2*x*F(w-d,m+1)-2*KC/(m*(m+1)) for d,x in zip(loads,c)]
    E=sum(d*x for d,x in zip(loads,eta));zeta=[F(m,m-2)*(x-E/(m*(m-1))) for x in eta]
    Delta=(h-q-1)*(h-D)-D*(q-1);rho=F(2*m-1,Delta);kap=rho/(h-2*D);theta=F(2*S-1,h*(h-2*D));g=F(s,h)
    Rgg=F(h*w-2*D*(2*q-1),Delta)
    gamma=[g-d*theta for d in loads];b=[1-x for x in gamma];Hsum=sum(F(d)/x for d,x in zip(loads,b));T=1+kap*Hsum;lam=(1-rho)/T
    nu=[-1+lam/x for x in b];Kgap=2*m+1-Rgg-Hsum*(1-rho)**2/T
    Gamma=[[F(i==j)*gamma[i]/(loads[i]*b[i])-kap/(T*b[i]*b[j])+nu[i]*nu[j]/Kgap for j in range(R)] for i in range(R)]
    # Balanced-coordinate basis x=e_i/d_i-e_last/d_last, input metric sum d_i x_i^2.
    balanced=[[F(j==i,loads[i])-F(j==R-1,loads[-1]) for j in range(R)] for i in range(R-1)]
    metric=[[sum(d*a*b for d,a,b in zip(loads,x,y)) for y in balanced] for x in balanced]
    budget=[]
    for x in balanced:
        row=[]
        for y in balanced:
            cost=sum(loads[i]*loads[j]*c[i]*x[i]*Gamma[i][j]*c[j]*y[j] for i in range(R) for j in range(R))
            row.append(sum(d*a*b*(1-z/h) for d,a,b,z in zip(loads,x,y,zeta))-cost)
        budget.append(row)
    C=max(F(1,m-1),F(1,w));need(C<=F(1,6) and all(abs(x)<C for x in c),'c bound')
    need(0<B0<(m+1)*w and C2<=C*C*m*(w+1) and abs(KC)<=C*m*w,'constructor bounds')
    need(all(F(319,420)*w<x<F(344,315)*w for x in eta),'eta interval')
    need(all(F(3,4)*w<x<F(7,5)*w for x in zeta),'zeta interval')
    need(0<rho<1 and 0<Rgg<1 and Delta>h*w>2*m-1,'plane resolvent')
    need(all(0<x<g<F(1,2) for x in gamma),'gamma')
    need(Kgap>F(m*(2*S-1),w+2*S),'Kgap')
    need(all(1-z/h-x*x*g/(1-g)>F(49,180) for z,x in zip(zeta,c)),'deviation budget')
    f=[x*y for x,y in zip(c,nu)];spread=max(f)-min(f)
    need(spread<F(3,w),'improved range')
    cost=F(m,4)*spread**2/Kgap
    bound=F(9*(w+2*S),4*(2*S-1)*w*w)
    need(cost<bound<=F(81,1400),'profile-dependent rank-one bound')
    lower=F(49,180)-bound;need(lower>=F(2701,12600)>F(1,5),'improved margin rational constants')
    strong=[[a-F(2701,12600)*v for a,v in zip(row,met)] for row,met in zip(budget,metric)]
    need(psd(strong)['rank']==R-1,'all balanced stronger-budget directions')
    return locals()

def record(q,loads):
    p=profile(q,loads)
    keys=['q','loads','R','D','m','S','w','h','c','B0','C2','KC','eta','zeta','Delta','rho','kap','theta','gamma','b','Hsum','T','lam','nu','Kgap','spread','cost','bound','lower']
    return {k:p[k] for k in keys}|{k+'_sha256':digest(p[k]) for k in ['Gamma','metric','budget']}|{'strong_budget_rank':p['R']-1}
