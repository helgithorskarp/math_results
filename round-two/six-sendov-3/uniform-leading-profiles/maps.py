"""Whole generic moment, root, normal, objective and closing maps.

Actual six-sendov-3 / researcher. Ordinary proof corroboration, not
independent review. Exact kernel credited to9671/10006; generic literal
eight-factor expansion and fourth cost credited to8619/8684. No samples.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import F,N0,N1,NW,na,ns,nm,np,ni,nc,need,canonical,sha256
from functools import lru_cache

ORDER=4
NV=7 # J3,J4,M,b,G,sigma,one generic profile coordinate V
ZERO=(0,)*NV
FZERO=(N0,N0); FONE=(N1,N0); FI=(N0,N1)
@lru_cache(maxsize=8192)
def fm(a,b):
    return N0 if a==N0 or b==N0 else nm(a,b)
@lru_cache(maxsize=8192)
def fc(a):return nc(a)
def ca(*zs):return (na(*(z[0] for z in zs)),na(*(z[1] for z in zs)))
def cs(z,q):return (ns(z[0],q),ns(z[1],q))
def cm(z,u):return (na(fm(z[0],u[0]),ns(fm(z[1],u[1]),-1)),na(fm(z[0],u[1]),fm(z[1],u[0])))
def cc(z):return (fc(z[0]),ns(fc(z[1]),-1))
def cf(q):return (ns(N1,F(q)),N0)
def cr(q):return (q,N0)
def fp(z,n):
    out=FONE
    for _ in range(n):out=cm(out,z)
    return out
def pc(z):return {} if z==FZERO else {ZERO:z}
def pv(j):
    exp=list(ZERO);exp[j]=1
    return {tuple(exp):FONE}
def pa(*ps):
    out={}
    for p in ps:
        for e,z in p.items():out[e]=ca(out.get(e,FZERO),z)
    return {e:z for e,z in out.items() if z!=FZERO}
def ps(p,q):return {e:u for e,z in p.items() if (u:=cs(z,q))!=FZERO}
def pm(p,q):
    out={}
    for e,z in p.items():
        for f,u in q.items():
            g=tuple(a+b for a,b in zip(e,f));out[g]=ca(out.get(g,FZERO),cm(z,u))
    return {e:z for e,z in out.items() if z!=FZERO}
def pp(p,n):
    out=pc(FONE)
    for _ in range(n):out=pm(out,p)
    return out
def pconj(p):return {e:cc(z) for e,z in p.items()}
def psub(p,j,image):
    out={}
    for e,z in p.items():
        f=list(e);power=f[j];f[j]=0
        out=pa(out,pm({tuple(f):z},pp(image,power)))
    return out
def pdiff(p,j):
    out={}
    for e,z in p.items():
        if e[j]:
            f=list(e);f[j]-=1;out[tuple(f)]=cs(z,e[j])
    return out
def peval(p,replacements):
    for j,image in replacements.items():p=psub(p,j,image)
    return p
def pfield(p,q):return pm(p,pc(cr(q)))
def pscalar(p,label):
    need(set(p)<={ZERO},label+' scalar map')
    return p.get(ZERO,FZERO)
def realfield(z,label):
    need(z[1]==N0 and fc(z[0])==z[0],label+' real field')
    return z[0]
def sc(z):return {0:pc(z)} if z!=FZERO else {}
def sa(*ss):
    out={}
    for s in ss:
        for j,p in s.items():out[j]=pa(out.get(j,{}),p)
    return {j:p for j,p in out.items() if p}
def ss(s,q):return {j:u for j,p in s.items() if (u:=ps(p,q))}
def sm(s,t):
    out={}
    for j,p in s.items():
        for k,q in t.items():
            if j+k<=ORDER:out[j+k]=pa(out.get(j+k,{}),pm(p,q))
    return {j:p for j,p in out.items() if p}
def sp(s,n):
    out=sc(FONE)
    for _ in range(n):out=sm(out,s)
    return out
def sconj(s):return {j:pconj(p) for j,p in s.items()}
def ssub(s,repl):return {j:u for j,p in s.items() if (u:=peval(p,repl))}
def zeval(poly,Z):
    out={}
    for s in reversed(poly):out=sa(sm(out,Z),s)
    return out
def encf(z):return [[str(q) for q in side] for side in z]
def encp(p):return [[list(e),encf(z)] for e,z in sorted(p.items())]
def encs(s):return [[j,encp(p)] for j,p in sorted(s.items())]

def literal_replay(damage=None):
    from literal import pv,pc,padd,pscale,pmul,ppow,pint,psubst,pdiff,phash,NV
    t,z=pv(0),pv(1)
    hs=[pv(i) for i in range(2,9)];hs.append(pscale(padd(*hs),-1))
    us=[pv(i) for i in range(9,17)];vs=[pv(i) for i in range(17,25)];ws=[pv(i) for i in range(25,33)]
    S,V,W=padd(*us),padd(*vs),padd(*ws)
    H=padd(*(ppow(h,2) for h in hs));J3=padd(*(ppow(h,3) for h in hs));J4=padd(*(ppow(h,4) for h in hs))
    J21=padd(*(pmul(h,h,u) for h,u in zip(hs,us)))
    U2=padd(*(ppow(u,2) for u in us));B=pscale(padd(*(pmul(h,u) for h,u in zip(hs,us))),2)
    D=padd(U2,pscale(padd(*(pmul(h,v) for h,v in zip(hs,vs))),-2))
    crit=[padd(pscale(pmul(t,h),0,1),pmul(ppow(t,2),u),pscale(pmul(ppow(t,3),v),0,1),pmul(ppow(t,4),w)) for h,u,v,w in zip(hs,us,vs,ws)]
    der=pscale(pmul(*(padd(z,pscale(q,-1)) for q in crit)),9)
    prim=pint(der,1);a=padd(pc(1),pscale(ppow(t,2),-1))
    actual=padd(prim,pscale(psubst(prim,1,a),-1))
    diff=lambda n:padd(ppow(z,n),pc(-1))
    g2=padd(pc(9),pscale(pmul(S,diff(8)),F(-9,8)),pscale(pmul(H,diff(7)),F(9,14)))
    g3=padd(pscale(pmul(V,diff(8)),0,F(-9,8)),pscale(pmul(B,diff(7)),0,F(-9,14)),pscale(pmul(J3,diff(6)),0,F(1,2)))
    g4=padd(pc(-36),pscale(S,-9),pscale(H,F(9,2)),pscale(pmul(W,diff(8)),F(-9,8)),pscale(pmul(padd(ppow(S,2),pscale(D,-1)),diff(7)),F(9,14)),pmul(padd(pscale(pmul(S,H),F(-3,4)),pscale(J21,F(3,2))),diff(6)),pmul(padd(pscale(ppow(H,2),F(9,40)),pscale(J4,F(-9,20))),diff(5)))
    expected=padd(diff(9),pmul(ppow(t,2),g2),pmul(ppow(t,3),g3),pmul(ppow(t,4),g4))
    if damage=='missing_critical_factor':der=pscale(der,F(8,9))
    need(actual==expected,'whole generic literal eight-factor anchored primitive')
    need(pdiff(expected,1)==der,'whole generic literal derivative')
    need(not psubst(actual,1,a),'whole generic literal anchor')
    return {'credited_source':'8619/f8df996dba7bfec1d05eb6731b3b8e667ca8f860','variables':NV,'order':4,'derivative_terms':len(der),'derivative_sha256':phash(der),'primitive_terms':len(actual),'primitive_sha256':phash(actual),'whole_maps_compared':True}

def build(damage=None):
    literal=literal_replay(damage)
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2));d=na(ns(fm(c,c),2),ns(N1,-1));e=na(ns(fm(d,d),2),ns(N1,-1))
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1));H=ns(y,14);U0=ns(x,-8);C=na(ns(N1,F(8,3)),y)
    k=ns(na(N1,ns(c,2)),F(-7,18));rho=ns(na(c,ns(N1,-5)),F(1,3));ell=na(k,rho)
    w4=ni(na(c,d));w3=ns(na(ns(N1,7),ns(fm(na(N1,ns(d,-1)),w4),-1)),F(2,3))
    J3,J4,M,b,G,S,V=(pv(j) for j in range(NV))
    # Expectation is formal summation over eight coordinates, using only
    # sumV=0, sumV^2=H, sumV^3=J3, sumV^4=J4. No sampled substitution.
    moments=[pc(cf(8)),{},pc(cr(H)),J3,J4]
    def expectation(p):
        out={}
        for exp,z in p.items():
            j=exp[6];need(j<5,'complete generic coordinate expectation degree')
            f=list(exp);f[6]=0;out=pa(out,pm({tuple(f):z},moments[j]))
        return out
    q=pa(pfield(pa(pp(V,2),pc(cr(ns(H,F(-1,8))))),ns(rho,-1)),pfield(pm(J3,V),fm(ell,ni(H))))
    u=pa(pc(cr(ns(x,-1))),q,pm(S,V))
    qnorm=pa(pfield(pa(J4,pc(cr(ns(fm(H,H),F(-1,8))))),fm(rho,rho)),pfield(pp(J3,2),fm(na(fm(k,k),ns(fm(rho,rho),-1)),ni(H))))
    j21=pa(pc(cr(ns(fm(x,H),-1))),pfield(pa(J4,pc(cr(ns(fm(H,H),F(-1,8))))),ns(rho,-1)),pfield(pp(J3,2),fm(ell,ni(H))),pm(S,J3))
    U2=pa(pc(cr(ns(fm(x,x),8))),qnorm,pfield(pm(S,J3),ns(k,2)),pfield(pp(S,2),H))
    mixed=pa(pfield(J3,k),pfield(S,H))
    need(not expectation(q),'balanced centered q correction')
    need(expectation(pm(V,q))==pfield(J3,k),'whole mixed critical constraint')
    need(expectation(pp(q,2))==qnorm,'whole optimal centered correction square')
    need(expectation(pm(pp(V,2),u))==j21,'whole second mixed moment')
    need(expectation(pp(u,2))==U2,'whole actual real correction square')
    a=sa(sc(FONE),{2:pc(cf(-1))})
    crit={1:pm(V,pc(FI)),2:u,3:pm(pa(G,pm(b,V)),pc(FI)),4:M}
    powers=[{}]+[{j:u for j,p in sp(crit,n).items() if (u:=expectation(p))} for n in range(1,5)]
    expected_powers=[{},{2:pc(cr(U0)),3:ps(pm(G,pc(FI)),8),4:ps(M,8)},
        {2:pc(cr(ns(H,-1))),3:ps(pm(mixed,pc(FI)),2),4:pa(U2,pfield(b,ns(H,-2)))},
        {3:pm(J3,pc(cs(FI,-1))),4:ps(j21,-3)}, {4:J4}]
    need(powers==expected_powers,'whole four actual power sum jets')
    # Independent Newton recurrence integrates the whole octic derivative.
    elementary=[sc(FONE)]
    for n in range(1,9):
        nxt={}
        for j in range(1,n+1):
            if j<5:nxt=sa(nxt,ss(sm(elementary[n-j],powers[j]),(-1)**(j-1)))
        elementary.append(ss(nxt,F(1,n)))
    primitive=[{} for _ in range(10)]
    for n in range(9):primitive[9-n]=ss(elementary[n],F(9*(-1)**n,9-n))
    primitive[0]=ss(zeval(primitive,a),-1)
    need(not zeval(primitive,a),'actual Newton primitive anchored at a')
    D=pa(U2,pfield(b,ns(H,-2)))
    P2=[{} for _ in range(10)];P3=[{} for _ in range(10)];P4=[{} for _ in range(10)]
    def harmonic(poly,n,coef):poly[n]=sa(poly[n],{0:coef});poly[0]=sa(poly[0],{0:ps(coef,-1)})
    P2[0]=sc(cf(9));harmonic(P2,8,pc(cr(ns(x,9))));harmonic(P2,7,pc(cr(ns(y,9))))
    harmonic(P3,8,ps(pm(G,pc(FI)),-9));harmonic(P3,7,ps(pm(mixed,pc(FI)),F(-9,7)));harmonic(P3,6,ps(pm(J3,pc(FI)),F(1,2)))
    P4[0]=sc(cr(na(ns(N1,-36),ns(U0,-9),ns(H,F(9,2)))))
    harmonic(P4,8,ps(M,-9));harmonic(P4,7,ps(pa(pc(cr(fm(U0,U0))),ps(D,-1)),F(9,14)))
    harmonic(P4,6,pa(pc(cr(ns(fm(U0,H),F(-3,4)))),ps(j21,F(3,2))))
    harmonic(P4,5,pa(pc(cr(ns(fm(H,H),F(9,40)))),ps(J4,F(-9,20))))
    expected=[{} for _ in range(10)];expected[9]=sc(FONE);expected[0]=sc(cf(-1))
    for n in range(10):
        for j,p in P2[n].items():expected[n]=sa(expected[n],{j+2:p})
        for j,p in P3[n].items():expected[n]=sa(expected[n],{j+3:p})
        for j,p in P4[n].items():expected[n]=sa(expected[n],{j+4:p})
    need(primitive==expected,'entire generic moment anchored fourth primitive')
    if damage=='wrong_cubic_sign':primitive[6][3]=ps(primitive[6][3],-1)
    roots=[];normals=[];AB=[];Rs=[];Os=[]
    for label in range(8 if damage=='missing_ninth_root' else 9):
        w=np(NW,label);winv=np(NW,(-label)%9);Z=sc(cr(w));invder=cr(ns(np(NW,(-8*label)%9),F(1,9)))
        for j in range(1,ORDER+1):
            residual=zeval(primitive,Z).get(j,{})
            Z=sa(Z,{j:pm(residual,pc(cs(invder,-1)))})
        need(not zeval(primitive,Z),'entire actual root substitution '+str(label))
        L=na(ns(w,F(-1,3)),ns(x,-1),ns(fm(y,winv),-1))
        need(Z.get(2,{})==pc(cr(L)),'whole second root map '+str(label))
        n=ss(sa(sm(Z,sconj(Z)),sc(cf(-1))),F(1,2))
        if damage=='missing_curvature':n[4]=pa(n.get(4,{}),pc(cs(cm(cr(L),cc(cr(L))),F(-1,2))))
        cos=ns(na(w,winv),F(1,2))
        need(n.get(2,{})==pc(cr(ns(fm(y,fm(na(cos,ns(N1,F(1,2))),na(cos,c))),-2))),'whole second half-normal '+str(label))
        sine=lambda j:(N0,ns(na(np(NW,(j*label)%9),ns(np(NW,(-j*label)%9),-1)),F(-1,2)))
        third=pa(pm(G,pc(sine(1))),ps(pm(mixed,pc(sine(2))),F(1,7)),ps(pm(J3,pc(sine(3))),F(-1,18)))
        need(n.get(3,{})==third,'whole individual third half-normal '+str(label))
        if label in (3,4,5,6):
            need(not n.get(2),'active second normal '+str(label))
            closedthird=peval(third,{4:pfield(J3,ns(k,F(1,7))),5:{}})
            if damage=='wrong_cubic_closure':closedthird=pa(closedthird,J3)
            need(not closedthird,'all four generic active cubic cancellations '+str(label))
        roots.append(Z);normals.append(n)
        if label in (3,4):
            A=na(N1,ns(cos,-1));B=na(N1,ns(ns(na(np(NW,2*label),np(NW,(-2*label)%9)),F(1,2)),-1))
            R=peval(n.get(4,{}),{2:{},3:{}})
            need(n.get(4,{})==pa(R,pfield(M,ns(A,-1)),pfield(b,ns(fm(H,B),F(1,7)))),'whole even-normal closing columns '+str(label))
            AB.append((A,B));Rs.append(R);Os.append(third)
    need(len(roots)==len(normals)==9,'all nine whole root maps')
    for label in range(9):
        for j in range(5):need(normals[label].get(j,{})==ps(normals[(-label)%9].get(j,{}),(-1)**j),'all nine conjugate reversal '+str(label)+'/'+str(j))
    (A3,B3),(A4,B4)=AB
    detE=ns(fm(H,na(fm(A4,B3),ns(fm(A3,B4),-1))),F(1,7))
    need(detE==ns(fm(H,na(c,d)),F(3,14)),'whole even two-by-two determinant')
    oG=[pscalar(pdiff(O,4),'odd G column') for O in Os];oS=[pscalar(pdiff(O,5),'odd sigma column') for O in Os]
    detO=ca(cm(oG[0],oS[1]),cs(cm(oG[1],oS[0]),-1))
    detOExpected=cm(cm(oG[0],oG[1]),cr(ns(fm(H,na(N1,ns(c,-2))),F(1,7))))
    if damage=='singular_odd_block':detO=FZERO
    need(detO==detOExpected and detO!=FZERO,'whole odd two-by-two determinant')
    need(all(not pdiff(O,j) for O in Os for j in (2,3)),'odd-to-even-zero Jacobian block')
    R3,R4=[peval(R,{5:{}}) for R in Rs]
    invE=ni(detE)
    M0=pfield(pa(pfield(R4,B3),ps(pfield(R3,B4),-1)),ns(fm(H,invE),F(1,7)))
    b0=pfield(pa(pfield(R4,A3),ps(pfield(R3,A4),-1)),invE)
    closure={2:M0,3:b0,4:pfield(J3,ns(k,F(1,7))),5:{}}
    if damage=='wrong_even_closure':closure[2]=ps(M0,-1)
    closednorm=[ssub(n,closure) for n in normals]
    for label in (3,4,5,6):need(not closednorm[label],'all four generic normals vanish through fourth order '+str(label))
    delta=sa(sm(sa(a,ss(crit,-1)),sconj(sa(a,ss(crit,-1)))),sc(cf(-1)))
    obj={};coef=F(1)
    for j in range(5):
        if j:coef=coef*F((-2 if damage=='wrong_first_power' else -1)-2*(j-1),2*j)
        obj=sa(obj,ss(sp(delta,j),coef))
    obj={j:expectation(p) for j,p in obj.items() if expectation(p)}
    need(obj.get(0)==pc(cf(8)) and obj.get(2)==pc(cr(C)) and not obj.get(1) and not obj.get(3),'complete first-power objective and exact C slope')
    fixedobj=ssub(obj,closure);Kmap=fixedobj.get(4,{})
    sigma4=na(ns(N1,F(3,8)),ns(na(fm(w3,ns(N1,F(3,2))),fm(w4,na(N1,ns(e,-1)))),F(-1,20)))
    alpha=na(sigma4,ns(fm(rho,rho),F(-1,2)));tau=ns(fm(ell,ell),F(1,2))
    need(alpha==na(ns(N1,F(-527,360)),ns(c,F(41,90)),ns(fm(c,c),F(13,90))),'credited alpha entire normal form')
    need(tau==na(ns(N1,F(1369,648)),ns(c,F(74,81)),ns(fm(c,c),F(8,81))),'credited tau entire normal form')
    Bstar=na(ns(N1,F(2311,108)),ns(c,F(4934,27)),ns(fm(c,c),F(-1976,9)))
    K1=na(Bstar,ns(fm(alpha,fm(H,H)),F(-1,2)))
    target=pa(pc(cr(K1)),pfield(J4,alpha),pfield(pp(J3,2),fm(tau,ni(H))))
    if damage=='wrong_profile_cost':target=pa(target,pc(FONE))
    need(Kmap==target,'whole attained least-profile fourth objective cost')
    # Two exact prior specializations: useful baseline controls only.
    opposed={0:{},1:pc(cr(ns(fm(H,H),F(1,2))))}
    need(realfield(pscalar(peval(Kmap,opposed),'opposed cost'),'opposed cost')==Bstar,'prior opposed-pair cost reproduced')
    Wstar=na(ns(N1,F(2512,27)),ns(c,F(5840,9)),ns(fm(c,c),F(-21392,27)))
    bstar=na(ns(N1,F(13,36)),ns(c,F(1253,72)),ns(fm(c,c),F(-50,3)))
    need(pscalar(peval(M0,opposed),'opposed M')==cr(ns(Wstar,F(1,8))) and pscalar(peval(b0,opposed),'opposed b')==cr(bstar),'prior opposed-pair closing controls reproduced')
    skewcost=na(K1,ns(fm(alpha,fm(H,H)),F(43,56)),ns(fm(tau,fm(H,H)),F(9,14)))
    lam=ns(na(N1,c),12)
    skewrepaired=na(skewcost,fm(na(w3,w4),ni(fm(lam,lam))))
    skewprior=na(ns(N1,F(2215,108)),ns(c,F(23741,486)),ns(fm(c,c),F(-15737,243)))
    need(skewrepaired==skewprior,'prior1+7 cost and removed fourth repair reproduced')
    # Classical finite-population skewness bound: the ordinary Lagrange
    # argument reduces extrema to two values; verify ALL7 count cases.
    skew_cases=[]
    for r in range(1,7 if damage=='missing_stationary_multiplicity' else 8):
        norm_factor=F(r)+F(r*r,8-r)
        cubic_factor=F(r)-F(r**3,(8-r)**2)
        ratio=cubic_factor**2/norm_factor**3
        closed=F((8-2*r)**2,8*r*(8-r))
        need(ratio==closed and ratio<=F(9,14),'whole stationary skewness count '+str(r))
        skew_cases.append({'count':r,'complement':8-r,'squared_skewness':str(ratio),'9_over14_gap':str(F(9,14)-ratio)})
    need([z['count'] for z in skew_cases]==list(range(1,8)),'all seven stationary multiplicity cases')
    projection=pa(pp(V,2),pc(cr(ns(H,F(-1,8)))),pfield(pm(J3,V),ns(ni(H),-1)))
    defect=pa(J4,pc(cr(ns(fm(H,H),F(-1,8)))),pfield(pp(J3,2),ns(ni(H),-1)))
    need(expectation(pp(projection,2))==defect,'whole centered-square Pearson identity')
    maxdefect=pa(pfield(pa(pc(cr(ns(fm(H,H),F(9,14)))),pfield(pp(J3,2),ns(ni(H),-1))),na(alpha,tau)),pfield(defect,ns(alpha,-1)))
    need(pa(pc(cr(skewcost)),ps(Kmap,-1))==maxdefect,'whole maximum-profile cost defect identity')
    # All signs and the common budget in the physical real embedding.
    def realcoeff(z):
        realfield(cr(z),'physical comparison')
        ee=4*z[1];bb=-2*z[4];aa=z[0]-ee/2
        need(z==na(ns(N1,aa),ns(c,bb),ns(fm(c,c),ee)),'entire real cubic normal form')
        return aa,bb,ee
    lo,hi=F(15,16),F(47,50)
    cubic=lambda t:8*t**3-6*t-1
    need(cubic(lo)<0<cubic(hi) and 24*lo*lo-6>0,'physical cosine embedding isolation')
    for _ in range(24):
        mid=(lo+hi)/2
        if cubic(mid)<0:lo=mid
        else:hi=mid
    def bounds(z):
        a,b,e=realcoeff(z)
        return a+min(b*lo,b*hi)+min(e*lo*lo,e*hi*hi),a+max(b*lo,b*hi)+max(e*lo*lo,e*hi*hi)
    upper=na(K1,fm(na(alpha,tau),fm(H,H)))
    signed=[('H',H),('positive even determinant',detE),('odd sine gap',na(ns(c,2),ns(N1,-1))),('negative alpha',ns(alpha,-1)),('positive tau',tau),('positive alpha plus tau',na(alpha,tau)),('15 minus coarse K bound',na(ns(N1,15),ns(upper,-1))),('10 minus sharp uniform K bound',na(ns(N1,10),ns(skewcost,-1))),('sharp maximum K minus9',na(skewcost,ns(N1,-9)))]
    margins=[]
    for name,z in signed:
        lower,ub=bounds(z);need(lower>0,'physical strict sign '+name);margins.append({'name':name,'whole_field':encf(cr(z)),'lower':str(lower),'upper':str(ub)})
    for label in (0,1,2,7,8):
        coefficient=realfield(pscalar(normals[label][2],'inactive second normal'),'inactive second normal')
        lower,ub=bounds(ns(coefficient,-1));need(lower>0,'all five strict inactive half-normals '+str(label))
        margins.append({'name':'negative inactive n2 '+str(label),'whole_field':encf(cr(ns(coefficient,-1))),'lower':str(lower),'upper':str(ub)})
    return {'agent':'six-sendov-3','role':'researcher','status':'PASS','formalized':False,'independent_review':False,
        'scope':'all balanced real profiles; whole fourth maps; uniform IFT and rate optimality are ordinary proof bridges',
        'variables':['J3','J4','M','b','G','sigma','V'],'order':4,'literal_generic_baseline':literal,
        'constants':{name:encf(cr(z)) for name,z in [('c',c),('d',d),('e',e),('y',y),('x',x),('H',H),('U0',U0),('C',C),('k',k),('rho',rho),('ell',ell),('w3',w3),('w4',w4),('alpha',alpha),('tau',tau),('K1',K1),('Bstar',Bstar),('coarse_K_upper',upper),('sharp_K_maximum',skewcost),('detE',detE)]},
        'all_seven_stationary_skewness_cases':skew_cases,'whole_Pearson_defect':encp(defect),'whole_maximum_cost_defect':encp(maxdefect),
        'embedding_bracket':[str(lo),str(hi)],'strict_margins':margins,
        'optimal_profile_centered_correction':encp(q),'generic_power_sum_jets':[encs(s) for s in powers],
        'entire_moment_primitive':[encs(s) for s in primitive],
        'all_nine_control_root_jets':[encs(s) for s in roots],'all_nine_control_half_normals':[encs(s) for s in normals],
        'closing_M0':encp(M0),'closing_b0':encp(b0),'odd_Jacobian':[[encf(z) for z in oG],[encf(z) for z in oS]],'odd_determinant':encf(detO),
        'all_nine_closed_root_jets':[encs(ssub(z,closure)) for z in roots],'all_nine_closed_half_normals':[encs(s) for s in closednorm],
        'entire_first_power_objective':encs(obj),'closed_first_power_objective':encs(fixedobj),'whole_profile_cost':encp(Kmap)}

if __name__=='__main__':
    import json,time,resource
    started=time.monotonic();record=build()
    Path(__file__).with_name('EXPECTED.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'sha256':sha256(canonical(record)).hexdigest(),'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'record_bytes':Path(__file__).with_name('EXPECTED.json').stat().st_size}))
