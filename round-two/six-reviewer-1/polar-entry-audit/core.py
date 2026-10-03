"""Independent full rational reconstruction of signed LEMMA9930.

Actual six-reviewer-1, independent mathematical reviewer. Written theorem
and proof visible, producer code/record initially unopened. Arithmetic and
cube-field primitives openly reuse this reviewer's earlier published work.
No solver, floating point, researcher import or external mathematical data.
"""
from fractions import Fraction as Q
from math import comb
from itertools import combinations
import hashlib,json
import arithmetic as A
import cube as C
need=A.need;poly=A.poly;atom=A.atom;add=A.add;sc=A.sc;mul=A.mul
pw=A.pw;integrate=A.integrate;ev=A.ev;uni=A.uni;pack=A.pack
E=Q(1,12000)

def positive(m,k,v):
    need(v>0,k);m[k]=str(v)

def polar():
    x,t=atom(0),atom(1);a=add(poly(1),sc(x,-1))
    b=add(poly(1),sc(pw(a,2),-1));L=add(poly(8),sc(x,3))
    terms=[sc(mul(mul(pw(a,8-k),pw(b,k)),pw(sc(L,Q(1,8)),k)),Q(comb(8,k),k+1))for k in range(9)]
    B=integrate(pw(add(a,sc(mul(mul(b,L),t),Q(1,8))),8));T=add(*terms[2:])
    need(B==add(*terms),'full balanced integral / binomial route')
    d=sc(mul(pw(a,7),b),Q(1,2))
    need(B==add(pw(a,8),mul(d,L),T),'full polar decomposition')
    ns=add(poly(1),sc(pw(a,16),-1),sc(mul(pw(d,2),pw(L,2)),-1),sc(mul(add(pw(a,8),mul(d,L)),T),-2),sc(pw(T,2),-1),sc(mul(mul(add(poly(8),sc(x,-Q(11,2))),pw(a,15)),b),-1))
    alt=add(poly(1),sc(pw(B,2),-1),sc(mul(mul(x,pw(a,15)),b),Q(17,2)))
    need(ns==alt,'entire squared-polar cancellation')
    nb=add(poly(1),sc(pw(x,2),9),sc(B,-1))
    nv=add(sc(mul(pw(a,6),pw(b,2)),13),sc(add(B,poly(-1)),-6))
    out={}
    for name,p,degree,head,cut in [('phase',ns,48,Q(1,3),0),('balanced',nb,24,Q(2,3),Q(1,2)),('variance',nv,24,Q(2),1)]:
        cs=uni(p);need(len(cs)==degree+1 and cs[:3]==[0,0,head],'all polar degrees/head '+name)
        lower=cs[2]-sum(abs(c)*E**(k-2)for k,c in enumerate(cs[3:],3))
        need(lower>cut,'whole polar tail '+name)
        out[name]={'coefficients':list(map(str,cs)),'lower_coefficient':str(lower),'cut':str(cut)}
    return {'whole_B':list(map(str,uni(B))),'whole_T':list(map(str,uni(T))),'streams':out}

def faces():
    x,t=atom(0),atom(1);a=add(poly(1),sc(x,-1));rows=[]
    for m in range(1,9):
        f=add(poly(1),a,sc(mul(a,t),-1));g=add(f,sc(mul(pw(a,2),t),Q(-8,m)))
        route1=sc(integrate(mul(pw(f,8-m),pw(g,m))),9)
        c=add(poly(1),x);s2=add(x,sc(pw(x,2),Q(8,m)));route2={}
        for i in range(9-m):
            for j in range(m+1):
                route2=add(route2,sc(mul(mul(pw(c,8-i-j),pw(x,i)),pw(s2,j)),Q(9*comb(8-m,i)*comb(m,j)*(-1)**(i+j),i+j+1)))
        route2=A.sub(route2,a,poly(0));need(route1==route2,'whole face two routes '+str(m))
        dm=Q(64*(m-1),m)-Q(256*(m-1)*(m-2),3*m*m)
        R=add(route1,sc(pw(add(poly(1),sc(a,Q(8,m))),m),-1),poly(-8),sc(pw(a,9),8),sc(pw(a,3),-Q(39,5)*dm))
        cs=uni(R);lead=next(k for k,v in enumerate(cs)if v)
        need(lead==(1 if m in [1,8]else 0),'entire face leading order')
        lower=cs[lead]-sum(abs(v)*E**(k-lead)for k,v in enumerate(cs[lead+1:],lead+1))
        need(lower>0,'closed whole face positivity')
        if m==2:need(ev(add(R,sc(pw(a,3),-Q(1,5)*dm)),0)<0,'penalty8 countercontrol')
        rows.append({'m':m,'whole_coefficients':list(map(str,cs)),'leading_order':lead,'positive_lower':str(lower),'dm':str(dm)})
    return rows

