"""six-reviewer-1, independent exact audit of LEMMA9818.

Written proof visible. Target native program/fixture not yet accessed this pass.
owned_core.py is the byte-identical OWN published25187d5 source, whose polynomial,
sector and Gaussian primitives are openly reused, not a blind new derivation.
owned_centered.py is the OWN9669 source785f5208. Ordinary bridges live in PROOF.
No solver, floating approximation, producer executable, or fixture import.
"""
from fractions import Fraction as Q
from math import comb,factorial
from itertools import combinations
import hashlib,json
import owned_core as old
import owned_centered as center

need=old.need;poly=old.poly;atom=old.atom;add=old.add;mul=old.mul;sc=old.sc
pw=old.pw;integrate=old.integrate;ev=old.ev;pack=old.pack;uni=old.uni
END=Q(1,16000)
def positive(m,k,v):
    need(v>0,k);m[k]=str(v)
def neg(m,k,v):
    need(v<0,k);m[k]=str(v)

def polar():
    h,t=atom(0),atom(1);a=add(poly(1),sc(h,-1))
    b=add(poly(1),sc(pw(a,2),-1));L=add(poly(8),sc(h,3))
    d=sc(mul(pw(a,7),b),Q(1,2))
    product=integrate(pw(add(a,sc(mul(mul(b,L),t),Q(1,8))),8))
    terms=[sc(mul(mul(pw(a,8-k),pw(b,k)),pw(sc(L,Q(1,8)),k)),Q(comb(8,k),k+1))for k in range(9)]
    need(product==add(*terms),'whole balanced product versus binomial integral')
    T=add(*terms[2:]);B=product
    nm=add(poly(1),sc(pw(a,16),-1),sc(mul(pw(d,2),pw(L,2)),-1),sc(mul(add(pw(a,8),mul(d,L)),T),-2),sc(pw(T,2),-1),sc(mul(mul(add(poly(8),sc(h,-6)),pw(a,15)),b),-1))
    nb=add(poly(1),sc(pw(h,2),9),sc(B,-1))
    nv=add(sc(mul(pw(a,6),pw(b,2)),13),sc(add(B,poly(-1)),-6))
    out={};m={}
    for name,p,degree,n2,cut in [('mean',nm,48,Q(4,3),1),('modulus',nb,24,Q(2,3),Q(1,2)),('variance',nv,24,Q(2),1)]:
        cs=uni(p);need(len(cs)==degree+1 and cs[:2]==[0,0] and cs[2]==n2,'whole polar support '+name)
        bound=cs[2]-sum(abs(v)*END**(k-2)for k,v in enumerate(cs[3:],3))
        positive(m,name,bound-cut);out[name]={'coefficients':list(map(str,cs)),'lower':str(bound)}
    return {'whole_B':list(map(str,uni(B))),'whole_T':list(map(str,uni(T))),'streams':out,'strict_margins':m}

def sectors():
    A=4+3*END;epsilon=Q(1,9);rows=[];m={};values={}
    for slots,d in [(7,1),(6,2)]:
        rs=[old.sector_piece(slots,k,d,A)for k in range(slots+1)];rows+=rs
        real=9*sum(Q(row['integral'])for row in rs)/(1-END)
        complex_=real+36*sum(epsilon**k/Q(factorial(k)*(k+d+1))for k in range(1,slots+1))/(1-END)
        if slots==7:
            positive(m,'real-gradient7/5',Q(7,5)-real)
            positive(m,'complex-gradient14/5',Q(14,5)-complex_)
            values.update(real_gradient=str(real),complex_gradient=str(complex_))
        else:
            positive(m,'complex-Hessian7/3',Q(7,3)-complex_)
            values['complex_Hessian']=str(complex_)
    positive(m,'one-negative-proper-product4',4-(Q(1,2)+A-1))
    positive(m,'two-negative-proper-product4',4-(Q(1,2)+A/2-1)**2)
    positive(m,'three-and-up-base1',1-(Q(1,2)+A/3-1))
    return {'whole15_sector_integrals':rows,'whole_bounds':values,'strict_margins':m}

