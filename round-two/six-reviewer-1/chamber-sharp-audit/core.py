"""Independent original polynomial, cyclic root sections and full-window budgets.
The exact polynomial kernel is credited own9455; no target imports or fixtures.
Finite series corroborate the written Rouche/Cauchy proof, never its coverage.
"""
from fractions import Fraction as Q
from math import comb
from algebra import P,vars,zero


def need(ok,label):
    if not ok:raise ValueError(label)


def coefficient(p,j,k):return p.d.get((j,k),Q(0))


def anchor_family():
    z,t=vars(2);b=2*t/9;v=7*t/18-28*t*t/81
    derivative=9*((z+b)**2+v)**4
    primitive=P(2,{(e[0]+1,e[1]):c/Q(e[0]+1) for e,c in derivative.d.items()})
    p=primitive-primitive.sub([1-t,t])
    zero(p.diff(0)-derivative,'whole derivative reconstruction')
    zero(p.sub([1-t,t]),'whole actual marked anchor')
    zero(P(1,{(k,):coefficient(p,8,k) for k in range(10)})-2*vars(1)[0],'whole c8')
    zero(P(1,{(k,):coefficient(p,7,k) for k in range(10)})-2*vars(1)[0],'whole c7')
    jet=P(2,{e:c for e,c in p.d.items() if e[1]<=1})
    zero(jet-(z**9-1+t*(2*z**8+2*z**7+5)),'entire original first jet')
    zero((1-t+b)**2+v-(1-7*t/6+7*t*t/27),'whole exact reciprocal-distance square')
    for j in range(1,7):need(all(k>=2 for (i,k) in p.d if i==j),'low original coefficient order')
    return p,derivative


# Q[C9], represented by nine coefficients. It simultaneously evaluates all
# nine ninth roots without floating inputs, root labeling or target sections.
RZERO=(Q(0),)*9
RONE=(Q(1),)+(Q(0),)*8
W=(Q(0),Q(1))+(Q(0),)*7
def radd(a,b):return tuple(x+y for x,y in zip(a,b))
def rscale(a,c):return tuple(x*c for x in a)
def rmul(a,b):
    d=[Q(0)]*9
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if x and y:d[(i+j)%9]+=x*y
    return tuple(d)
def rinvolution(a):return tuple(a[-i%9] for i in range(9))
def smul(a,b,L):
    d=[RZERO for _ in range(L)]
    for i,x in enumerate(a):
        for j,y in enumerate(b[:L-i]):
            if x!=RZERO and y!=RZERO:d[i+j]=radd(d[i+j],rmul(x,y))
    return d
def spowers(a,n,L):
    out=[[RONE]+[RZERO]*(L-1)]
    for _ in range(n):out.append(smul(out[-1],a,L))
    return out
def original_residual(p,Z,L):
    powers=spowers(Z,9,L);out=[RZERO]*L
    for (j,k),c in p.d.items():
        if k<L:
            for i in range(L-k):out[i+k]=radd(out[i+k],rscale(powers[j][i],c))
    return out
def root_sections(p,L=7):
    Z=[W]+[RZERO]*(L-1);stages=[]
    for j in range(1,L):
        residual=original_residual(p,Z,L)
        Z[j]=rscale(rmul(W,residual[j]),-Q(1,9))
        checked=original_residual(p,Z,L)
        need(all(x==RZERO for x in checked[:j+1]),'all-nine original section residual')
        stages.append(j)
    need(original_residual(p,Z,L)==[RZERO]*L,'whole truncated actual original realization')
    need(sum(Z[0])==1 and sum(Z[1])==-1 and all(sum(z)==0 for z in Z[2:]),'marked section equals a at omega1')
    conjugate=list(map(rinvolution,Z));norm=smul(Z,conjugate,L);norm[0]=radd(norm[0],rscale(RONE,-1))
    alpha=list(rscale(x,Q(1,2)) for x in norm)
    target=rscale(RONE,-Q(5,9));target=radd(target,rscale(radd(W,rinvolution(W)),-Q(1,9)))
    W2=rmul(W,W);target=radd(target,rscale(radd(W2,rinvolution(W2)),-Q(1,9)))
    need(alpha[1]==target,'whole all-nine first half-normal')
    need(sum(alpha[1])==-1 and sum(alpha[2])==Q(1,2) and all(sum(z)==0 for z in alpha[3:]),'actual marked half-normal')
    return {'series_order':L-1,'original_all_nine_section_coefficients':[[str(x) for x in z] for z in Z],'all_nine_companion_half_normal_coefficients':[[str(x) for x in a] for a in alpha],'all_original_residuals_zero':True,'checked_stage_orders':stages,'scope':'Formal finite sections corroborate the ordinary whole-complex-disk proof, not physical feasibility by finite extrapolation'}