def newton(stage):
    v=atom(0);B={0:poly(1),1:{},2:sc(v,Q(1,2))}
    if stage==1:
        endpoint=Q(1,10);B[3]=sc(v,Q(1,11));B[4]=sc(pw(v,2),Q(3,32))
        for k in range(5,8):
            B[k]=sc(add(mul(v,B[k-2]),sc(mul(v,B[k-3]),Q(3,11)),sc(mul(pw(v,2),add(*(sc(B[k-j],Q(3,10)**(j-4))for j in range(4,k+1)))),Q(7,8))),Q(1,k))
        expected=Q(14208849,38720000)
    else:
        endpoint=Q(1,350);B[3]=sc(v,Q(1,60));B[4]=sc(pw(v,2),Q(3,32))
        for k in range(5,8):B[k]=sc(mul(v,add(*(sc(B[k-j],Q(1,20)**(j-2))for j in range(2,k+1)))),Q(1,k))
        expected=Q(20409329741,43904000000)
    need(all(c>=0 for p in B.values()for c in p.values()),'whole Newton nonnegative coefficients')
    need(all(i>=1 for k in range(2,8)for i,j in B[k]),'legal variance quotient')
    gap=Q(27,56)-sum((1-Q((-1)**k,comb(8,k)))*ev(B[k],endpoint)/endpoint for k in range(3,8))
    need(gap==expected and gap>0,'whole Newton gap '+str(stage))
    return {'stage':stage,'endpoint':str(endpoint),'polynomials':{str(k):pack(v)for k,v in B.items()},'gap':str(gap)}

