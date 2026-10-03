"""Exact independent algebra for the moving-budget audit.

Direct simple-root perturbation, literal eight-coordinate moment sums,
and invariant expansion of the original quadratic correction cost.
No producer executable, fixture, certificate or expected record is read.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import C, F, Z, Poly, need


def constants():
    c = C
    y = 1/(3*(1+c))
    x = F(Q(2,3))-y
    H,U0 = 14*y,-8*x
    k,rho = -7*(1+2*c)/18,(c-5)/3
    alpha = F(Q(-527,360))+41*c/90+13*c*c/90
    tau = (k+rho)**2/2
    B = F(Q(2311,108))+4934*c/27-1976*c*c/9
    E = F(Q(6653,324))+23915*c/486-15839*c*c/243
    K1 = B-alpha*H*H/2
    K0 = K1-(U0+rho*H)**2/16
    return dict(c=c,y=y,x=x,H=H,U0=U0,k=k,rho=rho,alpha=alpha,tau=tau,
                Bstar=B,KE=E,K1=K1,K0=K0,sigma=alpha+rho*rho/2,
                gamma=tau+5*alpha/9,kappa=tau+10*alpha/27,
                q2=(8+25*c+20*c*c)/162,C=F(Q(8,3))+y)


def eval_z(polynomial, value):
    return sum((Z(coefficient)*value**exponent for exponent,coefficient in polynomial.items()),Z(0))


def derivative_z(polynomial):
    return {n-1:a*n for n,a in polynomial.items() if n}


def shifted(n, coefficient):
    return {n:F(coefficient),0:-F(coefficient)}


def add_dict(*polynomials):
    out = {}
    for p in polynomials:
        for k,v in p.items():
            out[k] = out.get(k,F(0))+v
    return out


def root_normals(K, damage=None):
    """Solve the actual coefficient equation at every ninth-root label.

    For p=z^9-1+eta*f+eta^2*g, solve first and second displacements
    directly, then form the coefficient of half the squared modulus.
    Five original g4 coefficient directions are retained separately.
    """
    c,x,y,H,U0 = (K[n] for n in ('c','x','y','H','U0'))
    omega = Z(2*c*c-1,2*c)
    need(omega**9==1 and omega!=1,'Ninth-root realization')
    f = add_dict({0:F(9)},shifted(8,9*x),shifted(7,9*y))
    g = dict(
        base=add_dict({0:-36-9*U0+9*H/2},shifted(7,9*U0*U0/14),
                      shifted(6,-3*U0*H/4),shifted(5,9*H*H/40)),
        W=shifted(8,Q(-9,8)),T=shifted(7,Q(-9,14)),
        J21=shifted(6,Q(3,2)),J4=shifted(5,Q(-9,20)))
    if damage=='wrong_root_second_coefficient':
        curvature = 35
    else:
        curvature = 36
    rows = []
    for j in (3,4):
        w = omega**j
        first = -eval_z(f,w)/(9*w**8)
        values = {}
        for label,poly in g.items():
            correction = eval_z(poly,w)
            if label=='base':
                correction = correction+curvature*w**7*first*first+eval_z(derivative_z(f),w)*first
            second = -correction/(9*w**8)
            values[label] = (second/w).r+(first.norm()/2 if label=='base' else F(0))
        need((first/w).r==0,'Active first radial coefficient does not vanish')
        A,B = 1-w.r,1-(w*w).r
        need(values['W']==-A/8 and values['T']==-B/14,'Actual active linear rows')
        need(values['J21']==(1-(w**6).r)/6,'Actual mixed-moment normal')
        need(values['J4']==-(1-(w**5).r)/20,'Actual fourth-moment normal')
        rows.append(dict(j=j,first=first.serial(),coefficients={n:a.serial()for n,a in values.items()}))
    d = 2*c*c-1
    w4 = 1/(c+d)
    w3 = (F(7)-(1-d)/(c+d))*Q(2,3)
    need(w3.sign()>0 and w4.sign()>0,'Positive original dual weights')
    weighted = {}
    for label in g:
        weighted[label] = sum((F(row['coefficients'][label])*weight for row,weight in zip(rows,(w3,w4))),F(0))
    need(weighted['W']==-1 and weighted['T']==F(Q(-1,2)),'Both exact dual rows')
    need(weighted['base']+8+2*U0-3*H/2==K['K0'],'Direct curvature constant')
    need(weighted['J21']-F(Q(3,2))==K['rho'],'Direct original mixed-cost coefficient')
    need(weighted['J4']+F(Q(3,8))==K['sigma'],'Direct fourth-cost coefficient')
    sine_rows = []
    for j in (3,4):
        row = ((omega**j).t/8,(omega**(2*j)).t/14,(omega**(6*j)).t/18)
        need(row[0]*8*K['k']/7+row[1]*2*K['k']+row[2]==0,'Unaveraged signed cubic constraint')
        sine_rows.append(row)
    determinant = sine_rows[0][0]*sine_rows[1][1]-sine_rows[1][0]*sine_rows[0][1]
    need(determinant!=0,'Independent unaveraged pair rows')
    motion = []
    for j in range(9):
        w = omega**j
        T = w*(3+4*c)-(1+w**(-1))*(1+2*c)-w**(-2)
        norm = T.norm()/324
        gap = K['q2']-norm
        need(gap==0 if j in(2,7) else gap.sign()>0,'Every original motion norm/winning label')
        motion.append(dict(j=j,complex_bracket=T.serial(),squared_norm=norm.serial(),gap=gap.serial()))
    return dict(active_normals=rows,weights=[w3.serial(),w4.serial()],
                weighted_normal={n:a.serial()for n,a in weighted.items()},
                signed_pair_rows=[[a.serial()for a in row]for row in sine_rows],
                signed_pair_determinant=determinant.serial(),all9_motion=motion)


def projection(K, damage=None):
    # Invariants of ORIGINAL eight-coordinate vectors; the derivation of
    # the norm expansion in PROOF.md is valid without constraints.
    S,V2,V3,V4,U,U2,T1,T2 = (Poly.var(8,j) for j in range(8))
    H,rho,k = (K[n]for n in ('H','rho','k'))
    s0 = (K['U0']+rho*H)/8
    b = V3*(k+rho)/H
    B = Poly.const(8,K['K0'])+U2/2+T2*rho+V4*K['sigma']
    cost = Poly.const(8,K['K1'])+V4*K['alpha']+V3**2*K['tau']/H
    norm = U2-U*(2*s0)-T1*2*b+T2*(2*rho)+8*s0*s0+S*(2*s0)*b-V2*(2*s0*rho)+V2*b*b-V3*2*b*rho+V4*rho*rho
    signed = b*(T1-V3*k)
    if damage=='wrong_projection_mixed_sign':
        signed = -signed
    defect = B-cost-norm/2-signed
    expected = (U-K['U0']+(V2-H)*rho)*s0-S*s0*b-(V2-H)*b*b/2
    need(defect.same(expected),'Whole unconstrained invariant polynomial defect')
    return dict(invariants=['sumv','sumv2','sumv3','sumv4','sumu','sumu2','sumvu','sumv2u'],
                original_cost=B.serial(),least_cost=cost.serial(),original_squared_residual=norm.serial(),
                signed_error=signed.serial(),whole_unconstrained_defect=defect.serial())


def moment_and_curve(K, damage=None):
    H,alpha,tau = K['H'],K['alpha'],K['tau']
    m = Poly.var(2,0)
    r = Poly.var(2,1)
    vectors = [m]*6+[-3*m+r,-3*m-r]
    def reduce_r(poly):
        result = Poly.const(2,0)
        replacement = Poly.const(2,H/2)-12*m*m
        for (a,b),value in poly.d.items():
            result = result+(m**a)*(r**(b%2))*(replacement**(b//2))*value
        return result
    powers = {j:reduce_r(sum((v**j for v in vectors),Poly.const(2,0)))for j in (1,2,3,4)}
    need(powers[1].same(0)and powers[2].same(H),'Literal eight-profile balance/norm')
    need(powers[3].same(168*m**3-9*H*m),'Literal eight-profile cubic')
    need(powers[4].same(H*H/2+30*H*m*m-840*m**4),'Literal eight-profile quartic')
    z = Poly.var(1,0)
    G = z*(9-168*z)**2
    Q4 = Poly.const(1,Q(1,2))+30*z-840*z*z
    P = (Q4-Q(1,2))*alpha+G*tau
    expected = z*(30*alpha+81*tau)+z*z*(-840*alpha-3024*tau)+z**3*(28224*tau)
    need(P.same(expected),'Entire least-cost curve from literal moments')
    gamma = K['gamma']+(F(Q(1,100))if damage=='too_large_lower_secant'else F(0))
    low_defect = P.derivative()-G.derivative()*gamma
    high_defect = G.derivative()*K['kappa']-P.derivative()
    need(low_defect.same((1-56*z)**2*(-15*alpha)),'Complete lower secant identity')
    need(high_defect.same(z*(1-56*z)*(-560*alpha)),'Complete upper secant identity')
    need(P.derivative().same((1-56*z)*(30*alpha+81*tau-1512*tau*z)),'Cost derivative endpoints')
    comparison = Q4-Q(1,8)-G
    need(comparison.same((1-56*z)**2*(Q(3,8)-9*z)),'All singular two-value cases comparison')
    if damage=='wrong_endpoint':
        e = Q(1,55)
    else:
        e = Q(1,56)
    need(G.evaluate([e])==F(Q(9,14)),'Merged cubic endpoint')
    need(K['Bstar']+H*H*P.evaluate([e])==K['KE'],'Entire cost endpoint')
    need(P.evaluate([0])==0 and P.derivative().evaluate([0])==81*K['kappa'],'Small-budget coefficient')
    # A=8? Seven complete two-value multiplicities, and ALL ordered triples.
    two = []
    for n in range(1,8):
        t = Q((8-2*n)**2,8*n*(8-n))
        need(t<=Q(9,14),'Complete cubic maximum multiplicities')
        two.append(dict(multiplicity=n,squared_skewness=str(t),normalized_fourth=str(Q(1,8)+t)))
    three = []
    for a in range(1,7):
        for b in range(1,8-a):
            d = 8-a-b
            three.append(dict(counts=[a,b,d],excluded_outer_repetition=a>1 or d>1))
    need(len(three)==21 and [r['counts']for r in three if not r['excluded_outer_repetition']]==[[1,6,1]],'Every three-count case')
    # Strict concavity in cubic-square: ratio is tau+10alpha/(27-504z).
    denominator = 81-1512*z
    ratio_numerator = Poly.const(1,30*alpha+81*tau)-z*(1512*tau)
    curvature_numerator = ratio_numerator.derivative()*denominator-ratio_numerator*denominator.derivative()
    need(curvature_numerator.same(45360*alpha),'Strict cost-vs-cubic-square concavity numerator')
    need(denominator.evaluate([0]).sign()>0 and denominator.evaluate([e]).sign()>0,'Nonzero canceled endpoint denominator')
    need(ratio_numerator.evaluate([0])/denominator.evaluate([0])==K['kappa'],'Optimal upper secant endpoint slope')
    need(ratio_numerator.evaluate([e])/denominator.evaluate([e])==K['gamma'],'Optimal lower secant endpoint slope')
    return dict(literal_eight_moments={str(j):p.serial()for j,p in powers.items()},
                cubic_square=G.serial(),quartic_frontier=Q4.serial(),least_cost_curve=P.serial(),
                lower_secant_defect=low_defect.serial(),upper_secant_defect=high_defect.serial(),
                singular_case_gap=comparison.serial(),endpoint=str(e),
                complete_two_value_cases=two,complete_three_value_cases=three,
                concavity_ratio_numerator=ratio_numerator.serial(),concavity_ratio_denominator=denominator.serial(),
                curvature_numerator=curvature_numerator.serial())


def first_power(K, damage=None):
    u,h2 = Poly.var(2,0),Poly.var(2,1)
    A,B = h2-2-2*u,(1+u)**2
    second = A*A*Q(3,8)-B/2
    expected = h2*h2*Q(3,8)-h2*(1+u)*Q(3,2)+(1+u)**2
    if damage=='wrong_reciprocal_power':
        second = A*A-B
    need(second.same(expected),'Actual reciprocal FIRST-power scalar coefficients')
    need(8+K['U0']-K['H']/2==K['C'],'Actual first boundary slope')
    return dict(squared_distance_first=A.serial(),squared_distance_second=B.serial(),
                reciprocal_first=(-A/2).serial(),reciprocal_second=second.serial())


def anchored_newton(K, damage=None):
    eta,W,T,J21,J4,z = (Poly.var(6,j)for j in range(6))
    def retained(p):
        return Poly(6,{powers:value for powers,value in p.d.items()if powers[0]<=2})
    powers = [None,eta*K['U0']+eta**2*W,-eta*K['H']+eta**2*T,
              -3*eta**2*J21,eta**2*J4]
    elementary = [Poly.const(6,1)]
    for n in range(1,5):
        value = sum((elementary[n-j]*powers[j]*((-1)**(j-1))for j in range(1,n+1)),Poly.const(6,0))/n
        elementary.append(retained(value))
    anchor = 1-(2 if damage=='wrong_actual_anchor'else 1)*eta
    literal = z**9-anchor**9
    for j in range(1,5):
        literal = literal+elementary[j]*(z**(9-j)-anchor**(9-j))*Q(9*((-1)**j),9-j)
    literal = retained(literal)
    H,U0 = K['H'],K['U0']
    f = 9+(z**8-1)*(9*K['x'])+(z**7-1)*(9*K['y'])
    g = -36-9*U0+9*H/2-(z**8-1)*W*Q(9,8)+(z**7-1)*(U0*U0-T)*Q(9,14)
    g = g+(z**6-1)*(-3*U0*H/4+J21*Q(3,2))+(z**5-1)*(9*H*H/40-J4*Q(9,20))
    need(literal.same(z**9-1+eta*f+eta**2*g),'Entire anchored real Newton map through second order')
    return dict(variables=['eta','W','T','J21','J4','original_z'],
                elementary_real_retained=[p.serial()for p in elementary[1:]],
                full_anchored_retained_polynomial=literal.serial())


def run(damage=None):
    K = constants()
    lo,hi = Q(15,16),Q(47,50)
    need(8*lo**3-6*lo-1<0<8*hi**3-6*hi-1,'Physical root bracket')
    need(all(8*r**3-6*r-1!=0 for q in (1,2,4,8)for r in (Q(1,q),Q(-1,q))),'Irreducible cubic rational-root test')
    signs = {}
    for name,value in dict(alpha_negative=-K['alpha'],alpha_gt_minus_one=K['alpha']+1,
                           tau_gt_three=K['tau']-3,gamma=K['gamma'],kappa=K['kappa'],
                           kappa_minus_gamma=K['kappa']-K['gamma'],H=K['H'],q2=K['q2'],
                           Bstar_negative=-K['Bstar'],KE_gt9=K['KE']-9,KE_lt10=10-K['KE']).items():
        need(value.sign()>0,'Physical embedding bound '+name)
        signs[name] = value.serial()
    return dict(schema='six-reviewer-4-independent-moving-budget-v1',
                constants={n:v.serial()for n,v in K.items()},embedding_signs=signs,
                direct_original_root_and_motion=root_normals(K,damage),
                complete_unconstrained_projection=projection(K,damage),
                literal_moments_and_secants=moment_and_curve(K,damage),
                original_first_power=first_power(K,damage),
                entire_anchored_real_Newton_map=anchored_newton(K,damage))


if __name__=='__main__':
    import json
    import sys
    damage = sys.argv[1] if len(sys.argv)>1 else None
    print(json.dumps(run(damage),sort_keys=True,separators=(',',':')))