def faces():
    # Route1: full (eta,t) factor product, integrate every coefficient.
    # Route2: full binomial expansion in a, then substitute a=1-eta.
    eta,t=atom(0),atom(1);a=add(poly(1),sc(eta,-1));x=atom(0);rows=[]
    for free in range(1,9):
        floor=8-free
        f=add(poly(1),a,sc(mul(a,t),-1))
        g=add(f,sc(mul(pw(a,2),t),Q(-8,free)))
        one=sc(integrate(mul(pw(f,floor),pw(g,free))),9)
        c=add(poly(1),x);s1=x;s2=add(x,sc(pw(x,2),Q(8,free)));two={}
        for i in range(floor+1):
            for j in range(free+1):
                term=mul(mul(pw(c,8-i-j),pw(s1,i)),pw(s2,j))
                two=add(two,sc(term,Q(9*comb(floor,i)*comb(free,j)*(-1)**(i+j),i+j+1)))
        two=old.sub(two,a,poly(0))
        need(one==two,'whole face integral two routes '+str(free))
        dm=Q(64*(free-1),free)-Q(256*(free-1)*(free-2),3*free*free)
        residual=add(one,sc(pw(add(poly(1),sc(a,Q(8,free))),free),-1),poly(-8),sc(pw(a,9),8),sc(pw(a,3),-Q(39,5)*dm))
        cs=uni(residual);lead=next(i for i,v in enumerate(cs)if v)
        need(lead==(1 if free in [1,8]else 0),'whole face leading order')
        margin=cs[lead]-sum(abs(v)*END**(k-lead)for k,v in enumerate(cs[lead+1:],lead+1))
        need(margin>0,'uniform face39/5 '+str(free))
        bad_at_one=ev(add(residual,sc(pw(a,3),-Q(1,5)*dm)),Q(0))
        if free==2:need(bad_at_one<0,'penalty8 genuinely fails at face2,a1')
        rows.append({'free':free,'whole_coefficients':list(map(str,cs)),'leading_order':lead,'positive_endpoint_margin':str(margin),'penalty8_at_a1':str(bad_at_one)})
    return rows

def majorant(stage):
    v=atom(0);bs={0:poly(1),1:{},2:sc(v,Q(1,2))}
    if stage==1:
        endpoint=Q(27,100);bs[3]=sc(v,Q(1,7));bs[4]=sc(pw(v,2),Q(3,32))
        for k in range(5,8):
            bs[k]=sc(add(mul(v,bs[k-2]),sc(mul(v,bs[k-3]),Q(3,7)),sc(mul(pw(v,2),add(*(sc(bs[k-j],Q(1,2)**(j-4))for j in range(4,k+1)))),Q(7,8))),Q(1,k))
        expected=Q(1047670269,4390400000);cut=Q(1,6)
    else:
        endpoint=Q(1,128);bs[3]=sc(v,Q(1,30));bs[4]=sc(pw(v,2),Q(1,8))
        for k in range(5,8):bs[k]=sc(mul(v,add(*(sc(bs[k-j],Q(1,10)**(j-2))for j in range(2,k+1)))),Q(1,k))
        expected=Q(2928703031,6553600000);cut=Q(4,9)
    need(all(c>=0 for p in bs.values()for c in p.values()),'whole majorant nonnegative coefficients')
    need(all(i>=1 for k in range(2,8)for i,j in bs[k]),'division by variance legal when positive')
    gap=Q(27,56)-sum((1-Q((-1)**k,comb(8,k)))*ev(bs[k],endpoint)/endpoint for k in range(3,8))
    need(gap==expected and gap>cut,'whole radial coercivity '+str(stage))
    return {'stage':stage,'endpoint':str(endpoint),'whole_polynomials':{str(k):pack(p)for k,p in bs.items()},'full_gap':str(gap),'weaker_cut':str(cut)}