def budgets():
    e=E;m={};p=lambda k,v:positive(m,k,v)
    sigma=Q(11,2);beta=Q(17,2);mc=Q(11,16)
    bp=beta*(1+sigma*e/4);S=16*bp
    need(bp==Q(1632187,192000) and S==Q(1632187,12000),'complete phase budgets')
    p('uniform-a-99over100',1-e-Q(99,100))
    p('standalone-sum-domain',Q(803,100)-8-3*e)
    p('transfer65over64',Q(65,64)-(1-e)**-2)
    p('mu-upper3over8-below11over16',mc-Q(3,8))
    p('whole-phase-l1-eight',Q(1,64)-2*(8+3*e)*bp*e)
    p('proper-product-gradient2',2-Q(753,700)**7)
    C0=Q(9,16)*bp+Q(3,8)*S+sigma*(Q(2,3)+2)
    need(C0==Q(43287127,614400),'entire origin comparison constant');p('C0-below71',71-C0)
    d0=Q(90880,39)
    p('coarse-E2-above7over4',28*(1-e)**2-26-Q(7,4))
    p('first-D-to-v',Q(8,5)-8*d0*e)
    p('E2-above99over4',28*(1-e)**2-2*Q(8,5)-Q(99,4))
    p('second-D-to-v',Q(11,100)-Q(56,99)*d0*e)
    p('E2-above111over4',28*(1-e)**2-2*Q(11,100)-Q(111,4))
    p('third-D-to-v',Q(1,10)-Q(56,111)*d0*e)
    p('first-radial-l2',Q(8,25)**2-Q(65,64)*Q(1,10)-8*mc*mc*e*e)
    p('first-individual-radius',(Q(3,10)-mc*e)**2-Q(7,8)*Q(65,64)*Q(1,10))
    p('first-radial-norm3',9-8-6*e-Q(65,64)*Q(1,10)-8*mc*mc*e*e)
    p('first-phase-l2',Q(9,200)**2-2*Q(13,10)*bp*e)
    p('first-scaled-whole-path',Q(4,25)-(Q(8,25)+Q(9,200)+3*e)**2)
    p('first-sixfactor-AMGM',Q(1,6)**2-Q(4,25)/6)
    for stage,z,g,h in [(1,Q(1,6),Q(1,5),Q(1,16)),(2,Q(1,24),Q(1,7),Q(1,24))]:
        p('whole-gradient-'+str(stage),g-sum(Q(k+1,8)*z**k for k in range(8)))
        p('whole-Hessian-'+str(stage),h-sum(Q((k+1)*(k+2),56)*z**k for k in range(7)))
    z=Q(1,6);U=1/(8*(1-z)**2)-Q(1,8)-z/4
    p('signed-real-gradient',Q(1,8)-(Q(3,10)+15*e)/28-U-Q(1,10))
    p('complex-path-sign',(1-e)*(1-18*e)/10-Q(1,16)/8)
    p('first-moment-skew',Q(1,121)-Q(1,140))
    c1=Q(newton(1)['gap']);K1=11*Q(1,5)+6+S/32
    need(K1==Q(4780987,384000),'all first cost terms')
    p('first-v34',34*c1-K1);need(33*c1-K1<0,'33eta unsupported negative control')
    p('strict-second-entry',Q(1,350)-34*e)
    # Distinguish moment radius from EVERY actual normalization path.
    need(Q(1,20)**2==Q(7,8)*Q(1,350),'normalized closed moment radius equality')
    p('second-radial-l2',Q(11,200)**2-Q(65,64)*34*e-8*mc*mc*e*e)
    p('second-individual-PATH51over1000',(Q(51,1000)-mc*e)**2-Q(7,8)*Q(65,64)*34*e)
    need((Q(1,20)-mc*e)**2-Q(7,8)*Q(65,64)*34*e<0,'moment radius not all-path radius')
    p('second-phase-l2',Q(1,25)**2-2*Q(1051,1000)*bp*e)
    p('second-scaled-path',Q(1,100)-(Q(11,200)+Q(1,25)+3*e)**2)
    p('second-sixfactor-AMGM',Q(1,24)**2-Q(1,600))
    pg=Q(16,15);p('second-proper-product',pg-((7+Q(51,1000)+3*e)/7)**7)
    K2=Q(11,7)+3*pg+S/48;c2=Q(newton(2)['gap']);Av=K2/c2;Ar=Q(65,64)*Av
    need(K2==Q(30663709,4032000) and Av==Q(3005043482000,183683967669) and Ar==Q(12207989145625,734735870676),'whole retained second coefficients')
    qcoef=Ar+17+8*mc*mc*e
    p('full-q-energy34',34-qcoef)
    p('actual-reciprocal-floor27over28',(Q(1,28)-mc*e)**2-Q(7,8)*Ar*e)
    p('sqrt34-35over6',Q(35,6)**2-34);p('sqrt8e-13over500',Q(13,500)**2-8*e)
    p('original-H37',37-(Q(490,81)+Q(13,500))**2);p('actual-H-entry320',Q(1,320)-37*e)
    # Independent SAME-DOMAIN refinement, retaining the complete q-energy.
    p('improved-qroot29over5',Q(29,5)**2-qcoef)
    improvedH=(Q(812,135)+Q(13,500))**2
    p('improved-actual-H73over2',Q(73,2)-improvedH)
    rho=Q(1,50);h=Q(1,320);tau=Q(21,400);r0=Q(9997,10000)
    lo=1-e-rho;hi=1+rho;s=hi+h/2;Lc=Q(1,2)
    As={j:Q(9*comb(8,9-j),8*j)*rho**(7-j)for j in range(1,7)}|{7:Q(9,14)}
    Cd=sum(j*As[j]*s**(j-1)for j in As);Bd=9*lo**8-36*s**7*Lc*h-Cd*h
    Nc=Q(7,4)*sum(As[j]*hi**j for j in [1,2,4,5,7]);Be=4*s**7/(25*lo**8)+Cd/(45*lo**8)
    Bs={5:Q(63,32),4:Q(63,32)*rho,2:Q(9,128)*rho*h,1:Q(9,4096)*h*h}
    p('mean-below-rho',8*rho*rho-h);p('nu-below-tau',tau*tau-Q(7,8)*h)
    p('root-nonzero-u',lo);p('critical-anchor-simple',(1-e)**2-h)
    p('all9-Rouche-circles',9*lo**8*Lc-36*s**7*Lc*Lc*h-sum(As[j]*(s**j+hi**j)for j in As))
    p('all9-disjoint',Q(4,9)*lo-2*Lc*h);p('positive-full-divisor',Bd)
    p('whole-delta-Wover5',Bd-5*Nc);p('whole-leading-delta-Wover5',9*lo**8-5*Nc)
    p('sqrt3-7over4',Q(7,4)**2-3)
    p('individual-cube1over5',Q(1,25)-Q(1,27))
    p('complete-paired-error4over5',Q(4,5)-(1+2*rho)*Be-Q(1,50)-Q(1,6)*sum(Bs[j]*lo**(j-7)for j in Bs))
    p('complete-individual-error7over8',Q(7,8)-(1+2*rho)*Be-Q(1,50)-Q(1,5)*sum(Bs[j]*lo**(j-7)for j in Bs))
    p('all-degree-tail3over5',Q(3,5)-(Q(1,2)+tau/(lo-tau))/lo**3)
    p('low-cut-reciprocal-radius-r0',1-r0-(3*e+Q(3,5)*h)/8)
    p('complex-trace-positive-coefficient',Q(3,4)/hi**3-Q(4,7))
    bc=Q(4,7)-1/(2*r0**3)-tau/((r0-tau)*r0**3);kappa=bc-Q(976,225)*h
    need(kappa==Q(2266385261714573,1164451364653531500),'entire retained-square coefficient')
    p('retained-square-kappa1over600',kappa-Q(1,600))
    need(bc-Q(16,3)*(rho/5+Q(4,5)*h)<0,'discard-mean negative countercontrol')
    p('unconditional-basic13over5',Q(8,3)-4*e/3-Q(13,5))
    return {'strict_margins':m,'normalization':{'sigma':str(sigma),'beta_prime':str(bp),'S_prime':str(S),'C0':str(C0),'K1':str(K1),'K2':str(K2),'c1':str(c1),'c2':str(c2),'Av':str(Av),'Ar':str(Ar),'q_energy_coefficient':str(qcoef)},'centered':{'A':{str(j):str(v)for j,v in As.items()},'higher_B':{str(j):str(v)for j,v in Bs.items()},'Cd':str(Cd),'Bd':str(Bd),'Nc':str(Nc),'Be':str(Be),'beta':str(bc),'kappa':str(kappa)},'refinement':{'eta_domain':'0<eta<=1/12000','actual_H_coefficient':'73/2','root_norm_upper':'29/5','r_floor':'27/28','complete_H_upper_coefficient':str(improvedH),'no_wider_domain_asserted':True}}

