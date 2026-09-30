#!/usr/bin/env python3
"""six-reviewer-1: integer-triple field, model, diameter and cap audit.

No author modules are imported. Published coordinate expressions are parsed
as data by a small AST whitelist. Geometry and certificates are regenerated.
"""
import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import gcd, isqrt, lcm
from pathlib import Path


def need(ok,message):
    if not ok:raise ValueError(message)


class E:
    """(a+b sqrt(5))/c, primitive integer triple with c positive."""
    __slots__=('a','b','c')
    def __init__(self,a=0,b=0):
        a,b=F(a),F(b);c=lcm(a.denominator,b.denominator)
        x=self.raw(a.numerator*(c//a.denominator),b.numerator*(c//b.denominator),c)
        self.a,self.b,self.c=x.a,x.b,x.c
    @classmethod
    def raw(cls,a,b,c):
        need(c!=0,'zero field denominator')
        if c<0:a,b,c=-a,-b,-c
        g=gcd(gcd(abs(a),abs(b)),c)
        out=object.__new__(cls);out.a,out.b,out.c=a//g,b//g,c//g;return out
    def __add__(self,x):
        if not isinstance(x,E):x=E(x)
        return self.raw(self.a*x.c+x.a*self.c,self.b*x.c+x.b*self.c,self.c*x.c)
    __radd__=__add__
    def __neg__(self):return self.raw(-self.a,-self.b,self.c)
    def __sub__(self,x):return self+-x if isinstance(x,E) else self+-E(x)
    def __rsub__(self,x):return -self+x
    def __mul__(self,x):
        if not isinstance(x,E):x=E(x)
        return self.raw(self.a*x.a+5*self.b*x.b,self.a*x.b+self.b*x.a,self.c*x.c)
    __rmul__=__mul__
    def __truediv__(self,x):
        if not isinstance(x,E):x=E(x)
        return self*self.raw(x.c*x.a,-x.c*x.b,x.a*x.a-5*x.b*x.b)
    def __rtruediv__(self,x):return E(x)/self
    def sign(self):
        a,b=self.a,self.b
        if not a:return (b>0)-(b<0)
        if not b or (a>0)==(b>0):return (a>0)-(a<0)
        t=a*a-5*b*b
        return ((a>0)-(a<0)) if t>0 else ((b>0)-(b<0))
    def __eq__(self,x):
        if not isinstance(x,E):
            try:x=E(x)
            except (TypeError,ValueError):return False
        return (self.a,self.b,self.c)==(x.a,x.b,x.c)
    def __hash__(self):return hash(F(self.a,self.c)) if not self.b else hash((self.a,self.b,self.c))
    def __lt__(self,x):return (self-x).sign()<0
    def __le__(self,x):return (self-x).sign()<=0
    def __gt__(self,x):return (self-x).sign()>0
    def __ge__(self,x):return (self-x).sign()>=0
    def pair(self):return [str(F(self.a,self.c)),str(F(self.b,self.c))]
    def __repr__(self):return str(self.pair())


def dot(a,b):return sum((x*y for x,y in zip(a,b)),E())
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(t,a):return tuple(t*x for x in a)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def projective(a):
    x=next((x for x in a if x!=0),None);need(x is not None,'zero projective axis')
    return tuple(y/x for y in a)
def encode(a):return [x.pair() for x in a]


def fixture(path):
    """Only constants, tuples, rational Q literals, names and +-*/ are data."""
    known={}
    def value(n):
        if isinstance(n,ast.Constant):
            need(type(n.value) in (int,str),'non-exact coordinate literal');return n.value
        if isinstance(n,ast.Tuple):return tuple(value(x) for x in n.elts)
        if isinstance(n,ast.Name):return known[n.id]
        if isinstance(n,ast.Call):
            need(isinstance(n.func,ast.Name) and n.func.id=='Q' and len(n.args)<=2 and not n.keywords,'unexpected coordinate call')
            return E(*(value(x) for x in n.args))
        if isinstance(n,ast.UnaryOp):
            need(isinstance(n.op,(ast.USub,ast.UAdd)),'unexpected unary operator')
            x=value(n.operand);return -x if isinstance(n.op,ast.USub) else x
        if isinstance(n,ast.BinOp):
            a,b=value(n.left),value(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b if isinstance(a,E) or isinstance(b,E) else F(a,b)
        raise ValueError('unsupported coordinate expression')
    for n in ast.parse(path.read_text()).body:
        if not isinstance(n,ast.Assign) or len(n.targets)!=1:continue
        target=n.targets[0]
        if isinstance(target,ast.Tuple) and all(isinstance(x,ast.Name) and x.id.startswith('C') for x in target.elts):
            values=value(n.value);need(len(values)==len(target.elts),'bad constant count')
            known.update((x.id,v) for x,v in zip(target.elts,values))
        elif isinstance(target,ast.Name) and target.id in ('VERTICES','FACES'):known[target.id]=value(n.value)
    vertices=known['VERTICES'];faces=known['FACES']
    need(len(vertices)==len(set(vertices))==55 and all(len(v)==3 and all(isinstance(x,E) for x in v) for v in vertices),'bad vertex data')
    return vertices,faces


def rotation(axis,cosine,sine_norm,v):
    return add(add(mul(cosine,v),mul((1-cosine)*dot(axis,v)/dot(axis,axis),axis)),mul(sine_norm,cross(axis,v)))


def model(vertices,faces):
    half=E(1)/2;axis=(E(),E(1,1)/2,E(1));r2=E(11,4)/4
    original=set()
    for base in ((half,half,E(2,1)/2),(E(),E(3,1)/4,E(5,1)/4),(E(3,1)/4,E(1,1)/4,E(1,1)/2)):
        for signs in product((-1,1),repeat=3):
            v=tuple(s*x for s,x in zip(signs,base))
            original.update((v,(v[1],v[2],v[0]),(v[2],v[0],v[1])))
    rim,top=E(5,3)/4,E(9,3)/4
    core={v for v in original if -rim<=dot(axis,v)<=rim}
    cupola={v for v in original if dot(axis,v)==-top}
    restored={rotation(axis,E(1,1)/4,E(-1,1)/4,v) for v in cupola}
    need((len(original),len(core),len(cupola))==(60,50,5) and set(vertices)==core|restored,'cupola construction mismatch')
    need(all(dot(v,v)==r2 for v in vertices),'wrong circumradius')
    need(all(mul(-1,v) in core for v in core),'core not symmetric')
    need(dot(vertices[8],cross(vertices[29],vertices[23]))!=0,'core does not span')
    need(all(vertices[i] in core for i in (8,29,23)),'interior pairs not in core')
    edges=Counter();planes=set()
    for face in faces:
        need(len(set(face))==len(face) and len(face) in (3,4,5,10),'invalid face')
        points=[vertices[i] for i in face];n=cross(sub(points[1],points[0]),sub(points[2],points[1]));height=dot(n,points[0])
        need(height!=0,'face through origin')
        if height<0:n,height=mul(-1,n),-height
        need(all(dot(n,p)==height for p in points) and all(dot(n,p)<=height for p in vertices),'not a supporting face')
        need({i for i,p in enumerate(vertices) if dot(n,p)==height}==set(face),'incomplete facet')
        normalized=mul(1/height,n)
        need(normalized not in planes,'repeated facet');planes.add(normalized)
        steps=[sub(points[(i+1)%len(points)],p) for i,p in enumerate(points)]
        cosine={3:E(-1)/2,4:E(),5:E(-1,1)/4,10:E(1,1)/4}[len(face)]
        need(all(dot(e,e)==1 for e in steps),'edge not unit')
        need(all(dot(e,steps[(i+1)%len(steps)])==cosine for i,e in enumerate(steps)),'face not regular')
        for a,b in zip(face,face[1:]+face[:1]):edges[tuple(sorted((a,b)))]+=1
    need(len(edges)==105 and set(edges.values())=={2} and len(faces)==52,'surface incidence mismatch')
    R=lambda v:rotation(axis,E(-1,1)/4,E(1)/2,v)
    basis=[tuple(E(int(i==j)) for i in range(3)) for j in range(3)]
    cols=[R(e) for e in basis]
    need(all(dot(a,b)==int(i==j) for i,a in enumerate(cols) for j,b in enumerate(cols)) and dot(cols[0],cross(cols[1],cols[2]))==1,'body rotation not proper')
    need({R(v) for v in vertices}==set(vertices),'rotation not a body symmetry')
    X=lambda v:(-v[0],v[1],v[2]);D=(E(),E(-1),E(7,1)/2)
    need({X(v) for v in vertices}==set(vertices) and X(D)==D,'mirror mismatch')
    orbit=[];d=D
    for _ in range(5):orbit.append(d);d=R(d)
    need(d==D and len({projective(x) for x in orbit})==5,'fivefold orbit mismatch')
    ids=[i for i,p in enumerate(vertices) if p in core and i<vertices.index(mul(-1,p))]
    need(len(ids)==25,'wrong core representatives')
    return D,orbit,ids,r2,{'vertices':55,'edges':105,'facets':dict(sorted(Counter(map(len,faces)).items())),'origin_in_interior':True,'body_group_order':10}


def direction_candidates(a):
    for i,v in enumerate(a):yield v,['one',i],False
    for i,j in combinations(range(len(a)),2):
        for s in (-1,1):yield add(a[i],mul(s,a[j])),['two',i,j,s],False
    for i,j,k in combinations(range(len(a)),3):
        for s,t in product((-1,1),repeat=2):
            u=a[i];q=sub(mul(s,a[j]),u);r=sub(mul(t,a[k]),u)
            g11,g12,g22=dot(q,q),dot(q,r),dot(r,r);det=g11*g22-g12*g12
            need(det>0,'collinear equal-radius triple')
            v,w=-dot(u,q),-dot(u,r)
            x,y=(v*g22-w*g12)/det,(w*g11-v*g12)/det
            d=add(u,add(mul(x,q),mul(y,r)))
            need(dot(d,q)==dot(d,r)==0,'affine-plane projection failed')
            zero=dot(d,d)==0
            if zero:
                d=cross(q,r);need(dot(u,d)==0,'zero nearest-point plane is inconsistent')
            yield d,['three',i,j,k,s,t],zero


def diameter(vertices,D,orbit,ids,r2,data):
    B=E(65,10)/596;beta=E(*data['beta']);need(0<beta<B,'bad region threshold')
    a=[vertices[i] for i in ids];winners=set();counts=Counter();event=sha256();full=sha256();zero=0;occ=0
    for number,(d,label,z) in enumerate(direction_candidates(a),1):
        n=dot(d,d);need(n>0,'zero candidate direction');zero+=z
        squares=[dot(v,d)*dot(v,d) for v in a]
        score=min(squares)/n;counts[label[0]]+=1
        blockers=[i for i,x in enumerate(squares) if x<=beta*n]
        if blockers:event.update((str(number)+':'+str(blockers[0])+'\n').encode())
        else:
            need(score==B,'unclassified intermediate or better candidate')
            winners.add(projective(d));occ+=1;event.update((str(number)+':MAX\n').encode())
        full.update((json.dumps([label,score.pair()],separators=(',',':'))+'\n').encode())
    need(counts=={'one':25,'two':600,'three':9200} and winners=={projective(v) for v in orbit} and occ==20,'candidate coverage mismatch')
    i,j,s=data['beta_witness'][1:];d=add(a[i],mul(s,a[j]));need(min(dot(v,d)*dot(v,d) for v in a)/dot(d,d)==beta,'runner-up not attained')
    # Complete distance checks, rather than a declared subset of active pairs.
    active=[];nonpaired=[];checks=0
    for oi,d in enumerate(orbit):
        n=dot(d,d);pairs=[]
        for i,j in combinations(range(55),2):
            v=sub(vertices[i],vertices[j]);z=dot(v,d);gap=4*(r2-B)-dot(v,v)+z*z/n
            need(gap>=0,'full shadow diameter exceeds core value');checks+=1
            if gap==0:pairs.append([i,j])
            if oi==0 and vertices[j]!=mul(-1,vertices[i]):nonpaired.append(gap)
        active.append(pairs)
    need(len(nonpaired)==1460 and min(nonpaired)==E(901,-125)/1490,'nonantipodal gap mismatch')
    return {'candidate_counts':dict(counts),'full_axial_height_comparisons':9825*25,'nearest_affine_planes_through_origin':zero,'maximizing_occurrences':occ,'projective_optimizers':5,'legacy_first_blocker_sha256':event.hexdigest(),'complete_candidate_score_sha256':full.hexdigest(),'full_body_pairs':checks,'equality_pairs':active,'nonantipodal_gap':min(nonpaired).pair()},min(nonpaired)


def shadow(vertices,D):
    plane=lambda v:(v[0],D[2]*v[1]+v[2]);points=list({plane(v) for v in vertices})
    start=min(points);p=start;boundary=[]
    # Jarvis wrapping, not the target's sorted-chain hull.
    while True:
        boundary.append(p);q=next(v for v in points if v!=p)
        for v in points:
            if v==p:continue
            a,b=sub(q,p),sub(v,p);turn=a[0]*b[1]-a[1]*b[0]
            if turn<0 or (turn==0 and dot(b,b)>dot(a,a)):q=v
        p=q
        if p==start:break
        need(p not in boundary and len(boundary)<56,'gift wrapping did not close')
    need(all(sum(plane(v)==p for v in vertices)==1 for p in boundary),'extreme preimage not unique')
    ids=[next(i for i,v in enumerate(vertices) if plane(v)==p) for p in boundary]
    need(len(ids)==17 and 15 in ids,'wrong shadow hull')
    at=ids.index(15);ids=ids[at:]+ids[:at]
    normals=[]
    for i,j in zip(ids,ids[1:]+ids[:1]):
        m=cross(sub(vertices[j],vertices[i]),D);h=dot(m,vertices[i]);need(h>0,'reversed outer edge')
        m=mul(1/h,m);need(all(dot(m,v)<=1 for v in vertices),'false shadow edge')
        need(dot(m,D)==0 and dot(m,m)<E(F(51,100))*E(F(51,100)),'outer probe bound fails')
        normals.append(m)
    return ids,normals


def planar_isometries(vertices,D,cycle):
    N=dot(D,D)
    projected=[(vertices[i][0],D[2]*vertices[i][1]+vertices[i][2]) for i in cycle]
    distance=lambda p,q:(p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1])/N
    matrix=[[distance(p,q) for q in projected] for p in projected]
    accepted=[]
    for sign,shift in product((1,-1),range(17)):
        mapping=[(shift+sign*i)%17 for i in range(17)]
        if all(matrix[i][j]==matrix[mapping[i]][mapping[j]] for i in range(17) for j in range(i+1,17)):
            accepted.append([sign,shift])
    need([x for x in accepted if x[0]==1]==[[1,0]] and len(accepted)==2,'planar isometry group differs')
    return {'squared_chord_correspondences':34,'isometries':accepted,'vertex_centroid':encode(tuple(sum((p[k] for p in projected),E())/17 for k in range(2)))}


def determinant(matrix):
    n=len(matrix);out=E()
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));term=E(-1 if inversions%2 else 1)
        for i,j in enumerate(p):term=term*matrix[i][j]
        out=out+term
    return out


