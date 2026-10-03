#!/usr/bin/env python3
"""Complete exact fourth-order jets of an ACTUAL degree-nine primitive.

Actual six-sendov-3 / researcher. Exact corroboration of the accompanying ordinary proof; not independent review.
Q[zeta_9,i] field operations are credited unchanged to arithmetic.py;
the sparse two-parameter and truncated-series layer is new here.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from arithmetic import F,N0,N1,NW,na,ns,nm,np,ni,nc,need,canonical,sha256
from functools import lru_cache
import json

ORDER=4
FZERO=(N0,N0)
FONE=(N1,N0)
FI=(N0,N1)
@lru_cache(maxsize=8192)
def fm(a,b):
    if a==N0 or b==N0:return N0
    return nm(a,b)
@lru_cache(maxsize=8192)
def fc(a):return nc(a)
def ca(*args):return (na(*(z[0] for z in args)),na(*(z[1] for z in args)))
def cs(z,q):return (ns(z[0],q),ns(z[1],q))
def cm(z,u):return (na(fm(z[0],u[0]),ns(fm(z[1],u[1]),-1)),
                      na(fm(z[0],u[1]),fm(z[1],u[0])))
def cc(z):return (fc(z[0]),ns(fc(z[1]),-1))
def cf(q):return (ns(N1,F(q)),N0)
def cr(z):return (z,N0)
def fp(z,n):
    out=FONE
    for _ in range(n):out=cm(out,z)
    return out
def pconst(z):return {} if z==FZERO else {(0,0):z}
def pvar(j):return {(int(j==0),int(j==1)):FONE}
def pa(*ps):
    out={}
    for p in ps:
        for m,z in p.items():out[m]=ca(out.get(m,FZERO),z)
    return {m:z for m,z in out.items() if z!=FZERO}
def ps(p,q):return {m:u for m,z in p.items() if (u:=cs(z,q))!=FZERO}
def pm(p,q):
    out={}
    for m,z in p.items():
        for n,u in q.items():
            k=(m[0]+n[0],m[1]+n[1]);out[k]=ca(out.get(k,FZERO),cm(z,u))
    return {m:z for m,z in out.items() if z!=FZERO}
def pc(p):return {m:cc(z) for m,z in p.items()}
def peval(p,M,b):
    out=FZERO
    for (r,t),z in p.items():out=ca(out,cm(z,cm(fp(M,r),fp(b,t))))
    return out
def sconst(z):return {0:pconst(z)} if z!=FZERO else {}
def sa(*ss):
    out={}
    for s in ss:
        for j,p in s.items():out[j]=pa(out.get(j,{}),p)
    return {j:p for j,p in out.items() if p}
def ss(s,q):return {j:p for j,r in s.items() if (p:=ps(r,q))}
def sm(s,t):
    out={}
    for j,p in s.items():
        for k,q in t.items():
            if j+k<=ORDER:out[j+k]=pa(out.get(j+k,{}),pm(p,q))
    return {j:p for j,p in out.items() if p}
def sp(s,n):
    out=sconst(FONE)
    for _ in range(n):out=sm(out,s)
    return out
def sc(s):return {j:pc(p) for j,p in s.items()}
def seval(s,M,b):return {j:pconst(z) for j,p in s.items() if (z:=peval(p,M,b))!=FZERO}
def zpoly_mul(p,q):
    out=[{} for _ in range(len(p)+len(q)-1)]
    for j,s in enumerate(p):
        for k,t in enumerate(q):out[j+k]=sa(out[j+k],sm(s,t))
    return out
def zpoly_eval(p,Z):
    out={}
    for s in reversed(p):out=sa(sm(out,Z),s)
    return out
def encf(z):return [[str(q) for q in side] for side in z]
def encp(p):return [[list(m),encf(z)] for m,z in sorted(p.items())]
def encs(s):return [[j,encp(p)] for j,p in sorted(s.items())]
def scalar(p,label):
    need(set(p)<={(0,0)},label+' constant parameter map')
    return p.get((0,0),FZERO)
def is_real_q9(z,label):
    need(z[1]==N0 and fc(z[0])==z[0],label+' real Q(zeta9) constant')
    return z[0]

def build(damage=None):
    c=ns(na(np(NW,4),np(NW,5)),F(-1,2))
    y=ns(ni(na(N1,c)),F(1,3));x=na(ns(N1,F(2,3)),ns(y,-1))
    lam=ns(na(N1,c),12);k=ns(na(N1,ns(c,2)),F(-7,18));g=ns(k,48)
    if damage=='wrong_cubic_mean':g=ns(g,-1)
    d=na(ns(fm(c,c),2),ns(N1,-1));C=na(ns(N1,F(8,3)),y)
    a=sa(sconst(FONE),{2:pconst(cr(ns(lam,-1)))})
    m={2:pconst(cr(ns(fm(x,lam),-1))),3:pconst((N0,g)),4:ps(pvar(0),-1 if damage=='wrong_mean_column' else 1)}
    nuL={1:pconst(cs(FI,7)),2:pconst(cr(ns(k,42))),3:ps(pvar(1),7)}
    nuL[3]=pm(nuL[3],pconst(FI))
    nuS={1:pconst(cs(FI,-1)),2:pconst(cr(ns(k,-6))),3:pm(ps(pvar(1),-1),pconst(FI))}
    zL=sa(m,nuL);zS=sa(m,nuS)
    weight=6 if damage=='missing_critical_multiplicity' else 7
    centered_sum=sa(nuL,ss(nuS,weight));need(not centered_sum,'all eight centered criticals sum zero')
    T=sa(sp(nuL,2),ss(sp(nuS,2),7));U=sa(sp(nuL,3),ss(sp(nuS,3),7))
    need(T.get(2)==pconst(cf(-56)),'full centered second-moment leading term')
    need(T.get(3)==pconst((N0,ns(k,672))),'full centered second-moment cubic term')
    need(U.get(3)==pconst(cs(FI,-336)),'full centered cubic moment')
    product=[sconst(FONE)]
    for z in [zL]+[zS]*7:product=zpoly_mul(product,[ss(z,-1),sconst(FONE)])
    primitive=[{}]+[ss(t,F(9,j+1)) for j,t in enumerate(product)]
    anchoring=zpoly_eval(primitive,a);primitive[0]=ss(anchoring,-1)
    need(not zpoly_eval(primitive,a),'actual primitive anchored at a')
    need(primitive[-1]==sconst(FONE),'degree nine monic entire primitive')
    # Separate ordinary Newton/integration formulas for the ENTIRE polynomial jet.
    m2=ns(fm(x,lam),-1)
    predicted=[{} for _ in range(10)]
    predicted[9]=sconst(FONE)
    predicted[8]={2:pconst(cr(ns(m2,-9))),3:pconst((N0,ns(g,-9))),4:ps(pvar(0),-9)}
    predicted[7]={2:pconst(cf(36)),3:pconst((N0,ns(k,-432))),
                  4:pa(pconst(cr(na(ns(fm(m2,m2),36),ns(fm(k,k),-1296)))),ps(pvar(1),72))}
    predicted[6]={3:pconst(cs(FI,168)),4:pconst(cr(na(ns(m2,-252),ns(k,3024))))}
    predicted[5]={4:pconst(cf(-378))}
    predicted[0]={0:pconst(cf(-1)),
        2:pconst(cr(na(ns(lam,9),ns(m2,9),ns(N1,-36)))),
        3:pconst((N0,na(ns(g,9),ns(k,432),ns(N1,-168)))),
        4:pa(pconst(cr(na(ns(fm(lam,lam),-36),fm(lam,na(ns(m2,-72),ns(N1,252))),
                          ns(fm(m2,m2),-36),ns(fm(k,k),1296),ns(m2,252),ns(k,-3024),ns(N1,378)))),
             ps(pvar(0),9),ps(pvar(1),-72))}
    need(primitive==predicted,'complete actual anchored polynomial fourth jet')
    if damage=='wrong_primitive_cubic_sign':primitive[6][3]=ps(primitive[6][3],-1)
    roots=[];normals=[]
    for label in range(8 if damage=='missing_ninth_root' else 9):
        w=np(NW,label);Z=sconst(cr(w));inv_derivative=cr(ns(np(NW,(-8*label)%9),F(1,9)))
        for j in range(1,ORDER+1):
            residual=zpoly_eval(primitive,Z).get(j,{})
            correction=pm(residual,pconst(cs(inv_derivative,-1)))
            Z=sa(Z,{j:correction})
        need(not zpoly_eval(primitive,Z),'full root substitution '+str(label))
        need(not Z.get(1),'root first jet zero '+str(label))
        winv=np(NW,(-label)%9);winv2=np(NW,(-2*label)%9)
        L=fm(lam,na(ns(w,F(-1,3)),ns(x,-1),ns(fm(y,winv),-1)))
        W=ca(cm((N0,g),cr(na(N1,winv,ns(w,-2)))),
             cm(cs(FI,F(-56,3)),cr(na(winv2,ns(w,-1)))))
        need(Z.get(2,{})==pconst(cr(L)),'entire second root jet '+str(label))
        need(Z.get(3,{})==pconst(W),'entire third root jet '+str(label))
        P4=zpoly_eval(primitive,sconst(cr(w))).get(4,{})
        P2prime=na(ns(fm(m2,np(w,7)),-72),ns(np(w,6),252))
        fourth_numerator=pa(P4,pconst(cm(cr(P2prime),cr(L))),
                            pconst(cs(cm(cr(np(w,7)),cm(cr(L),cr(L))),36)))
        analytic_V=pm(fourth_numerator,pconst(cs(inv_derivative,-1)))
        need(Z.get(4,{})==analytic_V,'entire analytic fourth root formula '+str(label))
        normal=ss(sa(sm(Z,sc(Z)),sconst(cf(-1))),F(1,2))
        if damage=='missing_modulus_curvature':
            normal[4]=pa(normal.get(4,{}),ps(pm(pconst(cr(L)),pconst(cc(cr(L)))),F(-1,2)))
        cosine=ns(na(w,winv),F(1,2))
        expected_n2=ns(fm(lam,fm(y,fm(na(cosine,ns(N1,F(1,2))),na(cosine,c)))),-2)
        need(normal.get(2,{})==pconst(cr(expected_n2)),'entire second normal factor '+str(label))
        sine=lambda j:(N0,ns(na(np(NW,(j*label)%9),ns(np(NW,(-j*label)%9),-1)),F(-1,2)))
        n3=ca(cm(cr(g),sine(1)),cm(cr(ns(k,48)),sine(2)),cs(sine(3),F(-56,3)))
        need(normal.get(3,{})==pconst(n3),'entire third individual normal formula '+str(label))
        if label in (3,4,5,6):
            need(not normal.get(2),'active second normal '+str(label))
            need(not normal.get(3),'active third normal '+str(label))
        if label in (3,6):
            need(W==cm((N0,ns(g,-3)),cr(w)),'nonzero cubic tangency '+str(label))
        roots.append(Z);normals.append(normal)
    need(len(roots)==len(normals)==9,'all nine entire root and normal maps')
    R=[];AB=[]
    for label in (3,4):
        w=np(NW,label);cosine=ns(na(w,np(NW,(-label)%9)),F(1,2))
        cosine2=ns(na(np(NW,2*label),np(NW,(-2*label)%9)),F(1,2))
        A=na(N1,ns(cosine,-1));B=na(N1,ns(cosine2,-1))
        fourth=normals[label].get(4,{})
        Rj=fourth.get((0,0),FZERO)
        expected=pa(pconst(Rj),pm(pvar(0),pconst(cr(ns(A,-1)))),pm(pvar(1),pconst(cr(ns(B,8)))))
        need(fourth==expected,'complete affine fourth normal '+str(label))
        R.append(is_real_q9(Rj,'fourth residual '+str(label)));AB.append((A,B))
    (A3,B3),(A4,B4)=AB;R3,R4=R
    det=ns(na(fm(B3,A4),ns(fm(A3,B4),-1)),8)
    need(det==ns(na(c,d),12),'whole fourth-normal determinant')
    inv=ni(det);q3=na(N1,R3);q4=na(N1,R4)
    M=fm(ns(na(fm(B3,q4),ns(fm(B4,q3),-1)),8),inv)
    b=fm(na(fm(A3,q4),ns(fm(A4,q3),-1)),inv)
    need(fc(M)==M and fc(b)==b,'closure parameters exactly real')
    def realc(a,b,e):return na(ns(N1,F(a)),ns(c,F(b)),ns(fm(c,c),F(e)))
    expected_R3=realc(F(-431,3),F(-320,3),F(-320,3))
    expected_R4=realc(F(-1636,9),F(-2842,9),-220)
    if damage=='wrong_fourth_residual':expected_R4=na(expected_R4,N1)
    need(R3==expected_R3 and R4==expected_R4,'whole fourth residuals in real cubic field')
    need(M==realc(F(-512,9),F(-1684,9),F(-1328,9)), 'whole explicit closing M')
    need(b==realc(F(43,9),F(-29,2),F(-86,9)), 'whole explicit closing b')
    if damage=='wrong_closing_M':M=ns(M,-1)
    fixed_roots=[seval(Z,cr(M),cr(b)) for Z in roots]
    fixed_normals=[seval(n,cr(M),cr(b)) for n in normals]
    for label in (3,4,5,6):
        need(fixed_normals[label].get(4)==pconst(cf(-1)),'active root strictly inward at fourth order '+str(label))
    for label in range(9):
        opposite=fixed_normals[(-label)%9]
        for j in range(ORDER+1):
            need(fixed_normals[label].get(j,{})==ps(opposite.get(j,{}),(-1)**j),'whole conjugate reversal normal '+str(label)+'/'+str(j))
    # Complete FIRST-power objective: binomial series of actual squared distances.
    objective={}
    for z,weight in ((zL,1),(zS,7)):
        distance=sa(a,ss(z,-1));sq=sm(distance,sc(distance));delta=sa(sq,sconst(cf(-1)))
        contribution={};coeff=F(1)
        for j in range(ORDER+1):
            if j:coeff=coeff*F((-2 if damage=='quadratic_instead_of_first_power' else -1)-2*(j-1),2*j)
            contribution=sa(contribution,ss(sp(delta,j),coeff))
        objective=sa(objective,ss(contribution,weight))
    need(objective.get(0)==pconst(cf(8)),'actual first-power base objective')
    need(not objective.get(1) and not objective.get(3),'actual first-power odd jets zero')
    need(objective.get(2)==pconst(cr(fm(lam,C))),'actual first-power exact C slope')
    fixed_objective=seval(objective,cr(M),cr(b))
    K_s=is_real_q9(scalar(fixed_objective.get(4,{}),'objective fourth coefficient'),'objective fourth coefficient')
    K_eta=fm(K_s,ni(fm(lam,lam)))
    need(K_eta==realc(F(2215,108),F(23741,486),F(-15737,243)), 'whole exact second objective coefficient')
    # Physical real embedding and scalar comparisons: NO floating point.
    clo,chi=F(15,16),F(47,50)
    cubic=lambda z:8*z**3-6*z-1
    coeff=lambda z:(19935+47482*z-62948*z*z)/972
    upper=F(9) if damage=='false_objective_upper_cut' else F(10)
    need(cubic(clo)<0<cubic(chi),'exact cosine embedding endpoint signs')
    need(24*clo*clo-6>0,'cosine cubic strictly increasing on bracket')
    need(47482-125896*clo<0,'objective coefficient decreasing on bracket')
    need(9<coeff(chi)<coeff(clo)<upper,'strict second objective coefficient bounds 9<K<10')
    return {'agent':'six-sendov-3','role':'researcher','status':'PASS',
       'order':ORDER,'field':'Q[w,i]/(w^6+w^3+1,i^2+1), physical embedding w=exp(2pi*i/9)',
       'scope':'full actual monic anchored primitive, all nine root jets and all eight critical multiplicities; asymptotic disk proof is an ordinary analytic bridge',
       'constants':{name:encf(cr(z)) for name,z in [('c',c),('d',d),('y',y),('x',x),('lambda',lam),('k',k),('g',g),('C',C),('det',det),('R3',R3),('R4',R4),('M',M),('b',b),('K_eta',K_eta)]},
       'strict_embedding_budgets':{'c_lower':str(clo),'c_upper':str(chi),
           'cubic_lower':str(cubic(clo)),'cubic_upper':str(cubic(chi)),
           '9_to_K_lower_gap':str(coeff(chi)-9),'K_upper_to_10_gap':str(10-coeff(clo))},
       'full_primitive_coefficients': [encs(s) for s in primitive],
       'centered_moments':{'T':encs(T),'U3':encs(U)},
       'all_nine_parameter_root_jets':[encs(z) for z in roots],
       'all_nine_parameter_half_normals':[encs(n) for n in normals],
       'all_nine_fixed_root_jets':[encs(z) for z in fixed_roots],
       'all_nine_fixed_half_normals':[encs(n) for n in fixed_normals],
       'complete_first_power_objective':encs(objective),'fixed_first_power_objective':encs(fixed_objective),
       'independent_review':False,'formalized':False}
