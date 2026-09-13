"""Direct physical edge checking, caching only proven unit multiples.

Every physical pair is examined. No event polynomial or edge-owner inventory
is imported. Cache equivalence uses its representative digit displacement and
an exact Eisenstein-unit rotation; one squared norm is evaluated per class.
"""
from itertools import product
from interface import A,physical
DIGITS=((0,0),(1,0),(0,1))
WORDS=tuple(product(range(3),repeat=5))
def class_key(left,right):
    row=tuple((DIGITS[a][0]-DIGITS[b][0],DIGITS[a][1]-DIGITS[b][1]) for a,b in zip(left,right))
    u,v=next((u,v) for u,v in row if u or v)
    A.need(u*u+u*v+v*v==1,'first displacement coefficient is a unit')
    # Multiply by conjugate(u+v omega)=(u+v)-v omega.
    return tuple((a*(u+v)+b*v,-a*v+b*u) for a,b in row)

def graph(field):
    points,labels=physical.coordinates(field);representatives=[None]*len(points)
    for word,p in zip(WORDS,labels):
        if representatives[p] is None:representatives[p]=word
    q=physical.polynomial(field['q']);one=physical.polynomial([1]);cache={};edges=[]
    for a,(ax,ay) in enumerate(points):
        for b in range(a):
            key=class_key(representatives[a],representatives[b])
            if key not in cache:
                bx,by=points[b];dx,dy=ax-bx,ay-by
                cache[key]=not((dx*dx+3*dy*dy-one)%q)
            if cache[key]:edges.append([b,a])
    edges.sort();triangle=[labels[i] for i in (0,81,162)]
    A.need(len(set(triangle))==3 and all(sorted((a,b)) in edges for a in triangle for b in triangle if a<b),'universal physical triangle')
    return points,labels,edges,triangle,len(cache)
