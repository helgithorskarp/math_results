"""Portable exact direct-completion cap certificates, v>=3l+8,l>=2.

Sparse Fraction identities, then integer binomial substitution
v=14+x+3y,l=2+y, x,y>=0. No sampling, GCD, solver or CAS.
All sign coefficients are regenerated before comparison with hashes.
six-downset-2, researcher.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from math import comb
from bivariate_certificates import RF


@lru_cache(None)
def monomial(pv,pl):
    out={}
    for i in range(pv+1):
        for j in range(pv-i+1):
            for h in range(pl+1):
                z=comb(pv,i)*comb(pv-i,j)*14**(pv-i-j)*3**j*comb(pl,h)*2**(pl-h)
                key=(i,j+h);out[key]=out.get(key,0)+z
    return tuple(out.items())


def shifted(p):
    out={}
    for(i,j),c in p.items():
        assert c.denominator==1;c=c.numerator
        for key,z in monomial(i,j):out[key]=out.get(key,0)+c*z
    return {p:c for p,c in out.items()if c}


def certificate(pair):
    lists=[];out={}
    for label,p in zip(('num','den'),pair):
        assert p.d=={(0,0):F(1)}
        z=shifted(p.n);assert z.get((0,0),0)>0 and all(c>=0 for c in z.values())
        lists.append([[i,j,str(c)]for(i,j),c in sorted(z.items())])
        out[label]={'constant':str(z[(0,0)]),'term_count':len(z)}
    out['coefficient_sha256']=sha256(json.dumps(lists,separators=(',',':')).encode()).hexdigest()
    return out


def run():
    v,l=RF({(1,0):1}),RF({(0,1):1})
    r=l*(v-1)/2;s=v+r;m=v*(v-1)/2;b=l*v*(v-1)/6;N=1+v+m+b
    F2,F3,F4=v-2,v-3,v-4
    D=l*(v*v-10*v+27)-6;C=3*v*v-3*(l+3)*v+11*l
    U=v*v-v-4;T=(v-1)*(l*F3-6)
    W=l*v*v+11*l*v-36*l+3*v**3-21*v*v+36*v
    H=3*l*l*v*v-12*l*l*v+9*l*l+l*v**3-12*l*v*v+11*l*v+36*l+12*v-24
    Lw=3*F4*F3*F2;Lh=F3*D
    c=C/(3*F2*F3);d=U/(F4*F3);t=T/D
    w=s-F3*c-(r-2*l)*d;h=s-F4*d-(r-3*l)*t
    den=24*v*D*F2*F3*F4
    base=den*(N-s)-6*D*F2*F3*F4*(v-1)*F2*F3
    cross12=2*v*D*W*(v+2)+3*v*D*F2*U*l*(v+7)
    cross13=6*v*F2*F4*H*(2*l+v-3)+6*v*F2*F3*F4*T*(l-1)*(6*l+v-1)
    cross23=3*v*D*F2*F4*U*(v+5)
    gaps=[base-8*v*D*F2*F3*F4*l-12*v*v*F2*F3*F4*T*l*(l-1)-cross12-cross13,
          base-8*v*D*F4*C-cross12-cross23,
          base-24*v*F2*F3*F4*T*(v-5)-cross13-cross23]
    a12=w*(v+2)/4+d*l*(v+7)/8
    a13=h*(2*l+v-3)/4+t*(l-1)*(6*l+v-1)/4
    a23=d*F4*(v+5)/8
    rows=[s+l/3+t*l*(l-1)*v/2+a12+a13,
          s+c+a12+a23,s+t*(v-5)+a13+a23]
    g=(v-1)*F2*F3/(4*v)
    alpha=l*(v+7)/6+1
    eqs={'w_cleared':w*Lw-W,'h_cleared':h*Lh-H,
        **{'row'+str(i+1)+'_gap_cleared':(N-row-g)*den-p for i,(row,p)in enumerate(zip(rows,gaps))},
        'point_radical_square':(v+2)**2-16*F2-(v-6)**2,
        'completion_radical_square':(v+7)**2-32*(v-1)-(v-9)**2,
        'B_AMGM_square':(2*l+v-3)**2-8*l*F3-(2*l-v+3)**2,
        'H_AMGM_square':(6*l+v-1)**2-24*l*(v-1)-(6*l-v+1)**2,
        'pair_triple_radical_square':(v+5)**2-16*(2*v-6)-(v-11)**2,
        'constant_gap':s-alpha-(v-1+l*(v-5)/3)}
    assert all(z.is_zero()for z in eqs.values())
    certs={'D_positive':(D,RF(1)),'c_positive':(C,3*F2*F3),
        'd_positive':(U,F4*F3),'t_positive':(T,D),
        'w_positive':(W,Lw),'h_positive':(H,Lh),
        'constant_below_s':(3*(v-1)+l*(v-5),RF(3)),
        **{'row'+str(i+1)+'_gap_gt_g':(p,den)for i,p in enumerate(gaps)}}
    records={name:certificate(pair)for name,pair in certs.items()}
    return {'agent':'six-downset-2','role':'researcher',
        'domain':'l>=2,v>=3l+8; v=14+x+3y,l=2+y,x,y>=0',
        'zero_identities':len(eqs),'identity_names':list(eqs),
        'strict_certificates':records,'strict_certificate_count':len(records),
        'cleared_gap_degrees':[max(i+j for i,j in p.n)for p in gaps],
        'arithmetic':'Sparse Fraction rational identities and integer binomial composition',
        'interpretation':'Exact scalar signs; ordinary complete-mode incidence/norm bridge in SPARSE_COMPLETION_CAP.md.'}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