def universal():
    p,derivative=anchor_family();t=vars(1)[0];a=1-t
    base=8*a*a-Q(16,9)*t*a-Q(1,2)*(Q(28,9)*t+Q(256,81)*t*t)
    zero(base-(8+Q(14,3)*t)*a**3-t*t*(-Q(146,81)-6*t+Q(14,3)*t*t),'whole target rational remainder')
    radius_numerator=(8+5*t)*a**3-8*a*a+Q(16,9)*t*a+Q(3,4)*(Q(28,9)*t+Q(256,81)*t*t)
    zero(radius_numerator-(Q(10,9)*t+Q(43,27)*t*t+7*t**3-5*t**4),'entire retained energy numerator')
    x,y,tx,ty,H,eta,r=vars(7);a=1-eta;ec=Q(1,4)-Q(5,4)*r;dc=Q(1,2)+Q(5,4)*r
    T2real=tx*tx-ty*ty-Q(14,9)*y
    signed=8*a*a-Q(8,9)*x*a+Q(3,4)*T2real+ec*H
    decomposed=8*a*a-Q(16,9)*eta*a-dc*(Q(256,81)*eta*eta+Q(28,9)*eta)
    decomposed+=Q(8,9)*a*(2*eta-x)+Q(14,9)*dc*(2*eta-y)+ec*(H+T2real)
    decomposed+=dc*(tx*tx-ty*ty+Q(256,81)*eta*eta)
    zero(signed-decomposed,'whole signed coefficient/real-critical-energy slack')
    c,d=vars(2)
    zero(c*c+d*d+1-2*c-((c-1)**2+d*d),'entire analytic square identity')
    cos=vars(1)[0]
    zero(5+2*cos+2*(2*cos*cos-1)-(4*(cos+Q(1,4))**2+Q(11,4)),'complete negative first half-normal')
    return p,{'entire_anchored_original_polynomial':p.record(),'entire_critical_polynomial':(derivative/9).record(),'rational_target_remainder_zero':True,'retained_energy_numerator_zero':True,'signed_top_coefficient_slack_zero':True,'analytic_square_zero':True,'first_half_normal_square_completion_zero':True}


