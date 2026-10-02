"""six-reviewer-1: fresh full rational arithmetic for committed LEMMA9776.
Target written statements visible; target executable and fixture unread.
Ordinary bridges are audited separately. Finite controls assert no actual
original-disk feasibility. owned_centered.py is this reviewer's credited
9669 source785f5208b1bf59c1abe5a9f91e2a9cebad0a7368; it is reused openly, not counted as a blind new input.
No floating point, solver, native researcher source or external data import.
"""
from fractions import Fraction as Q
from math import comb, factorial
import hashlib,json
import owned_centered as centered

def need(ok,what):
    if not ok:raise ValueError(what)
def poly(c=0):return {(0,0):Q(c)} if c else {}
def atom(i):return {(int(i==0),int(i==1)):Q(1)}
def clean(p):return {k:v for k,v in p.items() if v}
def add(*ps):
    r={}
    for p in ps:
        for k,v in p.items():r[k]=r.get(k,Q(0))+v
    return clean(r)
def sc(p,c):return clean({k:v*c for k,v in p.items()})
def mul(p,q):
    r={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():r[i+k,j+l]=r.get((i+k,j+l),Q(0))+v*w
    return clean(r)
def pw(p,n):
    r=poly(1)
    for _ in range(n):r=mul(r,p)
    return r
def integrate(p,coordinate=1):
    # Full integral on [0,1], not formal degree truncation.
    r={}
    for ij,v in p.items():
        k=list(ij);degree=k[coordinate];k[coordinate]=0;k=tuple(k)
        r[k]=r.get(k,Q(0))+v/(degree+1)
    return clean(r)
def ev(p,x,y=0):return sum((v*x**i*y**j for (i,j),v in p.items()),Q(0))
def pack(p):return [[i,j,str(v)] for (i,j),v in sorted(p.items())]
def uni(p):
    need(all(j==0 for i,j in p),'univariate support')
    return [p.get((i,0),Q(0)) for i in range(1+max((i for i,j in p),default=0))]
def coefficients(p):return list(map(str,uni(p)))
def sub(p,x,y):
    return add(*(sc(mul(pw(x,i),pw(y,j)),v)for (i,j),v in p.items()))
def strict(margins,k,v):need(v>0,k);margins[k]=str(v)

END=Q(1,25000)

def polar():
    h,t=atom(0),atom(1);a=add(poly(1),sc(h,-1));b=add(poly(1),sc(pw(a,2),-1));L=add(poly(8),sc(h,3));d=sc(mul(pw(a,7),b),Q(1,2))
    # Direct whole-product expansion/integration versus elementary binomial formula.
    B=integrate(pw(add(a,sc(mul(mul(b,L),t),Q(1,8))),8))
    terms=[sc(mul(mul(pw(a,8-k),pw(b,k)),pw(sc(L,Q(1,8)),k)),Q(comb(8,k),k+1))for k in range(9)]
    need(B==add(*terms),'entire balanced polar identity')
    T=add(*terms[2:]);need(B==add(pw(a,8),mul(d,L),T),'entire higher tail')
    Nm=add(poly(1),sc(pw(a,16),-1),sc(mul(pw(d,2),pw(L,2)),-1),sc(mul(add(pw(a,8),mul(d,L)),T),-2),sc(pw(T,2),-1),sc(mul(mul(add(poly(8),sc(h,-6)),pw(a,15)),b),-1))
    Nb=add(poly(1),sc(pw(h,2),9),sc(B,-1))
    Nv=add(sc(mul(pw(a,6),pw(b,2)),13),sc(add(B,poly(-1)),-6))
    streams={};margins={}
    for name,p,degree,n2,cut in [('mean',Nm,48,Q(4,3),1),('balanced',Nb,24,Q(2,3),Q(1,2)),('variance',Nv,24,Q(2),1)]:
        cs=uni(p);need(len(cs)==degree+1 and cs[:2]==[0,0] and cs[2]==n2,'entire '+name+' degree and leading terms')
        lower=cs[2]-sum(abs(v)*END**(k-2)for k,v in enumerate(cs[3:],3))
        strict(margins,name+'-whole-coefficient-budget',lower-cut);streams[name]={'coefficients':list(map(str,cs)),'lower_coefficient':str(lower)}
    return {'B':coefficients(B),'T':coefficients(T),'streams':streams,'strict_margins':margins}

def beta(n,m):return Q(factorial(n)*factorial(m),factorial(n+m+1))
def sector_piece(m,k,d,A):
    x=atom(0)
    if k==0:
        p=mul(pw(x,d),pw(add(poly(1),sc(x,Q(-1,2))),m));r=ev(integrate(p,0),0);threshold=Q(0)
        # x^d (1-x/2)^m = x^d 2^-m (1+(1-x))^m.
        positive=sum(Q(comb(m,j),2**m)*beta(d,j)for j in range(m+1))
    else:
        R=Q(1,2)+A/k;threshold=1/R;length=1-threshold
        p=mul(mul(pw(x,d),pw(add(poly(1),sc(x,Q(-1,2))),m-k)),pw(add(sc(x,R),poly(-1)),k))
        r=sum(v*(1-threshold**(i+1))/(i+1)for (i,j),v in p.items())
        # t=threshold+length*x; expand t^d and 1-t/2=(1+length*(1-x))/2.
        positive=R**k*length**(k+1)*sum(Q(comb(d,i)*comb(m-k,j),2**(m-k))*threshold**(d-i)*length**(i+j)*beta(k+i,j)for i in range(d+1)for j in range(m-k+1))
    need(r==positive,'whole two-route sector '+str((m,k,d)))
    need(r>0,'sector positivity')
    return {'m':m,'negative_factors':k,'weight_degree':d,'threshold':str(threshold),'integral':str(r),'whole_integrand_coefficients':coefficients(p)}

def sectors():
    A=4+3*END;eps=Q(1,12);rows=[];margins={}
    for m,d,cut,name in [(7,1,Q(5,2),'gradient'),(6,2,Q(9,4),'mixed-Hessian')]:
        subset=[sector_piece(m,k,d,A)for k in range(m+1)];rows+=subset
        value=(9*sum(Q(row['integral'])for row in subset)+36*sum(eps**k/Q(factorial(k)*(k+d+1))for k in range(1,m+1)))/(1-END)
        strict(margins,name+'-whole-sector-budget',cut-value)
    strict(margins,'proper-product-A',Q(9,2)-A);strict(margins,'proper-one-negative',4-(Q(1,2)+A-1));strict(margins,'proper-two-negative',4-(Q(1,2)+A/2-1)**2);strict(margins,'proper-three-and-up',1-(Q(1,2)+A/3-1))
    return {'complete_15_sector_integrals':rows,'strict_margins':margins}

def majorants(stage):
    x=atom(0);v=pw(x,1);b={0:poly(1),1:{},2:sc(v,Q(1,2))}
    if stage==1:
        bound=Q(23,50);rho=Q(2,3);b[3]=sc(v,Q(2,11));b[4]=sc(pw(v,2),Q(3,32))
        for k in range(5,8):b[k]=sc(add(mul(v,b[k-2]),sc(mul(v,b[k-3]),Q(6,11)),sc(mul(pw(v,2),add(*(sc(b[k-s],rho**(s-4))for s in range(4,k+1)))),Q(7,8))),Q(1,k))
        expected=Q(487362179,8131200000);cut=Q(1,20)
    else:
        bound=Q(1,64);rho=Q(1,8);b[3]=sc(v,rho/3);b[4]=sc(pw(v,2),Q(1,8))
        for k in range(5,8):b[k]=sc(mul(v,add(*(sc(b[k-s],rho**(s-2))for s in range(2,k+1)))),Q(1,k))
        expected=Q(32075187,73400320);cut=Q(3,7)
    need(all(coef>=0 for p in b.values()for coef in p.values()),'full nonnegative majorant support')
    need(all(i>=1 for k in range(2,8)for i,j in b[k]),'legal majorant divided by positive variance')
    value=Q(27,56)-sum((1-Q((-1)**k,comb(8,k)))*ev(b[k],bound)/bound for k in range(3,8))
    need(value==expected and value>cut,'complete radial coercivity '+str(stage))
    return {'stage':stage,'endpoint':str(bound),'rho':str(rho),'whole_majorants':{str(k):pack(p)for k,p in b.items()},'exact_coercivity':str(value),'cut':str(cut)}

def radial_certificate():
    # Independently rebuild the imported penalty-five gap, every profile and
    # all636 Bernstein coefficients, without loading the researcher's fixture.
    a,u=atom(0),atom(1) # integration of t is performed analytically below
    blocks=[];count=positive=zeros=0
    for k in range(8):
        m=8-k;degree=16-k
        # The t-linear factors have constants1+a and slopes a and
        # a+(8/m)a^2 u. Binomial expansion integrates their FULL product.
        c=add(poly(1),a);s1=a;s2=add(a,sc(mul(pw(a,2),u),Q(8,m)))
        integrated={}
        for i in range(k+1):
            for j in range(m+1):
                term=mul(mul(pw(c,8-i-j),pw(s1,i)),pw(s2,j));integrated=add(integrated,sc(term,Q(9*comb(k,i)*comb(m,j)*(-1)**(i+j),i+j+1)))
        P=add(integrated,sc(pw(add(poly(1),sc(mul(a,u),Q(8,m))),m),-1))
        D=add(sc(mul(pw(a,3),pw(u,2)),Q(64*(m-1),m)),sc(mul(pw(a,3),pw(u,3)),Q(-256*(m-1)*(m-2),3*m*m)))
        R=add(P,poly(-8),sc(pw(a,9),8),sc(D,-5))
        need(all(i<=degree and j<=m for i,j in R),'complete bidegree')
        Bs=[[sum(v*Q(comb(i,p),comb(degree,p))*Q(comb(j,q),comb(m,q))for(p,q),v in R.items()if p<=i and q<=j)for j in range(m+1)]for i in range(degree+1)]
        reconstructed={}
        # Invert the entire tensor Bernstein representation, every coefficient.
        for i,row in enumerate(Bs):
            for j,v in enumerate(row):
                for p in range(i,degree+1):
                    for q in range(j,m+1):
                        coef=v*comb(degree,i)*comb(degree-i,p-i)*comb(m,j)*comb(m-j,q-j)*(-1)**(p-i+q-j)
                        reconstructed[p,q]=reconstructed.get((p,q),Q(0))+coef
        need(clean(reconstructed)==R,'complete Bernstein inverse '+str(k));need(all(v>=0 for row in Bs for v in row),'penalty-five full-domain sign '+str(k))
        flat=[v for row in Bs for v in row];count+=len(flat);positive+=sum(v>0 for v in flat);zeros+=sum(v==0 for v in flat)
        blocks.append({'floor_count':k,'bidegree':[degree,m],'whole_power_coefficients':pack(R),'whole_Bernstein_coefficients':[[str(v)for v in row]for row in Bs]})
    need((count,positive,zeros)==(636,590,46),'full radial certificate counts')
    return {'scope':'only full-domain penalty-five gap; mean tube/annulus unused','blocks':blocks,'coefficient_count':count,'positive':positive,'zero':zeros}


def budgets():
    e=END;m={};p=lambda name,value:strict(m,name,value)
    p('normalization-a255/256',1-e-Q(255,256));p('normalization65/64',Q(65,64)-(1-e)**-2)
    p('angular10',10-9*(1+3*e/2));p('whole-normalization-phase161',161-(160+60*e));p('whole-phase1/12',Q(1,144)-161*e)
    p('global-product-gradient2',2-((8+3*e-Q(1,2))/7)**7)
    d0=Q(256*427,5);v0=Q(13)
    p('global-E2-7/4',28*(1-e)**2-2*v0-Q(7,4))
    stages=[(8*d0,Q(7),13),(Q(14,13)*d0,Q(1),25),(Q(14,25)*d0,Q(1,2),26),(Q(14,26)*d0,Q(12,25),27),(Q(14,27)*d0,Q(23,50),None)]
    for i,(coef,cut,nextE)in enumerate(stages):
        p('global-stage'+str(i)+'-variance',cut-coef*e)
        if nextE is not None:p('global-stage'+str(i)+'-E2',28*(1-e)**2-2*cut-nextE)
    p('local1-squared-norm15/32',Q(15,32)-Q(65,64)*Q(23,50)-Q(9,2)*e*e)
    p('local1-individual2/3',(Q(2,3)-3*e/4)**2-Q(7,8)*Q(65,64)*Q(23,50))
    p('local1-radial11/16',Q(11,16)**2-Q(15,32));p('local1-phase3/80',Q(3,80)**2-Q(100,3)*e)
    p('local1-whole-path3/5',Q(3,5)-(Q(11,16)+Q(3,80)+3*e)**2);p('local1-Cauchy8/25',Q(8,25)**2-Q(3,5)/6)
    z=Q(8,25);p('local1-gradient2/7',Q(2,7)-sum(Q(k+1,8)*z**k for k in range(8)));p('local1-Hessian3/25',Q(3,25)-sum(Q((k+1)*(k+2),56)*z**k for k in range(7)))
    tail=1/(8*(1-z)**2)-Q(1,8)-z/4
    p('local1-negative-gradient7/200',Q(1,8)-(Q(2,3)+15*e)/28-tail-Q(7,200))
    p('local1-complex-negative-gradient',Q(7,200)*(1-e)*(1-20*e)-Q(1,100))
    p('zero-sum-skew-linear6/11',Q(2,11)**2-Q(23,50)/14)
    p('first-proportional-375',375-Q(2624,7));p('first-proportional-entry1/64',Q(1,64)-Q(2624,7)*e)
    p('local2-squared-norm17/128',Q(17,128)**2-Q(65,64)*Q(1,64)-Q(9,2)*e*e)
    p('local2-individual1/8',(Q(1,8)-3*e/4)**2-Q(7,8)*Q(65,64)*Q(1,64))
    p('local2-phase1/32',Q(1,32)**2-Q(45,2)*e);p('local2-whole-path1/36',Q(1,36)-(Q(21,128)+3*e)**2);p('local2-Cauchy1/14',Q(1,14)**2-Q(1,36)/6)
    z=Q(1,14);p('local2-gradient3/20',Q(3,20)-sum(Q(k+1,8)*z**k for k in range(8)));p('local2-Hessian1/22',Q(1,22)-sum(Q((k+1)*(k+2),56)*z**k for k in range(7)))
    p('local2-product23/20',Q(23,20)-(Q(57,56)+3*e/7)**7)
    need(Q(39,10)+Q(40,11)+Q(6,5)==Q(961,110),'second exact upper cost')
    p('original-Vr83/4',Q(83,4)-Q(65,64)*Q(6727,330));p('original-qenergy39',39-Q(83,4)-18-Q(9,2)*e)
    p('critical-radius97/100',(Q(3,100)-3*e/4)**2-Q(581,32)*e)
    p('sqrt39-25/4',Q(25,4)**2-39);p('sqrt8eta-9/500',Q(9,500)**2-8*e)
    p('original-H42',42-(Q(625,97)+Q(9,500))**2);p('fixed-H-entry',Q(1,512)-42*e)
    # Proved refinement: retain the whole second radial coefficient rather
    # than replacing it by3/7. All previous regions and sign proofs retained.
    gap=Q(32075187,73400320);vcoef=Q(961,110)/gap;Vrcoef=Q(65,64)*vcoef
    qcoef=Vrcoef+18+Q(9,2)*e
    p('refined-qenergy-sqrt619/100',Q(619,100)**2-qcoef)
    p('refined-actual-H41',41-(Q(619,97)+Q(9,500))**2)
    # Fresh widened centered-root conditions. Uses credited universal ordinary
    #9620/9669 identities, never their old endpoint verification as premise.
    rho=Q(1,64);h=Q(1,512);lo=1-e-rho;hi=1+rho;s=hi+h/2;r0=Q(4999,5000);tau=Q(17,384)
    A={j:Q(9*comb(8,9-j),8*j)*rho**(7-j)for j in range(1,7)}|{7:Q(9,14)}
    Cd=sum(j*A[j]*s**(j-1)for j in A);Bd=9*lo**8-18*s**7*h-Cd*h;Nc=Q(7,4)*sum(A[j]*hi**j for j in [1,2,4,5,7]);Be=(s**7/9+Cd/54)/lo**8
    Bs={5:Q(63,32),4:Q(63,32)*rho,2:Q(9,128)*rho*h,1:Q(9,4096)*h*h}
    p('centered-positive-rminus',lo);p('centered-all-criticals-below-anchor',(1-e)**2-h);p('centered-radius17/384',tau*tau-h)
    p('widened-Rouche-whole',9*lo**8/2-9*s**7*h-sum(A[j]*(s**j+hi**j)for j in A));p('widened-Rouche-disjoint',4*lo/9-h)
    p('widened-Bd',Bd);p('widened-delta-W/6',Bd-6*Nc);p('widened-leading-W/6',9*lo**8-6*Nc)
    for c,name in [(Q(1,6),'paired'),(Q(1,5),'individual')]:p('widened-'+name+'-whole-normal',1-(1+2*rho)*Be-Q(1,72)-c*sum(Bs[j]*lo**(j-7)for j in Bs))
    p('widened-initial-reciprocal3/5',Q(3,5)-(Q(1,2)+tau/(lo-tau))/lo**3)
    p('widened-radius4999/5000',Q(1,5000)-(3*e+Q(3,5)*h)/8)
    p('widened-Q-coefficient',Q(3,4)/hi**3-Q(4,7))
    kappa=Q(4,7)-1/(2*r0**3)-tau/((r0-tau)*r0**3)-Q(16,3)*(rho/6+h)
    need(kappa==Q(3827263269609617,8250819527426593824),'whole widened kappa')
    p('widened-firstpower-positive-kappa',kappa-Q(1,2500));p('widened-basic13/5',Q(8,3)-4*e/3-Q(13,5))
    need(Q(8,3)-4*e/3==Q(49999,18750),'uniform first-power slope')
    old=Q(1,6400)-(3*e+Q(3,5)*h)/8;need(old<0,'old radius budget must fail')
    return {'strict_margins':m,'refinement':{'second_full_gap':str(gap),'v_coefficient':str(vcoef),'Vr_coefficient':str(Vrcoef),'reciprocal_energy_coefficient':str(qcoef),'actual_H_coefficient':41},'widened_centered':{'A':{str(j):str(v)for j,v in A.items()},'B_lower':{str(j):str(v)for j,v in Bs.items()},'Cd':str(Cd),'Bd':str(Bd),'Nc':str(Nc),'Be':str(Be),'kappa':str(kappa),'old_radius_budget_negative':str(old)}}

def build():
    return {'schema':1,'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_height':9776,'eta_endpoint':str(END),'polar':polar(),'sector':sectors(),'radial_penalty_five':radial_certificate(),'whole_newton_majorants':[majorants(1),majorants(2)],'budgets':budgets(),'credited_owned_centered_identities':centered.identities()}

def digest(record):return hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def fresh_literal_controls():
    # Owned Gaussian primitives are credited reuse. The following input set,
    # complete product/gradient/Hessian routes and moment checks are fresh.
    g=centered.ga;plus=centered.gadd;scale=centered.gsc;times=centered.gmul;power=centered.gp;total=centered.gsum;conj=centered.gcj;norm=centered.gn
    def product(xs):
        r=g(1)
        for x in xs:r=times(r,x)
        return r
    def elementary(xs,k):
        from itertools import combinations
        return total(product(group)for group in combinations(xs,k))
    def polynomial(xs):
        out=[g(1)]
        for x in xs:
            new=[g(0)for _ in range(len(out)+1)]
            for i,c in enumerate(out):new[i]=plus(new[i],c);new[i+1]=plus(new[i+1],times(c,x))
            out=new
        return out
    cases=[[g(1)]*8,[g(Q(7,8)),g(Q(9,8))]*4,[g(Q(11,10),Q(1,40)),g(Q(9,10),Q(-1,40))]*4,[g(Q(1,2)),g(Q(1,2)),g(Q(1,2)),g(Q(1,2)),g(Q(1,2)),g(Q(1,2)),g(Q(1,2)),g(Q(9,2))],
           [g(1,Q(k-3,80))for k in range(8)],[g(Q(15,16),Q(1,96)),g(Q(17,16),Q(-1,96))]*4,[g(Q(1,2))]*8]
    rows=[]
    for index,qs in enumerate(cases):
        a=Q(1)-Q(index+1,200000);b=1-a*a
        O=scale(total(scale(c,Q(1,k+1))for k,c in enumerate(polynomial([scale(q,-a)for q in qs]))),9)
        Os=scale(total(scale(elementary(qs,k),Q((-a)**k,k+1))for k in range(9)),9)
        need(O==Os,'fresh complete Gaussian origin')
        C=total(scale(elementary(qs,k),Q(a**(8-k)*b**k,k+1))for k in range(9))
        balanced=[g(a)]
        for q in qs:
            nxt=[g(0)for _ in range(len(balanced)+1)]
            for k,c in enumerate(balanced):nxt[k]=plus(nxt[k],scale(c,a));nxt[k+1]=plus(nxt[k+1],scale(times(c,q),b))
            balanced=nxt
        # The initial balanced constant is a, so remove this known factor.
        need(scale(total(scale(c,Q(1,k+1))for k,c in enumerate(balanced)),1/a)==C,'fresh entire Gaussian polar integral')
        grad=[];hess=[]
        for i in range(8):
            subset=[q for j,q in enumerate(qs)if j!=i]
            coeffs=polynomial([scale(q,-a)for q in subset]);direct=scale(total(scale(c,Q(1,k+2))for k,c in enumerate(coeffs)),-9*a)
            symmetric=scale(total(scale(elementary(subset,k),Q((-a)**k,k+2))for k in range(8)),-9*a)
            need(direct==symmetric,'fresh whole Gaussian gradient');grad.append([str(v)for v in direct])
            for j in range(8):
                if i==j:entry=g(0)
                else:
                    ss=[q for k,q in enumerate(qs)if k not in (i,j)];cs=polynomial([scale(q,-a)for q in ss]);entry=scale(total(scale(c,Q(1,k+3))for k,c in enumerate(cs)),9*a*a)
                    alt=scale(total(scale(elementary(ss,k),Q((-a)**k,k+3))for k in range(7)),9*a*a);need(entry==alt,'fresh whole Gaussian ordered Hessian')
                hess.append([i,j,[str(v)for v in entry]])
        rows.append({'index':index,'a':str(a),'q':[[str(v)for v in q]for q in qs],'whole_origin':[str(v)for v in O],'whole_polar':[str(v)for v in C],'whole_gradient':grad,'whole_ordered_Hessian':hess,'actual_disk_feasibility_asserted':False})
    moment=[]
    for k in range(1,8):
        xs=[Q(8-k,128)]*k+[Q(-k,128)]*(8-k);v=sum(x*x for x in xs);p3=sum(x**3 for x in xs);p4=sum(x**4 for x in xs)
        need(sum(xs)==0 and v>0,'fresh two-level balanced control')
        expected=Q((8-2*k)**2,8*k*(8-k));need(p3*p3==expected*v**3 and expected<=Q(9,14),'full two-level skew ratio')
        e4=elementary([g(x)for x in xs],4);need(e4==g(v*v/8-p4/4),'fresh whole fourth-moment Newton identity')
        need(abs(e4[0])<=3*v*v/32,'fresh fourth-moment bound')
        rs=[g(1+x)for x in xs];O=9*total(scale(c,Q(1,j+1))for j,c in enumerate(polynomial([scale(r,-1)for r in rs])))[0];P=product(rs)[0]
        full=total(scale(elementary([g(x)for x in xs],j),Q((-1)**j,comb(8,j))-1)for j in range(2,9))[0]
        need(O-P==full,'fresh whole radial identity');moment.append({'k':k,'coordinates':list(map(str,xs)),'variance':str(v),'skew_ratio_squared':str(expected),'p4':str(p4),'e4':str(e4[0]),'whole_radial_gap':str(full)})
    return {'whole_Gaussian_controls':rows,'two_level_moment_controls':moment}

# The command above is deliberately not the fixture-checking publication
# entry point. validate.py calls complete_build() and checks the full record.
def complete_build():
    out=build();out['fresh_definition_level_controls']=fresh_literal_controls();return out
