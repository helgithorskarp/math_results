"""Exact one-parameter formulas for registered affine strip copies.

An affine integer is (coefficient of k, constant). Atomic predicates are
linear equality/inequality or congruence modulo3. No search or solver.
"""
from strip_columns import MATRICES,UV_DIRS,require

COLS=((-2,(1,-1),(1,-1)),(-1,(1,0),(1,0)),(0,(0,0),(1,0)),
      (1,(0,1),(1,0)),(2,(0,2),(1,1)),(3,(0,2),(1,1)))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(n,a):return n*a[0],n*a[1]
def sub(a,b):return add(a,scale(-1,b))
def constant(n):return 0,n
def value(a,k):return a[0]*k+a[1]

def atom(kind,a,modulus=None):
    if kind=='mod' and a[0]%modulus==0:return a[1]%modulus==0
    if a[0]==0:
        if kind=='ge':return a[1]>=0
        if kind=='eq':return a[1]==0
        if kind=='mod':return a[1]%modulus==0
    return (kind,*a) if modulus is None else (kind,*a,modulus)
def both(*rows):
    if False in rows:return False
    rows=tuple(r for r in rows if r is not True)
    return True if not rows else rows[0] if len(rows)==1 else ('and',*rows)
def either(*rows):
    if True in rows:return True
    rows=tuple(r for r in rows if r is not False)
    return False if not rows else rows[0] if len(rows)==1 else ('or',*rows)
def neg(row):return not row if type(row) is bool else ('not',row)
def evaluate(row,k):
    if type(row) is bool:return row
    kind=row[0]
    if kind=='and':return all(evaluate(r,k) for r in row[1:])
    if kind=='or':return any(evaluate(r,k) for r in row[1:])
    if kind=='not':return not evaluate(row[1],k)
    n=row[1]*k+row[2]
    if kind=='ge':return n>=0
    if kind=='eq':return n==0
    if kind=='mod':return n%row[3]==0
    raise ValueError('Unknown formula')

def pose(row):return tuple(row['matrix']),tuple(row['u']),tuple(row['v'])
def inverse(g):
    (a,b,c,d),u,v=g;det=a*d-b*c
    require(det in (-1,1),'Non-D6 determinant')
    m=(d*det,-b*det,-c*det,a*det)
    return m,scale(-1,add(scale(m[0],u),scale(m[1],v))),scale(-1,add(scale(m[2],u),scale(m[3],v)))
def compose(g,h):
    (a,b,c,d),u,v=g;(e,f,j,l),x,y=h
    return (a*e+b*j,a*f+b*l,c*e+d*j,c*f+d*l),add(add(scale(a,x),scale(b,y)),u),add(add(scale(c,x),scale(d,y)),v)
def relative(g,h):return compose(inverse(g),h)
def point_membership(g,point):
    m,a,b=inverse(g);u,v=point
    x=add(add(scale(m[0],u),scale(m[1],v)),a)
    y=add(add(scale(m[2],u),scale(m[3],v)),b)
    return either(*(both(atom('eq',sub(x,constant(c))),atom('ge',sub(y,lo)),
                         atom('ge',sub(hi,y))) for c,lo,hi in COLS))

def intersection(g):
    (alpha,beta,gamma,delta),a,b=g
    require(g[0] in MATRICES,'Non-D6 action')
    clauses=[]
    for c,lo,hi in COLS:
        for d,target_lo,target_hi in COLS:
            if beta==0:
                left,right=(lo,hi) if delta==1 else (hi,lo)
                low=add(constant(gamma*c),add(scale(delta,left),b))
                high=add(constant(gamma*c),add(scale(delta,right),b))
                clauses.append(both(atom('eq',add(a,constant(alpha*c-d))),
                    atom('ge',sub(target_hi,low)),atom('ge',sub(high,target_lo))))
            else:
                B=abs(beta);require(B==3,'Unexpected denominator')
                n=scale(1 if beta>0 else -1,sub(constant(d-alpha*c),a))
                w=add(scale(B,add(constant(gamma*c),b)),scale(delta,n))
                clauses.append(both(atom('mod',n,B),atom('ge',sub(n,scale(B,lo))),
                    atom('ge',sub(scale(B,hi),n)),atom('ge',sub(w,scale(B,target_lo))),
                    atom('ge',sub(scale(B,target_hi),w))))
    return either(*clauses)

def touching(g):
    m,a,b=g
    return either(*(intersection((m,sub(a,constant(du)),sub(b,constant(dv)))) for du,dv in UV_DIRS))
def allowed(g,atlas):
    m,a,b=g
    return either(*(both(atom('eq',sub(a,x)),atom('eq',sub(b,y))) for n,x,y in atlas if n==m))
def conflict(g,h,atlas):
    rel=relative(g,h)
    return either(intersection(rel),both(touching(rel),neg(allowed(rel,atlas)),),
                  both(touching(rel),neg(allowed(inverse(rel),atlas))))

def atoms(rows):
    out=set();todo=list(rows)
    while todo:
        r=todo.pop()
        if type(r) is bool:continue
        if r[0] in ('and','or','not'):todo.extend(r[1:])
        else:out.add(r)
    return out
def partition(rows,minimum=6):
    cuts={minimum};period=1
    for row in atoms(rows):
        kind,A,B,*rest=row
        if kind=='mod':
            require(rest==[3],'Only period3 supported');period=3;continue
        if kind=='ge':
            cut=-(B//A) if A>0 else (-B)//A+1
            if cut>minimum:cuts.add(cut)
        elif kind=='eq':
            if (-B)%A==0:
                point=(-B)//A
                if point>=minimum:cuts.update((point,point+1))
        else:raise ValueError('Unknown atom')
    ordered=sorted(cuts);representatives=[];intervals=[]
    for j,lo in enumerate(ordered):
        hi=ordered[j+1]-1 if j+1<len(ordered) else None
        samples=[]
        for residue in range(period):
            k=lo+(residue-lo)%period
            if hi is None or k<=hi:samples.append(k);representatives.append(k)
        intervals.append({'lo':lo,'hi':hi,'representatives':samples})
    return {'minimum':minimum,'period':period,'cuts':ordered,'intervals':intervals,
            'representatives':representatives,'atomic_predicates':len(atoms(rows))}