def cramer(columns,target):
    n=len(columns)
    for rows in combinations(range(6),n):
        matrix=[[col[i] for col in columns] for i in rows];det=determinant(matrix)
        if det!=0:break
    else:raise ValueError('dependent stress columns')
    weights=[]
    for j in range(n):
        amended=[row[:] for row in matrix]
        for k,i in enumerate(rows):amended[k][j]=E(target[i])
        weights.append(determinant(amended)/det)
    need(all(sum((w*col[i] for w,col in zip(weights,columns)),E())==target[i] for i in range(6)),'stress fails original six coordinates')
    return weights


def local_stresses(vertices,D,cycle,normals,r2):
    probes=[]
    for j,vertex in enumerate(cycle):
        for t in (E(1)/4,E(3)/4):probes.append((vertex,add(mul(1-t,normals[j-1]),mul(t,normals[j]))))
    columns=[];gaps=[]
    for i,m in probes:
        need(dot(m,D)==0 and dot(m,vertices[i])==1,'bad local probe')
        gap=[dot(m,sub(vertices[i],w)) for j,w in enumerate(vertices) if i!=j]
        need(min(gap)>E(1)/80 and r2*dot(m,m)<E(9)/8*E(9)/8,'local probe inequality fails');gaps.extend(gap)
        columns.append(cross(vertices[i],m)+m)
    bases=[(0,1,[5,12,25,26]),(0,-1,[7,10,21,30]),(1,1,[2,13,18,19,27]),(1,-1,[4,15,24,32,33]),(2,1,[1,7,9,19,23]),(2,-1,[8,10,16,28,32])]
    rows=[];totals=[]
    for axis,sign,ids in bases:
        target=[0]*6;target[axis]=sign;w=cramer([columns[i] for i in ids],target)
        need(min(w)>0 and sum(w,E())<E(F(61,10)),'nonpositive or over-budget stress')
        rows.append([axis,sign,ids,encode(w)]);totals.append(sum(w,E()).pair())
    error=F(61,10)*F(9,8)*(F(1,200)+F(3,40))
    need(2*F(9,8)/200<F(1,80) and 3*error*error<1,'local theorem scalar gap fails')
    return {'unique_support_tests':len(gaps),'minimum_support_gap':min(gaps).pair(),'positive_stress_columns':sum(len(x[2]) for x in rows),'cramer_coefficient_sha256':sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),'coefficient_sums':totals,'torque_error':str(error)}


