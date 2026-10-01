"""Portable cleared-polynomial Sylvester certificates for dense caps.

Integer q>=0,v>=12,3v>=7q+10,l=v-2-q. Exact Fraction arithmetic
checks the identities; native integer binomial expansion checks all
coefficients. No GCD, CAS, floating point or sampled sign inference.
six-downset-2, researcher.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from math import comb
from bivariate_certificates import RF

DOMAINS={**{'q'+str(i):(12,0,i,0)for i in range(4)},
    'q4mod3':(13,7,4,3),'q5mod3':(15,7,5,3),'q6mod3':(18,7,6,3)}


@lru_cache(None)
def affine_monomial(pv,pq,domain):
    v0,vy,q0,qy=DOMAINS[domain];out={}
    for i in range(pv+1):
        for j in range(pv-i+1):
            for h in range(pq+1):
                z=comb(pv,i)*comb(pv-i,j)*v0**(pv-i-j)*vy**j*comb(pq,h)*q0**(pq-h)*qy**h
                key=(i,j+h);out[key]=out.get(key,0)+z
    return tuple((p,c)for p,c in out.items()if c)


def shifted(p,domain):
    out={}
    for (i,j),c in p.items():
        assert c.denominator==1;c=c.numerator
        for key,z in affine_monomial(i,j,domain):out[key]=out.get(key,0)+c*z
    return {p:c for p,c in out.items()if c}


def terms(p):return [[i,j,str(c)]for(i,j),c in sorted(p.items())]


def certificate(pair,domain):
    lists=[];record={}
    for label,p in zip(('num','den'),pair):
        assert p.d=={(0,0):F(1)}
        z=shifted(p.n,domain);assert z.get((0,0),0)>0 and all(c>=0 for c in z.values())
        lists.append(terms(z));record[label]={'constant':str(z[(0,0)]),'term_count':len(z)}
    record['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return record


def run():
    v,q=RF({(1,0):1}),RF({(0,1):1});l=v-2-q
    r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b;k=(v-2)*(v-3)/2
    F2,F3,F4=v-2,v-3,v-4
    D=l*(v*v-10*v+27)-6
    T=(v-1)*(l*F3-6);C=3*v*v-3*(l+3)*v+11*l;U=v*v-v-4
    c=C/(3*F2*F3);d=U/(F4*F3);t=T/D
    w=s-F3*c-(r-2*l)*d;h=s-F4*d-(r-3*l)*t
    tau=N-m*k/(v*v)
    A=12*v+6*v*v*(v-1)+2*v*l*(v-1)*F3;H=A-3*(v-1)*F2*F3
    X1=D*(H-4*v*l)-6*q*(q-1)*v*v*T
    X2=H*F2*F3-4*v*C;X3=D*H-12*v*T*(v-5)
    P12=2*(v+2)*F4*F3+U*q*(v+7)
    P13=D*(2*l+v-3)+2*T*q*F2;P23=U*(v+5)
    L1=12*v*D;L2=12*v*F2*F3
    B12=8*F4*F3;B13=2*D;B23=8*F3
    M1=X1
    M2=4*X1*X2*F4**2*F3-9*v*v*D*F2*P12**2
    M3=(4*X1*X2*X3*F4**2*F3-9*v*v*D*F4**2*F2*X1*P23**2
        -144*v*v*F4**2*F3*X2*P13**2-9*v*v*D*F2*X3*P12**2
        -108*v**3*D*F4*F2*P12*P13*P23)
    den2=576*v*v*D*F4**2*F3**2*F2
    den3=6912*v**3*D**2*F4**2*F3**2*F2
    Lw=6*F2*F4*F3;Lh=2*F3*D
    expressions={
        'lambda_gt6':(l-6,RF(1)),'D_positive':(D,RF(1)),
        'c_positive':(C,3*F2*F3),'d_positive':(U,F4*F3),'t_gt_1':(T-D,D),
        'd_minus_w_gt_minus1':(Lw*(1-s)+2*C*F4*F3+6*F2*(r-2*l+1)*U,Lw),
        'd_minus_w_lt1':(Lw*(1+s)-2*C*F4*F3-6*F2*(r-2*l+1)*U,Lw),
        'three_t_minus_h_gt_minus2':(Lh*(2-s)+2*D*U+2*F3*(r-3*l+3)*T,Lh),
        'three_t_minus_h_lt2':(Lh*(2+s)-2*D*U-2*F3*(r-3*l+3)*T,Lh),
        'constant_below_s':(3*(v-1)+l*(v-5),RF(3)),
        'Sylvester1':(M1,L1),'Sylvester2':(M2,den2),'Sylvester3':(M3,den3)}
    a,b0,z=X1/L1,X2/L2,X3/L1;p=P12/B12;hh=P13/B13;f=P23/B23
    eqs={
        'C11_cleared':(tau-s-l/3-t*q*(q-1)*v/2)*L1-X1,
        'C22_cleared':(tau-s-c)*L2-X2,
        'C33_cleared':(tau-s-t*(v-5))*L1-X3,
        'cross12_cleared':((v+2)/4+d*q*(v+7)/8)*B12-P12,
        'cross13_cleared':(l+(v-3)/2+t*q*F2)*B13-P13,
        'cross23_cleared':(d*F4*(v+5)/8)*B23-P23,
        'Sylvester2_cleared':(a*b0-p*p)*den2-M2,
        'Sylvester3_cleared':(a*b0*z-a*f*f-b0*hh*hh-z*p*p-2*p*hh*f)*den3-M3,
        'point_radical_square':(v+2)**2-16*(v-2)-(v-6)**2,
        'completion_radical_square':(v+7)**2-32*(v-1)-(v-9)**2,
        'pair_triple_radical_square':(v+5)**2-16*(2*v-6)-(v-11)**2,
        'completion_triple_radical_square':(v-2)**2-(v-1)*(v-3)-1,
        'Bl_AMGM_square':(l+(v-3)/2)**2-2*l*(v-3)-(l-(v-3)/2)**2,
        'constant_below_s':s-(l*(v+7)/6+1)-(v-1+l*(v-5)/3),
        **{name+'_cleared':(expr)*expressions[name][1]-expressions[name][0]
            for name,expr in [('d_minus_w_gt_minus1',1+d-w),('d_minus_w_lt1',1-d+w),
                ('three_t_minus_h_gt_minus2',2+3*t-h),('three_t_minus_h_lt2',2-3*t+h)]},
        'tau_minus_s_cleared':(tau-s)*12*v-H}
    assert all(z.is_zero()for z in eqs.values())
    records={domain:{name:certificate(z,domain)for name,z in expressions.items()}for domain in DOMAINS}
    return {'agent':'six-downset-2','role':'researcher',
        'arithmetic':'Sparse Fraction Q(v,q) identities; integer binomial affine expansion',
        'domain':'integer q>=0,v>=12,3v>=7q+10,l=v-2-q','affine_domains':{name:list(z)for name,z in DOMAINS.items()},
        'zero_identities':len(eqs),'identity_names':list(eqs),'strict_certificates':records,
        'strict_certificate_count':sum(len(z)for z in records.values()),
        'unshifted_Sylvester_numerator_degrees':{name:max(i+j for i,j in expressions[name][0].n)
            for name in ('Sylvester1','Sylvester2','Sylvester3')},
        'interpretation':'Positive denominators and91 coefficient signs certify3 leading Sylvester minors; ordinary full-mode bridge in DENSE_SCHUR_CAP.md.'}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
