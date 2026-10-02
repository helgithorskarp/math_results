"""Exact triangle-fan closure, Bezout/sign witnesses, and hexagon core.

Actual author six-tammes-1, researcher. Written physical-face bridge is
in PROOF.md. No floating-point arithmetic, solver or imported peer helper.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse,json,hashlib
from poly import add,sub,mul,scale,divrem,bernstein

R=[Q(0),Q(1)];O=[Q(1)];Z=[]
H=[Q(-2),Q(2),Q(1)]
LO,HI=Q(2,3),Q(3,4)
P0=(O,Z,Z);P1=(Z,O,Z);A0=(Z,Z,O)

def require(x,m):
    if not x:raise ValueError(m)

def xgcd(a,b):
    s0,s1,t0,t1=O,Z,Z,O
    while b:
        q,rem=divrem(a,b)
        a,b=b,rem;s0,s1=s1,sub(s0,mul(q,s1));t0,t1=t1,sub(t0,mul(q,t1))
    if not a:return Z,Z,Z
    v=1/a[-1]
    return scale(a,v),scale(s0,v),scale(t0,v)

def bezout(gaps):
    g=Z;us=[Z,Z,Z]
    for i,p in enumerate(gaps):
        g,s,t=xgcd(g,p)
        us=[mul(s,u) for u in us];us[i]=add(us[i],t)
    require(sum_polys(mul(u,p) for u,p in zip(us,gaps))==g,'literal Bezout reconstruction')
    return g,us

def sum_polys(ps):
    out=Z
    for p in ps:out=add(out,p)
    return out

def reflect(center,now,before):
    return tuple(sub(mul(R,add(x,y)),z) for x,y,z in zip(center,now,before))

def fan(previous,current,outside,m):
    before,now=previous,outside
    for _ in range(m-1):before,now=now,reflect(current,now,before)
    return current,now,before

def closure(word):
    state=P0,P1,A0
    for m in word:state=fan(*state,m)
    return tuple(sub(x,y) for x,y in zip(state[1],P0))

def enc(p):return [str(x) for x in p]
def vec(v):return [enc(p) for p in v]
def mod(p):return divrem(p,H)[1]
def plus(a,b):return mod(add(a,b))
def times(a,b):return mod(mul(a,b))
C=scale(add(R,O),Q(1,3))

def dot(a,b):
    return plus(times(sub(O,C),sum_polys(times(x,y) for x,y in zip(a,b))),
                times(C,times(sum_polys(a),sum_polys(b))))

def hexagon():
    ring=[P0,P1];outside=[A0];state=P0,P1,A0
    for _ in range(5):
        state=fan(*state,3)
        ring.append(tuple(mod(p) for p in state[1]))
        outside.append(tuple(mod(p) for p in state[2]))
    require(ring[-1]==P0,'hexagonal closure')
    ring=ring[:-1];points=ring+outside
    require(len(points)==12,'12 reference points')
    require(mod(sub(times(C,C),[Q(1,3)]))==Z,'c^2=1/3')
    require(mod(sub(mul(C,sub([Q(2)],R)),R))==Z,'c=r/(2-r)')
    gram=[[dot(x,y) for y in points] for x in points]
    within=(O,C,sub(scale(C,3),[Q(2)]),sub(scale(C,4),[Q(3)]))
    cross=(C,C,sub(O,scale(C,2)),sub([Q(2)],scale(C,5)),sub([Q(2)],scale(C,5)),sub(O,scale(C,2)))
    for i in range(12):
        for j in range(12):
            if (i<6)==(j<6):
                k=(i-j)%6;expected=within[min(k,6-k)]
            else:
                upper,lower=(i,j-6) if i<6 else (j,i-6)
                expected=cross[(upper-lower)%6]
            require(gram[i][j]==mod(expected),'literal reference antiprism Gram match')
    state=P0,P1,A0
    for _ in range(6):state=fan(*state,3)
    require(tuple(tuple(mod(p) for p in v) for v in state)==(P0,P1,A0),'entire closed3-fan state returns')
    state=P0,P1,A0
    for _ in range(5):state=fan(*state,3)
    changed=fan(*state,4)
    corner4_gap=tuple(mod(sub(x,y)) for x,y in zip(changed[1],P1))
    require(any(corner4_gap),'four triangles at final corner do not close')
    return {'root_polynomial':enc(H),'root_bracket':['2/3','3/4'],'c':enc(C),
            'vectors':[vec(p) for p in points],'gram':[[enc(p) for p in row] for row in gram],
            'closed_three_fan_state':[vec(p) for p in (P0,P1,A0)],
            'four_fan_final_corner_gap':vec(corner4_gap)}

def certificate():
    rows=[]
    for sides in (4,5,6):
        for word in product((3,4),repeat=sides-1):
            gaps=closure(word);g,us=bezout(gaps)
            exception=sides==6 and word==(3,3,3,3,3)
            coefficients=[] if exception else bernstein(g,LO,HI)
            require(exception or all(x>0 for x in coefficients) or all(x<0 for x in coefficients),'strict whole-band closure exclusion')
            rows.append({'sides':sides,'word':list(word),'gaps':vec(gaps),'bezout':vec(us),
                         'combination':enc(g),'bernstein':enc(coefficients),'hexagonal_exception':exception})
    cap={'c_lower_squared_gap':str(Q(1,3)-Q(73,128)**2),
         'c_upper_squared_gap':str(Q(3,5)**2-Q(1,3)),
         'a_squared_lower_gap':str(Q(3,2)*(1-Q(3,5))-Q(3,4)**2),
         'b_squared_lower_gap':str(2*Q(73,128)-1-Q(3,8)**2),
         'rho':'9/10','horizontal_sqrt_chord':'1-2*q/3',
         'chord_squared_gap_polynomial':['0','4/3','-13/9'],
         'chord_at_rho_coefficient_gap':str(12-13*Q(9,10)),
         'ring_dot_lower':str(Q(3,4)-Q(9,10)/8),
         'ring_dot_gap_above_band':str(Q(3,4)-Q(9,10)/8-Q(3,5)),
         'same_cap_dot_lower':str(2*Q(9,10)**2-1),
         'same_cap_dot_gap_above_band':str(2*Q(9,10)**2-1-Q(3,5)),
         'capacity_each_pole_cap':1,'additional_points_at_most':2,'total_points_at_most':14}
    return {'format':1,'actual_agent':'six-tammes-1','role':'researcher','c_band':['1/2','3/5'],
            'r_band':['2/3','3/4'],'records':rows,'hexagon':hexagon(),'cap':cap}

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',type=Path);args=p.parse_args()
    data=certificate();raw=json.dumps(data,sort_keys=True,separators=(',',':'))+'\n'
    if args.emit:args.emit.write_text(raw)
    else:require(Path(__file__).with_name('CERTIFICATE.json').read_text()==raw,'included certificate regeneration')
    print(json.dumps({'cases':56,'strict_full_band_exclusions':55,'hexagonal_exception':1,
                     'reference_unit_points':12,'total_point_bound':14,
                     'certificate_sha256':hashlib.sha256(raw.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
