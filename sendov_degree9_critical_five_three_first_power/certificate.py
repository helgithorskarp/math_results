"""Exact shared-denominator tensor Bernstein arithmetic, four variables.

Adapted from six-sendov-1 source 49de03a4636330c86a240bc97d772720991ae548,
certificate.py SHA256 2cc888e66b64a8b89aaa88397c3229831239d792017baf6e5d1f72c581619856.
Self-contained author reuse, not independent review. The new rational-ratio
subdivision supports the signed 5+3 imbalance interval.
"""
from fractions import Fraction as F
from math import comb,lcm,prod
from collections import defaultdict

def bernstein(p,degrees=None):
    if degrees is None:
        degrees=tuple(max(e[i] for e in p) for i in range(4))
    shape=tuple(d+1 for d in degrees)
    stride=tuple(prod(shape[i+1:]) for i in range(4))
    initial=lcm(*(v.denominator for v in p.values()))
    data=[0]*prod(shape)
    for e,v in p.items():data[sum(e[i]*stride[i] for i in range(4))]=int(v*initial)
    denominator=initial
    for axis,n in enumerate(degrees):
        norm=lcm(*(comb(n,k) for k in range(n+1)))
        weights=[[comb(i,k)*(norm//comb(n,k)) for k in range(i+1)] for i in range(n+1)]
        out=[0]*len(data);step=stride[axis];block=step*(n+1)
        for outer in range(0,len(data),block):
            for inner in range(step):
                offset=outer+inner
                for i,w in enumerate(weights):
                    out[offset+i*step]=sum(data[offset+k*step]*v for k,v in enumerate(w))
        data=out;denominator*=norm
    return data,denominator,degrees

def affine_cell(p,axis,low,high):
    out=defaultdict(F)
    for e,v in p.items():
        for j in range(e[axis]+1):
            f=list(e);f[axis]=j
            out[tuple(f)]+=v*comb(e[axis],j)*low**(e[axis]-j)*(high-low)**j
    return {e:v for e,v in out.items() if v}

def invert(values,den,degrees):
    """Inverse basis identity, independent of the forward weights."""
    shape=[d+1 for d in degrees]
    stride=[prod(shape[i+1:]) for i in range(4)]
    data=values.copy()
    for axis,n in enumerate(degrees):
        step=stride[axis];block=step*(n+1);out=[0]*len(data)
        for outer in range(0,len(data),block):
            for inner in range(step):
                offset=outer+inner
                for k in range(n+1):
                    out[offset+k*step]=comb(n,k)*sum((-1)**(k-j)*comb(k,j)*data[offset+j*step] for j in range(k+1))
        data=out
    result={}
    for index,v in enumerate(data):
        if v:
            e=tuple((index//stride[i])%shape[i] for i in range(4))
            result[e]=F(v,den)
    return result

def split(data,den,degrees,axis):
    """Independent midpoint de Casteljau transform on an existing tensor."""
    n=degrees[axis];shape=[d+1 for d in degrees]
    step=prod(shape[axis+1:]);block=step*(n+1)
    left=[0]*len(data);right=[0]*len(data)
    lw=[[comb(i,k)*2**(n-i) for k in range(i+1)] for i in range(n+1)]
    rw=[[comb(n-i,k)*2**i for k in range(n-i+1)] for i in range(n+1)]
    for outer in range(0,len(data),block):
        for inner in range(step):
            offset=outer+inner
            for i in range(n+1):
                left[offset+i*step]=sum(data[offset+k*step]*w for k,w in enumerate(lw[i]))
                right[offset+i*step]=sum(data[offset+(i+k)*step]*w for k,w in enumerate(rw[i]))
    return (left,den*2**n),(right,den*2**n)

def split_at(data,den,degrees,axis,ratio):
    """De Casteljau subdivision at an arbitrary exact rational ratio."""
    ratio=F(ratio)
    if not 0<ratio<1:raise ValueError('Subdivision ratio must be in (0,1)')
    p,q=ratio.numerator,ratio.denominator
    n=degrees[axis];shape=[d+1 for d in degrees]
    step=prod(shape[axis+1:]);block=step*(n+1)
    left=[0]*len(data);right=[0]*len(data)
    lw=[[comb(i,k)*p**k*(q-p)**(i-k)*q**(n-i) for k in range(i+1)] for i in range(n+1)]
    rw=[[comb(n-i,k)*p**k*(q-p)**(n-i-k)*q**i for k in range(n-i+1)] for i in range(n+1)]
    for outer in range(0,len(data),block):
        for inner in range(step):
            offset=outer+inner
            for i in range(n+1):
                left[offset+i*step]=sum(data[offset+k*step]*w for k,w in enumerate(lw[i]))
                right[offset+i*step]=sum(data[offset+(i+k)*step]*w for k,w in enumerate(rw[i]))
    return (left,den*q**n),(right,den*q**n)
