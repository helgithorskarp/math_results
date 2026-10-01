"""Optional independent exact CAS certificate for the dense upper cap.

SymPy1.14.0, one thread, no floating arithmetic. The portable checker
needs no CAS. A base evaluation chooses a common exact +/- orientation;
both entire shifted coefficient lists must then prove positivity.
Author: six-downset-2, researcher.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sympy as S
assert S.__version__=='1.14.0'
v,q=S.symbols('v q');x,y=S.symbols('x y');l=v-2-q
r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b;k=(v-2)*(v-3)/2
D=l*(v*v-10*v+27)-6
c=(v*v-(l+3)*v+S.Rational(11,3)*l)/((v-2)*(v-3))
d=(v*v-v-4)/((v-4)*(v-3));t=(v-1)*(l*(v-3)-6)/D
w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*t
B=s+v*v/2+(q*q+2*q+S.Rational(3,2))*v-10
delta=N-B;gamma=delta-m*k/(2*v*v)
H=132*v-12*v*v*(q*q+2*q+2)+2*v*(v-q-2)*(v-1)*(v-3)-3*(v-1)*(v-2)*(v-3)
row1=s+(q*q+S.Rational(3,2)*q+S.Rational(13,6))*v
row2=s+S.Rational(4,3)+v/3+q*v/2+v*(v-4)/2
row3=s+v*v/2+(2*q+S.Rational(3,2))*v-10
rq,uq=q*(v-1)/2,q*(q-1)/2;ul=l*(l-1)/2
eqs={
 'delta_polynomial':delta-(66-6*v*(q*q+2*q+2)+(v-q-2)*(v-1)*(v-3))/6,
 'repair_margin_polynomial':gamma-delta/2-H/(24*v),
 'row1_difference':B-row1-(v*v/2+(q/2-S.Rational(2,3))*v-10),
 'row2_difference':B-row2-(q*q*v+(S.Rational(3,2)*q+S.Rational(19,6))*v-S.Rational(4,3)-10),
 'row3_difference':B-row3-q*q*v,
 'constant_difference':B-(l*(v+7)/6+1)-(B-s+v-1+l*(v-5)/3),
 'complement_variance':(r-ul)-(rq-uq)-(l-q),
 'completion_Z_bound':q*rq-(rq-uq)-uq*v,
 'root_square_difference':(v-2)**2-8*(v-3)-(v*(v-12)+28)}
assert all(S.cancel(z)==0 for z in eqs.values())
expressions={
 'D_positive':D,'c_positive':c,'c_lt_4_over_3':S.Rational(4,3)-c,
 'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
 'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
 'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
 'gap_positive':delta,'repaired_gap_gt_delta_over_2':H/(24*v),
 'constant_cap':B-(l*(v+7)/6+1),'row1_comparison':B-row1,
 'row2_comparison':B-row2,'root_comparison':(v-2)**2-8*(v-3)}


def shifted(p,domain):
    if domain in ('q0','q1'):p=p.subs({q:int(domain[1:]),v:12+x})
    else:p=p.subs(v,4*(q+1)+x).subs(q,2+y)
    return S.Poly(S.expand(p),x,y)


def cert(expr,domain):
    num,den=S.fraction(S.cancel(expr));base_q=int(domain[1:]) if domain in ('q0','q1') else 2
    value=den.subs({v:12,q:base_q});assert value!=0
    sign=1 if value>0 else -1;num,den=sign*num,sign*den
    record={'exact_orientation_sign':sign};lists=[]
    for label,p in [('num',num),('den',den)]:
        p=shifted(p,domain);constant=p.coeff_monomial(1)
        assert constant>0 and all(z>=0 for z in p.coeffs())
        terms=[[i,j,str(z)]for(i,j),z in sorted(p.terms())if z];lists.append(terms)
        record[label]={'term_count':len(terms),'constant':str(constant)}
    record['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return record


def run():
    domains=['q0','q1','q2plus']
    records={domain:{name:cert(z,domain)for name,z in expressions.items()}for domain in domains}
    tables={}
    for domain in domains:
        p=shifted(H,domain);assert p.coeff_monomial(1)>0 and all(z>=0 for z in p.coeffs())
        tables[domain]=[[i,j,str(z)]for(i,j),z in sorted(p.terms())if z]
    return {'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0',
        'domain':'integer q>=0, v>=12, v>=4(q+1), l=v-2-q',
        'zero_identities':len(eqs),'identity_names':list(eqs),
        'strict_certificate_count':sum(len(z)for z in records.values()),'records':records,
        'repaired_H_shifted_coefficients':tables,
        'boundary_q2v12':{name:str(S.cancel(z.subs({q:2,v:12})))for name,z in {'B':B,'delta':delta,'gamma':gamma}.items()},
        'status':'Exact scalar signs; ordinary norm/completeness interpretation in DENSE_COMPLEMENT_CAP.md.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('dense_lambda_symbolic.json')
    if args.check:assert out==json.loads(path.read_text())
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
