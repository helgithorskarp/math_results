"""Two fixed ORIGINAL matrix controls for the new inverse bound.

These literal n4/h2,h3 checks validate the physical translation only;
the unbounded statement uses the ordinary proof and coefficient certificate.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
import sys,json,time,signal,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,psd_rank,dot,matvec,unit,scale,vecadd,fingerprint,family_star
from linear import solve
from probe import construct,whole_lift
from check import model

def control(n,h):
    require((n,h) in ((4,2),(4,3)),'precisely two declared original controls')
    p,metric,frame,floor,Cseed,rows=construct(n,h)
    q,N,s=p['q'],p['N'],p['s'];Q=whole_lift(Cseed)
    P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    K=[[N*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
    gauge=[[K[i][j]+F(1,N) for j in range(N)] for i in range(N)]
    require(psd_rank(Q)==N-4 and psd_rank(gauge)==N,'whole original seed and inverse domain')
    first=2*q+6*h;u=vecadd(*(unit(N,i) for i in range(first,first+3)),scale(-3,unit(N,0)))
    v=vecadd(unit(N,N-1),scale(-1,unit(N,0)))
    require((sum(u),sum(v),dot(u,u),dot(v,v),dot(u,v))==(0,0,12,2,3),'whole original repair vectors including empty')
    iu,iv=solve(gauge,u),solve(gauge,v)
    require(sum(iu)==sum(iv)==0 and matvec(K,iu)==u and matvec(K,iv)==v,'EVERY original inverse equation')
    A,B,C=dot(u,iu),dot(v,iv),dot(u,iv)
    e=model(q,h);beta,nu,c=p['beta'],p['nu'],p['c'];theta=F(2*h-1,2*h)
    require(beta==e['beta'] and nu==e['nu'],'separately cleared primitive seed reconstruction')
    U=dot(u,matvec(Q,u));V=dot(v,matvec(Q,v))
    Uform=2*s*c*c*h/(3*(h-1))+9*theta*nu
    Vform=2*s*c*c*(2*h+9)/(27*(h-1))+beta+theta*nu
    require((U,V)==(Uform,Vform),'full ORIGINAL first Neumann energies')
    mean=nu/(2*h*(N-3*nu))
    require(C==(3-3*mean)/N,'original crossed inverse energy')
    require(A>0 and B>0 and A*B>C*C,'entire original inverse Gram positive')
    require(A>=F(12,N)+U/N**2>=e['a0']>0,'full original u inverse lower bound')
    require(B>=F(2,N)+V/N**2>=e['b0']>0,'full original v inverse lower bound')
    require(C>e['c0'] and e['comparison']>0 and e['nu_upper']==e['upper_gap']>0,'corrected bound and active-endpoint signs')
    kappa=e['kappa'];dL=6/kappa
    determinant=A*B-C*C;cap_det=1-2*dL*C-dL*dL*determinant
    require(cap_det<0,'entire original cap already indefinite at lower endpoint')
    cap=[[K[i][j]-dL*(u[i]*v[j]+v[i]*u[j]) for j in range(N)] for i in range(N)]
    Qend=[[Q[i][j]+dL*(u[i]*v[j]+v[i]*u[j]) for j in range(N)] for i in range(N)]
    L=[[1+z for z in row] for row in Qend]
    M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
    require(psd_rank(L)==N-3,'whole lower endpoint has the credited extra kernel')
    private=[];marked=[]
    for facet in range(2*h):
        masks=[1<<(n+2*facet),1<<(n+2*facet+1),3<<(n+2*facet)]
        private.extend(masks);marked.extend((1 if facet<h else 2)|a for a in masks)
    family=[0]+list(range(1,2**n))+marked+private
    require(len(family)==N and family_star(family)==s,'whole original downset and maximum star')
    for i in range(N):
        require(sum(M[i])==1,'every original row sum')
        for j in range(N):
            require(M[i][j]==M[j][i],'every original symmetric position')
            if family[i]&family[j]:require(M[i][j]==0,'every original intersection zero')
    require(Qend[0][0]==Q[0][0]+6*dL and all(Qend[i][i]==Q[i][i] for i in range(1,N)),'actual empty loop and every nonempty diagonal')
    for mark in (1,2):
        kernel=[F(bool(a&mark))-s/N for a in family]
        require(not any(matvec(L,kernel)),'both WHOLE original centered-star kernels')
    g00=A-2*dL*A*C;g01=C-dL*(A*B+C*C);g11=B-2*dL*B*C
    require(g00*g11-g01*g01==determinant*cap_det<0,'entire inverse-span negative determinant')
    if g00<0:negative=iu
    elif g00>0:negative=vecadd(scale(-g01/g00,iu),iv)
    else:
        require(g01!=0,'nonzero mixed negative form')
        t=-F(1 if g01>0 else -1)*(abs(g11)+1)/(2*abs(g01));negative=vecadd(scale(t,iu),iv)
    energy=dot(negative,matvec(cap,negative))
    require(sum(negative)==0 and energy<0,'EVERY original coordinate of the lower-endpoint negative cap witness')
    return {'n':n,'h':h,'q':q,'N':N,'original_positions':N*N,'original_inverse_equalities':2*N,'empty_retained':True,'all_support_rows_and_diagonals':True,'both_whole_star_kernels':True,'U':str(U),'V':str(V),'A':str(A),'B':str(B),'C':str(C),'a0':str(e['a0']),'b0':str(e['b0']),'c0':str(e['c0']),'comparison':str(e['comparison']),'dL':str(dL),'cap_determinant_at_dL':str(cap_det),'lower_rank_at_dL':N-3,'full_negative_cap_energy':str(energy),'negative_vector_sha256':fingerprint([negative]),'lower_endpoint_M_sha256':fingerprint(M),'scope':'Exact fixed control only; unbounded theorem is the ordinary proof and complete polynomial identities'}
def main():
    def alarm(a,b):raise TimeoutError('unchanged60s literal original controls')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    out=[control(4,2),control(4,3)];signal.alarm(0)
    work=Path(__file__).resolve().parent/'work';work.mkdir(exist_ok=True)
    (work/f'controls-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETE both whole original controls','cases':[[a['n'],a['h'],a['N']] for a in out],'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':sys.flags.optimize}),flush=True)
if __name__=='__main__':main()
