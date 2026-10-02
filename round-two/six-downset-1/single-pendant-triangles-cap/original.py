"""Whole original and complete fixed-space comparisons; credited literal primitives.

The structural proof is in PROOF.md; author controls are not peer review.
"""
from fractions import Fraction as F
from model import forms,base_pairing
from sectors import check_reduced,reduced,frame
from builder import build,solve
from verify_original import compare,baseline
from exact import require,matvec,dot,scale,vecadd,unit,zero,psd_rank,lift

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
    N=p['N'];s=p['s'];m=p['m'];ell=p['ell']
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

def fixed_control(q,r,l):
    small,p=check_reduced(q,r,l,'cap-harmonic');G,S=small['fixed']
    f=forms(q,r,l);N=p['N'];H=N-1;s=p['s'];m=p['m'];t=p['t']
    h=scale(F(1,3),vecadd(unit(8,1),scale(F(1,r),unit(8,2))))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    E=vecadd(h,scale(-p['rho'],v))
    Z=vecadd(scale(f['aZ'],E),scale(f['bZ'],unit(8,4)),scale(F(1,r),unit(8,7)))
    Dv=vecadd(scale(f['dE'],E),scale(f['bD'],unit(8,4)),scale(F(-3,2*r),unit(8,6)))
    ix=[0,1,2,3,5];Gamma=[[G[i][j] for j in ix] for i in ix]
    B5=[[S[i][j] for j in ix] for i in ix]
    for count,z in ((F(3*r*m,l),Z),(F(2*r,3),Dv)):
        image=matvec(G,z)
        for i,a in enumerate(ix):
            for j,b in enumerate(ix):B5[i][j]-=count*image[a]*image[b]
    A5=[[H*Gamma[i][j]-B5[i][j] for j in range(5)] for i in range(5)]
    require(psd_rank(A5)==5,'whole old/light base5 positive')
    eb=matvec(Gamma,[E[i] for i in ix]);tau=dot(eb,solve(A5,eb))
    S3,b,EE,_=base_pairing(q,r,l)
    require(psd_rank(S3)==3,'whole inverse Schur3 positive')
    require(tau==EE+dot(b,solve(S3,b)) and 0<tau<f['tauhat'],'complete Gaussian5/Woodbury inverse and bound')
    require(psd_rank(f['augmented'])==4,'whole augmented inverse4')
    actual=[[f['final'][i][j]+(f['tauhat']-tau)*[f['aZ'],f['dE']][i]*[f['aZ'],f['dE']][j]
             for j in range(2)] for i in range(2)]
    require(psd_rank(f['final'])==psd_rank(actual)==2,'sufficient and actual final2 positive')
    require(psd_rank([[actual[i][j]-f['final'][i][j] for j in range(2)] for i in range(2)])==1,
            'exact final tau Loewner difference')
    TG,TS=small['triangle_standard']
    direct=[[H*TG[i][j]-TS[i][j] for j in range(4)] for i in range(4)]
    updated=[[f['base'][i]*(i==j)-sum(count*f['updates'][k][i]*f['updates'][k][j]
              for k,count in enumerate((4,2))) for j in range(4)] for i in range(4)]
    require(direct==updated,'all16 complete triangle diagonal/two-update identities')
    schur=[[(F(1,4) if i==0 else F(1,2))*(i==j)-sum(f['updates'][i][k]*f['updates'][j][k]/f['base'][k] for k in range(4)) for j in range(2)] for i in range(2)]
    require(schur==f['triangle'],'all4 cancelled triangle Schur identities')
    AG,AS=small['anti'];norms=[AG[i][i] for i in range(2)]
    require([[ (H*AG[i][j]-AS[i][j])/(norms[i]*norms[j]) for j in range(2)] for i in range(2)]==f['anti'],
            'all4 exact anti congruence positions')
    if l>1:
        PG,PS=small['pendant_standard'];bases=[(H-6)*PG[0][0],H*PG[1][1],H*PG[2][2]]
        images=[[PG[0][0]/6,PG[1][1]/2,F(0)],[p['g']*PG[0][0]/6,p['g']*PG[1][1]/2,PG[2][2]/2]]
        require([[bases[i]*(i==j)-2*sum(z[i]*z[j] for z in images) for j in range(3)] for i in range(3)]==[[H*PG[i][j]-PS[i][j] for j in range(3)] for i in range(3)],
                'all9 complete pendant diagonal/two-update identities')
        require([[F(1,2)*(i==j)-sum(images[i][k]*images[j][k]/bases[k] for k in range(3)) for j in range(2)] for i in range(2)]==f['pendant'],
                'all4 cancelled pendant Schur identities')
    grouped=control(q,r,l)
    return {'q':str(q),'r':r,'l':l,'tau':str(tau),'tauhat':str(f['tauhat']),
            'grouped':grouped,'triangle_update_positions':16,'triangle_Schur_positions':4,
            'anti_positions':4,'pendant_update_positions':9 if l>1 else 0,'pendant_Schur_positions':4 if l>1 else 0,
            'Gaussian5_inverse_checked':True,'final_Loewner_difference_rank':1}

def actual(n,r,l):
    row=compare(n,r,l,'cap-harmonic')
    family,C,W,p,*_=build(n,r,l,mean_recipe='cap-harmonic');N=p['N'];s=p['s']
    delta=F(row['whole']['delta']);private=[2*p['q']-1+2*i for i in range(p['m'])]
    repaired=[v[:] for v in C]
    for i in range(3):
        a,b=private[i],private[-1]
        require(not family[a+1]&family[b+1],'actual three repair pairs disjoint')
        repaired[a][b]+=delta;repaired[b][a]+=delta
    M=lift(repaired,s);L=[[(N-s)*M[i][j]+s*(i==j) for j in range(N)] for i in range(N)]
    kernels=[]
    for i in range(r):
        z=[F(bool(A&(1<<i)))-F(s,N) for A in family]
        require(matvec(L,z)==[F(0)]*N,'ALL actual centered maximum-star kernel coordinates')
        kernels.append(z)
    require(psd_rank([[dot(a,b) for b in kernels] for a in kernels])==r,'all independent actual maximum-star kernels')
    row['actual_maximum_star_kernels']=r
    row['full_original_positions_per_seed_or_repair']=N*N
    return row
