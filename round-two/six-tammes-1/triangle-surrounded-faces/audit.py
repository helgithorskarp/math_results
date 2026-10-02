"""Literal transfer-matrix and polynomial-identity audit.

Imports neither producer nor its polynomial helpers. Dict polynomials,
literal Bernstein basis expansion and reference antiprism Gram entries
give a second exact algorithmic route. Not independent researcher review.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,hashlib

def require(x,m):
    if not x:raise ValueError(m)
def read(p):
    require(isinstance(p,list) and all(type(s) is str for s in p),'rational string coefficient list')
    vals=[F(s) for s in p]
    require(not vals or vals[-1]!=0,'trimmed polynomial')
    return {i:v for i,v in enumerate(vals) if v}
def plus(*ps):
    out={}
    for p in ps:
        for i,v in p.items():out[i]=out.get(i,F(0))+v
    return {i:v for i,v in out.items() if v}
def sc(p,c):return {i:v*c for i,v in p.items() if v*c}
def neg(p):return sc(p,-1)
def times(p,q):
    out={}
    for i,x in p.items():
        for j,y in q.items():out[i+j]=out.get(i+j,F(0))+x*y
    return {i:v for i,v in out.items() if v}
def power(p,n):
    out={0:F(1)}
    for _ in range(n):out=times(out,p)
    return out
Z={};O={0:F(1)};R={1:F(1)}
H={0:F(-2),1:F(2),2:F(1)}
LO,HI=F(2,3),F(3,4)

def residue(p):
    p=p.copy()
    while p and max(p)>=2:
        k=max(p);v=p[k]
        correction={i+k-2:-v*x for i,x in H.items()}
        p=plus(p,correction)
    return p
def evaluate(p,x):return sum((v*x**i for i,v in p.items()),F(0))
def sign(p):
    if not p:return 0
    a=b=F(0)
    for i in range(max(p),-1,-1):
        products=[a*LO,a*HI,b*LO,b*HI]
        a,b=min(products)+p.get(i,0),max(products)+p.get(i,0)
    require(a>0 or b<0,'resolved nonzero closed-band sign')
    return 1 if a>0 else -1
def matmul(a,b):
    return [[plus(*(times(a[i][k],b[k][j]) for k in range(3))) for j in range(3)] for i in range(3)]
I=[[O if i==j else Z for j in range(3)] for i in range(3)]
T3=[[Z,O,Z],[neg(R),plus(R,power(R,2)),plus(power(R,2),neg(O))],
    [neg(O),R,R]]
T4=[[Z,O,Z],[plus(O,neg(power(R,2))),plus(power(R,2),power(R,3)),plus(power(R,3),sc(R,-2))],
    [neg(R),plus(R,power(R,2)),plus(power(R,2),neg(O))]]

def transfer(word):
    m=I
    for n in word:m=matmul(T3 if n==3 else T4,m)
    return m

def verify(data):
    require(data['format']==1 and data['c_band']==['1/2','3/5'] and data['r_band']==['2/3','3/4'],'fixed mathematical domain')
    expected={(q,tuple(3+(mask>>j&1) for j in range(q-1))) for q in (4,5,6) for mask in range(2**(q-1))}
    observed=set();excluded=0;exceptions=0;coefficient_positions=0
    for row in data['records']:
        key=(row['sides'],tuple(row['word']))
        require(key in expected and key not in observed,'complete unique unquotiented word domain')
        observed.add(key)
        matrix=transfer(row['word'])
        gaps=[plus(matrix[1][j],neg(O) if j==0 else Z) for j in range(3)]
        require([read(p) for p in row['gaps']]==gaps,'literal transfer matches every gap coefficient')
        us=[read(p) for p in row['bezout']];require(len(us)==3,'three Bezout multipliers')
        g=read(row['combination'])
        require(bool(g) and plus(*(times(u,p) for u,p in zip(us,gaps)))==g,'complete Bezout polynomial identity')
        exception=key==(6,(3,3,3,3,3))
        require(row['hexagonal_exception'] is exception,'only exact hexagon exception')
        if exception:
            factor=times(times(times(R,plus(R,O)),plus(R,sc(O,2))),H)
            require(g==factor and row['bernstein']==[],'literal factored exceptional closure')
            require(sign(R)>0 and sign(plus(R,O))>0 and sign(plus(R,sc(O,2)))>0,'no removed factor vanishes on closed band')
            exceptions+=1
        else:
            b=[F(s) for s in row['bernstein']];n=max(g)
            require(len(b)==n+1 and (all(x>0 for x in b) or all(x<0 for x in b)),'strict coefficient signs including both endpoints')
            u={0:-LO/(HI-LO),1:1/(HI-LO)}
            v={0:HI/(HI-LO),1:-1/(HI-LO)}
            expanded=plus(*(sc(times(power(u,k),power(v,n-k)),comb(n,k)*b[k]) for k in range(n+1)))
            require(expanded==g,'literal Bernstein basis coefficient identity')
            excluded+=1
        coefficient_positions+=sum(max(p,default=-1)+1 for p in gaps)
    require(observed==expected and excluded==55 and exceptions==1,'entire56-word census')
    hx=data['hexagon'];require(read(hx['root_polynomial'])==H and hx['root_bracket']==['2/3','3/4'],'exact isolated quadratic root')
    require(evaluate(H,LO)<0<evaluate(H,HI) and 2*LO+2>0,'unique bracketed quadratic root')
    c=sc(plus(R,O),F(1,3));require(read(hx['c'])==c,'positive exact cosine')
    require(residue(plus(times(c,c),sc(O,-F(1,3))))==Z,'c^2=1/3')
    require(residue(plus(times(c,plus(sc(O,2),neg(R))),neg(R)))==Z,'c=r/(2-r)')
    ring=[I[0],I[1]];outer=[I[2]]
    m=I
    for _ in range(5):
        m=matmul(T3,m);ring.append([residue(p) for p in m[1]]);outer.append([residue(p) for p in m[2]])
    require(ring[-1]==I[0],'sixth boundary vertex closes first')
    points=ring[:-1]+outer
    require([[read(p) for p in v] for v in hx['vectors']]==points and len(points)==12,'all twelve coefficient vectors independently reconstructed')
    def inner(x,y):
        return residue(plus(*(times(times(x[i],y[j]),O if i==j else c) for i in range(3) for j in range(3))))
    W=[O,c,plus(sc(c,3),sc(O,-2)),plus(sc(c,4),sc(O,-3))]
    B=[c,c,plus(O,sc(c,-2)),plus(sc(O,2),sc(c,-5)),plus(sc(O,2),sc(c,-5)),plus(O,sc(c,-2))]
    positions=0;contact_pairs=0;strict_pairs=0
    require(len(hx['gram'])==12 and all(len(row)==12 for row in hx['gram']),'full12x12 Gram shape')
    for i in range(12):
        for j in range(12):
            actual=inner(points[i],points[j])
            if (i<6)==(j<6):
                k=(i-j)%6;reference=W[min(k,6-k)]
            else:
                upper,lower=(i,j-6) if i<6 else (j,i-6)
                reference=B[(upper-lower)%6]
            require(actual==residue(reference)==read(hx['gram'][i][j]),'every reference Gram entry')
            if i==j:require(actual==O,'exact unit norm')
            if i<j:
                s=sign(plus(c,neg(actual)))
                require(s>=0,'different-point separation')
                if s:strict_pairs+=1
                else:contact_pairs+=1
            positions+=1
    require(contact_pairs==24 and strict_pairs==42,'12 distinct physical points and24 antiprism contacts')
    closed=matmul(T3,m)
    require([[residue(p) for p in row] for row in closed]==I==[[read(p) for p in row] for row in hx['closed_three_fan_state']],'full state return closes all six three-fans')
    changed=matmul(T4,m)
    gap=[residue(plus(changed[1][j],neg(O) if j==1 else Z)) for j in range(3)]
    require(gap==[read(p) for p in hx['four_fan_final_corner_gap']] and gap[2]==neg(O),'four-fan final corner has a constant nonzero coordinate gap')
    cap=data['cap'];rho=F(cap['rho']);require(rho==F(9,10),'fixed polar cap')
    equalities={'c_lower_squared_gap':F(1,3)-F(73,128)**2,
        'c_upper_squared_gap':F(3,5)**2-F(1,3),
        'a_squared_lower_gap':F(3,2)*(1-F(3,5))-F(3,4)**2,
        'b_squared_lower_gap':2*F(73,128)-1-F(3,8)**2,
        'chord_at_rho_coefficient_gap':12-13*rho,
        'ring_dot_lower':F(3,4)-rho/8,
        'ring_dot_gap_above_band':F(3,4)-rho/8-F(3,5),
        'same_cap_dot_lower':2*rho*rho-1,
        'same_cap_dot_gap_above_band':2*rho*rho-1-F(3,5)}
    for name,value in equalities.items():
        require(F(cap[name])==value and (value>=0 if name=='b_squared_lower_gap' else value>0),'exact strict cap arithmetic '+name)
    require(read(cap['chord_squared_gap_polynomial'])=={1:F(4,3),2:F(-13,9)} and cap['horizontal_sqrt_chord']=='1-2*q/3','literal horizontal chord identity')
    require(cap['capacity_each_pole_cap']==1 and cap['additional_points_at_most']==2 and cap['total_points_at_most']==14,'capacity conclusion')
    return {'cases':56,'exclusions':excluded,'hexagonal_exception':exceptions,
            'closure_coefficient_positions':coefficient_positions,'hexagon_Gram_positions':positions,
            'hexagon_contacts':contact_pairs,'hexagon_strict_pair_gaps':strict_pairs,'point_bound':14}

if __name__=='__main__':
    raw=Path(__file__).with_name('CERTIFICATE.json').read_bytes();data=json.loads(raw)
    out=verify(data);out['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(out,sort_keys=True))
