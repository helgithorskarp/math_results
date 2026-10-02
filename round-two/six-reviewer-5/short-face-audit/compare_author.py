"""Late independent native-certificate check; imports only the sealed own core."""
import independent as I
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json,sys,hashlib,copy

def poly(p):
    I.need(type(p) is list and all(type(s) is str for s in p),'rational-string polynomial')
    a=I.trim(p or ['0'])
    I.need(not p or Q(p[-1])!=0,'native normalized polynomial')
    return a
def residue(p):
    a=I.divmodp(p,I.trim((-2,2,1)))[1]
    return (a[0],a[1] if len(a)>1 else Q(0))

def verify(d):
    own=I.build();cases={tuple(r['word']):r for r in own['cases']}
    I.need(d['format']==1 and d['c_band']==['1/2','3/5'] and d['r_band']==['2/3','3/4'],'exact closed domain')
    seen=set();positions=0;bernstein_nodes=0
    for row in d['records']:
        word=tuple(row['word']);I.need(word in cases and word not in seen and row['sides']==len(word)+1,'complete unique words')
        seen.add(word);expected=cases[word]
        gaps=[poly(p) for p in row['gaps']]
        I.need(gaps==[I.trim(p) for p in expected['gaps']],'all own interpolated closure coefficients')
        positions+=sum(len(p) if p!=I.ZERO else 0 for p in gaps)
        us=[poly(p) for p in row['bezout']];I.need(len(us)==3,'three Bezout multipliers')
        g=poly(row['combination']);total=I.ZERO
        for u,p in zip(us,gaps):total=I.add(total,I.mul(u,p))
        I.need(g!=I.ZERO and total==g,'literal complete Bezout identity')
        exception=word==(3,3,3,3,3)
        I.need(row['hexagonal_exception'] is exception,'exact sole exception')
        if exception:
            I.need(g==I.mul(I.mul(I.mul((0,1),(1,1)),(2,1)),(-2,2,1)) and row['bernstein']==[],'exception factor identity')
        else:
            n=len(g)-1;b=[Q(x) for x in row['bernstein']]
            I.need(len(b)==n+1 and (all(x>0 for x in b) or all(x<0 for x in b)),'strict Bernstein signs')
            # Equality at n+1 rational points proves the degree-n Bernstein identity.
            for j in range(n+1):
                u=Q(j,n) if n else Q(0);r=Q(2,3)+(Q(3,4)-Q(2,3))*u
                literal=sum((comb(n,k)*b[k]*u**k*(1-u)**(n-k) for k in range(n+1)),Q(0))
                I.need(literal==I.value(g,r),'all Bernstein interpolation positions');bernstein_nodes+=1
    I.need(seen==set(cases),'no missing word')
    hx=d['hexagon'];c=I.trim(hx['c'])
    I.need(poly(hx['root_polynomial'])==I.trim((-2,2,1)) and hx['root_bracket']==['2/3','3/4'],'quadratic root domain')
    I.need(residue(c)==I.C,'cosine field')
    vertices=[tuple(residue(poly(p)) for p in row) for row in hx['vectors']]
    I.need(vertices==[tuple(tuple(Q(s) for s in a) for a in row) for row in own['core']['vertices']],'all12 native vectors match independent reconstruction')
    I.need(len(hx['gram'])==12 and all(len(row)==12 for row in hx['gram']),'144 Gram positions')
    for i in range(12):
        for j in range(12):I.need(residue(poly(hx['gram'][i][j]))==I.dot(vertices[i],vertices[j]),'every native Gram entry')
    I.need([tuple(residue(poly(p)) for p in row) for row in hx['closed_three_fan_state']]==list(I.FE),'six-corner state')
    state=I.FE
    for _ in range(5):state=I.fan_field(3,state)
    changed=I.fan_field(4,state)[1]
    final_gap=tuple(I.fadd(a,I.fneg(b)) for a,b in zip(changed,I.FE[1]))
    I.need(tuple(residue(poly(p)) for p in hx['four_fan_final_corner_gap'])==final_gap,'omitted native four-corner gap')
    cap=d['cap'];rho=Q(cap['rho']);I.need(rho==Q(9,10),'polar radius')
    exact={'c_lower_squared_gap':Q(1,3)-Q(73,128)**2,'c_upper_squared_gap':Q(3,5)**2-Q(1,3),
        'a_squared_lower_gap':Q(3,2)*(1-Q(3,5))-Q(3,4)**2,'b_squared_lower_gap':2*Q(73,128)-1-Q(3,8)**2,
        'chord_at_rho_coefficient_gap':12-13*rho,'ring_dot_lower':Q(3,4)-rho/8,
        'ring_dot_gap_above_band':Q(3,4)-rho/8-Q(3,5),'same_cap_dot_lower':2*rho*rho-1,
        'same_cap_dot_gap_above_band':2*rho*rho-1-Q(3,5)}
    for k,v in exact.items():I.need(Q(cap[k])==v,'every cap rational:'+k)
    I.need(poly(cap['chord_squared_gap_polynomial'])==I.trim((0,Q(4,3),-Q(13,9))) and cap['horizontal_sqrt_chord']=='1-2*q/3','chord identity')
    I.need((cap['capacity_each_pole_cap'],cap['additional_points_at_most'],cap['total_points_at_most'])==(1,2,14),'original nonfacial core capacity')
    return dict(words=len(seen),closure_coefficient_positions=positions,bernstein_evaluation_positions=bernstein_nodes,gram_positions=144,cap_rationals=len(exact),all_native_entries_match=True)

