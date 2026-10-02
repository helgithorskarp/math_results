"""Regenerate the compact integer orbit dual from an original PD solve."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import json
import inputs
from literal import core_data,require,action
from exact import digest
from claims import POLY
from field import Q,sign
from schur import phase


def generate():
    upper,X,K,active,Y=phase('upper',raw=True)
    ue=upper['even_odd_blocks'][0];a,b,c=F(ue[0][0]),F(ue[0][1]),F(ue[1][1])
    A,B,C=POLY;disc=B*B-4*A*C
    require(a*c==F(disc,A*A) and b==F(B,A),'exact field polynomial from upper forms')
    xi=Q(0,1);y=[-b-2*xi,-b-2*xi,Q(a),Q(a)]
    n=len(X)-1;w=[Q(0) for _ in range(n)]
    for j,i in enumerate(active):w[i]+=y[j]
    for h,group in enumerate(K):
        value=-sum(Y[h][j]*y[j] for j in range(4))
        for i in group:w[i]+=value
    scale=lcm(*(value.denominator for x in w for value in (x.a,x.b)))
    w=[scale*x for x in w];orbits={}
    for mask,x in zip(X[1:],w):
        key=(int(bool(mask&1)),(mask&6).bit_count(),(mask&56).bit_count(),(mask>>6).bit_count())
        require(x.a.denominator==x.b.denominator==1,'integral affine witness')
        value=[int(x.a),int(x.b)]
        if key in orbits:
            require(orbits[key]['value']==value,'exact original orbit invariance');orbits[key]['count']+=1
        else:orbits[key]={'key':list(key),'count':1,'value':value}
    rows=[orbits[key] for key in sorted(orbits)]
    fixture=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    require(scale==fixture['dual_integer_scale'] and rows==fixture['orbits'],'entire frozen integer orbit dual differs')
    _,N,s,C0,delta,R,U0=core_data(8,3)
    require(all(sum(U0[i][j]*w[j] for j in range(n))-xi*sum(R[i][j]*w[j] for j in range(n))==0 for i in range(n)), 'all original algebraic cap kernel actions')
    quad=lambda T:sum(w[i]*T[i][j]*w[j] for i in range(n) for j in range(n))
    u,d,r=quad(U0),quad(delta),quad(R)
    require(u==xi*r and r==scale*scale*Q(4*a*b,8*a),'original endpoint pairings')
    require(sign(r,'lower')<0 and sign(r,'upper')>0 and sign(d,'lower')>0 and sign(d,'upper')>0,'all original dual orientations')
    ix={mask:i for i,mask in enumerate(X[1:])};outside=sum(delta[ix[8]][j]*w[j] for j in range(n))
    require(outside!=0 and not any(R[ix[8]]),'strict positive-kappa dual boundary obstruction')
    trace_d=2*d.a-F(B,A)*d.b;rho=r.b/2
    require(trace_d>0 and rho>0,'positive rational bound denominators')
    cap=rho*F(disc,A*A)/trace_d
    require(F(1,16)<cap<F(1,14),'exact rational enclosure of necessary kappa bound')
    rec={'q':8,'k':3,'N':N,'polynomial':list(POLY),'integer_scale':scale,'orbit_count':len(rows),'orbits':rows,
         'U0_pairing':u.record(),'Delta_pairing':d.record(),'R_pairing':r.record(),
         'lower_slope':(d/(-r)).record(),'upper_slope':(d/r).record(),
         'outside_Delta_action':outside.record(),'kappa_strict_necessary_bound':str(cap),
         'original_kernel_actions':n,'both_Delta_signs_positive':True,'negative_kappa_lower_alpha':'1071/29'}
    rec['record_sha256']=digest(rec);return rec
if __name__=='__main__':print(json.dumps(generate(),sort_keys=True,indent=2))
