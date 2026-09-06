"""Independent dense-integer exact geometry and transversal-colouring audit."""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
from collections import Counter
import argparse,copy,hashlib,json,math,time
HERE=Path(__file__).resolve().parent
PRIMES=(3,19)
RAD=tuple(math.prod(p for k,p in enumerate(PRIMES) if mask&(1<<k)) for mask in range(4))
RID={r:i for i,r in enumerate(RAD)}
Z=(0,)*4
ONE=(1,)+(0,)*3
ROOTS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
CROSS=((0,2),(0,3),(1,2),(1,3))
def require(ok,why):
    if not ok:raise ValueError(why)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(x*k for x in a)
def mul(a,b):
    out=[0]*4
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
        out=[Fraction(0)]*4;seen=[]
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
def audit(data):
    require(data['schema']==1 and data['orientation']==[[3,5],[4,5]] and data['translation']==[[1,5],[-2,5]],'fixed geometry')
    require(data['target_found'] is False and data['sharp_kernel_bound']==108,'claim scope')
    q=20;unit=scale(ONE,q*q)
    D=[(Z,Z),(scale(ONE,q),Z),(scale(ONE,4),scale(ONE,-8)),(scale(ONE,16),scale(ONE,8))]
    require(len(set(D))==4 and cplus(D[0],D[1])==cplus(D[2],D[3]),'common midpoint')
    require(dist(D[0],D[1])==dist(D[2],D[3])==unit,'unit diagonals')
    I=[];norms=[]
    require(len(data['cross_intersections'])==4,'all cross pairs')
    for (a,b),row in zip(CROSS,data['cross_intersections']):
        points=[]
        for encoded in row:
            z=decode(encoded)
            require(all((f*q).denominator==1 for axis in z for f in axis),'fixed integral scale')
            points.append(tuple(tuple(int(q*f) for f in axis) for axis in z))
        dd=dist(D[a],D[b]);require(dd[1:]==Z[1:] and 0<dd[0]<q*q,'strict cross centre distance')
        require(len(points)==len(set(points))==2,'complete two-circle intersection count')
        for z in points:require(dist(z,D[a])==dist(z,D[b])==unit,'intersection lies on both circles')
        require(cplus(*points)==cplus(D[a],D[b]),'two roots have correct midpoint')
        I.append(points);norms.append(Fraction(dd[0],q*q))
    roots=[]
    for a,b in ROOTS:
        roots.append((scale(ONE,(2*a+b)*q//2),tuple(b*q//2 if i==RID[3] else 0 for i in range(4))))
    def rotate(z,k):return divide(cmul(z,roots[k]),q)
    def orbit(z):return frozenset(rotate(z,k) for k in range(6))
    crossS=[set(),set()]
    for (a,b),row in zip(CROSS,I):
        for x in row:
            crossS[0].update(orbit(cminus(x,D[a])))
            crossS[1].update(orbit(cminus(x,D[b])))
    require(crossS[0]==crossS[1] and len(crossS[0])==24,'four common cross-direction orbits')
    directionB=cminus(D[3],D[2])
    S=[crossS[0]|set(roots),crossS[1]|set(orbit(directionB))]
    require([len(s) for s in S]==data['directions']==[30,30],'sharp intrinsic-orbit count')
    PA={cplus(D[h],u) for h in range(2) for u in S[0]}
    PB={cplus(D[h],u) for h in range(2,4) for u in S[1]}
    V=sorted(PA|PB,key=lambda z:sortkey(z,q));idx={z:i for i,z in enumerate(V)}
    require(len(PA)==len(PB)==58 and len(PA&PB)==8,'patch overlap counts')
    require(len(V)==data['vertices']==108 and digest([encode(z,q) for z in V])==data['point_sha256'],'actual kernel point stream')
    ci=[idx[d] for d in D];require(ci==data['centres'],'centre labels')
    E=[(a,b) for a,b in combinations(range(len(V)),2) if dist(V[a],V[b])==unit]
    require(len(E)==data['edges']==294 and digest(E)==data['edge_sha256'],'all exact unit edges')
    owners=[{h for h,d in enumerate(D) if dist(z,d)==unit} for z in V]
    require(all(1<=len(o)<=2 for o in owners),'one or two owners')
    mixed=sorted(idx[z] for z in PA&PB)
    require(len(mixed)==8 and all(v not in ci for v in mixed),'eight noncentre mixed points')
    pairs=sorted({tuple(sorted((v,idx[cminus(D[1],V[v])]))) for v in mixed})
    require(len(pairs)==4 and list(map(list,pairs))==data['cross_pairs'],'central pairs')
    pairsets=set(map(frozenset,pairs));cross_orbit_checks=0
    for g in range(2):
        classes={}
        for v in mixed:
            groupowners=[h for h in owners[v] if h//2==g]
            require(len(groupowners)==1,'unique owner in each group')
            h=groupowners[0];classes.setdefault(orbit(cminus(V[v],D[h])),set()).add(v)
        require(len(classes)==4 and {frozenset(v) for v in classes.values()}==pairsets,'only antipodal mixed points share a group orbit')
        cross_orbit_checks+=len(classes)
    masks=[];owner_checks=0
    for v,o in enumerate(owners):
        mask=1<<(2,3,0,1)[ci.index(v)] if v in ci else 3 if o<={0,1} else 12 if o<={2,3} else 15
        masks.append(mask)
        if v not in ci:
            for h in o:require(cminus(V[v],D[h]) in S[h//2],'owner direction present');owner_checks+=1
    require(''.join(format(m,'x') for m in masks)==data['lists'],'owner lists')
    rows=data['colourings'];require([row['transversal_mask'] for row in rows]==list(range(16)),'all sixteen transversals')
    phase_checks=0;edge_checks=0;prescriptions=0
    for mask,row in enumerate(rows):
        text=row['colouring'];require(isinstance(text,str) and len(text)==len(V) and all(c in '0123' for c in text),'colour string')
        c=list(map(int,text));require(all(m&(1<<z) for m,z in zip(masks,c)),'allowed lists and centre pins')
        require(all(c[a]!=c[b] for a,b in E),'proper full kernel');edge_checks+=len(E)
        selected={p[(mask>>j)&1] for j,p in enumerate(pairs)}
        for v in mixed:
            ai=next(h for h in owners[v] if h<2);bj=next(h for h in owners[v] if h>=2)-2
            want=1-bj if v in selected else 2+1-ai
            require(c[v]==want,'transversal prescribed colour');prescriptions+=1
        # Check the actual phase consistency using a different representative order.
        phase=[{},{}]
        for v,z in enumerate(V):
            if v in ci:continue
            g=c[v]//2
            for h in owners[v]:
                if h//2!=g:continue
                u=cminus(z,D[h]);orb=orbit(u);rep=min(orb)
                k=next(k for k in range(6) if rotate(rep,k)==u)
                alpha=(c[v]-2*g+h%2+k)%2
                require(rep not in phase[g] or phase[g][rep]==alpha,'single phase per direction orbit')
                phase[g][rep]=alpha;phase_checks+=1
    return {'status':'PASS','vertices':108,'edges':294,'kernel_bound':108,'bound_attained':True,
            'coordinate_scale':20,'field_basis':list(RAD),'cross_squared_centre_distances':[[x.numerator,x.denominator] for x in norms],
            'cross_intersection_points':8,'intersection_unit_norm_checks':16,'common_cross_direction_orbits':4,
            'cross_orbit_class_checks':cross_orbit_checks,'directions':[30,30],'paired_patch_sizes':[58,58],'patch_overlap':8,
            'actual_patch_pair_norms':len(V)*(len(V)-1)//2,'owner_direction_checks':owner_checks,
            'transversals':16,'positive_unit_edge_checks':edge_checks,'mixed_colour_prescriptions':prescriptions,'phase_consistency_checks':phase_checks,
            'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256'],'native_solver_calls':0,'target_found':False}

def reject_mutants(data):
    mutants=[]
    bad=copy.deepcopy(data);bad['cross_intersections'][0].pop();mutants.append(bad)
    bad=copy.deepcopy(data);bad['colourings'].pop();mutants.append(bad)
    bad=copy.deepcopy(data);bad['cross_intersections'][0][0][0][0][1]+=1;mutants.append(bad)
    bad=copy.deepcopy(data);bad['colourings'][0]['colouring']='0'*108;mutants.append(bad)
    bad=copy.deepcopy(data);bad['point_sha256']='0'*64;mutants.append(bad)
    bad=copy.deepcopy(data);bad['orientation'][0]=[2,5];mutants.append(bad)
    bad=copy.deepcopy(data);bad['cross_pairs'][0][0]+=1;mutants.append(bad)
    bad=copy.deepcopy(data);bad['sharp_kernel_bound']=107;mutants.append(bad)
    for n,bad in enumerate(mutants):
        try:audit(bad)
        except ValueError:continue
        raise ValueError('malformed certificate accepted '+str(n))
    return len(mutants)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default=str(HERE/'certificate.json'));ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    blob=Path(args.certificate).read_bytes();data=json.loads(blob);r=audit(data)
    r.update(malformed_certificate_rejections=reject_mutants(data),certificate_bytes=len(blob),certificate_sha256=hashlib.sha256(blob).hexdigest())
    if (HERE/'expected.json').exists():require(r==json.loads((HERE/'expected.json').read_text()),'expected exact report')
    out.joinpath('result.json').write_text(json.dumps(r,indent=2)+'\n')
    out.joinpath('timing.json').write_text(json.dumps({'seconds':time.monotonic()-start})+'\n');print(json.dumps(r))
if __name__=='__main__':main()
