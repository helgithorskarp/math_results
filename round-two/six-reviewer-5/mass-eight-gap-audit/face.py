"""Fresh independent centered/face arithmetic. No author executable input."""
import hashlib
import importlib.util
import itertools
import json
import math
import pathlib
from fractions import Fraction as F

HERE = pathlib.Path(__file__).resolve().parent
BASE_PIN = 'b47b4a46202c60c3353d05f5b69d73fa735dfc25f90fa473cc5cd87175ddf281'
COVER_PIN = '70a773a61a3a7074719c124318ae8e9bf2e6b5d7719af45709dcefed2b8ed55a'
if hashlib.sha256((HERE/'base.py').read_bytes()).hexdigest() != BASE_PIN:
    raise ValueError('owned pure helper pin BEFORE import')
spec = importlib.util.spec_from_file_location('r5_owned_base', HERE/'base.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

def trinomial_power(coefficients, degree):
    result = [F(0)]*(2*degree+1)
    for constant in range(degree+1):
        for linear in range(degree-constant+1):
            quadratic = degree-constant-linear
            result[linear+2*quadratic] += F(math.factorial(degree), math.factorial(constant)*math.factorial(linear)*math.factorial(quadratic))*coefficients[0]**constant*coefficients[1]**linear*coefficients[2]**quadratic
    return result

def centered_constants():
    eta = {2:F(1)}
    endpoint_records = []
    for m in (2, 3, 4):
        high = F(7,8)**m+F(1,8)**m
        b.require(high >= F(1,2)**(m-1), 'both even-moment regimes')
        eta[2*m] = high
        endpoint_records.append(dict(order=2*m, small_radius_regime=F(1,2)**(m-1), endpoint=high))
    for k in (3,5,7):
        eta[k] = b.root_grid(eta[k-1]*eta[k+1], 1024, True)
    tau = b.root_grid(F(1,8), 1024, True)
    c = [F(1),F(0)]
    steps = []
    for k in range(2,9):
        newton_terms = [c[k-j]*eta[j]/k for j in range(2,k+1)]
        newton = sum(newton_terms)
        maclaurin = F(math.comb(8,k), 8**(k//2))*(tau if k%2 else 1)
        c.append(min(newton,maclaurin))
        steps.append(dict(order=k, newton_terms=newton_terms, newton=newton, maclaurin=maclaurin, chosen=c[-1]))
    b.require(c[2:] == list(map(F,('1/2','151/512','41/128','1497/5120','7/128','363/65536','1/4096'))), 'all seven derived claimed coefficients')
    initial = c[:]
    # REAL Banach theorem is an explicitly cited ordinary external premise.
    # Its complexification is proved in PROOF.md, not assumed norm-preserving.
    real_min = F(1,8)-F(25,32)/4
    real_max = F(1,8)-F(1,8)/4
    norm = max(-real_min,real_max)
    b.require((real_min,real_max,norm) == (F(-9,128),F(3,32),F(3,32)), 'whole real quartic interval/norm')
    c[4] = 2*norm
    b.require(c[4] == F(3,16) and c[:4]+c[5:] == initial[:4]+initial[5:], 'only quartic replaced; no later Newton reoptimization')
    return c, dict(even_moments=endpoint_records, eta=eta, tau=tau, all_newton_steps=steps, initial=c[:4]+[initial[4]]+c[5:], final=c, real_quartic_interval=[real_min,real_max], real_norm=norm)

def quartic_controls():
    records=[]
    seeds=[([1,1,1,1,-1,-1,-1,-1],[1,-1,2,-2,3,-3,4,-4]), ([0,1,2,3,4,5,6,-21],[2,3,5,7,11,13,17,-58]), ([1,-1,0,0,0,0,0,0],[0,0,1,-1,0,0,0,0]), ([1,1,1,1,-1,-1,-1,-1],[1,1,1,1,-1,-1,-1,-1])]
    for x,y in seeds:
        b.require(sum(x)==sum(y)==0, 'formal centered quartic fixture')
        direct=[F(0)]*5
        for subset in itertools.combinations(range(8),4):
            term=[F(1)]
            for i in subset:term=b.multiply(term,[F(x[i]),F(y[i])])
            direct=b.add(direct,term)
        p2=b.add(*[b.power([F(x[i]),F(y[i])],2) for i in range(8)])
        p4=b.add(*[b.power([F(x[i]),F(y[i])],4) for i in range(8)])
        newton=b.add(b.scale(b.power(p2,2),F(1,8)),b.scale(p4,F(-1,4)))
        b.require(direct==newton, 'whole quartic elementary/Newton coefficients')
        real_at_i=direct[0]-direct[2]+direct[4]
        imag_at_i=direct[1]-direct[3]
        records.append(dict(x=x,y=y,all_five_coefficients=direct,real_at_i=real_at_i,imag_at_i=imag_at_i,mixed_fourlinear_value=direct[2]/6))
    b.require(records[-1]['all_five_coefficients'][2] == 6*records[-1]['all_five_coefficients'][0] != 2*records[-1]['all_five_coefficients'][0], 'six mixed quartic terms, not two')
    # At equal X=Y=1, the real-norm complexification upper polynomial is8M.
    # Using only M*(X+Y)^2=4M cannot pay that sufficient bound.
    b.require(F(3,32)*8 > F(3,32)*4 and F(3,16)*4 == F(3,32)*8, 'complexification loss factor required')
    return records

def scalar_origin(box, t_interval, constants):
    a, h, el, eh, ul, uh, wl, wh = box
    tl, tu = t_interval
    actual_norm = min(F(1), uh**2+wh)
    envelope_norm = min(actual_norm, ul**2+wh)
    centered_energy = min(eh-8*((1-uh)**2+wl), tu+8-8*(ul**2+wl))
    b.require(centered_energy>=0 and ul**2<=envelope_norm<=actual_norm<=1, 'scalar mean/centered-energy enclosures')
    anchor=min(a,2*ul/envelope_norm-h)
    b.require(F(3,5)<=anchor<=a<=h and 2*ul >= (anchor+h)*envelope_norm, 'scalar whole marked-interval anchor')
    beta=[F(1),-2*anchor*ul,anchor**2*envelope_norm]
    beta1=sum(beta)
    b.require(ul>anchor*envelope_norm and 0<beta1<1 and 1-anchor*ul>0, 'scalar decreasing beta/positive square')
    upper_sqrt=[F(1),-anchor*ul,anchor**2*(envelope_norm-ul**2)/(2*(1-anchor*ul))]
    dmean=b.root_grid(actual_norm,4096,True)
    dbeta=b.root_grid(beta1,4096,True)
    denergy=b.root_grid(centered_energy,4096,True)
    b.require(1-dbeta*beta1**4>0 and dmean>0, 'positive scalar diagonal numerator/actual norm denominator')
    contributions=[]
    for k in range(2,9):
        degree=(8-k)//2 if k%2==0 else (7-k)//2
        envelope=b.power(beta,degree)
        direct=trinomial_power(beta,degree)
        if k%2:
            envelope=b.multiply(envelope,upper_sqrt)
            alternative=[F(0)]*(len(direct)+2)
            for i,value in enumerate(direct):
                for j,root_term in enumerate(upper_sqrt):alternative[i+j]+=value*root_term
            direct=alternative
        factor=9*h**k*constants[k]*centered_energy**(k//2)*(denergy if k%2 else 1)
        coefficients=b.scale([F(0)]*k+envelope,factor)
        coefficients += [F(0)]*(10-len(coefficients))
        other=[F(0)]*10
        for i,value in enumerate(direct):other[k+i]+=factor*value
        b.require(coefficients==other, 'whole independent scalar remainder vector')
        value=b.integral(coefficients)
        b.require(value>=0, 'nonnegative complete scalar remainder integral')
        contributions.append(dict(order=k,full_ten_coefficients=coefficients,integral=value))
    diagonal=(1-dbeta*beta1**4)/(h*dmean)
    lower=diagonal-sum(c['integral'] for c in contributions)
    return dict(actual_mean_squared_cap=actual_norm,beta_envelope_parameter=envelope_norm,centered_energy_cap=centered_energy,anchor=anchor,beta=beta,upper_square_root=upper_sqrt,actual_norm_sqrt_ceiling=dmean,beta1_sqrt_ceiling=dbeta,centered_sqrt_ceiling=denergy,all_seven_remainders=contributions,diagonal_lower=diagonal,origin_lower=lower)

def polar_budgets(box,t_interval):
    a,h,el,eh,ul,uh,wl,wh=box
    tl,tu=t_interval
    minb,maxb=1-h*h,1-a*a
    amin=min(a*(1-a*a),h*(1-h*h))
    c=a+1-a*a-h
    excess=min(b.root_grid(F(7,8)*tu,256,True),7-7/(1+h))
    mc=h+maxb*(1+excess)
    nu=maxb*(1+excess)/mc
    b.require(excess>=0 and c>0 and 0<=nu<1, 'whole polar radius/endpoint signs')
    g2=b.add(*[b.scale(b.binomial_linear(1,-1,n),F(n+1)*nu**n/mc**2) for n in range(5)])
    return dict(a=a,h=h,el=el,minb=minb,maxb=maxb,amin=amin,c=c,excess=excess,mc=mc,nu=nu,g2=g2)

def standard_polar(box,t_interval):
    v=polar_budgets(box,t_interval)
    h,minb,c,amin=v['h'],v['minb'],v['c'],v['amin']
    tl,tu=t_interval
    delta=b.root_grid(F(tl)/56,1024,False)
    phase=max(F(0),(v['el']-tu)/2)
    b.require(c-minb*delta>0, 'standard radial positivity')
    radial=b.multiply([h,c+7*minb*delta],b.power([h,c-minb*delta],7))
    kernel=b.scale([F(0)]+v['g2'],amin*phase)
    full=b.multiply(radial,b.add([F(1)],b.scale(kernel,-1),b.scale(b.power(kernel,2),F(1,2))))
    b.require(len(full)==19, 'whole standard polar vector')
    other=[F(0)]*19
    payment=F(0)
    kernel_terms=[(1,n,amin*phase*F(n+1)*v['nu']**n/v['mc']**2) for n in range(5)]
    terms=[(0,0,F(1))]+[(i,n,-amount) for i,n,amount in kernel_terms]
    terms += [(i+j,n+m,amount*amount2/2) for i,n,amount in kernel_terms for j,m,amount2 in kernel_terms]
    for degree in range(9):
        phi=((-1)**degree*math.comb(7,degree) if degree<=7 else 0)+(7*(-1)**(degree-1)*math.comb(7,degree-1) if degree>=1 else 0)
        for linear in range(9-degree):
            value=phi*(minb*delta)**degree*math.comb(8-degree,linear)*h**(8-degree-linear)*c**linear
            for shift,n,amount in terms:
                payment += value*amount*b.beta_integral(degree+linear+shift,n)
                for j in range(n+1):other[degree+linear+shift+j] += value*amount*(-1)**j*math.comb(n,j)
    b.require(other==full and payment==b.integral(full), 'whole standard vector and separate beta payment')
    return dict(budgets=v,delta=delta,phase_floor=phase,full_nineteen_coefficients=full,upper=payment)

def sparse_add(*polynomials):
    out={}
    for polynomial in polynomials:
        for key,value in polynomial.items():out[key]=out.get(key,F(0))+value
    return {key:value for key,value in out.items() if value}

def sparse_scale(polynomial,factor):
    return {key:value*factor for key,value in polynomial.items() if value*factor}

def sparse_multiply(left,right):
    out={}
    for (d,t),v in left.items():
        for (e,u),w in right.items():
            key=(d+e,t+u)
            out[key]=out.get(key,F(0))+v*w
    return {key:value for key,value in out.items() if value}

def sparse_power(polynomial,degree):
    out={(0,0):F(1)}
    for _ in range(degree):out=sparse_multiply(out,polynomial)
    return out

def bernstein_controls(coefficients,low,high,degree):
    b.require(len(coefficients)==degree+1 and low<=high, 'whole Bernstein domain/degree')
    width=high-low
    translated=[sum((coefficients[j]*math.comb(j,k)*low**(j-k)*width**k for j in range(k,degree+1)),F(0)) for k in range(degree+1)]
    alternate=[coefficients[-1]]
    for coefficient in reversed(coefficients[:-1]):alternate=b.add(b.multiply(alternate,[low,width]),[coefficient])
    b.require(translated==alternate, 'whole independent translation')
    controls=[sum((translated[k]*F(math.comb(i,k),math.comb(degree,k)) for k in range(i+1)),F(0)) for i in range(degree+1)]
    reconstructed=[F(0)]*(degree+1)
    partition=[F(0)]*(degree+1)
    for i in range(degree+1):
        for j in range(degree-i+1):
            basis=math.comb(degree,i)*(-1)**j*math.comb(degree-i,j)
            reconstructed[i+j]+=controls[i]*basis
            partition[i+j]+=basis
    b.require(reconstructed==translated and partition==[F(1)]+[F(0)]*degree, 'every Bernstein coefficient and full unity partition')
    return dict(translated=translated,controls=controls,reconstructed=reconstructed)

def joint_polar(box,t_interval):
    v=polar_budgets(box,t_interval)
    tl,tu=t_interval
    low,high=b.root_grid(F(tl)/56,4096,False),b.root_grid(F(tu)/56,4096,True)
    h,c,minb,amin=v['h'],v['c'],v['minb'],v['amin']
    b.require(v['el']/2-28*high**2>=0 and c-minb*high>0, 'whole joint phase/radial domain')
    radial=sparse_multiply({(0,0):h,(0,1):c,(1,1):7*minb},sparse_power({(0,0):h,(0,1):c,(1,1):-minb},7))
    kernel={}
    for d,phase in ((0,v['el']/2),(2,F(-28))):
        for t,g in enumerate(v['g2']):kernel[(d,t+1)]=amin*phase*g
    exponential=sparse_add({(0,0):F(1)},sparse_scale(kernel,-1),sparse_scale(sparse_multiply(kernel,kernel),F(1,2)))
    full=sparse_multiply(radial,exponential)
    b.require(all(d<=12 and t<=18 for d,t in full), 'joint bidegree')
    matrix=[[full.get((d,t),F(0)) for t in range(19)] for d in range(13)]
    alternate=[[F(0)]*19 for _ in range(13)]
    beta_integrals=[F(0)]*13
    k_terms=[(d,1,n,amin*phase*F(n+1)*v['nu']**n/v['mc']**2) for d,phase in ((0,v['el']/2),(2,F(-28))) for n in range(5)]
    terms=[(0,0,0,F(1))]+[(d,t,n,-amount) for d,t,n,amount in k_terms]
    terms += [(d+e,t+u,n+m,amount*amount2/2) for d,t,n,amount in k_terms for e,u,m,amount2 in k_terms]
    for d in range(9):
        phi=((-1)**d*math.comb(7,d) if d<=7 else 0)+(7*(-1)**(d-1)*math.comb(7,d-1) if d>=1 else 0)
        for linear in range(9-d):
            value=phi*minb**d*math.comb(8-d,linear)*h**(8-d-linear)*c**linear
            for kd,shift,n,amount in terms:
                beta_integrals[d+kd] += value*amount*b.beta_integral(d+linear+shift,n)
                for j in range(n+1):alternate[d+kd][d+linear+shift+j] += value*amount*(-1)**j*math.comb(n,j)
    integrals=[b.integral(row) for row in matrix]
    b.require(matrix==alternate and integrals==beta_integrals, 'whole thirteen-by-nineteen joint matrix and all integrals')
    controls=bernstein_controls(integrals,low,high,12)
    maximum=max(controls['controls'])
    b.require(maximum<F(599,600), 'strict joint-polar face surplus')
    return dict(budgets=v,d_interval=[low,high],full_thirteen_by_nineteen_matrix=matrix,all_thirteen_integrals=integrals,bernstein=controls,upper=maximum,strict_polar_margin=F(599,600)-maximum)

def multiplicity_terms(polynomial,degree):
    items=list(polynomial.items())
    terms=[]
    def choices(position,remaining,counts):
        if position==len(items)-1:
            counts=counts+[remaining]
            u,t,coefficient=0,0,F(math.factorial(degree))
            for ((du,dt),value),count in zip(items,counts):
                u+=du*count;t+=dt*count
                coefficient*=value**count/math.factorial(count)
            terms.append((u,t,coefficient))
        else:
            for count in range(remaining+1):choices(position+1,remaining-count,counts+[count])
    choices(0,degree,[])
    return terms

def retained_mean_family(box,t_interval,constants,family):
    a,h,el,eh,ul,uh,wl,wh=box
    tl,tu=t_interval
    anchor=min(a,2*ul/(ul**2+wh)-h,2*uh/(uh**2+wh)-h)
    b.require(0<anchor<=a<=h and 2*ul>=(anchor+h)*(ul**2+wh) and 2*uh>=(anchor+h)*(uh**2+wh), 'BOTH mean-anchor endpoint gates')
    b.require(1-anchor*uh>0, 'positive whole-u square-root denominator')
    beta={(0,0):F(1),(1,1):-2*anchor,(2,2):anchor**2,(0,2):anchor**2*wh}
    root={(0,0):F(1),(1,1):-anchor,(0,2):anchor**2*wh/(2*(1-anchor*uh))}
    beta1=[1+anchor**2*wh,-2*anchor,anchor**2]
    beta_low=sum(beta1[k]*ul**k for k in range(3))
    beta_high=sum(beta1[k]*uh**k for k in range(3))
    b.require(0<beta_high<=beta_low<1, 'whole-u positive decreasing endpoint beta')
    dmean=b.root_grid(min(F(1),uh**2+wh),4096,True)
    dbeta=b.root_grid(beta_low,4096,True)
    b.require(1-dbeta*beta_low**4>0 and dmean>0, 'positive retained-mean diagonal and ACTUAL norm')
    if family=='E':
        energy={(0,0):eh-8-8*wl,(1,0):F(16),(2,0):F(-8)}
        minimum=eh-8*((1-ul)**2+wl)
        maximum=eh-8*((1-uh)**2+wl)
    elif family=='T':
        energy={(0,0):tu+8-8*wl,(2,0):F(-8)}
        minimum=tu+8-8*(uh**2+wl)
        maximum=tu+8-8*(ul**2+wl)
    else:raise ValueError('mean-family schema')
    b.require(0<=minimum<=maximum, 'whole-u chosen centered-energy envelope')
    denergy=b.root_grid(maximum,4096,True)
    remainder_matrices=[]
    total={}
    total_integral=[F(0)]*9
    for k in range(2,9):
        beta_degree=(8-k)//2 if k%2==0 else (7-k)//2
        factor=9*h**k*constants[k]*(denergy if k%2 else 1)
        polynomial=sparse_multiply(sparse_power(energy,k//2),sparse_power(beta,beta_degree))
        if k%2:polynomial=sparse_multiply(polynomial,root)
        polynomial={(u,t+k):value*factor for (u,t),value in polynomial.items()}
        b.require(all(u<=8 and t<=9 for u,t in polynomial), 'mean remainder bidegree')
        matrix=[[polynomial.get((u,t),F(0)) for t in range(10)] for u in range(9)]
        alternative=[[F(0)]*10 for _ in range(9)]
        direct_integral=[F(0)]*9
        # Complete uncoalesced multiplicity choices, separate from convolution.
        for eu,et,ev in multiplicity_terms(energy,k//2):
            for bu,bt,bv in multiplicity_terms(beta,beta_degree):
                for ru,rt,rv in (list((u,t,v) for (u,t),v in root.items()) if k%2 else [(0,0,F(1))]):
                    u,t=eu+bu+ru,et+bt+rt+k
                    value=factor*ev*bv*rv
                    alternative[u][t]+=value
                    direct_integral[u]+=value/(t+1)
        integrals=[b.integral(row) for row in matrix]
        b.require(matrix==alternative and integrals==direct_integral, 'ALL ninety mean remainder coefficients and all nine integrals')
        remainder_matrices.append(dict(order=k,full_nine_by_ten_matrix=matrix,all_nine_integrals=integrals))
        total=sparse_add(total,polynomial)
        total_integral=b.add(total_integral,integrals)
    numerator=b.add([F(1)],b.scale(b.power(beta1,4),-dbeta))
    numerator_other=b.add([F(1)],b.scale(trinomial_power(beta1,4),-dbeta))
    b.require(numerator==numerator_other and len(numerator)==9, 'whole retained diagonal numerator')
    bounded_diagonal=b.scale(numerator,1/(h*dmean))
    degree_eight=b.add(bounded_diagonal,b.scale(total_integral,-1))
    eight_controls=bernstein_controls(degree_eight,ul,uh,8)
    eight_lower=min(eight_controls['controls'])
    denominator=[h*wh/(2*ul),h]
    denominator_low=denominator[0]+h*ul
    denominator_high=denominator[0]+h*uh
    b.require(0<denominator_low<=denominator_high, 'positive whole-u linear ACTUAL-norm denominator')
    cleared=sparse_multiply({(0,0):denominator[0],(1,0):h},total)
    matrix=[[cleared.get((u,t),F(0)) for t in range(10)] for u in range(10)]
    alternate=[[F(0)]*10 for _ in range(10)]
    for u in range(9):
        for t in range(10):
            value=total.get((u,t),F(0))
            alternate[u][t]+=denominator[0]*value
            alternate[u+1][t]+=h*value
    b.require(matrix==alternate, 'ALL one hundred cleared mean coefficients')
    integrals=[b.integral(row) for row in matrix]
    cleared_numerator=b.add(numerator,b.scale(denominator,-1),b.scale(integrals,-1))
    direct_numerator=b.add(numerator,b.scale(b.multiply(denominator,b.add([F(1)],total_integral)),-1))
    b.require(cleared_numerator==direct_numerator and len(cleared_numerator)==10, 'whole ten cleared numerator coefficients and integral bridge')
    ten_controls=bernstein_controls(cleared_numerator,ul,uh,9)
    pmin=min(ten_controls['controls'])
    endpoint=denominator_high if pmin>=0 else denominator_low
    ten_lower=1+pmin/endpoint
    lower=max(eight_lower,ten_lower)
    return dict(family=family,anchor=anchor,actual_mean_squared_cap=min(F(1),uh**2+wh),actual_mean_sqrt_ceiling=dmean,beta_at_low=beta_low,beta_sqrt_ceiling=dbeta,whole_centered_energy_polynomial=[[u,t,v] for (u,t),v in energy.items()],whole_energy_interval=[minimum,maximum],energy_sqrt_ceiling=denergy,all_seven_remainder_matrices=remainder_matrices,all_nine_remainder_integrals=total_integral,full_nine_numerator_coefficients=numerator,nine_controls=eight_controls,degree_eight_lower=eight_lower,positive_linear_denominator=denominator,denominator_interval=[denominator_low,denominator_high],full_ten_by_ten_cleared_matrix=matrix,full_ten_cleared_numerator_coefficients=cleared_numerator,ten_controls=ten_controls,minimum_cleared_control=pmin,sign_dependent_endpoint=endpoint,degree_nine_lower=ten_lower,whole_u_lower=lower)

def refinement(polar_upper):
    epsilon=F(1,340)
    floor=F(40,67)
    sigma=(8+epsilon-floor)/7
    jc=b.binomial_linear(F(27,40),F(5,9)*sigma,7)
    lj=F(5,9)*b.integral(jc,1)
    a,d=F(27,40),F(5,9)*sigma
    endpoint=F(5,9)/d**2*((a+d)**9/9-a*(a+d)**8/8-a**9/9+a*a**8/8)
    b.require(lj==endpoint and lj<F(7,12), 'new entire polar derivative')
    radius=8+epsilon-7*floor
    lower_mean=F(57,80)-epsilon/8
    upper_energy=F(23,5)+2*(radius+1)*epsilon
    coupled=upper_energy+16*lower_mean-8
    b.require(coupled==8+2*radius*epsilon, 'new coupled mean-energy compensation')
    coeff=[F(8,7),-F(16,7)*F(2,3)*lower_mean,F(27,40)**2*coupled/7]
    b.require(coeff[2]>0 and coeff[1]+2*coeff[2]<0 and sum(coeff)>0 and F(107,100)**2>coeff[0], 'new whole positive decreasing B')
    cube=b.power(coeff,3)
    b.require(cube==trinomial_power(coeff,3), 'new entire signed cubic')
    lo=9*F(27,40)*F(107,100)*b.integral(cube,1)
    b.require(lo<F(6,5), 'new origin-gradient bound')
    ratio=b.binomial_linear(F(1),epsilon/(8*floor),8)
    b.require(ratio==b.power([F(1),epsilon/(8*floor)],8), 'new entire eight-factor product ratio')
    loss=sum(ratio)-1+F(6,5)*epsilon
    b.require(loss<F(1,100) and 1-lj*epsilon>F(49,50), 'new strict origin loss/entry')
    b.require(1-lj*epsilon>polar_upper, 'new strict loss against ALL independently paid polar leaves')
    return dict(epsilon=epsilon,polar_leaf_maximum=polar_upper,all_eight_polar_derivative_coefficients=jc,polar_derivative=lj,polar_loss=lj*epsilon,polar_strict_margin=1-lj*epsilon-polar_upper,radius_cap=radius,mean_lower=lower_mean,energy_upper=upper_energy,B_coefficients=coeff,all_seven_cubic_coefficients=cube,origin_derivative=lo,all_nine_ratio_coefficients=ratio,origin_loss=loss,origin_strict_margin=F(1,100)-loss,scope='SAME closed2/3..27/40 annulus, parentF<=8 exclusion explicit; no global first-power result/optimal gap. Independent sufficient strengthening1/340.')

def semantic_controls():
    result=[]
    def reject(label,operation,reason):
        try:operation()
        except ValueError as error:
            b.require(reason in str(error), 'control rejected for intended reason')
            result.append(dict(case=label,rejection=reason))
            return
        raise ValueError('control accepted: '+label)
    reject('lost_highest_Bernstein_coefficient',lambda:bernstein_controls([F(1),F(0)],0,1,2),'degree')
    reject('reversed_Bernstein_interval',lambda:bernstein_controls([F(1),F(0),F(0)],F(1),F(0),2),'domain')
    interior=bernstein_controls([F(1),F(-4),F(4)],F(0),F(1),2)
    b.require(interior['controls']==[F(1),F(-1),F(1)], 'known interior Bernstein control')
    reject('endpoint_only_lower_bound',lambda:b.require(sum([F(1),F(-4,2),F(4,4)])>=1,'interior point below endpoint-only bound'),'endpoint-only')
    reject('negative_control_divided_by_high_endpoint',lambda:b.require(1-F(1,2)<=1-F(1),'negative control wrong denominator'),'wrong denominator')
    reject('beta_coefficient_as_ACTUAL_norm',lambda:b.require(F(7,10)**2>=F(1),'q_j=1 formal mass8 has ACTUAL squared mean1'),'ACTUAL')
    reject('floating_zero_in_exact_record',lambda:plain({'math_zero':0.0}),'floating')
    return result

def plain(value):
    if isinstance(value,float):raise ValueError('floating arithmetic in exact mathematical record')
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [plain(v) for v in value]
    return value

def main():
    raw=(HERE/'COVER.json').read_bytes()
    b.require(hashlib.sha256(raw).hexdigest()==COVER_PIN, 'defining cover before parse')
    cover=b.decode_cover(raw)
    cells,coverage=b.cover_cells(cover)
    constants,derivation=centered_constants()
    controls=quartic_controls()
    completed=[]
    for cell in cells:
        rounds,interval=b.tighten_mass_eight(cell['raw_box'])
        box=rounds[-1]
        payment=scalar_origin(box,interval,constants)
        product=b.product_cap(box,interval)
        margin=payment['origin_lower']-product['product_upper_bound']
        if cell['role']=='scalar-product-origin':
            b.require(margin>F(1,100), 'strict original scalar-origin face surplus')
        row=dict(path=cell['path'],role=cell['role'],tight_box=box,t_interval=interval,scalar_origin=payment,product=product,scalar_product_surplus=margin)
        if cell['role'] in ('standard-polar','joint-energy-polar'):
            row['standard_polar']=standard_polar(box,interval)
            if cell['role']=='standard-polar':b.require(row['standard_polar']['upper']<F(599,600), 'strict standard-polar face surplus')
            else:row['joint_polar']=joint_polar(box,interval)
        if cell['role']=='retained-mean-product-origin':
            row['retained_mean']=[retained_mean_family(box,interval,constants,family) for family in ('E','T')]
            row['mean_product_surplus']=max(v['whole_u_lower'] for v in row['retained_mean'])-product['product_upper_bound']
            b.require(row['mean_product_surplus']>F(1,100), 'strict retained-mean original face surplus')
        completed.append(row)
    b.require(hashlib.sha256((HERE/'base.py').read_bytes()).hexdigest()==BASE_PIN and (HERE/'COVER.json').read_bytes()==raw, 'entire input stable')
    maximum_polar=max(v['joint_polar']['upper'] if v['role']=='joint-energy-polar' else v['standard_polar']['upper'] for v in completed if v['role'] in ('joint-energy-polar','standard-polar'))
    out=dict(agent='six-reviewer-5',role='independent reviewer',status='Complete exact original mass-eight face arithmetic plus independent1/340 sufficient gap',scope='ALL139 defining face leaves paid:79 scalar-origin,9 BOTH retained-mean families,2 standard-polar,49 joint-polar. SAME closed marked annulus and explicit parent exclusion. No original polynomial converse, whole-disk/global first-power result or formalization.',centered_derivation=derivation,quartic_formal_controls=controls,coverage=coverage,all_leaf_attempts=completed,strict_scalar_origin_leaves=79,strict_retained_mean_leaves=9,strict_standard_polar_leaves=2,strict_joint_polar_leaves=49,scalar_minimum_surplus=min(v['scalar_product_surplus'] for v in completed if v['role']=='scalar-product-origin'),joint_minimum_surplus=min(v['joint_polar']['strict_polar_margin'] for v in completed if v['role']=='joint-energy-polar'),mean_minimum_surplus=min(v['mean_product_surplus'] for v in completed if v['role']=='retained-mean-product-origin'),refinement=refinement(maximum_polar),semantic_controls=semantic_controls())
    print(json.dumps(plain(out),sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
