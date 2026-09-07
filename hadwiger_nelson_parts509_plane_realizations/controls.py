"""Small field and geometry controls, plus mutations of each proof layer."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import verify as checker

HERE=Path(__file__).resolve().parent

def main():
    require=checker.require;field_cases=0
    for square in (-3,33):
        q=checker.Quadratic(square)
        values=[q.make(a,b,d) for a,b,d in product(range(-2,3),range(-2,3),(1,2,3))]
        for x,y in product(values,repeat=2):
            a,b,c=x;d,e,f=y
            expected=q.parse(F(a,c)*F(d,f)+square*F(b,c)*F(e,f),F(a,c)*F(e,f)+F(b,c)*F(d,f))
            require(q.mul(x,y)==expected,'field multiplication')
            require(q.sub(q.add(x,y),y)==x,'field addition inverse')
            if y!=checker.ZERO:require(q.mul(q.mul(x,y),q.inv(y))==x,'field division')
            field_cases+=1
    # A diamond with distinct apices satisfies the midpoint identity. Collapsing
    # its short diagonal preserves the four sides and destroys that identity.
    # Coordinates are independently represented in Q(sqrt(3)), scale two.
    diamond=[((0,0),(0,0)),((2,0),(0,0)),((1,0),(0,1)),((1,0),(0,-1))]
    def distance(p,r):
        a=b=0
        for x,y in zip(p,r):
            u=x[0]-y[0];v=x[1]-y[1];a+=u*u+3*v*v;b+=2*u*v
        return a,b
    require(all(distance(diamond[a],diamond[b])==(4,0) for a in (0,1) for b in (2,3)),'diamond units')
    collapsed=[diamond[0],diamond[0],diamond[2],diamond[3]]
    require(all(distance(collapsed[a],collapsed[b])==(4,0) for a in (0,1) for b in (2,3)),'degenerate diamond units')
    require(tuple(sum(collapsed[i][j][k] for i in (0,1))-sum(collapsed[i][j][k] for i in (2,3)) for j in range(2) for k in range(2))!=(0,0,0,0),'degeneracy requires special treatment')
    # Two different equality pairs always remove at least two classes.
    equality_cases=0
    pairs=[(a,b) for a in range(5) for b in range(a+1,5)]
    for i,p in enumerate(pairs):
        for r in pairs[i+1:]:
            blocks=[{v} for v in range(5)]
            for a,b in (p,r):
                union=set().union(*(s for s in blocks if a in s or b in s))
                blocks=[s for s in blocks if a not in s and b not in s]+[union]
            require(len(blocks)==3,'two-pair image loss');equality_cases+=1
    cert=json.loads((HERE/'certificate.json').read_text());edges,points,K=checker.load_inputs();V=checker.get_directions(cert,edges,K)
    rejected=[]
    def reject(name,mutate,check):
        bad=deepcopy(cert);mutate(bad)
        try:check(bad)
        except (ValueError,KeyError,IndexError,ZeroDivisionError):rejected.append(name)
        else:raise ValueError('accepted malformed certificate: '+name)
    rh=lambda c:checker.check_rhombi(c,edges,K)
    ori=lambda c:checker.check_orientations(c,K,V)
    pol=lambda c:checker.check_polynomials(c,V)
    reject('duplicate basis row',lambda c:c['bases'][0].__setitem__(0,c['bases'][0][1]),rh)
    reject('missing exception',lambda c:c['exceptions'].pop(),rh)
    reject('false edge exception',lambda c:c['exceptions'][1].update(edge=True),rh)
    reject('repeated K23 vertex',lambda c:c['exceptions'][1]['k23'].__setitem__(0,c['exceptions'][1]['k23'][2]),rh)
    reject('K23 uses removed label',lambda c:c['exceptions'][1]['k23'].__setitem__(0,c['exceptions'][1]['pair'][1]),rh)
    reject('wrong direction witness',lambda c:c['direction_edges'].__setitem__(0,[0,0]),lambda c:checker.get_directions(c,edges,K))
    reject('false triad',lambda c:c['triads'][0].__setitem__(3,-c['triads'][0][3]),ori)
    reject('missing orientation prefix',lambda c:c['orientation_cover'].pop(),ori)
    reject('duplicate orientation prefix',lambda c:c['orientation_cover'].append(c['orientation_cover'][0]),ori)
    reject('repeated equality pair',lambda c:c['orientation_cover'][0]['pairs'].__setitem__(1,c['orientation_cover'][0]['pairs'][0]),ori)
    reject('false equality pair',lambda c:c['orientation_cover'][0]['pairs'].__setitem__(0,[0,397]),ori)
    reject('false surviving orientation',lambda c:c['orientation_cover'][0].update(survivor=True),ori)
    reject('zero polynomial weight',lambda c:c['polynomial_combinations']['y'].__setitem__(0,[c['polynomial_combinations']['y'][0][0],'0','0']),pol)
    reject('missing polynomial term',lambda c:c['polynomial_combinations']['d_minus_c_b'].pop(),pol)
    damaged=deepcopy(points);damaged[0]=(tuple([1]+[0]*7),damaged[0][1])
    try:checker.check_realizations(damaged,edges)
    except ValueError:rejected.append('changed source coordinate')
    else:raise ValueError('accepted changed source coordinate')
    print(json.dumps({'field_cases':field_cases,'diamond_controls':2,'two_equality_pair_cases':equality_cases,
                      'malformed_certificates_rejected':len(rejected),'rejections':rejected,'all_checks_passed':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
