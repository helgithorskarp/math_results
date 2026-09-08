"""Independent H510 realization checker: no producer imports or solver dependency.

Quadratic arithmetic uses normalized integer triples. Rhombus ranks use reverse
pivots. Orientation exclusions are checked as row-space consequences, and the
last identities are expanded directly as polynomials in four real variables.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, isqrt, lcm
from pathlib import Path

HERE=Path(__file__).resolve().parent
ALIGN_FILE='hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json'
UNION_FILE='hadwiger_nelson_parts509_heule_union_minimum/union_510.json'
RAD=(1,3,5,15,11,33,55,165)
USED=(0,2,5,7,9,11,12,14)
ZERO=(0,0,1)
ONE=(1,0,1)


def require(condition,message):
    if not condition: raise ValueError(message)


class Quadratic:
    def __init__(self,square): self.square=square
    def make(self,a,b=0,d=1):
        require(d!=0,'zero denominator')
        if d<0: a,b,d=-a,-b,-d
        g=gcd(gcd(a,b),d)
        return (a//g,b//g,d//g)
    def rational(self,x):
        x=Fraction(x); return self.make(x.numerator,0,x.denominator)
    def parse(self,a,b):
        a,b=Fraction(a),Fraction(b); d=lcm(a.denominator,b.denominator)
        return self.make(int(a*d),int(b*d),d)
    def add(self,x,y):
        a,b,c=x;d,e,f=y;return self.make(a*f+d*c,b*f+e*c,c*f)
    def neg(self,x): return (-x[0],-x[1],x[2])
    def sub(self,x,y): return self.add(x,self.neg(y))
    def mul(self,x,y):
        a,b,c=x;d,e,f=y;return self.make(a*d+self.square*b*e,a*e+b*d,c*f)
    def inv(self,x):
        a,b,c=x;return self.make(a*c,-b*c,a*a-self.square*b*b)
    def reduce(self,row,basis):
        row=list(row)
        for p in sorted(basis,reverse=True):
            x=row[p]
            if x!=ZERO: row=[self.sub(a,self.mul(x,b)) for a,b in zip(row,basis[p])]
        return row
    def basis(self,rows):
        out={}
        for row in rows:
            row=self.reduce(row,out)
            pivots=[i for i,x in enumerate(row) if x!=ZERO]
            if pivots:
                p=max(pivots);inv=self.inv(row[p]);out[p]=[self.mul(x,inv) for x in row]
        return out


def modular_rank(rows,p):
    basis={}
    for raw in rows:
        row={j:x%p for j,x in raw.items() if x%p}
        while row:
            col=max(row)
            if col not in basis:
                inv=pow(row[col],-1,p);basis[col]={j:x*inv%p for j,x in row.items()};break
            factor=row[col]
            for j,x in basis[col].items():
                value=(row.get(j,0)-factor*x)%p
                if value: row[j]=value
                else: row.pop(j,None)
    return len(basis)


def squared_distance(p,q):
    result={}
    for axis in range(2):
        entries=[(r,a-b) for r,a,b in zip(RAD,p[axis],q[axis]) if a!=b]
        for r,a in entries:
            for s,b in entries:
                g=gcd(r,s);rad=r*s//(g*g)
                result[rad]=result.get(rad,0)+a*b*g
    return {r:v for r,v in result.items() if v}


def load_inputs():
    pin=json.loads((HERE/'inputs.json').read_text())
    require(set(pin)=={ALIGN_FILE,UNION_FILE},'input names')
    loaded={}
    for name,digest in pin.items():
        raw=(HERE.parent/name).read_bytes();require(sha256(raw).hexdigest()==digest,'input hash')
        loaded[name]=json.loads(raw)
    aligned=loaded[ALIGN_FILE]
    require(aligned.get('vtx')=='510.vtx' and len(aligned['aligned_H'])==510,'aligned H510 input')
    union=loaded[UNION_FILE];require(len(union['points'])==553,'union point count')
    def key(point):return tuple(tuple(axis) for axis in point)
    lookup={key(point):i for i,point in enumerate(union['points'])}
    require(len(lookup)==553,'distinct union coordinates')
    h_to_union=[lookup[key(point)] for point in aligned['aligned_H']]
    require(len(set(h_to_union))==510,'distinct H510 coordinates')
    back={u:h for h,u in enumerate(h_to_union)}
    edges=sorted((min(back[u],back[v]),max(back[u],back[v])) for u,v in union['edges'] if u in back and v in back)
    require(len(edges)==2504 and edges==sorted(set(edges)),'source edge census')
    require(all(0<=u<v<510 for u,v in edges),'source edge range')
    points=[];K=[]
    for pair in aligned['aligned_H']:
        require(len(pair)==2 and all(len(x)==8 for x in pair),'coordinate shape')
        row=[96*Fraction(x) for xy in pair for x in xy]
        require(all(x.denominator==1 for x in row),'integer coordinate scale')
        row=list(map(int,row));require(all(row[j]==0 for j in range(16) if j not in USED),'coordinate support')
        points.append((tuple(row[:8]),tuple(row[8:])))
        K.append(tuple(Fraction(row[j],96) for j in USED))
    require(len(set(points))==510 and points[0]==((0,)*8,(0,)*8),'distinct source points and origin')
    require(all(squared_distance(points[u],points[v])=={1:9216} for u,v in edges),'exact source unit edges')
    return edges,points,K


def check_rhombi(cert,edges,K):
    edge_set=set(edges);adj=[set() for _ in K]
    for u,v in edges: adj[u].add(v);adj[v].add(u)
    rhombi=[];opposite={}
    for a,b in combinations(range(510),2):
        common=sorted(adj[a]&adj[b]);require(len(common)<=2,'source common-neighbour bound')
        if len(common)==2 and (a,b)<tuple(common):
            i=len(rhombi);rhombi.append([a,b,*common]);opposite[(a,b)]=i;opposite[tuple(common)]=i
    require(len(rhombi)==3953 and len(opposite)==7906,'rhombus census')
    for a,b,c,d in rhombi:
        require(all(x+y==z+w for x,y,z,w in zip(K[a],K[b],K[c],K[d])),'rational rhombus kernel')
    p=cert['prime'];require(p==1000000007 and all(p%d for d in range(2,isqrt(p)+1)),'prime')
    rows=[{j:int(x*96) for j,x in enumerate((Fraction(1),)+k)} for k in K]
    require(modular_rank(rows,p)==9,'kernel column independence')
    bases=cert['bases'];require(len(bases)==20,'basis count')
    for ids in bases:
        require(len(ids)==len(set(ids))==501 and all(type(i)==int and 0<=i<len(rhombi) for i in ids),'basis indices')
        rows=[]
        for i in ids:
            a,b,c,d=rhombi[i];rows.append({a:1,b:1,c:-1,d:-1})
        require(modular_rank(rows,p)==501,'rhombus basis rank')
    base_sets=list(map(set,bases));allmask=(1<<len(bases))-1
    masks=[sum(1<<j for j,b in enumerate(base_sets) if i in b) for i in range(len(rhombi))]
    pair_hits=[(i,j) for i,j in combinations(range(len(rhombi)),2) if masks[i]|masks[j]==allmask]
    require(all(m!=allmask for m in masks),'single-row basis coverage')

    supplied={};k23_cases=0
    for ex in cert['rank_exceptions']:
        pair=tuple(ex['rows']);require(len(pair)==2 and pair in pair_hits and pair not in supplied,'rank exception rows')
        r,s=pair;expected={(tuple(rhombi[r][:2]),tuple(rhombi[s][:2])),
                           (tuple(rhombi[r][:2]),tuple(rhombi[s][2:])),
                           (tuple(rhombi[r][2:]),tuple(rhombi[s][:2])),
                           (tuple(rhombi[r][2:]),tuple(rhombi[s][2:]))}
        seen=set()
        for case in ex['cases']:
            collision=tuple(tuple(x) for x in case['pairs']);require(collision in expected and collision not in seen,'collision exception cases');seen.add(collision)
            parent=list(range(510))
            def find(x):
                while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
                return x
            for u,v in collision:
                a,b=find(u),find(v)
                if a!=b:parent[b]=a
            require(not any(find(u)==find(v) for u,v in edges),'exception collapses edge')
            qedges={tuple(sorted((find(u),find(v)))) for u,v in edges if find(u)!=find(v)}
            witness=case['k23'];require(len(witness)==5 and all(type(x)==int and 0<=x<510 for x in witness),'K2,3 witness labels')
            roots=list(map(find,witness));require(len(set(roots))==5,'K2,3 quotient vertices distinct')
            require(all(tuple(sorted((roots[i],roots[j]))) in qedges for i in range(2) for j in range(2,5)),'K2,3 quotient edges')
            k23_cases+=1
        require(seen==expected,'collision exception coverage');supplied[pair]=True
    require(sorted(supplied)==pair_hits,'rank exception coverage')

    graph=[set() for _ in range(510)]
    for u,v in opposite:graph[u].add(v);graph[v].add(u)
    triangle_count=0;triangle_hits=[]
    for u in range(510):
        for v in sorted(x for x in graph[u] if x>u):
            for w in sorted(x for x in graph[u]&graph[v] if x>v):
                triangle_count+=1;ids=tuple(sorted({opposite[(u,v)],opposite[(u,w)],opposite[(v,w)]}))
                require(len(ids)==3,'opposition triangle rows')
                if masks[ids[0]]|masks[ids[1]]|masks[ids[2]]==allmask:triangle_hits.append(((u,v,w),ids))
    require(triangle_count==cert['opposition_triangle_count']==31582,'opposition triangle census')
    claimed=[(tuple(x['vertices']),tuple(x['rows'])) for x in cert['opposition_triangle_hits']]
    require(claimed==triangle_hits,'opposition triangle hit coverage')
    require(all(any(set(pair)<=set(ids) for pair in pair_hits) for vertices,ids in triangle_hits),'triangle exception reduces to pair exception')
    return {'rhombi':len(rhombi),'rhombus_rank':501,'kernel_dimension':9,'checked_bases':len(bases),
            'rank_exception_pairs':len(pair_hits),'exceptional_collision_cases':k23_cases,
            'opposition_triangles':triangle_count,'opposition_triangle_exceptions':len(triangle_hits)}


def get_directions(cert,edges,K):
    def direction(u,v):
        row=tuple(b-a for a,b in zip(K[u],K[v]));sign=next(x for x in row if x)
        return row if sign>0 else tuple(-x for x in row)
    available={direction(u,v) for u,v in edges};edge_set=set(edges);V=[]
    for u,v in cert['direction_edges']:
        require((u,v) in edge_set,'direction witness edge');V.append(direction(u,v))
    require(len(V)==len(set(V))==36 and set(V)==available,'complete distinct directions')
    return V


def check_orientations(cert,K,V):
    f=Quadratic(-3);triads=cert['triads'];require(len(triads)==12,'triad count')
    for i,j,k,s,r in triads:
        require(0<=i<j<k<36 and s in (-1,1) and r in (-1,1),'triad format')
        require(all(a+s*b==r*c for a,b,c in zip(V[i],V[j],V[k])),'triad linear identity')
    require(sorted(i for triad in triads for i in triad[:3])==list(range(36)),'triads partition directions')
    cover=set();survivors=[];rejections=0;depths=Counter()
    for leaf in cert['orientation_cover']:
        signs=leaf['signs'];require(len(signs)<=12 and all(type(s)==int and s in (-1,1) for s in signs),'orientation signs')
        depths[len(signs)]+=1
        for tail in product((-1,1),repeat=12-len(signs)):
            word=tuple(signs)+tail;require(word not in cover,'overlapping orientation prefixes');cover.add(word)
        rows=[]
        for sign,(i,j,k,s,r) in zip(signs,triads):
            factor=f.make(-s,sign,2)
            rows.append([f.sub(f.rational(b),f.mul(factor,f.rational(a))) for a,b in zip(V[i],V[j])])
        basis=f.basis(rows)
        if leaf.get('survivor') is True:
            require(len(signs)==12 and len(basis)==4,'survivor rank')
            orientations=[]
            for sigma in (-1,1):
                relations=[]
                for x,y,den in [(0,4,1),(1,5,1),(2,6,3),(3,7,3)]:
                    row=[ZERO]*8;row[y]=ONE;row[x]=f.make(0,-sigma,den);relations.append(row)
                if all(all(z==ZERO for z in f.reduce(row,basis)) for row in relations):orientations.append(sigma)
            require(len(orientations)==1,'surviving frame relations');survivors.extend(orientations)
        else:
            pairs=leaf['pairs'];require(len(pairs)==3,'three coincidence witnesses')
            require(all(len(pair)==2 and all(type(v)==int for v in pair) and 0<=pair[0]<pair[1]<510 for pair in pairs),'coincidence pair format')
            require(len({tuple(pair) for pair in pairs})==3,'distinct coincidence witnesses')
            for u,v in pairs:
                row=[f.rational(a-b) for a,b in zip(K[u],K[v])]
                require(all(z==ZERO for z in f.reduce(row,basis)),'coincidence row-space consequence')
            parent=list(range(510))
            def find(x):
                while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
                return x
            for u,v in pairs:
                u,v=find(u),find(v)
                if u!=v:parent[v]=u
            require(510-len({find(v) for v in range(510)})>=3,'forced image loss')
            rejections+=1
    require(len(cover)==4096 and sorted(survivors)==[-1,1],'orientation completeness')
    # These three unit directions give |A|=1 and C real with C^2=33,
    # once the positive orientation has E=t A and A is normalized to 1.
    required=[(1,0,0,0,0,0,0,0),
              (0,0,Fraction(1,6),0,Fraction(1,6),0,0,0),
              (0,0,Fraction(1,6),0,Fraction(-1,6),0,0,0)]
    require(all(tuple(d) in V for d in required),'normalizing unit directions')
    return {'orientation_words':len(cover),'rejected_prefixes':rejections,'surviving_prefixes':len(survivors),
            'prefix_depth_histogram':dict(sorted(depths.items()))}


def check_polynomials(cert,V):
    f=Quadratic(33);C=f.make(0,1);three=f.make(3);zero_exp=(0,0,0,0)
    # Arrays are coefficients of 1,b,y,d,z in real part and t-part, t^2=-3.
    r=[[ZERO]*5 for _ in range(8)];s=[[ZERO]*5 for _ in range(8)]
    r[0][0]=ONE;r[1][1]=ONE;s[1][2]=ONE;r[2][0]=C;r[3][3]=ONE;s[3][4]=ONE
    s[4][0]=ONE;r[5][2]=f.make(-3);s[5][1]=ONE;s[6][0]=f.make(0,1,3)
    r[7][4]=f.make(-1);s[7][3]=f.make(1,0,3)
    exps=[zero_exp]+[tuple(int(i==j) for i in range(4)) for j in range(4)]
    def plus(poly,term,coefficient):
        value=f.add(poly.get(term,ZERO),coefficient)
        if value!=ZERO:poly[term]=value
        else:poly.pop(term,None)
    equations=[]
    for direction in V:
        real=[ZERO]*5;imag=[ZERO]*5
        for a,R,S in zip(direction,r,s):
            scalar=f.rational(a)
            real=[f.add(x,f.mul(scalar,y)) for x,y in zip(real,R)]
            imag=[f.add(x,f.mul(scalar,y)) for x,y in zip(imag,S)]
        poly={zero_exp:f.make(-1)}
        for i,j in product(range(5),repeat=2):
            term=tuple(x+y for x,y in zip(exps[i],exps[j]))
            value=f.add(f.mul(real[i],real[j]),f.mul(three,f.mul(imag[i],imag[j])))
            plus(poly,term,value)
        equations.append(poly)
    targets={
        'norm_B_minus_5':{(2,0,0,0):ONE,(0,2,0,0):three,zero_exp:f.make(-5)},
        'y':{(0,1,0,0):ONE},'z':{(0,0,0,1):ONE},
        'd_minus_c_b':{(0,0,1,0):ONE,(1,0,0,0):f.neg(C)}}
    combinations_=cert['polynomial_combinations'];require(set(combinations_)==set(targets),'polynomial targets')
    terms=0
    for name,weights in combinations_.items():
        poly={};seen=set()
        for i,a,b in weights:
            require(type(i)==int and 0<=i<36 and i not in seen,'polynomial weight index');seen.add(i)
            weight=f.parse(a,b);require(weight!=ZERO,'nonzero polynomial weight');terms+=1
            for term,coefficient in equations[i].items():plus(poly,term,f.mul(weight,coefficient))
        require(poly==targets[name],'polynomial identity '+name)
    return {'polynomial_identities':4,'polynomial_combination_terms':terms}


def check_realizations(points,edges):
    hashes=[]
    for sign5,sign11 in product((-1,1),repeat=2):
        images=[]
        for point in points:
            image=[]
            for axis in point:
                image.append(tuple(a*(sign5 if rad%5==0 else 1)*(sign11 if rad%11==0 else 1) for a,rad in zip(axis,RAD)))
            images.append(tuple(image))
        require(len(set(images))==510,'conjugate injectivity')
        require(all(squared_distance(images[u],images[v])=={1:9216} for u,v in edges),'conjugate unit edges')
        raw=(json.dumps(images,separators=(',',':'))+'\n').encode();hashes.append(sha256(raw).hexdigest())
    return {'normalized_representatives':4,'vertices_per_representative':510,'unit_edges_checked':4*len(edges),
            'conjugate_coordinate_sha256':hashes}


def verify(cert):
    require(cert['version']==1,'certificate version')
    edges,points,K=load_inputs();result={}
    result.update(check_rhombi(cert,edges,K));V=get_directions(cert,edges,K)
    result.update(check_orientations(cert,K,V));result.update(check_polynomials(cert,V))
    result.update(check_realizations(points,edges))
    result.update(verified=True,source_vertices=510,source_edges=2504,unit_directions=36,
                  no_realization_with_508_or_509_images=True,all_near_injective_realizations_classified=True,
                  images_at_most_507_classified=False,record_improvement=False,solver_required=False)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args()
    raw=args.certificate.read_bytes();result=verify(json.loads(raw))
    result.update(certificate_sha256=sha256(raw).hexdigest(),certificate_bytes=len(raw))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
