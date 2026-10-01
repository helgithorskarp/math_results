"""Independent exact CAS signs for the maximum-row cap.

SymPy1.14.0, one thread. Rational cancellation and affine substitution
are independent of the portable Fraction backend. The common +/-
orientation is chosen exactly; all coefficients then prove strict signs.
six-downset-2, researcher.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sympy as S
assert S.__version__=='1.14.0'
v,q,x,y=S.symbols('v q x y');l=v-2-q
r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b;k=(v-2)*(v-3)/2
D=l*(v*v-10*v+27)-6
c=(v*v-(l+3)*v+S.Rational(11,3)*l)/((v-2)*(v-3))
d=(v*v-v-4)/((v-4)*(v-3));t=(v-1)*(l*(v-3)-6)/D
w=s-(v-3)*c-(r-2*l)*d;h=s-(v-4)*d-(r-3*l)*t
u=q*(q-1)/2
rows=[s+l/3+t*u*v+v/3+q*v/2+(S.Rational(3,2)+2*q)*v,
    s+S.Rational(4,3)+v/3+q*v/2+v*(v-4)/2,
    s+v*v/2+(2*q+S.Rational(3,2))*v-10]
A=12*v+6*v*v*(v-1)+2*v*l*(v-1)*(v-3);prod=(v-1)*(v-2)*(v-3)
polynomials=[D*(A-4*v*l-(22+30*q)*v*v-3*prod)-6*q*(q-1)*v*v*(v-1)*(l*(v-3)-6),
    A-16*v-(4+6*q)*v*v-6*v*v*(v-4)-3*prod,
    A-6*v*v*v-(24*q+18)*v*v+120*v-3*prod]
rq,uq=q*(v-1)/2,q*(q-1)/2;ul=l*(l-1)/2
eqs={
    **{'row'+str(i)+'_repair_margin_polynomial':N-R-m*k/v**2-G/(12*v*(D if i==1 else 1))
        for i,(R,G)in enumerate(zip(rows,polynomials),1)},
    'constant_below_s':s-(l*(v+7)/6+1)-(v-1+l*(v-5)/3),
    'complement_variance':(r-ul)-(rq-uq)-(l-q),
    'completion_Z_bound':q*rq-(rq-uq)-uq*v,
    'root_square_difference':(v-2)**2-8*(v-3)-(v*(v-12)+28)}
assert all(S.cancel(z)==0 for z in eqs.values())
domains={'q0':(12+x,S.Integer(0)),'q1':(12+x,S.Integer(1)),
    'q2':(12+x,S.Integer(2)),'q4':(15+x,S.Integer(4)),
    'odd3plus':(13+5*y+x,3+2*y),'even6plus':(20+5*y+x,6+2*y)}
expressions={
    'D_positive':D,'c_positive':c,'c_lt_4_over_3':S.Rational(4,3)-c,
    'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
    'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
    'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
    'root_comparison':(v-2)**2-8*(v-3),
    'constant_below_s':s-(l*(v+7)/6+1),
    **{'row'+str(i)+'_repair_half_margin':N-R-m*k/v**2 for i,R in enumerate(rows,1)}}


def shifted(p,domain):
    vv,qq=domains[domain]
    return S.Poly(S.expand(p.subs({v:vv,q:qq},simultaneous=True)),x,y)


def cert(expr,domain):
    n,d=S.fraction(S.cancel(expr));base=shifted(d,domain).coeff_monomial(1);assert base!=0
    sign=1 if base>0 else -1;record={'exact_orientation_sign':sign};lists=[]
    for label,p in [('num',sign*n),('den',sign*d)]:
        p=shifted(p,domain);constant=p.coeff_monomial(1)
        assert constant>0 and all(z>=0 for z in p.coeffs())
        terms=[[i,j,str(z)]for(i,j),z in sorted(p.terms())if z];lists.append(terms)
        record[label]={'term_count':len(terms),'constant':str(constant)}
    record['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return record


def run():
    records={domain:{name:cert(z,domain)for name,z in expressions.items()}for domain in domains}
    tables={}
    for domain in domains:
        tables[domain]={}
        for i,G in enumerate(polynomials,1):
            p=shifted(G,domain);assert p.coeff_monomial(1)>0 and all(z>=0 for z in p.coeffs())
            tables[domain]['G'+str(i)]=[[a,b,str(z)]for(a,b),z in sorted(p.terms())if z]
    boundaries={}
    for name,vv,qq in [('boundary_q3v13',13,3),('boundary_q4v15',15,4)]:
        R=[S.cancel(z.subs({v:vv,q:qq}))for z in rows];NN=N.subs({v:vv,q:qq});BB=max(R)
        values={'N':NN,'s':s.subs({v:vv,q:qq}),**{'R'+str(i):z for i,z in enumerate(R,1)},
            'B':BB,'delta':NN-BB,'twice_norm_loss':(m*k/v**2).subs({v:vv,q:qq}),
            'twice_half_gap_margin':NN-BB-(m*k/v**2).subs({v:vv,q:qq}),
            'half_gap_margin':(NN-BB-(m*k/v**2).subs({v:vv,q:qq}))/2}
        boundaries[name]={key:str(S.cancel(z))for key,z in values.items()}
    return {'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0',
        'domain':'integer q>=0,v>=12,2v>=5q+10,l=v-2-q',
        'zero_identities':len(eqs),'identity_names':list(eqs),
        'strict_certificate_count':sum(len(z)for z in records.values()),'records':records,
        'repair_margin_shifted_polynomials':tables,**boundaries,
        'status':'Exact scalar signs; ordinary incidence/norm interpretation in DENSE_ROW_CAP.md.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('dense_row_symbolic.json')
    if args.check:assert out==json.loads(path.read_text())
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
