"""Reconstruct and check the complete exact collar coefficient inventory."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,comb
import json,hashlib,time,resource
import algebra as A

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

def direct_integral(U,V,a,polar=False):
    f0=a if polar else F(1)
    f1=1-a*a if polar else -a
    rows=[]
    for W in [U,V]:
        rows.append([gaussian_scale(gaussian_power(W,k),comb(4,k)*f0**(4-k)*f1**k) for k in range(5)])
    coefficients=[(F(0),F(0))]*9
    for j in range(5):
        for k in range(5):coefficients[j+k]=gaussian_add(coefficients[j+k],gaussian_mul(rows[0][j],rows[1][k]))
    z=(F(0),F(0))
    for k,row in enumerate(coefficients):z=gaussian_add(z,gaussian_scale(row,F(1 if polar else 9,k+1)))
    return z

def derive():
    delta,J,P,Q=A.norm_polynomials()
    p,q=A.alternate_integral_coefficients()
    need(p==P and q==Q,'All direct-convolution integral coefficients')
    even,skew=A.alternate_norm(p,q)
    R=A.add(A.power(A.variable(1),2),A.scale(A.variable(4),-1))
    need(A.add(even,A.scale(A.power(R,8),-1))==delta and skew==J,'Complete independent norm expansion')
    cert,shifted,shifted_J=A.certificate(delta,J)
    inv=shifted;inv_J=shifted_J
    for axis in range(4):
        inv=A.shifted_axis(inv,axis);inv_J=A.shifted_axis(inv_J,axis)
    need(inv==delta and inv_J==J,'Whole inverse affine substitutions')
    I=[F(9*comb(4,j)*(-1)**j*factorial(2*j)*factorial(8-2*j),factorial(9)) for j in range(5)]
    need(I==[F(1),F(-1,7),F(3,35),F(-1,7),F(1)],'Independent beta-integral base')
    base=[F(0)]*9
    for j in range(5):
        for k in range(5):base[j+k]+=I[j]*I[k]
    base=[v-F(comb(8,k)*(-1)**k) for k,v in enumerate(base)]
    need([str(v) for v in base]==cert['base_coefficients'],'Whole base polynomial')
    moment=lambda j,k:F(factorial(j)*factorial(k),factorial(j+k+1))
    first=[144*moment(1,7),144*moment(1,7)+16,
           144*moment(1,6),F(0)]
    need([str(v) for v in first]==cert['first_variation'],'Independent integral first variations')
    need(F(8)-72*moment(2,6)==F(54,7),'Radial q coefficient')
    need(F(333,140)*F(7,8)>2 and F(431,448)>F(7,8),'Uniform base inequality arithmetic')
    need(F(cert['K'])<=2**cert['epsilon_power_two'] and cert['epsilon_power_two']==14,'Explicit collar constant')
    profiles=[(F(1),F(0)),(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(399,401),F(40,401))]
    controls=[]
    for index,(c,d) in enumerate(profiles):
        for h in [F(0),F(1,1000),F(-1,4)]:
            x,y=profiles[(index+1)%len(profiles)]
            if index%2:y=-y
            a=F(3,5);m=F(7,8);w=(x,y)
            u=gaussian_mul(w,(c,d));v=gaussian_mul(w,(c,-d))
            U=gaussian_scale(u,m+h);V=gaussian_scale(v,m-h)
            actual=direct_integral(U,V,a)
            values=(a,m,c,x,h*h);lam=-h*d*y
            predicted=A.evaluate(A.add(delta,A.power(R,8)),values)+lam*A.evaluate(J,values)
            need(predicted==gaussian_norm(actual),'Rational direct Gaussian identity')
            controls.append([str(z) for z in [a,m,h,c,d,x,y,*actual,predicted]])
    for h in [F(0),F(1,8),F(499,1000)]:
        a=F(16383,16384);m=F(1);U=(m+h,F(0));V=(m-h,F(0))
        polar=direct_integral(U,V,a,True);origin=direct_integral(U,V,a)
        need(gaussian_norm(polar)>=1,'Exact polar-feasible collar control')
        gap=gaussian_norm(origin)-(m*m-h*h)**8
        need(gap>=1-a+h*h,'Exact collar gap control')
        need(min(m+h,m-h)>=1/(1+a),'Exact lower-radius control')
        controls.append([str(z) for z in [a,m,h,*polar,*origin,gap]])
    payload={'delta':A.canonical(delta),'J':A.canonical(J),
             'shifted_delta':A.canonical(shifted),'shifted_J':A.canonical(shifted_J)}
    cert.update(unshifted_terms={'delta':len(delta),'J':len(J)},
                direct_integral_component_polynomials=18,complete_norm_identity_polynomials=2,
                complete_inverse_polynomials=2,rational_profile_count=len(controls),
                profile_sha256=hashlib.sha256(json.dumps(controls,separators=(',',':')).encode()).hexdigest(),
                full_coefficients_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest())
    return cert

def check_manifest(actual,expected):
    if actual!=expected:
        raise ArithmeticError('Compact manifest mismatch')

def main():
    start=time.monotonic()
    actual=derive()
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    check_manifest(actual,expected)
    corruptions=[('epsilon_power_two',13),('first_variation',['-2','18','18/7','0']),
                 ('full_coefficients_sha256','0'*64),('delta_shifted_terms',28617),
                 ('direct_integral_component_polynomials',17),('K','1')]
    rejected=0
    for field,value in corruptions:
        bad=dict(expected);bad[field]=value
        try:check_manifest(actual,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Corrupted compact manifest accepted')
    need(rejected==6,'Mutation controls')
    need(F(actual['K'])<13000 and F(actual['Kq'])+2*F(actual['Lq'])<353,
         'Readable exact majorant bounds')
    print('PASS: full affine-skew identity and whole inverse reconstructions')
    print('Coefficient inventory SHA256',actual['full_coefficients_sha256'])
    print('44,485 coefficients pinned; 18 integral, 2 norm and 2 inverse polynomial checks')
    print('15 exact rational profiles; 6 corrupted compact manifests rejected')
    print('K < 13000 < 16384; collar epsilon = 1/16384')
    print('Elapsed seconds',round(time.monotonic()-start,6),
          'peak RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

if __name__=='__main__':main()
