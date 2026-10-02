"""Original-space replay of the two-triangle extension.

Uses the pre-existing independently derived literal mixed builder, rather
than manufacturing actual Gram entries from the new scalar expressions.
All finite checks complement the ordinary uniform proof in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,signal,resource
from model import parameters,fixed,base_pairing
from sectors import check_reduced
from builder import build,solve
from verify_original import compare,baseline
from exact import require,matvec,dot,scale,vecadd,unit,zero,psd_rank,lift
from sectors import reduced,frame

def control(q,r,l):
    sectors,p=reduced(q,r,l,mean_recipe='cap-harmonic');G,S=sectors['fixed']
    h=scale(F(1,3),vecadd(unit(8,1),scale(F(1,r),unit(8,2))))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    E=vecadd(h,scale(-p['rho'],v))
    K=vecadd(unit(8,0),scale(F(3*r+l-3,3),unit(8,1)),unit(8,2),scale(F(1,3),unit(8,3)),unit(8,5))
    t=r+l-1
    Z=vecadd(scale(-l*p['Fp']/(3*r),E),scale(p['c']*l/(9*r*t),unit(8,4)),scale(F(1,r),unit(8,7)))
    D=vecadd(scale(p['A']-p['D'],E),scale(p['c']*F(t+2*(r-1),6*r*t),unit(8,4)),scale(F(-3,2*r),unit(8,6)))
    old=zero(8);old[0][0]=q*q-1;old[0][1]=old[1][0]=3*(q-1);old[1][1]=F(9)
    for i in (2,3):
        for j in (2,3):old[i][j]=6*G[i][j]
    grouped=frame(G,[(F(1,6*r),unit(8,4)),(3*r,h),(l,v),(F(1,p['ell']),K),
                     (F(3*r*p['m'],l),Z),(F(2*r,3),D)],old)
    require(all(isinstance(z,F) for row in grouped for z in row),'exact Fraction grouping; no float coercion')
    require(grouped==S,'ALL64 both-count grouped frame identities with actual empty')
    N=int(p['N']);s=int(p['s']);m=p['m'];ell=p['ell']
    J=(N-q-2)*(N-4)-3*(q-1);Db=N-7;Hb=N-1;A0=N-q-2
    def inner(x,y):
        return ((q-1)*(N-4)*x[0]*y[0]+3*(q-1)*(x[0]*y[1]+x[1]*y[0])+3*A0*x[1]*y[1])/J+3*(r*(q-r)*x[2]*y[2]-r*l*(x[2]*y[3]+x[3]*y[2])+l*(q-l)*x[3]*y[3])/Db+F(2*l*s,3)*x[4]*y[4]/Hb
    ix=[0,1,2,3,5];columns=[[z[i] for i in ix] for z in (h,v,K)];weights=[F(1,3*r),F(1,l),F(ell)]
    S3=[[weights[i]*(i==j)-inner(a,b) for j,b in enumerate(columns)] for i,a in enumerate(columns)]
    change=[[1,3*r,-3*r],[-1,l,-l],[0,0,1]]
    transformed=[[sum(change[a][i]*S3[a][b]*change[b][j] for a in range(3) for b in range(3)) for j in range(3)] for i in range(3)]
    aa=(m-F(q*(l+r),Db)-F(2*r*s,Hb))/(3*r*l)
    zz=F(2*(6*r+2*l-7),Db*Hb)
    bb=m-F(m*m*A0,3*J)-F((l+9*r)*q-m*m,3*Db)-F(2*l*s,3*Hb)
    cc=-m*(1-F(6*r+2*l-1,J));dd=2*m+1-F((q-1)*(N-10)+3*A0,J)
    arrow=[[aa,zz,F(0)],[zz,bb,cc],[F(0),cc,dd]]
    require(transformed==arrow,'ALL9 both-count base Schur arrow identities')
    return {'q':q,'r':r,'l':l,'positions':64,'Cmean':str(p['cross']),
            'necessary_mean_cap':str(p['m']*p['cross']),'N':str(p['N']),
            'arrow_identity_positions':9,'candidate_tau_bound':str(F(m,3*r*l)),
            'scope':'exact grouping identity only; no uniform sign or new H claim'}

def fixed_control(q,l):
    sectors,oldp=check_reduced(q,2,l,'cap-harmonic')
    G,S=sectors['fixed'];N=oldp['N'];m=oldp['m'];t=l+1;p=parameters(q,l)
    for key in ('rho','d','g','A','D','Fp','c','etaL','etaF','etaP','mu','alpha','beta','ast','nuT','nuL'):
        require(p[key]==oldp[key],'every old/new closed scalar '+key)
    require(p['C']==oldp['cross'],'harmonic mean scalar identity')
    h=scale(F(1,3),vecadd(unit(8,1),scale(F(1,2),unit(8,2))))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    E=vecadd(h,scale(-p['rho'],v))
    Z=vecadd(scale(-l*p['Fp']/6,E),scale(p['c']*F(l,18*t),unit(8,4)),scale(F(1,2),unit(8,7)))
    D=vecadd(scale(p['A']-p['D'],E),scale(p['c']*F(t+2,12*t),unit(8,4)),scale(F(-3,4),unit(8,6)))
    ix=[0,1,2,3,5];Gamma=[[G[i][j] for j in ix] for i in ix]
    B5=[[S[i][j] for j in ix] for i in ix]
    for count,z in ((F(6*m,l),Z),(F(4,3),D)):
        image=matvec(G,z)
        for i,a in enumerate(ix):
            for j,b in enumerate(ix):B5[i][j]-=count*image[a]*image[b]
    A5=[[(N-1)*Gamma[i][j]-B5[i][j] for j in range(5)] for i in range(5)]
    require(psd_rank(A5)==5,'complete old/light base5')
    eb=matvec(Gamma,[E[i] for i in ix]);tau=dot(eb,solve(A5,eb))
    S3,b,EE,_=base_pairing(q,l)
    woodbury=EE+dot(b,solve(S3,b))
    _,final,_,info=fixed(q,l,upper_bounds=True)
    require(tau==woodbury and tau<info['tau_bound'],'full Gaussian5/Schur3 inverse and uniform bound')
    # All16 triangle-standard bilinear entries; first marked updates have
    # exactly diagonal contribution (6q^2,12s^2,0,0).
    TG,TS=sectors['triangle_standard']
    direct=[[(N-1)*TG[i][j]-TS[i][j] for j in range(4)] for i in range(4)]
    updated=[[p['base'][i]*(i==j)-sum(c*p['updates'][k][i]*p['updates'][k][j]
              for k,c in enumerate((4,2))) for j in range(4)] for i in range(4)]
    require(updated==direct,'ALL16 triangle diagonal/two-update positions')
    schur=[[(F(1,4) if i==0 else F(1,2))*(i==j)-sum(
             p['updates'][i][k]*p['updates'][j][k]/p['base'][k] for k in range(4))
             for j in range(2)] for i in range(2)]
    require(schur==p['triangle'],'ALL4 already-cancelled triangle Schur positions')
    grouped=control(q,2,l)
    return {'q':q,'l':l,'N':int(N),'fixed_positions':64,'triangle_update_positions':16,
            'triangle_schur_positions':4,'tau':str(tau),'tau_bound':str(info['tau_bound']),
            'scalar_parameters_compared':17,'grouped_control':grouped}

def actual(n,l):
    row=compare(n,2,l,'cap-harmonic')
    family,C,W,pars,*_=build(n,2,l,mean_recipe='cap-harmonic');N=pars['N'];s=pars['s']
    p=parameters(pars['q'],l)
    for key in ('d','g','A','D','Fp','a','c','etaL','etaF','etaP','mu','alpha','beta'):
        require(p[key]==pars[key],'new closed/independent literal scalar '+key)
    require(p['pair']==pars['R'] and p['C']==pars['cross'],'literal pairing and harmonic mean')
    require(p['nuT']==pars['mu']-pars['a_mean'] and p['nuL']==pars['etaP']-pars['b_mean'],
            'literal actual mean standard eigenvalues')
    delta=F(row['whole']['delta']);private=[2*pars['q']-1+2*i for i in range(pars['m'])]
    repaired=[r[:] for r in C]
    for i in range(3):
        a,b=private[i],private[-1]
        repaired[a][b]+=delta;repaired[b][a]+=delta
    M=lift(repaired,s);lower=[[(N-s)*M[i][j]+s*(i==j) for j in range(N)] for i in range(N)]
    kernels=[]
    for bit in (1,2):
        z=[F(bool(A&bit))-F(s,N) for A in family]
        require(matvec(lower,z)==[F(0)]*N and any(z),'actual centered maximum-star kernel')
        kernels.append(z)
    require(kernels[0]!=kernels[1] and kernels[0]!=scale(-1,kernels[1]),'two distinct forced star kernels')
    require(psd_rank([[dot(a,b) for b in kernels] for a in kernels])==2,'independent actual maximum-star kernel Gram')
    row['two_actual_maximum_star_kernels']=True
    row['full_original_positions_per_seed_or_repair']=N*N
    return row