def cube_and_square():
    # Fresh Laurent construction retains every centered coefficient BEFORE
    # reduction; d3,d6 vanish ONLY in the base cubic evaluation.
    u,ub=C.tok('u'),C.tok('bar_u');rows=[]
    for j in range(1,8):
        delta=C.sc(C.prod([C.tok('d'+str(j)),C.tok('u',j-8),C.add(C.phase(j-8),C.sc(C.phase(-8),-1))]),Q(-1,9))
        normal=C.prod([ub,C.phase(-1),delta])
        # Pair omega and omega^2 by direct phase substitution.
        switched={}
        for (ph,k),val in normal.items():switched=C.add(switched,C.sc(C.mul(C.phase(-ph),{(0,k):Q(1)}),val))
        paired=C.sc(C.add(normal,switched),Q(1,2))
        expected={} if j in [3,6]else C.sc(C.prod([C.tok('d'+str(j)),C.tok('u',j-8),ub]),Q(1,6))
        need(paired==expected,'full paired cube coefficient '+str(j))
        rows.append({'j':j,'full_individual':C.pack(normal),'full_pair':C.pack(paired)})
    t,w=atom(0),atom(1)
    raw=add(sc(pw(t,2),4),sc(mul(t,w),-Q(16,15)),sc(pw(w,2),-Q(64,15)))
    square=add(sc(pw(add(t,sc(w,-Q(2,15))),2),4),sc(pw(w,2),-Q(976,225)))
    need(raw==square,'whole mean square identity')
    return {'all7_coefficients':rows,'whole_original_square':pack(raw),'whole_completed_square':pack(square)}