def budgets():
    e=END;m={};negative={}
    p=lambda k,v:positive(m,k,v)
    p('a255/256',1-e-Q(255,256));p('transfer65/64',Q(65,64)-(1-e)**-2)
    p('phase-deficit10',10-9*(1+3*e/2));p('phase161',161-160-60*e);p('whole-phase1/9',Q(1,81)-161*e)
    p('product-gradient2',2-((8+3*e-Q(1,2))/7)**7)
    p('phase-real-and-mixed',Q(7,5)-Q(7,6));p('complete-origin-cost253',253-224-6*(Q(14,5)+2))
    d0=Q(323840,39);p('coarse-E2-7/4',28*(1-e)**2-26-Q(7,4))
    for i,(c,cut,nxt)in enumerate([(8*d0,Q(5),17),(Q(14,17)*d0,Q(43,100),27),(Q(14,27)*d0,Q(27,100),None)]):
        p('bootstrap'+str(i)+'-endpoint',cut-c*e)
        if nxt is not None:p('bootstrap'+str(i)+'-E2',28*(1-e)**2-2*cut-nxt)
    p('first-radial-7/25',Q(7,25)-Q(65,64)*Q(27,100)-Q(9,2)*e*e)
    p('first-individual1/2',(Q(1,2)-3*e/4)**2-Q(7,8)*Q(65,64)*Q(27,100))
    p('first-radial-root53/100',Q(53,100)**2-Q(7,25));p('first-phase9/200',Q(9,200)**2-30*e)
    p('first-path1/3',Q(1,3)-(Q(53,100)+Q(9,200)+3*e)**2);p('first-scale6/25',Q(6,25)**2-Q(1,18))
    z=Q(6,25)
    p('first-gradient2/9',Q(2,9)-sum(Q(k+1,8)*z**k for k in range(8)))
    p('first-Hessian1/12',Q(1,12)-sum(Q((k+1)*(k+2),56)*z**k for k in range(7)))
    tail=1/(8*(1-z)**2)-Q(1,8)-z/4
    p('first-signed-gradient3/40',Q(1,8)-(Q(1,2)+15*e)/28-tail-Q(3,40))
    p('first-complex-radial-sign',Q(3,40)*(1-e)*(1-20*e)-Q(1,108))
    p('first-linear-skew3/7',Q(1,7)**2-Q(27,100)/14)
    need(3*(Q(2,9)+2)+80*Q(1,12)+8*Q(2,9)==Q(136,9),'complete first upper cost')
    p('first-v91',91-Q(272,3));p('first-entry1/128',Q(1,128)-Q(272,3)*e)
    p('second-radial9/100',Q(9,100)**2-Q(65,64)*Q(1,128)-Q(9,2)*e*e)
    p('second-individual1/10',(Q(1,10)-3*e/4)**2-Q(7,8)*Q(65,64)*Q(1,128))
    p('second-phase3/80',Q(3,80)**2-22*e);p('second-path1/60',Q(1,60)-(Q(9,100)+Q(3,80)+3*e)**2)
    p('second-scale1/18',Q(1,18)**2-Q(1,360))
    z=Q(1,18)
    p('second-gradient1/7',Q(1,7)-sum(Q(k+1,8)*z**k for k in range(8)))
    p('second-Hessian1/23',Q(1,23)-sum(Q((k+1)*(k+2),56)*z**k for k in range(7)))
    p('second-product10/9',Q(10,9)-(Q(71,70)+3*e/7)**7)
    Bstar=Q(11,7)+Q(10,3)+Q(80,23);need(Bstar==Q(4049,483),'entire second upper cost')
    vc=Q(9,4)*Bstar
    p('Vr77/4',Q(77,4)-Q(65,64)*vc);p('reciprocal-squared38',38-Q(77,4)-18-Q(9,2)*e)
    p('radius24/25',(Q(1,25)-3*e/4)**2-Q(539,32)*e)
    p('sqrt38-37/6',Q(37,6)**2-38);p('sqrt8e-9/400',Q(9,400)**2-8*e)
    p('actual-H42',42-(Q(925,144)+Q(9,400))**2);p('actual-H-entry1/375',Q(1,375)-42*e)
    # New refinement, preserving every previously justified path/sign region.
    c2=Q(2928703031,6553600000);vcoef=Bstar/c2;vrcoef=Q(65,64)*vcoef
    qcoef=vrcoef+18+Q(9,2)*e
    p('retained-gap-qroot609/100',Q(609,100)**2-qcoef)
    p('retained-gap-radius29/30',(Q(1,30)-3*e/4)**2-Q(7,8)*vrcoef*e)
    need(Q(609,100)/Q(29,30)==Q(63,10),'exact improved reciprocal factor')
    p('retained-gap-actual-H40',40-(Q(63,10)+Q(9,400))**2)
    p('retained-gap-Hentry1/400',Q(1,400)-40*e) if Q(1,400)>40*e else need(Q(1,400)==40*e,'endpoint equality with strict H bound')
    rho=Q(1,54);h=Q(1,375);tau=Q(1,19);r0=Q(3999,4000);lo=1-e-rho;hi=1+rho;s=hi+h/2;Lc=Q(1,2)
    A={j:Q(9*comb(8,9-j),8*j)*rho**(7-j)for j in range(1,7)}|{7:Q(9,14)}
    Cd=sum(j*A[j]*s**(j-1)for j in A);Bd=9*lo**8-36*s**7*Lc*h-Cd*h
    Nc=Q(7,4)*sum(A[j]*hi**j for j in [1,2,4,5,7])
    Be=4*s**7/(25*lo**8)+Cd/(45*lo**8)
    Bs={5:Q(63,32),4:Q(63,32)*rho,2:Q(9,128)*rho*h,1:Q(9,4096)*h*h}
    p('centered-mean-rho',8*rho*rho-h);p('centered-nu-tau',tau*tau-h);p('centered-positive-rminus',lo)
    p('centered-critical-anchor',(1-e)**2-h)
    p('Rouche-entire',9*lo**8*Lc-36*s**7*Lc*Lc*h-sum(A[j]*(s**j+hi**j)for j in A))
    p('nine-circle-disjoint',(Q(4,9)*lo)-2*Lc*h);p('entire-Bd',Bd)
    p('whole-delta-W/5',Bd-5*Nc);p('whole-delta0-W/5',9*lo**8-5*Nc)
    for c,name in [(Q(1,6),'paired'),(Q(1,5),'individual')]:
        p('whole-'+name+'-normal',1-(1+2*rho)*Be-Q(1,50)-c*sum(Bs[j]*lo**(j-7)for j in Bs))
    p('entire-geometric-tail3/5',Q(3,5)-(Q(1,2)+tau/(lo-tau))/lo**3)
    p('positive-radius3999/4000',1-r0-(3*e+Q(3,5)*h)/8)
    p('positive-Q-coefficient',Q(3,4)/hi**3-Q(4,7))
    beta=Q(4,7)-1/(2*r0**3)-tau/((r0-tau)*r0**3);kappa=beta-Q(1216,225)*h
    p('whole-square-kappa1/1000',kappa-Q(1,1000))
    actual_kappa=beta-Q(1216,225*400)
    p('actual-retained-energy-kappa1/600',actual_kappa-Q(1,600))
    p('basic-slope13/5',Q(8,3)-4*e/3-Q(13,5))
    neg(negative,'old-gradient5/2',Q(5,2)-Q(sectors()['whole_bounds']['complex_gradient']))
    neg(negative,'old-displacement-W/6',Bd-6*Nc)
    neg(negative,'discarded-mean-kappa',beta-Q(16,3)*(rho/5+h))
    return {'strict_margins':m,'negative_old_budgets':negative,'new_refinement':{'c2':str(c2),'Bstar':str(Bstar),'v_coefficient':str(vcoef),'Vr_coefficient':str(vrcoef),'q_energy_coefficient':str(qcoef),'r_floor':'29/30','q_norm_upper':'609/100','H_coefficient':'40','H_reciprocal_coefficient':str((Q(63,10)+Q(9,400))**2),'strict_margin':str(40-(Q(63,10)+Q(9,400))**2),'absolute_energy_after_entry':'1/400','actual_kappa':str(actual_kappa)},'new_centered':{'A':{str(j):str(v)for j,v in A.items()},'lower_B':{str(j):str(v)for j,v in Bs.items()},'Cd':str(Cd),'Bd':str(Bd),'Nc':str(Nc),'Be':str(Be),'beta':str(beta),'kappa':str(kappa)}}

