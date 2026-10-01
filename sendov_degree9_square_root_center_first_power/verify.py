"""six-sendov-1, researcher: exact evidence for a written analytic proof.

Python3.11+, standard library only. No imported campaign program or
floating proof input. Full coefficient dictionaries and expected records
are compared; explicit exceptions remain active under -O.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import comb, prod
import json, hashlib, copy

ROOT=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ArithmeticError(message)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class Ring:
    def __init__(self,n):self.n=n;self.zero=(0,)*n;self.one={self.zero:F(1)}
    def v(self,i):
        e=list(self.zero);e[i]=1;return {tuple(e):F(1)}
    def add(self,*ps):
        out=defaultdict(F)
        for p in ps:
            for e,v in p.items():out[e]+=v
        return {e:v for e,v in out.items() if v}
    def scale(self,p,v):return {e:c*v for e,c in p.items() if c*v}
    def mul(self,p,q):
        out=defaultdict(F)
        for e,v in p.items():
            for f,w in q.items():out[tuple(a+b for a,b in zip(e,f))]+=v*w
        return {e:v for e,v in out.items() if v}
    def power(self,p,k):
        out=self.one
        for _ in range(k):out=self.mul(out,p)
        return out
    def canonical(self,p):return [[list(e),str(v)] for e,v in sorted(p.items())]
    def integral(self,p):return sum(v/prod(i+1 for i in e) for e,v in p.items())

def symbolic():
    Q=Ring(10);a,ai,b,bi,c,ci,s,opening,z,w=[Q.v(i) for i in range(10)]
    add=lambda *ps:tuple(Q.add(*(p[i] for p in ps)) for i in range(2))
    scale=lambda p,v:tuple(Q.scale(x,v) for x in p)
    real=lambda p,v:tuple(Q.mul(x,v) for x in p)
    conj=lambda p:(p[0],Q.scale(p[1],-1))
    mul=lambda p,q:(Q.add(Q.mul(p[0],q[0]),Q.scale(Q.mul(p[1],q[1]),-1)),
                    Q.add(Q.mul(p[0],q[1]),Q.mul(p[1],q[0])))
    AA,BB,CC=(a,ai),(b,bi),(c,ci);s2=Q.power(s,2);sc=Q.mul(s,opening)
    I0=add(AA,real(BB,Q.scale(sc,-2)),real(CC,s2))
    D0=add(real(BB,Q.scale(sc,-2)),real(CC,Q.scale(Q.mul(s2,z),2)))
    Iq=add(AA,real(mul((z,w),BB),Q.scale(sc,-2)),real(mul(mul((z,w),(z,w)),CC),s2))
    h2=Q.scale(Q.add(Q.one,Q.scale(z,-1)),2)
    even=real(add(real(BB,sc),real(CC,Q.scale(Q.mul(s2,Q.add(Q.one,z)),-1))),h2)
    odd=real(mul(({},Q.one),D0),w)
    def reduce(p):
        out={}
        for e,v in p.items():
            f=list(e);k=f[9]//2;f[9]%=2
            basis=Q.power(Q.add(Q.one,Q.scale(Q.power(z,2),-1)),k)
            out=Q.add(out,{tuple(a+b for a,b in zip(f,j)):v*c for j,c in basis.items()})
        return out
    delta=tuple(reduce(p) for p in add(Iq,scale(I0,-1)))
    require(delta==add(even,odd),'Complete unit-circle phase decomposition failed')
    skew=mul(I0,conj(D0))[1]
    AB,AC,BC=mul(AA,conj(BB))[1],mul(AA,conj(CC))[1],mul(BB,conj(CC))[1]
    rhs=Q.add(Q.scale(Q.mul(sc,AB),-2),Q.scale(Q.mul(Q.mul(s2,z),AC),2),
              Q.scale(Q.mul(Q.mul(Q.power(s,3),opening),Q.mul(Q.add(Q.one,Q.scale(z,-2)),BC)),2))
    require(skew==rhs,'Complete three-moment skew identity failed')
    # Full sixth-power difference, independently as binomial polynomials.
    T=Ring(2);xr,xi=T.v(0),T.v(1)
    tmul=lambda p,q:(T.add(T.mul(p[0],q[0]),T.scale(T.mul(p[1],q[1]),-1)),
                    T.add(T.mul(p[0],q[1]),T.mul(p[1],q[0])))
    tp=lambda p,k:__import__('functools').reduce(tmul,[p]*k,(T.one,{}))
    Z=(xr,xi);Zbar=(xr,T.scale(xi,-1));lhs=tp(Z,6)
    lhs=(T.add(lhs[0],T.scale(tp(Zbar,6)[0],-1)),T.add(lhs[1],T.scale(tp(Zbar,6)[1],-1)))
    pieces=[tmul(tp(Z,5-j),tp(Zbar,j)) for j in range(6)]
    total=tuple(T.add(*(p[i] for p in pieces)) for i in range(2))
    require(lhs==tmul(({},T.scale(xi,2)),total),'Complete sixth-power telescoping failed')
    return {'phase_component_terms':[len(p) for p in delta],
            'phase_components_sha256':digest([Q.canonical(p) for p in delta]),
            'skew_terms':len(skew),'skew_sha256':digest(Q.canonical(skew)),
            'sixth_power_difference_sha256':digest([T.canonical(p) for p in lhs])}

def exact_constants():
    Q=Ring(2);tau,sigma=Q.v(0),Q.v(1);difference=Q.add(tau,Q.scale(sigma,-1))
    weight0=Q.power(difference,2)
    weights=[weight0,Q.mul(weight0,Q.add(tau,sigma)),Q.mul(weight0,Q.mul(tau,sigma))]
    values=[Q.integral(p) for p in weights]
    require(values==[F(1,6),F(1,6),F(1,36)],'Antisymmetric weight integrals failed')
    moment_constants=[243*v for v in values]
    require(moment_constants==[F(81,2),F(81,2),F(27,4)],'Moment-product constants failed')
    M=F(7,6);s=F(5,2)
    skew=81*s+81*s*s+F(27,2)*s**3
    Icap=9+9*s+3*s*s;Ecap=F(9,2)*s+6*s*s
    require((skew,Icap,Ecap)==(F(14715,16),F(201,4),F(195,4)),'Moment caps failed')
    linear=4*skew*M**10;quadratic=2*Icap*Ecap*M**12
    require(linear==F(153949010705,8957952)<18000,'Square-root loss comparison failed')
    require(quadratic==F(60278805760355,1934917632)<32000,'Quadratic loss comparison failed')
    tube_loss=F(18000,40000)+F(32000,40000**2)
    require(tube_loss==F(22501,50000)<F(1,2),'Tube half-surplus failed')
    require(F(28,9)<4,'Heavy imaginary budget comparison failed')
    return {'weight_integrals':list(map(str,values)),
            'weights_sha256':digest([Q.canonical(p) for p in weights]),
            'moment_skew_constants':list(map(str,moment_constants)),
            'skew_cap':str(skew),'moment_caps':list(map(str,[Icap,Ecap])),
            'exact_linear_loss':str(linear),'exact_quadratic_loss':str(quadratic),
            'tube_loss':str(tube_loss),'tube_constant':40000,'surplus':'(1-b)/2'}

def ga(p,q):return p[0]+q[0],p[1]+q[1]
def gs(p,v):return p[0]*v,p[1]*v
def gc(p):return p[0],-p[1]
def gm(p,q):return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]
def gn(p):return p[0]*p[0]+p[1]*p[1]
def gi(p):return gs(gc(p),1/gn(p))
def gp(p,k):
    out=F(1),F(0)
    for _ in range(k):out=gm(out,p)
    return out
def gsum(ps):
    out=F(0),F(0)
    for p in ps:out=ga(out,p)
    return out
def unit(k):return (1-k*k)/(1+k*k),2*k/(1+k*k)
def moments(b,U):
    return [gsum(gs(gp(U,j),F(9*(-1)**j*comb(6,j),j+l+1)*b**(j+l)) for j in range(7)) for l in range(3)]
def phase(A,B,C,s,c,q):return gsum([A,gs(gm(q,B),-2*s*c),gs(gm(gp(q,2),C),s*s)])

def gaussian_controls():
    M=F(7,6);rows=[];nonreal=shifted=farther=opened=0
    for b in [F(0),F(1,4),F(1,2),F(9,10),F(1)]:
     for r in [F(3,4),F(1),F(17,16),F(7,6)]:
      s=4-3*r
      if min(r,s)<1/(1+b):continue
      for heavy_k in [F(0),F(-1,100),F(1,100),F(-1,5),F(1,5)]:
       U=gs(unit(heavy_k),r);x,Y=U
       if gn(ga((b,0),gs(gi(U),-1)))>1:continue
       A,B,C=moments(b,U)
       for opening_k in [F(0),F(1,5),F(1,2),F(1)]:
        c=unit(opening_k)[0]
        I0=phase(A,B,C,s,c,(F(1),F(0)))
        for center_k in [F(0),F(-1,500000),F(1,500000),F(-1,1000000),F(1,1000000)]:
            q=unit(center_k);z,W=q;h2=gn(ga(q,(F(-1),F(0))));eps=1-b
            if (3*x+s*c*z)/4<b or h2>eps/40000**2:continue
            require(Y*Y<=F(28,9)*eps,'Gaussian heavy budget failed')
            for P,Q,bound in [(A,B,F(81,2)*b*b),(A,C,F(81,2)*b**3),(B,C,F(27,4)*b**4)]:
                require(gm(P,gc(Q))[1]**2<=(bound*abs(Y)*M**10)**2,'Gaussian moment-product bound failed')
            actual=phase(A,B,C,s,c,q);R=r**12*s**4
            require(gn(I0)>=R+eps and gn(actual)>=R+eps/2,'Gaussian tube surplus failed')
            E=gs(gsum([gs(B,s*c),gs(C,-s*s*(1+z))]),h2)
            D=gsum([gs(B,-2*s*c),gs(C,2*s*s*z)])
            require(ga(I0,ga(E,gm((F(0),W),D)))==actual,'Gaussian phase identity failed')
            loss=gn(I0)-gn(actual)-F(39195,8)*M**12*h2
            if loss>0:
                require(loss**2<=(F(14715,8)*abs(Y)*M**10)**2*h2,'Gaussian squared loss bound failed')
            nonreal+=Y!=0;shifted+=center_k!=0;farther+=r<1;opened+=c<1
            rows.append(list(map(str,[b,r,x,Y,c,*q,gn(I0),gn(actual)])))
    require(len(rows)>100 and nonreal>20 and shifted>20 and farther>0,'Insufficient analytic controls')
    return {'count':len(rows),'nonreal_heavy':nonreal,'shifted':shifted,'farther_heavy':farther,
            'opened':opened,'all_records_sha256':digest(rows)}

def validate_center(v,w,q):
    require(gn(v)==gn(w)==gn(q)==1,'Nonunit center input')
    total=ga(v,w);projection=gm(total,gc(q))
    require(gn(total)>0 and projection[1]==0 and projection[0]>0,'Undefined or incorrect short center')

def product_poly(roots):
    out=[(F(1),F(0))]
    for r in roots:
        new=[(F(0),F(0)) for _ in range(len(out)+1)]
        for j,p in enumerate(out):
            new[j]=ga(new[j],gs(gm(p,r),-1));new[j+1]=ga(new[j+1],p)
        out=new
    return out
def value(poly,z):
    out=F(0),F(0)
    for p in reversed(poly):out=ga(gm(out,z),p)
    return out
def integrate_factors(points,constant,linear,scale=F(1)):
    out=[(F(1),F(0))]
    for p in points:
        nxt=[(F(0),F(0)) for _ in range(len(out)+1)]
        for j,x in enumerate(out):
            nxt[j]=ga(nxt[j],gs(x,constant));nxt[j+1]=ga(nxt[j+1],gm(x,gs(p,linear)))
        out=nxt
    return gsum(gs(x,scale/F(j+1)) for j,x in enumerate(out))

def actual_example():
    a=F(1,2);k=F(1,160000);q=unit(k);v=gm(q,(F(3,5),F(4,5)));w=gm(q,(F(3,5),F(-4,5)))
    H=(a,F(1,100));L1=ga((a,0),gs(gc(v),F(-1,50)));L2=ga((a,0),gs(gc(w),F(-1,50)))
    actual_v=gs(gi(ga((a,0),gs(L1,-1))),F(1,50))
    actual_w=gs(gi(ga((a,0),gs(L2,-1))),F(1,50))
    require((actual_v,actual_w)==(v,w),'Original unit reciprocals differ')
    validate_center(actual_v,actual_w,q)
    require(ga(v,w)==gs(q,F(6,5)) and L2!=gc(L1),'Example actual short-center/nonreflection fails')
    chord2=gn(ga(q,(F(-1),0)))
    require(chord2==F(4,25600000001) and ((1-a)/80000)**2<chord2<=(1-a)/40000**2,
            'Example does not enlarge previous tube')
    require(gi(ga((a,0),gs(H,-1)))[0]==0<a*(4+3*a)/(3+4*a),'Example fails to leave old heavy cone')
    points=[H]*6+[L1,L2];offsets=[ga(p,(-a,0)) for p in points]
    dp_center=[gs(x,9) for x in product_poly(offsets)]
    centered=[(F(0),F(0))]+[gs(x,F(1,j+1)) for j,x in enumerate(dp_center)]
    p=[(F(0),F(0)) for _ in range(10)]
    for j,c in enumerate(centered):
        for l in range(j+1):p[l]=ga(p[l],gs(c,comb(j,l)*(-a)**(j-l)))
    dp=[gs(p[j+1],j+1) for j in range(9)]
    require(dp==[gs(x,9) for x in product_poly(points)] and value(p,(a,0))==(0,0),
            'Complete original derivative/marked polynomial fails')
    require(p[-1]==(1,0) and any(co[1] for co in p),'Nonreal monic example fails')
    require(all(gn(x)==F(1,100)**2 for x in offsets[:6]) and all(gn(x)==F(1,50)**2 for x in offsets[6:]),
            'Centered critical magnitudes fail')
    major=[F(1)]
    for radius in [F(1,100)]*6+[F(1,50)]*2:
        nxt=[F(0)]*(len(major)+1)
        for j,c in enumerate(major):nxt[j]+=c*radius;nxt[j+1]+=c
        major=nxt
    require(all(gn(dp_center[j])<=(9*major[j])**2 for j in range(9)),
            'Complete derivative coefficient majorant fails')
    radius=F(1,4);tail=sum(9*major[j]*radius**(j+1)/F(j+1) for j in range(8))
    require(tail<radius**9 and a+radius<1,'Exact Rouche majorant failed')
    communication=[]
    for m in [F(1,2),F(3,4),F(1)]:
        b=m*a;pm=[gs(c,m**(9-j)) for j,c in enumerate(p)];dpm=[gs(pm[j+1],j+1) for j in range(9)]
        recip=[gi(ga((b,0),gs(P,-m))) for P in points]
        origin=integrate_factors(recip,F(1),-b,F(9));recprod=gp(recip[0],6)
        recprod=gm(recprod,gm(recip[6],recip[7]))
        require(origin==gs(gm(pm[0],recprod),-1/b),'Full actual origin communication fails')
        norm=gn(origin)/prod(gn(x) for x in recip)
        require(norm==m**16*gn(p[0])/(a*a),'Actual m16 normalization fails')
        polar=integrate_factors(recip,b,1-b*b)
        target=gs(gm(value(pm,(1/b,0)),gi(value(dpm,(b,0)))),b**9/(1-b*b))
        require(polar==target and gn(polar)>=1,'Full actual polar communication fails')
        communication.append(list(map(str,[m,b,norm,*polar])))
    invalid=0
    for vbad,wbad,qbad in [(gm(q,(0,1)),gm(q,(0,-1)),q),(v,w,gs(q,-1))]:
        try:validate_center(vbad,wbad,qbad)
        except ArithmeticError:invalid+=1
        else:raise ArithmeticError('Invalid mathematical center control accepted')
    require(invalid==2,'Invalid mathematical center controls missing')
    return {'a':str(a),'H':list(map(str,H)),'L1':list(map(str,L1)),'L2':list(map(str,L2)),
            'center':list(map(str,q)),'light_opening_cosine':'3/5','unit_sum_norm_squared':'36/25',
            'center_chord_squared':str(chord2),'previous_tube_squared':str(((1-a)/80000)**2),
            'new_tube_squared':str((1-a)/40000**2),'rouche_radius':str(radius),
            'rouche_tail_majorant':str(tail),'rouche_leading_bound':str(radius**9),
            'polynomial_coefficients_sha256':digest([[str(x),str(y)] for x,y in p]),
            'communication_scalings':len(communication),'communication_sha256':digest(communication),
            'rejected_invalid_center_controls':invalid}

def compute():
    return {'result':'PASS','author':'six-sendov-1','role':'researcher','symbolic':symbolic(),
            'constants':exact_constants(),'gaussian_controls':gaussian_controls(),'actual_example':actual_example()}
def validate(fresh,fixture):require(fixture==fresh,'Compact exact evidence mismatch')
def corruptions(fresh):
    paths=[('symbolic','skew_sha256'),('symbolic','phase_components_sha256'),
           ('constants','weight_integrals'),('constants','tube_constant'),
           ('gaussian_controls','all_records_sha256'),('actual_example','unit_sum_norm_squared'),
           ('actual_example','rouche_tail_majorant'),('actual_example','rejected_invalid_center_controls')]
    rejected=0
    for first,second in paths:
        bad=copy.deepcopy(fresh);bad[first][second]='incorrect'
        try:validate(fresh,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Altered compact record accepted')
    require(rejected==len(paths),'Altered record inventory failed');return rejected
def main():
    fresh=compute();validate(fresh,json.loads((ROOT/'expected.json').read_text()))
    print(json.dumps({**fresh,'rejected_altered_records':corruptions(fresh)},sort_keys=True,indent=2))
if __name__=='__main__':main()
