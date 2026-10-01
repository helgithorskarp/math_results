"""Independent rational-formula CAS replay of sparse completion caps.

SymPy1.14.0 QQ polynomial ring and literal rational numerator expansion.
No author arithmetic imports; portable verification needs no CAS.
six-downset-2, researcher.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sympy as S
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
assert S.__version__=='1.14.0'
R,v,l,x,y=ring('v,l,x,y',QQ)
r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b
F2,F3,F4=v-2,v-3,v-4
D=l*(v*v-10*v+27)-6;C=3*v*v-3*(l+3)*v+11*l
U=v*v-v-4;T=(v-1)*(l*F3-6)
W=l*v*v+11*l*v-36*l+3*v**3-21*v*v+36*v
H=3*l*l*v*v-12*l*l*v+9*l*l+l*v**3-12*l*v*v+11*l*v+36*l+12*v-24
Lw=3*F4*F3*F2;Lh=F3*D;den=24*v*D*F2*F3*F4
base=den*(N-s)-6*D*F2*F3*F4*(v-1)*F2*F3
cross12=2*v*D*W*(v+2)+3*v*D*F2*U*l*(v+7)
cross13=6*v*F2*F4*H*(2*l+v-3)+6*v*F2*F3*F4*T*(l-1)*(6*l+v-1)
cross23=3*v*D*F2*F4*U*(v+5)
gaps=[base-8*v*D*F2*F3*F4*l-12*v*v*F2*F3*F4*T*l*(l-1)-cross12-cross13,
      base-8*v*D*F4*C-cross12-cross23,
      base-24*v*F2*F3*F4*T*(v-5)-cross13-cross23]
certs={'D_positive':(D,R.one),'c_positive':(C,3*F2*F3),
 'd_positive':(U,F4*F3),'t_positive':(T,D),'w_positive':(W,Lw),
 'h_positive':(H,Lh),'constant_below_s':(3*(v-1)+l*(v-5),R(3)),
 **{'row'+str(i+1)+'_gap_gt_g':(p,den)for i,p in enumerate(gaps)}}


def identities():
    V,L=S.symbols('v l');rr=L*(V-1)/2;ss=V+rr
    nn=1+V+V*(V-1)/2+L*V*(V-1)/6
    DD=L*(V*V-10*V+27)-6
    cc=(V*V-(L+3)*V+S.Rational(11,3)*L)/((V-2)*(V-3))
    dd=(V*V-V-4)/((V-4)*(V-3));tt=(V-1)*(L*(V-3)-6)/DD
    ww=ss-(V-3)*cc-(rr-2*L)*dd;hh=ss-(V-4)*dd-(rr-3*L)*tt
    A12=ww*(V+2)/4+dd*L*(V+7)/8
    A13=hh*(2*L+V-3)/4+tt*(L-1)*(6*L+V-1)/4
    A23=dd*(V-4)*(V+5)/8
    rows=[ss+L/3+tt*L*(L-1)*V/2+A12+A13,ss+cc+A12+A23,ss+tt*(V-5)+A13+A23]
    gg=(V-1)*(V-2)*(V-3)/(4*V)
    eqs={'w_cleared':ww*Lw.as_expr()-W.as_expr(),'h_cleared':hh*Lh.as_expr()-H.as_expr(),
        **{'row'+str(i+1)+'_gap_cleared':(nn-row-gg)*den.as_expr()-p.as_expr()for i,(row,p)in enumerate(zip(rows,gaps))},
        'point_radical_square':(V+2)**2-16*(V-2)-(V-6)**2,
        'completion_radical_square':(V+7)**2-32*(V-1)-(V-9)**2,
        'B_AMGM_square':(2*L+V-3)**2-8*L*(V-3)-(2*L-V+3)**2,
        'H_AMGM_square':(6*L+V-1)**2-24*L*(V-1)-(6*L-V+1)**2,
        'pair_triple_radical_square':(V+5)**2-16*(2*V-6)-(V-11)**2,
        'constant_gap':ss-(L*(V+7)/6+1)-(V-1+L*(V-5)/3)}
    for name,z in eqs.items():assert S.expand(S.fraction(S.together(z))[0])==0,name
    return list(eqs)


def certificate(pair):
    lists=[];out={}
    for label,p in zip(('num','den'),pair):
        z=p.compose({v:14+x+3*y,l:2+y});assert all(i==j==0 for i,j,_,_ in z)
        table=[[i,j,str(c)]for(_,_,i,j),c in sorted(z.items())if c]
        constant=z.get((0,0,0,0),QQ.zero)
        assert constant>0 and all(S.Rational(c)>=0 for i,j,c in table)
        out[label]={'constant':str(constant),'term_count':len(table)};lists.append(table)
    out['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return out


def run():
    names=identities();records={name:certificate(pair)for name,pair in certs.items()}
    boundaries={}
    for vv,ll in ((15,2),(17,3),(21,4),(26,6)):
        zz={v:R(vv),l:R(ll)};dd=den.compose(zz).get((0,0,0,0),QQ.zero)
        margins=[p.compose(zz).get((0,0,0,0),QQ.zero)/dd for p in gaps]
        nn=N.compose(zz).get((0,0,0,0),QQ.zero);gg=QQ((vv-1)*(vv-2)*(vv-3),4*vv)
        rows=[nn-gg-z for z in margins]
        boundaries['v'+str(vv)+'l'+str(ll)]={'N':str(nn),'rows':list(map(str,rows)),
            'B':str(max(rows)),'delta':str(nn-max(rows)),'g':str(gg),'margins':list(map(str,margins))}
    return {'agent':'six-downset-2','role':'researcher','CAS':'SymPy1.14.0 QQ polynomial ring',
        'domain':'l>=2,v>=3l+8; v=14+x+3y,l=2+y,x,y>=0',
        'zero_identities':len(names),'identity_names':names,'strict_certificates':records,
        'strict_certificate_count':len(records),'boundaries':boundaries,
        'interpretation':'Exact scalar certificate; full-mode ordinary bridge in SPARSE_COMPLETION_CAP.md.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('sparse_completion_symbolic.json')
    if args.check:assert out==json.loads(path.read_text())
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
