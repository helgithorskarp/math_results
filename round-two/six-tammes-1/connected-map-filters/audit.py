"""Independent algorithm, SAME AUTHOR: sparse identities, Bernstein products,
cut-mask profiles, Gaussian supporting planes and union-find trees.
No producer imports, third-party libraries or floating-point predicates.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parent
LO,HI=F(1,2),F(5,7)


def need(condition,message):
    if not condition:raise ValueError(message)


def poly(values):
    return {i:F(x) for i,x in enumerate(values) if F(x)}


def add(a,b):
    out=dict(a)
    for i,x in b.items():out[i]=out.get(i,F(0))+x
    return {i:x for i,x in out.items() if x}


def neg(a):return {i:-x for i,x in a.items()}


def mul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return {i:x for i,x in out.items() if x}


ZERO=({}, {0:F(1)})
ONE=({0:F(1)}, {0:F(1)})
C=({1:F(1)}, {0:F(1)})
H=({0:F(1),1:F(2)}, {0:F(1)})


def plus(a,b):return add(mul(a[0],b[1]),mul(b[0],a[1])),mul(a[1],b[1])
def minus(a,b):return plus(a,(neg(b[0]),b[1]))
def times(a,b):return mul(a[0],b[0]),mul(a[1],b[1])
def divide(a,b):
    need(bool(b[0]),'nonzero rational divisor')
    return mul(a[0],b[1]),mul(a[1],b[0])
def scalar(k):return ({0:F(k)} if k else {},{0:F(1)})
def equal(a,b):return mul(a[0],b[1])==mul(b[0],a[1])
def peval(p,x):return sum(v*x**i for i,v in p.items())
def value(r,x):
    d=peval(r[1],x);need(d!=0,'no pole at evaluation')
    return peval(r[0],x)/d


def rational(obj):
    need(isinstance(obj,dict) and set(obj)=={'numerator','denominator'},'rational schema')
    n,d=poly(obj['numerator']),poly(obj['denominator'])
    need(bool(d) and all(x>0 for x in d.values()),'positive polynomial denominator on c>0')
    return n,d


def elevate(b,degree):
    b=list(b)
    while len(b)-1<degree:
        d=len(b)-1
        b=[(F(j,d+1)*b[j-1] if j else 0)+
           ((1-F(j,d+1))*b[j] if j<=d else 0) for j in range(d+2)]
    return b


def bproduct(a,b):
    m,n=len(a)-1,len(b)-1
    out=[F(0)]*(m+n+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y*F(comb(m,i)*comb(n,j),comb(m+n,i+j))
    return out


def bernstein(p):
    degree=max(p,default=0);powers=[[F(1)]]
    for _ in range(degree):powers.append(bproduct(powers[-1],[LO,HI]))
    out=[F(0)]*(degree+1)
    for i,x in p.items():
        term=elevate(powers[i],degree)
        out=[a+x*b for a,b in zip(out,term)]
    return out


def shifted_derivative(p):
    """Taylor coefficients of p'(LO+z); z>=0 throughout the interval."""
    d=max(p,default=0)
    return [sum(v*i*comb(i-1,k)*LO**(i-1-k)
                for i,v in p.items() if i>k) for k in range(d)]


def check_sign(p,encoded,increasing=False):
    bs=bernstein(p)
    need(bs==list(map(F,encoded)) and all(x<0 for x in bs),'bound Bernstein entries')
    ds=shifted_derivative(p)
    if increasing:
        need(bool(ds) and ds[0]>0 and all(x>=0 for x in ds),'positive derivative expansion')
        need(peval(p,HI)<0,'negative right maximum')
    else:
        need(bool(ds) and ds[0]<0 and all(x<=0 for x in ds),'negative derivative expansion')
        need(peval(p,LO)<0,'negative left maximum')