def literal_controls():
    g=A.ga;plus=A.gadd;times=A.gmul;scale=A.gsc;total=A.gsum
    def product(xs):
        out=g(1)
        for x in xs:out=times(out,x)
        return out
    def el(xs,k):return total(product(c)for c in combinations(xs,k))
    def prodpoly(xs):
        p=[g(1)]
        for x in xs:
            n=[g(0)for _ in range(len(p)+1)]
            for k,c in enumerate(p):n[k]=plus(n[k],c);n[k+1]=plus(n[k+1],times(c,x))
            p=n
        return p
    cases=[[g(Q(1,2))]*7+[g(Q(9,2))],[g(Q(49,48),Q(1,96)),g(Q(47,48),Q(-1,96))]*4,[g(Q(27+j,32),Q((-1)**j,127))for j in range(8)]]
    rows=[]
    for idx,qs in enumerate(cases):
        a=1-E/(idx+1);b=1-a*a
        origin=scale(total(scale(c,Q(1,k+1))for k,c in enumerate(prodpoly([scale(q,-a)for q in qs]))),9)
        need(origin==scale(total(scale(el(qs,k),Q((-a)**k,k+1))for k in range(9)),9),'full literal origin')
        polar=total(scale(el(qs,k),Q(a**(8-k)*b**k,k+1))for k in range(9))
        cp=[g(1)]
        for q in qs:
            nxt=[g(0)for _ in range(len(cp)+1)]
            for k,c in enumerate(cp):nxt[k]=plus(nxt[k],scale(c,a));nxt[k+1]=plus(nxt[k+1],scale(times(c,q),b))
            cp=nxt
        need(polar==total(scale(c,Q(1,k+1))for k,c in enumerate(cp)),'full literal polar')
        grad=[];hess=[]
        for i in range(8):
            ss=[q for j,q in enumerate(qs)if j!=i]
            v=scale(total(scale(c,Q(1,k+2))for k,c in enumerate(prodpoly([scale(q,-a)for q in ss]))),-9*a)
            need(v==scale(total(scale(el(ss,k),Q((-a)**k,k+2))for k in range(8)),-9*a),'all8 literal gradients');grad.append(list(map(str,v)))
            for j in range(8):
                v=g(0)
                if i!=j:
                    ss=[q for k,q in enumerate(qs)if k not in [i,j]]
                    v=scale(total(scale(c,Q(1,k+3))for k,c in enumerate(prodpoly([scale(q,-a)for q in ss]))),9*a*a)
                    need(v==scale(total(scale(el(ss,k),Q((-a)**k,k+3))for k in range(7)),9*a*a),'all64 literal Hessian entries')
                hess.append([i,j,list(map(str,v))])
        # Whole anchored centered polynomial from actual critical-coordinate
        # translation and independent direct integration; all10 coefficients.
        zs=[plus(g(a),scale((q[0]/A.gn(q),-q[1]/A.gn(q)),-1))for q in qs]
        mean=scale(total(zs),Q(1,8));nus=[plus(z,scale(mean,-1))for z in zs];u=plus(g(a),scale(mean,-1))
        rp=A.gpoly(zs);p=[g(0)]+[scale(rp[j-1],Q(9,j))for j in range(1,10)];p[0]=scale(A.ge(p,g(a)),-1)
        np=A.gpoly(nus);c=[g(0)]+[scale(np[j-1],Q(9,j))for j in range(1,10)];c[0]=scale(A.ge(c,u),-1)
        shifted=[g(0)for _ in range(10)]
        for j,v in enumerate(c):
            for k in range(j+1):shifted[k]=plus(shifted[k],scale(times(v,A.gp(scale(mean,-1),j-k)),comb(j,k)))
        need(p==shifted and c[8]==g(0),'all10 centered translation coefficients')
        need(c[7]==scale(total(A.gp(z,2)for z in nus),Q(-9,14)) and c[6]==scale(total(A.gp(z,3)for z in nus),Q(-1,2)),'entire centered d7,d6')
        rows.append({'index':idx,'a':str(a),'q':[list(map(str,q))for q in qs],'origin':list(map(str,origin)),'polar':list(map(str,polar)),'all8_gradient':grad,'all64_Hessian':hess,'all10_original_coefficients':[list(map(str,z))for z in p],'all10_centered_coefficients':[list(map(str,z))for z in c],'actual_disk_feasibility_asserted':False})
    moments=[]
    for k in range(1,8):
        xs=[Q(8-k,384)]*k+[Q(-k,384)]*(8-k);v=sum(x*x for x in xs);p3=sum(x**3 for x in xs);p4=sum(x**4 for x in xs)
        e4=el([g(x)for x in xs],4)[0];ratio=Q((8-2*k)**2,8*k*(8-k))
        need(p3*p3==ratio*v**3 and ratio<=Q(9,14),'all7 twolevel cubic extrema controls')
        need(e4==v*v/8-p4/4 and abs(e4)<=3*v*v/32,'whole e4 moment')
        rs=[g(1+x)for x in xs]
        gap=scale(total(scale(c,Q(1,j+1))for j,c in enumerate(prodpoly([scale(r,-1)for r in rs]))),9)[0]-product(rs)[0]
        need(gap==sum((Q((-1)**j,comb(8,j))-1)*el([g(x)for x in xs],j)[0]for j in range(2,9)),'whole radial degree8 identity')
        moments.append({'k':k,'x':list(map(str,xs)),'variance':str(v),'cubic_ratio_squared':str(ratio),'e4':str(e4),'whole_gap':str(gap)})
    return {'Gaussian':rows,'all7_twolevel_controls':moments}

