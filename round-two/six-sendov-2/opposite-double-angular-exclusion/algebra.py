"""Credited exact arithmetic helpers from source39ccb1ee/LEMMA10235.

Adapted by the same author, six-sendov-2/researcher. Standard library only.
No independent-review claim. The new verifier derives its actual-domain data.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json

DOMAIN='QQ[p,tau][z]; actual p>2,0<tau<T,tau<1/(p^2+1),p=r+r^3,r>1'
ZERO={}
ONE={(0,0):Q(1)}

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2)+"\n").encode("utf-8")

def require(ok,message):
    if not ok:raise ValueError(message)

def add(a,b):
    out=dict(a)
    for k,v in b.items():
        out[k]=out.get(k,Q(0))+v
        if not out[k]:out.pop(k)
    return out

def scale(a,c):
    return {k:v*c for k,v in a.items() if v*c}

def sub(a,b):return add(a,scale(b,-1))

def mul(a,b):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            key=(i+k,j+l)
            out[key]=out.get(key,Q(0))+v*w
    return {k:v for k,v in out.items() if v}

def power(a,n):
    out=ONE
    for _ in range(n):out=mul(out,a)
    return out

def parse(rows):
    require(type(rows)is list,'coefficient rows type')
    require(len(rows)<=512,'bounded complete sparse coefficient list')
    out={}
    previous=None
    for row in rows:
        require(type(row)is dict and set(row)=={'powers','coefficient'},'coefficient schema')
        p=row['powers'];c=row['coefficient']
        require(type(p)is list and len(p)==2 and all(type(i)is int and 0<=i<=32 for i in p),'power vector')
        require(type(c)is str and 0<len(c)<=500,'rational string')
        v=Q(c);require(str(v)==c and v!=0,'canonical nonzero coefficient')
        k=tuple(p);require(previous is None or previous<k,'strict sparse monomial order');previous=k;require(k not in out,'duplicate monomial')
        out[k]=v
    return out

def terms(a):
    return [{'powers':list(k),'coefficient':str(v)} for k,v in sorted(a.items())]

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a or [ZERO]

def zadd(a,b):
    return trim([add(a[i] if i<len(a) else ZERO,b[i] if i<len(b) else ZERO)
                 for i in range(max(len(a),len(b)))])

def zscale(a,c):return trim([scale(x,c) for x in a])

def zmul(a,b):
    out=[ZERO for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=add(out[i+j],mul(x,y))
    return trim(out)

def zderivative(a):
    return trim([scale(a[i],i) for i in range(1,len(a))])

def zdivide(a,b):
    require(b[-1]==ONE,'monic outer divisor')
    a=trim(a);out=[ZERO for _ in range(max(1,len(a)-len(b)+1))]
    while a!=[ZERO] and len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]
        out[k]=add(out[k],c)
        a=zadd(a,[ZERO]*k+[scale(mul(c,v),-1) for v in b])
    return trim(out),trim(a)

def resultant(a,b):
    n,m=len(a)-1,len(b)-1;size=n+m
    rows=[]
    for i in range(m):
        rows.append([ZERO]*i+list(reversed(a))+[ZERO]*(m-i-1))
    for i in range(n):
        rows.append([ZERO]*i+list(reversed(b))+[ZERO]*(n-i-1))
    dp={0:ONE}
    for row in rows:
        new={}
        for mask,value in dp.items():
            for j,c in enumerate(row):
                if mask&(1<<j) or not c:continue
                term=mul(value,c)
                if (mask>>(j+1)).bit_count()%2:term=scale(term,-1)
                key=mask|(1<<j)
                new[key]=add(new.get(key,ZERO),term)
        dp=new
    return dp.get((1<<size)-1,ZERO)

def expand_y(a):
    return {(2*i,j):c for (i,j),c in a.items()}

def tensor_bernstein(a):
    n=max(i for i,j in a);m=max(j for i,j in a)
    first={}
    for k in range(n+1):
        for j in range(m+1):
            first[k,j]=sum(a.get((i,j),Q(0))*Q(comb(k,i),comb(n,i))
                           for i in range(k+1))
    return [[sum(first[k,j]*Q(comb(l,j),comb(m,j)) for j in range(l+1))
             for l in range(m+1)] for k in range(n+1)]

def u_trim(a):
    a = list(a)
    while len(a) > 1 and (not a[-1]):
        a.pop()
    return a or [Q(0)]

def u_add(a, b):
    return u_trim([(a[i] if i < len(a) else Q(0)) + (b[i] if i < len(b) else Q(0)) for i in range(max(len(a), len(b)))])

def u_scale(a, t):
    return u_trim([x * t for x in a])

def u_sub(a, b):
    return u_add(a, u_scale(b, -1))

def u_mul(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i + j] += x * y
    return u_trim(c)

def u_divide(a, b):
    a, b = (u_trim(a), u_trim(b))
    require(b != [0], 'zero polynomial divisor')
    q = [Q(0)] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        j, v = (len(a) - len(b), a[-1] / b[-1])
        q[j] += v
        a = u_sub(a, [Q(0)] * j + u_scale(b, v))
    return (u_trim(q), u_trim(a))

def zero_matrix():
    return [[Q(0) for _ in range(7)] for _ in range(7)]

def identity(c=Q(1)):
    out = zero_matrix()
    for i in range(7):
        out[i][i] = c
    return out

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(7)] for i in range(7)]

def matrix_mul(a, b):
    out = zero_matrix()
    for i in range(7):
        for k in range(7):
            if a[i][k]:
                for j in range(7):
                    if b[k][j]:
                        out[i][j] += a[i][k] * b[k][j]
    return out

def matrix_scale(a, c):
    return [[v * c for v in row] for row in a]

def matrix_inverse(a):
    out = [row[:] + e for row, e in zip(a, identity())]
    for j in range(7):
        pivot = next((i for i in range(j, 7) if out[i][j]), None)
        require(pivot is not None, 'singular seven-slot derivative')
        out[j], out[pivot] = (out[pivot], out[j])
        t = out[j][j]
        out[j] = [v / t for v in out[j]]
        for i in range(7):
            if i != j and out[i][j]:
                t = out[i][j]
                out[i] = [v - t * w for v, w in zip(out[i], out[j])]
    return [row[7:] for row in out]

def matrix_eval(a, H):
    out = zero_matrix()
    for c in reversed(a):
        out = matrix_add(matrix_mul(out, H), identity(c))
    return out

def matrix_trace(a):
    return sum((a[i][i] for i in range(7)))

def unique_object(pairs):
    value={}
    for key,item in pairs:
        require(key not in value,'duplicate JSON key')
        value[key]=item
    return value

def load_json(path):
    raw=Path(path).read_bytes()
    require(len(raw)<=100000,'oversized defining certificate or compact fixture')
    return json.loads(raw,object_pairs_hook=unique_object)

def typed_equal(a,b):
    require(type(a)is type(b),'whole fixture exact type')
    if type(a)is dict:
        require(set(a)==set(b),'whole fixture key set')
        for key in a:typed_equal(a[key],b[key])
    elif type(a)is list:
        require(len(a)==len(b),'whole fixture list length')
        for left,right in zip(a,b):typed_equal(left,right)
    else:require(a==b,'whole fixture scalar')

def certificate_schema(cert):
    fields={'domain','critical_quintic','inverse_common_denominator',
            'inverse_numerators','discriminant',
            'discriminant_divided_by_inverse_denominator',
            'angular_numerator_y_tau','angular_denominator_y_tau'}
    require(type(cert)is dict and set(cert)==fields,'complete certificate schema')
    require(type(cert['domain'])is str and cert['domain']==DOMAIN,'exact coefficient/physical domain')
    for name,length in [('critical_quintic',6),('inverse_numerators',5)]:
        require(type(cert[name])is list and len(cert[name])==length,'complete quintic slots')
        for rows in cert[name]:parse(rows)
    for name in fields-{'domain','critical_quintic','inverse_numerators'}:parse(cert[name])

def bidegree(poly):
    return [max(i for i,j in poly),max(j for i,j in poly)]

def variations(values):
    signs=[(x>0)-(x<0)for x in values if x]
    return sum(a!=b for a,b in zip(signs,signs[1:]))

def u_derivative(a):
    return u_trim([(i+1)*a[i+1]for i in range(len(a)-1)])

def root_count(a):
    chain=[a,u_derivative(a)]
    while True:
        rem=u_divide(chain[-2],chain[-1])[1]
        if rem==[0]:break
        chain.append(u_scale(rem,-1))
    at0=variations([p[0]for p in chain]);plus=variations([p[-1]for p in chain])
    minus=variations([p[-1]*(-1)**(len(p)-1)for p in chain])
    zero=int(a[0]==0)
    return {'positive_distinct':at0-plus,'negative_distinct':minus-at0-zero,
            'zero_distinct':zero,
            'gcd_degree':len(chain[-1])-1,
            'entire_sturm_chain':[[str(c)for c in row]for row in chain]}

def scalar(poly,y,tau):
    return sum(c*y**i*tau**j for (i,j),c in poly.items())
