"""Exact coupled-phase construction and complete small clause census."""
from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import argparse,hashlib,json,math,time
def clean(x):
    return {r:F(v) for r,v in x.items() if v}


def plus(x, y):
    z = dict(x)
    for r,v in y.items():
        z[r] = z.get(r,F(0))+v
    return clean(z)


def neg(x):
    return {r:-v for r,v in x.items()}


def times(x, y):
    z = {}
    for r,a in x.items():
        for s,b in y.items():
            g = math.gcd(r,s)
            t = r*s//(g*g)
            z[t] = z.get(t,F(0))+g*a*b
    return clean(z)


def cadd(z, w):
    return (plus(z[0],w[0]),plus(z[1],w[1]))


def csub(z, w):
    return (plus(z[0],neg(w[0])),plus(z[1],neg(w[1])))


def cmul(z, w):
    return (plus(times(z[0],w[0]),neg(times(z[1],w[1]))),
            plus(times(z[0],w[1]),times(z[1],w[0])))


def squared(z, w):
    a,b = csub(z,w)
    return plus(times(a,a),times(b,b))


def point(a=0,b=0,c=0,d=0):
    return (clean({1:a,3:b}),clean({1:c,3:d}))


def key(z):
    return tuple(tuple(sorted(v.items())) for v in z)


UNIT={1:F(1)}
ZERO=({}, {})
ONE=point(1)
OMEGA=point(F(1,2),0,0,F(1,2))
ROOTS=[ONE]
for _ in range(5):ROOTS.append(cmul(ROOTS[-1],OMEGA))
CROSS=[(0,2),(0,3),(1,2),(1,3)]