def tangent_hull(vertices,D,ids):
    n=dot(D,D);B=E(65,10)/596
    a=[]
    for i in ids:
        p=dot(vertices[i],D)
        if p*p==B*n:a.append(mul(p.sign(),vertices[i]))
    need(len(a)==4,'critical tangent set mismatch')
    tangent=[sub(v,mul(dot(v,D)/n,D)) for v in a];distances=[];edges=set()
    # Enumerate all supporting lines of the four-point hull directly.
    for i,j in combinations(range(4),2):
        m=cross(sub(tangent[j],tangent[i]),D);h=dot(m,tangent[i])
        if h<0:m,h=mul(-1,m),-h
        if h>0 and all(dot(m,v)<=h for v in tangent):
            distances.append(h*h/dot(m,m));edges.add((i,j))
    need(len(edges)==4 and min(distances)==E(233,-10)/596 and min(distances)>E(1)/4,'tangent inradius fails')
    return min(distances)


def concave_check(p,lo,hi,bound):
    need(p[2]<=0,'roll lower polynomial is not concave')
    values=[p[0]+E(x)*p[1]+E(x*x)*p[2] for x in (lo,hi)]
    need(min(values)>bound,'endpoint lower bound is too small')
    return values


def rolls(vertices,D,normals,data):
    root_lo,root_hi=(E(F(x)) for x in data['root_N_enclosure']);N=dot(D,D)
    need(0<root_lo<root_hi and root_lo*root_lo<N<root_hi*root_hi,'root enclosure fails')
    need({c['sign'] for c in data['covers']}=={-1,1} and len(data['covers'])==2,'both roll signs required')
    endpoint_min=None;rows=[]
    for cover in data['covers']:
        endpoint=F(data['roll_tangent_threshold']);need(endpoint==F(1,50),'changed roll threshold')
        for piece in cover['pieces']:
            lo,hi=map(F,piece['interval']);need(lo==endpoint and lo<hi<=1,'incomplete roll interval');endpoint=hi
            probe=piece['probe'];i,j=piece['source_pair'];orientation=piece['orientation']
            need(type(probe) is int and 0<=probe<17 and orientation in (-1,1) and i!=j and 0<=i<55 and 0<=j<55,'bad roll fixture')
            m=mul(orientation,normals[probe]);w=sub(vertices[i],vertices[j]);values=[dot(m,v) for v in vertices];H=max(values)-min(values)
            d=dot(m,w);z=cover['sign']*dot(m,cross(D,w));k=z/(root_hi if z>=0 else root_lo)
            p=(d-H,2*k,-d-H)
            ends=concave_check(p,lo,hi,E(1)/48)
            endpoint_min=min(ends) if endpoint_min is None else min(endpoint_min,*ends)
            rows.append({'sign':cover['sign'],'interval':[str(lo),str(hi)],'quadratic':encode(p),'endpoints':encode(ends)})
        need(endpoint==1,'remote roll endpoint missing')
    need(len(rows)==12,'wrong closed roll cover size')
    ids=data['half_turn_indices'];weights=[E(*x) for x in data['half_turn_weights']]
    need(len(ids)==len(set(ids))==len(weights)==3 and min(weights)>0 and sum(weights,E())==1,'invalid half-turn stress')
    need(all(sum((w*normals[i][k] for w,i in zip(weights,ids)),E())==0 for k in range(3)),'half-turn translation does not cancel')
    gap=sum((w*(max(-dot(normals[i],v) for v in vertices)-1) for w,i in zip(weights,ids)),E())
    need(gap==E(-151,74)/241 and gap>E(3)/50,'half-turn margin fails')
    return {'concave_pieces':len(rows),'checked_endpoints':2*len(rows),'minimum_endpoint':endpoint_min.pair(),'endpoint_lower_bound':'1/48','half_turn_gap':gap.pair(),'half_turn_lower_bound':'3/50','piece_evidence':rows},gap


