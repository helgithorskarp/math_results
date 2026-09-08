"""Independent certificate checker: Newton identities and root-direction census.

No producer imports, external packages, solver, floating point, or assertions.
Finite controls check the implementation; PROOF.md supplies the uniform theorem.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd, prod
from pathlib import Path
import argparse, copy, hashlib, json

HERE=Path(__file__).resolve().parent
def need(ok, message):
    if not ok: raise ValueError(message)

def factorization(n):
    result={}; d=2
    while d*d<=n:
        while n%d==0: result[d]=result.get(d,0)+1; n//=d
        d+=1
    if n>1: result[n]=1
    return result
def totient(n): return prod((p-1)*p**(a-1) for p,a in factorization(n).items())
def mobius(n):
    ff=factorization(n)
    return 0 if any(a>1 for a in ff.values()) else (-1)**len(ff)

def newton_cyclotomic(n):
    """Recover Phi_n from its Ramanujan power sums, independently of division."""
    d=totient(n)
    power=[0]+[mobius(n//gcd(n,k))*d//totient(n//gcd(n,k)) for k in range(1,d+1)]
    descending=[1]
    for k in range(1,d+1):
        numerator=-sum(descending[k-j]*power[j] for j in range(1,k+1))
        need(numerator%k==0,'Newton divisibility')
        descending.append(numerator//k)
    return list(reversed(descending))

def check_functional(c):
    n=c['n']; need(type(n) is int and n>=1,'conductor')
    f=c['cyclotomic_polynomial']; lam=c['functional']; d=totient(n)
    need(all(type(a) is int for a in f),'polynomial type')
    need(f==newton_cyclotomic(n),'cyclotomic polynomial mismatch')
    need(len(lam)==d and all(type(a) is int and 0<=a<3 for a in lam),'functional format')
    v=[1]+[0]*(d-1); weights=[]
    # Multiplication by X in F_3[X]/Phi_n validates every root direction.
    for _ in range(n):
        value=sum(a*b for a,b in zip(v,lam))%3
        need(value!=0,'vanishing root colour')
        weights.append(value)
        top=v[-1]; v=[0]+v[:-1]
        v=[(a-top*b)%3 for a,b in zip(v,f)]
    need(v==[1]+[0]*(d-1),'root period')
    return weights

def remainder(a,f):
    a=list(a); d=len(f)-1
    a.extend([0]*max(0,d-len(a)))
    for j in range(len(a)-1,d-1,-1):
        top=a[j]
        for k in range(d): a[j-d+k]-=top*f[k]
    return tuple(a[:d])
def multiply(a,b,f):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if x and y: c[i+j]+=x*y
    return remainder(c,f)
def powers(n,f):
    v=(1,)+(0,)*(len(f)-2); rr=[]
    for _ in range(n): rr.append(v); v=remainder((0,)+v,f)
    need(v==rr[0],'exact root period')
    return rr
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scale(a,q): return tuple(x*q for x in a)

def check_fixture(g,cert):
    need(g['conductor']==30 and cert['n']==30,'fixture conductor')
    pts=g['points']; lam=cert['functional']
    need(pts==[list(v) for v in product((0,1),repeat=8)],'complete binary cube')
    need(g['functional']==lam,'fixture functional mismatch')
    word=g['colouring']
    need(len(word)==256 and all(type(c) is int and 0<=c<3 for c in word),'colour word')
    need(word==[sum(a*b for a,b in zip(v,lam))%3 for v in pts],'colour formula mismatch')
    f=newton_cyclotomic(30); directions=set(powers(30,f))
    # The CM/Kronecker lemma implies every integral norm-one difference is a
    # root of unity. Q(zeta_30) has exactly 30 roots (PROOF.md, Section 3).
    # Thus direction membership gives a full edge census, without norm tests.
    edges=[]; pairs=0
    for i,j in combinations(range(256),2):
        pairs+=1
        if sub(pts[j],pts[i]) in directions:
            edges.append([i,j]); need(word[i]!=word[j],'monochromatic unit edge')
    need(edges==g['edges'],'strict edge census mismatch')
    triangle=[0,4,128] # 0, zeta_30^5, 1
    need(all([i,j] in edges for i,j in combinations(triangle,2)),'unit triangle')
    need(len({word[i] for i in triangle})==3,'triangle lower bound')
    return {'vertices':256,'strict_edges':len(edges),'pairs_checked':pairs,
            'chromatic_number':3,'triangle':triangle,
            'colour_counts':[word.count(c) for c in range(3)]}

def denominator_boundary():
    n=132; f=newton_cyclotomic(n); rr=powers(n,f); one=rr[0]; zero=scale(one,0)
    star=lambda z: tuple(sum(z[j]*rr[-j%n][k] for j in range(40)) for k in range(40))
    b=add(one,scale(rr[44],2))
    c=zero
    for j in range(1,11):c=add(c,scale(rr[12*j],1 if pow(j,5,11)==1 else -1))
    need(multiply(b,b,f)==scale(one,-3),'sqrt(-3)')
    need(multiply(c,c,f)==scale(one,-11),'sqrt(-11)')
    need(star(c)==scale(c,-1),'Gauss conjugation')
    w=scale(add(one,b),Q(1,2)); u=scale(add(scale(one,5),c),Q(1,6))
    need(add(u,star(u))==scale(one,Q(5,3)),'nonintegral quadratic trace')
    need(multiply(u,star(u),f)==one,'nonintegral unit direction')
    need(add(sub(scale(multiply(u,u,f),3),scale(u,5)),scale(one,3))==zero,'minimal polynomial')
    pts=[zero,one,w,add(one,w),u,multiply(u,w,f),multiply(u,add(one,w),f)]
    need(len(set(pts))==7,'Moser point distinctness')
    edges=[]
    for i,j in combinations(range(7),2):
        delta=sub(pts[i],pts[j])
        if multiply(delta,star(delta),f)==one:edges.append((i,j))
    expected={(0,1),(0,2),(1,2),(1,3),(2,3),(0,4),(0,5),(4,5),(4,6),(5,6),(3,6)}
    need(set(edges)==expected,'two diamonds and bridge')
    word=[0,1,2,0,1,2,3]
    need(all(word[i]!=word[j] for i,j in edges),'four-colour boundary word')
    return {'vertices':7,'strict_edges':11,'chromatic_number':4,
            'field':'Q(zeta_132)','nonintegral_direction_minpoly':[3,-5,3],
            'quadratic_trace':'5/3','lower_bound':'two diamonds force equal tips, contradicted by bridge'}

def rejected(call):
    try:call()
    except ValueError:return True
    raise ValueError('deliberately invalid certificate accepted')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args()
    certs=json.loads((HERE/'CERTIFICATES.json').read_text())
    need(len({c['n'] for c in certs})==len(certs),'duplicate conductor')
    all_values=[check_functional(c) for c in certs]
    by_n={c['n']:c for c in certs}
    dyadic=[]
    for c in certs:
        n=c['n']
        if n&(n-1)==0:
            f=newton_cyclotomic(n)
            need(sum(f)%2==0,'binary evaluation descends')
            need(all(sum(v)%2==1 for v in powers(n,f)),'binary root separation')
            dyadic.append(n)
    fixture=json.loads((HERE/'FIXTURE.json').read_text())
    fixture_report=check_fixture(fixture,by_n[30])
    bad=copy.deepcopy(by_n[15]);bad['functional']=[0]*8
    controls={'zero_functional':rejected(lambda:check_functional(bad))}
    bad=copy.deepcopy(by_n[105]);bad['cyclotomic_polynomial'][0]+=1
    controls['wrong_cyclotomic']=rejected(lambda:check_functional(bad))
    bad=copy.deepcopy(by_n[15]);bad['functional']=[1]*8
    controls['all_ones_functional']=rejected(lambda:check_functional(bad))
    bad=copy.deepcopy(fixture);i,j=bad['edges'][0];bad['colouring'][j]=bad['colouring'][i]
    controls['monochromatic_word']=rejected(lambda:check_fixture(bad,by_n[30]))
    bad=copy.deepcopy(fixture);bad['edges']=bad['edges'][1:]
    controls['omitted_unit_edge']=rejected(lambda:check_fixture(bad,by_n[30]))
    report={'status':'VERIFIED_CM_INTEGRAL_COLOURING_CONTROLS',
            'uniform_proof':'PROOF.md; finite checks do not prove the all-conductor theorem',
            'functional_certificates':len(certs),'conductors':[c['n'] for c in certs],
            'root_directions_checked':sum(map(len,all_values)),
            'binary_colouring_conductors':dyadic,
            'polynomial_method':'Ramanujan power sums and Newton identities',
            'fixture':fixture_report,'denominator_boundary':denominator_boundary(),
            'negative_controls':controls,'solver_calls':0,
            'certificate_sha256':hashlib.sha256((HERE/'CERTIFICATES.json').read_bytes()).hexdigest(),
            'fixture_sha256':hashlib.sha256((HERE/'FIXTURE.json').read_bytes()).hexdigest()}
    if args.check_expected:need(report==json.loads((HERE/'EXPECTED.json').read_text()),'expected report mismatch')
    print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
