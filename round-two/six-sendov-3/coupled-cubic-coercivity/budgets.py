"""Exact whole-window budgets for the joint cubic and fresh stability.

Actual six-sendov-3 / researcher. The domain/local estimates are CREDITED
9857; these Fraction calculations do not prove its analytic bridges.
"""
from arithmetic import F, need

ETA_MAX=F(1,16000)
A_MIN=1-ETA_MAX
V_MAX=5*ETA_MAX
TAU=F(1,60)
BETA_CAP=F(271,200)
PHYSICAL_ERROR=F(247)
OBJECTIVE_ERROR=F(230)


def budgets(changes=None):
    changes={} if changes is None else changes
    e=ETA_MAX; a=A_MIN; hi=1+e; v=V_MAX
    b=F(changes.get('beta_cap',BETA_CAP))
    physical=F(changes.get('physical_error',PHYSICAL_ERROR))
    objective=F(changes.get('objective_error',OBJECTIVE_ERROR))
    alpha=F(7,8)
    w4lo=F(625,1067); w4hi=F(3,5)
    rows=[]
    def positive(name,q):
        q=F(q); need(q>0,'budget: '+name)
        rows.append({'name':name,'strict_margin':str(q)})
    positive('local positive radius floor',a)
    positive('local positive full tail denominator',a-TAU)
    positive('local centered radius from V5',TAU**2-alpha*v)
    positive('joint A is positive',hi**-4-w4hi/(12*a))
    positive('joint beta minus A is positive',F(1,2)*hi**-4-w4hi/(6*a))
    positive('joint A below1',1-a**-4+w4lo/(12*hi))
    beta_max=F(3,2)*a**-4-w4lo/(4*hi)
    positive('joint beta below271/200',b-beta_max)
    k=F(3,4)*b*b; q=b*(1+b)/4
    routes=[]
    for name,delta,default_lambda in (('physical',F(1,4),F(69,50)),
                                    ('objective',F(1,2),F(69,100))):
        lam=F(changes.get(name+'_lambda',default_lambda))
        a0=delta*delta-q*v
        b0=delta*lam-k/2
        det=a0*lam*lam-b0*b0
        positive(name+' positive E-square coefficient',a0)
        positive(name+' positive full determinant',det)
        routes.append({'name':name,'delta':str(delta),'lambda':str(lam),
          'a0':str(a0),'b0':str(b0),'determinant':str(det),
          'V_fourth_square_remainder':str(det/a0)})
    G=1/((a-TAU)*a**4)
    physical_lambda=F(routes[0]['lambda']); objective_lambda=F(routes[1]['lambda'])
    full_physical_cost=190+25*(alpha*G+physical_lambda)
    full_objective_cost=190+25*(alpha*G+objective_lambda)
    positive('complete physical error247',physical-full_physical_cost)
    positive('complete objective error230',objective-full_objective_cost)
    positive('unconditional slope141/50',F(826,291)-objective*e-F(141,50))
    positive('entire paired R3 cap29',29-F(1,2)-F(3,2)*F(4,5)-F(3,2)*F(169,225)-F(13,15)*5/6-25)
    positive('entire paired R4 noncubic cap33',33-F(1,2)-2*F(4,5)-2*F(169,225)-F(13,15)*5/4-F(9,8)*25)
    positive('entire individual cube error26',26-F(13,15)*5/6-25)
    positive('complete objective noncubic cost36',36-8*F(4,5)*(2-e)/a**2-4*F(169,225)/a**3-20)
    positive('complete dual noncubic cost190',190-36-29*F(23,5)-33*F(3,5))
    sqrt_floor=F(changes.get('sqrt_physical_floor',F(31,2)))
    positive('sqrt247 above31/2',physical-sqrt_floor**2)
    positive('fresh cube normal below3Delta/8',F(3,8)-F(1,4)-29/physical)
    positive('fresh fourth residual belowDelta/2',F(1,2)-33/physical-F(5,2)/(sqrt_floor*a))
    M=F(62,651)*F(3,8)+F(128,217)*F(5,2)
    Y=F(24832,32550)*F(3,8)+F(128,217)*F(5,2)
    positive('Cramer mean8Delta/5',F(8,5)-M)
    positive('Cramer negative rotated trace9Delta/5',F(9,5)-Y)
    positive('rotated trace26Delta',26-14*F(9,5))
    positive('variance34Delta with strict Cramer trace',34-14*Y-8)
    positive('critical energy35Delta',1-8*F(169,225)/physical)
    positive('unrotated real energy13Delta',1-F(384,25)/physical-4*e/(physical*a*a))
    positive('imaginary mean sqrt coefficient1',196*a*a-80)
    positive('imaginary mean Delta coefficient1',1-F(7,24)/a)
    positive('imaginary mean eta2 coefficient31',31-F(7,6)*26/a)
    positive('sqrt80 below9',81-80)
    positive('complete mu3 coefficient21/2',F(21,10)**2-F(35,8))
    positive('whole original eta2 coefficient88',88-62-25-F(896,1395)/a)
    positive('all9 original Delta coefficient19/2',F(19,2)-F(26,5)-F(26,7)/a-88/physical)
    positive('all9 original sqrt coefficient7/2',F(7,2)-2-F(9,7)/a-F(7,6)/(sqrt_floor*a*a))
    clo=F(15,16); chi=F(47,50)
    positive('selected cosine lower sign',-(8*clo**3-6*clo-1))
    positive('selected cosine upper sign',8*chi**3-6*chi-1)
    positive('selected cosine monotone',24*clo**2-6)
    positive('w4 below3/5',F(3,5)-F(128,217))
    positive('w4 above1/2',w4lo-F(1,2))
    positive('w3 above4',F(2,3)*(7-F(31,217))-4)
    positive('w3 below23/5',F(23,5)-F(2,3)*(7-F(291,2134)))
    # These endpoint equalities become STRICT by c>clo and monotonicity;
    # an endpoint equality is never recorded as a positive rational margin.
    positive('Cramer determinant monotone',1+4*clo)
    positive('Cramer B4 strictly decreases',4*clo)
    need(F(3,2)*(clo+2*clo**2-1)==F(651,256),'Cramer determinant endpoint equality')
    need(2-2*clo**2==F(31,128),'Cramer B4 endpoint equality')
    return {'eta_endpoint':str(e),'local_radius_floor':str(a),'V_endpoint':str(v),
      'beta_cap':str(b),'beta_endpoint_upper':str(beta_max),'k':str(k),'q':str(q),
      'quartic_factor':str(alpha),'G':str(G),'routes':routes,
      'physical_error':str(physical),'objective_error':str(objective),
      'complete_physical_cost':str(full_physical_cost),
      'complete_objective_cost':str(full_objective_cost),
      'stability_sqrt_floor':str(sqrt_floor),
      'Cramer_endpoint_equalities':{'determinant':'651/256','B4':'31/128'},'rows':rows}
