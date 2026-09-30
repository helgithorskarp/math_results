"""Exact standalone check of the coalesced minimum coefficient bounds.

Arithmetic and Gaussian controls adapt the credited preceding collar
source. Whole-reference, quotient and optimality bounds are new here.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,comb
import importlib.util
import json,hashlib,time,resource

spec=importlib.util.spec_from_file_location('local_algebra',Path(__file__).with_name('algebra.py'))
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)

def need(condition,message):
    if not condition:raise ArithmeticError(message)

def gaussian_add(u,v):return (u[0]+v[0],u[1]+v[1])
def gaussian_mul(u,v):return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0])
def gaussian_scale(u,k):return (u[0]*k,u[1]*k)
def gaussian_norm(u):return u[0]**2+u[1]**2
def gaussian_power(u,n):
    z=(F(1),F(0))
    for _ in range(n):z=gaussian_mul(z,u)
    return z

def direct_integral(U,V,a):
    rows=[]
    for W in [U,V]:
        rows.append([gaussian_scale(gaussian_power(W,k),comb(4,k)*(-a)**k)
                     for k in range(5)])
    coefficients=[(F(0),F(0))]*9
    for j in range(5):
        for k in range(5):
            coefficients[j+k]=gaussian_add(coefficients[j+k],gaussian_mul(rows[0][j],rows[1][k]))
    z=(F(0),F(0))
    for k,row in enumerate(coefficients):z=gaussian_add(z,gaussian_scale(row,F(9,k+1)))
    return z

def derive():
    oldP,oldJ,Pk,Qk=A.norm_polynomials()
    p,q=A.alternate_integral_coefficients()
    need(p==Pk and q==Qk,'18 full direct-convolution component polynomials')
    E,J=A.alternate_norm(p,q)
    a,m,c,x,q=[A.variable(i) for i in range(5)]
    R=A.add(A.power(m,2),A.scale(q,-1));R8=A.power(R,8)
    need(A.add(E,A.scale(R8,-1))==oldP and J==oldJ,'2 whole norm identities')
    P=A.add(A.mul(A.power(a,2),E),A.scale(R8,-1))
    J=A.mul(A.power(a,2),J)
    cert,shifted,skew,pure,quotient=A.coefficient_certificate(P,J)
    inv=shifted;invJ=skew
    for axis in range(4):inv=A.shifted_axis(inv,axis);invJ=A.shifted_axis(invJ,axis)
    need(inv==P and invJ==J,'2 whole inverse affine substitutions')
    independent_pure=A.reference_polynomial()
    independent_pure=A.shifted_axis(A.shifted_axis(independent_pure,0),3)
    need(pure==independent_pure,'Whole coalesced Chebyshev identity')
    delta=A.variable(0);chi=A.variable(3)
    ref=A.diagonal(pure)
    need(A.add(A.mul(A.add(chi,A.scale(delta,-1)),quotient),ref)==pure,
         'Whole exact difference quotient')
    D=A.add(A.ONE,A.scale(A.power(a,2),-1))
    real=A.add(*(A.scale(A.mul(A.power(a,2*j),A.power(D,9-j)),(-1)**j*comb(9,2*j))
                 for j in range(5)))
    closed=A.add(A.scale(real,-2),A.power(D,9))
    need(A.shifted_axis(closed,0)==ref,'Whole geometric real-ninth-power reference')
    need(min(sum(e) for e in pure)==5 and min(sum(e) for e in quotient)==4,
         'No lower-order pure or quotient terms')
    pure5={e:v for e,v in pure.items() if sum(e)==5}
    need(pure5=={(1,0,0,4,0):F(-288),(0,0,0,5,0):F(-288)},'Full pure leading form')
    need(cert['leading_quotient']==['-576','-576','-576','-576','-288'],
         'Full decreasing quotient leading form')
    I=[F(9*comb(4,j)*(-1)**j*factorial(2*j)*factorial(8-2*j),factorial(9)) for j in range(5)]
    need(I==[F(1),F(-1,7),F(3,35),F(-1,7),F(1)],'Independent beta-integral boundary')
    base=[F(0)]*9
    for j in range(5):
        for k in range(5):base[j+k]+=I[j]*I[k]
    base=[v-F(comb(8,k)*(-1)**k) for k,v in enumerate(base)]
    need([str(v) for v in base]==cert['base_coefficients'],'Whole radial base polynomial')
    moment=lambda j,k:F(factorial(j)*factorial(k),factorial(j+k+1))
    first=[144*moment(1,7)-2,144*moment(1,7)+16,144*moment(1,6),F(0)]
    need([str(v) for v in first]==cert['first_variation'],'Independent integral first variations')
    need(F(333,140)*F(7,8)>2 and F(431,448)>F(7,8),'Uniform base inequality')
    b={k:F(v) for k,v in cert['bounds'].items()};eps=F(cert['epsilon'])
    caps={'Mq':700,'Me':150,'M_gamma':30,'Jmax':3,'S':85000,'M':190000,'T':800}
    for k,cap in caps.items():need(b[k]<cap,'Exact rounded bound '+k)
    need(2-700*eps-F(3,64)>=F(19,10),'Full q absorption')
    need(18-150*eps>=17,'Full e absorption')
    need(F(18,7)-30*eps-F(3,64)>=F(5,2),'Full gamma absorption')
    need(576-85000*eps>288,'Decreasing common-phase quotient')
    need(380000*eps**4/F(128)<F(1,8),'Phase excess absorption')
    need(12800*eps**5<F(1,8),'Reference denominator absorption')
    need(F(19,10)-F(1,4)>=F(3,2) and 17-F(1,4)>=16 and F(5,2)-F(1,4)>=2,
         'Coercive minimum penalty')
    need((1-eps)**2>F(1,2) and 1600*eps**3<1,'Strict origin margin')
    series=[]
    for k in range(6):
        # (1+Fref)/(1-delta)^2, using the full diagonal polynomial.
        value=F(k+1)+sum(v*(k-e[0]+1) for e,v in ref.items() if e[0]<=k)
        series.append(str(value))
    need(series==['1','2','3','4','5','-570'],'Sharp fifth-order minimum expansion')
    profiles=[(F(1),F(0)),(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(399,401),F(40,401))]
    controls=[]
    for index,(cv,dv) in enumerate(profiles):
        for h in [F(0),F(1,1000),F(-1,4)]:
            xv,yv=profiles[(index+1)%len(profiles)]
            if index%2:yv=-yv
            av=F(3,5);mv=F(7,8);w=(xv,yv)
            u=gaussian_mul(w,(cv,dv));v=gaussian_mul(w,(cv,-dv))
            U=gaussian_scale(u,mv+h);V=gaussian_scale(v,mv-h)
            actual=direct_integral(U,V,av)
            values=(av,mv,cv,xv,h*h);lam=-h*dv*yv
            predicted=A.evaluate(A.add(P,R8),values)+lam*A.evaluate(J,values)
            need(predicted==av*av*gaussian_norm(actual),'Direct rational signed-skew identity')
            controls.append([str(z) for z in [av,mv,h,cv,dv,xv,yv,*actual,predicted]])
    feasible=[]
    for k in [256,512]:
        av=F(k*k-1,k*k+1);yv=F(2*k,k*k+1)
        for sign in [-1,1]:feasible.append((av,F(1),F(0),F(1),F(0),av,sign*yv,True))
    av=1-eps
    for h in [F(0),F(1,8),F(499,1000)]:
        feasible.append((av,F(1),h,F(1),F(0),F(1),F(0),False))
    feasible.append((av,1-eps/2,F(0),F(1),F(0),F(1),F(0),False))
    cv=F(1024**2-1,1024**2+1);dv=F(2048,1024**2+1)
    for h in [-F(1,4),F(1,4)]:feasible.append((av,F(1),h,cv,dv,cv,dv,False))
    for av,mv,h,cv,dv,xv,yv,attained in feasible:
        u=gaussian_mul((xv,yv),(cv,dv));v=gaussian_mul((xv,yv),(cv,-dv))
        U=gaussian_scale(u,mv+h);V=gaussian_scale(v,mv-h)
        actual=direct_integral(U,V,av);rv=mv*mv-h*h
        need(av>=1-eps and av<1 and mv+h>=F(1,2) and mv-h>=F(1,2) and mv<=1,
             'Rational profile radial domain')
        need(gaussian_norm(u)==gaussian_norm(v)==1 and (U[0]+V[0])/2>=av,
             'Rational profile actual-mean domain')
        fstar=A.evaluate(ref,(1-av,F(0),F(0),F(0),F(0)))
        loss=av*av*gaussian_norm(actual)-rv**8*(1+fstar)
        penalty=F(3,2)*h*h+16*(1-mv)+2*(1-cv)
        need(loss>=penalty,'Rational coercive minimum control')
        if attained:need(loss==0,'Exact attained minimum, both conjugates')
        else:need(loss>0,'Strict nonminimum control')
        controls.append([str(z) for z in [av,mv,h,cv,dv,xv,yv,loss,penalty]])
    av=F(1,2)
    real_norm=gaussian_norm(direct_integral((F(1),F(0)),(F(1),F(0)),av))
    saturated_norm=(1+A.evaluate(ref,(1-av,F(0),F(0),F(0),F(0))))/(av*av)
    polar=sum(F(comb(8,k),k+1)*av**(8-k)*(1-av*av)**k for k in range(9))
    need(real_norm==F(261121,65536) and saturated_norm==F(281827,65536),
         'Exact obstruction to a global mean-saturated minimum')
    need(saturated_norm-real_norm==F(10353,32768) and polar==F(72319,65536)>1,
         'Polar-feasible strict obstruction; not an origin-feasible polynomial')
    controls.append([str(z) for z in [av,real_norm,saturated_norm,polar]])
    payload={'P':A.canonical(P),'J':A.canonical(J),'shifted_P':A.canonical(shifted),
             'shifted_J':A.canonical(skew),'pure':A.canonical(pure),
             'quotient':A.canonical(quotient),'diagonal_reference':A.canonical(ref)}
    cert.update(unshifted_terms={'P':len(P),'J':len(J)},
        total_pinned_coefficients=sum(len(z) for z in payload.values()),
        direct_integral_component_polynomials=18,complete_norm_identity_polynomials=2,
        complete_inverse_polynomials=2,complete_reference_polynomials=3,
        minimum_series=series,rational_profile_count=len(controls),attained_minimum_profiles=4,
        global_minimum_extension_obstruction={'a':'1/2','real_norm':str(real_norm),
            'saturated_norm':str(saturated_norm),'polar':str(polar),
            'strict_difference':str(saturated_norm-real_norm)},
        profile_sha256=hashlib.sha256(json.dumps(controls,separators=(',',':')).encode()).hexdigest(),
        full_coefficients_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest())
    return cert

def check_manifest(actual,expected):
    if actual!=expected:raise ArithmeticError('Compact manifest mismatch')

def main():
    start=time.monotonic();actual=derive()
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    check_manifest(actual,expected)
    corruptions=[('epsilon','1/8192'),('first_variation',['2','18','18/7','0']),
                 ('full_coefficients_sha256','0'*64),('shifted_P_terms',32558),
                 ('direct_integral_component_polynomials',17),('pure_minimum_degree',4),
                 ('leading_quotient',['576']*5),('minimum_series',['1','2','3','4','5','6'])]
    rejected=0
    for field,value in corruptions:
        bad=dict(expected);bad[field]=value
        try:check_manifest(actual,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Corrupted compact manifest accepted')
    need(rejected==8,'Mutation controls')
    print('PASS: exact coalesced reference and full signed-skew minimum majorants')
    print('Coefficient inventory SHA256',actual['full_coefficients_sha256'])
    print(actual['total_pinned_coefficients'],'exact coefficients pinned')
    print('18 integral, 2 norm, 2 inverse and 3 reference polynomial identities')
    print(actual['rational_profile_count'],'exact rational controls; 4 attained minima; 8 corruptions rejected')
    print('Minimum series:',','.join(actual['minimum_series']))
    print('Elapsed seconds',round(time.monotonic()-start,6),
          'peak RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

if __name__=='__main__':main()
