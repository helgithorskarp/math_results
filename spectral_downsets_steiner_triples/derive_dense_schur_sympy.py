"""Independent exact CAS reproduction of the dense Sylvester certificate.

SymPy1.14.0 polynomial ring QQ[v,q,x,y]; rational identity numerators
are expanded without GCD. No author arithmetic is imported. One thread.
The portable checker needs no CAS. six-downset-2, researcher.
"""
import argparse
import json
from pathlib import Path
from hashlib import sha256
import sympy as S
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
assert S.__version__=='1.14.0'
R,v,q,x,y=ring('v,q,x,y',QQ);l=v-2-q
r=l*(v-1)/2;s=v+r
F2,F3,F4=v-2,v-3,v-4
D=l*(v*v-10*v+27)-6
T=(v-1)*(l*F3-6);C=3*v*v-3*(l+3)*v+11*l;U=v*v-v-4
prod=(v-1)*F2*F3
A=12*v+6*v*v*(v-1)+2*v*l*(v-1)*F3
H=A-3*prod
X1=D*(H-4*v*l)-6*q*(q-1)*v*v*T
X2=H*F2*F3-4*v*C
X3=D*H-12*v*T*(v-5)
P12=2*(v+2)*F4*F3+U*q*(v+7)
P13=D*(2*l+v-3)+2*T*q*F2
P23=U*(v+5)
M1=X1
M2=4*X1*X2*F4**2*F3-9*v*v*D*F2*P12**2
M3=(4*X1*X2*X3*F4**2*F3-9*v*v*D*F4**2*F2*X1*P23**2
    -144*v*v*F4**2*F3*X2*P13**2-9*v*v*D*F2*X3*P12**2
    -108*v**3*D*F4*F2*P12*P13*P23)
Lw=6*F2*F4*F3;Lh=2*F3*D
expressions={
 'lambda_gt6':(l-6,R.one),'D_positive':(D,R.one),'c_positive':(C,3*F2*F3),
 'd_positive':(U,F4*F3),'t_gt_1':(T-D,D),
 'd_minus_w_gt_minus1':(Lw*(1-s)+2*C*F4*F3+6*F2*(r-2*l+1)*U,Lw),
 'd_minus_w_lt1':(Lw*(1+s)-2*C*F4*F3-6*F2*(r-2*l+1)*U,Lw),
 'three_t_minus_h_gt_minus2':(Lh*(2-s)+2*D*U+2*F3*(r-3*l+3)*T,Lh),
 'three_t_minus_h_lt2':(Lh*(2+s)-2*D*U-2*F3*(r-3*l+3)*T,Lh),
 'constant_below_s':(3*(v-1)+l*(v-5),R(3)),
 'Sylvester1':(M1,12*v*D),
 'Sylvester2':(M2,576*v*v*D*F4**2*F3**2*F2),
 'Sylvester3':(M3,6912*v**3*D**2*F4**2*F3**2*F2)}
domains={**{'q'+str(i):(12,0,i,0)for i in range(4)},
 'q4mod3':(13,7,4,3),'q5mod3':(15,7,5,3),'q6mod3':(18,7,6,3)}
def shifted(p,domain):
    a,b,c,d=domains[domain]
    z=p.compose({v:a+x+b*y,q:c+d*y})
    assert all(i==j==0 for i,j,_,_ in z)
    return [[i,j,str(c)]for(_,_,i,j),c in sorted(z.items())if c]
