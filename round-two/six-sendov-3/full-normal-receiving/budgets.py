"""Exact fresh local root/normal and separate receiving budgets.

Actual six-sendov-3 / researcher. Analytic and domain bridges in PROOF.md.
Rho controls centered RMS coefficients; r has a separate explicit box.
"""
from arithmetic import F, comb, need

ETA_MAX=F(1,12000)
A_MIN=1-ETA_MAX
RHO=F(1,128)
TAU=F(1,50)
PAIR=F(9,16)
INDIVIDUAL=F(5,8)
ALL_NORMAL=F(7,8)
NONCUBIC=F(135)
PHYSICAL=F(192)
OBJECTIVE=F(175)


def budgets(changes=None):
    changes={} if changes is None else changes
    e=F(changes.get('eta_endpoint',ETA_MAX)); a=1-e; hi=1+e
    v=5*e; t=F(13,15)*e; rho=F(changes.get('rho',RHO))
    tau=F(changes.get('tau',TAU)); s=hi+v/2
    pair=F(changes.get('pair_cap',PAIR))
    individual=F(changes.get('individual_cap',INDIVIDUAL))
    all_normal=F(changes.get('all_normal_cap',ALL_NORMAL))
    physical=F(changes.get('physical',PHYSICAL))
    objective=F(changes.get('objective',OBJECTIVE))
    r3=F(changes.get('R3',18)); r4=F(changes.get('R4',27))
    rows=[]
    def positive(name,value):
        value=F(value); need(value>0,'budget: '+name)
        rows.append({'name':name,'strict_margin':str(value)})
    positive('positive actual radius floor',a)
    positive('fresh centered RMS coefficient endpoint',8*rho*rho-v)
    positive('mean below independent coefficient scale',rho-t)
    positive('centered max norm below fresh full-tail radius',tau*tau-F(7,8)*v)
    positive('positive entire tail denominator',a-tau)
    positive('final inverse cube cost4eta',4-3/a**4)
    A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)}
    A[7]=F(9,14)
    Cd=sum(j*A[j]*s**(j-1) for j in A)
    divisor=9*a**8-18*s**7*v-Cd*v
    positive('all nine full counted Rouche circles',F(9,2)*a**8-9*s**7*v-sum(A[j]*(s**j+hi**j) for j in A))
    positive('all nine disjoint counted circles',F(4,9)*a-v)
    positive('positive full root divisor',divisor)
    B={5:F(63,32),4:F(63,32)*rho,3:F(21,128)*v,
       2:F(9,128)*rho*v,1:F(9,4096)*v*v}
    branches=[]
    for D,name,ids,c in ((F(1,6),'cube',(1,2,4,5,7),F(7,4)),
                          (F(1,4),'all9',tuple(range(1,8)),F(2))):
        N=c*sum(A[j]*hi**j for j in ids)
        positive(name+' full displacement bound',D*divisor-N)
        positive(name+' entire linear displacement bound',D*9*a**8-N)
        Be=4*s**7*D*D/a**8+D*Cd/(9*a**8)
        row={'name':name,'displacement_scale':str(D),'N':str(N),'full_nonlinear_cost':str(Be)}
        if name=='cube':
            higher=sum(B[j]*a**(j-7) for j in (1,2,4,5))
            actual_pair=(t+hi)*Be+D*D/2+higher/6
            actual_individual=(t+hi)*Be+D*D/2+higher/5
            positive('fresh full paired cube normal9/16',pair-actual_pair)
            positive('fresh full individual cube normal5/8',individual-actual_individual)
            positive('strict sqrt3/9 below1/5',F(1,25)-F(1,27))
            row.update({'pair_cost':str(actual_pair),'individual_cost':str(actual_individual),'all_higher_linear_cost':str(higher)})
        else:
            higher=sum(B[j]*a**(j-7) for j in B)
            actual_normal=(t+hi)*Be+D*D/2+F(2,9)*higher
            actual_motion=Be+F(2,9)*higher/a
            positive('fresh full all9 normal7/8',all_normal-actual_normal)
            positive('fresh all9 non-T whole motion cost1',F(changes.get('motion_cap',1))-actual_motion)
            row.update({'normal_cost':str(actual_normal),'non_T_motion_cost':str(actual_motion),'all_higher_linear_cost':str(higher)})
        branches.append(row)
    pair_sum=F(1,2)+F(3,2)*F(4,5)+F(3,2)*F(169,225)+F(13,15)*5/6+25*pair
    fourth_sum=F(1,2)+2*F(4,5)+2*F(169,225)+F(13,15)*5/4+25*all_normal
    individual_sum=F(13,15)*5/6+25*individual
    positive('complete paired R3 below18eta2',r3-pair_sum)
    positive('complete noncubic paired R4 below27eta2',r4-fourth_sum)
    positive('complete individual cube below17eta2',17-individual_sum)
    Dcost=8*F(4,5)*(2-e)/a**2+4*F(169,225)/a**3+20
    positive('complete objective conversion below36eta2',36-Dcost)
    # The endpoint sum is EXACTLY135, not a strict margin. All actual
    # errors and both positive dual upper bounds are strict, so cost<135.
    dual_upper=36+r3*F(23,5)+r4*F(3,5)
    need(dual_upper<=NONCUBIC,'budget: whole dual normal cost135')
    b=F(271,200); wlo=F(625,1067); whi=F(3,5)
    positive('combined signed A positive',hi**-4-whi/(12*a))
    positive('combined signed beta minus A positive',F(1,2)*hi**-4-whi/(6*a))
    positive('combined signed A below1',1-a**-4+wlo/(12*hi))
    positive('combined signed beta below271/200',b-F(3,2)*a**-4+wlo/(4*hi))
    k=F(3,4)*b*b; q=b*(1+b)/4; routes=[]
    for name,delta,lam in (('physical',F(1,4),F(69,50)),('objective',F(1,2),F(69,100))):
        a0=delta*delta-q*v; b0=delta*lam-k/2; det=a0*lam*lam-b0*b0
        positive(name+' positive full E-square coefficient',a0)
        positive(name+' positive complete determinant',det)
        routes.append({'name':name,'delta':str(delta),'lambda':str(lam),'a0':str(a0),'b0':str(b0),'determinant':str(det),'V4_remainder':str(det/a0)})
    G=1/((a-tau)*a**4)
    complete_physical=NONCUBIC+25*(F(7,8)*G+F(69,50))
    complete_objective=NONCUBIC+25*(F(7,8)*G+F(69,100))
    positive('separate whole physical error192',physical-complete_physical)
    positive('whole objective error175',objective-complete_objective)
    positive('conditional and actual slope141/50',F(826,291)-objective*e-F(141,50))
    sf=F(changes.get('sqrt_physical_floor',F(27,2)))
    positive('fresh sqrt192 above27/2',physical-sf*sf)
    positive('fresh cube residual3Delta/8',F(3,8)-F(1,4)-r3/physical)
    positive('fresh fourth residualDelta/2',F(1,2)-r4/physical-F(5,2)/(sf*a))
    M=F(62,651)*F(3,8)+F(128,217)*F(5,2)
    Y=F(24832,32550)*F(3,8)+F(128,217)*F(5,2)
    positive('complete Cramer mean8Delta/5',F(8,5)-M)
    positive('complete Cramer trace9Delta/5',F(9,5)-Y)
    positive('whole rotated trace26Delta',26-14*Y)
    positive('whole variance34Delta',34-14*Y-8)
    positive('whole critical energy35Delta',1-8*F(169,225)/physical)
    positive('whole unrotated real energy13Delta',1-F(384,25)/physical-4*e/(physical*a*a))
    positive('imaginary mean sqrt coefficient1',196*a*a-80)
    positive('imaginary mean Delta coefficient1',1-F(7,24)/a)
    # Retain the previous conservative26 in this estimate; fresh17 is stronger.
    positive('imaginary mean eta2 coefficient31',31-F(7,6)*26/a)
    positive('sqrt80 below9',81-80)
    positive('complete mu3 coefficient21/2',F(21,10)**2-F(35,8))
    positive('whole original eta2 cost88',88-62-25-F(896,1395)/a)
    positive('all9 original Delta coefficient19/2',F(19,2)-F(26,5)-F(26,7)/a-88/physical)
    positive('all9 original sqrt coefficient7/2',F(7,2)-2-F(9,7)/a-F(7,6)/(sf*a*a))
    clo=F(15,16); chi=F(47,50)
    positive('selected cosine lower sign',-(8*clo**3-6*clo-1))
    positive('selected cosine upper sign',8*chi**3-6*chi-1)
    positive('selected cosine monotonicity',24*clo**2-6)
    positive('positive dual w3 above4',F(2,3)*(7-F(31,217))-4)
    positive('dual w3 below23/5',F(23,5)-F(2,3)*(7-F(291,2134)))
    positive('dual w4 above1/2',wlo-F(1,2))
    positive('dual w4 below3/5',whi-F(128,217))
    return {'eta_endpoint':str(e),'actual_unconditional_endpoint':'1/12000',
      'rho_for_centered_RMS_only':str(rho),'actual_radius_min':str(a),'actual_radius_max':str(hi),
      'V_endpoint':str(v),'mean_endpoint':str(t),'full_tail_radius':str(tau),
      'all_coefficient_A':{str(j):str(A[j]) for j in sorted(A)},
      'all_coefficient_B':{str(j):str(B[j]) for j in sorted(B)},
      'derivative_coefficient':str(Cd),'full_root_divisor':str(divisor),'branches':branches,
      'complete_paired_R3_cost':str(pair_sum),'complete_paired_R4_noncubic_cost':str(fourth_sum),
      'complete_individual_cube_cost':str(individual_sum),'conversion_cost':str(Dcost),
      'noncubic_cost':str(NONCUBIC),'dual_endpoint_sum':str(dual_upper),
      'dual_endpoint_sum_equals135':dual_upper==NONCUBIC,
      'joint_k':str(k),'joint_q':str(q),'routes':routes,'G':str(G),
      'complete_physical_cost':str(complete_physical),'complete_objective_cost':str(complete_objective),
      'physical_error':str(physical),'objective_error':str(objective),
      'stability_sqrt_floor':str(sf),'rows':rows}