def controls(d):
    changes=[]
    def damage(name,fn):
        a=copy.deepcopy(d);fn(a)
        try:verify(a)
        except (ValueError,KeyError,IndexError,TypeError):changes.append(name)
        else:raise ValueError('damage accepted:'+name)
    damage('missing word',lambda a:a['records'].pop())
    damage('duplicate word',lambda a:a['records'].append(copy.deepcopy(a['records'][0])))
    damage('gap coefficient',lambda a:a['records'][0]['gaps'][0].__setitem__(0,'3'))
    damage('Bezout multiplier',lambda a:a['records'][0]['bezout'].__setitem__(0,['9']))
    damage('Bernstein coefficient',lambda a:a['records'][0]['bernstein'].__setitem__(0,'-123'))
    damage('exception flag',lambda a:a['records'][0].__setitem__('hexagonal_exception',True))
    damage('root band',lambda a:a['hexagon'].__setitem__('root_bracket',['1/2','3/4']))
    damage('core vector',lambda a:a['hexagon']['vectors'][0].__setitem__(0,['2']))
    damage('off-diagonal Gram entry',lambda a:a['hexagon']['gram'][0].__setitem__(1,['0']))
    damage('final state',lambda a:a['hexagon']['closed_three_fan_state'][0].__setitem__(0,['2']))
    damage('cap arithmetic',lambda a:a['cap'].__setitem__('ring_dot_lower','3/5'))
    damage('core capacity',lambda a:a['cap'].__setitem__('total_points_at_most',15))
    # A nonzero positive scalar rescales a sign witness without changing its proof.
    scaled=copy.deepcopy(d);row=next(r for r in scaled['records'] if not r['hexagonal_exception'])
    for name in ('combination','bernstein'):
        row[name]=[str(2*Q(v)) for v in row[name]]
    row['bezout']=[[str(2*Q(v)) for v in p] for p in row['bezout']]
    verify(scaled)
    return dict(rejected_damages=changes,valid_witness_rescaling_accepted=True)

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('author')/'CERTIFICATE.json'
    raw=path.read_bytes();data=json.loads(raw);result=dict(certificate_sha256=hashlib.sha256(raw).hexdigest(),verification=verify(data),controls=controls(data))
    print(json.dumps(result,sort_keys=True))
