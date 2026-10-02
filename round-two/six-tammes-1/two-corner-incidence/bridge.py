"""Audit the parent facts needed for one unrestricted hexagon corner.

Checks32 partial-closure words and the twelve vectors from FIVE updates.
Never reads either final-corner certificate field. The ordinary physical
bridge and cap argument remain written proof, not formal verification.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
from audit import require,read,plus,scale,neg,times,transfer,matmul,I,T3,R,O,Z,LO,HI,bernstein_identity

H={0:F(-2),1:F(2),2:F(1)}
def residue(p):
    p=p.copy()
    while p and max(p)>=2:
        n=max(p);v=p[n];p=plus(p,{i+n-2:-v*x for i,x in H.items()})
    return p
def at(p,x):return sum((v*x**i for i,v in p.items()),F(0))
def verify(data):
    require(data['c_band']==['1/2','3/5'] and data['r_band']==['2/3','3/4'],'parent closed band')
    domain={tuple(3+(mask>>j&1) for j in range(5)) for mask in range(32)};seen=set();excluded=0
    for row in data['records']:
        if row['sides']!=6:continue
        word=tuple(row['word']);require(word in domain and word not in seen,'full partial hexagon word domain');seen.add(word)
        gaps=[plus(p,neg(O) if j==0 else Z) for j,p in enumerate(transfer(word)[1])]
        require([read(p) for p in row['gaps']]==gaps,'all parent closure coordinates from five updates')
        multipliers=[read(p) for p in row['bezout']];g=read(row['combination'])
        require(len(multipliers)==3 and plus(*(times(u,p) for u,p in zip(multipliers,gaps)))==g and bool(g),'literal parent Bezout identity')
        exception=word==(3,3,3,3,3);require(row['hexagonal_exception'] is exception,'unique parent partial exception')
        if exception:
            expected=times(times(times(R,plus(R,O)),plus(R,scale(O,2))),H)
            require(g==expected and row['bernstein']==[],'exact exceptional factors')
        else:bernstein_identity(g,row['bernstein']);excluded+=1
    require(seen==domain and excluded==31,'all32 partial hexagon cases')
    hx=data['hexagon'];require(read(hx['root_polynomial'])==H and hx['root_bracket']==['2/3','3/4'],'exact hexagon root')
    require(at(H,LO)<0<at(H,HI) and 2*LO+2>0,'unique positive bracketed root')
    c=scale(plus(R,O),F(1,3));require(read(hx['c'])==c,'root cosine')
    require(residue(plus(times(c,c),scale(O,-F(1,3))))==Z,'c squared is1/3')
    require(residue(plus(times(c,plus(scale(O,2),neg(R))),neg(R)))==Z,'actual c=r/(2-r)')
    state=I;ring=[I[0],I[1]];outside=[I[2]]
    for _ in range(5):
        state=matmul(T3,state);ring.append([residue(p) for p in state[1]]);outside.append([residue(p) for p in state[2]])
    require(ring[-1]==I[0],'boundary returns without an update at the free corner')
    points=ring[:-1]+outside
    require(len(points)==12 and [[read(p) for p in v] for v in hx['vectors']]==points,'twelve vectors after only five updates')
    require(len(hx['gram'])==12 and all(len(row)==12 for row in hx['gram']),'full parent Gram shape')
    def inner(x,y):return residue(plus(*(times(times(x[i],y[j]),O if i==j else c) for i in range(3) for j in range(3))))
    contacts=strict=0
    for i in range(12):
        for j in range(12):
            v=inner(points[i],points[j]);require(v==read(hx['gram'][i][j]),'every parent Gram entry from partial reconstruction')
            if i==j:require(v==O,'unit points')
            if i<j:
                gap=plus(c,neg(v));require(max(gap,default=-1)<=1,'linear root-residue gap')
                if gap:require(min(at(gap,LO),at(gap,HI))>0,'strict separated physical core pair');strict+=1
                else:contacts+=1
    require(contacts==24 and strict==42,'twelve distinct points with antiprism pair census')
    cap=data['cap'];rho=F(cap['rho']);require(rho==F(9,10),'exact two-cap threshold')
    scalars={'c_lower_squared_gap':F(1,3)-F(73,128)**2,'c_upper_squared_gap':F(3,5)**2-F(1,3),
             'a_squared_lower_gap':F(3,2)*(1-F(3,5))-F(3,4)**2,
             'b_squared_lower_gap':2*F(73,128)-1-F(3,8)**2,
             'chord_at_rho_coefficient_gap':12-13*rho,'ring_dot_lower':F(3,4)-rho/8,
             'ring_dot_gap_above_band':F(3,4)-rho/8-F(3,5),
             'same_cap_dot_lower':2*rho*rho-1,'same_cap_dot_gap_above_band':2*rho*rho-1-F(3,5)}
    for name,v in scalars.items():require(F(cap[name])==v and (v>=0 if name=='b_squared_lower_gap' else v>0),'exact cap comparison '+name)
    require(read(cap['chord_squared_gap_polynomial'])=={1:F(4,3),2:F(-13,9)} and cap['horizontal_sqrt_chord']=='1-2*q/3','parent ring-coverage comparison')
    require(cap['capacity_each_pole_cap']==1 and cap['additional_points_at_most']==2 and cap['total_points_at_most']==14,'parent capacity bound')
    return {'partial_hexagon_words':32,'partial_hexagon_exclusions':31,'exception':1,
            'actual_corner_updates':5,'final_corner_fields_read':False,'core_points':12,'Gram_positions':144,
            'contacts':contacts,'strict_pair_gaps':strict,'total_point_bound':14}

def load():
    here=Path(__file__).resolve().parent;pins=json.loads((here/'PINS.json').read_text())
    parent=here.parent/'triangle-surrounded-faces'
    for row in pins['parent_files']:
        raw=(parent/row['path']).read_bytes();require(sha256(raw).hexdigest()==row['sha256'] and len(raw)==row['bytes'],'actual immutable parent source bytes')
    return json.loads((parent/'CERTIFICATE.json').read_text())
if __name__=='__main__':print(json.dumps(verify(load()),sort_keys=True))
