#!/usr/bin/env python3
"""Independent reflected-light audit: six-reviewer-3, independent reviewer.

No target module or coefficient table is imported. Sparse Fraction operations
are adapted, with attribution, from this reviewer's cbfb1909... checker.
Integral cross-products, closed binomial radius composition, triangular basis
solves and literal inverse expansions regenerate the whole finite proof.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb, lcm, prod
import argparse, hashlib, json
ZERO=(0,0,0,0)
def demand(ok,label):
    if not ok: raise ValueError(label)
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
class P:
    def __init__(self,value=0):
        self.terms=({e:F(c) for e,c in value.items() if c} if isinstance(value,dict)
                    else {ZERO:F(value)} if value else {})
    @staticmethod
    def cast(value): return value if isinstance(value,P) else P(value)
    def __add__(self,other):
        out=dict(self.terms)
        for e,c in P.cast(other).terms.items(): out[e]=out.get(e,F(0))+c
        return P(out)
    __radd__=__add__
    def __neg__(self): return P({e:-c for e,c in self.terms.items()})
    def __sub__(self,other): return self+-P.cast(other)
    def __rsub__(self,other): return P.cast(other)+-self
    def __mul__(self,other):
        out=defaultdict(F)
        for e,c in self.terms.items():
            for f,d in P.cast(other).terms.items():
                out[tuple(a+b for a,b in zip(e,f))]+=c*d
        return P(out)
    __rmul__=__mul__
    def __truediv__(self,other): return P({e:c/F(other) for e,c in self.terms.items()})
    def __pow__(self,n):
        demand(type(n) is int and n>=0,'nonnegative integer power')
        out,base=P(1),self
        while n:
            if n&1: out=out*base
            n//=2
            if n: base=base*base
        return out
    def substitute_axis(self,axis,replacement):
        powers=[replacement**j for j in range(1+max(e[axis] for e in self.terms))]
        out=defaultdict(F)
        for e,c in self.terms.items():
            old=list(e);old[axis]=0
            for f,d in powers[e[axis]].terms.items():
                out[tuple(a+b for a,b in zip(old,f))]+=c*d
        return P(out)
    def canonical(self): return [[list(e),str(c)] for e,c in sorted(self.terms.items())]
    def evaluate(self,point):
        powers=[[point[i]**j for j in range(1+max(e[i] for e in self.terms))] for i in range(4)]
        return sum((c*prod(powers[i][e[i]] for i in range(4)) for e,c in self.terms.items()),F(0))
def variable(axis):
    e=list(ZERO);e[axis]=1;return P({tuple(e):1})
b,r,x,t=[variable(i) for i in range(4)]
s=4-3*r;D=1+b
def raw_integral():
    # I=sum_j g_j U^j; U*conj(U)=r^2. Re(U^k) by its two-root recurrence.
    g=[9*comb(6,j)*(-b)**j*(F(1,j+1)-2*b*t/F(j+2)+b*b*s*s/F(j+3)) for j in range(7)]
    real=[P(1),x]
    for k in range(1,6): real.append(2*x*real[k]-r*r*real[k-1])
    norm=P()
    for j in range(7):
        norm+=g[j]*g[j]*r**(2*j)
        for k in range(j+1,7): norm+=2*g[j]*g[k]*r**(2*j)*real[k-j]
    raw=norm-r**12*s**4
    demand(len(raw.terms)==292,'complete raw support')
    phase=raw.substitute_axis(2,r-F(4,3)*(1-b)*x)
    loss=phase.substitute_axis(3,s-4*(1-b)*(1-x)*t)
    demand((len(phase.terms),len(loss.terms))==(929,1453),'complete loss supports')
    return raw,loss
def radius_compose(loss,alpha):
    # r=(D+alpha*b*y)/D; D^16 r^j expands by a single closed binomial formula.
    out=defaultdict(F)
    for (eb,er,eu,ew),c in loss.terms.items():
        demand(er<=16,'clearing exponent sufficient')
        for j in range(er+1):
            d=c*comb(er,j)*alpha**j
            for k in range(17-j):out[(eb+j+k,j,eu,ew)]+=d*comb(16-j,k)
    mapped=P(out);margin=mapped-(1-b)*D**16
    demand(len(mapped.terms)==4570,'complete radius support')
    demand(tuple(max(e[i] for e in margin.terms) for i in range(4))==(32,16,8,2),'complete degree tensor')
    return mapped,margin
def fibres(degrees,axis):
    shape=[n+1 for n in degrees];stride=prod(shape[axis+1:]);block=stride*shape[axis]
    for start in range(0,prod(shape),block):
        for tail in range(stride):yield [start+tail+i*stride for i in range(shape[axis])]
def tensor(polynomial,degrees):
    shape=[n+1 for n in degrees];stride=[prod(shape[i+1:]) for i in range(len(shape))]
    denominator=lcm(*(c.denominator for c in polynomial.terms.values()))
    values=[0]*prod(shape)
    for e,c in polynomial.terms.items():values[sum(e[i]*stride[i] for i in range(len(e)))]=int(c*denominator)
    return values,denominator
def bernstein(polynomial,degrees):
    values,denominator=tensor(polynomial,degrees)
    for axis,n in enumerate(degrees):
        scale=lcm(*(comb(n,k) for k in range(n+1)))
        for fibre in fibres(degrees,axis):
            coefficients=[]
            for k,index in enumerate(fibre):
                # Triangular solve for power_k / choose(n,k).
                value=values[index]*(scale//comb(n,k))
                value-=sum((-1)**(k-j)*comb(k,j)*coefficients[j] for j in range(k))
                coefficients.append(value)
            for index,value in zip(fibre,coefficients):values[index]=value
        denominator*=scale
    return values,denominator
def literal_inverse(values,denominator,degrees):
    values=list(values)
    for axis,n in enumerate(degrees):
        for fibre in fibres(degrees,axis):
            old=[values[i] for i in fibre]
            new=[sum(old[i]*comb(n,i)*comb(n-i,k-i)*(-1)**(k-i) for i in range(k+1)) for k in range(n+1)]
            for index,value in zip(fibre,new):values[index]=value
    shape=[n+1 for n in degrees];stride=[prod(shape[i+1:]) for i in range(len(shape))]
    return {tuple((index//stride[i])%shape[i] for i in range(len(shape))):F(value,denominator)
            for index,value in enumerate(values) if value}
def certificate(mapped,margin,label,original_tensors=None):
    degrees=(32,16,8,2);values,den=bernstein(margin,degrees)
    demand(literal_inverse(values,den,degrees)==margin.terms,'full inverse polynomial '+label)
    demand(len(values)==15147 and min(values)>=0,'whole tensor signs '+label)
    stride=[prod(n+1 for n in degrees[i+1:]) for i in range(4)]
    zeros={tuple((j//stride[i])%(degrees[i]+1) for i in range(4)) for j,v in enumerate(values) if not v}
    demand(zeros=={(32,j,k,l) for j in (0,1) for k in range(9) for l in range(3)},'entire zero face '+label)
    demand(min(F(v,den) for v in values if v>0)==79,'minimum positive '+label)
    if original_tensors is not None:
        supplied=original_tensors[label]
        demand(len(supplied)==len(values),'entire original tensor length')
        for i,(value,reference) in enumerate(zip(values,supplied)):
            demand(F(value,den)==F(reference),'literal original coefficient '+label+str(i))
    changed=list(values);changed[-1]+=den
    demand(literal_inverse(changed,den,degrees)!=margin.terms,'damaged positive coefficient detected')
    # Inequality extraction: summing every zero basis term leaves 1-b^32 J(y).
    return {'chart':label,'degrees':list(degrees),'count':len(values),'negative':0,'positive':sum(v>0 for v in values),
            'zero':len(zeros),'minimum':'0','minimum_positive':'79',
            'coefficient_sha256':digest([str(F(v,den)) for v in values]),
            'zero_support_sha256':digest([list(e) for e in sorted(zeros)]),
            'mapped_sha256':digest(mapped.canonical()),'margin_sha256':digest(margin.canonical())}
def refinements():
    # N=4096 sum_0^31 b^k-(1+b)^16; small independent triangular solve/inverse.
    coefficients=[4096-(comb(16,k) if k<=16 else 0) for k in range(32)]
    controls=[]
    for k,c in enumerate(coefficients):
        controls.append(F(c,comb(31,k))-sum((-1)**(k-j)*comb(k,j)*controls[j] for j in range(k)))
    inverse=[sum(controls[i]*comb(31,i)*comb(31-i,k-i)*(-1)**(k-i) for i in range(k+1)) for k in range(32)]
    demand(inverse==coefficients and min(controls)==4095,'complete geometric-series bound')
    factor=lambda u:162*(1+u+u*u/3)*(u+2*u*u/3)
    demand(factor(F(5,2))==6030 and factor(F(1))==630,'two radius norm-loss caps')
    demand(630*F(7,6)**12<6030,'larger-radius cap below 6030')
    gap=1+F(79,4096)-F(6030,6000)
    demand(gap==F(1463,102400) and gap>0,'6000 tube positive surplus')
    return {'geometric_bernstein_degree':31,'geometric_positive_controls':32,'geometric_minimum':'4095',
            'geometric_controls_sha256':digest([str(v) for v in controls]),'norm_loss_lipschitz':'6030',
            'larger_radius_cap':str(630*F(7,6)**12),'reflected_linear_surplus':'4175/4096',
            'center_tube_denominator':6000,'center_norm_surplus':'1463/102400*(1-b)'}
def quadratic_controls(raw,loss):
    # Direct eight-factor multiplication in Q[iY], with Y^2=r^2-x^2.
    def multiply(p,q,y2):return (p[0]*q[0]-y2*p[1]*q[1],p[0]*q[1]+p[1]*q[0])
    records=[]
    for alpha in (F(1,3),F(-1)):
      for bb,yy,uu,ww in product((F(0),F(1,2),F(1)),repeat=4):
        rr=1+alpha*bb*yy/(1+bb);ss=4-3*rr
        xx=rr-F(4,3)*(1-bb)*uu;tt=ss-4*(1-bb)*(1-uu)*ww;y2=rr*rr-xx*xx
        demand(y2>=0,'real enlarged cube')
        tau=[(F(1),F(0))]
        for _ in range(6):
            out=[(F(0),F(0))]*(len(tau)+1)
            for j,c in enumerate(tau):
                out[j]=(out[j][0]+c[0],out[j][1]+c[1])
                d=multiply(c,(-bb*xx,-bb),y2)
                out[j+1]=(out[j+1][0]+d[0],out[j+1][1]+d[1])
            tau=out
        integrated=[F(0),F(0)]
        for j,c in enumerate(tau):
            for k,wgt in enumerate((F(1),-2*bb*tt,bb*bb*ss*ss)):
                for component in (0,1):integrated[component]+=9*c[component]*wgt/F(j+k+1)
        norm=integrated[0]**2+y2*integrated[1]**2
        difference=norm-rr**12*ss**4
        demand(raw.evaluate((bb,rr,xx,tt))==difference,'direct quadratic-field raw identity')
        demand(loss.evaluate((bb,rr,uu,ww))==difference,'direct complete loss identity')
        records.append([str(alpha),*map(str,(bb,yy,uu,ww,difference))])
    return {'count':len(records),'sha256':digest(records)}
class G:
    """Rational Gaussian number; no floating complex arithmetic."""
    def __init__(self,re=0,im=0):self.re,self.im=F(re),F(im)
    @staticmethod
    def cast(z):return z if isinstance(z,G) else G(z)
    def __add__(self,z):
        z=G.cast(z);return G(self.re+z.re,self.im+z.im)
    __radd__=__add__
    def __neg__(self):return G(-self.re,-self.im)
    def __sub__(self,z):return self+-G.cast(z)
    def __rsub__(self,z):return G.cast(z)+-self
    def __mul__(self,z):
        z=G.cast(z);return G(self.re*z.re-self.im*z.im,self.re*z.im+self.im*z.re)
    __rmul__=__mul__
    def conjugate(self):return G(self.re,-self.im)
    def norm(self):return self.re*self.re+self.im*self.im
    def __truediv__(self,z):
        z=G.cast(z);demand(z.norm()>0,'nonzero Gaussian divisor');v=self*z.conjugate()
        return G(v.re/z.norm(),v.im/z.norm())
    def __pow__(self,n):
        out=G(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,z):
        z=G.cast(z);return self.re==z.re and self.im==z.im
    def strings(self):return [str(self.re),str(self.im)]
def gaussian_product(factors):
    result=[G(1)]
    for c,d in factors:
        out=[G() for _ in range(len(result)+1)]
        for j,z in enumerate(result):out[j]+=c*z;out[j+1]+=d*z
        result=out
    return result
def gaussian_value(coefficients,z):
    out=G()
    for c in reversed(coefficients):out=out*z+c
    return out
def gaussian_integral(factors):
    coefficients=gaussian_product(factors)
    return sum((c/F(j+1) for j,c in enumerate(coefficients)),G())
def actual_examples():
    records=[]
    for k in (F(0),F(1,1000000)):
        a=F(1,2);alpha=G((1-k*k)/(1+k*k),2*k/(1+k*k))
        offsets=[G(0,F(1,100))]*6+[G(0,F(1,50))*alpha.conjugate(),G(0,F(-1,50))*alpha.conjugate()]
        points=[a+z for z in offsets]
        derivative=[9*c for c in gaussian_product([(-z,G(1)) for z in offsets])]
        centered=[G()]+[c/F(j+1) for j,c in enumerate(derivative)]
        global_p=[G() for _ in range(10)]
        for j,c in enumerate(centered):
            for l in range(j+1):global_p[l]+=c*comb(j,l)*(-a)**(j-l)
        global_dp=[(j+1)*global_p[j+1] for j in range(9)]
        demand(global_dp==[9*c for c in gaussian_product([(-z,G(1)) for z in points])],'whole original derivative')
        demand(gaussian_value(global_p,G(a))==0 and gaussian_value(global_dp,G(a)).norm()>0,'marked simple root')
        tail=sum((abs(c.re)+abs(c.im))*F(1,4)**j for j,c in enumerate(centered[:-1]))
        demand(centered[-1]==1 and tail<F(1,4)**9,'strict Rouche certificate')
        demand(any(c.im for c in global_p),'actual polynomial nonreal')
        demand(offsets[-1].norm()==offsets[-2].norm()==F(1,50)**2,'equal light distances')
        demand(points[-1]!=points[-2].conjugate() if k else points[-1]==points[-2].conjugate(),'reflection classification')
        demand((alpha-1).norm()<=F(1,160000)**2,'author example tube chord')
        ratios=[]
        for m in (F(1,2),F(3,4),F(1)):
            bb=m*a;pm=[c*m**(9-j) for j,c in enumerate(global_p)]
            dp=[(j+1)*pm[j+1] for j in range(9)];recip=[G(1)/(bb-m*z) for z in points]
            integral=9*gaussian_integral([(G(1),-bb*u) for u in recip])
            recprod=prod(recip)
            demand(integral==-pm[0]*recprod/bb,'actual scaled origin communication')
            normalized=integral.norm()/prod(u.norm() for u in recip)
            demand(normalized==m**16*global_p[0].norm()/(a*a),'exact m16 normalization')
            polar=gaussian_integral([(G(bb),(1-bb*bb)*u) for u in recip])
            demand(polar==bb**9/(1-bb*bb)*gaussian_value(pm,G(1/bb))/gaussian_value(dp,G(bb)) and polar.norm()>=1,'actual polar communication')
            # Synthetic division at the marked root, then direct derivative identity.
            quotient=[G() for _ in range(9)];quotient[8]=pm[9]
            for j in range(7,-1,-1):quotient[j]=pm[j+1]+bb*quotient[j+1]
            d2=[(j+1)*dp[j+1] for j in range(8)];qp=[(j+1)*quotient[j+1] for j in range(8)]
            demand(gaussian_value(d2,G(bb))/gaussian_value(dp,G(bb))==2*gaussian_value(qp,G(bb))/gaussian_value(quotient,G(bb)),'marked derivative identity')
            ratios.append([*map(str,(m,bb,normalized)),*polar.strings()])
        records.append({'a':str(a),'H':points[0].strings(),'L1':points[-2].strings(),'L2':points[-1].strings(),
                        'heavy_unit_real':'0','old_cone_required_real':'11/20','center_halfangle':str(k),
                        'center_chord_squared':str((alpha-1).norm()),'centered_rouche_radius':'1/4',
                        'centered_rouche_tail':str(tail),'centered_rouche_leading_bound':'1/262144',
                        'original_coefficients_sha256':digest([c.strings() for c in global_p]),
                        'communication_scalings':len(ratios),'communication_sha256':digest(ratios)})
    return records
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',type=Path);parser.add_argument('--write',type=Path)
    parser.add_argument('--original',type=Path);parser.add_argument('--original-tensors',type=Path);args=parser.parse_args()
    expected_check=json.loads(args.check.read_text()) if args.check else None
    original_tensors=json.loads(args.original_tensors.read_text()) if args.original_tensors else None
    raw,loss=raw_integral();charts=[]
    for label,alpha in (('nearer',F(1,3)),('farther',F(-1))):
        mapped,margin=radius_compose(loss,alpha);charts.append(certificate(mapped,margin,label,original_tensors))
    result={'reviewer':'six-reviewer-3','role':'independent mathematical reviewer','verified':True,
            'raw_terms':292,'phase_terms':929,'loss_terms':1453,'raw_sha256':digest(raw.canonical()),
            'loss_sha256':digest(loss.canonical()),'charts':charts,'complete_tensor_signs':30294,
            'full_tensor_inverse_identities':2,'refinements':refinements(),'quadratic_controls':quadratic_controls(raw,loss),
            'damaged_positive_coefficients_rejected':2,'example_and_communication':actual_examples()}
    if args.original:
        original=json.loads(args.original.read_text())
        for key in ('raw_terms','phase_terms','loss_terms','raw_sha256','loss_sha256','charts','example_and_communication'):
            demand(result[key]==original[key],'complete original record comparison '+key)
    if args.check:demand(result==expected_check,'complete mandatory independent fixture')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verified':True,'complete_tensor_signs':30294,'full_inverse_identities':2,
                      'center_tube_denominator':6000,'result_sha256':digest(result)},sort_keys=True))
if __name__=='__main__':main()
