"""Independent generic arithmetic for Q(sqrt3,sqrt11,sqrt247).

Three independent square classes give the bit-indexed eight-element basis.
Coordinate values in this module are physical coordinates times 36.
"""
from fractions import Fraction as F

ZERO=(0,)*8
ONE=(1,)+(0,)*7

def scalar(v):return (v,)+(0,)*7
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-v for v in a)
def sub(a,b):return add(a,neg(b))
def scale(a,v):return tuple(x*v for x in a)
def mul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if not y:continue
            common=i&j;factor=1
            for k,p in enumerate((3,11,247)):
                if common & (1<<k):factor*=p
            out[i^j]+=factor*x*y
    return tuple(out)

def psub(a,b):return sub(a[0],b[0]),sub(a[1],b[1])
def padd(a,b):return add(a[0],b[0]),add(a[1],b[1])
def conjugate(p):return p[0],neg(p[1])
def cmul(a,b):
    return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def pscale(p,v):return scale(p[0],v),scale(p[1],v)
def norm(p):return add(mul(p[0],p[0]),mul(p[1],p[1]))
def distance(p,q):return norm(psub(p,q))

def point(row):
    a,b,c,d=row
    return (0,a,b,0,0,0,0,0),(c,0,0,d,0,0,0,0)

def row(p):
    x,y=p
    if any(x[i] for i in (0,3,4,5,6,7)) or any(y[i] for i in (1,2,4,5,6,7)):
        raise ValueError('Unexpected field support')
    out=(x[1],x[2],y[0],y[3])
    if any(F(v).denominator!=1 for v in out):raise ValueError('Nonintegral row')
    return tuple(int(v) for v in out)

ROT120=(scalar(F(-1,2)),(0,F(1,2),0,0,0,0,0,0))
ROT_SPINDLE=(scalar(F(119,128)),(0,0,0,0,F(3,128),0,0,0))

def frame(source_a,source_b,target_a,target_b,squared_length,reflection=False):
    """Return p -> translation + multiplier*(p or conjugate(p))."""
    if reflection:source_a,source_b=conjugate(source_a),conjugate(source_b)
    delta=psub(source_b,source_a)
    if norm(delta)!=scalar(squared_length):raise ValueError('Source frame length')
    multiplier=pscale(cmul(psub(target_b,target_a),conjugate(delta)),F(1,squared_length))
    if norm(multiplier)!=ONE:raise ValueError('Frame is not an isometry')
    translation=psub(target_a,cmul(multiplier,source_a))
    return multiplier,translation,reflection

def apply(frame,p):
    multiplier,translation,reflection=frame
    if reflection:p=conjugate(p)
    return padd(translation,cmul(multiplier,p))
