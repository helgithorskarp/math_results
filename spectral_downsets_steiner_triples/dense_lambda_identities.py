"""Portable exact scalar certificates for the dense-complement cap.

Integer q>=0, v>=12, v>=4(q+1), l=v-2-q. Three exact affine quadrants
cover q0, q1 and q>=2. No CAS, floating point or polynomial GCD.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from bivariate_certificates import RF,poly,terms


def shifted(p,domain):
    assert domain in ('q0','q1','q2plus');out={}
    for (pv,pq),c in p.items():
        if domain in ('q0','q1'):
            q0=int(domain[1:])
            for i in range(pv+1):
                key=(i,0)
                out[key]=out.get(key,F(0))+c*comb(pv,i)*12**(pv-i)*q0**pq
        else:
            # q=2+y, v=12+4y+x. Expand the v power trinomially.
            for i in range(pv+1):
                for j in range(pv-i+1):
                    for k in range(pq+1):
                        key=(i,j+k)
                        factor=comb(pv,i)*comb(pv-i,j)*12**(pv-i-j)*4**j*comb(pq,k)*2**(pq-k)
                        out[key]=out.get(key,F(0))+c*factor
    return poly(out)


def certificate(expr,domain):
    n,d=shifted(expr.n,domain),shifted(expr.d,domain)
    assert n.get((0,0),F(0))>0 and d.get((0,0),F(0))>0
    assert all(z>=0 for z in n.values()) and all(z>=0 for z in d.values())
    serial=json.dumps([terms(n),terms(d)],separators=(',',':'))
    return {'num_terms':len(n),'den_terms':len(d),
        'num_constant':str(n[(0,0)]),'den_constant':str(d[(0,0)]),
        'coefficient_sha256':sha256(serial.encode()).hexdigest()}


def run():
    v,q=RF({(1,0):1}),RF({(0,1):1});l=v-2-q
    r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b;k=(v-2)*(v-3)/2
    D=l*(v*v-10*v+27)-6
    c=(v*v-(l+3)*v+F(11,3)*l)/((v-2)*(v-3))
    d=(v*v-v-4)/((v-4)*(v-3));t=(v-1)*(l*(v-3)-6)/D
    w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*t
    B=s+v*v/2+(q*q+2*q+F(3,2))*v-10;delta=N-B
    gap_poly=66-6*v*(q*q+2*q+2)+(v-q-2)*(v-1)*(v-3)
    G=132*v-12*v*v*(q*q+2*q+2)+2*v*(v-q-2)*(v-1)*(v-3)-3*(v-1)*(v-2)*(v-3)
    row1=s+(q*q+F(3,2)*q+F(13,6))*v
    row2=s+F(4,3)+v/3+q*v/2+v*(v-4)/2
    row3=s+v*v/2+(2*q+F(3,2))*v-10
    rq,uq=q*(v-1)/2,q*(q-1)/2;ul=l*(l-1)/2
    eqs={
        'delta_polynomial':delta-gap_poly/6,
        'repair_margin_polynomial':delta/2-m*k/(2*v*v)-G/(24*v),
        'row1_difference':B-row1-(v*v/2+(q/2-F(2,3))*v-10),
        'row2_difference':B-row2-(q*q*v+(F(3,2)*q+F(19,6))*v-F(4,3)-10),
        'row3_difference':B-row3-q*q*v,
        'constant_difference':B-(l*(v+7)/6+1)-(B-s+v-1+l*(v-5)/3),
        'complement_variance':(r-ul)-(rq-uq)-(l-q),
        'completion_Z_bound':q*rq-(rq-uq)-uq*v,
        'root_square_difference':(v-2)**2-8*(v-3)-(v*(v-12)+28)}
    assert all(eq.is_zero() for eq in eqs.values())
    expressions={'D_positive':D,'c_positive':c,'c_lt_4_over_3':RF(F(4,3))-c,
        'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
        'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
        'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
        'gap_positive':delta,'repaired_gap_gt_delta_over_2':G/(24*v),
        'constant_cap':B-(l*(v+7)/6+1),'row1_comparison':B-row1,
        'row2_comparison':B-row2,'root_comparison':(v-2)**2-8*(v-3)}
    records={domain:{name:certificate(expr,domain) for name,expr in expressions.items()}
        for domain in ('q0','q1','q2plus')}
    tables={domain:terms(shifted(G.n,domain)) for domain in records}
    assert shifted(G.n,'q2plus')[(0,0)]==342 and len(tables['q2plus'])==15
    return {'agent':'six-downset-2','role':'researcher','arithmetic':'Sparse Fraction Q(v,q) coefficient cross-multiplication',
        'domain':'integer q>=0, v>=12, v>=4(q+1), l=v-2-q',
        'quadrants':{'q0':'q=0,v=12+x','q1':'q=1,v=12+x','q2plus':'q=2+y,v=12+4y+x; x,y>=0'},
        'zero_identities':len(eqs),'identity_names':list(eqs),'strict_certificates':records,
        'strict_certificate_count':sum(len(z) for z in records.values()),
        'repaired_H_shifted_coefficients':tables,
        'radical_comparisons':['sqrt2<3/2','sqrt(v)<=v/3 forv>=12',
            'sqrt(v-4)<=(v-4)/2','sqrt((v-3)/2)<(v-2)/4'],
        'boundary_q2v12':{'B':'232','delta':'23','norm_loss':'165/16','repaired_gap_lower_bound':'203/16','stated_gap':'23/2'}}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
