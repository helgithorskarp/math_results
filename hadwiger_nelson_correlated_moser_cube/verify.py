"""Independent exact geometry, polynomial coverage and positive-colouring audit.

Imports no producer code and does not use SymPy, SAT answers or floating point.
"""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations,product
import hashlib
import json
from pathlib import Path
import flint
import algebra as A

HERE=Path(__file__).resolve().parent
Z=(0,0)


def require(ok,why):
    if not ok:
        raise ValueError(why)


def digest(data):
    return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()


def ctimes(z,w):
    x,y=z;u,v=w
    return (A.minus(A.times(x,u),tuple(3*a for a in A.times(y,v))),
            A.plus(A.times(x,v),A.times(y,u)))


def spindle():
    zero=(Z,Z);one=((1,0),Z)
    rho=((F(1,2),0),(F(1,2),0))
    far=(A.plus(one[0],rho[0]),rho[1])
    rotation=((F(5,6),0),(0,F(1,18)))
    points=[zero,one,rho,far,rotation,ctimes(rotation,rho),ctimes(rotation,far)]
    rows=[]
    for x,y in points:
        row=[36*F(v) for v in x+y]
        require(all(v.denominator==1 for v in row),'spindle denominator')
        rows.append(tuple(map(int,row)))
    return rows


def padd(a,b):
    a=list(a)+[Z]*max(0,len(b)-len(a));b=list(b)+[Z]*max(0,len(a)-len(b))
    return [A.plus(x,y) for x,y in zip(a,b)]


def pscale(a,c):
    return [A.times(x,c) for x in a]


def numerator_points(M,addresses):
    D=[(1,0),Z,(3,0)];C=[(1,0),Z,(-3,0)];S=[Z,(2,0)]
    D2=A.multiply(D,D)
    shapes=[(D2,[Z]),(A.multiply(D,C),A.multiply(D,S)),
            (padd(A.multiply(C,C),pscale(A.multiply(S,S),(-3,0))),
             pscale(A.multiply(C,S),(2,0)))]
    terms=[]
    for X,Y in shapes:
        rows=[]
        for a,b,c,d in M:
            rows.append((padd(pscale(X,(a,b)),pscale(Y,(-3*c,-3*d))),
                         padd(pscale(X,(c,d)),pscale(Y,(a,b)))))
        terms.append(rows)
    points=[]
    for i,j,k in addresses:
        x=[Z]*5;y=[Z]*5
        for level,v in enumerate((i,j,k)):
            x=padd(x,terms[level][v][0]);y=padd(y,terms[level][v][1])
        points.append((x,y))
    return points,D2


def independent_contacts():
    M=spindle();addresses=list(product(range(7),repeat=3))
    points,D2=numerator_points(M,addresses)
    unit=defaultdict(list);collision=defaultdict(list);generic=[]
    for v,w in combinations(range(343),2):
        dx=[A.minus(a,b) for a,b in zip(points[v][0],points[w][0])]
        dy=[A.minus(a,b) for a,b in zip(points[v][1],points[w][1])]
        numerator=padd(A.multiply(dx,dx),pscale(A.multiply(dy,dy),(3,0)))
        numerator += [Z]*(9-len(numerator))
        # Divide the degree-eight norm numerator by (1+3t^2)^2.
        # Its constant coefficient is1, so coefficient recurrence is integral.
        q=[]
        for k in range(9):
            value=numerator[k]
            if k>=2:value=A.minus(value,tuple(6*a for a in q[k-2]))
            if k>=4:value=A.minus(value,tuple(9*a for a in q[k-4]))
            q.append(value)
        require(q[5:]==[Z]*4,'exact norm denominator cancellation')
        q=q[:5]
        zero=A.canonical(q)
        require(bool(zero),'distinct formal addresses')
        if len(zero)>1:collision[zero].append([v,w])
        p=A.canonical(padd(q,pscale(D2,(-1296,0))))
        if not p:generic.append([v,w])
        elif len(p)>1:unit[p].append([v,w])
    return M,addresses,generic,unit,collision


def polynomial(value):
    require(isinstance(value,list) and 1<=len(value)<=5,'polynomial shape')
    require(all(isinstance(c,list) and len(c)==2 and all(type(x)is int for x in c)
                for c in value),'quadratic coefficients')
    p=tuple(map(tuple,value))
    require(A.canonical(p)==p,'canonical polynomial')
    return p


