#!/usr/bin/env python3
"""Independent exact algebra for claim8530 and a smaller cubic correction.

six-reviewer-3, independent reviewer. No author imports or floating arithmetic.
The written review supplies the analytic uniformity and converse bridges.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, label):
    if not ok:
        raise ValueError(label)


class Cyclo:
    """Q[w]/(w^6+w^3+1), w=exp(2pi i/9), a different field presentation."""
    def __init__(self, a=0):
        if isinstance(a, Cyclo):
            self.a = a.a
        elif isinstance(a,(tuple,list)):
            require(len(a)==6,'six cyclotomic coordinates')
            self.a = tuple(map(F,a))
        else:
            self.a = (F(a),)+(F(0),)*5

    def __add__(self,b):
        return Cyclo(tuple(x+y for x,y in zip(self.a,Cyclo(b).a)))
    __radd__ = __add__
    def __neg__(self):
        return Cyclo(tuple(-x for x in self.a))
    def __sub__(self,b):
        return self+-Cyclo(b)
    def __rsub__(self,b):
        return Cyclo(b)+-self
    def __mul__(self,b):
        B = Cyclo(b).a
        v = [F(0)]*11
        for i,x in enumerate(self.a):
            for j,y in enumerate(B):
                v[i+j] += x*y
        for i in range(10,5,-1):
            v[i-3] -= v[i]
            v[i-6] -= v[i]
        return Cyclo(v[:6])
    __rmul__ = __mul__
    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'nonnegative exponent')
        answer = Cyclo(1)
        for _ in range(n):
            answer *= self
        return answer
    def inverse(self):
        columns = [(self*Cyclo(tuple(int(i==j) for i in range(6)))).a for j in range(6)]
        A = [[columns[j][i] for j in range(6)]+[F(i==0)] for i in range(6)]
        for j in range(6):
            row = next((i for i in range(j,6) if A[i][j]),None)
            require(row is not None,'field inverse exists')
            A[j],A[row] = A[row],A[j]
            pivot = A[j][j]
            A[j] = [x/pivot for x in A[j]]
            for i in range(6):
                if i!=j:
                    factor = A[i][j]
                    A[i] = [x-factor*y for x,y in zip(A[i],A[j])]
        answer = Cyclo([A[i][-1] for i in range(6)])
        require(self*answer==1,'checked inverse identity')
        return answer
    def __truediv__(self,b):
        return self*Cyclo(b).inverse()
    def __rtruediv__(self,b):
        return Cyclo(b)*self.inverse()
    def __eq__(self,b):
        return self.a==Cyclo(b).a
    def conjugate(self):
        w = Cyclo((0,1,0,0,0,0))
        return sum((x*w**((-i)%9) for i,x in enumerate(self.a)),Cyclo())
    def real(self):
        return (self+self.conjugate())/2
    def record(self):
        return list(map(str,self.a))


def real_coordinates(value,c):
    """Recover coefficients in 1,c,c^2 from six cyclotomic coordinates."""
    basis = [Cyclo(1),c,c*c]
    A = [[basis[j].a[i] for j in range(3)]+[value.a[i]] for i in range(6)]
    row = 0
    for j in range(3):
        pivot = next((i for i in range(row,6) if A[i][j]),None)
        require(pivot is not None,'real subfield basis rank')
        A[row],A[pivot] = A[pivot],A[row]
        factor = A[row][j]
        A[row] = [x/factor for x in A[row]]
        for i in range(6):
            if i!=row:
                factor = A[i][j]
                A[i] = [x-factor*y for x,y in zip(A[i],A[row])]
        row += 1
    require(all(not A[i][3] for i in range(3,6)),'value in real subfield')
    coefficients = [A[i][3] for i in range(3)]
    require(sum((a*b for a,b in zip(coefficients,basis)),Cyclo())==value,'real-coordinate reconstruction')
    return coefficients


def enclosure(value,c,lo,hi):
    coefficients = real_coordinates(value,c)
    lower = upper = coefficients[0]
    for i,a in enumerate(coefficients[1:],1):
        lower += min(a*lo**i,a*hi**i)
        upper += max(a*lo**i,a*hi**i)
    return lower,upper


def sign_c(t):
    return 8*t**3-6*t-1


def isolate():
    lo,hi = F(15,16),F(1)
    require(sign_c(lo)<0<sign_c(hi),'initial isolating endpoints')
    for _ in range(90):
        mid = (lo+hi)/2
        if sign_c(mid)<0:
            lo = mid
        else:
            hi = mid
    require(sign_c(lo)<0<sign_c(hi),'final exact isolation')
    return lo,hi


# Sparse Gaussian-rational polynomial; epsilon order is truncated at3.
# Independent variables: epsilon,z,x,tau,h1,...,h7; h8=-sum(h1,...,h7).
NVAR = 11
ZERO = (0,)*NVAR


def constant(re=0,im=0):
    return {} if re==im==0 else {ZERO:(F(re),F(im))}


def variable(j):
    exponent = [0]*NVAR
    exponent[j] = 1
    return {tuple(exponent):(F(1),F(0))}


def add(*terms):
    result = {}
    for polynomial in terms:
        for exponent,(a,b) in polynomial.items():
            u,v = result.get(exponent,(F(0),F(0)))
            if (a+u,b+v)==(0,0):
                result.pop(exponent,None)
            else:
                result[exponent] = (a+u,b+v)
    return result


def scale(polynomial,re=1,im=0):
    re,im = F(re),F(im)
    return {e:(a*re-b*im,a*im+b*re) for e,(a,b) in polynomial.items()
            if (a*re-b*im,a*im+b*re)!=(0,0)}


def multiply(*terms):
    result = constant(1)
    for polynomial in terms:
        output = {}
        for e,(a,b) in result.items():
            for f,(u,v) in polynomial.items():
                if e[0]+f[0]>3:
                    continue
                key = tuple(x+y for x,y in zip(e,f))
                old = output.get(key,(F(0),F(0)))
                output[key] = (old[0]+a*u-b*v,old[1]+a*v+b*u)
        result = {e:ab for e,ab in output.items() if ab!=(0,0)}
    return result


def power(polynomial,n):
    return multiply(*([polynomial]*n))


def integrate_z(polynomial):
    result = {}
    for e,(a,b) in polynomial.items():
        key = list(e)
        key[1] += 1
        result[tuple(key)] = (a/key[1],b/key[1])
    return result


def evaluate_z(polynomial,z):
    result = {}
    for e,ab in polynomial.items():
        key = list(e)
        key[1] = 0
        result = add(result,multiply({tuple(key):ab},power(z,e[1])))
    return result


def polynomial_record(polynomial):
    return [[list(e),str(a),str(b)] for e,(a,b) in sorted(polynomial.items())]


def sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def exact_jets():
    e,z,x,tau = [variable(j) for j in range(4)]
    h = [variable(j) for j in range(4,11)]
    h.append(scale(add(*h),-1))
    require(not add(*h),'full formal balance')
    p2,p3 = add(*(power(t,2) for t in h)),add(*(power(t,3) for t in h))
    elementary2 = add(*(multiply(h[i],h[j]) for i in range(8) for j in range(i+1,8)))
    elementary3 = add(*(multiply(h[i],h[j],h[k]) for i in range(8)
                       for j in range(i+1,8) for k in range(j+1,8)))
    require(elementary2==scale(p2,F(-1,2)),'balanced second Newton identity')
    require(elementary3==scale(p3,F(1,3)),'balanced third Newton identity')
    m = add(scale(multiply(x,power(e,2)),-1),multiply(tau,power(e,3)))
    factors = [add(z,scale(m,-1),scale(multiply(e,t),0,-1)) for t in h]
    derivative = scale(multiply(*factors),9)
    expected_derivative = add(scale(power(z,8),9),
        scale(multiply(power(e,2),x,power(z,7)),72),
        scale(multiply(power(e,2),p2,power(z,6)),F(9,2)),
        scale(multiply(power(e,3),tau,power(z,7)),-72),
        scale(multiply(power(e,3),p3,power(z,5)),0,3))
    require(derivative==expected_derivative,'generic full derivative jet through order3')
    primitive = integrate_z(derivative)
    a = add(constant(1),scale(power(e,2),-1))
    anchored = add(primitive,scale(evaluate_z(primitive,a),-1))
    expected_anchored = add(power(z,9),constant(-1),scale(power(e,2),9),
        scale(multiply(power(e,2),x,add(power(z,8),constant(-1))),9),
        scale(multiply(power(e,2),p2,add(power(z,7),constant(-1))),F(9,14)),
        scale(multiply(power(e,3),tau,add(power(z,8),constant(-1))),-9),
        scale(multiply(power(e,3),p3,add(power(z,6),constant(-1))),0,F(1,2)))
    require(anchored==expected_anchored,'generic anchored polynomial jet through order3')
    # Single critical-distance binomial expansion, with symbolic profile coordinate.
    dist = add(power(add(a,scale(m,-1)),2),multiply(power(e,2),power(h[0],2)))
    u = add(dist,constant(-1))
    reciprocal = add(constant(1),scale(u,F(-1,2)),scale(power(u,2),F(3,8)),scale(power(u,3),F(-5,16)))
    expected_reciprocal = add(constant(1),multiply(power(e,2),add(constant(1),scale(x,-1),scale(power(h[0],2),F(-1,2)))),multiply(tau,power(e,3)))
    require(reciprocal==expected_reciprocal,'single exact inverse-distance jet')
    require(multiply(power(reciprocal,2),dist)==constant(1),'independent reciprocal defining equation')
    # Generic converse inverse-distance expansion: zeta=e(X+iY), eta=e^2.
    X,Y = x,tau
    dist_converse = add(power(add(a,scale(multiply(e,X),-1)),2),multiply(power(e,2),power(Y,2)))
    u = add(dist_converse,constant(-1))
    inverse = add(constant(1),scale(u,F(-1,2)),scale(power(u,2),F(3,8)),scale(power(u,3),F(-5,16)))
    quadratic = add(constant(1),multiply(e,X),multiply(power(e,2),add(constant(1),power(X,2),scale(power(Y,2),F(-1,2)))))
    require(all(e[0]==3 for e in add(inverse,scale(quadratic,-1))),'generic converse quadratic jet')
    rejected = 0
    for correct,altered in [(derivative,add(expected_derivative,scale(multiply(power(e,3),p3,power(z,5)),0,-6))),
                            (anchored,add(expected_anchored,scale(multiply(power(e,3),tau,power(z,8)),1))),
                            (reciprocal,add(expected_reciprocal,multiply(tau,power(e,3))))]:
        require(correct!=altered,'damaged symbolic identity rejected')
        rejected += 1
    return {'derivative_terms':len(derivative),'anchored_terms':len(anchored),
            'derivative_sha256':sha(polynomial_record(derivative)),
            'anchored_sha256':sha(polynomial_record(anchored)),
            'inverse_sha256':sha(polynomial_record(reciprocal)),
            'symbolic_corruption_controls':rejected}


def build():
    w = Cyclo((0,1,0,0,0,0))
    require(w**9==1 and w**3!=1,'primitive ninth-root identities')
    c = -(w**4+w**5)/2
    d = (w+w**8)/2
    require(8*c**3-6*c-1==0 and d==2*c*c-1,'real-subfield trigonometry')
    y = 1/(3*(1+c))
    x,H,C = Cyclo(F(2,3))-y,14*y,Cyclo(F(8,3))+y
    w4 = 1/(c+d)
    w3 = F(2,3)*(7-(1-d)*w4)
    require(8-8*x-H/2==C==8-w3-w4,'primal and dual boundary constant')
    require(F(3,16)*w3+(1+c)*w4/8==1,'dual first moment')
    require(F(3,28)*w3+(1-d)*w4/14==F(1,2),'dual second moment')
    det = F(3,16)*(1-d)/14-F(3,28)*(1+c)/8
    require(det==-3*(c+d)/224 and det!=0,'converse constraint determinant')
    lo,hi = isolate()
    require(enclosure(w3,c,lo,hi)[0]>0 and enclosure(w4,c,lo,hi)[0]>0,'positive dual weights')
    radial = []
    for k in range(9):
        omega = w**k
        g2 = 9+9*x*(omega**8-1)+9*y*(omega**7-1)
        G2 = -g2.real()/9
        motion = -omega-x*(1-omega)-y*(omega**8-omega)
        require(motion==-omega/3-x-y*omega**8,'every limiting original-root motion')
        A,B = 1-omega.real(),1-(omega**2).real()
        require(G2==-1+x*A+y*B,'every second-order radial coefficient')
        # General tau coefficient in g3=-9tau(omega^8-1)+ip3(omega^6-1)/2.
        # p3 coefficient is (omega^6-omega^-6)/(36i); square is real.
        p3_radial_square = -(omega**6-(omega**6).conjugate())**2/1296
        if k in [3,4,5,6]:
            require(G2==0,'active radial pair')
        elif k!=0:
            require(enclosure(G2,c,lo,hi)[1]<0,'strict nonactive radial pair')
        if k in [3,6]:
            require(A==F(3,2) and p3_radial_square==0,'cube-root cubic tangency')
        if k in [4,5]:
            require(A==1+c and p3_radial_square==F(1,432),'outer active cubic tangency')
        radial.append({'k':k,'G2_real_basis':list(map(str,real_coordinates(G2,c))),
                       'G2_interval':list(map(str,enclosure(G2,c,lo,hi))),
                       'tau_radial_coefficient_real_basis':list(map(str,real_coordinates(-A,c))),
                       'p3_radial_coefficient_square':p3_radial_square.record()})
    require(enclosure(H,c,lo,hi)[1]<3,'profile compact norm bound')
    # Exact stationary candidate squares for the sharp balanced cubic moment.
    candidate_squares = {str(k):F((8-2*k)**2,8*k*(8-k)) for k in range(1,8)}
    require(max(candidate_squares.values())==F(9,14),'sharp cubic moment coefficient')
    require([k for k,v in candidate_squares.items() if v==F(9,14)]==['1','7'],'complete cubic equality multiplicities')
    # Threshold squared = (3H^(3/2)/sqrt14)^2 / (432(1+c)^2).
    threshold_squared = F(9,14)*H**3/(432*(1+c)**2)
    require(threshold_squared==F(49,324)/(1+c)**5,'sharp common correction threshold')
    tau = F(3,40)
    margin = tau*tau-threshold_squared
    require(enclosure(margin,c,lo,hi)[0]>0,'rational correction above sharp threshold')
    elementary_margin = 2916*31**5-78400*16**5
    require(elementary_margin>0 and sign_c(F(15,16))==F(-17,512),'short rational threshold proof')
    CL,CH = enclosure(C,c,lo,hi)
    require(F(2838515200687,10**12)<CL<CH<F(2838515200688,10**12),'exact descriptive C enclosure')
    threshold_lo,threshold_hi = enclosure(threshold_squared,c,lo,hi)
    tau_lo,tau_hi = F(0),F(1)
    for _ in range(80):
        mid = (tau_lo+tau_hi)/2
        if mid*mid<threshold_lo:
            tau_lo = mid
        elif mid*mid>threshold_hi:
            tau_hi = mid
        else:
            break
    require(tau_lo*tau_lo<threshold_lo<=threshold_hi<tau_hi*tau_hi,'certified threshold enclosure')
    return {'reviewer':'six-reviewer-3','role':'independent mathematical reviewer',
            'field':'Q[w]/(w^6+w^3+1); w=exp(2pi i/9), with real embedding c in (15/16,1)',
            'c_interval':[str(lo),str(hi)],'C_interval':[str(CL),str(CH)],
            'C_real_basis':list(map(str,real_coordinates(C,c))),
            'x_real_basis':list(map(str,real_coordinates(x,c))),
            'y_real_basis':list(map(str,real_coordinates(y,c))),
            'H_real_basis':list(map(str,real_coordinates(H,c))),
            'dual_weights_real_basis':[list(map(str,real_coordinates(v,c))) for v in (w3,w4)],
            'radial_constraints':radial,'stationary_cubic_moment_squares':{k:str(v) for k,v in candidate_squares.items()},
            'threshold_squared_real_basis':list(map(str,real_coordinates(threshold_squared,c))),
            'threshold_interval':[str(tau_lo),str(tau_hi)],'rational_correction':str(tau),
            'corrected_first_power_cubic_coefficient':str(8*tau),
            'threshold_square_margin_interval':list(map(str,enclosure(margin,c,lo,hi))),
            'elementary_integer_margin':elementary_margin,'formal_jets':exact_jets(),
            'trust_boundary':'Exact finite algebra only. Ordinary proofs supply concentration/bootstrap premises, uniform root/Taylor bridges, Lagrange multiplier completeness and all-root containment.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write-expected',action='store_true')
    args = p.parse_args()
    result = build()
    if args.write_expected:
        (HERE/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print('Exact independent record generated')
    else:
        require(result==json.loads((HERE/'expected.json').read_text()),'frozen full record match')
        print('PASS: nine exact radial constraints, converse dual identities, generic polynomial jets, sharp cubic moment and smaller correction')


if __name__=='__main__':
    main()
