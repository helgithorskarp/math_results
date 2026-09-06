"""Independent rational-interval, all-labelled-pairs positive witness audit.

Imports neither the producer nor its arithmetic. Circle intersection formulas
use distances and perpendicular heights; producer uses a polynomial discriminant.
Every arithmetic result is rounded outward to multiples of 10**-45.
"""
import argparse,hashlib,json,time
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=10**45

def down(x): return F((x.numerator*D)//x.denominator,D)
def up(x): return -down(-x)

class R:
    def __init__(self,a,b=None):
        self.a,self.b=F(a),F(a if b is None else b)
        assert self.a<=self.b
    @staticmethod
    def bounds(a,b): return R(down(a),up(b))
    def __add__(self,y): return R.bounds(self.a+y.a,self.b+y.b)
    def __neg__(self): return R(-self.b,-self.a)
    def __sub__(self,y): return self+-y
    def __mul__(self,y):
        vals=[a*b for a in (self.a,self.b) for b in (y.a,y.b)]
        return R.bounds(min(vals),max(vals))
    def __truediv__(self,y):
        assert y.a*y.b>0
        vals=[a/b for a in (self.a,self.b) for b in (y.a,y.b)]
        return R.bounds(min(vals),max(vals))
    def sqrt(self):
        assert self.a>=0
        def lower(x):
            return isqrt((x.numerator*D*D)//x.denominator)
        a,b=lower(self.a),lower(self.b)
        return R(F(a,D),F(b+(F(b*b,D*D)<self.b),D))
    def square(self):
        vals=[self.a*self.a,self.b*self.b]
        return R.bounds(0 if self.a<=0<=self.b else min(vals),max(vals))

class Z:
    def __init__(self,x,y): self.x,self.y=x,y
    def __add__(self,z): return Z(self.x+z.x,self.y+z.y)
    def __sub__(self,z): return Z(self.x-z.x,self.y-z.y)
    def times(self,r): return Z(self.x*r,self.y*r)
    def product(self,z): return Z(self.x*z.x-self.y*z.y,self.x*z.y+self.y*z.x)
    def perp(self): return Z(-self.y,self.x)
    def norm2(self): return self.x.square()+self.y.square()

def generate():
    sqrt3=R(3).sqrt();sqrt11=R(11).sqrt();sqrt7=R(7).sqrt()
    rho=Z(R(F(5,6)),sqrt11/R(6));v=Z(R(F(1,2)),sqrt3/R(2));u=Z(R(1),R(0))
    m=[Z(R(0),R(0)),u,v,u+v,rho.product(u),rho.product(v),rho.product(u+v)]
    points=list(m);labels=[['M',i] for i in range(7)];triangles=[];branches=[]
    for i in range(7):
        for j in range(i+1,7):
            delta=m[j]-m[i];dist=delta.norm2().sqrt()
            assert dist.a>0 and dist.b<2
            height=(R(1)-(dist/R(2)).square()).sqrt()
            foot=m[i]+delta.times(R(F(1,2)))
            for s in (-1,1):
                a=foot+delta.perp().times(R(s)*height/dist)
                for k in range(7):
                    label=[i,j,s,k];diff=m[k]-a;distance=diff.norm2().sqrt()
                    if distance.b<(sqrt7-R(1)).a or distance.a>(sqrt7+R(1)).b:
                        branches.append([label,'absent']);continue
                    assert distance.a>(sqrt7-R(1)).b and distance.b<(sqrt7+R(1)).a, label
                    branches.append([label,'two'])
                    along=(distance.square()+R(6))/(R(2)*distance)
                    vertical=(R(7)-along.square()).sqrt()
                    for side in (-1,1):
                        b=a+diff.times(along/distance)+diff.perp().times(R(side)*vertical/distance)
                        for orient in (-1,1):
                            z=b-a
                            c=a+z.times(R(F(1,2)))+z.perp().times(R(orient)*sqrt3/R(2))
                            triangles.append(list(range(len(points),len(points)+3)))
                            points.extend([a,b,c]);labels.extend([label+[side,orient,t] for t in range(3)])
    return points,labels,triangles,branches

def pair_audit(points,colours):
    assert len(points)==len(colours) and all(type(c) is int and c in range(4) for c in colours)
    equal_colour_pairs=0;different_colour_pairs=0
    for i,j in combinations(range(len(points)),2):
        z=points[i]-points[j]
        if colours[i]==colours[j]:
            d=z.norm2();assert d.b<1 or d.a>1, ('possible monochromatic unit edge',i,j)
            equal_colour_pairs+=1
        else:
            # Any pair carrying different colours must be provably distinct.
            assert z.x.b<0 or z.x.a>0 or z.y.b<0 or z.y.a>0, ('possible differently coloured alias',i,j)
            different_colour_pairs+=1
    return {'same_colour_nonunit_checks':equal_colour_pairs,'different_colour_distinctness_checks':different_colour_pairs}

def rejected(fn):
    try:fn()
    except AssertionError:return True
    raise AssertionError('invalid control accepted')

def controls():
    # Exact corner extrema for multiplication/division, including negative values.
    count=0
    for a,b,c,d in [(-3,2,-4,5),(-5,-2,-7,-1),(-3,4,2,7),(0,0,1,3)]:
        x,y=R(F(a,7),F(b,7)),R(F(c,11),F(d,11));z=x*y
        vals=[p*q for p in (x.a,x.b) for q in (y.a,y.b)]
        assert z.a<=min(vals)<=max(vals)<=z.b;count+=1
        if y.a*y.b>0:
            z=x/y;vals=[p/q for p in (x.a,x.b) for q in (y.a,y.b)]
            assert z.a<=min(vals)<=max(vals)<=z.b;count+=1
    for n in (0,1,2,3,7,11,49):
        z=R(n).sqrt();assert z.a*z.a<=n<=z.b*z.b;count+=1
    eps=F(1,D)
    for x in (F(1)-eps,F(1),F(1)+eps):
        z=R(x).sqrt();assert z.a*z.a<=x<=z.b*z.b;count+=1
    z=Z(R(0),R(0));one=Z(R(1),R(0))
    assert rejected(lambda:pair_audit([z,one],[0,0]))
    assert rejected(lambda:pair_audit([z,z],[0,1]))
    assert rejected(lambda:pair_audit([z],[4]))
    return {'arithmetic_controls':count,'rejection_controls':3}

def main():
    assert __debug__,'run without -O'
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);a=p.parse_args();start=time.monotonic()
    data=json.loads((Path(a.work)/'build.json').read_text());expected=json.loads((HERE/'expected.json').read_text())
    digest=hashlib.sha256(json.dumps(data,separators=(',',':'),sort_keys=True).encode()).hexdigest()
    assert digest==expected['data_sha256']
    points,labels,triangles,branches=generate()
    assert labels==data['labels'] and triangles==data['labelled_triangles'] and branches==data['circle_branches']
    # Cross-check both enclosures. Their intersection is necessary but never
    # treated as a proof of equality or a substitute for the direct pair audit.
    for point,box in zip(points,data['points']):
        for interval,bounds in zip((point.x,point.y),box):
            lo,hi=(F(t,2**data['bits']) for t in bounds)
            assert max(interval.a,lo)<=min(interval.b,hi)
    cert=json.loads((HERE/'certificate.json').read_text())
    assert len(cert['labelled_colours'])==len(points) and all(c in '0123' for c in cert['labelled_colours'])
    colours=list(map(int,cert['labelled_colours']))
    assert colours==[cert['colours'][g] for g in data['groups']]
    result=pair_audit(points,colours)
    assert all(len({colours[i] for i in t})>1 for t in triangles)
    result.update(controls())
    # Exact Q(sqrt3) fixture refuting the tempting free-terminal shortcut.
    fixture=[(F(1,2),F(-1,2)),(F(0),F(1)),(F(5,2),F(1,2))]
    base=[(F(0),F(0)),(F(1),F(0)),(F(1,2),F(1,2)),(F(3,2),F(1,2))]
    d2=lambda p,q:(p[0]-q[0])**2+3*(p[1]-q[1])**2
    assert all(d2(fixture[i],fixture[j])==7 for i,j in combinations(range(3),2))
    assert all(d2(fixture[i],base[j])==1 for i,j in [(0,0),(0,1),(1,2),(2,3)])
    result['exact_all_contact_fixture_checks']=7
    # A corruption at a known spindle edge must be rejected by direct geometry.
    corrupt=colours[:];corrupt[1]=corrupt[0]
    assert rejected(lambda:pair_audit(points,corrupt));result['rejection_controls']+=1
    result.update({'status':'PASS','decimal_digits':45,'points':len(points),
        'all_pairs':len(points)*(len(points)-1)//2,'nonmono_triangles':len(triangles),
        'coordinate_enclosure_comparisons':2*len(points),'seconds':time.monotonic()-start})
    (Path(a.work)/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
