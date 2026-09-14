"""Exact origin-anchored equilateral affine frames; coordinates in Q(sqrt5,sqrt33)."""
import hashlib, json
from fractions import Fraction as F
from pathlib import Path
from math import lcm
from itertools import combinations

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json'
SOURCE_HASH='41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729'
RAD=(1,5,33,165)
Z=(0,0,0,0)
def require(c,m):
    if not c: raise ValueError(m)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    out=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i^j]+=x*y*RAD[i&j]
    return tuple(out)
def scale(a,k): return tuple(k*x for x in a)
def det(a,b): return sub(mul(a[0],b[1]),mul(a[1],b[0]))
def points():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_HASH,'changed source')
    raw=json.loads(SOURCE.read_text())['coordinates']
    out=[]
    for k in range(509):
        x,y=[[F(t) for t in row] for row in raw[str(k)]]
        require(all(x[i]==0 for i in (1,3,4,6)) and all(y[i]==0 for i in (0,2,5,7)), 'source parity')
        out.append(((x[0],x[2],x[5],x[7]),(y[1],y[3],y[4]/3,y[6]/3)))
    den=lcm(*(t.denominator for p in out for row in p for t in row))
    out=[tuple(tuple(int(den*t) for t in row) for row in p) for p in out]
    require(len(set(out))==509 and out[0]==(Z,Z),'source labels')
    return out,den
def metric(a,b):
    ax,ay=a; bx,by=b
    xx=add(sub(mul(by,by),mul(by,ay)),mul(ay,ay))
    xy=sub(add(mul(by,ax),mul(ay,bx)),scale(add(mul(by,bx),mul(ax,ay)),2))
    yy=add(sub(mul(bx,bx),mul(bx,ax)),mul(ax,ax))
    dd=mul(det(a,b),det(a,b))
    return xx,xy,yy,dd
def unit(q,d):
    x,y=d;xx,xy,yy,dd=q
    return add(add(mul(xx,mul(x,x)),mul(xy,mul(x,y))),mul(yy,mul(y,y)))==dd
def diff(a,b): return (sub(a[0],b[0]),sub(a[1],b[1]))
def is_original(q,den):
    xx,xy,yy,dd=q
    return xy==Z and scale(xx,den*den)==dd and scale(yy,den*den)==scale(dd,3)
def prime(p):
    return p>=2 and all(p%d for d in range(2,__import__('math').isqrt(p)+1))
def projection(p,r5,r33):
    require(prime(p) and r5*r5%p==5 and r33*r33%p==33, 'bad field projection')
    return lambda a: (a[0]+a[1]*r5+a[2]*r33+a[3]*r5*r33)%p
def prepare(work,p=1000000009,r5=0,r33=0):
    # Roots are supplied, checked, and never used as real approximations.
    proj=projection(p,r5,r33); P,den=points()
    groups={}
    for i,j in combinations(range(509),2):
        d=diff(P[j],P[i]); d=min(d,(neg(d[0]),neg(d[1])))
        groups.setdefault(d,[]).append((i,j))
    groups=sorted(groups.items())
    with (work/'input.txt').open('w') as f:
        f.write(f'{p} 509 {len(groups)}\n')
        for x,y in P: f.write(f'{proj(x)} {proj(y)}\n')
        for (x,y),edges in groups:
            xx,xy,yy=proj(mul(x,x)),proj(mul(x,y)),proj(mul(y,y))
            f.write(f'{xx} {xy} {yy} {len(edges)} '+' '.join(f'{i} {j}' for i,j in edges)+'\n')
    data={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'denominator':den,'points':509,'difference_groups':len(groups),'pairs':sum(len(e) for d,e in groups),'p':p,'sqrt5':r5,'sqrt33':r33}
    (work/'input_summary.json').write_text(json.dumps(data,indent=2)+'\n')
    print(data,flush=True)
    return P,groups
