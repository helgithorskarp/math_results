"""Private two-parameter G22 extension-certificate development.

Actual author: six-tammes-2, researcher.  Uses the committed 9193 model;
this file is not a completed proof or a publication. Version2 uses exact
within-A Gram identities and shared-plane cut identities; original saved
witnesses must be rechecked against this separately pinned backend.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
import importlib.util, sys

SOURCE=Path(__file__).resolve().parents[1]/'round-two/six-tammes-2/twenty-two-contact-strip'
sys.path.insert(0,str(SOURCE))
spec=importlib.util.spec_from_file_location('g22_strip_model',SOURCE/'model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I,D2,S=m.I,m.D2,m.S
LO=Q(577,1000);HI=Q('0.59260590292507377809642492233276')
ZLO=Q(9,10);ZHI=Q(7,5)
LABELS=(0,1,2,4,5,6,7,8,9,10,11,12,13,'cut')
QUAD=(7,8,10,11)
TRIPLES=tuple(combinations(range(14),3))
CRITICAL=TRIPLES.index(tuple(LABELS.index(j) for j in (1,4,7)))
CONTACTS=set(m.e.CONTACTS)
RHO=Q(893,1000);OUTER_BOUND=10
XX_TRIPLES=((0,4,6),(0,4,7),(1,4,7))
XX_WEIGHTS=(Q(1),Q(1),Q(4,5))
K_PAIRS={(6,7),(6,9),(7,9)}
H_PAIRS={(0,9),(5,6),(7,11)}
def merge(a,b):
    return D2(m.intersect(a.v,b.v),m.intersect(a.dt,b.dt),
              m.intersect(a.dz,b.dz),m.intersect(a.c,b.c))

def sign(a):return 1 if a.l>0 else -1 if a.h<0 else 0
def edot(a,b):return sum(x*y for x,y in zip(a,b))
def cm(A,rhs):
    pairs=(m.cross(A[1],A[2]),m.cross(A[2],A[0]),m.cross(A[0],A[1]))
    D=edot(A[0],pairs[0])
    C=[sum(rhs[j]*pairs[j][i] for j in range(3)) for i in range(3)]
    return C,D

def plain_solve(A,rhs):
    C,D=cm(A,rhs)
    dv=D.v if isinstance(D,D2) else D
    if not sign(dv):raise ArithmeticError('matrix nonsingularity unresolved')
    return [c/D for c in C]

def refined_solve(A,rhs):
    x=plain_solve(A,rhs)
    if not isinstance(x[0],D2):return x
    Av=[[a.v for a in row] for row in A]
    derivatives=[]
    try:
        for variable in ('dt','dz'):
            rr=[getattr(rhs[j],variable)-sum(getattr(a,variable)*v.v for a,v in zip(A[j],x)) for j in range(3)]
            derivatives.append(plain_solve(Av,rr))
    except ArithmeticError:
        return x
    return [D2(v.v,m.intersect(v.dt,derivatives[0][j]),
               m.intersect(v.dz,derivatives[1][j]),v.c) for j,v in enumerate(x)]

def geometry(P,t):
    rows={i:[(1-t)*v+t*sum(P[i]) for v in P[i]] for i in P}
    xx=[refined_solve([rows[i] for i in triple],[t]*3)
        for triple in XX_TRIPLES]
    n=[xx[0][j]+xx[1][j]+Q(4,5)*xx[2][j] for j in range(3)]
    nn=m.dot(n,n,t)
    if nn.v.l<=0:raise ArithmeticError('nonzero normal unresolved')
    length=nn.sqrt()
    rows['cut']=[(1-t)*v+t*sum(n) for v in n]
    rows['cut'][2]=merge(rows['cut'][2],Q(14,5)*t)
    return dict(P=P,t=t,n=n,nn=nn,length=length,
                A=[rows[i] for i in LABELS],rhs=[t]*13+[RHO*length],rows=rows,intersections=xx)

def gram_product(model,i,j):
    if i==j:return D2(1)
    pair=tuple(sorted((i,j)))
    if pair in CONTACTS:return model['t']
    cache=model.setdefault('products',{})
    if pair not in cache:
        t=model['t'];raw=m.dot(model['P'][i],model['P'][j],t)
        exact=None
        if pair in K_PAIRS:exact=t*(9*t*t-2*t-3)/(1+t)**2
        if pair in H_PAIRS:exact=4*t*t/(1+t)-1
        cache[pair]=raw if exact is None else merge(raw,exact)
    return cache[pair]

def normal_product(model,label):
    cache=model.setdefault('normal_products',{})
    if label not in cache:
        P,t,n=(model[k] for k in ('P','t','n'))
        constant=sum(w for w,triple in zip(XX_WEIGHTS,XX_TRIPLES) if label in triple)
        refined=constant*t+sum(w*m.dot(x,P[label],t) for w,triple,x in
            zip(XX_WEIGHTS,XX_TRIPLES,model['intersections']) if label not in triple)
        cache[label]=merge(m.dot(n,P[label],t),refined)
    return cache[label]

def core_cut(triple,model):
    if triple[-1]==13:return None
    labels=[LABELS[j] for j in triple]
    a=gram_product(model,labels[0],labels[1]);b=gram_product(model,labels[0],labels[2]);c=gram_product(model,labels[1],labels[2])
    determinant=1+2*a*b*c-a*a-b*b-c*c
    q=[(1-c)*(1+c-a-b),(1-b)*(1+b-a-c),(1-a)*(1+a-b-c)]
    residual=model['t']*sum(qi*normal_product(model,label) for qi,label in zip(q,labels))-RHO*model['length']*determinant
    return ('F',) if residual.v.l>0 else None

def gram3_classify(triple_index,model):
    triple=TRIPLES[triple_index]
    if triple[-1]==13:return None
    if triple_index==CRITICAL:return ('K',)
    labels=[LABELS[j] for j in triple]
    a=gram_product(model,labels[0],labels[1])
    b=gram_product(model,labels[0],labels[2])
    c=gram_product(model,labels[1],labels[2])
    determinant=1+2*a*b*c-a*a-b*b-c*c
    q=[(1-c)*(1+c-a-b),(1-b)*(1+b-a-c),(1-a)*(1+a-b-c)]
    # An independent triple of vectors has a positive Gram determinant,
    # regardless of the width or sign of its interval enclosure.
    if (model['t']**2*sum(q)-determinant).v.h<0:return ('T',)
    def center(v):return (v.c.l+v.c.h)/(2*S)
    scores={j:sum(center(qi)*center(gram_product(model,label,k)) for qi,k in zip(q,labels))-center(determinant)
            for j,label in enumerate(LABELS[:-1]) if j not in triple}
    for j in sorted(scores,key=lambda j:-scores[j]):
        residual=sum(qi*gram_product(model,LABELS[j],k) for qi,k in zip(q,labels))-determinant
        if residual.v.l>0:return ('R',j)
    return None

def bounded(model):
    P,t,rows=(model[k] for k in ('P','t','rows'))
    w=refined_solve([[P[i][j] for i in QUAD[:3]] for j in range(3)],[-v for v in P[QUAD[3]]])
    if any(v.v.l<=0 for v in w):raise ArithmeticError('positive spanning unresolved')
    vertices=[]
    for triple in combinations(QUAD,3):
        v=refined_solve([rows[i] for i in triple],[t]*3)
        if any(max(abs(x.v.l),abs(x.v.h))>=OUTER_BOUND*S for x in v):
            raise ArithmeticError('outer coordinate bound unresolved')
        vertices.append(v)
    return min(v.v.l for v in w),max(max(abs(x.v.l),abs(x.v.h)) for v in vertices for x in v)

def cut_gram(triple,model):
    if triple[-1]!=13:return None
    a,b=(LABELS[j] for j in triple[:2])
    P,n,t=(model[k] for k in ('P','n','t'))
    s=gram_product(model,a,b)
    delta=1-s*s
    if delta.v.l<=0:return None
    def product(j):return normal_product(model,j)
    na,nb=product(a),product(b)
    perpendicular=model['nn']-(na*na+nb*nb-2*s*na*nb)/delta
    if perpendicular.v.l<=0:return None
    height=RHO*model['length']-t*(na+nb)/(1+s)
    norm=2*t*t/(1+s)+height*height/perpendicular
    return ('G',) if norm.v.h<S else None

def classify(triple_index,model,use_gram3=True):
    if triple_index==CRITICAL:return ('K',)
    if use_gram3:
        gram3=gram3_classify(triple_index,model)
        if gram3 is not None:return gram3
    triple=TRIPLES[triple_index]
    A,rhs,t=(model[k] for k in ('A','rhs','t'))
    cut=core_cut(triple,model)
    if cut is not None:return cut
    C,D=cm([A[j] for j in triple],[rhs[j] for j in triple])
    ds=sign(D.v);dh=max(abs(D.v.l),abs(D.v.h))
    for j,c in enumerate(C):
        if sign(c.v) and min(abs(c.v.l),abs(c.v.h))>OUTER_BOUND*dh:
            return ('C',j)
    if ds:
        x=[c/D for c in C]
        if m.dot(x,x,t).v.h<S:return ('N',)
    need_positive=ds>=0;need_negative=ds<=0;wp=wn=None
    # Float centers choose a promising inequality only.  Acceptance below uses
    # its exact outward-rounded interval, never a float sign or tolerance.
    def center(v):return (v.c.l+v.c.h)/(2*S)
    cc=[center(v) for v in C];dd=center(D)
    scores={j:sum(center(a)*v for a,v in zip(row,cc))-center(rhs[j])*dd
            for j,row in enumerate(A) if j not in triple}
    order=sorted(scores,key=lambda j:-abs(scores[j]))
    if ds:order.sort(key=lambda j:-ds*scores[j])
    for j in order:
        row=A[j]
        res=(edot(row,C)-rhs[j]*D).v
        if need_positive and res.l>0:wp=j;need_positive=False
        if need_negative and res.h<0:wn=j;need_negative=False
        if not need_positive and not need_negative:return ('H',wp,wn)
    # The Gram identity often avoids unstable direct division near cut vertices.
    gram=cut_gram(triple,model)
    if gram is not None:return gram
    return None

def packing_prune(P,t):
    for pair in m.e.PAIRS:
        if m.pair_gap(P,t,pair).v.l>0:return ('pair',*pair)
    return None

def box(td,ti,zd,zi):
    tw=(HI-LO)/2**td;zw=(ZHI-ZLO)/2**zd
    return LO+ti*tw,LO+(ti+1)*tw,ZLO+zi*zw,ZLO+(zi+1)*zw

def enc(v):return m.enc(v)