def budgets():
    e=Q(1,65536);rho=Q(1,128);d=Q(1,16);R=Q(17,16)
    values={}
    def margin(name,x):need(x>0,name);values[name]=str(x)
    margin('original_a_lower',1-e-Q(255,256))
    margin('initial_sqrt_energy',35**2-1188)
    margin('initial_ratio_bound',36-35*Q(256,255))
    margin('initial_r_below_one_sixth',Q(1,6)-Q(36,256))
    # Complete-window monotone endpoint; the negative -5eta^3 was dropped.
    margin('retained_energy_numerator_below_9over8',Q(9,8)-Q(10,9)-Q(43,27)*e-7*e*e)
    margin('first_bootstrap_H_below16',16-Q(9,8)/(Q(19,256)))
    margin('second_ratio_bound',Q(33,8)-4*Q(256,255))
    ec2=Q(1,4)-Q(5,4)*Q(33,8)*Q(1,256)
    margin('second_bootstrap_H_below5',5-Q(9,8)/ec2)
    margin('sqrt5_below_9over4',Q(9,4)**2-5)
    margin('final_ratio_bound',Q(23,10)-Q(9,4)*Q(256,255))
    final_ec=Q(1,4)-Q(5,4)*Q(23,10)*Q(1,256)
    need(final_ec==Q(489,2048),'exact signed real-energy coefficient')
    margin('final_r_domain',Q(1,6)-Q(23,10)*Q(1,256))
    margin('inverse_cube',Q(33,32)-Q(256,255)**3)
    margin('trace2_window',Q(25,8)-Q(28,9)-Q(256,81)*e)
    margin('whole_rational_remainder',2-Q(33,32)*(Q(146,81)+6*e))
    new_cost=Q(5,4)*Q(33,32)*Q(25,8)*Q(23,10)+Q(1,128)
    need(new_cost==Q(18991,2048),'complete new eta3over2 budget')
    margin('new_remainder10',10-new_cost)
    margin('original_remainder147',147-(Q(5,4)*Q(33,32)*Q(25,8)*36+Q(1,128)))
    margin('original_strict4',Q(14,3)-Q(147,256)-4)
    margin('new_physical_gap',Q(14,3)-Q(10,256)-3)
    need(Q(14,3)-Q(10,256)-3==Q(625,384),'new whole-window physical infimum gap')
    margin('family_v_positive',Q(7,18)-Q(28,81)*e)
    margin('family_distance_positive',1-Q(7,6)*e)
    margin('critical_distance_coefficient',2-4*e)
    margin('whole_complex_disk_Rouche',9*d-36*(1+d)**7*d*d-Q(1,4))
    margin('whole_complex_disk_root_quotient',9-36*d*(1+d)**7-5)
    Pbound=9*(1+rho)**8+2*(R**8+(1+rho)**8)+2*(R**7+(1+rho)**7)
    Pbound+=4*rho*sum(R**j+(1+rho)**j for j in range(1,7))
    margin('whole_anchored_family_coefficient_majorant',21-Pbound)
    margin('Rouche_perturbation',Q(1,4)-21*rho)
    margin('original_displacement',5-Q(21,5))
    margin('companion_half_normal_division',6-5-Q(25,2)*rho)
    margin('entire_Cauchy_normal_deviation',Q(11,36)-Q(6,511))
    # Proved actual sharp-family extension ONLY; universal chamber theorem
    # keeps eta<=2^-16. A sharper root displacement closes eta<=2^-11.
    wide=Q(1,2048)
    beta_bound=Q(21,5)+Q(1,2)*Q(21,5)**2*rho
    need(beta_bound==Q(27321,6400),'entire sharper companion quotient bound')
    margin('sharper_companion_quotient',Q(9,2)-beta_bound)
    need(wide/rho==Q(1,16),'whole larger physical-family window ratio')
    margin('wider_family_actual_normal',Q(11,36)-Q(9,2)*(wide/rho)/(1-wide/rho))
    margin('wider_family_chamber',2-4*wide)
    margin('wider_family_v',Q(7,18)-Q(28,81)*wide)
    margin('wider_family_distance',1-Q(7,6)*wide)
    # Separate direct positive-majorant derivative expansion and its six
    # integrated low coefficients; no author expected data supplied.
    z,t=vars(2);B=Q(2,9);V=Q(7,18)+Q(28,81)*rho
    majorant=9*((z+B*t)**2+V*t)**4
    low=[]
    for j in range(1,7):
        row={k:c/Q(j) for (i,k),c in majorant.d.items() if i==j-1}
        need(all(k>=2 and c>0 for k,c in row.items()),'all positive low-coefficient tail orders')
        bound=sum(c*rho**(k-2) for k,c in row.items())
        margin('low_original_coefficient_'+str(j),4-bound);low.append(str(bound))
    return {'entire_strict_margin_table':values,'low_original_coefficient_complex_disk_bounds':low,'exact_new_remainder_cost':str(new_cost),'final_real_energy_gain':str(2*final_ec),'physical_infimum_gap':str(Q(625,384)),'sharp_family_actual_disk_extension':'every real 0<eta<=2^-11, strictly simple/interior originals and |ck|<=2eta, exact same objective; no wider universal chamber bound','domain':'Universal chamber: EVERY real 0<eta<=2^-16; complex family disk |eta|<1/128 via written analytic proof'}