def build():
    return {'schema':1,'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_height':9930,'eta_endpoint':str(E),'polar':polar(),'faces':faces(),'Newton':[newton(1),newton(2)],'budgets':budgets(),'cube_square':cube_and_square(),'definition_level':literal_controls()}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def typed(a,b):
    need(type(a)is type(b),'whole record type')
    if isinstance(a,dict):
        need(a.keys()==b.keys(),'whole record key set')
        for k in a:typed(a[k],b[k])
    elif isinstance(a,list):
        need(len(a)==len(b),'whole record length')
        for x,y in zip(a,b):typed(x,y)
    else:need(a==b,'whole record scalar')
def load(path):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
        return d
    def invalid(v):raise ValueError('nonfinite JSON')
    return json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=invalid)
if __name__=='__main__':
    from pathlib import Path
    import sys
    d=build();target=Path(sys.argv[1])if len(sys.argv)>1 and sys.argv[1]!='--write'else Path(__file__).with_name('EXPECTED.json')
    if '--write'in sys.argv:target.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    else:typed(d,load(target))
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','whole_record_sha256':digest(d),'polar_coefficients':sum(len(v['coefficients'])for v in d['polar']['streams'].values()),'faces':len(d['faces']),'strict_margins':len(d['budgets']['strict_margins']),'Gaussian_controls':len(d['definition_level']['Gaussian']),'whole_cube_coefficients':len(d['cube_square']['all7_coefficients'])},sort_keys=True))
