"""Fresh actual complex anchored-domain, reciprocal and bootstrap audit.
Own earlier sparse-polynomial kernel is credited; no target code/fixture.
Finite series corroborate, never replace, the written all-orders argument.
"""
from fractions import Fraction as Q
from math import comb
from algebra import P,vars,zero


def need(ok,label):
    if not ok:raise ValueError(label)


def polycoefficient(p,j,k):return p.d.get((j,k),Q(0))


# Q[i,w]/(i^2+1,w^2+w+1), basis 1,i,w,iw. The involution changes
# BOTH i and w; reflected original roots need not be conjugate roots.
RZERO=(Q(0),)*4;RONE=(Q(1),Q(0),Q(0),Q(0))
I=(Q(0),Q(1),Q(0),Q(0));W=(Q(0),Q(0),Q(1),Q(0))
def ra(x,y):return tuple(a+b for a,b in zip(x,y))
def rs(x,c):return tuple(a*c for a in x)
def rm(x,y):
    out=[Q(0)]*4
    for j,a in enumerate(x):
        for k,b in enumerate(y):
            ie=j%2+k%2;we=j//2+k//2;v=a*b*(-1 if ie==2 else 1);ie%=2
            if we==2:
                out[ie]-=v;out[ie+2]-=v
            else:out[ie+2*we]+=v
    return tuple(out)
def rp(x,n):
    out=RONE
    for _ in range(n):out=rm(out,x)
    return out
