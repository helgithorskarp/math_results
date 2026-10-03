"""Actual input-to-LC forward bridge on eta<=1/12000.

Actual six-sendov-3 / researcher. Explicitly credited f785 input; no
old numerical transport. Two FULL real-energy squares before any V7 box.
All analytic steps are in BOOTSTRAP.md; Fraction records corroborate them.
"""
from arithmetic import F,comb,need


def bootstrap_budgets(changes=None):
    changes={} if changes is None else changes
    e=F(1,12000);a=1-e;h=F(1,320);rho=F(1,50);r0=F(9997,10000);tau=F(21,400)
    lo=a-rho;hi=1+rho;s=hi+h/2
    A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)};A[7]=F(9,14)
    Cd=sum(j*A[j]*s**(j-1) for j in A);div=9*lo**8-18*s**7*h-Cd*h
    N=F(7,4)*sum(A[j]*hi**j for j in (1,2,4,5,7));Be=4*s**7/(25*lo**8)+Cd/(45*lo**8)
    B={5:F(63,32),4:F(63,32)*rho,2:F(9,128)*rho*h,1:F(9,4096)*h*h}
    higher=sum(B[j]*lo**(j-7) for j in B)
    rows=[]
    def p(n,x):
     x=F(x);need(x>0,'bootstrap budget: '+n);rows.append({'name':n,'strict_margin':str(x)})
    def tail(t,r):return t/((r-t)*r**3)
    p('actual37 entry belowH320',h-37*e)
    p('broad RMS',8*rho*rho-h)
    p('broad centered max',tau*tau-F(7,8)*h)
    p('broad9circle',F(9,2)*lo**8-9*s**7*h-sum(A[j]*(s**j+hi**j) for j in A))
    p('broadcubeV5',div/5-N)
    p('broadpair4/5',F(4,5)-(1+2*rho)*Be-F(1,50)-higher/6)
    p('broadindividual7/8',F(7,8)-(1+2*rho)*Be-F(1,50)-higher/5)
    p('broadFbound3V5',F(3,5)-F(1,2)/lo**3-tail(tau,lo))
    p('initialradiusr0',1-(3*e+F(3,5)*h)/8-r0)
    kappa=F(4,7)-F(1,2)/r0**3-tail(tau,r0)-F(976,225)*h
    p('retainedmeansquarekappa600',kappa-F(1,600))
    p('firstmeansquaretbelowh',(h-2*h/15)**2-e/12-e*e/3)
    p('initialsqrteta109',F(1,109)**2-e)
    p('initialsqrt3611250',F(361,1250)**2-F(1,12)-e/3)
    p('first t2beloweta8',F(1,8)-(F(74,15*109)+F(361,1250))**2)
    ap=37*h/5+F(4,5)*37**2*e;ai=37*h/5+F(7,8)*37**2*e;early=1-F(141,40)*e
    p('earlyradiuslo legal',F(141,40)-(3+F(3,5)*37)/8)
    p('earlyrupper1+3eta',6+F(2,3)-F(37,7)-F(4,3)*ap-e/3)
    early_cost=F(changes.get('early_inverse_cost',11))
    p('earlyinverse11',early_cost-3*F(141,40)/early**4)
    p('initialMupper3',3+F(5,8)*a*a-F(1,16)/a-F(3,40)*37)
    p('initialMlower4',4-(F(2,3)+F(37,14)+F(2,3)*ap)/a)
    p('initialslack3eta5',F(3,5)-F(1,16)-(F(45,16)+F(21,8)*37)*e-F(3,16)*37*tail(tau,early)-ai)
    p('initialD15/4',F(15,4)-(F(37,14)+F(7,6)*F(3,5))/a)
    p('initialmean11/2',F(11,2)**2-16-F(15,4)**2)
    stages=[]
    for prior,target,inv,rmin,tt in ((37,F(changes.get('early_target',7)),early_cost,early,tau),(7,5,4,a,F(23,1000))):
     p('variance radius '+str(prior),tt*tt-F(7,8)*prior*e)
     G=1/((rmin-tt)*rmin**4);K=F(3,2)/rmin**4
     Bv=F(976,225)+F(7,8)*(G+F(7,10)*K*K)
     coef=F(1,14)-inv*e-prior*Bv*e
     p('TWO squares '+str(prior)+'to'+str(target),target*coef-F(1,3)-4*e/3)
     stages.append({'prior_V_cap':str(prior),'new_V_cap':str(target),'inverse_cube_cost':str(inv),'radius_floor':str(rmin),'full_tail_radius':str(tt),'whole_G':str(G),'whole_K':str(K),'complete_square_cost':str(Bv),'whole_divisor':str(coef)})
    p('V7 rlo1-eta',1-(3+F(3,5)*7)/8)
    p('V7 rhi1+eta',2-F(7,7)-F(4,3)*(F(11,2)*7/5+F(4,5)*49)*e)
    p('final inverse4',4-3/a**4)
    rhof=F(1,128);v=5*e;hif=1+e;sf=hif+v/2;tp=F(11,2)*e
    Af={j:F(9,8*j)*comb(8,9-j)*rhof**(7-j) for j in range(1,7)};Af[7]=F(9,14)
    Cdf=sum(j*Af[j]*sf**(j-1) for j in Af)
    Bef=sf**7/(9*a**8)+Cdf/(54*a**8)
    Bf={5:F(63,32),4:F(63,32)*rhof,2:F(9,128)*rhof*v,1:F(9,4096)*v*v}
    highf=sum(Bf[j]*a**(j-7) for j in Bf)
    p('preliminary fine pair9/16',F(9,16)-(hif+tp)*Bef-F(1,72)-highf/6)
    p('preliminary fine individual5/8',F(5,8)-(hif+tp)*Bef-F(1,72)-highf/5)
    Ep=F(895,48);Ei=F(485,24);tf=F(1,50);qt=tail(tf,a)
    p('V5 fulltailradius1/50',tf*tf-F(7,8)*v)
    joint_cap=F(changes.get('joint_cap',13))
    p('joint7V+5Q below13eta',joint_cap-F(28,3)-(F(112,3)+560)*e-140*qt-F(448,3)*Ep*e)
    p('Jmax squared below8/3',F(64,9)-joint_cap*joint_cap/24)
    p('finalslacketa10',F(1,10)-F(1,16)-(F(45,16)+F(105,16))*e-F(15,16)*qt-Ei*e)
    p('finalDeta3',F(1,3)-(F(4,21)+F(7,60))/a)
    p('finalMnegative',a*a/4-F(1,16)/a)
    p('finalM4eta5',F(4,5)-(F(2,3)+F(13,168)+F(2,3)*Ep*e)/a)

    return {'eta_endpoint':str(e),'input_H_cap':'37eta<1/320','input_mean_square':'f785 H<=1/320,positivekappa retained square AFTER genuine actual entry',
     'broad_rho':str(rho),'broad_energy_endpoint':str(h),'broad_radius_floor':str(lo),'broad_radius_ceiling':str(hi),
     'broad_pair_cost':str((1+2*rho)*Be+F(1,50)+higher/6),'broad_individual_cost':str((1+2*rho)*Be+F(1,50)+higher/5),
     'credited_kappa':str(kappa),'early_V_cap':'37','early_mean_cap':'11eta/2','early_radius_floor':str(early),
     'EARLY_inverse_cube_cost':str(early_cost),'FINAL_inverse_cube_cost':'4','two_square_forward_stages':stages,
     'preliminary_fine_pair_cost':str((hif+tp)*Bef+F(1,72)+highf/6),'preliminary_fine_individual_cost':str((hif+tp)*Bef+F(1,72)+highf/5),
     'preliminary_fine_pair_eta2_cost':str(Ep),'preliminary_fine_individual_eta2_cost':str(Ei),'final_joint_trace_cap':str(joint_cap),
     'conclusions':['V<5eta','-4eta/5<M<0','|D|<eta/3','|m|<13eta/15','1-eta<r<1+eta'],
     'all_complete_margins':rows}
