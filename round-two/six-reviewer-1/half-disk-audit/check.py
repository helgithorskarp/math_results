"""Fresh constants and continuous-proof obligations for original and enlarged budgets.

Written target proof/data exposed. Native checker/fixture not used or imported.
Checks finite exact algebra, not the surrounding ordinary analytic proof.
"""
from fractions import Fraction as Q
from exact import (require,add,scale,mul,power,integrate,bernstein,
                   binomial_integral,newton_constants,encode)
import json

BASE_CELLS = [(Q(0),Q(1,2),Q(2,3)),(Q(1,2),Q(1),Q(1)),
              (Q(1),Q(3,2),Q(7,6)),(Q(3,2),Q(2),Q(4,3)),
              (Q(2),Q(5,2),Q(3,2)),(Q(5,2),Q(3),Q(5,3)),
              (Q(3),Q(56,9),Q(7,3))]
A_CELLS = [(Q(2,5),Q(9,20)),(Q(9,20),Q(1,2))]

def polar_cells(eta):
    previous_a=Q(2,5)
    for lo,hi in A_CELLS:
        require(lo==previous_a and hi>=lo,'complete closed a cover')
        require(Q(2,5)<=lo<=hi<=Q(1,2),'original marked-a domain')
        previous_a=hi
    require(previous_a==Q(1,2),'right closed marked endpoint')
    tmax=Q(56,9)+Q(14,3)*eta+eta**2
    cells=[]
    previous=Q(0)
    for index,(lower,upper,d0) in enumerate(BASE_CELLS):
        if index==6: upper=tmax
        d=d0+(2*eta if index==6 else eta)
        require(lower==previous and upper>=lower,'closed T cover')
        require((d-eta)**2>=Q(7,8)*upper,'positive radial ceiling')
        previous=upper
        p=max(Q(0),(3-upper)/2)
        for lo,hi in A_CELLS:
            bh=1-hi**2; ceiling=hi+bh
            denominator=hi+(1-lo**2)*(1+d)
            k1=lo*(1-lo**2)*p/denominator**2
            k2=bh**2*lower/(2*ceiling*denominator)
            loss=[Q(0),k1,k2]
            kernel=add(add([Q(1)],scale(loss,-1)),scale(mul(loss,loss),Q(1,2)))
            polynomial=mul(power([hi,bh],8),kernel)
            polynomial += [Q(0)]*(13-len(polynomial))
            u=integrate(polynomial)
            bs=bernstein(polynomial,12)
            require(u==sum(bs)/13,'full Bernstein integral')
            moments=[binomial_integral(hi,bh,8,j) for j in range(5)]
            direct=(moments[0]-k1*moments[1]+(-k2+k1*k1/2)*moments[2]
                    +k1*k2*moments[3]+k2*k2/2*moments[4])
            require(u==direct,'complete binomial kernel integral')
            # exp(eta) <= 1/(1-eta), proved analytically for eta in [0,1).
            require(0<=eta<1,'exponential budget domain')
            inflated=u/(1-eta)
            require(inflated<Q(199,200),'all fourteen strict polar gates')
            cells.append(dict(a=[lo,hi],T=[lower,upper],d=d,phase_floor=p,
                              k1=k1,k2=k2,coefficients=polynomial,
                              bernstein_degree12=bs,integral=u,
                              exponential_majorant=inflated,
                              strict_gate_slack=Q(199,200)-inflated))
    require(previous==tmax and len(cells)==14,'complete closed cover cardinality')
    return cells

def origin(eta):
    m=1+eta/8; squared=m*m; gamma=Q(63,80)
    constants=newton_constants()
    beta=[Q(1),-gamma,squared/4]  # x=t/2
    items=[]
    for ell in range(2,9):
        if ell%2:
            h=mul(power(beta,(7-ell)//2),scale(add([Q(1)],beta),Q(1,2)))
            deviation=Q(7,4)*3**((ell-1)//2)
        else:
            h=power(beta,(8-ell)//2)
            deviation=Q(3)**(ell//2)
        polynomial=scale([Q(0)]*ell+h,Q(9,2**ell)*constants[ell]*deviation)
        integral=integrate(polynomial)
        bs=bernstein(polynomial,len(polynomial)-1)
        require(integral==sum(bs)/len(bs),'whole origin Bernstein integral')
        items.append(dict(order=ell,coefficients=polynomial,bernstein=bs,
                          integral=integral,constant=constants[ell]))
    remainder=sum(x['integral'] for x in items)
    require(remainder<Q(111,128),'complete seven-order remainder cap')
    # Derivative completion of square in ORIGINAL x, for beta=1-2gamma*x+c*x^2.
    # 2beta+3x beta' = 8(x-63/128)^2+127/2048+8(c-1)x^2.
    derivative=[Q(2),-10*gamma,8*squared]
    square=add(power([-Q(63,128),Q(1)],2),[Q(127,16384)])
    square=add(scale(square,8),[Q(0),Q(0),8*(squared-1)])
    require(derivative==square,'entire derivative square identity')
    require(squared<2*gamma,'beta decreasing on original x interval')
    require(squared>=1,'derivative nonnegative surplus')
    # beta is positive: 1-2gamma*x+x^2 >=1-gamma^2, c>=1.
    require(1-gamma**2>0,'whole beta positive')
    diagonal=1-2*Q(2,5)*gamma+Q(4,25)*squared
    require(diagonal<Q(9,16),'diagonal square-root bound')
    require(Q(3,4)*diagonal**4<Q(1,16),'ninth-power diagonal gate')
    origin_floor=Q(15,8)/m-Q(111,128)
    require(origin_floor>m**8,'original AM-GM contradiction with enlarged mass')
    return dict(constants=constants,seven_terms=items,remainder=remainder,
                remainder_slack=Q(111,128)-remainder,
                mean_ceiling=m,mean_real_floor=gamma,
                derivative_coefficients=derivative,diagonal_beta_ceiling=diagonal,
                origin_strict_floor=origin_floor,original_product_ceiling=m**8,
                original_contradiction_slack=origin_floor-m**8)

def record(eta):
    m=1+eta/8
    small=integrate(power([Q(2,5),Q(21,25)*m],8))
    mass=integrate(power([Q(1,2),Q(117,160)],8))
    require(small==binomial_integral(Q(2,5),Q(21,25)*m,8),'whole small-a integral')
    require(mass==binomial_integral(Q(1,2),Q(117,160),8),'whole mass floor integral')
    require(small<1 and mass<1,'closed small-a and mass-floor exclusions')
    require(Q(4,5)*m<1,'small-a monotonicity with enlarged mass')
    require(m**8<9,'a=0 product margin')
    return dict(eta=eta,closed_budget=8+eta,scalar_small_a=small,
                scalar_mass_floor=mass,polar=polar_cells(eta),origin=origin(eta))

def build():
    return encode(dict(agent='six-reviewer-1',role='independent mathematical reviewer',
                       original=record(Q(0)),refinement=record(Q(1,1000))))

if __name__=='__main__':
    print(json.dumps(build(),sort_keys=True,separators=(',',':')))