def verify_proposals(work,M,addresses,generic,unit,collision):
    proposal=json.loads((work/'contacts.json').read_text())
    require(proposal['M']==[list(p)for p in M],'producer spindle coordinates')
    require(proposal['addresses']==[list(p)for p in addresses],'producer address ordering')
    require(proposal['generic_edges']==generic,'generic edge census')
    source={}
    for kind,name,actual in [('unit','contacts',unit),('collision','collision_norms',collision)]:
        rows=proposal[name]
        require(len(rows)==len(actual),'event polynomial count')
        require([polynomial(r['poly'])for r in rows]==sorted(actual),'complete event polynomial list')
        for i,row in enumerate(rows):
            p=polynomial(row['poly'])
            require(row['pairs']==actual[p],'complete event-pair incidence')
            source[kind,i]=(p,actual[p])
    rows=json.loads((work/'factorizations.json').read_text())
    expected_keys=[(kind,i)for kind,name in [('unit','contacts'),('collision','collision_norms')]
                   for i in range(len(proposal[name]))]
    require([(r['kind'],r['index'])for r in rows]==expected_keys,'complete factor-proposal list')
    pieces={};identities=0
    for row in rows:
        p,pairs=source[row['kind'],row['index']]
        expected=p if row['kind']=='unit'else A.pgcd(p,A.derivative(p))
        result=[(1,0)];seen=set()
        for raw,exponent in row['factors']:
            f=polynomial(raw)
            require(len(f)>1 and f not in seen,'distinct nonconstant factors in row')
            require(type(exponent)is int and 1<=exponent<=4,'factor multiplicity')
            seen.add(f)
            for _ in range(exponent):result=A.multiply(result,f)
            if f not in pieces:pieces[f]={'extra_edges':[],'equalities':[]}
            key='extra_edges'if row['kind']=='unit'else'equalities'
            pieces[f][key].extend(pairs)
        require(A.canonical(result)==A.canonical(expected),'factor product identity')
        identities+=1
    return sorted(pieces),pieces,identities