def square():
    t,w=atom(0),atom(1)
    original=add(sc(pw(t,2),4),sc(mul(t,w),-Q(16,15)),sc(pw(w,2),-Q(16,3)))
    completed=add(sc(pw(add(t,sc(w,-Q(2,15))),2),4),sc(pw(w,2),-Q(1216,225)))
    need(original==completed,'ENTIRE mean square coefficient identity')
    controls=[]
    for T,W in [(Q(0),Q(0)),(Q(1,100),Q(1,375)),(Q(2,15*375),Q(1,375)),(Q(1,54),Q(1,400))]:
        need(ev(original,T,W)==ev(completed,T,W),'whole literal square control')
        controls.append({'t':str(T),'W':str(W),'value':str(ev(original,T,W))})
    return {'whole_original':pack(original),'whole_completed':pack(completed),'whole_controls':controls}

def fresh_controls():
    g=center.ga;plus=center.gadd;times=center.gmul;scale=center.gsc;total=center.gsum
    def product(xs):
        out=g(1)
        for x in xs:out=times(out,x)
        return out
    def elementary(xs,k):return total(product(c)for c in combinations(xs,k))
    def polynomial(xs):
        out=[g(1)]
        for x in xs:
            nxt=[g(0)for _ in range(len(out)+1)]
            for i,c in enumerate(out):nxt[i]=plus(nxt[i],c);nxt[i+1]=plus(nxt[i+1],times(c,x))
            out=nxt
        return out
    cases=[[g(1)]*8,[g(Q(63,64)),g(Q(65,64))]*4,[g(Q(31,30),Q(1,50)),g(Q(29,30),Q(-1,50))]*4,[g(Q(1,2))]*7+[g(Q(9,2))],[g(Q(16+k,20),Q(k-4,100))for k in range(8)],[g(Q(1,3),Q(1,4)),g(0),g(0),g(-1,Q(1,2)),g(2),g(2),g(1),g(3)],[g(1,Q(k-3,160))for k in range(8)]]
    rows=[]
    for idx,qs in enumerate(cases):
        a=1-Q(idx+1,16000*(idx+1));bs=1-a*a
        origin=scale(total(scale(c,Q(1,k+1))for k,c in enumerate(polynomial([scale(q,-a)for q in qs]))),9)
        alt=scale(total(scale(elementary(qs,k),Q((-a)**k,k+1))for k in range(9)),9)
        need(origin==alt,'fresh entire Gaussian origin')
        polar=total(scale(elementary(qs,k),Q(a**(8-k)*bs**k,k+1))for k in range(9))
        pc=[g(1)]
        for q in qs:
            nxt=[g(0)for _ in range(len(pc)+1)]
            for k,c in enumerate(pc):
                nxt[k]=plus(nxt[k],scale(c,a))
                nxt[k+1]=plus(nxt[k+1],scale(times(c,q),bs))
            pc=nxt
        need(total(scale(c,Q(1,k+1))for k,c in enumerate(pc))==polar,'fresh full Gaussian polar two routes')
        grad=[];hess=[]
        for i in range(8):
            ss=[q for j,q in enumerate(qs)if j!=i]
            direct=scale(total(scale(c,Q(1,k+2))for k,c in enumerate(polynomial([scale(q,-a)for q in ss]))),-9*a)
            alt=scale(total(scale(elementary(ss,k),Q((-a)**k,k+2))for k in range(8)),-9*a)
            need(direct==alt,'fresh full8Gaussian gradient');grad.append([str(v)for v in direct])
            for j in range(8):
                if i==j:value=g(0)
                else:
                    ss=[q for k,q in enumerate(qs)if k not in [i,j]]
                    value=scale(total(scale(c,Q(1,k+3))for k,c in enumerate(polynomial([scale(q,-a)for q in ss]))),9*a*a)
                    alt=scale(total(scale(elementary(ss,k),Q((-a)**k,k+3))for k in range(7)),9*a*a)
                    need(value==alt,'fresh full64orderedGaussian Hessian')
                hess.append([i,j,[str(v)for v in value]])
        rows.append({'index':idx,'a':str(a),'q':[[str(v)for v in q]for q in qs],'whole_origin':[str(v)for v in origin],'whole_polar':[str(v)for v in polar],'whole_gradient':grad,'whole_ordered_Hessian':hess,'actual_disk_feasibility_asserted':False})
    return rows

