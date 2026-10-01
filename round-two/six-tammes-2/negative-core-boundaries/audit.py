"""Direct polynomial audit of the quadratic/quartic resultant identity.

No SymPy or production geometric imports. Uses an explicit low-degree
resultant formula, integer coefficient products and closed Bernstein signs.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
LO,HI=Q(14,25),Q(593,1000);F=(-1,-3,2,6,-1,13)
def require(ok,message):
    if not ok:raise ValueError(message)
def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return tuple(p)
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-x for x in a)
def mul(a,b):
    if not a or not b:return ()
    p=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):p[i+j]+=x*y
    return trim(p)
def power(a,k):
    r=(1,)
    for _ in range(k):r=mul(r,a)
    return r
def value(a,x):
    r=Q(0)
    for c in reversed(a):r=r*x+c
    return r
def bernstein(p,left,right):
    n=len(p)-1
    a=[sum(Q(p[j])*comb(j,k)*left**(j-k)*(right-left)**k for j in range(k,n+1)) for k in range(n+1)]
    return [sum(a[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
def nonzero(p):
    require(p,'nonzero pole/locus polynomial')
    row=bernstein(p,LO,HI)
    require(all(x>0 for x in row) or all(x<0 for x in row),'strict closed-domain Bernstein sign')
def clear(rows):
    # Product denominators suffice; no polynomial GCD or CAS is needed.
    den=(1,)
    for r in rows:den=mul(den,tuple(r['d']))
    out=[]
    for i,r in enumerate(rows):
        n=tuple(r['n'])
        for j,s in enumerate(rows):
            if i!=j:n=mul(n,tuple(s['d']))
        out.append(n)
    return out,den
def factors(part):
    r=(Q(part['constant']),)
    for row in part['factors']:r=mul(r,power(tuple(row['coefficients']),row['multiplicity']))
    return r
def verify_pair(item,name,exception,other,pieces):
    require(len(item['E'])==3 and len(item['P'])==5,'quadratic/quartic literal degrees')
    (c,b,a),DE=clear(item['E']);(p0,p1,p2,p3,p4),DP=clear(item['P'])
    require(a and p4,'nonzero generic leading coefficients')
    A=add(add(mul(p1,power(a,3)),neg(mul(p2,mul(b,power(a,2))))),
          add(mul(p3,mul(a,add(power(b,2),neg(mul(a,c))))),
              mul(p4,add(neg(power(b,3)),mul((2,),mul(a,mul(b,c)))))))
    B=add(add(mul(p0,power(a,3)),neg(mul(p2,mul(c,power(a,2))))),
          add(mul(p3,mul(a,mul(b,c))),mul(p4,add(neg(mul(power(b,2),c)),mul(a,power(c,2))))))
    nr,dr=tuple(item['resultant']['n']),tuple(item['resultant']['d'])
    left=mul(power(a,3),mul(nr,mul(power(DE,4),power(DP,2))))
    right=mul(dr,add(add(mul(c,power(A,2)),neg(mul(b,mul(A,B)))),mul(a,power(B,2))))
    require(left==right,'exact resultant by quadratic remainder: '+name)
    nf,df=factors(item['numerator_factors']),factors(item['denominator_factors'])
    require(mul(nr,df)==mul(dr,nf),'literal resultant factorization: '+name)
    found=False
    for where in ('numerator_factors','denominator_factors'):
        require(Q(item[where]['constant'])!=0,'nonzero factorization constant')
        for row in item[where]['factors']:
            pol=tuple(row['coefficients']);require(row['multiplicity']>=1,'positive multiplicity')
            if pol==exception:
                require(other and where=='numerator_factors' and row['multiplicity']==1 and row['roots_on_I']==1,
                        'single specified exceptional root');found=True
            else:
                require(row['roots_on_I']==0,'no other exceptional factor')
                nonzero(pol);pieces.add(pol)
    require(found==other,'exception is present only in other-neighbor alternative')

def rational_poles(data,poles):
    if isinstance(data,dict):
        if set(data)=={'n','d'}:
            require(isinstance(data['n'],list) and isinstance(data['d'],list),'literal rational arrays')
            require(all(type(c)is int for c in data['n']+data['d']),'integer rational coefficients')
            p=trim(data['d']);nonzero(p);poles.add(p)
        else:
            for v in data.values():rational_poles(v,poles)
    elif isinstance(data,list):
        for v in data:rational_poles(v,poles)

def verify(data):
    require(data['format']==1 and data['authoring_agent']=='six-tammes-2' and data['role']=='researcher',
            'fixed data format and actual author role')
    pieces=set();poles=set();identities=0
    alpha=(-1,0,3)
    for family,first,exception in (('critical','B1',F),('lower','A0',alpha)):
        c=data[family]
        require(c['format']==1 and c['domain']==['14/25','593/1000'] and c['coefficient_domain']=='Q(t)[q]',
                'fixed closed domain and coefficient field')
        require(set(c['resultants'])=={first,'other'},'both unit common-neighbor alternatives')
        for name in (first,'other'):
            verify_pair(c['resultants'][name],family+'/'+name,exception,name=='other',pieces)
            identities+=1
    require(data['lower']['selector_pair']==[5,12],'literal packing selector')
    rational_poles(data,poles)
    require(all(x>0 for x in bernstein(tuple(i*F[i] for i in range(1,len(F))),LO,HI)),
            'strict incumbent quintic monotonicity')
    require(value(F,LO)<0<value(F,HI) and value(F,Q(29,50))<0,'unique quintic and sign-witness order')
    tau_lo=Q('0.59260590292507377809642492233275')
    tau_hi=Q('0.59260590292507377809642492233276')
    require(value(F,tau_lo)<0<value(F,tau_hi),'exact credited incumbent root enclosure')
    require(value(alpha,LO)<0<value(alpha,Q(29,50)) and value(alpha,Q(577,1000))<0,
            'unique positive lower root and its rational lower bound')
    return {'status':'AUDITED','integer_resultant_identities':identities,
            'distinct_nonzero_factors':len(pieces),'distinct_coefficient_poles':len(poles),
            'critical_boundary_polynomial':list(F),'lower_boundary_polynomial':list(alpha),
            'geometric_tables_rederived':False}
if __name__=='__main__':
    print(json.dumps(verify(json.loads((HERE/'certificate.json').read_text())),sort_keys=True))