def modular_separation(factors):
    # Lucas-Lehmer proves that2^61-1 is prime (61 is prime by trial division).
    require(all(61%d for d in range(2,8)),'prime exponent')
    prime=2**61-1;s=4
    for _ in range(59):s=(s*s-2)%prime
    require(s==0,'Lucas-Lehmer prime certificate')
    root=pow(33,(prime+1)//4,prime)
    require(root*root%prime==33,'quadratic ring projection')
    polys=[flint.nmod_poly([(a+b*root)%prime for a,b in f],prime)for f in factors]
    require(all(p.degree()==len(f)-1 for p,f in zip(polys,factors)),'modular degree preservation')
    while len(polys)>1:
        polys=[polys[i]*polys[i+1]if i+1<len(polys)else polys[i]for i in range(0,len(polys),2)]
    p=polys[0]
    require(p.gcd(p.derivative()).degree()==0,'squarefree product of all pieces')
    return {'prime':prime,'sqrt33_mod_prime':root,'product_degree':p.degree(),
            'product_derivative_gcd_degree':0}


def infinity_case(M,addresses):
    points=[tuple(a-b+c for a,b,c in zip(M[i],M[j],M[k]))for i,j,k in addresses]
    equal=[];edges=[]
    for u,v in combinations(range(343),2):
        dx=tuple(a-b for a,b in zip(points[u][:2],points[v][:2]))
        dy=tuple(a-b for a,b in zip(points[u][2:],points[v][2:]))
        q=A.plus(A.times(dx,dx),tuple(3*a for a in A.times(dy,dy)))
        if q==Z:equal.append([u,v])
        if q==(1296,0):edges.append([u,v])
    return {'extra_edges':edges,'equalities':equal}


def quotient_counts(case,generic):
    parent=list(range(343))
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    for a,b in case['equalities']:
        a,b=root(a),root(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    edges={tuple(sorted((root(a),root(b))))for a,b in generic+case['extra_edges']}
    require(all(a!=b for a,b in edges),'no edge collapsed at a real parameter')
    return len({root(v)for v in range(343)}),len(edges)


def verify(work,certificate):
    M,addresses,generic,unit,collision=independent_contacts()
    medges=[]
    for i,j in combinations(range(7),2):
        a,b,c,d=(x-y for x,y in zip(M[i],M[j]))
        if A.plus(A.times((a,b),(a,b)),tuple(3*x for x in A.times((c,d),(c,d))))==(1296,0):
            medges.append((i,j))
    require(len(medges)==11,'Moser spindle has eleven edges')
    require(not any(all(w[a]!=w[b]for a,b in medges)for w in product(range(3),repeat=7)),
            'Moser spindle has no three-colouring')
    cartesian=set()
    for address in addresses:
        for coordinate in range(3):
            for a,b in medges:
                if address[coordinate]==a:
                    other=list(address);other[coordinate]=b
                    v=49*address[0]+7*address[1]+address[2]
                    w=49*other[0]+7*other[1]+other[2]
                    cartesian.add(tuple(sorted((v,w))))
    require({tuple(e)for e in generic}==cartesian,'all and only Cartesian generic edges')
    factors,pieces,identities=verify_proposals(work,M,addresses,generic,unit,collision)
    modular=modular_separation(factors)
    cert=json.loads(certificate.read_text())
    require(cert['version']=='correlated-moser-cube-v1','certificate version')
    words=cert['words'];assignment=cert['assignment']
    require(isinstance(words,list) and words and len(set(words))==len(words),'distinct colour words')
    for w in words:
        require(type(w)is str and len(w)==343 and set(w)<=set('0123'),'colour word shape')
        require(all(w[u]!=w[v]for u,v in generic),'generic colouring')
    require(len(assignment)==len(factors)+1,'complete assignment array')
    require(type(cert['generic_word'])is int and 0<=cert['generic_word']<len(words),'generic word index')
    mw=cert['M_colour_word']
    require(len(mw)==7 and all(type(c)is int and 0<=c<=3 for c in mw)
            and all(mw[a]!=mw[b]for a,b in medges),'positive Moser four-colouring')
    require(words[cert['generic_word']]==''.join(str(mw[i]^mw[j]^mw[k])for i,j,k in addresses),
            'product-colouring formula')
    histogram=Counter();counts=[];real_cases=0;collision_cases=0;real_angles=0;edge_checks=0;equal_checks=0
    for i,f in enumerate(factors):
        nroots=A.real_roots(f);histogram[nroots]+=1
        require(0<=nroots<len(f),'real root count range')
        index=assignment[i]
        require(type(index)is int,'integer assignment index')
        if not nroots:
            require(index==-1,'nonreal piece marker');continue
        require(0<=index<len(words),'real piece colouring index')
        c=pieces[f];w=words[index]
        require(all(w[a]!=w[b]for a,b in c['extra_edges']),'exceptional unit edges')
        require(all(w[a]==w[b]for a,b in c['equalities']),'coincident addresses have equal colours')
        n,e=quotient_counts(c,generic) if c['equalities']else (343,len(generic)+len(c['extra_edges']))
        counts.append([i,nroots,n,e,index]);real_cases+=1;real_angles+=nroots
        collision_cases+=bool(c['equalities']);edge_checks+=len(c['extra_edges']);equal_checks+=len(c['equalities'])
    infinity=infinity_case(M,addresses);index=assignment[-1]
    require(type(index)is int and 0<=index<len(words),'infinity colouring index')
    w=words[index]
    require(all(w[a]!=w[b]for a,b in infinity['extra_edges']),'infinity unit edges')
    require(all(w[a]==w[b]for a,b in infinity['equalities']),'infinity coincidences')
    infinity_counts=quotient_counts(infinity,generic)
    used={cert['generic_word']}|{i for i in assignment if i>=0}
    require(used==set(range(len(words))),'all certificate words used')
    return {'verified':True,'construction':'M+uM+u^2M, every |u|=1','chromatic_number':4,
            'maximum_vertices':343,'record_improvement':False,'pair_checks':343*342//2,
            'generic_vertices':343,'generic_edges':len(generic),'M_edges':len(medges),
            'unit_event_polynomials':len(unit),'collision_norm_polynomials':len(collision),
            'factor_product_identities':identities,'coprime_squarefree_pieces':len(factors),
            'factor_degree_histogram':dict(sorted(Counter(len(f)-1 for f in factors).items())),
            'real_root_histogram':dict(sorted(histogram.items())),
            'finite_real_parameters':real_angles,'real_polynomial_cases':real_cases,
            'real_cases_with_collisions':collision_cases,'infinity_vertices':infinity_counts[0],
            'infinity_edges':infinity_counts[1],'finite_vertex_range':[min(r[2]for r in counts),max(r[2]for r in counts)],
            'finite_edge_range':[min(r[3]for r in counts),max(r[3]for r in counts)],
            'colour_words':len(words),'generic_colour_edge_checks':len(words)*len(generic),
            'event_colour_edge_checks':edge_checks,'event_equality_checks':equal_checks,
            'modular_separation':modular,'factors_sha256':digest(factors),
            'finite_case_summary_sha256':digest(counts),
            'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args()
    result=verify(args.work,args.certificate)
    text=json.dumps(result,sort_keys=True)
    if args.check_expected:
        require(json.loads(text)==json.loads((HERE/'expected.json').read_text()),'expected result')
    print(text)


if __name__=='__main__':
    main()
