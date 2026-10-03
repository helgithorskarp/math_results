"""six-reviewer-1: fresh Fraction reconstruction from the written 9954 proof.

No target executable, fixture, numerical output or old receiving budget imported.
Sparse multivariate and cyclotomic arithmetic are independently implemented here.
Ordinary Rouché, Maclaurin, convergence and domain implications are in PROOF.md.
"""
from fractions import Fraction as F
from math import comb
import json, hashlib, sys

def need(v, msg):
    if not v:
        raise ValueError(msg)

def clean(p):
    return {k:v for k,v in p.items() if v}

def con(v):
    return {():F(v)} if v else {}

def var(n, degree=1):
    return {((n,degree),):F(1)} if degree else con(1)

def add(*ps):
    r={}
    for p in ps:
        for k,v in p.items():
            r[k]=r.get(k,F(0))+v
    return clean(r)

def scale(p,v):
    return clean({k:c*v for k,c in p.items()})

def mul(p,q):
    r={}
    for k,c in p.items():
        for l,d in q.items():
            z=dict(k)
            for n,e in l:
                z[n]=z.get(n,0)+e
            z=tuple(sorted((n,e) for n,e in z.items() if e))
            r[z]=r.get(z,F(0))+c*d
    return clean(r)

def power(p,n):
    r=con(1)
    for _ in range(n):
        r=mul(r,p)
    return r

def pack(p):
    return [[[n,e] for n,e in k]+[str(v)] for k,v in sorted(p.items())]

def subtract(p,q):
    return add(p,scale(q,-1))

def equal(p,q,msg,records):
    need(p==q,msg)
    records[msg]=pack(p)

# Q[w]/(w^6+w^3+1), all six coordinates explicitly retained.
def phase(n):
    n%=9
    a=[F(0)]*6
    if n<6:
        a[n]=F(1)
    else:
        a[n-6]=F(-1);a[n-3]=F(-1)
    return tuple(a)

def fa(x,y):
    return tuple(a+b for a,b in zip(x,y))

def fs(x,c):
    return tuple(a*c for a in x)

def fm(x,y):
    r=(F(0),)*6
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            r=fa(r,fs(phase(i+j),a*b))
    return r

def fc(x):
    r=(F(0),)*6
    for i,a in enumerate(x):
        r=fa(r,fs(phase(-i),a))
    return r

def fi(x):
    need(any(x),'nonzero field denominator')
    cols=[fm(x,phase(j)) for j in range(6)]
    rows=[[cols[j][i] for j in range(6)]+[F(i==0)] for i in range(6)]
    for col in range(6):
        pivot=next(i for i in range(col,6) if rows[i][col])
        rows[col],rows[pivot]=rows[pivot],rows[col]
        z=rows[col][col];rows[col]=[q/z for q in rows[col]]
        for i in range(6):
            if i!=col:
                z=rows[i][col];rows[i]=[q-z*r for q,r in zip(rows[i],rows[col])]
    out=tuple(r[-1] for r in rows)
    need(fm(x,out)==phase(0),'complete field inverse')
    return out

