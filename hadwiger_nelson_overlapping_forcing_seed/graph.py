"""Producer for the two-copy spindle of the certified equal-pair graph."""
from itertools import combinations
from lattice import edges as lattice_edges

def crossunit(p,q,den=1):
    a,b,c,d=p;e,f,h,k=q
    if a*h+11*b*k-c*e-11*d*f or b*h+3*a*k-c*f-3*d*e:
        return False
    ap=3*a*a+11*b*b+c*c+33*d*d;bp=2*a*b+2*c*d
    aq=3*e*e+11*f*f+h*h+33*k*k;bq=2*e*f+2*h*k
    dot0=3*a*e+11*b*f+c*h+33*d*k
    dot1=a*f+b*e+c*k+d*h
    return (64*(ap+aq)-119*dot0==64*1296*den*den
            and 64*(bp+bq)-119*dot1==0)

def spindle(points,den=1):
    if list(points[0])!=[0,0,0,0]:raise ValueError('Origin must be first')
    n=len(points);es=lattice_edges(points,den)
    second=lambda i:n+i-1 if i else 0
    result=set(map(tuple,es))
    result.update(tuple(sorted((second(i),second(j)))) for i,j in es)
    cross=[]
    for i in range(1,n):
        for j in range(1,n):
            if crossunit(points[i],points[j],den):
                result.add((i,second(j)));cross.append([i,j])
    labels=[[0]+list(p) for p in points]+[[1]+list(p) for p in points[1:]]
    return labels,[list(e) for e in sorted(result)],cross
