"""Exact finite controls for a proposed uniform analytic pendant cap.

The surrounding inequalities and arbitrary-dimension bridges are ordinary
mathematics in PROOF.md, not finite enumeration.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse,json,resource,signal,time
def require(p,message):
    if not p:raise ValueError(message)
def alarm(signum,frame):raise TimeoutError('analytic-control stage60s guard')
signal.signal(signal.SIGALRM,alarm)

def parameters(q,loads):
    require(type(q) is int and q>=8 and all(type(d) is int and d>=1 for d in loads),'exact positive domain')
    D=max(loads);m=sum(loads);S=m-D;w=q+D-1;h=2*q+2*m-1
    require(D>=3 and m>=7 and S>=4 and w>=10 and q>len(loads),'analytic sufficient domain')
    ci=[F(m*(w-d-m-1),(m+1)*((m-1)*w-1+d)) for d in loads]
    B0=w+m*(q+D)-sum(d*d for d in loads)-2*m
    C2=sum(d*c*c*(q+D-d) for d,c in zip(loads,ci));KC=sum(d*c*(w-d) for d,c in zip(loads,ci))
    eta=[F(w)-F(B0,(m+1)**2)-c*c*w+F(2,m)*c*c*(q+D-d)-C2/m**2+F(2,m+1)*c*(w-d)-F(2,m*(m+1))*KC for d,c in zip(loads,ci)]
    E=sum(d*e for d,e in zip(loads,eta));zeta=[F(m,m-2)*(e-E/(m*(m-1))) for e in eta]
    delta=(h-q-1)*(h-D)-D*(q-1);u=2*m-1;rho=F(u,delta);kappa=F(u,delta*(h-2*D));g=F(q+D,h)
    theta=F(2*S-1,h*(h-2*D))
    gamma=[F(d*q,D*(h-2*D))+F(q+D,h)*(1-F(d,D)) for d in loads]
    b=[1-a for a in gamma];H=sum(F(d)/b0 for d,b0 in zip(loads,b))
    Rgg=F(h*w-2*D*(2*q-1),delta)
    denominator=1+kappa*H;lam=(1-rho)/denominator
    Kgap=2*m+1-Rgg-H*(1-rho)**2/denominator
    nu=[-1+lam/b0 for b0 in b]
    Gamma=[[F(gamma[i],loads[i]*b[i])*int(i==j)-kappa/(denominator*b[i]*b[j])+nu[i]*nu[j]/Kgap for j in range(len(loads))] for i in range(len(loads))]
    require(0<rho<1 and 0<Rgg<1 and 0<lam<1,'resolvent auxiliary intervals')
    require(all(0<a<g<F(1,2) and g-a==d*theta for d,a in zip(loads,gamma)),'every marked-spoke scalar and exact difference')
    require(Kgap>F(m*(2*S-1),w+2*S)>0,'common-update Schur lower bound')
    require(all(F(3*w,4)<e<F(11*w,10) for e in eta),'uniform eta interval control')
    require(all(F(3*w,4)<z<F(7*w,5) for z in zeta),'uniform zeta interval control')
    require(all(abs(c)<F(1,6) for c in ci),'uniform singleton coefficient control')
    within=[1-F(z,h)-c*c*g/(1-g) for c,z in zip(ci,zeta)]
    require(all(x>F(49,180)>F(1,4) for x in within),'uniform internal margin control')
    values=[c*n for c,n in zip(ci,nu)];width=max(values)-min(values)
    require(width<F(4,w),'common-update coefficient range')
    weighted_mean=sum(d*x for d,x in zip(loads,values))/m
    variance=sum(d*(x-weighted_mean)**2 for d,x in zip(loads,values))
    require(variance<=m*width*width/4,'weighted Popoviciu control')
    require(variance/Kgap<F(18,175),'common-update variance budget control')
    # Restrict the true residual update budget to sum_i d_i*x_i=0.
    # Basis x_j=1/d_j, x_last=-1/d_last, without a guessed orthogonalization.
    balanced=[[F(i==j,loads[j])-F(i==len(loads)-1,loads[-1]) for i in range(len(loads))] for j in range(len(loads)-1)]
    def form(x,y):
        diagonal=sum(d*(1-F(z,h))*a*b0 for d,z,a,b0 in zip(loads,zeta,x,y))
        old=sum(loads[i]*ci[i]*x[i]*Gamma[i][j]*loads[j]*ci[j]*y[j] for i in range(len(loads)) for j in range(len(loads)))
        return diagonal-old
    budget=[[form(x,y) for y in balanced] for x in balanced]
    metric=[[sum(d*x*y for d,x,y in zip(loads,a,b0)) for b0 in balanced] for a in balanced]
    # Exact LDL with positive pivots of budget-(1/6)*input metric.
    test=[[x-F(1,6)*y for x,y in zip(a,b0)] for a,b0 in zip(budget,metric)]
    pivots=[]
    for j in range(len(test)):
        p=test[j][j];require(p>0,'analytic singleton budget full positive pivot');pivots.append(p)
        for i in range(j+1,len(test)):
            for k in range(j+1,len(test)):test[i][k]-=test[i][j]*test[j][k]/p
    return {'q':q,'loads':loads,'m':m,'D':D,'S':S,'w':w,'h':h,'ci':ci,'eta':eta,'zeta':zeta,'B0':B0,'g':g,'theta':theta,'rho':rho,'kappa':kappa,'H':H,'Rgg':Rgg,'Kgap':Kgap,'nu':nu,'Gamma':Gamma,'within':within,'balanced_budget':budget,'balanced_metric':metric,'K_coefficient_range':width,'K_variance_ratio':variance/Kgap,'positive_budget_pivots':pivots}

def check():
    start=time.monotonic();signal.alarm(60)
    profiles=[[3,2,1,1],[3,2,2,1],[3,3,2,1],[4,3,2,1],[10,3,2,1],[10000,2,1,1],[4,3,2,1,1],[3,3,2,1,1],[8,6,4,3,1],[3,2,1,1,1,1]]
    rows=[]
    cases=[(q,loads) for q in [8,16,32,128,1000000] for loads in profiles if q>len(loads)]
    cases += [(2048,list(range(12,0,-1))),(2048,[6,6,5,5,4,4,3,3,2,2,1,1]),(1<<20,[3,2]+[1]*18)]
    for q,loads in cases:
        p=parameters(q,loads)
        encoded=json.dumps(list(map(str,p['positive_budget_pivots'])),separators=(',',':')).encode()
        rows.append({'q':q,'loads':loads,'Kgap':str(p['Kgap']),'minimum_internal_slack':str(min(p['within'])),'maximum_variance_loss':str(p['K_variance_ratio']),'balanced_budget_dimension':len(loads)-1,'positive_budget_pivots_sha256':sha256(encoded).hexdigest(),'every_budget_pivot_checked':True})
    signal.alarm(0)
    return {'agent':'six-downset-1','role':'researcher','status':'finite exact analytic-identity/bound controls,not a universal proof','cases':rows,'case_count':len(rows),'stage_seconds_guard':60,'elapsed_seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path);args=parser.parse_args();out=check()
    def stable(obj):
        if isinstance(obj,dict):return {k:stable(v) for k,v in obj.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
        if isinstance(obj,list):return [stable(v) for v in obj]
        return obj
    if args.expected:require(stable(out)==stable(json.loads(args.expected.read_text())['bounds']),'whole analytic-control frozen record')
    if args.write:args.write.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
