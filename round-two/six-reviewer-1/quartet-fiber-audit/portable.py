"""Fresh standard-library coefficient/Sturm reconstruction; no CAS/author import."""
from fractions import Fraction as F
import argparse
import itertools
import json
import math
from pathlib import Path

V = tuple("A B E G J S T U a a1 a2 a3 a4 b d s t v57 x z".split())
ZERO = (0,) * len(V)


def number(c):
    c=F(c)
    return {ZERO:c} if c else {}


def var(name):
    e=list(ZERO);e[V.index(name)]=1
    return {tuple(e):F(1)}


def add(p,q):
    r=dict(p)
    for k,c in q.items():
        r[k]=r.get(k,F(0))+c
        if not r[k]:del r[k]
    return r


def neg(p):return {k:-c for k,c in p.items()}
def sub(p,q):return add(p,neg(q))


def mul(p,q):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            k=tuple(x+y for x,y in zip(a,b));r[k]=r.get(k,F(0))+c*d
    return {k:c for k,c in r.items() if c}


def power(p,n):
    r=number(1)
    for _ in range(n):r=mul(r,p)
    return r


def monodiv(p,q):
    if len(q)!=1:raise ValueError('nonmonomial division')
    (b,d),=q.items()
    return {tuple(x-y for x,y in zip(a,b)):c/d for a,c in p.items()}


def coeff(p,k,name='z'):
    i=V.index(name);r={}
    for a,c in p.items():
        if a[i]==k:
            b=list(a);b[i]=0;r[tuple(b)]=c
    return r


def decode(p):
    if type(p)!=dict or set(p)!={'variables','terms'}:raise ValueError('polynomial schema')
    names=p['variables'];rows=p['terms']
    if type(names)!=list or names!=sorted(set(names)) or any(v not in V for v in names):
        raise ValueError('coefficient domain')
    if type(rows)!=list or not rows:raise ValueError('coefficient list')
    r={};seen=set();last=None
    for row in rows:
        if type(row)!=dict or set(row)!={'powers','coefficient'}:raise ValueError('term schema')
        e=row['powers'];c=row['coefficient']
        if type(e)!=list or len(e)!=len(names) or any(type(i)!=int or i<0 for i in e):raise ValueError('powers')
        e=tuple(e)
        if e in seen or (last is not None and e>=last):raise ValueError('ordered unique monomials')
        if type(c)!=str or str(F(c))!=c:raise ValueError('exact canonical rational')
        seen.add(e);last=e;a=list(ZERO)
        for name,i in zip(names,e):a[V.index(name)]=i
        if F(c):r[tuple(a)]=F(c)
        elif len(rows)!=1 or any(e):raise ValueError('noncanonical zero')
    return r


def require(p,q,label):
    if p!=q:raise ValueError('whole coefficient mismatch '+label)


def newton(cs,limit):
    n=len(cs)-1;p=[number(n)]
    for j in range(1,limit+1):
        value={}
        for i in range(1,min(j,n+1)):value=add(value,mul(cs[i],p[j-i]))
        if j<=n:value=add(value,mul(number(j),cs[j]))
        p.append(neg(value))
    return p


def product(ps):
    r=number(1)
    for p in ps:r=mul(r,p)
    return r


def radd(a,b):return add(mul(a[0],b[1]),mul(b[0],a[1])),mul(a[1],b[1])
def rmul(a,b):return mul(a[0],b[0]),mul(a[1],b[1])
def rpow(a,n):return power(a[0],n),power(a[1],n)
def rdiv(a,b):return mul(a[0],b[1]),mul(a[1],b[0])
def rational(p):return p,number(1)


def utrim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p


def remainder(a,b):
    a=utrim(a);b=utrim(b)
    if not b:raise ValueError('zero Euclid divisor')
    while len(a)>=len(b):
        q=a[-1]/b[-1];j=len(a)-len(b)
        for i,c in enumerate(b):a[i+j]-=q*c
        a=utrim(a)
    return a


def sturm(cs):
    p=utrim(cs);der=utrim([i*c for i,c in enumerate(p)][1:]);out=[p,der]
    while out[-1]:
        nxt=[-c for c in remainder(out[-2],out[-1])]
        if not nxt:break
        out.append(nxt)
    if len(out[-1])!=1:raise ValueError('control not squarefree')
    return out


def eval_u(p,x):
    a=F(0)
    for c in reversed(p):a=a*x+c
    return a


def changes(values):
    sg=[1 if c>0 else -1 for c in values if c]
    return sum(a!=b for a,b in zip(sg,sg[1:]))


def univar(p,name='z'):
    i=V.index(name)
    if any(any(k[j] for j in range(len(V)) if j!=i) for k in p):raise ValueError('not univariate')
    if not p:return []
    return [p.get(tuple(n if j==i else 0 for j in range(len(V))),F(0))
            for n in range(max(k[i] for k in p)+1)]


