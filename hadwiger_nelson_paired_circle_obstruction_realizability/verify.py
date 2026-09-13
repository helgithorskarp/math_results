#!/usr/bin/env python3
"""Independent tensor-basis verifier for the regular two-variable witness."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import argparse,copy,hashlib,json


# Basis order is 1,sqrt(3),i,i*sqrt(3).
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    out=[F(0)]*4
    for m,a in enumerate(x):
        for n,b in enumerate(y):
            if not a or not b:continue
            s=(m&1)+(n&1);j=((m>>1)&1)+((n>>1)&1);c=a*b
            if s>=2:c*=3;s-=2
            if j>=2:c=-c;j-=2
            out[s+2*j]+=c
    return tuple(out)
def conj(x):return (x[0],x[1],-x[2],-x[3])
def norm(x):return mul(x,conj(x))
ZERO=(F(0),)*4;ONE=(F(1),F(0),F(0),F(0));II=(F(0),F(0),F(1),F(0));OMEGA=(F(1,2),F(0),F(0),F(1,2))
ROOTS=[ONE]
for _ in range(5):ROOTS.append(mul(ROOTS[-1],OMEGA))
if mul(ROOTS[-1],OMEGA)!=ONE:raise RuntimeError('sixth-root failure')


def enc(z):return [[[z[0].numerator,z[0].denominator],[z[1].numerator,z[1].denominator]],
                    [[z[2].numerator,z[2].denominator],[z[3].numerator,z[3].denominator]]]
def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def orbit(direction):
    candidates=[mul(direction,u) for u in ROOTS];rep=min(candidates)
    return rep,next(k for k,u in enumerate(ROOTS) if mul(rep,u)==direction)


def geometry():
    w5=ROOTS[5];us=(OMEGA,ONE,OMEGA,ONE);vs=(II,II,mul(II,w5),mul(II,w5));ds=[sub(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,sub(ds[0],ds[2]),ds[0],ds[1]);cross=((0,0),(0,1),(1,0),(1,1));intersections=[];reps={};clauses=[]
    if sub(centres[3],centres[1])!=ds[3] or norm(centres[1])!=ONE or norm(sub(centres[3],centres[2]))!=ONE:raise ValueError('centre geometry')
    if len(set(centres))!=4:raise ValueError('coincident centres')
    for (i,j),u,v in zip(cross,us,vs):
        if u in (v,neg(v)):raise ValueError('nonregular pair')
        x=add(centres[i],u);y=sub(add(centres[i],centres[2+j]),x)
        if x==y:raise ValueError('tangent pair')
        for p in (x,y):
            if norm(sub(p,centres[i]))!=ONE or norm(sub(p,centres[2+j]))!=ONE:raise ValueError('bad intersection')
        intersections.append((x,y));ru,k=orbit(u);rv,l=orbit(v);reps[ru]=None;reps[rv]=None;s=(1+i+j)&1
        clauses.append(((ru,(s+k)&1),(rv,(1+s+l)&1)))
    ordered=sorted(reps);oi={r:i for i,r in enumerate(ordered)};clauses=[sorted([[oi[r],v] for r,v in c]) for c in clauses]
    S=[set(),set()]
    for g in range(2):
        seeds=[sub(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,intersections):seeds.extend(sub(p,centres[i if g==0 else 2+j]) for p in row)
        for seed in seeds:S[g].update(mul(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres):points.update(add(c,u) for u in S[h//2])
    vertices=sorted(points);edges=[list(e) for e in combinations(range(len(vertices)),2) if norm(sub(vertices[e[0]],vertices[e[1]]))==ONE]
    return centres,ds,clauses,S,vertices,edges


def validate(data):
    if data.get('schema')!=1 or data.get('field')!='Q(sqrt(3),i)':raise ValueError('schema')
    centres,ds,clauses,S,V,E=geometry()
    if [enc(x) for x in centres]!=data.get('centres'):raise ValueError('centres')
    cross=[[[x.numerator,x.denominator] for x in norm(d)[:2]] for d in ds]
    if cross!=data.get('cross_squared_norms'):raise ValueError('cross norms')
    if any(norm(d) in (ZERO,ONE,(F(3),F(0),F(0),F(0)),(F(4),F(0),F(0),F(0))) for d in ds):raise ValueError('cross boundary')
    solutions=sum(all(any(a[v]==value for v,value in row) for row in clauses) for a in product(range(2),repeat=data['orbit_variables']))
    if clauses!=data.get('clauses') or data.get('orbit_variables')!=2 or solutions!=0 or data.get('phase_solutions')!=0:raise ValueError('phase obstruction')
    if (list(map(len,S)),len(V),len(E))!=(data.get('direction_sizes'),data.get('patch_vertices'),data.get('patch_edges')):raise ValueError('counts')
    if digest([enc(x) for x in V])!=data.get('point_sha256') or digest(E)!=data.get('edge_sha256'):raise ValueError('hashes')
    p=neg(II)
    if enc(p)!=data.get('common_neighbour'):raise ValueError('common neighbour label')
    pi=V.index(p);ci=[V.index(c) for c in centres]
    if any([min(pi,i),max(pi,i)] not in E for i in ci):raise ValueError('not common neighbour')
    triangle=(pi,ci[0],ci[1])
    if any([min(a,b),max(a,b)] not in E for a,b in combinations(triangle,2)):raise ValueError('triangle')
    colouring=[int(c) for c in data.get('three_colouring','')]
    if len(colouring)!=len(V) or max(colouring)>2 or any(colouring[a]==colouring[b] for a,b in E):raise ValueError('three-colouring')
    if data.get('chromatic_number')!=3 or data.get('kernel_list_colourable') is not False:raise ValueError('chromatic/list flags')
    # With four distinct centre pins the common neighbour sees all colours.
    if len({2,3,0,1})!=4 or any(i==pi for i in ci):raise ValueError('list obstruction')
    if data.get('full_support_four_colourable') is not None or data.get('record_improved') is not False:raise ValueError('scope')
    return {'status':'PASS','orbit_variables':2,'phase_solutions':0,'patch_vertices':len(V),'patch_edges':len(E),
            'chromatic_number':3,'common_neighbour_degree_to_centres':4,'kernel_list_colourable':False,
            'full_support_status':'unresolved','record_improved':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default=str(Path(__file__).with_name('certificate.json')));ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
    data=json.loads(Path(args.certificate).read_text());result=validate(data);bad=[]
    x=copy.deepcopy(data);x['phase_solutions']=1;bad.append(x)
    x=copy.deepcopy(data);x['point_sha256']='0'*64;bad.append(x)
    x=copy.deepcopy(data);x['three_colouring']='0'*x['patch_vertices'];bad.append(x)
    x=copy.deepcopy(data);x['kernel_list_colourable']=True;bad.append(x)
    x=copy.deepcopy(data);x['full_support_four_colourable']=True;bad.append(x)
    rejected=0
    for malformed in bad:
        try:validate(malformed)
        except (ValueError,KeyError,IndexError):rejected+=1
    if rejected!=len(bad):raise ValueError('malformed control accepted')
    result['rejected_controls']=rejected
    if args.check_expected and result!=json.loads(Path(__file__).with_name('expected.json').read_text()):raise ValueError('expected result mismatch')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
