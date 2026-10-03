"""Literal sets and fresh abstract Gram; no producer inputs."""
import argparse,hashlib,json,pathlib,sys
from fractions import Fraction as F
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from canonical import Mat,K

def need(ok,why):
    if not ok:raise ValueError(why)

def psd_rank(matrix):
    a=[list(map(lambda x:F(str(x)),row)) for row in matrix.tolist()];rank=0
    while a:
        for i in range(len(a)):
            need(a[i][i]>=0,'negative PSD pivot')
        p=max(range(len(a)),key=lambda i:a[i][i]);t=a[p][p]
        if not t:
            need(not any(x for row in a for x in row),'zero-diagonal nonzero PSD remainder');break
        rest=[i for i in range(len(a)) if i!=p]
        a=[[a[i][j]-a[i][p]*a[p][j]/t for j in rest] for i in rest];rank+=1
    return rank

def run(n,h,damage=None):
    need(3<=n<=6 and 2<=h and 2**n+6*h+6<=80,'literal guard')
    q=F(2**(n-1));h=F(h);s=q+3*h;d=3*h;ell=3*h+4;hh=int(h);w=s-1;N=int(2*q+6*h+6)
    oldsets=list(range(1,2**n));m=len(oldsets);p=hh+1
    ib=m;iy=ib+hh;it=iy+1;im=it+3*p;iwa=im+p;iwf=iwa+p;dim=iwf+p
    def v(pairs):
        out=Mat(dim,1)
        for i,x in pairs.items():out[i]=x
        return out
    old=[v({i:1}) for i in range(m)]
    G=sum(old,Mat(dim,1));Hx=-sum((old[i] for i,A in enumerate(oldsets) if A&1),Mat(dim,1));Hy=-sum((old[i] for i,A in enumerate(oldsets) if A&2),Mat(dim,1))
    hx=Hx/d;hy=Hy/d;Y=v({iy:1});rho=(q-1)/(s-4);E=hx-rho*(hy+Y)
    KK=G+Hx+Hy/h+3*Y;e2=q/(3*h)+rho*rho*(s-3)/3;c0=(ell*q+6*h-16)/(ell*ell)
    FF=(q-8)/(ell*rho*(s-3));AA=FF/(2*h);cL=-4*(q-8)/(ell*s)
    b=3*h*(q-ell-1)/(ell*s*(h-1));a=-b/2;cH=-9*(q-ell-1)/(2*ell*s)+AA*q/(h*s);b2=s*(h-1)/(3*h)
    eHL=w-c0-AA*AA*e2-a*a*b2-2*s*cH*cH/3
    eHF=w-c0-b*b*b2-2*s*cH*cH/(3*(h-1))-2*s*cL*cL/(3*h*h)
    eLL=w-c0-FF*FF*e2-2*s*cL*cL/3;eLF=w-c0-9*FF*FF*e2
    rH=-1-c0-a*b*b2;rL=-1-c0+3*FF*FF*e2
    muH=(2*rH+eHF)/3;muL=(2*rL+eLF)/3
    alH=2*(2*eHL-rH-eHF);beH=eHF-muH;alL=2*(2*eLL-rL-eLF);beL=eLF-muL
    nu=(h*muH-muL/h)/(h-1)
    need(min(alH,beH,alL,beL,nu,muL)>0,'literal scalar signs')
    metric=Mat(dim)
    for i,A in enumerate(oldsets):
        for j,B in enumerate(oldsets):metric[i,j]=s*(i==j)+(q-d)*(A^B==2**n-1)-1
    if damage=='whole-ground-complement':
        for i,A in enumerate(oldsets):
            for j,B in enumerate(oldsets):metric[i,j]=s*(i==j)-1
    for i in range(hh):
        for j in range(hh):metric[ib+i,ib+j]=s/3*((i==j)-1/h)
    metric[iy,iy]=b2
    for i in range(p):
        for a0 in range(3):
            for b0 in range(3):metric[it+3*i+a0,it+3*i+b0]=s*((a0==b0)-F(1,3))
        metric[iwa+i,iwa+i]=alH if i<hh else alL
        metric[iwf+i,iwf+i]=beH if i<hh else beL
        for j in range(p):
            metric[im+i,im+j]=(muH if i==j else (muL/h-muH)/(h-1)) if i<hh and j<hh else (muL if i==j else -muL/h)
    rows=list(old);sets=list(oldsets);private=[];marked=[]
    for i in range(p):
        ti=[v({it+3*i+j:1}) for j in range(3)];mi=v({im+i:1});wa=v({iwa+i:1});wf=v({iwf+i:1})
        if i<hh:
            Bi=v({ib+i:1});vv=[hx+Bi+t for t in ti]
            pp=[-KK/ell+AA*E+a*Bi+cH*ti[1],-KK/ell+AA*E+a*Bi+cH*ti[0],-KK/ell+b*Bi+cH/(h-1)*sum((v({it+3*j+2:1}) for j in range(hh) if j!=i),Mat(dim,1))+cL/h*v({it+3*hh+2:1})]
        else:
            vv=[hy+Y+t for t in ti];pp=[-KK/ell+FF*E+cL*ti[1],-KK/ell+FF*E+cL*ti[0],-KK/ell-3*FF*E]
        ww=[mi+(wa-wf)/2,mi+(-wa-wf)/2,mi+wf];uu=[pp[j]+ww[j] for j in range(3)]
        u=1<<(n+2*i);vbit=1<<(n+2*i+1);z=1 if i<hh else 2
        marked.append(list(range(len(rows),len(rows)+3)));rows+=vv;sets += [z|u,z|vbit,z|u|vbit]
        private.append(list(range(len(rows),len(rows)+3)));rows+=uu;sets += [u,vbit,u|vbit]
    need(len(rows)==N-1 and len(set(sets))==N-1,'literal census')
    Crows=Mat(len(rows),dim,[[r[j] for j in range(dim)] for r in rows])
    C=Crows*metric*Crows.T
    need(all(C[i,i]==K(w) for i in range(N-1)),'all literal norms')
    mandatory=0
    for i,A in enumerate(sets):
        for j,B in enumerate(sets):
            if i!=j and A&B:need(C[i,j]==-1,'literal mandatory intersection');mandatory+=1
    total=sum(rows,Mat(dim,1));need(all(x==0 for x in metric*(total-KK/ell)),'literal total and actual empty')
    def lift(C):
        E0=Mat(N,N-1)
        for i in range(N-1):E0[0,i]=-1;E0[i+1,i]=1
        return E0*C*E0.T
    Q=lift(C);need(all(sum(row)==0 for row in Q.tolist()),'actual empty row sums')
    seedrank=psd_rank(C);need(seedrank==N-3,'seed core rank')
    kappa=(h-1)/(h*nu)+1/muL+4/beL;delta=1/(4*(8+kappa))
    CC=Mat(N-1,N-1,[list(row) for row in C.tolist()]);j=private[-1][2]
    for i in private[0]:need(not (sets[i]&sets[j]),'repair support');CC[i,j]+=delta;CC[j,i]+=delta
    Q1=lift(CC)
    if damage=='old-empty-retention':
        for i in range(N):Q1[0,i]=Q[0,i];Q1[i,0]=Q[i,0]
    need(all(sum(row)==0 for row in Q1.tolist()),'recomputed repaired empty')
    need(psd_rank(CC)==N-2,'repaired core rank')
    M=Mat(N)
    for i in range(N):
        for j in range(N):M[i,j]=(Q1[i,j]+1-s*(i==j))/(N-s)
    allsets=[0]+sets
    for i,A in enumerate(allsets):
        need(sum(M.tolist()[i])==1,'original M row sum')
        for j,B in enumerate(allsets):
            if A&B:need(M[i,j]==0,'original M support')
    cap=Mat(N-1)
    for i in range(N-1):
        for j in range(N-1):cap[i,j]=N*(i==j)-1-CC[i,j]
    need(psd_rank(cap)==N-1,'full cap rank')
    stars=[sum(bool(A&(1<<i)) for A in allsets) for i in range(n+2*p)]
    need(stars[0]==s and max(stars[1:])<s,'unique heavy largest star')
    for i in range(N-1):need(sum(CC[i,j] for j,A in enumerate(sets) if A&1)==0,'exact core star kernel')
    return dict(n=n,h=hh,N=N,mandatory_ordered_pairs=mandatory,seed_rank=seedrank,repaired_core_rank=N-2,cap_rank=N-1,
                vertices=allsets,seed=[[str(x) for x in row] for row in C.tolist()],repaired_M=[[str(x) for x in row] for row in M.tolist()],kappa=str(kappa),delta=str(delta))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('n',type=int);ap.add_argument('h',type=int);ap.add_argument('--damage');a=ap.parse_args()
    print(json.dumps(run(a.n,a.h,a.damage),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
