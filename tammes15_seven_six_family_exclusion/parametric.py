"""Uniform rational-function polytope certificates, with finite exceptions closed by continuity."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from collections import Counter
from rational import Rat
from polynomial import need,ONE,primitive,pgcd,exactdiv,mul,power,root_count,value
from patches import dot,H,one,zero,t

LOW=(Fraction(11,20),Fraction(59,100))
HIGH=(Fraction(59,100),Fraction(3,5))
NORM_BOUND=Fraction(999,1000)

def number(q):
    q=Fraction(q);return Rat((q.numerator,),(q.denominator,))


@lru_cache(None)
def odd_part(p):
    p=primitive(p)
    if len(p)<2:return ONE
    derivative=tuple(i*p[i] for i in range(1,len(p)))
    common=pgcd(p,derivative);w=exactdiv(p,common);out=ONE;square=ONE;degree=1
    while len(w)>1:
        y=pgcd(w,common);z=exactdiv(w,y)
        if degree%2:out=mul(out,z)
        square=mul(square,power(z,degree//2))
        w=y;common=exactdiv(common,y);degree+=1
    need(primitive(mul(out,mul(square,square)))==p,'odd-factor square reconstruction')
    need(len(pgcd(out,tuple(i*out[i] for i in range(1,len(out)))))==1,'odd factor squarefree')
    return primitive(out)


@lru_cache(None)
def sign_poly(p,lo,hi):
    if not p:return 0
    odd=odd_part(p)
    if root_count(odd,lo,hi):return None
    for i in range(1,len(p)+1):
        x=lo+(hi-lo)*Fraction(i,len(p)+1);v=value(p,x)
        if v:return 1 if v>0 else -1
    raise ValueError('nonzero polynomial vanishes on too many sample points')


def sign(x,lo,hi):
    a=sign_poly(x.n,lo,hi);b=sign_poly(x.d,lo,hi)
    return a*b if a is not None and b is not None else None


def det(m):
    return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])


def rows(points):
    return [[sum((x*H[j][i] for j,x in enumerate(p)),zero) for i in range(3)] for p in points]


def solve(m,rhs):
    d=det(m)
    if not d.n:return None
    return [det([[rhs[i] if j==k else m[i][j] for j in range(3)] for i in range(3)])/d for k in range(3)]


def audit(points,bounds,lo,hi,norm_bound):
    matrix=rows(points);records=[]
    for triple in combinations(range(len(points)),3):
        v=solve([matrix[i] for i in triple],[bounds[i] for i in triple])
        if v is None:
            records.append({'triple':triple,'kind':'identically_singular'});continue
        if sign(number(norm_bound)-dot(v,v),lo,hi)==1:
            records.append({'triple':triple,'kind':'norm_bound'});continue
        slacks=[];witness=None
        for i,(p,b) in enumerate(zip(points,bounds)):
            x=dot(p,v)-b;slacks.append(x)
            if sign(x,lo,hi)==1:witness=(i,);break
        if witness is None:
            for i,j in combinations(range(len(slacks)),2):
                if sign(slacks[i]*slacks[j],lo,hi)==-1:
                    witness=(i,j);break
        if witness is not None:records.append({'triple':triple,'kind':'infeasible','witness':witness})
        else:records.append({'triple':triple,'kind':'unresolved','norm':{'n':dot(v,v).n,'d':dot(v,v).d},
                             'slack_signs':[sign(x,lo,hi) for x in slacks],
                             'determinant_roots':root_count(det([matrix[i] for i in triple]).n,lo,hi)})
    return records


def prepare(points,threshold=Fraction(19,20)):
    need(set(points)==set(range(13)),'continuous point labels')
    points=[points[i] for i in range(13)]
    need(all(dot(p,p)==one for p in points),'continuous unit norms')
    for p in points:
        for x in p:
            need(root_count(x.d,LOW[0],HIGH[1])==0 and value(x.d,LOW[0])*value(x.d,HIGH[1])!=0,'point coefficient continuity')
    gap=dot(points[2],points[10])-t
    a,b=Fraction(1,2),LOW[0]
    need(root_count(gap.n,a,b)==root_count(gap.d,a,b)==0,'low packing witness roots')
    need(all(value(gap.n,x)/value(gap.d,x)>0 for x in (a,b)),'low packing witness signs')
    sample=Fraction(57,100)
    need(all(value((dot(points[i],points[j])-t).n,sample)/value((dot(points[i],points[j])-t).d,sample)<=0
             for i,j in combinations(range(13),2)),'exact continuous packing specialization')
    chosen=[points[i] for i in (0,1,2,7)]
    weights=[(-1 if i%2 else 1)*det([chosen[j] for j in range(4) if j!=i]) for i in range(4)]
    total=sum(weights,zero);weights=[w/total for w in weights]
    need(all(sign(w,LOW[0],HIGH[1])==1 for w in weights),'generic positive origin weights')
    need(sum(weights,zero)==one and all(sum((w*v[k] for w,v in zip(weights,chosen)),zero)==zero for k in range(3)),'origin identities')
    matrix=rows(points);q=solve([matrix[i] for i in (1,2,11)],[t]*3)
    need(q is not None,'continuous cap normal singular')
    need(all(root_count(x.d,*HIGH)==0 and value(x.d,HIGH[0])*value(x.d,HIGH[1])!=0 for x in q),'cap normal continuity')
    threshold=number(threshold)
    need(sign(threshold,*HIGH)==1,'cap threshold positive')
    guard=2*threshold*threshold-(one+t)*dot(q,q)
    need(sign(guard-number(Fraction(1,25)),*HIGH)==1,'cap diameter margin')
    return [(points,[t]*13,LOW),(points+[q],[t]*13+[threshold],HIGH)]


def make_tables(points):
    result={}
    for name,(p,b,domain) in zip(('low','high'),prepare(points)):
        records=audit(p,b,*domain,NORM_BOUND)
        need(all(r['kind']!='unresolved' for r in records),'unresolved parametric triple')
        result[name]=[None if r['kind']=='identically_singular' else [] if r['kind']=='norm_bound' else list(r['witness']) for r in records]
    return result


def validate_cover(points,bounds,domain,codes):
    triples=tuple(combinations(range(len(points)),3))
    need(type(codes) is list and len(codes)==len(triples),'active triple cover length')
    matrix=rows(points);counts=Counter()
    for triple,code in zip(triples,codes):
        v=solve([matrix[i] for i in triple],[bounds[i] for i in triple])
        if v is None:
            need(code is None,'singular triple code');counts['identically_singular']+=1;continue
        need(type(code) is list and len(code)<=2,'parametric witness code')
        need(all(type(i) is int and 0<=i<len(points) for i in code),'parametric witness label')
        if not code:
            need(sign(number(NORM_BOUND)-dot(v,v),*domain)==1,'uniform norm certificate');counts['norm_bound']+=1
        elif len(code)==1:
            i=code[0]
            need(sign(dot(points[i],v)-bounds[i],*domain)==1,'positive uniform infeasibility witness');counts['infeasible']+=1
        else:
            i,j=code;need(i!=j,'distinct infeasibility pair')
            need(sign((dot(points[i],v)-bounds[i])*(dot(points[j],v)-bounds[j]),*domain)==-1,'opposite-sign uniform infeasibility witnesses');counts['infeasible']+=1
    return dict(counts)


def verify(points,tables,threshold=Fraction(19,20)):
    need(set(tables)=={'low','high'},'parametric certificate fields')
    domains=prepare(points,threshold)
    counts={name:validate_cover(p,b,domain,tables[name]) for name,(p,b,domain) in zip(('low','high'),domains)}
    need(counts['low']=={'infeasible':257,'norm_bound':25,'identically_singular':4},'low parametric cover counts')
    need(counts['high']=={'infeasible':331,'norm_bound':29,'identically_singular':4},'high parametric cover counts')
    return {'exact_packing_parameter':[57,100],'saturation_domain':[[11,20],[59,100]],
            'cap_domain':[[59,100],[3,5]],'maximum_squared_norm_bound':[999,1000],
            'cap_threshold':[19,20],'cap_diameter_margin':[1,25],
            'active_triple_cover':counts,'additional_points_at_most':1,
            'finite_exception_method':'strict positive halfspaces, scaling and continuity'}
