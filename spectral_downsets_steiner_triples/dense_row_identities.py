"""Exact maximum-row cap certificates, without CAS or numerical sampling.

Integer q>=0, v>=12, 2v>=5q+10, l=v-2-q. The six affine domains
cover all integer parameters. Coefficient cross-multiplication supplies
seven identities and 96 strict signs. six-downset-2, researcher.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from bivariate_certificates import RF,poly,terms

# v=v0+x+vy*y, q=q0+qy*y, with x,y>=0. Fixed-q domains use y=0.
DOMAINS={'q0':(12,0,0,0),'q1':(12,0,1,0),'q2':(12,0,2,0),
    'q4':(15,0,4,0),'odd3plus':(13,5,3,2),'even6plus':(20,5,6,2)}


def shifted(p,domain):
    v0,vy,q0,qy=DOMAINS[domain];out={}
    for (pv,pq),c in p.items():
        for i in range(pv+1):
            for j in range(pv-i+1):
                for h in range(pq+1):
                    factor=comb(pv,i)*comb(pv-i,j)*v0**(pv-i-j)*vy**j*comb(pq,h)*q0**(pq-h)*qy**h
                    key=(i,j+h)
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
    u=q*(q-1)/2
    R1=s+l/3+t*u*v+v/3+q*v/2+(F(3,2)+2*q)*v
    R2=s+F(4,3)+v/3+q*v/2+v*(v-4)/2
    R3=s+v*v/2+(2*q+F(3,2))*v-10
    A=12*v+6*v*v*(v-1)+2*v*l*(v-1)*(v-3)
    prod=(v-1)*(v-2)*(v-3)
    G1=D*(A-4*v*l-(22+30*q)*v*v-3*prod)-6*q*(q-1)*v*v*(v-1)*(l*(v-3)-6)
    G2=A-16*v-(4+6*q)*v*v-6*v*v*(v-4)-3*prod
    G3=A-6*v*v*v-(24*q+18)*v*v+120*v-3*prod
    rows=[R1,R2,R3];polynomials=[G1,G2,G3]
    rq,uq=q*(v-1)/2,q*(q-1)/2;ul=l*(l-1)/2
    eqs={
        **{'row'+str(i)+'_repair_margin_polynomial':N-R-m*k/(v*v)-G/(12*v*(D if i==1 else 1))
            for i,(R,G) in enumerate(zip(rows,polynomials),1)},
        'constant_below_s':s-(l*(v+7)/6+1)-(v-1+l*(v-5)/3),
        'complement_variance':(r-ul)-(rq-uq)-(l-q),
        'completion_Z_bound':q*rq-(rq-uq)-uq*v,
        'root_square_difference':(v-2)**2-8*(v-3)-(v*(v-12)+28)}
    assert all(z.is_zero() for z in eqs.values())
    expressions={
        'D_positive':D,'c_positive':c,'c_lt_4_over_3':RF(F(4,3))-c,
        'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
        'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
        'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
        'root_comparison':(v-2)**2-8*(v-3),
        'constant_below_s':s-(l*(v+7)/6+1),
        **{'row'+str(i)+'_repair_half_margin':N-R-m*k/(v*v) for i,R in enumerate(rows,1)}}
    records={domain:{name:certificate(z,domain)for name,z in expressions.items()}for domain in DOMAINS}
    tables={domain:{'G'+str(i):terms(shifted(G.n,domain))for i,G in enumerate(polynomials,1)}for domain in DOMAINS}
    for domain in tables:
        for table in tables[domain].values():
            assert any(i==j==0 and F(z)>0 for i,j,z in table)
            assert all(F(z)>=0 for i,j,z in table)
    return {'agent':'six-downset-2','role':'researcher',
        'arithmetic':'Sparse Fraction Q(v,q) coefficient cross-multiplication',
        'domain':'integer q>=0,v>=12,2v>=5q+10,l=v-2-q',
        'affine_domains':{name:{'v0':a,'vy':b,'q0':c,'qy':d}for name,(a,b,c,d)in DOMAINS.items()},
        'zero_identities':len(eqs),'identity_names':list(eqs),
        'strict_certificate_count':sum(len(z)for z in records.values()),
        'strict_certificates':records,'repair_margin_shifted_polynomials':tables,
        'boundary_q3v13':{'N':'300','s':'61','R1':'7289/29','R2':'434/3','R3':'233',
            'B':'7289/29','delta':'1411/29','twice_norm_loss':'330/13','half_gap_margin':'8773/377'},
        'boundary_q4v15':{'N':'436','s':'78','R1':'7589/19','R2':'1181/6','R3':'323',
            'B':'7589/19','delta':'695/19','twice_norm_loss':'182/5','half_gap_margin':'17/95'}}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