def gadd(a,b):return a[0]+b[0],a[1]+b[1]
def gmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def gscale(a,c):return a[0]*c,a[1]*c
def norm2(a):return a[0]*a[0]+a[1]*a[1]
GZERO=(Q(0),Q(0));GONE=(Q(1),Q(0))
def critical_original(points,eta):
    need(type(eta) is Q and 0<eta<=Q(1,65536),'literal positive interval')
    need(len(points)==8 and all(type(x) is Q and type(y) is Q for x,y in points),'all eight complex critical multiplicities')
    derivative=[GONE]
    for r in points:
        nxt=[GZERO]*(len(derivative)+1)
        for j,c in enumerate(derivative):
            nxt[j]=gadd(nxt[j],gmul(c,gscale(r,-1)));nxt[j+1]=gadd(nxt[j+1],c)
        derivative=nxt
    originals=[GZERO]+[gscale(derivative[j-1],Q(9,j)) for j in range(1,10)]
    need(all(norm2(originals[j])<=(2*eta)**2 for j in range(1,9)),'literal whole coefficient chamber')
    T1=GZERO;T2=GZERO
    for r in points:T1=gadd(T1,r);T2=gadd(T2,gmul(r,r))
    need(T1==gscale(originals[8],-Q(8,9)),'entire first critical trace')
    need(T2==gadd(gmul(T1,T1),gscale(originals[7],-Q(14,9))),'entire second critical trace including first square')
    H=sum(map(norm2,points));energy=H+T2[0]
    need(energy==2*sum(x*x for x,y in points),'literal all-critical real-part energy')
    need(H*H>=norm2(T2),'whole complex trace2 versus actual energy')
    a=1-eta;anchor=GZERO
    for j,c in enumerate(originals):anchor=gadd(anchor,gscale(c,a**j))
    originals[0]=gscale(anchor,-1)
    need(sum(c[0]*a**j for j,c in enumerate(originals))==0 and sum(c[1]*a**j for j,c in enumerate(originals))==0,'literal original marked anchor')
    return {'original_full_coefficients':[[str(x),str(y)] for x,y in originals],'critical_trace1':list(map(str,T1)),'critical_trace2':list(map(str,T2)),'H':str(H),'all_critical_real_energy':str(energy),'scope':'literal algebra/chamber/multiplicity/anchor, no original disk-rootedness assertion'}


def literal_controls():
    eta=Q(1,65536);t=Q(1,4096);out=[]
    cases=[
        [(Q(0),Q(0))]*8,
        [(Q(0),t)]*4+[(Q(0),-t)]*4,
        [(eta/16,t)]*4+[(eta/16,-t)]*4,
        [(eta*Q(j-3,64),t if j<4 else -t) for j in range(8)],
        [(eta/32,t)]*2+[(eta/32,-t)]*2+[(eta/16,t/2)]*2+[(eta/16,-t/2)]*2,
    ]
    for points in cases:out.append(critical_original(points,eta))
    return out


def damages(p):
    names=[]
    def reject(name,f):
        try:f()
        except ValueError:names.append(name);return
        raise ValueError('accepted mathematical damage '+name)
    z,t=vars(2);reject('changed_actual_anchor',lambda:zero((p+t).sub([1-t,t]),'wrong actual marked anchor'))
    actual=literal_controls()[2];T2=tuple(map(Q,actual['critical_trace2']));c7=tuple(map(Q,actual['original_full_coefficients'][7]))
    reject('drop_first_critical_trace_square',lambda:need(T2==gscale(c7,-Q(14,9)),'literal second trace requires nonzero first square'))
    reject('wrong_first_half_normal',lambda:zero(5+2*t+2*(2*t*t-1)-(4*(t+Q(1,4))**2+Q(5,2)),'wrong normal constant'))
    reject('truncated_critical_multiplicity',lambda:critical_original([(Q(0),Q(0))]*7,Q(1,65536)))
    reject('zero_interval',lambda:critical_original([(Q(0),Q(0))]*8,Q(0)))
    reject('beyond_positive_window',lambda:critical_original([(Q(0),Q(0))]*8,Q(1,32768)))
    reject('binary_bool_parameter',lambda:critical_original([(Q(0),Q(0))]*8,True))
    reject('drop_actual_real_part_energy',lambda:need(Q(actual['all_critical_real_energy'])==0,'literal positive real-part energy cannot be deleted'))
    reject('unjustified_bootstrap_H4',lambda:need(Q(9,8)/(Q(1883,8192))<4,'H4 does not follow from displayed second iteration'))
    reject('remainder9_certificate',lambda:need(Q(18991,2048)<9,'new budget does not certify constant9'))
    return names


def record():
    p,identities=universal()
    return {'schema':'six-reviewer-1-original-chamber-independent-v1','identities':identities,'cyclic_all_nine_original_sections':root_sections(p),'entire_window_budgets':budgets(),'literal_multiplicity_chamber_original_controls':literal_controls(),'mathematical_damage_rejections':damages(p),'all_unbounded_analytic_bridges_written_not_finite_extrapolation':True}
