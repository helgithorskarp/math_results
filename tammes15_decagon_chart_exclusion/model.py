"""Exact polynomial model for the fourth decagon and rational sphere chart."""
from fractions import Fraction as Q
import kernel as P
LABELS=(0,1,2,3,4,5,6,7,11,12)
FOLDS=((1,2,7,6),(0,1,7,2),(4,2,6,7),(3,2,4,6),(5,4,6,2),(11,0,1,7),(12,0,7,1))

def core_points():
    points={2:[P.ONE,P.ZERO,P.ZERO],6:[P.ZERO,P.ONE,P.ZERO],7:[P.ZERO,P.ZERO,P.ONE]}
    for new,i,j,old in FOLDS:
        P.need(new not in points and {i,j,old}<=set(points),'ordered reflection')
        points[new]=[P.sub(P.mul(P.T,P.add(x,y)),z) for x,y,z in zip(points[i],points[j],points[old])]
    D=P.power(P.S,3)
    def substitute(p):
        P.need(len(p)<=4,'reflection degree at most three')
        result=P.ZERO
        for k,c in enumerate(p):
            result=P.add(result,P.scale(P.mul(P.power((0,2),k),P.power(P.S,3-k)),c))
        return result
    P.need(set(points)==set(LABELS),'ten labels')
    return {i:[substitute(p) for p in points[i]] for i in LABELS},D

def forms(index):
    P.need(index==3,"fixed fourth core");points,D=core_points();result=[]
    g0=(1,0,-1);g1=(0,1,-1)
    for i in LABELS:
        n=P.normal(points[i]);td=P.mul(P.T,D);a=P.sub(n[0],td)
        result.append([P.scale(P.add(n[0],td),-1),
                       P.scale(P.sub(n[1],P.mul(P.T,n[0])),2),
                       P.scale(P.sub(n[2],P.mul(P.T,n[0])),2),
                       P.mul(a,g0),P.scale(P.mul(a,g1),2)])
    return result

def t_bernstein_forms(index,lo,hi):
    rows=forms(index);degree=max(len(p)-1 for row in rows for p in row)
    return [[P.bernstein(tuple(p)+(0,)*(degree+1-len(p)),lo,hi) for p in row] for row in rows]

def exact_box_coefficients(row,cell):
    depth,i,j=cell;h=Q(8,2**depth);u=-4+i*h;v=-4+j*h
    f,l,m,a,b=row
    c00=P.add(P.add(f,P.scale(l,u)),P.add(P.scale(m,v),P.add(P.scale(a,u*u+v*v),P.scale(b,u*v))))
    c10=P.scale(P.add(l,P.add(P.scale(a,2*u),P.scale(b,v))),h)
    c01=P.scale(P.add(m,P.add(P.scale(a,2*v),P.scale(b,u))),h)
    c20=P.scale(a,h*h);c11=P.scale(b,h*h)
    out=[]
    for r in range(3):
        for s in range(3):
            out.append(P.add(c00,P.add(P.scale(c10,Q(r,2)),P.add(P.scale(c01,Q(s,2)),
                P.add(P.scale(c20,int(r==2)+int(s==2)),P.scale(c11,Q(r*s,4)))))))
    return out

def gmetric(z,t):
    u,v=z
    return (1-t*t)*(u*u+v*v)+2*t*(1-t)*u*v

def box_bounds(cell):
    depth,i,j=cell;h=Q(8,2**depth)
    return (-4+i*h,-4+j*h),(-4+(i+1)*h,-4+(j+1)*h)

def exact_rmin(cell,t):
    lo,hi=box_bounds(cell)
    if all(a<=0<=b for a,b in zip(lo,hi)):return Q(1)
    choices=[];ratio=t/(1+t)
    for fixed in range(2):
        other=1-fixed
        for v in (lo[fixed],hi[fixed]):
            z=[Q(0),Q(0)];z[fixed]=v
            z[other]=max(lo[other],min(hi[other],-ratio*v))
            choices.append(gmetric(z,t))
    return 1+min(choices)

def exact_qmax(left,right,t):
    a,b=box_bounds(left);c,d=box_bounds(right)
    lo=[a[i]-d[i] for i in range(2)];hi=[b[i]-c[i] for i in range(2)]
    return max(gmetric((u,v),t) for u in (lo[0],hi[0]) for v in (lo[1],hi[1]))