def star(x):
    out=RZERO
    for j,a in enumerate(x):
        b=rm(rp(rs(I,-1),j%2),rp(ra(rs(W,-1),rs(RONE,-1)),j//2))
        out=ra(out,rs(b,a))
    return out
def rr(x):return list(map(str,x))


def paired_original():
    symbols=vars(17);eta=symbols[0];xs=symbols[1:9];ys=symbols[9:17];a=1-eta
    left=rs(RONE,1-a**9);right=rs(RONE,1-a**9);table=[]
    for j,(x,y) in enumerate(zip(xs,ys),1):
        w=rp(W,j);wr=rp(star(W),j);avg=rs(ra(w,wr),Q(1,2))
        need(avg==(RONE if j%3==0 else rs(RONE,-Q(1,2))),'complete cube phase table')
        c=(x,y,P(17,0),P(17,0))
        left=ra(left,rm(c,ra(w,rs(RONE,-a**j))))
        right=ra(right,rm(c,ra(wr,rs(RONE,-a**j))))
        table.append({'j':j,'phase':rr(w),'reflected_phase':rr(wr),'average':rr(avg)})
    avg=rs(ra(left,right),Q(1,2))
    zero(avg[2],'all complex paired omega coefficient');zero(avg[3],'all complex paired iomega coefficient')
    C=sum((xs[j-1] for j in [1,2,4,5,7,8]),P(17,0))
    target=1-a**9-Q(3,2)*C+sum((xs[j-1]*(1-a**j) for j in range(1,9)),P(17,0))
    zero(avg[0]-target,'whole anchored complex original paired real equation')
    # Weighted order counts each capped coefficient as eta order1.
    # No unanchored c0 substitution or free coefficient O(eta^2) claim.
    residual=avg[0]/9-eta+C/6
    need(all(sum(ex)>=2 for ex in residual.d),'entire paired anchored weighted residual order2')
    return {'complete_phase_table':table,'entire_mean_real_original_value':avg[0].record(),'entire_mean_imag_original_value':avg[1].record(),'entire_anchored_mean_residual':residual.record(),'complex_imaginary_coefficients_cancel_from_mean_real':True}


def identities():
    z,eta,*cs=vars(10);a=1-eta
    p=z**9-a**9+sum((c*(z**j-a**j) for j,c in enumerate(cs,1)),P(10,0))
    zero(p.sub([a,eta,*cs]),'whole actual anchor')
    pa=p.diff(0).sub([a,eta,*cs]);paa=p.diff(0).diff(0).sub([a,eta,*cs])
    trace=sum((j*(j-9)*c*a**(j-1) for j,c in enumerate(cs,1)),P(10,0))
    zero(a*paa-8*pa-trace,'entire marked logarithmic derivative numerator')
    roots=vars(9);zz=roots[8];full=P(9,1)
    for r in roots[:8]:full=full*(zz-r)
    primitive=P(9,{ex[:8]+(ex[8]+1,):9*c/Q(ex[8]+1) for ex,c in full.d.items()})
    zero(primitive.diff(8)-9*full,'entire generic original derivative')
    c8=P(9,{ex[:8]+(0,):9*c/Q(8) for ex,c in full.d.items() if ex[8]==7})
    c7=P(9,{ex[:8]+(0,):9*c/Q(7) for ex,c in full.d.items() if ex[8]==6})
    S1=sum(roots[:8],P(9,0));S2=sum((r*r for r in roots[:8]),P(9,0))
    zero(S1+Q(8,9)*c8,'whole multiplicity first trace')
    zero(S2-S1*S1+Q(14,9)*c7,'whole multiplicity second trace')
    t=vars(1)[0];aa=1-t
    J=8*aa**2-8*aa**3-Q(14,3)*t-Q(64,9)*t*(aa-Q(7,8))
    zero(J-t*(Q(22,9)-Q(80,9)*t+8*t*t),'whole rational objective numerator')
    # Signed paired-normal slack V=6eta+10368eta^2-Cstar; actual V>=0.
    # Complete trace substitution, keeping both extra signed positive terms.
    eta,rec7,rec8,T1real2,Rc=vars(5)
    Cstar=rec7+rec8+Rc
    left=T1real2-Q(14,9)*rec7
    rhs=T1real2-Q(28,3)*eta-Q(28,3)*1728*eta**2+Q(14,9)*rec8
    rhs+=Q(14,9)*Rc+Q(14,9)*(6*eta+6*1728*eta**2-Cstar)
    zero(left-rhs,'entire signed normal slack trace identity')
    return {'entire_anchored_free_original':p.record(),'entire_generic_critical_factorization':full.record(),'marked_trace_numerator_zero':True,'both_entire_newton_identities_zero':True,'entire_J_numerator_zero':True,'entire_signed_normal_slack_zero':True}


def reciprocal():
    x,y,u=vars(3);v=2*x*u-(x*x+y*y)*u*u
    series=P(3,0)
    for m in range(11):
        q=Q(comb(2*m,m),4**m)*v**m
        series+=P(3,{ex:c for ex,c in q.d.items() if ex[2]<=10})
    polys=[]
    for n in range(11):
        actual=P(2,{ex[:2]:c for ex,c in series.d.items() if ex[2]==n})
        xx,yy=vars(2)
        laplace=sum((Q(comb(n,2*j)*comb(2*j,j),4**j)*(-1)**j*xx**(n-2*j)*yy**(2*j) for j in range(n//2+1)),P(2,0))
        zero(actual-laplace,'whole reciprocal/Laplace coefficient')
        polys.append(actual.record())
    xx,yy=vars(2)
    zero(P(2,{tuple(e):Q(c) for e,c in polys[2]})-(xx*xx-yy*yy/2),'full reciprocal quadratic')
    zero(P(2,{tuple(e):Q(c) for e,c in polys[3]})-(xx**3-Q(3,2)*xx*yy*yy),'full reciprocal cubic')
    U,V=vars(2)
    # Revised Young allocation X/(5a^3)+45H^2/(16a^5).
    zero((U*U/5+Q(45,16)*V*V-Q(3,2)*U*V)-(U/5-Q(3,4)*V)**2*5,'whole revised Young square')
    return {'whole_reciprocal_homogeneous_coefficients_through10':polys,'new_young_square_zero':True,'infinite_tail_requires_written_Laplace_modulus_bound':True}


def explicit_low_family():
    z,t=vars(2);x=Q(12,25);H=Q(121,50);b=x*t;v=H*t/8
    d=9*((z+b)**2+v)**4
    primitive=P(2,{(j+1,k):c/Q(j+1) for (j,k),c in d.d.items()})
    p=primitive-primitive.sub([1-t,t])
    zero(p.diff(0)-d,'whole new low family derivative');zero(p.sub([1-t,t]),'whole new low family anchor')
    c8=P(1,{(k,):c for (j,k),c in p.d.items() if j==8})
    c7=P(1,{(k,):c for (j,k),c in p.d.items() if j==7})
    tt=vars(1)[0]
    zero(c8-Q(108,25)*tt,'whole low-family c8')
    zero(c7-(Q(1089,700)*tt+Q(5184,625)*tt*tt),'whole low-family c7')
    zero((1-t+b)**2+v-(1-Q(59,80)*t+Q(169,625)*t*t),'whole low-family reciprocal-distance square')
    baseline=1-Q(59,80)*tt+Q(169,625)*tt*tt
    sublevel=(8+3*tt)**2*baseline-64
    zero(sublevel-(Q(4,5)*tt-Q(5684,625)*tt**2+Q(126834,20000)*tt**3+Q(1521,625)*tt**4),'entire physical low-sublevel squared objective')
    jet=P(2,{ex:c for ex,c in p.d.items() if ex[1]<=1})
    zero(jet-(z**9-1+t*(Q(108,25)*z**8+Q(1089,700)*z**7+Q(2187,700))),'whole original low-family first jet')
    return p,{'entire_new_low_sublevel_original_polynomial':p.record(),'entire_derivative':d.record(),'entire_squared_sublevel_margin':sublevel.record(),'all_parameter_original_feasibility_requires_written_Rouche_Cauchy':True}


def budgets():
    e=Q(1,65536);a=1-e;K=8;L=16;Phi=(1+L*e)**7;out={}
    def margin(name,v):need(v>0,name);out[name]=str(v)
    margin('original_Rouche',9*L-9-16*K-(36*L*L+36*K*L)*Phi*e)
    margin('original_circle_disjoint',Q(4,9)-2*L*e)
    margin('complete_paired_normal1728',1728-((4*L*L+4*K*L)*Phi+Q(L*L,2)+4+4*K))
    margin('critical_Rouche',Q(9,3**8)-Q(9*K,4)*e)
    margin('marked_derivative_nonzero',9-(72+36*K)*e)
    margin('marked_trace108',108-Q(120*K)/(a*(9-(72+36*K)*e)))
    margin('second_real_trace13',13-Q(64,9)**2*e-Q(112,9))
    margin('initial_H1130',1130-(30+1080+13))
    margin('initial_H_sqrt_domain',Q(4,225)-1130*e)
    margin('higher_original_loss9over4',Q(9,4)-Q(21,10)-Q(1,12000)-Q(1,1440000))
    N=Q(28,3)*1728+Q(64,9)**2
    margin('original_N16180',16180-N)
    margin('original_n8100',8100-N/(2*a**3))
    originalc=Q(7,4)/a**3+Q(9,4)/a**5+1/(a**5*(1-1/(3*a)))
    margin('original_tail6',6-originalc)
    margin('trace_coefficient_positive',a-Q(7,8))
    margin('original_J12over5',Q(22,9)-Q(80,9)*e-Q(12,5))
    margin('original_b29',29-Q(134,5)-81000*e)
    for left,right in [(1130,288),(288,38),(38,30)]:
        margin('original_divisor_'+str(left),1-52*left*e)
        margin('original_bootstrap_'+str(left)+'_'+str(right),right*(1-52*left*e)-29)
    margin('original_objective2',Q(12,5)-(8100+6*30**2)*e-2)
    margin('new_N16179',16179-N);margin('new_n8091',8091-N/(2*a**3))
    newc=Q(7,4)/a**3+Q(45,16)/a**5+1/(a**5*(1-1/(3*a)))
    margin('new_tail607over100',Q(607,100)-newc)
    b=Q(688,27)+(Q(1600,27)+16179+Q(20,3)*8091)*e
    margin('new_b133over5',Q(133,5)-b)
    margin('new_beta44',44-Q(7,2)-Q(20,3)*Q(607,100))
    for left,right in [(1130,111),(111,29),(29,Q(136,5)),(Q(136,5),Q(271,10))]:
        margin('new_divisor_'+str(left),1-44*left*e)
        margin('new_bootstrap_'+str(left)+'_'+str(right),right*(1-44*left*e)-Q(133,5))
    margin('new_objective9over4',Q(22,9)-Q(9,4)-(Q(80,9)+8091+Q(607,100)*Q(271,10)**2)*e)
    margin('retained_c8_gain',Q(1,8)-e)
    # Independent actual low-sublevel test family; no branch-cover import.
    rho=Q(1,128);R=Q(17,16);d=Q(1,16);x=Q(12,25);h=Q(121,50)
    z,t=vars(2);majorant=9*((z+x*t)**2+h*t/8)**4
    low=[]
    for j in range(1,7):
        row={k:c/Q(j) for (i,k),c in majorant.d.items() if i==j-1}
        need(all(k>=2 and c>0 for k,c in row.items()),'entire low-family double-order tail')
        bound=sum(c*rho**(k-2) for k,c in row.items());margin('low_family_coefficient_'+str(j),6-bound);low.append(str(bound))
    margin('low_family_c7_complex',Q(13,8)-Q(1089,700)-Q(5184,625)*rho)
    Pbound=9*(1+rho)**8+Q(108,25)*(R**8+(1+rho)**8)+Q(13,8)*(R**7+(1+rho)**7)
    Pbound+=6*rho*sum(R**j+(1+rho)**j for j in range(1,7))
    margin('low_family_anchor_P27',27-Pbound)
    margin('low_family_Rouche',9*d-36*(1+d)**7*d*d-Q(1,4))
    margin('low_family_perturbation',Q(1,4)-27*rho)
    margin('low_family_quotient5',9-36*d*(1+d)**7-5)
    margin('low_family_companion6',6-Q(27,5)-Q(1,2)*Q(27,5)**2*rho)
    margin('low_family_normal_positive_cos',1-x-h/7-Q(1,50))
    margin('low_family_normal_cube',1-Q(3,2)*x-Q(3,28)*h-Q(1,50))
    margin('low_family_normal_negative_cos',1-x*(1+Q(15,16))-h/7*(1-Q(15,16)**2)-Q(1,50))
    margin('negative_cos_derivative',2*h/7*Q(15,16)-x)
    margin('cos_cubic_lower',-(8*Q(15,16)**3-6*Q(15,16)-1))
    margin('cos_cubic_upper',8*Q(31,32)**3-6*Q(31,32)-1)
    margin('low_family_all_positive_normal',Q(1,50)-Q(6,511))
    margin('low_family_c8_cap8',8-Q(108,25))
    margin('low_family_c8_outside_cap2',Q(108,25)-2)
    margin('low_family_c7_cap8',8-Q(1089,700)-Q(5184,625)*e)
    margin('low_family_low_coefficient_cap8',8-6*e)
    margin('low_family_actual_sublevel',Q(4,5)-Q(5684,625)*e)
    margin('low_family_distance_positive',1-Q(59,80)*e)
    return {'entire_strict_margin_table':out,'new_low_family_lower_coefficient_complex_disk_bounds':low,'new_low_family_P_bound':str(Pbound),'new_normal_slack_c8_coefficient':str(Q(8,9)*(Q(1,8)-e)),'new_objective_loss':str(Q(80,9)+8091+Q(607,100)*Q(271,10)**2)}


def gmul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def gp(x,n):
    r=(Q(1),Q(0))
    for _ in range(n):r=gmul(r,x)
    return r
def norm2(x):return x[0]**2+x[1]**2


def literal(eta,q):
    need(type(eta) is Q and 0<eta<=Q(1,65536),'actual positive parameter')
    need(all(type(x) is Q for x in q),'literal original complex type')
    a=1-eta;r=(a-q[0],-q[1]);coeff=[]
    for j in range(10):
        c=gp((-q[0],-q[1]),9-j);c=tuple(comb(9,j)*v for v in c)
        if j==0:
            ar=gp(r,9);c=tuple(v-u for v,u in zip(c,ar))
        coeff.append(c)
    need(all(norm2(coeff[j])<=(8*eta)**2 for j in range(1,9)),'literal full coefficient chamber')
    need(sum(c[0]*a**j for j,c in enumerate(coeff))==0 and sum(c[1]*a**j for j,c in enumerate(coeff))==0,'literal actual marked anchor')
    # A rigorously sufficient disk-interior condition by triangle; no roots.
    need(abs(q[0])+abs(q[1])+abs(r[0])+abs(r[1])<1,'all-nine literal original disk interior')
    QR=(q[0],q[1],Q(0),Q(0));RR=(r[0],r[1],Q(0),Q(0))
    originals=[ra(QR,rm(RR,w)) for w in [W,star(W)]]
    for Z in originals:
        need(ra(rp(ra(Z,rs(QR,-1)),9),rs(rp(RR,9),-1))==RZERO,'entire actual cube-original equation')
    normals=[rs(ra(rm(Z,star(Z)),rs(RONE,-1)),Q(1,2)) for Z in originals]
    mean=rs(ra(*normals),Q(1,2));need(mean[1:]==(Q(0),)*3,'whole literal paired half-normal rational')
    Cstar=sum(coeff[j][0] for j in [1,2,4,5,7,8])
    error=mean[0]+eta-Cstar/6;need(abs(error)<1728*eta*eta,'literal actual root normal full remainder')
    need(Cstar<=6*eta+10368*eta*eta,'literal actual paired inequality')
    S1=tuple(8*v for v in q);S2=tuple(8*v for v in gp(q,2))
    need(S1==tuple(-Q(8,9)*v for v in coeff[8]),'literal first trace')
    need(S2==tuple(v-Q(14,9)*c for v,c in zip(gmul(S1,S1),coeff[7])),'literal second trace retains square')
    H=8*norm2(q);X=8*q[0]*q[0]
    need(H==2*X-S2[0],'literal actual real/imaginary energy')
    return {'eta':str(eta),'critical_center':list(map(str,q)),'entire_original_coefficients':[[str(v) for v in c] for c in coeff],'actual_paired_originals':[rr(Z) for Z in originals],'actual_paired_normals':[rr(n) for n in normals],'whole_paired_normal_error':str(error),'H':str(H),'X':str(X),'reflected_original_is_conjugate':originals[1]==star(originals[0]),'scope':'All nine original roots simple/strictly interior by shifted-circle triangle proof; all eight criticals equal q; no low-sublevel assertion'}


def controls():
    e=Q(1,65536)
    return [literal(e,q) for q in [(Q(0),Q(0)),(Q(0),e/4),(Q(0),-e/4),(e/4,Q(0)),(-e/4,Q(0))]]


def optional_covered_branch():
    # The existence, actual originals and box are IMPORTED9113/9174 only.
    # Fresh bounds conditionally decode that box; no continuation replay.
    rho=Q(1,1024);e=Q(1,65536)
    def plus(a,b):return a[0]+b[0],a[1]+b[1]
    def scaled(a,c):return tuple(sorted([a[0]*c,a[1]*c]))
    def times(a,b):
        v=[x*y for x in a for y in b];return min(v),max(v)
    def box(a):return a[0]-rho,a[1]+rho
    y=(Q(32,189),Q(16,93));H=scaled(y,14)
    U=scaled(plus((Q(2,3),Q(2,3)),scaled(y,-1)),-8)
    hh=(-Q(65,48),-Q(43,32));hhH=times(hh,H)
    x=scaled(plus(U,hhH),Q(1,8));yy=plus(x,scaled(hhH,-Q(1,2)));T=scaled(H,Q(1,2))
    xt,yt,Tt=box(x),box(yy),box(T);trace=(U[0]-8*rho,U[1]+8*rho)
    need(trace[0]>-4 and trace[1]<-Q(32,9),'entire true-box trace bounds')
    need(max(map(abs,xt))<Q(9,8) and max(map(abs,yt))<Q(9,8) and max(map(abs,Tt))<Q(25,16),'whole true-box primitive coordinate bounds')
    z,eta,xv,yv,tv=vars(5)
    q=9*(z-eta*xv)**6*((z-eta*yv)**2+eta*tv)
    c8=P(5,{(0,)+ex[1:]:v/Q(8) for ex,v in q.d.items() if ex[0]==7})
    zero(c8+Q(9,8)*eta*(6*xv+2*yv),'whole imported-profile top coefficient')
    zz,ee=vars(2);majorant=9*(zz+Q(9,8)*ee)**6*((zz+Q(9,8)*ee)**2+Q(25,16)*ee)
    bounds=[]
    for j in range(1,8):
        row={k:v/Q(j) for (i,k),v in majorant.d.items() if i==j-1}
        need(all(k>=1 and v>0 for k,v in row.items()),'entire branch positive orders')
        bound=sum(v*e**(k-1) for k,v in row.items());need(bound<3,'all seven covered branch coefficient bounds');bounds.append(str(bound))
    return {'imported_scope':'9113 covered actual branch and radius1/1024 true cube, confirmed9174; existence/continuation not re-audited','trace_box':list(map(str,trace)),'x_box':list(map(str,xt)),'y_box':list(map(str,yt)),'T_box':list(map(str,Tt)),'all_seven_low_coefficient_majorants_divided_by_eta':bounds,'top_coefficient_entire_identity_zero':True}


def damages():
    rejected=[]
    def reject(name,fn):
        try:fn()
        except ValueError:rejected.append(name);return
        raise ValueError('accepted damage '+name)
    cs=controls();eta=Q(1,65536);q=(Q(0),eta/4)
    reject('declared_original_conjugation',lambda:need(cs[1]['reflected_original_is_conjugate'],'actual complex originals not conjugate'))
    z,t=vars(2);reject('changed_anchor',lambda:zero((t+z**9-(1-t)**9).sub([1-t,t]),'changed anchor'))
    reject('drop_first_trace_square',lambda:need(8*gmul(q,q)[0]==-Q(14,9)*Q(cs[1]['entire_original_coefficients'][7][0]),'actual first square needed'))
    reject('zero_parameter',lambda:literal(Q(0),(Q(0),Q(0))))
    reject('parameter_outside_interval',lambda:literal(2*eta,(Q(0),Q(0))))
    reject('bool_parameter',lambda:literal(True,(Q(0),Q(0))))
    reject('coefficient_chamber_damage',lambda:literal(eta,(Q(0),20*eta)))
    e=eta
    reject('nonpositive_first_bootstrap_divisor',lambda:need(1-52*1300*e>0,'failed divisor'))
    reject('insufficient_new_H27_budget',lambda:need(27*(1-44*Q(136,5)*e)>Q(133,5),'H27 does not follow from displayed budget'))
    reject('insufficient_new_linear23over10',lambda:need(Q(22,9)-(Q(80,9)+8091+Q(607,100)*Q(271,10)**2)*e>Q(23,10),'2.3 is not certified by displayed budget'))
    reject('drop_imaginary_cube_phase',lambda:need(W==star(W),'cube labels need not coincide'))
    reject('wrong_physical_mean_normal',lambda:need(Q(cs[1]['whole_paired_normal_error'])==0,'entire actual normal error nonzero'))
    return rejected


def record():
    p,family=explicit_low_family()
    return {'schema':'six-reviewer-1-actual-cap8-independent-v1','original_paired_domain':paired_original(),'identities':identities(),'reciprocal_and_young':reciprocal(),'proved_new_actual_low_family':family,'entire_window_budgets':budgets(),'literal_actual_original_controls':controls(),'optional_imported_branch':optional_covered_branch(),'mathematical_damage_rejections':damages(),'unbounded_analytic_bridges_written_not_finite_extrapolation':True}
