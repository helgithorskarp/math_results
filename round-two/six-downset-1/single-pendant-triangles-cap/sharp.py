"""Actual original-set repair using the conditional whole norm credited to9723."""
from fractions import Fraction as F
from builder import build,solve
from verify_original import compare
from exact import require,psd_rank,dot,matvec,lift,check,scale,fingerprint

def pair_data(N,private,last):
    u=[F(0)]*N;v=[F(0)]*N;u[0]=-3;v[0]=-1
    for i in private[:3]:u[i+1]=1
    v[last+1]=1
    require(dot(u,u)==12 and dot(v,v)==2 and dot(u,v)==3,'whole E0 pair Gram with actual empty')
    require(sum(u)==sum(v)==0,'whole pair orthogonal to1')
    return u,v

def repaired(n,r):
    old=compare(n,r,1,'cap-harmonic')
    family,C,W,p,*_=build(n,r,1,mean_recipe='cap-harmonic');N=p['N'];s=p['s'];m=p['m']
    require(all(sum(row)==0 for row in W),'balanced residual')
    require(psd_rank(W)==m-1,'all residual eigenvalues and sole kernel')
    A=[row[:-1] for row in W[:-1]];u0=[F(i<3) for i in range(m-1)]
    kappa=dot(u0,solve(A,u0));nu=p['mu']-p['a_mean']
    predicted=(r-1)/(r*nu)+9/p['etaP']
    require(kappa==predicted and kappa>0,'full deleted Gaussian versus spectral single-pendant inverse')
    delta=1/(4*(8+kappa));require(kappa*delta<F(1,4) and 8*delta<F(1,4),'both strict rational repair budgets')
    require(6*delta-kappa*delta*delta>0,'complete repaired residual Schur positive')
    private=[2*p['q']-1+2*i for i in range(m)];last=private[-1]
    sharp=[row[:] for row in C];RW=[row[:] for row in W]
    for i in range(3):
        a=private[i];require(not family[a+1]&family[last+1],'all3 actual repair pairs free')
        sharp[a][last]+=delta;sharp[last][a]+=delta;RW[i][-1]+=delta;RW[-1][i]+=delta
    require(psd_rank(RW)==m,'complete repaired residual PD')
    M=lift(sharp,s);status=check(family,M,s)
    require(status['lower_rank']==N-r and status['upper_rank']==N-1,'both entire greatest endpoint ranks')
    seedM=lift(C,s)
    difference=[[(N-s)*(M[i][j]-seedM[i][j]) for j in range(N)] for i in range(N)]
    u,v=pair_data(N,private,last)
    require(difference==[[delta*(u[i]*v[j]+v[i]*u[j]) for j in range(N)] for i in range(N)],'ALL whole repair positions including empty row and loop')
    Q=[[(N-s)*M[i][j]+s*(i==j)-1 for j in range(N)] for i in range(N)]
    bound=1-8*delta
    gap=[[(N-bound)*((i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(gap)==N-1 and bound>F(3,4),'complete actual cap with stronger rational floor')
    L=[[(N-s)*M[i][j]+s*(i==j) for j in range(N)] for i in range(N)]
    stars=[]
    for j in range(r):
        z=[F(bool(A&(1<<j)))-F(s,N) for A in family]
        require(matvec(L,z)==[F(0)]*N,'ALL actual centered maximum-star coordinates')
        stars.append(z)
    require(psd_rank([[dot(a,b) for b in stars] for a in stars])==r,'all forced stars independent')
    return {'n':n,'r':r,'l':1,'q':p['q'],'N':N,'old_complete_correspondence':old,
            'sharp_delta':str(delta),'kappa':str(kappa),'actual_cap_floor':str(bound),'whole_pair_Gram':['12','3','2'],
            'whole_repair_identity_positions':N*N,'whole_cap_positions':N*N,'actual_star_kernels':r,
            'sharp_matrix_sha256':fingerprint(M),'status':status,'independent_review':False,'formalization':False}