def cap_margins(d,nonpaired):
    d=E(d);B=E(65,10)/596;r2=E(11,4)/4;beta=E(5,-1)/20;M=E(F(51,100));a=E(1)/50
    values={'radius':E(81)/16-r2,'c0_lower':B-E(9)/64,'c0_upper':E(4)/25-B,
            'diameter_active':nonpaired-16*r2*d,'winning_region':B-E(9)/5*d-beta,
            'sine_domain':E(1)/10-5*d,'half_turn':E(3)/50-M*(14*d+E(9)/4*2*a),
            'remote_roll':E(1)/48-56*d*M,'full_rotation':E(3)/20-(2*a+E(101)/100*6*d),
            'local_receiver':E(1)/200-d,'transport_arcsine':E(101)/100*E(101)/100*E(399)/400-1,
            'chord_sine_factor':E(101)/100*E(101)/100-E(200)/199}
    need(all(x>0 for x in values.values()),'cap-transfer scalar inequality fails')
    return {k:v.pair() for k,v in values.items()}


def controls():
    den=10**160;lower=isqrt(5*den*den);low,high=F(lower,den),F(lower+1,den)
    signed=0
    for a,b in product(range(-8,9),repeat=2):
        x=E(a,b)
        ends=(F(a)+F(b)*low,F(a)+F(b)*high)
        expected=0 if x==0 else (1 if min(ends)>0 else -1)
        need(x==0 or min(ends)>0 or max(ends)<0,'inconclusive control enclosure')
        need(x.sign()==expected,'integer field sign disagrees with rational enclosure');signed+=1
        if x!=0:need(x*(1/x)==1,'field inversion control failed')
    pell=E(1)
    for _ in range(60):pell=pell*E(9,-4)
    for x in (pell,-pell):
        ends=(F(x.a,x.c)+F(x.b,x.c)*low,F(x.a,x.c)+F(x.b,x.c)*high)
        need((min(ends)>0 and x.sign()==1) or (max(ends)<0 and x.sign()==-1),'small Pell sign failed')
    basis=[tuple(E(int(i==j)) for i in range(3)) for j in range(3)]
    for size in (1,2,3):
        scores=[min(dot(v,d)*dot(v,d) for v in basis[:size])/dot(d,d) for d,label,z in direction_candidates(basis[:size])]
        need(max(scores)==E(1)/size,'active-set control failed')
    return {'rational_enclosure_field_cases':signed+2,'orthogonal_active_set_cases':3}


