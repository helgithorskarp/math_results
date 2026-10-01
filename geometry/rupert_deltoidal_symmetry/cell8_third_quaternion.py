"""Exact generic quaternion identities and rational matrix regressions."""
from fractions import Fraction as F
import hashlib,json,itertools,time
if not __debug__:raise RuntimeError('quaternion verification requires assertions')
N=5;ZERO={};ONE={(0,)*N:F(1)}
def var(i):
    key=[0]*N;key[i]=1;return {tuple(key):F(1)}
def add(a,b):
    d=a.copy()
    for e,c in b.items():d[e]=d.get(e,F(0))+c
    return {e:c for e,c in d.items() if c}
def neg(a):return {e:-c for e,c in a.items()}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    d={}
    for e,c in a.items():
        for f,k in b.items():
            g=tuple(x+y for x,y in zip(e,f));d[g]=d.get(g,F(0))+c*k
    return {e:c for e,c in d.items() if c}
def scale(c,a):return {e:c*k for e,k in a.items() if c*k}
def sq(a):return mul(a,a)
def sum_poly(xs):
    out={}
    for x in xs:out=add(out,x)
    return out
def dot(a,b):return sum_poly([mul(x,y) for x,y in zip(a,b)])
def cross(a,b):
    return [sub(mul(a[1],b[2]),mul(a[2],b[1])),
            sub(mul(a[2],b[0]),mul(a[0],b[2])),
            sub(mul(a[0],b[1]),mul(a[1],b[0]))]
def quaternion(a,b):
    s,v=a;t,w=b
    return sub(mul(s,t),dot(v,w)),[sum_poly([mul(s,y),mul(t,x),z]) for x,y,z in zip(v,w,cross(v,w))]
def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def cayley(v):
    r=sum(x*x for x in v);x,y,z=v
    skew=[[0,-z,y],[z,0,-x],[-y,x,0]]
    return [[((1-r)*(i==j)+2*v[i]*v[j]+2*skew[i][j])/(1+r) for j in range(3)] for i in range(3)]
def run():
    start=time.monotonic();a,b,c,d,x=[var(i) for i in range(N)]
    dp=add(mul(a,c),mul(b,d));h=sub(mul(a,d),mul(b,c))
    scalar=add(add(ONE,dp),mul(x,h))
    vector=[add(sub(c,a),mul(x,add(d,b))),
            sub(sub(d,b),mul(x,add(c,a))),
            add(h,mul(x,sub(ONE,dp)))]
    actual=quaternion(quaternion((ONE,[c,d,ZERO]),(ONE,[ZERO,ZERO,x])),(ONE,[neg(a),neg(b),ZERO]))
    assert actual==(scalar,vector)
    norm_product=mul(mul(sum_poly([ONE,sq(a),sq(b)]),sum_poly([ONE,sq(c),sq(d)])),add(ONE,sq(x)))
    assert sum_poly([sq(scalar),*(sq(v) for v in vector)])==norm_product
    n0=sum_poly([sq(sub(c,a)),sq(sub(d,b)),sq(h)])
    n2=sum_poly([ONE,sq(a),sq(b),sq(c),sq(d),sq(dp)])
    direct=sum_poly([n0,mul(sq(x),n2),scale(-2,mul(mul(x,h),add(ONE,dp)))])
    assert dot(vector,vector)==direct
    first=[(F(0),F(0)),(F(1,9),F(1,15)),(F(-1,8),F(1,20)),(F(1,30),F(-1,10))]
    second=[(F(0),F(0)),(F(1,23),F(-1,18)),(F(-1,17),F(-1,16))]
    rolls=[F(0),F(1,64),F(-1,64),F(1,32),F(-1,32),F(1),F(-1)]
    matrix_checks=0
    for (av,bv),(cv,dv),xv in itertools.product(first,second,rolls):
        dpv=av*cv+bv*dv;hv=av*dv-bv*cv;sv=1+dpv+xv*hv
        vv=(cv-av+xv*(dv+bv),dv-bv-xv*(cv+av),hv+xv*(1-dpv))
        assert sv>0
        actual_matrix=mm(mm(cayley((cv,dv,F(0))),cayley((F(0),F(0),xv))),cayley((-av,-bv,F(0))))
        assert actual_matrix==cayley(tuple(v/sv for v in vv))
        matrix_checks+=9
    records=[sorted((list(e),str(c)) for e,c in p.items()) for p in [scalar,*vector,norm_product,direct]]
    record={'agent':'six-rupert-1','role':'researcher','pass_number':26,
        'status':'exact generic quaternion identities for actual proper transports and signed roll',
        'generic_variables':5,'product_vector_identities':4,'norm_product_identity':True,
        'orthogonal_roll_squared_numerator_identity':True,'rational_matrix_comparisons':matrix_checks,
        'generic_coefficient_sha256':hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),
        'elapsed_seconds':time.monotonic()-start}
    print(json.dumps(record,indent=2))
    return record
if __name__=='__main__':run()