def check_cases(rows):
    need(len(rows)==6,'all six endpoint types')
    keyed={(r['t'],r['s']):r for r in rows}
    need(len(keyed)==6 and set(keyed)=={(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)},'literal complete type domain')
    direct={1:ONE,2:divide(C,H),3:divide(minus(C,ONE),plus(ONE,times(scalar(3),C)))}
    divisors={(1,1):times(H,plus(ONE,C)),
        (1,2):times(plus(ONE,C),plus(ONE,C)),
        (1,3):divide(times(H,times(plus(ONE,C),plus(ONE,C))),plus(ONE,times(scalar(3),C))),
        (2,2):times(C,plus(ONE,C)),
        (2,3):divide(times(scalar(2),times(times(C,C),plus(ONE,C))),plus(ONE,times(scalar(3),C))),
        (3,3):divide(times(H,times(minus(C,ONE),plus(ONE,C))),plus(ONE,times(scalar(3),C)))}
    numerators={1:poly([1,-6,-7]),2:poly([1,0,-11,-6]),3:poly([1,8,-2,-40,-15])}
    denominators={1:H,2:times(plus(ONE,C),plus(ONE,C)),3:times(H,times(plus(ONE,C),plus(ONE,C)))}
    for key,row in keyed.items():
        t,s=key
        bt,bs=rational(row['B_t_over_A']),rational(row['B_s_over_A'])
        need(equal(bt,direct[t]) and equal(bs,direct[s]),'direct cotangent values')
        determinant=times(H,plus(bt,times(C,bs)))
        need(equal(determinant,divisors[key]),'nonvanishing signed star determinant')
        sigma,p=rational(row['S_over_A']),rational(row['P'])
        d,l,u=(rational(row[k]) for k in ('discriminant','lower_gap_product','upper_gap_product'))
        need(equal(plus(p,times(H,times(bt,sigma))),ONE),'first functional star')
        need(equal(minus(p,times(C,C)),times(C,times(H,times(bs,sigma)))),'second functional star')
        need(equal(d,minus(times(H,times(sigma,sigma)),times(scalar(4),p))),'discriminant binding')
        need(equal(l,plus(minus(divide(times(C,C),H),times(C,sigma)),p)),'lower x,y bound binding')
        need(equal(u,plus(minus(H,times(H,sigma)),p)),'upper x,y bound binding')
        ob=row['obstruction'];r=rational(ob['rational'])
        if t==1:
            target=divide((numerators[s],{0:F(1)}),denominators[s])
            need(ob['kind']=='negative_discriminant' and equal(r,d) and equal(d,target),'case1 discriminant obstruction')
            check_sign(r[0],ob['Bernstein_numerator'])
        elif key==(2,2):
            factor=divide(times(scalar(-1),times(minus(times(scalar(2),C),ONE),times(plus(ONE,C),plus(ONE,C)))),times(C,C))
            need(ob['kind']=='strict_above_lower_endpoint' and equal(r,d) and equal(d,factor),'case22 exact factor')
            need(ob['factor']=='-(2c-1)(1+c)^2/c^2' and
                F(ob['exception_c'])==LO and F(ob['exception_P'])==LO and
                F(ob['exception_S_over_A'])==1 and F(ob['exception_x_equals_y_squared'])==LO,'true lower endpoint exception')
            need(value(d,LO)==0 and value(p,LO)==LO and value(sigma,LO)==1,'endpoint algebra')
        elif key==(2,3):
            n=rational(ob['numerator']);expected=(poly([-1,-3,1,7]),{0:F(1)})
            need(ob['kind']=='negative_lower_gap_product' and equal(r,l) and equal(n,expected),'case23 literal lower obstruction')
            need(equal(l,divide(expected,times(C,H))),'case23 denominator')
            check_sign(expected[0],ob['Bernstein_numerator'],increasing=True)
        else:
            target=divide(times(scalar(-1),plus(ONE,times(scalar(3),C))),H)
            need(ob['kind']=='negative_sum' and equal(r,sigma) and equal(sigma,target),'case33 positivity contradiction')
            check_sign(r[0],ob['Bernstein_numerator'])


def solve_plane(rows):
    a=[list(map(F,row))+[F(1)] for row in rows]
    for j in range(3):
        choices=[i for i in range(j,3) if a[i][j]]
        if not choices:return None
        k=choices[-1];a[j],a[k]=a[k],a[j]
        scale=a[j][j];a[j]=[x/scale for x in a[j]]
        for i in range(3):
            if i!=j:
                scale=a[i][j];a[i]=[x-scale*y for x,y in zip(a[i],a[j])]
    return tuple(a[i][3] for i in range(3))


class Union:
    def __init__(self,items):self.parent={i:i for i in items}
    def root(self,x):
        while self.parent[x]!=x:x=self.parent[x]
        return x
    def join(self,a,b):
        a,b=self.root(a),self.root(b)
        if a==b:return False
        self.parent[a]=b;return True
    def groups(self):
        out={}
        for x in self.parent:out.setdefault(self.root(x),set()).add(x)
        return list(out.values())