def sqrtfrac(q):
    if q==0:return {}
    if q<0:raise ValueError('negative square root')
    n=q.numerator*q.denominator;factor=1;rad=1;prime=2
    while prime*prime<=n:
        e=0
        while n%prime==0:n//=prime;e+=1
        factor*=prime**(e//2)
        if e%2:rad*=prime
        prime+=1
    return {rad*n:F(factor,q.denominator)}

def cscale(z,q):return (times(z[0],{1:q}),times(z[1],{1:q}))
def intersections(a,b):
    d=csub(b,a);q=squared(a,b)
    if any(r!=1 for r in q):raise ValueError('rational squared separation required')
    q=q.get(1,F(0))
    if q==0:raise ValueError('distinct centres required')
    if q>4:return []
    mid=cscale(cadd(a,b),F(1,2))
    if q==4:return [mid]
    factor=sqrtfrac((4-q)/(4*q))
    perp=(neg(d[1]),d[0])
    off=(times(perp[0],factor),times(perp[1],factor))
    return sorted([cadd(mid,off),csub(mid,off)],key=key)

def encode(z):
    return [[[r,q.numerator,q.denominator] for r,q in sorted(axis.items())] for axis in z]
def raw(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(data):return hashlib.sha256(raw(data)).hexdigest()

def orbit(u):
    candidates=[cmul(u,z) for z in ROOTS]
    rep=min(candidates,key=key)
    k=next(k for k,z in enumerate(ROOTS) if key(cmul(rep,z))==key(u))
    return key(rep),k

def literal_value(lit,assignment):
    return assignment[lit[0]]==lit[1]


def normalize_clause(lits):
    lits=sorted(set(lits))
    if len(lits)==2 and lits[0][0]==lits[1][0]:return None
    return tuple(lits)


def clause_census():
    rows=[];forbidden=[]
    for n in [2,3,4]:
        clauses=[((i,a),(j,b)) for i,j in combinations(range(n),2) for a,b in product(range(2),repeat=2)]
        assignments=list(product(range(2),repeat=n))
        truth=[sum(1<<k for k,x in enumerate(assignments) if any(literal_value(l,x) for l in c)) for c in clauses]
        states=[];hist=Counter()
        for m in range(5):
            for inds in combinations(range(len(clauses)),m):
                mask=(1<<(1<<n))-1
                for i in inds:mask &= truth[i]
                count=mask.bit_count();hist[count]+=1;states.append(count)
                if not count:forbidden.append({'n':n,'clauses':[clauses[i] for i in inds]})
        rows.append({'variables':n,'clause_options':len(clauses),'formulas':len(states),'satisfying_assignment_histogram':{str(k):v for k,v in sorted(hist.items())},'count_stream_sha256':digest(states)})
    return {'rows':rows,'unsatisfiable':forbidden}


def geometry(D,positive):
    I=[intersections(D[a],D[b]) for a,b in CROSS]
    orbits={}
    for (a,b),row in zip(CROSS,I):
        for x in row:
            for h in (a,b):
                rep,k=orbit(csub(x,D[h]));orbits[rep]=rep
    ordered=sorted(orbits);oi={v:i for i,v in enumerate(ordered)}
    clauses=[];slots=[]
    centre_keys={key(x) for x in D}
    for (a,b),row in zip(CROSS,I):
        candidates=[x for x in row if key(x) not in centre_keys]
        per=[]
        for x in candidates:
            v,k=orbit(csub(x,D[a]));w,l=orbit(csub(x,D[b]));s=(1+a+(b-2))%2
            per.append(normalize_clause([(oi[v],(s+k)%2),(oi[w],(1+s+l)%2)]))
        if per and any(z!=per[0] for z in per):raise ValueError('root clause mismatch')
        c=per[0] if per else None
        slots.append(c)
        if c is not None:clauses.append(c)
    solutions=[list(x) for x in product(range(2),repeat=len(ordered)) if all(any(literal_value(l,x) for l in c) for c in clauses)]
    result={'centres':[encode(x) for x in D], 'cross_squared_distances':[[squared(D[a],D[b])[1].numerator,squared(D[a],D[b])[1].denominator] for a,b in CROSS],
      'intersections':[[encode(x) for x in row] for row in I], 'orbit_representatives':[encode((dict(k[0]),dict(k[1]))) for k in ordered],
      'slot_clauses':slots,'solutions':len(solutions),'satisfiable':bool(solutions)}
    if positive:
        if not solutions:raise ValueError('positive formula failed')
        assignment=solutions[0]
        S=[{},{}]
        for g in range(2):
            seeds=[csub(D[2*g+1],D[2*g])]+[csub(x,D[h]) for h in [2*g,2*g+1] for row in I for x in row if squared(x,D[h])==UNIT]
            for seed in seeds:
                for root in ROOTS:
                    x=cmul(seed,root);S[g][key(x)]=x
        vertices={key(cadd(d,u)):cadd(d,u) for h,d in enumerate(D) for u in S[h//2].values()}
        V=sorted(vertices.values(),key=key);ci={key(d):i for i,d in enumerate(D)};col=[]
        for z in V:
            if key(z) in ci:c=(2,3,0,1)[ci[key(z)]]
            else:
                own=[h for h,d in enumerate(D) if squared(z,d)==UNIT];eligible=[]
                for g in sorted({h//2 for h in own}):
                    h=next(h for h in own if h//2==g);rep,k=orbit(csub(z,D[h]))
                    alpha=assignment[oi[rep]] if rep in oi else 0
                    value=2*g+(alpha+g+h%2+k)%2
                    if all(value!=(2,3,0,1)[j] for j in own):eligible.append(value)
                if not eligible:raise ValueError('uncolourable mixed point')
                c=min(eligible)
            col.append(c)
        E=[(a,b) for a,b in combinations(range(len(V)),2) if squared(V[a],V[b])==UNIT]
        if any(col[a]==col[b] for a,b in E):raise ValueError('monochromatic unit edge')
        result.update({'assignment':assignment,'directions':[len(s) for s in S],'vertices':len(V),'edges':len(E),'point_sha256':digest([encode(z) for z in V]),'edge_sha256':digest(E),'colouring':''.join(map(str,col))})
    else:
        if solutions:raise ValueError('negative control unexpectedly SAT')
        z=point(F(1,2),0,0,F(1,2))
        if any(squared(z,d)!=UNIT for d in D):raise ValueError('common neighbour witness')
        result['common_neighbour']=encode(z)
        result['five_point_colouring']=[0,1,0,1,2]
    return result


def build():
    t=point(F(12,7),0,0,F(1,7));r=point(F(-1,2),0,0,F(1,2))
    positive=geometry([ZERO,ONE,t,cadd(t,r)],True)
    negative=geometry([ZERO,ONE,point(0,0,0,1),point(1,0,0,1)],False)
    return {'schema':1,'regular_example':positive,'tangent_pin_obstruction':negative,'boolean_census':clause_census(),'target_found':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--discover',action='store_true');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();cert=build();blob=raw(cert)
    if not args.discover and blob!=(Path(__file__).parent/'certificate.json').read_bytes():raise ValueError('certificate mismatch')
    (out/'certificate.json').write_bytes(blob)
    result={'status':'PASS','vertices':cert['regular_example']['vertices'],'edges':cert['regular_example']['edges'],'phase_solutions':cert['regular_example']['solutions'],'census_formulas':sum(x['formulas'] for x in cert['boolean_census']['rows']),'unsatisfiable_formulas':len(cert['boolean_census']['unsatisfiable']),'certificate_bytes':len(blob),'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-start}
    (out/'build.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