def evidence_controls(vertices,D,normals,data,nonpaired):
    # Exact nonidentity proper rotation with equal shadows, at the base normal.
    N=dot(D,D);P=lambda v:sub(v,mul(dot(D,v)/N,D));X=lambda v:(-v[0],v[1],v[2])
    M=lambda v:sub(v,mul(2*dot(D,v)/N,D));Q=lambda v:M(X(v))
    basis=[tuple(E(int(i==j)) for i in range(3)) for j in range(3)]
    cols=[Q(v) for v in basis]
    need(cols!=basis and dot(cols[0],cross(cols[1],cols[2]))==1,'closed mirror equality is not proper nonidentity')
    need(all(dot(a,b)==int(i==j) for i,a in enumerate(cols) for j,b in enumerate(cols)),'closed equality rotation is not orthogonal')
    need({P(Q(v)) for v in vertices}=={P(v) for v in vertices},'literal closed equality fails')
    rows=(basis[0],(E(),D[2],E(1)))
    need(cross(X(rows[0]),X(rows[1]))==mul(-1,X(cross(*rows))),'improper-frame cross normal identity fails')
    # A convex quadratic can have positive endpoints and a negative interior.
    bad_poly=(E(1)/10,E(-1),E(1))
    need(bad_poly[0]>0 and sum(bad_poly,E())>0 and bad_poly[0]+bad_poly[1]/2+bad_poly[2]/4<0,'concavity countercontrol is ineffective')
    rejections=0
    def copy():return json.loads(json.dumps(data))
    bad=[]
    x=copy();x['covers'].pop();bad.append(lambda x=x:rolls(vertices,D,normals,x))
    x=copy();x['covers'][0]['pieces'][-1]['interval'][1]='9/10';bad.append(lambda x=x:rolls(vertices,D,normals,x))
    x=copy();x['covers'][0]['pieces'][0]['source_pair']=[0,0];bad.append(lambda x=x:rolls(vertices,D,normals,x))
    x=copy();x['root_N_enclosure'][0]='5';bad.append(lambda x=x:rolls(vertices,D,normals,x))
    x=copy();x['half_turn_weights'][0]=['-1','0'];bad.append(lambda x=x:rolls(vertices,D,normals,x))
    bad.append(lambda:concave_check(bad_poly,F(0),F(1),E(0)))
    bad.append(lambda:cap_margins(F(1,1000),nonpaired))
    reversed_normals=[mul(-1,m) for m in normals]
    bad.append(lambda:local_stresses(vertices,D,[15,48,32,54,24,51,30,44,11,8,41,29,16,19,31,45,12],reversed_normals,E(11,4)/4))
    for f in bad:
        try:f()
        except ValueError:rejections+=1
        else:raise ValueError('malformed geometry evidence accepted')
    return {'malformed_evidence_rejections':rejections,'proper_nonidentity_closed_equality_checked':True,'improper_frame_normal_checked':True,'positive_endpoint_convex_countercontrol':True}