def check_calibration(data):
    labels=['E'+str(i) for i in range(6)]+['U'+str(i) for i in range(3)]+['L'+str(i) for i in range(3)]
    expected=[(1,0,0),(F(1,2),F(1,2),0),(-F(1,2),F(1,2),0),(-1,0,0),
        (-F(1,2),-F(1,2),0),(F(1,2),-F(1,2),0),
        (F(1,2),F(1,6),F(1,3)),(-F(1,2),F(1,6),F(1,3)),(0,-F(1,3),F(1,3)),
        (F(1,2),F(1,6),-F(1,3)),(-F(1,2),F(1,6),-F(1,3)),(0,-F(1,3),-F(1,3))]
    ps=[tuple(map(F,row)) for row in data['scaled_points']]
    need(data['labels']==labels and ps==expected and data['coordinate_metric']==[1,3,6] and F(data['c'])==LO,'literal endpoint coordinates')
    point=dict(zip(labels,ps));weights=[F(1),F(3),F(6)]
    def linear(a,b):return sum(x*y for x,y in zip(a,b))
    def gram(a,b):return sum(w*x*y for w,x,y in zip(weights,point[a],point[b]))
    full=[[gram(a,b) for b in labels] for a in labels]
    need(full==[list(map(F,row)) for row in data['Gram']],'all144 Gram entries')
    need(all(full[i][i]==1 for i in range(12)) and all(full[i][j]<=LO for i,j in combinations(range(12),2)),'unit packing')
    edges={frozenset((a,b)) for a,b in combinations(labels,2) if gram(a,b)==LO}
    need(len(edges)==24 and data['contacts']==24 and data['strict_noncontacts']==42,'24 contacts42 strict noncontacts')
    need(all(sum(p[j] for p in ps)==0 for j in range(3)),'positive zero barycenter')
    planes={};triples=0
    for triple in combinations(labels,3):
        triples+=1;n=solve_plane([point[v] for v in triple])
        if n is None:continue
        if all(linear(n,p)<=1 for p in ps):
            vertices=frozenset(v for v in labels if linear(n,point[v])==1)
            need(len(vertices) in (3,4),'supporting facet type')
            planes[vertices]=n
    need(triples==220 and len(planes)==14,'all supporting triples/full-dimensional hull')
    encoded={}
    for record in data['supporting_planes']:
        key=frozenset(record['vertices']);k=F(record['constant']);n=tuple(map(F,record['normal']))
        need(len(key)==len(record['vertices']) and k>0 and len(n)==3 and key not in encoded,'support plane domain')
        encoded[key]=tuple(x/k for x in n)
    need(encoded==planes,'whole Gaussian facet plane comparison')
    faces=data['faces'];face_keys=[frozenset(f) for f in faces]
    need(len(faces)==14 and len(set(face_keys))==14 and set(face_keys)==set(planes),'whole actual facet domain')
    boundaries={}
    for f in faces:
        key=frozenset(f);need(len(key)==len(f),'simple face boundary')
        es={frozenset((f[i],f[(i+1)%len(f)])) for i in range(len(f))}
        expected_es={frozenset((a,b)) for a,b in combinations(f,2) if gram(a,b)==LO}
        need(len(es)==len(f) and es==expected_es,'exact convex facet boundary/contact edges')
        if len(f)==4:
            need(all(gram(a,b)==0 for a,b in combinations(f,2) if frozenset((a,b)) not in es),'six spherical square facets')
        boundaries[key]=es
    need(set().union(*boundaries.values())==edges and data['T_Q_counts']==[8,6],'contacts exactly hull1-skeleton')
    qfaces={k for k in planes if len(k)==4};tfaces={k for k in planes if len(k)==3}
    qgroups=Union(qfaces);tgroups=Union(tfaces);tt=[];qq=[]
    for a,b in combinations(qfaces,2):
        if a&b:qgroups.join(a,b)
    need(len(qgroups.groups())==1 and set().union(*qfaces)==set(labels),'Jordan premise calibration')
    for edge in edges:
        incident=[k for k,es in boundaries.items() if edge in es]
        need(len(incident)==2,'each edge exactly two actual faces')
        a,b=incident
        if len(a)==len(b)==3:
            need(tgroups.join(a,b),'TT forest no union-find cycle');tt.append((a,b))
        if len(a)==len(b)==4:
            stars=[sorted(len(k) for k in planes if v in k) for v in sorted(edge)]
            need(stars==[[3,3,4,4],[3,3,4,4]],'TTQQ endpoint face stars')
            qq.append({'edge':sorted(edge),'endpoint_face_sizes':stars})
    expected_qq={tuple(r['edge']):r['endpoint_face_sizes'] for r in qq}
    got_qq={tuple(sorted(r['edge'])):r['endpoint_face_sizes'] for r in data['QQ_edges']}
    need(len(data['QQ_edges'])==3 and len(got_qq)==3 and got_qq==expected_qq,'whole QQ countercalibration')
    need(len(tt)==3 and data['NN_edges']==3 and data['TT_edges']==3,'calibration seams')
    expected_components={}
    for group in tgroups.groups():
        key=frozenset(group);vertices=set().union(*group)
        count=sum(a in group and b in group for a,b in tt)
        need(count==len(group)-1 and len(vertices)<=len(group)+2,'component tree/support bound')
        expected_components[key]=(frozenset(vertices),len(group),count)
    encoded_components={}
    for r in data['triangle_components']:
        key=frozenset(frozenset(t) for t in r['triangles'])
        need(key not in encoded_components and len(key)==len(r['triangles']),'component domain')
        encoded_components[key]=(frozenset(r['vertices']),r['faces'],r['TT_edges'])
    need(encoded_components==expected_components and sorted(len(g) for g in tgroups.groups())==[1,1,2,2,2],'all triangle components')


