"""Whole rational endpoint budgets; universal analytic bridges are in PROOF.md.

Actual six-sendov-3/researcher. Fraction arithmetic only; no sampling.
"""
from arithmetic import F, comb, need

E_MAX = F(1, 16000)
A_MIN = 1-E_MAX
TAU = F(1, 60)
ERROR = F(272)
OBJECTIVE_ERROR = F(243)
QUARTIC_FACTOR = F(7, 8)


def budgets(error=ERROR, changes=None):
    changes = {} if changes is None else changes
    alpha=changes.get('quartic_factor',QUARTIC_FACTOR)
    objective_error=changes.get('objective_error',OBJECTIVE_ERROR)
    e=E_MAX; a=A_MIN; h=F(1,375); rho=F(1,54)
    lo=a-rho; hi=1+rho; s=hi+h/2; r0=F(3999,4000)
    rows=[]
    def positive(name,q):
        q=F(q); need(q>0,'budget: '+name)
        rows.append({'name':name,'strict_margin':str(q)})
    def tail(tau,r): return tau/((r-tau)*r**3)
    A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)}
    A[7]=F(9,14)
    Cd=sum(j*A[j]*s**(j-1) for j in A)
    div=9*lo**8-18*s**7*h-Cd*h
    Nc=F(7,4)*sum(A[j]*hi**j for j in (1,2,4,5,7))
    Be=4*s**7/(25*lo**8)+Cd/(45*lo**8)
    B={5:F(63,32),4:F(63,32)*rho,
       2:F(9,128)*rho*h,1:F(9,4096)*h*h}
    higher=sum(B[j]*lo**(j-7) for j in B)
    pair=(1+2*rho)*Be+F(1,50)+higher/6
    individual=(1+2*rho)*Be+F(1,50)+higher/5
    positive('global42 entry below fixedH375',h-42*e)
    positive('broad mean/RMS bound',8*rho*rho-h)
    positive('broad centered radius1/19',F(1,19)**2-h)
    positive('broad positive tail denominator',lo-F(1,19))
    positive('finite reciprocal denominators after entry',a*a-h)
    positive('broad nine counted circles',F(9,2)*lo**8-9*s**7*h-sum(A[j]*(s**j+hi**j) for j in A))
    positive('broad disjoint circles',F(4,9)*lo-h)
    positive('broad positive full root divisor',div)
    positive('broad cube displacementV/5',div/5-Nc)
    positive('broad cube linear displacementV/5',9*lo**8/5-Nc)
    positive('broad whole pair quadratic normal4/5',changes.get('pair_cap',F(4,5))-pair)
    positive('broad whole individual quadratic normal7/8',changes.get('individual_cap',F(7,8))-individual)
    positive('individual higher coefficient sqrt3/9 below1/5',F(1,25)-F(1,27))
    positive('broad objective lower8/r-3V/5',F(3,5)-F(1,2)/lo**3-tail(F(1,19),lo))
    positive('broad lowF lower radius3999/4000',1-(3*e+F(3,5)*h)/8-r0)
    positive('positive Q coefficient in staged bootstrap',F(3,4)/hi**3-F(4,7))
    kappa=F(4,7)-F(1,2)/r0**3-tail(F(1,19),r0)-F(1216,225)*h
    positive('credited whole retained mean square divisor1/1000',kappa-F(1,1000))
    positive('first retained-square mean below1/375',(F(1,375)-2*h/15)**2-e/12-e*e/3)
    positive('sqrt eta below1/126',F(1,126)**2-e)
    positive('sqrt(1/12+e/3) below361/1250',F(361,1250)**2-F(1,12)-e/3)
    positive('first mean-square beloweta/9',F(1,3)-F(28,5*126)-F(361,1250))
    initial_pair=42*F(1,375)/5+F(4,5)*42**2*e
    initial_individual=42*F(1,375)/5+F(7,8)*42**2*e
    early_lo=1-F(141,40)*e
    positive('early upper radius1+3eta',6+F(2,3)-42/F(7)-F(4,3)*initial_pair-e/3)
    positive('early positive radius denominator',early_lo-F(6,125))
    positive('early inverse-cube adjustment11eta',changes.get('early_inverse_cube',11)-3*F(141,40)/early_lo**4)
    positive('initial M upper3eta',3+F(5,8)*a*a-F(1,18)/a-F(3,40)*42)
    positive('initial M lower-4eta',4-(F(2,3)+42/F(14)+F(2,3)*initial_pair)/a)
    positive('initial individual slack3eta/5',F(3,5)-F(1,16)-(F(45,16)+F(21,8)*42)*e-F(3,16)*42*tail(F(6,125),early_lo)-initial_individual)
    positive('initial D below15eta/4',F(15,4)-(3+F(7,6)*F(3,5))/a)
    positive('initial mean below11eta/2',F(11,2)**2-4**2-F(15,4)**2)
    stages=((42,F(6,125),38),(38,F(23,500),28),(28,F(1,25),16),
            (16,F(3,100),10),(10,F(3,125),8),(8,F(21,1000),F(15,2)),
            (F(15,2),F(41,2000),changes.get('last_stage_target',7)))
    stage_records=[]
    for cap,tau,target in stages:
        positive('stage centered radius fromV'+str(cap)+'eta',tau*tau-F(7,8)*cap*e)
        beta=F(4,7)-F(1,2)/r0**3-tail(tau,r0)-F(16,3)*(F(11,2)*e/5+F(4,5)*cap*e)
        positive('stage positive divisor fromV'+str(cap)+'eta',beta)
        positive('stage contractV below'+str(target)+'eta',target*beta-F(1,3)-4*e/3)
        stage_records.append({'prior_V_cap':str(cap),'tau':str(tau),
                              'new_V_cap':str(target),'whole_divisor':str(beta)})
    positive('V7 lower radius1-eta',1-(3+F(3,5)*7)/8)
    positive('V7 upper radius1+eta',2-F(7,7)-F(4,3)*(F(11,2)*7/5+F(4,5)*49)*e)
    positive('final-box inverse-cube adjustment4eta',4-3/a**4)
    variance_tau=F(1,50)
    positive('V7 signed-cubic full-tail radius',variance_tau**2-F(7,8)*7*e)
    Gv=1/((a-variance_tau)*a**4); Kv=F(3,2)/a**4
    variance_error=F(976,225)+alpha*(Gv+F(7,10)*Kv*Kv)
    positive('signed cubic TWO squares giveV5eta',5*(F(1,14)-4*e-7*variance_error*e)-F(1,3)-4*e/3)
    positive('V5 centered radius1/60',TAU*TAU-F(7,8)*5*e)
    qt=tail(TAU,a)
    positive('joint7V+5Q below12eta',12-F(28,3)-(F(112,3)+112*5)*e-28*5*qt-F(448,3)*F(51,2)*e)
    positive('final individual slacketa/12',F(1,12)-F(1,16)-(F(45,16)+F(21,16)*5)*e-F(3,16)*5*qt-F(219,8)*e)
    positive('final M strictly negative',a*a/4-F(1,18)/a)
    positive('final M cap4eta/5',F(4,5)-(F(2,3)+F(1,14)+F(2,3)*F(51,2)*e)/a)
    positive('final D capeta/3',F(1,3)-(F(5,28)+F(7,72))/a)
    positive('sqrt6 below5/2',F(25,4)-6)
    positive('2/sqrt3 below7/6',F(49,36)-F(4,3))
    lr=F(1,160); lv=5*e; lminus=a-lr; lplus=1+lr; ls=lplus+lv/2
    positive('fine mean below1/160',lr-F(13,15)*e)
    LA={j:F(9,8*j)*comb(8,9-j)*lr**(7-j) for j in range(1,7)}
    LA[7]=F(9,14)
    lcd=sum(j*LA[j]*ls**(j-1) for j in LA)
    ldiv=9*lminus**8-18*ls**7*lv-lcd*lv
    positive('fine nine counted circles',F(9,2)*lminus**8-9*ls**7*lv-sum(LA[j]*(ls**j+lplus**j) for j in LA))
    positive('fine disjoint circles',F(4,9)*lminus-lv)
    positive('fine positive root divisor',ldiv)
    LH={5:F(63,32),4:F(63,32)*lr,3:F(21,128)*lv,
        2:F(9,128)*lr*lv,1:F(9,4096)*lv*lv}
    for D,name,ids,coefficient in ((F(1,6),'cube',(1,2,4,5,7),F(7,4)),
                                  (changes.get('all_phase_scale',F(1,4)),'all-phase',tuple(range(1,8)),F(2))):
        N=coefficient*sum(LA[j]*lplus**j for j in ids)
        positive(name+' full displacement',D*ldiv-N)
        positive(name+' linear displacement',D*9*lminus**8-N)
        mb=4*ls**7*D*D/lminus**8+D*lcd/(9*lminus**8)
        if name=='cube':
            for hc in (F(1,6),F(1,5)):
                positive('fine cube complete normal '+str(hc),1-(1+2*lr)*mb-D*D/2-hc*sum(LH[j]*lminus**(j-7) for j in (1,2,4,5)))
        else:
            lhigher=sum(LH[j]*lminus**(j-7) for j in LH)
            positive('all-phase complete quadratic normal9/8',F(9,8)-(1+2*lr)*mb-D*D/2-F(2,9)*lhigher)
            positive('all-phase complete non-T root error1',1-mb-F(2,9)/a*lhigher)
    positive('whole R3 below29eta2',29-F(1,2)-F(3,2)*F(4,5)-F(3,2)*F(169,225)-F(13,15)*5/6-25)
    positive('whole R4 without signed cubic below33eta2',33-F(1,2)-2*F(4,5)-2*F(169,225)-F(13,15)*5/4-F(9,8)*25)
    positive('whole individual cube E3 below26eta2',26-F(13,15)*5/6-25)
    positive('whole objective noncubic cost36',36-8*F(4,5)*(2-e)/a**2-4*F(169,225)/a**3-20)
    positive('whole dual normal cost190',190-36-29*F(23,5)-33*F(3,5))
    G=1/((a-TAU)*a**4); K=F(3,2)/a**4+F(3,20)/a
    positive('positive infinite-tail denominator',a-TAU)
    positive('whole physical quadratic error272',error-190-25*alpha*(G+K*K))
    positive('whole unconditional quadratic error243',objective_error-190-25*alpha*(G+K*K/2))
    positive('unconditional slope141/50',F(826,291)-objective_error*e-F(141,50))
    positive('sqrt272 above16',error-16**2)
    positive('cube residual/slack below3Delta/8',F(3,8)-F(1,4)-29/error)
    positive('fourth residual with signed cubic belowDelta/2',F(1,2)-33/error-F(5,32)/a)
    M=F(62,651)*F(3,8)+F(128,217)*F(5,2)
    Y=F(24832,32550)*F(3,8)+F(128,217)*F(5,2)
    positive('real mean inversion8Delta/5',F(8,5)-M)
    positive('negative rotated trace inversion9Delta/5',F(9,5)-Y)
    positive('rotated trace difference26Delta',26-14*F(9,5))
    positive('critical energy difference35Delta',1-8*F(169,225)/error)
    positive('unrotated real energy13Delta',1-F(384,25)/error-4*e/(error*a*a))
    positive('imaginary mean sqrt coefficient1',196*a*a-80)
    positive('imaginary mean Delta coefficient1',1-F(7,24)/a)
    positive('imaginary mean eta2 coefficient31',31-F(7,6)*26/a)
    positive('sqrt80 below9',81-80)
    positive('complete mu3 coefficient21/2',F(21,10)**2-F(35,8))
    positive('whole original eta2 aggregate88',88-62-25-F(896,1395)/a)
    positive('all9 original Delta coefficient19/2',F(19,2)-F(26,5)-F(26,7)/a-88/error)
    positive('all9 original sqrt coefficient7/2',F(7,2)-2-F(9,7)/a-F(7,96)/a**2)
    clo=F(15,16); chi=F(47,50)
    positive('selected cosine lower sign',-(8*clo**3-6*clo-1))
    positive('selected cosine upper sign',8*chi**3-6*chi-1)
    positive('selected cosine monotone',24*clo**2-6)
    positive('w4 below3/5',F(3,5)-F(128,217))
    positive('w4 above1/2',F(625,1067)-F(1,2))
    positive('w3 above4',F(2,3)*(7-F(31,217))-4)
    positive('w3 below23/5',F(23,5)-F(2,3)*(7-F(291,2134)))
    return {'eta_endpoint':str(e),'physical_error':str(error),
        'objective_error':str(objective_error),'quartic_factor':str(alpha),'G':str(G),'K':str(K),
        'broad_energy':str(h),'broad_rho':str(rho),'broad_pair_coefficient':str(pair),
        'broad_individual_coefficient':str(individual),'early_radius_floor':str(early_lo),
        'credited_kappa':str(kappa),'variance_G':str(Gv),'variance_K':str(Kv),
        'variance_error':str(variance_error),'stages':stage_records,
        'fine_rho':str(lr),'fine_V_endpoint':str(lv),'rows':rows}
