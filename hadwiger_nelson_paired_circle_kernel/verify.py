"""Independent exact intersection-count and direct list-colouring audit."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
from collections import Counter
import argparse,copy,hashlib,json,math,time
HERE=Path(__file__).resolve().parent
PRIMES=(3,5,7,11,13)
RAD=tuple(math.prod(p for k,p in enumerate(PRIMES) if mask&(1<<k)) for mask in range(32))
RID={r:i for i,r in enumerate(RAD)}
Z=(0,)*32
ONE=(1,)+(0,)*31
ROOTS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
CROSS=((0,2),(0,3),(1,2),(1,3))
def require(ok,why):
    if not ok:raise ValueError(why)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(x*k for x in a)
def mul(a,b):
    out=[0]*32
    aa=[(i,x) for i,x in enumerate(a) if x];bb=[(j,y) for j,y in enumerate(b) if y]
    for i,x in aa:
        for j,y in bb:out[i^j]+=x*y*RAD[i&j]
    return tuple(out)
def cplus(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def cminus(a,b):return minus(a[0],b[0]),minus(a[1],b[1])
def cmul(a,b):return minus(mul(a[0],b[0]),mul(a[1],b[1])),plus(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(z):return plus(mul(z[0],z[0]),mul(z[1],z[1]))
def dist(a,b):return norm(cminus(a,b))
def divide(z,q):
    require(all(x%q==0 for axis in z for x in axis),'integral coordinate scaling')
    return tuple(tuple(x//q for x in axis) for axis in z)
def decode(z):
    require(isinstance(z,list) and len(z)==2,'two coordinate axes')
    result=[]
    for axis in z:
        require(isinstance(axis,list),'coordinate array')
        out=[Fraction(0)]*32;seen=[]
        for triple in axis:
            require(isinstance(triple,list) and len(triple)==3 and all(type(x)is int for x in triple),'rational coordinate triple')
            r,n,d=triple
            require(r in RID and d>0 and n!=0 and math.gcd(n,d)==1,'canonical radical coefficient')
            require(r not in seen,'unique radical coefficient');seen.append(r);out[RID[r]]=Fraction(n,d)
        require(seen==sorted(seen),'sorted radicals')
        result.append(tuple(out))
    return tuple(result)
def sortkey(z,q):
    return tuple(tuple((r,Fraction(axis[RID[r]],q)) for r in sorted(RID) if axis[RID[r]]) for axis in z)
def encode(z,q):
    return [[[r,x.numerator,x.denominator] for r,x in axis] for axis in sortkey(z,q)]
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def case_audit(row):
    m,n=row['translation']
    encoded=row['cross_intersections'];require(len(encoded)==4,'all four cross pairs')
    decoded=[[decode(z) for z in points] for points in encoded]
    q=2*math.lcm(2,*(f.denominator for row in decoded for point in row for axis in point for f in axis))
    I=[[tuple(tuple(int(q*f) for f in axis) for axis in z) for z in row] for row in decoded]
    D=[(Z,Z),(scale(ONE,q),Z),(scale(ONE,m*q//2),scale(ONE,n*q//2)),(scale(ONE,(m+2)*q//2),scale(ONE,n*q//2))]
    require(len(set(D))==4,'distinct centres')
    unit=scale(ONE,q*q)
    require(dist(D[0],D[1])==dist(D[2],D[3])==unit,'unit centre pairs')
    icount=Counter();intersection_points=0
    for (a,b),points in zip(CROSS,I):
        dd=dist(D[a],D[b])
        require(dd[1:]==Z[1:] and dd[0]>0,'rational nonzero centre separation')
        count=0 if dd[0]>4*q*q else 1 if dd[0]==4*q*q else 2
        require(len(points)==len(set(points))==count,'complete circle-intersection count')
        for z in points:
            require(dist(z,D[a])==dist(z,D[b])==unit,'intersection point lies on both circles')
        if count:
            endpoints=cplus(points[0],points[-1])
            require(endpoints==cplus(D[a],D[b]),'antipodal intersection identity')
        icount[count]+=1;intersection_points+=len(points)
    roots=[]
    for a,b in ROOTS:
        roots.append((scale(ONE,(2*a+b)*q//2),tuple(b*q//2 if i==RID[3] else 0 for i in range(32))))
    S=[set(roots),set(roots)]
    for (a,b),points in zip(CROSS,I):
        for z in points:
            for g,d in ((0,a),(1,b)):
                direction=cminus(z,D[d])
                for r in roots:S[g].add(divide(cmul(direction,r),q))
    require(S[0]==S[1],'parallel common-direction identity')
    require([len(s) for s in S]==row['directions'] and all(len(s)<=42 and len(s)%6==0 for s in S),'parallel seven-orbit bound')
    V=sorted({cplus(d,r) for h,d in enumerate(D) for r in S[h//2]},key=lambda z:sortkey(z,q))
    require(len(V)==row['vertices'] and len(V)<=156,'complete actual patch')
    require(digest([encode(z,q) for z in V])==row['point_sha256'],'canonical point stream')
    idx={z:i for i,z in enumerate(V)};ci=[idx[d] for d in D]
    E=[(a,b) for a,b in combinations(range(len(V)),2) if dist(V[a],V[b])==unit]
    require(len(E)==row['edges'] and digest(E)==row['edge_sha256'],'complete unit-edge stream')
    owners=[{h for h,d in enumerate(D) if dist(z,d)==unit} for z in V]
    masks=[];boundary_directions=0;mixed=0
    for i,own in enumerate(owners):
        require(bool(own),'every patch point owned')
        if i in ci:mask=1<<(2,3,0,1)[ci.index(i)]
        elif own<={0,1}:mask=3
        elif own<={2,3}:mask=12
        else:mask=15;mixed+=1
        masks.append(mask)
        if i not in ci:
            for h in own:
                require(cminus(V[i],D[h]) in S[h//2],'every owner direction in its group orbit set')
                boundary_directions+=1
    require(''.join(format(a,'x') for a in masks)==row['lists'],'owner-group lists and centre pins')
    colours=row['colouring']
    require(isinstance(colours,str) and len(colours)==len(V) and all(c in '0123' for c in colours),'colour string')
    c=list(map(int,colours))
    require(all(mask&(1<<colour) for mask,colour in zip(masks,c)),'every allowed list')
    require(all(c[a]!=c[b] for a,b in E),'all positive edge inequalities')
    return {'translation':[m,n],'scale':q,'vertices':len(V),'edges':len(E),'directions':len(S[0]),
            'intersection_histogram':{str(k):v for k,v in sorted(icount.items())},'intersection_points':intersection_points,
            'pair_norms':len(V)*(len(V)-1)//2,'owner_direction_checks':boundary_directions,
            'mixed_owner_noncentres':mixed,'point_sha256':row['point_sha256'],'edge_sha256':row['edge_sha256']}

def audit(data):
    require(data['translation_denominator']==2,'frozen denominator')
    cases=[(m,n) for m in range(5) for n in range(5) if (m,n) not in [(0,0),(2,0),(0,2)]]
    require([row['translation'] for row in data['cases']]==list(map(list,cases)),'complete twenty-two canonical cases')
    results=[case_audit(row) for row in data['cases']]
    # Verify the finite symmetry quotient and the three inherited classes.
    representatives=Counter();inherited=Counter()
    for m,n in product(range(-4,5),repeat=2):
        t=(abs(m),abs(n))
        if t in [(0,0),(2,0)]:inherited['coincident']+=1
        elif t==(0,2):inherited['unit_rhombus']+=1
        else:
            require(t in cases,'complete symmetry quotient');representatives[t]+=1
    require(sum(representatives.values())==76 and dict(inherited)=={'coincident':3,'unit_rhombus':2},'all eighty-one translations')
    hist=Counter()
    for row in results:hist.update({int(k):v for k,v in row['intersection_histogram'].items()})
    return {'status':'PASS','canonical_new_placements':22,'signed_new_placements':76,
            'inherited_coincident_placements':3,'inherited_rhombus_placements':2,'total_signed_placements':81,
            'general_kernel_vertex_bound':204,'parallel_kernel_vertex_bound':156,
            'parallel_bound_attained':max(r['vertices'] for r in results)==156,
            'max_observed_vertices':max(r['vertices'] for r in results),'max_observed_direction_orbits':max(r['directions']//6 for r in results),
            'cross_circle_pair_checks':88,'cross_intersection_count_histogram':{str(k):v for k,v in sorted(hist.items())},
            'cross_intersection_point_checks':sum(r['intersection_points'] for r in results),
            'actual_patch_pair_norms':sum(r['pair_norms'] for r in results),
            'positive_patch_edge_checks':sum(r['edges'] for r in results),
            'patch_owner_direction_checks':sum(r['owner_direction_checks'] for r in results),
            'mixed_owner_noncentre_checks':sum(r['mixed_owner_noncentres'] for r in results),
            'staircase':next(r for r in results if r['translation']==[2,2]),
            'all_frozen_supports_four_colourable':True,'criterion_is_only_sufficient':True,
            'native_solver_calls':0,'cases':results}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);ap.add_argument('--discover',action='store_true')
    args=ap.parse_args();w=Path(args.work);start=time.monotonic()
    certificate=(w/'certificate.json').read_bytes()
    require(certificate==(HERE/'certificate.json').read_bytes(),'published certificate bytes')
    data=json.loads(certificate);report=audit(data)
    mutants=[]
    bad=copy.deepcopy(data);bad['cases'].pop();mutants.append(bad)
    bad=copy.deepcopy(data);bad['cases'][0]['cross_intersections'][0].pop();mutants.append(bad)
    bad=copy.deepcopy(data);bad['cases'][0]['cross_intersections'][0][0][0][0][1]+=2*bad['cases'][0]['cross_intersections'][0][0][0][0][2];mutants.append(bad)
    bad=copy.deepcopy(data);bad['cases'][0]['point_sha256']='0'*64;mutants.append(bad)
    bad=copy.deepcopy(data);bad['cases'][0]['colouring']='0'*len(bad['cases'][0]['colouring']);mutants.append(bad)
    bad=copy.deepcopy(data);bad['cases'][0]['lists']='0'*len(bad['cases'][0]['lists']);mutants.append(bad)
    rejected=0
    for bad in mutants:
        try:audit(bad)
        except ValueError:rejected+=1
        else:raise ValueError('malformed certificate accepted')
    report.update(malformed_certificate_rejections=rejected,certificate_bytes=len(certificate),certificate_sha256=hashlib.sha256(certificate).hexdigest())
    if not args.discover:require(report==json.loads((HERE/'expected.json').read_text()),'expected report')
    w.joinpath('verification.json').write_text(json.dumps(report,indent=2)+'\n')
    w.joinpath('timing.json').write_text(json.dumps({'seconds':time.monotonic()-start},indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},sort_keys=True),flush=True)
if __name__=='__main__':main()