def check_profiles(data):
    expected_blocks=[{frozenset(t) for t in ((0,5,11),(0,6,11),(0,5,7),(5,9,11))},
                     {frozenset(t) for t in ((1,2,4),(2,4,8),(1,2,10),(1,10,12))}]
    blocks=[{frozenset(t) for t in b} for b in data['triangles']]
    need(blocks==expected_blocks and all(len(b)==4 for b in data['triangles']),'exact eight-face motif')
    supports=[];edges=set()
    for block in blocks:
        ids=list(block);u=Union(range(4));degrees=[0]*4
        for i,j in combinations(range(4),2):
            if len(ids[i]&ids[j])==2:u.join(i,j);degrees[i]+=1;degrees[j]+=1
        need(len(u.groups())==1 and sorted(degrees) in ([1,1,1,3],[1,1,2,2]),'connected literal cluster')
        supports.append(set().union(*block))
        edges|={frozenset(e) for tri in block for e in combinations(tri,2)}
    need([sorted(s) for s in supports]==data['cluster_supports'] and
        len(supports[0])==len(supports[1])==6 and not(supports[0]&supports[1]),'twelve injective vertices')
    need(len(edges)==18 and len(data['prescribed_edges'])==18 and
        {frozenset(e) for e in data['prescribed_edges']}==edges,'literal eighteen-edge interface')
    parts=set()
    for mask in range(1<<10):
        chunks=[];last=0
        for j in range(1,11):
            if mask&(1<<(j-1)):chunks.append(j-last);last=j
        chunks.append(11-last);parts.add(tuple(sorted(chunks)))
    need(len(parts)==56 and data['all_partitions_11']==56,'complete cut-mask domain')
    domain={p for p in parts if len(p)<=8};encoded={}
    for row in data['rows']:
        key=tuple(sorted(row['component_sizes']))
        need(key not in encoded and sum(key)==11 and all(x>0 for x in key),'profile domain')
        encoded[key]=row
    need(set(encoded)==domain and len(domain)==52 and data['cohort_profile_count']==52,'all52 entry-level profiles')
    eligible=set()
    for key,row in encoded.items():
        need(row['NN_edges']==8-len(key) and row['TT_edges']==11-len(key),'edge/component Euler counts')
        possible=any(f+2>=12 for f in key) or any(key[i]>=4 and key[j]>=4 for i,j in combinations(range(len(key)),2))
        need(type(row['motif_size_condition']) is bool and row['motif_size_condition']==possible,'necessary size condition')
        if possible:eligible.add(key)
    listed={tuple(sorted(p)) for p in data['motif_compatible_profiles']}
    need(listed==eligible and len(data['motif_compatible_profiles'])==11 and len(eligible)==11 and
        data['motif_incompatible_profiles']==41,'whole eleven-profile interface')
    need(data['not_sufficient_for_occurrence'] is True and data['no_profile_excludes_packings'] is True,'necessary-only trust boundary')


def verify(obj):
    need(obj['schema']=='tammes-connected-map-filters-v1' and
        list(map(F,obj['algebraic_closed_band']))==[LO,HI] and
        obj['local_conclusion_lower_strict'] is True and obj['local_upper_included'] is True,'theorem domain/strict endpoint')
    check_cases(obj['QQ_cases']);check_calibration(obj['endpoint_calibration'])
    check_profiles(obj['triangle_forest_profiles'])
    return True


def main():
    parser=argparse.ArgumentParser();parser.add_argument('certificate',nargs='?',type=Path,default=ROOT/'CERTIFICATE.json')
    args=parser.parse_args();data=args.certificate.read_bytes();verify(json.loads(data))
    print(json.dumps({'verified':True,'QQ_cases':6,'Gaussian_facet_triples':220,
        'calibration_Gram_entries':144,'calibration_QQ_edges':3,
        'cut_masks':1024,'forest_profiles':52,'motif_compatible':11,
        'motif_incompatible':41,'sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
