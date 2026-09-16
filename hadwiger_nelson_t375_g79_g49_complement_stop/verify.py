#!/usr/bin/env python3
"""Solver-free exact reconstruction using integral squarefree-radicand arithmetic.
No producer or sibling executable source is imported. Coordinates are /4608.
"""
import argparse,hashlib,json,math
from itertools import combinations,product
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_small_triangle_forcer375'
RAD=(1,3,11,33,247,741,2717,8151)
RI={r:i for i,r in enumerate(RAD)}
ZERO=(0,)*8
SCALE=4608
TERMS=[]
for i in range(8):
    for j in range(i,8):
        g=math.gcd(RAD[i],RAD[j]);TERMS.append((i,j,RI[RAD[i]*RAD[j]//(g*g)],g*(1 if i==j else 2)))


def need(ok,msg):
    if not ok:raise ValueError(msg)


def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def scale(a,t):return tuple(t*x for x in a)
def radical(a,r):
    out=[0]*8
    for i,c in enumerate(a):
        g=math.gcd(RAD[i],r);out[RI[RAD[i]*r//(g*g)]]+=c*g
    return tuple(out)

def row(p):
    a,b,c,d=p
    return (0,a,b,0,0,0,0,0),(c,0,0,d,0,0,0,0)

def pairscale(p,t):return scale(p[0],t),scale(p[1],t)
def final_frame(p):return p[0],add((3072,0,0,0,0,0,0,0),neg(p[1]))
def normdiff(p,q):
    x=tuple(a-b for a,b in zip(p[0],q[0]));y=tuple(a-b for a,b in zip(p[1],q[1]));out=[0]*8
    for i,j,k,f in TERMS:out[k]+=f*(x[i]*x[j]+y[i]*y[j])
    return tuple(out)

def edges(points):return [[i,j] for i,j in combinations(range(len(points)),2) if normdiff(points[i],points[j])==(SCALE*SCALE,0,0,0,0,0,0,0)]


def input_data():
    pins=[(0,0,12,0),(-6,0,-6,0),(6,0,-6,0)]
    expected=json.loads((HERE/'DEPENDENCIES.json').read_text());data={}
    for name,h in expected.items():
        b=(SOURCE/name).read_bytes();need(hashlib.sha256(b).hexdigest()==h,'pinned input '+name);data[name]=json.loads(b)
    orbit=set(map(tuple,data['appendix.json']));front=list(orbit)
    while front:
        a,b,c,d=front.pop();rr=(-a-c,-b-3*d,3*a-c,b-d)
        need(all(t%2==0 for t in rr),'integral120 rotation')
        for t in (tuple(t//2 for t in rr),(-a,-b,c,d)):
            if t not in orbit:orbit.add(t);front.append(t)
    need(len(orbit)==627 and set(pins)<=orbit,'parent orbit')
    reference=pins+sorted(orbit-set(pins));indices=data['certificate.json']['retained_reference_indices']
    need(len(indices)==375 and indices==sorted(set(indices)) and indices[:3]==[0,1,2],'frozen host labels')
    native=[reference[i] for i in indices]
    need(digest(native)=='0bf15083801eb6fa982b04e820aca6c5a16c9b75b2d85b3efd00c53716edb1fe','parent native points')
    return data,[pairscale(row(p),128) for p in native]


def geometry():
    data,host=input_data();pins=host[:3];base40=list(map(row,data['g40.json']));base49=list(map(row,data['g49.json']))
    need(len(base40)==40 and len(base49)==49,'source orders')
    P=row((0,0,30,-6));Q=row((0,0,30,6));need(P in base40 and Q in base40,'frozen anchors')
    orig={pairscale(p,128) for p in base40}
    rotated={(add(scale(x,119),scale(radical(y,247),-3)),add(scale(radical(x,247),3),scale(y,119))) for x,y in base40}
    g79=orig|rotated;need(len(g79)==79 and len(orig&rotated)==1,'exact79 construction')
    p49=[final_frame(pairscale((add(x,P[0]),add(y,P[1])),128)) for x,y in base49]
    p79={final_frame(p) for p in g79};need([p49[i] for i in [4,2,3]]==pins,'three exact receiving pins')
    need(normdiff(pairscale(P,128),pairscale(Q,128))==(4752*128*128,0,0,0,0,0,0,0),'named pair metric')
    need(len(p79&set(p49))==2,'two source overlaps')
    cset=p79|set(p49);comp=pins+sorted(cset-set(pins));union=host+sorted(cset-set(host))
    need(len(set(comp))==len(comp)<=136 and len(set(union))==len(union)<=508,'physical distinctness and caps')
    need(all(normdiff(pins[i],pins[j])==(SCALE*SCALE//3,0,0,0,0,0,0,0) for i,j in combinations(range(3),2)),'side1/sqrt3 pins')
    ce=edges(comp);ue=edges(union);he=[e for e in ue if e[1]<375]
    need(len(he)==1661 and digest(he)=='0e3d04cf0e0df94e9a7a9adda6677d92db162faf3ab29947dde8e0f52c287660','complete host edges')
    idx={p:i for i,p in enumerate(union)};cmap=[idx[p] for p in comp]
    inherited={tuple(e) for e in he}|{tuple(sorted((cmap[i],cmap[j]))) for i,j in ce}
    extra=[e for e in ue if tuple(e) not in inherited]
    outside=[i for i,p in enumerate(comp) if any(p[k][j] for k in (0,1) for j in range(4,8))]
    return host,comp,union,ce,ue,cmap,extra,outside


def colour(word,n,es):
    need(isinstance(word,list) and len(word)==n and all(type(c)==int and 0<=c<4 for c in word),'four-word domain')
    need(all(word[i]!=word[j] for i,j in es),'every strict edge bichromatic')


def verify(cert,geom=None):
    host,comp,union,ce,ue,cmap,extra,outside=geometry() if geom is None else geom
    need(cert['schema']=='hn-t375-g79-g49-one-complement-v1' and cert['scale']==SCALE,'certificate schema')
    need(cert['complement_points']==len(comp) and cert['union_points']==len(union),'orders')
    need(cert['complement_edges']==len(ce) and cert['union_edges']==len(ue),'edge counts')
    need(cert['overlap_count']==len(set(host)&set(comp)),'complete overlap')
    for k,x in [('complement_point_sha256',comp),('union_point_sha256',union),('complement_edge_sha256',ce),('union_edge_sha256',ue)]:need(cert[k]==digest(x),'full exact stream '+k)
    need(cert['complement_to_union']==cmap,'component embedding')
    need(cert['extra_cross_edges']==extra,'all incidental cross contacts')
    need(cert['outside_native_field_indices']==outside and len(outside)>0,'outside registered native-field closure')
    colour(cert['union_colour_word'],len(union),ue);colour(cert['complement_colour_word'],len(comp),ce)
    need([cert['union_colour_word'][i] for i in cmap]==cert['complement_colour_word'],'restriction word')
    need(cert['pins']==cert['union_colour_word'][:3] and len(set(cert['pins']))>1,'nonmonochromatic extension')
    need(cert['record_candidate'] is False,'honest non-candidate status')
    return {'status':'PASS','complement_points':len(comp),'complement_complete_edges':len(ce),'union_points':len(union),'union_complete_edges':len(ue),'overlaps':len(set(host)&set(comp)),'incidental_cross_edges':len(extra),'outside_native_field_points':len(outside),'checked_pin_colours':cert['pins'],'ordinary_four_colourable':True,'monochromatic_complement_forcing':False,'record_candidate':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');p.add_argument('--export',type=Path);a=p.parse_args()
    geom=geometry();r=verify(json.loads(a.certificate.read_text()),geom)
    if a.check_expected:need(r==json.loads((HERE/'EXPECTED.json').read_text()),'expected summary')
    if a.export:
        a.export.mkdir(parents=True,exist_ok=True);_,c,u,ce,ue,*_=geom
        for name,x in [('complement_points',c),('union_points',u),('complement_edges',ce),('union_edges',ue)]:
            (a.export/(name+'.json')).write_text(json.dumps(x,separators=(',',':'))+'\n')
    print(json.dumps(r,indent=2,sort_keys=True))