def check(rec):
    if set(rec)!={'schema','identities','polynomials','bernstein','root_controls'} or rec['schema']!='six-reviewer-1/quartet-fiber/1':
        raise ValueError('closed record schema')
    ids={'whole Orlando six-pair product','pencil factor decomposition','pencil invariant R',
         'direction discriminant','level polynomial','level first derivative','three-branch derivative',
         'three-branch cubic derivative','fourth-moment displacement','multiplier factor','constraint minor',
         'lower Hessian','upper Hessian','triple Jensen gap','triple upper gap',
         'triple lower-branch boundary gap','omitted fifth control difference',
         'wzero first normal','wzero second normal','wzero forced negative variance'}
    ids|={'root Newton moment '+str(i)for i in (1,3,5)}
    ids|={'root derivative product '+str(i)for i in range(4)}
    ids|={'pencil odd moment '+str(i)for i in (1,3,5)}
    ids|={'critical cubic '+n for n in ('zero','quarter','half')}
    ids|={'original octic coefficient '+str(i)for i in range(9)}
    ids|={'full original moment '+str(i)for i in (1,2,3,5)}
    ids|={f'opening{k} '+n for k in (2,3)for n in ('first moment','third moment','first fifth derivative')}
    ids|={f'Bernstein reconstruction opening{k} {label} {end}'for k in (2,3)
           for label in ('delta2','positivity','gain')for end in ('numerator','denominator')}
    ids|={'omitted fifth control moment '+str(i)for i in (1,3)}
    ids|={f'parity coupling {i}{j}'for i in range(3)for j in range(3)}
    if set(rec['identities'])!=ids:raise ValueError('all75 identity names required')
    for name,row in rec['identities'].items():
        if set(row)!={'left','right','clearing_denominator'}:raise ValueError('identity schema')
        require(decode(row['left']),decode(row['right']),name)
        if not decode(row['clearing_denominator']):raise ValueError('zero clearing denominator')
    z,S,T,U,d=map(var,['z','S','T','U','d']);one=number(1)
    B=sub(mul(number(F(1,2)),power(S,2)),number(F(1,4)))
    q=sub(sub(power(z,2),mul(S,z)),monodiv(T,S))
    g=add(sub(add(sub(power(z,4),mul(S,power(z,3))),mul(B,power(z,2))),
              mul(add(mul(S,B),T),z)),sub(U,monodiv(mul(T,B),S)))
    def reflect(p):return {k:c*(-1)**k[V.index('z')]for k,c in p.items()}
    octic=mul(add(g,mul(d,q)),sub(reflect(g),mul(d,reflect(q))))
    cs=[coeff(octic,i)for i in range(8,-1,-1)]
    for i in range(9):
        row=rec['identities']['original octic coefficient '+str(i)]
        require(mul(coeff(octic,i),decode(row['clearing_denominator'])),decode(row['left']),
                'literal octic coefficient '+str(i))
    orig=newton(cs,8)
    expected_poly_names={'critical_cubic'}|{'original_moment_'+str(i)for i in range(9)}|{'critical_trace_'+str(i)for i in range(11)}
    if set(rec['polynomials'])!=expected_poly_names:raise ValueError('whole polynomial domain')
    for i,p in enumerate(orig):require(mul(p,power(S,8)),decode(rec['polynomials']['original_moment_'+str(i)]),'original moment '+str(i))
    critical=newton([one,{},number(-F(3,8)),{},var('E'),{},var('G'),var('J')],10)
    for i,p in enumerate(critical):require(p,decode(rec['polynomials']['critical_trace_'+str(i)]),'critical trace '+str(i))
    N=sub(sub(add(mul(number(-8),power(z,3)),mul(number(9),mul(S,power(z,2)))),mul(number(3),mul(power(S,2),z))),T)
    require(N,decode(rec['polynomials']['critical_cubic']),'critical cubic')
    roots=list(map(var,['a1','a2','a3','a4']))
    require(product(add(roots[i],roots[j])for i in range(4)for j in range(i+1,4)),
            decode(rec['identities']['whole Orlando six-pair product']['right']),'Orlando defining roots')
    X=var('x')
    for k in (2,3):
        cen=rational(sub(one,mul(number(F(1,k)),X)))
        delta=rdiv(radd(radd(rational(number(k)),rmul(rational(number(-k)),rpow(cen,3))),
                           rational(neg(power(X,3)))),rmul(rational(number(6)),cen))
        fifth=radd(radd(rmul(rational(number(k)),rpow(cen,5)),
                         rmul(rational(number(20)),rmul(rpow(cen,3),delta))),
                   radd(rmul(rational(number(10)),rmul(cen,rpow(delta,2))),rational(power(X,5))))
        exprs={'delta2':rdiv(delta,rational(X)),
               'positivity':radd(rpow(cen,2),rmul(rational(number(-1)),delta)),
               'gain':rdiv(radd(fifth,rational(number(-k))),rational(X))}
        for label,(num,den) in exprs.items():
            pair=[rec['bernstein'][f'opening{k} {label} '+end]for end in ('numerator','denominator')]
            require(mul(num,decode(pair[1]['polynomial'])),mul(den,decode(pair[0]['polynomial'])),'opening full rational '+label)
    if len(rec['bernstein'])!=12:raise ValueError('all12 closed Bernstein maps')
    for name,row in rec['bernstein'].items():
        if set(row)!={'interval','polynomial','coefficients'} or row['interval']!=['0','1/4']:raise ValueError('closed Bernstein domain')
        p=decode(row['polynomial']);cs=univar(p,'x');n=len(cs)-1
        want=[sum(cs[j]*F(math.comb(i,j),math.comb(n,j))*F(1,4)**j for j in range(i+1))for i in range(n+1)]
        if row['coefficients']!=list(map(str,want)) or not all(v>0 for v in want):raise ValueError('whole closed Bernstein coefficients '+name)
    base=product(sub(z,number(i))for i in range(1,5));q0=add(sub(power(z,2),mul(number(10),z)),number(30))
    dub=mul(power(sub(z,number(1)),2),power(sub(z,number(2)),2));q2=add(sub(power(z,2),mul(number(6),z)),number(10))
    tri=mul(power(sub(z,number(1)),3),sub(z,number(2)));q3=add(sub(power(z,2),mul(number(5),z)),number(F(38,5)))
    zero=product(sub(z,number(i))for i in range(4))
    controls={'distinct fiber '+str(sign):add(base,mul(number(F(sign,1000)),q0))for sign in (-1,1)}
    controls.update({'excluded zero boundary':zero,'open zero boundary interior':add(zero,mul(number(F(1,1000)),q2)),
                     'two-double interior':sub(dub,mul(number(F(1,1000)),q2)),
                     'outside two-double endpoint':add(dub,mul(number(F(1,1000)),q2))})
    controls.update({'outside triple singleton '+str(sign):add(tri,mul(number(F(sign,1000)),q3))for sign in (-1,1)})
    if set(controls)!=set(rec['root_controls']):raise ValueError('complete root control domain')
    for name,p in controls.items():
        row=rec['root_controls'][name];cs=univar(p);chain=sturm(cs)
        if set(row)!={'coefficients','sturm_chain','positive_root_count','brackets','moments_1_3_5'}:
            raise ValueError('root control schema')
        if row['coefficients']!=list(map(str,reversed(cs))):raise ValueError('literal root control '+name)
        if [univar(decode(q))for q in row['sturm_chain']]!=chain:raise ValueError('whole Sturm chain '+name)
        count=changes([eval_u(q,F(0))for q in chain])-changes([q[-1]for q in chain])
        if type(row['positive_root_count'])!=int or count!=row['positive_root_count']:raise ValueError('root count '+name)
        bracket_count=0 if name.startswith('outside') else (3 if name=='excluded zero boundary' else 4)
        if type(row['brackets'])!=list or len(row['brackets'])!=bracket_count:raise ValueError('complete isolated root brackets')
        previous=None
        for r in row['brackets']:
            if type(r)!=dict or set(r)!={'lo','hi','values','root_count'}:raise ValueError('root bracket schema')
            lo,hi=F(r['lo']),F(r['hi']);values=[eval_u(cs,lo),eval_u(cs,hi)]
            if previous is not None and lo<previous:raise ValueError('disjoint root brackets')
            previous=hi
            if row['brackets'] and not (lo>0 and hi>lo and values[0]*values[1]<0):raise ValueError('positive sign bracket')
            n=changes([eval_u(q,lo)for q in chain])-changes([eval_u(q,hi)for q in chain])
            if r['values']!=list(map(str,values)) or type(r['root_count'])!=int or n!=r['root_count']:raise ValueError('isolated root count')
        pms=newton([number(c)for c in reversed(cs)],5)
        if row['moments_1_3_5']!=[str(pms[k].get(ZERO,F(0)))for k in (1,3,5)]:raise ValueError('literal odd moments')
    return {'schema':rec['schema'],'identities':len(rec['identities']),
            'whole_polynomials_rederived':len(rec['polynomials']),
            'closed_bernstein_vectors':len(rec['bernstein']),
            'whole_sturm_chains_rederived':len(controls)}


def main():
    p=argparse.ArgumentParser();p.add_argument('record');args=p.parse_args()
    print(json.dumps(check(json.loads(Path(args.record).read_text())),sort_keys=True))


if __name__=='__main__':main()
