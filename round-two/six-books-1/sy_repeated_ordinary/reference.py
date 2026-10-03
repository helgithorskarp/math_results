"""Separately constructed coordinate bit model; no old-neighborhood import."""
from itertools import combinations, product

CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=(40,20)
PATH1=((0,4),(4,3),(1,2),(2,5))
PATH2=((0,5),(5,2),(1,3),(3,4))
P,S,H,K,C,L=13,50,43,23,3,60

def build(rows,sy,qend=(2,2,4,2,2),rename=(0,1,2)):
    n=[0]*16
    def edge(i,j):n[i]|=1<<j;n[j]|=1<<i
    for i in range(1,11):edge(0,i)
    for i in (2,11,12):edge(1,i)
    for i in range(9,16):edge(2,i)
    for i,j in CYCLE:edge(3+i,3+j)
    for k,w in enumerate(OWN):
        for i in range(6):
            if w>>i&1:edge(9+k,3+i)
    # Direct incidence words; the repeated omission is T0.
    for k,w in enumerate((5,3,6,6)):
        for t in range(3):
            if w>>t&1:edge(9+k,13+rename[t])
    for z,w in zip((11,12,*(13+t for t in rename)),(*sy,*rows)):
        for i in range(6):
            if w>>i&1:edge(z,3+i)
    d=[10,10,9]+[10]*8+[0]*5
    for z,k in zip((11,12,*(13+t for t in rename)),qend):d[z]=n[z].bit_count()+k
    q=tuple(d[i]-n[i].bit_count() for i in range(16))
    return tuple(n),tuple(d),q

def allowances(n,d):
    return {(i,j):(3 if n[i]>>j&1 else d[i]+d[j]-14)-(n[i]&n[j]).bit_count()
            for i,j in combinations(range(16),2)}

def terminal_cases():
    covers=[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in CYCLE)]
    a=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in PATH1)]
    b=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in PATH2)]
    pairs=[(x,y) for x,y in product(a,b) if x|y==63]
    return sorted((x,y,u,v) for x,y in pairs for u,v in product(covers,repeat=2)
                  if u|v==63 and all((z&w).bit_count()<=2 for z,w in product((u,v),(x,y))))
