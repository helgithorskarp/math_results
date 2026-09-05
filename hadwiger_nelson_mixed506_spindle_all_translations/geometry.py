"""Finite two-circle census for one fixed mixed506 rotation."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
from hashlib import sha256
from math import gcd,lcm,isqrt
import importlib.util,json
import square_field as F
HERE=Path(__file__).resolve().parent
PRIMES=(131,181,229,239,359,421)
ROOTS=((38,23,50),(33,27,83),(71,66,34),(106,31,49),(163,148,27),(74,200,46))

def require(ok,msg):
    if not ok:raise ValueError(msg)

def load(name,path,pin):
    p=HERE.parent/path
    require(sha256(p.read_bytes()).hexdigest()==pin,'source pin mismatch')
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m

C=load('overlap_source','hadwiger_nelson_mixed505_spindle_rotation/census.py','148fef89b7d9692e5631918a9fc6a1f849fe95f2fdaed0b90bc5a6d743de308a')

def data():
    B,V,EB,EV=C.sources();zero=(0,0,0,0)
    I,J=incidence(B),incidence(V)
    return B,V,EB,EV,sorted(I),sorted(J),I,J

def incidence(G):
    out=defaultdict(list)
    for i,p in enumerate(G):
        for j,q in enumerate(G):out[tuple(b-a for a,b in zip(p,q))].append((i,j))
    return out

def images(G,p,roots,rotate,signs):
    r3,r5,r11=roots;r11*=signs[0];r5*=signs[1]
    i72,i8=pow(72,-1,p),pow(8,-1,p);out=[]
    for a,b,c,d in G:
        x=(a+b*r3*r11)*i72%p;y=(c*r3+d*r11)*i72%p
        if rotate:x,y=(7*x-r3*r5*y)*i8%p,(r3*r5*x+7*y)*i8%p
        out.append((x,y))
    return out

def prepare(X,Y):
    tables=[]
    for p,r in zip(PRIMES,ROOTS):
        require(all(p%d for d in range(2,isqrt(p)+1)) and all(a*a%p==d for a,d in zip(r,(3,5,11))),'invalid prime data')
        qr={x*x%p for x in range(p)};inv3=pow(3,-1,p)
        accepts=[d*(4-d)*inv3%p in qr for d in range(p)]
        for signs in product((1,-1),repeat=2):tables.append((p,images(X,p,r,False,signs),images(Y,p,r,True,signs),accepts))
    return tables

def screen(tables,begin=0,end=None):
    if end is None:end=len(tables[0][1])
    stages=[0]*len(tables);out=[]
    for i in range(begin,end):
        for j in range(len(tables[0][2])):
            for stage,(p,xx,yy,accept) in enumerate(tables):
                x,y=xx[i];a,b=yy[j];d=((x-a)**2+(y-b)**2)%p
                if not accept[d]:break
                stages[stage]+=1
            else:out.append((i,j))
    return stages,out

def canonical(den,nums):
    g=gcd(den,*nums)
    return (den//g,)+tuple(a//g for a in nums)

def offset(p,q):
    a,b,c,d=p;A,B,C,D=q
    return (24*a-21*A,24*b-21*B,9*C,3*D,24*c-21*C,8*d-7*D,-3*A,-3*B)

def classify(X,Y,survivors):
    positive=[];negative=[];zero=[]
    for i,j in survivors:
        hs=F.circles(X[i],Y[j])
        if hs:positive.append((i,j,hs))
        elif X[i]==Y[j]==(0,0,0,0):zero.append((i,j))
        else:negative.append((i,j))
    require(len(zero)==1,'zero difference handling failed')
    return positive,negative,zero

def project(B,V,I,J,X,Y,positive):
    z=[offset(p,q) for p in B for q in V];overlap={canonical(1728,x) for x in z}
    require(len(overlap)==62488,'offset centres are not distinct')
    translated={};hits=overlap_hits=0;seen_overlaps=set()
    for i,j,hs in positive:
        for hh in hs:
            h=[c for row in hh for c in row];den=lcm(1728,*(c.denominator for c in h));num=tuple(int(c*den) for c in h);factor=den//1728
            for p0,p1 in I[X[i]]:
                for q0,q1 in J[Y[j]]:
                    e0,e1=p0*214+q0,p1*214+q1
                    if e0>=e1:continue
                    key=canonical(den,[a+factor*b for a,b in zip(num,z[e0])]);hits+=1
                    if key in overlap:overlap_hits+=1;seen_overlaps.add(key);continue
                    if key not in translated:translated[key]={e0,e1}
                    else:translated[key].update((e0,e1))
    rows=[(key,sorted(ee)) for key,ee in sorted(translated.items())]
    return rows,{'pair_intersection_events':hits,'overlap_events':overlap_hits,'overlap_translations':len(seen_overlaps)}

def digest(obj):return sha256((json.dumps(obj,separators=(',',':'))+'\n').encode()).hexdigest()
def positive_json(positive):return [[i,j,[F.encode(h) for h in hs]] for i,j,hs in positive]