def build(damage=None):
    e=F(1,12000);a=1-e;v=5*e;rho=F(1,128);h=F(1,320)
    if damage=='old_rms':
        rho=F(1,160)
    margins={};maps={};fields={}
    def positive(name,x):
        need(x>0,name);margins[name]=str(x)
    def zero(name,x):
        need(x==0,name);maps[name]=str(x)
    def setup(name,l,rp,cap,rms,mean,b,paired,individual,all_phase=None):
        A={j:F(9,8*j)*comb(8,9-j)*rms**(7-j) for j in range(1,7)}
        A[7]=F(9,14)
        s=rp+cap/2
        cd=sum((j*A[j]*s**(j-1) for j in A),F(0))
        bd=9*l**8-18*s**7*cap-cd*cap
        nc=F(7,4)*sum((A[j]*rp**j for j in (1,2,4,5,7)),F(0))
        n=2*sum((A[j]*rp**j for j in A),F(0))
        positive(name+'_RMS',8*rms**2-cap)
        positive(name+'_Rouchetaylor',9*l**8/2-9*s**7*cap-sum((A[j]*(s**j+rp**j) for j in A),F(0)))
        positive(name+'_disjoint',F(4,9)*l-cap)
        positive(name+'_derivative',bd)
        for tag,z,f in [('cube',nc,b),('all',n,F(1,4) if all_phase is not None else F(1,2))]:
            positive(name+'_'+tag+'_actual',f*bd-z)
            if tag=='cube' or all_phase is not None:
                positive(name+'_'+tag+'_linear',9*f*l**8-z)
        B={j:F(9,j)*comb(8,9-j)/64*((cap/8)**((9-j)//2-2))*
              (rms if (9-j)%2 else 1) for j in range(1,6)}
        # Reconstruct Maclaurin V^2 factors from q=9-j, including odd q.
        need(B[5]==F(63,32),'B5 exact')
        need(B[4]==F(63,32)*rms,'B4 exact')
        need(B[3]==F(21,128)*cap,'B3 exact')
        need(B[2]==F(9,128)*rms*cap,'B2 exact')
        need(B[1]==F(9,4096)*cap**2,'B1 exact')
        def displacement(z):
            return 4*s**7*z*z/l**8+z*cd/(9*l**8)
        lower=sum((B[j]*l**(j-7) for j in (1,2,4,5)),F(0))
        # For broad cube sqrt(3)/9 < 1/5 also; paired exactly1/6.
        pair=(mean+rp)*displacement(b)+b*b/2+lower/6
        indiv=(mean+rp)*displacement(b)+b*b/2+lower/5
        positive(name+'_paired_normal',paired-pair)
        positive(name+'_individual_normal',individual-indiv)
        if all_phase is not None:
            z=F(1,4);lower_all=sum((B[j]*l**(j-7) for j in B),F(0))
            full=(mean+rp)*displacement(z)+z*z/2+F(2,9)*lower_all
            positive(name+'_all_normal',all_phase-full)
            positive(name+'_all_nonT_motion',1-displacement(z)-F(2,9)/l*lower_all)
        maps[name+'_A']={str(j):str(A[j]) for j in sorted(A)}
        maps[name+'_B']={str(j):str(B[j]) for j in sorted(B)}
        maps[name+'_whole_budgets']={k:str(z) for k,z in
            dict(s=s,cd=cd,bd=bd,nc=nc,n=n,pair=pair,individual=indiv).items()}
        return pair,indiv

    # BROAD is legal only after actual entry9930, as confirmed by9956.
    lb=1-e-F(1,50);rp=1+F(1,50);tb=F(21,400)
    setup('broad',lb,rp,h,F(1,50),F(1,50),F(1,5),F(4,5),F(7,8))
    positive('broad_tail_radius',tb*tb-F(7,8)*h)
    positive('broad_tail_denominator',lb-tb)
    positive('broad_reciprocal_coefficient',F(3,5)-1/(2*lb**3)-tb/((lb-tb)*lb**3))
    positive('entry_H37_to_fixed',h-37*e)
    positive('B_to_t_h',(h-F(2,15)*h)**2-e/12-e**2/3)
    positive('sqrt_eta',1-F(109)**2*e)
    positive('sqrt_mean',F(361,1250)**2-F(1,12)-e/3)
    positive('early_t2',F(1,8)-(F(74,15*109)+F(361,1250))**2)
    ap=37*h/5+F(4,5)*37**2*e
    ai=37*h/5+F(7,8)*37**2*e
    positive('early_r_upper',6-(-F(2,3)+F(37,7)+F(4,3)*ap))
    positive('early_M_upper',3-F(1,16)/a-F(3,40)*37)
    positive('early_M_lower',4-(1+F(3,16)+F(111,28)+ap)/(F(3,2)*a))
    re=1-F(141,40)*e
    positive('early_inverse_cube',11-3*F(141,40)/re**4)
    positive('early_imaginary_slack',F(3,5)-F(1,16)-(F(45,16)+F(21,8)*37)*e-F(3,16)*37*tb/((re-tb)*re**3)-ai)
    positive('early_D',F(15,4)-(F(37,14)+F(7,10))/a)
    positive('early_complex_mean',F(11,2)**2-4**2-F(15,4)**2)

    def contraction(name,l,tau,L,previous,next_):
        positive(name+'_radius',tau*tau-F(7,8)*previous*e)
        positive(name+'_denominator',l-tau)
        K=F(3,2)/l**4;G=1/((l-tau)*l**4)
        B=F(976,225)+F(7,8)*(G+F(7,10)*K*K)
        z=F(1,14)-L*e-previous*e*B
        positive(name+'_positive_divisor',z)
        positive(name+'_contraction',next_*z-F(1,3)-F(4,3)*e)
        maps[name+'_constants']={k:str(z) for k,z in dict(K=K,G=G,B=B,divisor=z).items()}
    contraction('37_to7',re,tb,11,37,7)
    positive('final_r_lower',1-(3+F(3,5)*7)/8)
    bp=F(77,10)+F(196,5)
    positive('final_r_upper',2+F(2,3)-e/3-1-F(4,3)*bp*e)
    positive('final_inverse_cube',4-3/a**4)
    contraction('7_to5',a,F(23,1000),4,7,5)
    setup('fine_preliminary',a,1+e,v,rho,F(11,2)*e,F(1,6),F(9,16),F(5,8),F(7,8))
    positive('fine_tail',F(1,50)**2-F(7,8)*v)
    qt=F(1,50)/((a-F(1,50))*a**3)
    np=F(11,2)*5/6+25*F(9,16)
    ni=F(11,2)*5/6+25*F(5,8)
    zero('preliminary_paired',np-F(895,48))
    zero('preliminary_individual',ni-F(485,24))
    positive('joint13',13-F(28,3)-(F(112,3)+560)*e-140*qt-F(448,3)*np*e)
    positive('conic_J',F(64,9)-F(169,24))
    positive('fine_individual_slack',F(1,10)-F(1,16)-(F(45,16)+F(105,16))*e-F(15,16)*qt-ni*e)
    positive('final_D',F(1,3)-(F(4,21)+F(7,60))/a)
    positive('final_M_lower',F(4,5)-(F(2,3)+F(13,168)+F(2,3)*np*e)/a)
    positive('final_M_negative',a*a/4-1/(16*a))
    zero('final_complex_mean',F(13,15)**2-F(4,5)**2-F(1,3)**2)
    setup('receiving',a,1+e,v,rho,F(13,15)*e,F(1,6),F(9,16),F(5,8),F(7,8))
    r3=F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)*5/6+25*F(9,16)
    r4=F(1,2)+2*F(4,5)+2*F(169,225)+F(13,15)*5/4+25*F(7,8)
    zero('R3_exact',r3-F(63401,3600));zero('R4_exact',r4-F(47809,1800))
    positive('R3_rounding',18-r3);positive('R4_rounding',27-r4)
    positive('E3_rounding',17-F(13,15)*5/6-25*F(5,8))
    tau=F(1,50)
    if damage=='old_tail':
        tau=F(1,60)
    positive('receiving_tail_radius',tau*tau-F(7,8)*v)
    G=1/((a-tau)*a**4)
    conversion=8*F(4,5)*(2-e)/a**2+4*F(169,225)/a**3+20
    positive('conversion',36-conversion)
    c0,c1=F(15,16),F(47,50)
    positive('cosine_lower_sign',-(8*c0**3-6*c0-1))
    positive('cosine_upper_sign',8*c1**3-6*c1-1)
    wlo=F(625,1067);whi=F(3,5);b=F(271,200)
    positive('A_positive',1/(1+e)**4-whi/(12*a))
    positive('A_upper',1-1/a**4+wlo/(12*(1+e)))
    positive('beta_minus_A',1/(2*(1+e)**4)-whi/(6*a))
    positive('beta_upper',b-F(3,2)/a**4+wlo/(4*(1+e)))
    k=F(3,4)*b*b;q=b*(1+b)/4
    zero('k_exact',k-F(220323,160000))
    for name,delta,lam in [('physical',F(1,4),F(69,50)),('objective',F(1,2),F(69,100))]:
        aa=delta*delta-q*v;bb=delta*lam-k/2
        positive(name+'_square_a',aa)
        positive(name+'_square_det',aa*lam*lam-bb*bb)
        cost=135+25*(F(7,8)*G+lam)
        positive(name+'_stated_cost',(192 if name=='physical' else 175)-cost)
        refined=36+F(23,5)*r3+F(3,5)*r4+25*(F(7,8)*G+lam)
        positive(name+'_refined_cost',(190 if name=='physical' else 173)-refined)
        maps[name+'_costs']={n:str(z) for n,z in dict(a0=aa,b0=bb,cost=cost,refined=refined).items()}
    zero('noncubic_rounded_equality',36+18*F(23,5)+27*F(3,5)-135)
    positive('firstpower_slope',F(826,291)-175*e-F(141,50))
    positive('sqrt192',192-F(27,2)**2)
    positive('L3_stability',F(3,8)-F(1,4)-F(18,192))
    positive('L4_stability',F(1,2)-F(27,192)-5/(27*a))
    mcost=F(62,651)*F(3,8)+F(128,217)*F(5,2)
    qcost=F(24832,32550)*F(3,8)+F(128,217)*F(5,2)
    positive('Cramer_M',F(8,5)-mcost)
    positive('Cramer_Q',F(9,5)-qcost)
    positive('Q_rounding',26-14*qcost)
    positive('H_stability',1-8*F(169,225)/192)
    positive('D_sqrt',1-F(80)/(14*a)**2)
    positive('D_Delta',1-F(7,24)/a)
    positive('D_eta2',31-F(7,6)*26/a)
    positive('unrotated_real_energy',1-(F(384,25)+4*e/a**2)/192)
    positive('original_motion_delta',F(19,2)-F(26,5)-F(26,7)/a-F(88,192))
    positive('original_motion_sqrt',F(7,2)-2-F(9,7)/a-F(7,81)/a**2)
    positive('original_motion_eta',88-62-25-F(896,1395)/a)
    positive('mu3',F(21,2)**2-F(7,8)*5**3)
    # The unrounded proof gives173/190, including every stability denominator.
    positive('refined_sqrt190',190-F(27,2)**2)
    positive('refined_L3',F(3,8)-F(1,4)-F(18,190))
    positive('refined_L4',F(1,2)-F(27,190)-5/(27*a))
    positive('refined_H',1-8*F(169,225)/190)
    positive('refined_real_energy',1-(F(384,25)+4*e/a**2)/190)
    positive('refined_motion_delta',F(19,2)-F(26,5)-F(26,7)/a-F(88,190))

    # Independently selected rational cosine interval and whole exact dual.
    def w3_at(c):
        dd=2*c*c-1
        return F(2,3)*(7-(1-dd)/(c+dd))
    positive('w3_lower',w3_at(c0)-4)
    positive('w3_upper',F(23,5)-w3_at(c1))
    positive('w4_upper',whi-1/(c0+2*c0*c0-1))
    zero('determinant_lower_endpoint',F(3,2)*(c0+2*c0*c0-1)-F(651,256))
    zero('B4_upper_endpoint',1-(2*c0*c0-1)-F(31,128))
    zero('A4_upper_endpoint',1+c1-F(97,50))
    cc=fs(fa(phase(4),phase(-4)),F(-1,2))
    dd=fs(fa(phase(1),phase(-1)),F(1,2))
    one=phase(0)
    def field_eq(name,left,right):
        need(left==right,name);maps[name]=list(map(str,left))
    field_eq('cosine_cubic',fa(fa(fs(fm(fm(cc,cc),cc),8),fs(cc,-6)),fs(one,-1)),(F(0),)*6)
    field_eq('double_angle',dd,fa(fs(fm(cc,cc),2),fs(one,-1)))
    yy=fs(fi(fa(one,cc)),F(1,3));xx=fa(fs(one,F(2,3)),fs(yy,-1))
    ww4=fi(fa(cc,dd))
    ww3=fs(fa(fs(one,7),fs(fm(fa(one,fs(dd,-1)),ww4),-1)),F(2,3))
    A3=B3=fs(one,F(3,2));A4=fa(one,cc);B4=fa(one,fs(dd,-1))
    field_eq('dual_M',fa(fm(ww3,A3),fm(ww4,A4)),fs(one,8))
    field_eq('dual_Q',fa(fm(ww3,B3),fm(ww4,B4)),fs(one,7))
    field_eq('dual_C',fa(fa(fs(one,8),fs(ww3,-1)),fs(ww4,-1)),fa(fs(one,F(8,3)),yy))
    field_eq('profile_cube',fa(fm(A3,xx),fm(B3,yy)),one)
    field_eq('profile_four',fa(fm(A4,xx),fm(B4,yy)),one)
    field_eq('Cramer_determinant',fa(fm(A3,B4),fs(fm(A4,B3),-1)),fs(fa(cc,dd),F(-3,2)))

    # Full Taylor identity, no degree truncated.
    z=var('z');d=var('d');w=var('w')
    lhs=subtract(subtract(power(add(z,d),9),power(z,9)),scale(mul(power(z,8),d),9))
    rhs={}
    for j in range(8):
        rhs=add(rhs,scale(mul(power(z,7-j),power(d,j+2)),F(72)*comb(7,j)/((j+1)*(j+2))))
    equal(lhs,rhs,'ninth_power_integral_Taylor',maps)
    for j in range(1,8):
        lhs=subtract(power(add(z,d),j),power(z,j))
        rhs=mul(d,add(*(mul(power(add(z,d),j-1-i),power(z,i)) for i in range(j))))
        equal(lhs,rhs,'lower_telescoping_'+str(j),maps)
    # Universal square completions and conic: symbolic polynomials.
    E=var('E');V=var('V');t=var('t');S=var('sqrtE')
    equal(subtract(scale(power(t,2),4),scale(mul(t,V),F(16,15))),
          subtract(scale(power(subtract(t,scale(V,F(2,15))),2),4),scale(power(V,2),F(16,225))),
          'mean_square',maps)
    K=var('K');W=var('W')
    equal(subtract(scale(power(S,2),F(5,14)),mul(mul(K,W),S)),
          subtract(scale(power(subtract(S,scale(mul(K,W),F(7,5))),2),F(5,14)),
                   scale(power(mul(K,W),2),F(7,10))),'real_energy_square',maps)
    Q=var('Q');eta=var('eta')
    equal(subtract(power(scale(subtract(scale(eta,13),scale(Q,5)),F(1,7)),2),power(Q,2)),
          subtract(scale(power(eta,2),F(169,24)),scale(power(add(Q,scale(eta,F(65,24))),2),F(24,49))),
          'joint13_conic',maps)
    for name,delta,lam in [('physical',F(1,4),F(69,50)),('objective',F(1,2),F(69,100))]:
        aa=delta*delta-q*v;bb=delta*lam-k/2
        left=subtract(power(add(scale(E,delta),scale(power(V,2),lam)),2),
                      mul(E,add(scale(power(V,2),k),scale(mul(E,V),q))))
        right=add(scale(power(add(E,scale(power(V,2),bb/aa)),2),aa),
                  scale(power(V,4),lam*lam-bb*bb/aa),
                  scale(mul(subtract(con(v),V),power(E,2)),q))
        equal(left,right,name+'_full_PSD_square',maps)
    X=var('X');Y=var('Y')
    norm=add(power(X,2),power(Y,2))
    equal(subtract(scale(mul(power(X,2),power(norm,2)),9),
                   power(subtract(power(X,3),scale(mul(X,power(Y,2)),3)),2)),
          add(scale(power(X,6),8),scale(mul(power(X,4),power(Y,2)),24)),
          'whole_real_cubic_control',maps)
    equal(subtract(scale(mul(power(X,2),power(norm,2)),F(9,4)),
                   power(subtract(power(X,3),scale(mul(X,power(Y,2)),F(3,2))),2)),
          add(scale(power(X,6),F(5,4)),scale(mul(power(X,4),power(Y,2)),F(15,2))),
          'whole_Legendre_cubic_control',maps)
    # Whole zero-sum complex quartic SOS, fourteen free real variables.
    xs=[var('x'+str(i)) for i in range(7)];ys=[var('y'+str(i)) for i in range(7)]
    xs.append(scale(add(*xs),-1));ys.append(scale(add(*ys),-1))
    ns=[add(power(x,2),power(y,2)) for x,y in zip(xs,ys)]
    VV=add(*ns);EE=add(*(power(x,2) for x in xs))
    S4=add(*(power(n,2) for n in ns))
    sos={}
    for j in range(8):
        inner={}
        for k1 in range(8):
            for k2 in range(k1+1,8):
                if j in (k1,k2):
                    continue
                inner=add(inner,power(subtract(xs[k1],xs[k2]),2),power(subtract(ys[k1],ys[k2]),2))
        equal(inner,subtract(scale(VV,7),scale(ns[j],8)),'quartic_inner_'+str(j),maps)
        sos=add(sos,mul(ns[j],inner))
    equal(subtract(scale(power(VV,2),7),scale(S4,8)),sos,'whole_complex_zero_sum_quartic',maps)
    # Generic variance decomposition in scalar aggregate variables: no n=8 test substitute.
    aa=var('A');bb=var('beta');ee=var('E');vv=var('V');s4=var('S4');x4=var('X4');xy=var('X2Y2')
    sumf=subtract(mul(add(aa,bb),ee),mul(bb,vv))
    sumf2=subtract(subtract(mul(power(bb,2),s4),mul(subtract(power(bb,2),power(aa,2)),x4)),
                   scale(mul(mul(bb,add(aa,bb)),xy),2))
    variance=subtract(sumf2,scale(power(sumf,2),F(1,8)))
    bracket=add(scale(mul(power(bb,2),power(vv,2)),F(3,4)),
                scale(mul(mul(mul(bb,add(aa,bb)),ee),subtract(vv,ee)),F(1,4)))
    difference=add(mul(power(bb,2),subtract(scale(power(vv,2),F(7,8)),s4)),
                   mul(subtract(power(bb,2),power(aa,2)),subtract(x4,scale(power(ee,2),F(1,8)))),
                   scale(mul(mul(bb,add(aa,bb)),xy),2))
    equal(subtract(bracket,variance),difference,'universal_joint_cubic_variance',maps)
    # All nine whole phases and every lower coefficient.
    # Principal normal is -Re[d_j bar(u)/u^(8-j)*(w^j-1)]/9.
    for kphase in range(9):
        rows={}
        for j in range(1,8):
            diff=fa(phase(kphase*j),fs(phase(0),-1))
            avg=fs(fa(diff,fc(diff)),F(-1,18))
            # Independent average of k and -k individual factors.
            paired=fs(fa(fa(phase(kphase*j),phase(-kphase*j)),fs(phase(0),-2)),F(-1,18))
            need(avg==paired,'phase paired average')
            rows[str(j)]={'individual':list(map(str,fs(diff,F(-1,9)))),
                          'paired':list(map(str,paired)),
                          'displacement':list(map(str,fa(phase(kphase*(j-8)),fs(phase(kphase),-1))))}
            if kphase in (3,6) and j in (3,6):
                need(all(x==0 for x in diff),'cube cancellations')
        fields[str(kphase)]=rows
    if damage=='drop_d3':
        fields['4'].pop('3')
    need(set(fields['4'])==set(map(str,range(1,8))),'all lower coefficients including d3 at phase4')
    need(fields['3']['6']['paired']==['0']*6,'cube cubic vanishes')
    need(fields['4']['6']['paired']==['1/6']+['0']*5,'phase4 cubic multiplier')
    # Since d6=-U3/2, preceding1/6 gives NEGATIVE1/12.
    signed=F(-1,12) if damage!='flip_cubic' else F(1,12)
    zero('phase4_signed_cubic',signed+F(1,12))
    failures={'old_rms':str(8*F(1,160)**2-v),
              'old_tail':str(F(1,60)**2-F(7,8)*v),
              'old_tail_at_V7':str(F(1,50)**2-F(7,8)*7*e),
              'old_scalar_t2':str(F(1,9)-(F(74,15*109)+F(361,1250))**2)}
    need(all(F(z)<0 for z in failures.values()),'retired comparisons really fail')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'endpoint':str(e),'margins':margins,'maps':maps,'all9_phase_maps':fields,
            'preserved_invalid_comparisons':failures}

def canonical(r):
    return json.dumps(r,sort_keys=True,separators=(',',':')).encode()

if __name__=='__main__':
    r=build(sys.argv[1] if len(sys.argv)>1 else None)
    print(json.dumps(r,sort_keys=True,indent=2))