def main():
    p=argparse.ArgumentParser(description=__doc__);here=Path(__file__).resolve().parent
    p.add_argument('--model',type=Path,default=here.parent/'rupert_j77_projection_diameter/model.py')
    p.add_argument('--certificate',type=Path,default=here.parent/'rupert_j77_all_source_diameter_caps/certificates.json')
    p.add_argument('--write',type=Path);args=p.parse_args()
    V,faces=fixture(args.model);data=json.loads(args.certificate.read_text())
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','input_sha256':{'model':sha256(args.model.read_bytes()).hexdigest(),'certificate':sha256(args.certificate.read_bytes()).hexdigest()},'controls':controls()}
    D,orbit,ids,r2,result['model']=model(V,faces)
    result['diameter'],nonpaired=diameter(V,D,orbit,ids,r2,data)
    cycle,normals=shadow(V,D);result['reference_cycle']=cycle
    result['reference_planar_isometries']=planar_isometries(V,D,cycle)
    result['local_stress_dependency']=local_stresses(V,D,cycle,normals,r2)
    result['tangent_inradius_squared']=tangent_hull(V,D,ids).pair()
    result['roll_certificate'],gap=rolls(V,D,normals,data)
    result['original_cap_margins']=cap_margins(F(1,2000),nonpaired)
    result['strengthened_cap_margins']=cap_margins(F(1,1400),nonpaired)
    result['strengthened_receiver_chord']='1/1400'
    result['strengthened_full_rotation_upper_bound']=str(F(1,25)+F(101,100)*6*F(1,1400))
    result['evidence_controls']=evidence_controls(V,D,normals,data,nonpaired)
    result=json.loads(json.dumps(result));out=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:args.write.write_text(out)
    else:need(result==json.loads((here/'expected.json').read_text()),'independent manifest differs')
    print(out,end='')


if __name__=='__main__':main()
