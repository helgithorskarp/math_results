"""Separate coordinate bit model; columns use physical BLUE pages directly."""
from itertools import combinations

CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
P,S,H,K,C,L=13,50,43,23,3,60
OWN=(40,20); PATH_A=((0,4),(4,3),(1,2),(2,5));PATH_D=((0,5),(5,2),(1,3),(3,4))

def build(r,rows,sy,excess=(0,0,0)):
    n=[0]*16
    def e(i,j):n[i]|=1<<j;n[j]|=1<<i
    for i in range(1,11):e(0,i)
    for i in (2,11,12):e(1,i)
    for i in range(9,16):e(2,i)
    for i,j in CYCLE:e(i+3,j+3)
    for k,w in enumerate(OWN):
        for i in range(6):
            if w>>i&1:e(k+9,i+3)
    for k,w in enumerate((6,5) if r==0 else (5,6)):
        for i in range(3):
            if w>>i&1:e(k+9,i+13)
    for k,w in enumerate((6,3)):
        for i in range(3):
            if w>>i&1:e(k+11,i+13)
    for k,w in enumerate((*sy,*rows)):
        for i in range(6):
            if w>>i&1:e(k+11,i+3)
    degrees=(10,10,9,*([10]*8),6+sy[0].bit_count(),6+sy[1].bit_count(),
        6+rows[0].bit_count()+excess[0],6+rows[1].bit_count()+excess[1],7+rows[2].bit_count()+excess[2])
    q=tuple(degrees[i]-n[i].bit_count() for i in range(16))
    return tuple(n),degrees,q

def allowances(n,d):
    out={}
    for i,j in combinations(range(16),2):
        cap=3 if n[i]>>j&1 else d[i]+d[j]-14
        out[i,j]=out[j,i]=cap-(n[i]&n[j]).bit_count()
    return out

def permutation(which):
    p=list(range(16))
    pairs=((0,1),(2,4),(3,5)) if which=='phi' else ((2,3),(4,5))
    if which=='psi':p[9],p[10]=10,9
    for i,j in pairs:p[i+3],p[j+3]=j+3,i+3
    return tuple(p)

def transport(w,p):return sum(1<<(p[3+i]-3) for i in range(6) if w>>i&1)