def cert(pair,domain):
    out={};lists=[]
    for label,p in zip(('num','den'),pair):
        table=shifted(p,domain)
        constant=next((c for i,j,c in table if i==j==0),'0')
        assert S.Rational(constant)>0 and all(S.Rational(c)>=0 for i,j,c in table)
        out[label]={'constant':constant,'term_count':len(table)};lists.append(table)
    out['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return out


def identities():
    V,Q=S.symbols('v q');L=V-2-Q
    rr=L*(V-1)/2;ss=V+rr
    NN=1+V+V*(V-1)/2+L*V*(V-1)/6
    DD=L*(V*V-10*V+27)-6
    tt=(V-1)*(L*(V-3)-6)/DD
    cc=(V*V-(L+3)*V+S.Rational(11,3)*L)/((V-2)*(V-3))
    dd=(V*V-V-4)/((V-4)*(V-3))
    ww=ss-(V-3)*cc-(rr-2*L)*dd
    hh=ss-(V-4)*dd-(rr-3*L)*tt
    tau=NN-(V-1)*(V-2)*(V-3)/(4*V)
    aa=tau-ss-L/3-tt*Q*(Q-1)*V/2
    bb=tau-ss-cc;zz=tau-ss-tt*(V-5)
    pp=(V+2)/4+dd*Q*(V+7)/8
    gg=L+(V-3)/2+tt*Q*(V-2)
    ff=dd*(V-4)*(V+5)/8
    exprs={
        'C11_cleared':aa*(12*v*D).as_expr()-X1.as_expr(),
        'C22_cleared':bb*(12*v*F2*F3).as_expr()-X2.as_expr(),
        'C33_cleared':zz*(12*v*D).as_expr()-X3.as_expr(),
        'cross12_cleared':pp*(8*F4*F3).as_expr()-P12.as_expr(),
        'cross13_cleared':gg*(2*D).as_expr()-P13.as_expr(),
        'cross23_cleared':ff*(8*F3).as_expr()-P23.as_expr(),
        'Sylvester2_cleared':(aa*bb-pp*pp)*expressions['Sylvester2'][1].as_expr()-M2.as_expr(),
        'Sylvester3_cleared':(aa*bb*zz-aa*ff*ff-bb*gg*gg-zz*pp*pp-2*pp*gg*ff)*expressions['Sylvester3'][1].as_expr()-M3.as_expr(),
        'point_radical_square':(V+2)**2-16*(V-2)-(V-6)**2,
        'completion_radical_square':(V+7)**2-32*(V-1)-(V-9)**2,
        'pair_triple_radical_square':(V+5)**2-16*(2*V-6)-(V-11)**2,
        'completion_triple_radical_square':(V-2)**2-(V-1)*(V-3)-1,
        'Bl_AMGM_square':(L+(V-3)/2)**2-2*L*(V-3)-(L-(V-3)/2)**2,
        'constant_below_s':ss-(L*(V+7)/6+1)-(V-1+L*(V-5)/3),
        **{name+'_cleared':actual*expressions[name][1].as_expr()-expressions[name][0].as_expr()
            for name,actual in [('d_minus_w_gt_minus1',1+dd-ww),('d_minus_w_lt1',1-dd+ww),
                ('three_t_minus_h_gt_minus2',2+3*tt-hh),('three_t_minus_h_lt2',2-3*tt+hh)]},
        'tau_minus_s_cleared':(tau-ss)*12*V-H.as_expr()}
    for name,z in exprs.items():
        numerator=S.fraction(S.together(z))[0]
        assert S.expand(numerator)==0,name
    return list(exprs)


def run():
    names=identities()
    records={domain:{name:cert(z,domain)for name,z in expressions.items()}for domain in domains}
    boundaries={}
    for vv,qq in [(13,4),(15,5),(18,6),(17,6)]:
        name='q'+str(qq)+'v'+str(vv)
        boundaries[name]={}
        for key,pair in expressions.items():
            nn,dd=[p.compose({v:R(vv),q:R(qq)}).get((0,0,0,0),QQ.zero)for p in pair]
            boundaries[name][key]=str(nn/dd)
    return {'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0 QQ polynomial ring',
        'domain':'integer q>=0,v>=12,3v>=7q+10,l=v-2-q',
        'affine_domains':{name:list(z)for name,z in domains.items()},
        'zero_identities':len(names),'identity_names':names,
        'strict_certificates':records,'strict_certificate_count':sum(len(z)for z in records.values()),
        'boundaries':boundaries,
        'interpretation':'Exact denominator-clearing identities and positive coefficient certificates; ordinary full-mode bridge in DENSE_SCHUR_CAP.md.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('dense_schur_symbolic.json')
    if args.check:assert out==json.loads(path.read_text())
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
