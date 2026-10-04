"""Fresh actual full reciprocal-distance scalar, two complete exact routes."""
from pathlib import Path
import sys,json,signal,time,resource,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as Q
from field import E,C,need
from series import *
from family import family
def invsqrt(s,n):
    out=sj(1,n);power=sj(1,n);h=sa(s,sj(-1,n),n=n);co=Q(1)
    need(not h[0],'positive branch constant one')
    for k in range(1,n//2+1):
        power=sm(power,h,n);co*=Q(-(2*k-1),2*k);out=sa(out,ss(power,co),n=n)
    need(sm(sm(out,out,n),s,n)==sj(1,n),'complete binomial inverse-square-root equation')
    return out
def inverse_square_branch(s,n):
    out=sj(1,n)
    for j in range(1,n+1):out[j]=ps(sm(sm(out,out,j),s,j)[j],-Q(1,2))
    need(sm(sm(out,out,n),s,n)==sj(1,n),'complete recurrence positive branch equation')
    return out
def run(tau=0):
    n=11;v,A,B,K=family(tau,n);H=v['H'];anchor=sj(1,n);anchor[2]=pc(-1)
    ga=sa(anchor,ss(A,-1),n=n);gb=sa(anchor,ss(B,-1),n=n)
    VA=sm(ga,conj(ga),n);VB=sa(sm(gb,conj(gb),n),[{},{}]+ss(sm(K,conj(K),n),H/2)[:n-1],n=n)
    r=sm(gb,conj(K),n);real=ss(sa(r,conj(r),n=n),Q(1,2));X2=[{},{}]+ss(sm(real,real,n),2*H)[:n-1]
    need(X2[:8]==[{}]*8,'whole actual pair square starts at degree eight')
    U=inverse_square_branch(VA,n);R=inverse_square_branch(sa(sm(VB,VB,n),ss(X2,-1),n=n),n)
    target=sa(ss(sm(VB,sm(R,R,n),n),2),ss(R,2),n=n);S=sj(2,n)
    for j in range(1,n+1):S[j]=ps(pa(target[j],ps(sm(S,S,j)[j],-1)),Q(1,4))
    need(sm(S,S,n)==target,'complete positive pair scalar equation')
    F=sa(ss(U,6),S,n=n)
    direct=sa(ss(invsqrt(VA,n),6),ss(invsqrt(VB,n),2),ss(sm(X2,sa(sj(1,n),ss(sa(VB,sj(-1,n),n=n),-Q(5,2)),n=n),n),Q(3,4)),n=n)
    need(F==direct,'all complete physical scalar routes agree')
    f5=[E(Q(46162779724939271,69657034752))+Q(36338752485008003,11609505792)*C-Q(11846579474774765,2902376448)*C*C,
        E(Q(932974693,279936))+Q(6209560805,279936)*C-Q(1933889279,69984)*C*C,
        -E(Q(809,54))-Q(3545,54)*C+Q(166,3)*C*C]
    P0=E(Q(134807893,18289152))+Q(57634811,4064256)*C+Q(159762149,18289152)*C*C
    P1=E(Q(241,1764))+Q(331,882)*C+Q(233,882)*C*C
    fifth=pa({(j,0):x for j,x in enumerate(f5)},pc(8*tau),{(0,2):P0,(1,2):P1})
    fourth=pa(pc(v['Gstar']),ps(MU,v['L']),ps(pp(MU,2),Q(4,3)),ps(pp(T,2),v['kappa']/H))
    wanted=[{}]*12
    for j,x in [(0,pc(8)),(2,pc(E(Q(8,3))+v['y'])),(4,pc(v['Bstar'])),(6,pc(v['Tstar'])),(8,fourth),(10,fifth)]:wanted[j]=x
    need(F==wanted,'entire actual mixed physical cost and every monomial cancellation')
    ImA=ss(sa(A,ss(conj(A),-1),n=n),1/(2*__import__('field').I));ImB=ss(sa(B,ss(conj(B),-1),n=n),1/(2*__import__('field').I));ImK=ss(sa(K,ss(conj(K),-1),n=n),1/(2*__import__('field').I))
    moment=sa(ss(sp(ImA,3,n),6),ss(sp(ImB,3,n),2),[{},{}]+ss(sm(ImB,sm(ImK,ImK,n),n),3*H)[:n-1],n=n)
    U7=2*v['gamma']+3*H*v['k']/7
    need(moment[:5]==[{}]*5 and moment[5]==T and moment[6]=={} and moment[7]==ps(T,U7) and moment[8]=={},'complete actual cubic imaginary moment through degree eight')
    return {'tau':tau,'VA':record(VA),'VB':record(VB),'X2':record(X2),'U':record(U),'R':record(R),'S':record(S),'F':record(F),'entire_actual_cubic_imaginary_moment':record(moment),'P0':P0.record(),'P1':P1.record(),'all_complete_scalar_equations_and_cost_paid':True}
if __name__=='__main__':
    signal.alarm(45);start=time.monotonic();rec=run(int(sys.argv[1]));raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode();Path(sys.argv[2]).write_bytes(raw)
    print(json.dumps({'tau':rec['tau'],'whole_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
