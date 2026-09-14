#!/usr/bin/env python3
"""Exact algebra controls, reversed-tower event gate, and faulty audit fixtures."""
import argparse,json,subprocess
from fractions import Fraction as F
from itertools import product
from model import Field,ONE,Z,points,inventory,flat_mul,require,add,sub,scale,peel
from verify import literal_coordinates

def reverse(a):return tuple(a[((i&1)<<2)|(i&2)|((i&4)>>2)]for i in range(8))

def main(binary):
    K=Field();basis=[tuple(F(i==j)for i in range(8))for j in range(8)]
    for a in basis:
        for b in basis:require(K.mul(a,b)==flat_mul(a,b),'basis products')
    square_count=0
    for i in range(8):
        for j in range(i+1,8):
            for a,b in product(range(-2,3),repeat=2):
                x=add(scale(basis[i],a),scale(basis[j],b));q=K.mul(x,x);r=K.sqrt(q)
                require(r is not None and flat_mul(r,r)==q,'constructed square');square_count+=1
    P,_=points();_,events,_,ys=inventory(P);L=Field((11,5,3));root_count=0
    for y,r in ys.items():
        q=sub(ONE,flat_mul(y,y));v=L.sqrt(reverse(q))
        require((v is None)==(r is None),'reversed-tower disagreement')
        if v is not None:require(flat_mul(reverse(v),reverse(v))==q,'reversed root');root_count+=1
    # Direct polynomial substitution with flat arithmetic at every returned event.
    root_checks=0
    for t,es in events.items():
        for i,j in es:
            x=scale(sub(P[i][0],P[j][0]),F(1,288));y=scale(sub(P[i][1],P[j][1]),F(1,288))
            u=add(x,flat_mul(t,y))
            require(add(flat_mul(u,u),flat_mul(y,y))==ONE,'flat contact');root_checks+=1
    # A square control is physically bipartite, then explicit corruptions fail.
    small=[((0,)*8,(0,)*8),((288,)+(0,)*7,(0,)*8),((0,)*8,(288,)+(0,)*7),((288,)+(0,)*7,(288,)+(0,)*7)]
    den,Q=literal_coordinates(small,Z);E=[(0,1),(0,2),(1,3),(2,3)]
    def text(Q=Q,E=E,den=den,extra=''):
        return '1\n'+f'{len(Q)} {len(E)} {den}\n'+''.join(' '.join(map(str,p))+'\n'for p in Q)+''.join(f'{a} {b}\n'for a,b in E)+extra
    good=subprocess.run([str(binary)],input=text(),capture_output=True,text=True);require(good.returncode==0,'valid square')
    require(json.loads(good.stdout)['unit_edges']==4,'square edges')
    q=list(Q);q[-1]=q[0]
    bad=[text(E=E[:-1]),text(E=sorted(E+[(0,3)])),text(Q=q),text(den=0),text(extra='junk\n'),text()[:-4],text(E=list(reversed(E)))]
    too_large=list(Q);too_large[0]=(2**50,)+Q[0][1:];bad.append(text(Q=too_large))
    for s in bad:require(subprocess.run([str(binary)],input=s,capture_output=True,text=True).returncode!=0,'corrupt audit accepted')
    # Peeling lower/upper controls: clique K5 requires degeneracy four.
    require(peel(5,[(i,j)for i in range(5)for j in range(i+1,5)])[0]==4,'K5 peeling')
    require(peel(4,E)[0]==2,'square peeling')
    return dict(status='CONTROLS_PASS',basis_products=64,constructed_squares=square_count,
        reversed_tower_discriminants=len(ys),square_discriminants=root_count,
        flat_contact_checks=root_checks,positive_audit_controls=1,corrupt_audit_rejections=len(bad),peeling_controls=2)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--audit-binary',required=True,type=__import__('pathlib').Path);a=ap.parse_args()
    print(json.dumps(main(a.audit_binary.resolve()),indent=2,sort_keys=True))
