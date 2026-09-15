#!/usr/bin/env python3
"""Exact full two-circle closure of one frozen receiving boundary; no solver."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import isqrt, gcd
from pathlib import Path
import argparse, hashlib, json
RAD=(1,3,11,33)
Z=(F(0),)*4
ONE=(F(1),F(0),F(0),F(0))
H=[v for v in range(374) if v!=310]
B=[0,150,169,243,244,245,287,296,344,345,346,357,358,359,360,361,362,363,364,365,366,367,368]
SOURCE_SHA='f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50'
BASE=Path(__file__).resolve().parent

def need(p,m):
    if not p: raise ValueError(m)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tuple(k*x for x in a)
def mul(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i^j]+=x*y*RAD[i&j]
    return tuple(out)
def mul_gcd(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            g=gcd(RAD[i],RAD[j]);out[RAD.index(RAD[i]*RAD[j]//(g*g))]+=g*x*y
    return tuple(out)
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def pairsub(a,b):return tuple(sub(x,y) for x,y in zip(a,b))
def iadd(a,b):return a[0]+b[0],a[1]+b[1]
def imul(a,b):
    q=[x*y for x in a for y in b];return min(q),max(q)
def floor(x):return x.numerator//x.denominator
def ceil(x):return -floor(-x)
def sqrt_bounds(x,bits):
    need(x>=0,'sqrt argument nonnegative')
    scale2=1<<bits
    k=isqrt((x.numerator<<(2*bits))//x.denominator)
    lo=F(k,scale2)
    hi=lo if lo*lo==x else F(k+1,scale2)
    need(lo*lo<=x<=hi*hi,'directed sqrt bound')
    return lo,hi
@lru_cache(None)
def field_interval(a,bits=128):
    r=(F(0),F(0))
    for d,c in zip(RAD,a):
        if c:r=iadd(r,imul((c,c),sqrt_bounds(F(d),bits)))
    return r
@lru_cache(None)
def root_interval(r,bits=128):
    if r==Z:return F(0),F(0)
    lo,hi=field_interval(r,bits+16)
    need(lo>0,'positive radical isolated')
    return sqrt_bounds(lo,bits)[0],sqrt_bounds(hi,bits)[1]
def sign_field(a):
    if a==Z:return 0
    for bits in (128,256,512):
        lo,hi=field_interval(a,bits)
        if lo>0:return 1
        if hi<0:return -1
    raise ValueError('unresolved nonzero field sign; no theorem')
def linear_zero(a,b,r):
    if r==Z or b==Z:return a==Z
    if a==Z:return False
    if mul(a,a)!=mul(r,mul(b,b)):return False
    return sign_field(a)==-sign_field(b)
def linear_sign(a,b,r):
    if linear_zero(a,b,r):return 0
    for bits in (128,256,512):
        lo,hi=iadd(field_interval(a,bits),imul(field_interval(b,bits),root_interval(r,bits)))
        if lo>0:return 1
        if hi<0:return -1
    raise ValueError('unresolved quadratic sign; no theorem')

def distance_equal(p,q,target):
    # p=A+sqrt(r)U, q=C+sqrt(s)V. All A,U,C,V have K coordinates.
    A,U,r=p;C,V,s=q;W=pairsub(A,C)
    a=sub(add(add(dot(W,W),mul(r,dot(U,U))),mul(s,dot(V,V))),scale(ONE,target))
    b=scale(dot(W,U),2);c=scale(dot(W,V),-2);d=scale(dot(U,V),-2)
    if s==Z:return linear_zero(a,b,r)
    e=sub(add(mul(a,a),mul(r,mul(b,b))),mul(s,add(mul(c,c),mul(r,mul(d,d)))))
    f=scale(sub(mul(a,b),mul(s,mul(c,d))),2)
    if not linear_zero(e,f,r):return False
    u0=linear_zero(a,b,r);v0=linear_zero(c,d,r)
    if u0 or v0:return u0 and v0
    return linear_sign(a,b,r)==-linear_sign(c,d,r)

def point_box(p,bits):
    A,U,r=p;result=[]
    for a,u in zip(A,U):
        lo,hi=iadd(field_interval(a,bits+16),imul(field_interval(u,bits+16),root_interval(r,bits+16)))
        result.append((floor(lo*(1<<bits)),ceil(hi*(1<<bits))))
    return tuple(result)
def square_box(a):
    lo,hi=a
    return (0 if lo<=0<=hi else min(lo*lo,hi*hi),max(lo*lo,hi*hi))
def distance_box(p,q):
    axes=[]
    for (a,b),(c,d) in zip(p,q):axes.append(square_box((a-d,b-c)))
    return axes[0][0]+axes[1][0],axes[0][1]+axes[1][1]
def point_key(p):return [[[str(x) for x in z] for z in p[0]],[[str(x) for x in z] for z in p[1]],[str(x) for x in p[2]]]
def digest(data):return hashlib.sha256(json.dumps(data,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def reconstruct(bits=128):
    raw=(BASE/'points.tsv').read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'pinned physical source')
    full=[tuple(map(int,l.split())) for l in raw.decode().splitlines() if l and not l.startswith('#')]
    need(len(full)==509 and all(len(r)==16 for r in full),'source shape')
    source={}
    for v in H:
        r=full[v];need(all(r[i]==0 for i in (2,3,6,7,10,11,14,15)),'host lies in K^2')
        source[v]=(tuple(F(r[i],96) for i in (0,1,4,5)),tuple(F(r[i],96) for i in (8,9,12,13)))
    points=[(source[v],(Z,Z),Z) for v in H];origins=[['host',v] for v in H]
    boxes=[point_box(p,bits) for p in points];routes=[];counts={'secant':0,'tangent':0,'none':0};collision_checks=0
    for a,b in combinations(B,2):
        A=source[a];C=source[b];delta=pairsub(C,A);s=dot(delta,delta)
        need(s[1]==s[2]==0 and sign_field(s)>0,'nonzero boundary squared distance in Q(sqrt33)')
        sig=sign_field(sub(s,scale(ONE,4)))
        if sig>0:counts['none']+=1;continue
        if sig==0:counts['tangent']+=1;signs=(0,);r=Z
        else:
            counts['secant']+=1;signs=(-1,1)
            denom=s[0]*s[0]-33*s[3]*s[3];need(denom!=0,'inverse denominator')
            inv=(s[0]/denom,F(0),F(0),-s[3]/denom)
            need(mul(s,inv)==ONE,'exact inverse')
            r=sub(scale(inv,4),ONE);need(sign_field(r)>0,'lens radicand positive')
        mid=tuple(scale(add(x,y),F(1,2)) for x,y in zip(A,C))
        for sign in signs:
            U=(scale(delta[1],F(-sign,2)),scale(delta[0],F(sign,2)))
            q=(mid,U,r);box=point_box(q,bits)
            hits=[]
            for i,pbox in enumerate(boxes):
                lo,hi=distance_box(box,pbox)
                if lo<=0<=hi:
                    collision_checks+=1
                    if distance_equal(q,points[i],0):hits.append(i)
            need(len(hits)<=1,'unique exact merged representative')
            if hits:j=hits[0]
            else:j=len(points);points.append(q);boxes.append(box);origins.append(['lens',a,b,sign])
            routes.append([a,b,sign,j])
    # Preflight exact merged budget before chromatic checks.
    need(len(points)-len(H)<=135,'replacement cap')
    unit=1<<(2*bits);edges=[];possible_units=0;interval_rejections=0;unmerged_possible=0
    for i,j in combinations(range(len(points)),2):
        lo,hi=distance_box(boxes[i],boxes[j])
        if lo<=0<=hi:
            unmerged_possible+=1;need(not distance_equal(points[i],points[j],0),'missed physical collision')
        if lo<=unit<=hi:
            possible_units+=1
            if distance_equal(points[i],points[j],1):edges.append([i,j])
        else:interval_rejections+=1
    es={tuple(e) for e in edges};idx={v:i for i,v in enumerate(H)}
    for a,b,sign,j in routes:
        for v in (a,b):need(tuple(sorted((idx[v],j))) in es,'every defining unit contact')
    host_edges=[e for e in edges if e[1]<373]
    cross=[e for e in edges if e[0]<373<=e[1]]
    private=[e for e in edges if e[0]>=373]
    actual_boundary=sorted({H[a] for a,b in cross})
    result={'points':len(points),'new_points':len(points)-373,'unit_edges':len(edges),'host_unit_edges':len(host_edges),'host_new_edges':len(cross),'new_new_edges':len(private),'pair_classes':counts,'formal_lens_occurrences':len(routes),'all_merged_pairs':len(points)*(len(points)-1)//2,'possible_units_exactly_decided':possible_units,'interval_nonunit_rejections':interval_rejections,'collision_tests_exactly_decided':collision_checks,'unmerged_possible_collision_tests':unmerged_possible,'actual_host_boundary':actual_boundary,'extra_host_boundary_outside_B':sorted(set(actual_boundary)-set(B)),'edge_sha256':digest(edges),'route_sha256':digest(routes),'point_formula_sha256':digest([point_key(p) for p in points]),'origins_sha256':digest(origins),'record_candidate':False}
    return result,points,edges,origins,source

def verify(cert,bits=128):
    result,points,edges,origins,source=reconstruct(bits)
    word=cert['colour4'];need(len(word)==len(points) and set(word)<=set('0123'),'colour domain')
    need(all(word[a]!=word[b] for a,b in edges),'all physical unit edges properly coloured')
    need(word[:373]==cert['host_word'],'frozen full host word retained')
    need(''.join(word[H.index(v)] for v in B)==cert['boundary_word'],'exact receiving boundary word')
    # A five-word is an optional direct upper-bound check, not a nonfour claim.
    five='4'+word[1:];need(all(five[a]!=five[b] for a,b in edges),'proper five word')
    # A literal seven-vertex induced obstruction; exhaust all 3^7 words.
    labels=cert['three_colour_obstruction_labels']
    need(len(labels)==len(set(labels))==7 and set(labels)<=set(H),'obstruction labels')
    mv=[H.index(v) for v in labels]
    me=[[mv.index(a),mv.index(b)] for a,b in edges if a in mv and b in mv]
    need(len(me)==11,'complete seven-point eleven-edge obstruction')
    need(not any(all(w[a]!=w[b] for a,b in me) for w in product(range(3),repeat=7)),'seven-point obstruction not three-colourable')
    result.update({'boundary_word':cert['boundary_word'],'host_word_extended':True,'proper_four_checked':True,'proper_five_checked':True,'chromatic_number':4,'moser_original_labels':labels,'colour4_sha256':hashlib.sha256(word.encode()).hexdigest(),'host_relation_census_replayed':False,'solver_required':False})
    if 'expected' in cert:need(result==cert['expected'],'expected exact census')
    return result

def arithmetic_controls():
    for i,j in product(range(4),repeat=2):
        a=tuple(F(k==i) for k in range(4));b=tuple(F(k==j) for k in range(4))
        need(mul(a,b)==mul_gcd(a,b),'independent basis products')
    for q in (F(0),F(1),F(2),F(999999,1000000),F(10**40+1,10**40)):
        lo,hi=sqrt_bounds(q,128);need(lo*lo<=q<=hi*hi,'sqrt rounding control')
    need(linear_zero(scale(ONE,-2),ONE,scale(ONE,4)),'positive-root cancellation')
    need(not linear_zero(scale(ONE,2),ONE,scale(ONE,4)),'squaring sign branch rejected')
    p=((Z,Z),(ONE,Z),scale(ONE,4));q=((scale(ONE,2),Z),(Z,Z),Z)
    need(distance_equal(p,q,0),'nested positive-root cancellation')
    need(not distance_equal(p,q,1),'false unit rejected')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--bits',type=int,choices=(128,192),default=128);ap.add_argument('--output',type=Path);args=ap.parse_args()
    arithmetic_controls();r=verify(json.loads(args.certificate.read_text()),args.bits)
    text=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