def fresh_moments():
    rows=[]
    for k in range(1,8):
        xs=[Q(8-k,256)]*k+[Q(-k,256)]*(8-k)
        v=sum(x*x for x in xs);p3=sum(x**3 for x in xs);p4=sum(x**4 for x in xs)
        e4=sum((__import__('functools').reduce(lambda a,b:a*b,c,Q(1))for c in combinations(xs,4)),Q(0))
        need(sum(xs)==0 and p3*p3==Q((8-2*k)**2,8*k*(8-k))*v**3,'fresh all twolevel skew ratios')
        need(e4==v*v/8-p4/4 and abs(e4)<=3*v*v/32,'fresh complete fourth moment')
        rows.append({'positive_count':k,'coordinates':list(map(str,xs)),'variance':str(v),'p3':str(p3),'p4':str(p4),'e4':str(e4),'skew_ratio_squared':str(Q((8-2*k)**2,8*k*(8-k)))})
    return rows

def build():
    return {'schema':1,'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_height':9818,'eta_endpoint':str(END),'polar':polar(),'sectors':sectors(),'whole_radial_faces39over5':faces(),'whole_majorants':[majorant(1),majorant(2)],'budgets':budgets(),'whole_mean_square':square(),'fresh_Gaussian_controls':fresh_controls(),'fresh_twolevel_moment_controls':fresh_moments(),'credited_owned_universal_centered_identities':center.identities()}
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
