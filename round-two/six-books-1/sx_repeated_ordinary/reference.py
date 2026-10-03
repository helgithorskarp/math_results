"""Separately constructed coordinate bit model; no old-neighborhood import."""
from itertools import combinations, product

CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=(40,20)
PATH1=((0,4),(4,3),(1,2),(2,5))
PATH2=((0,5),(5,2),(1,3),(3,4))
P,S,H,K,C,L=13,50,43,23,3,60

def build(rows,sy,qend=(2,2,2,3,3),rename=(0,1,2),sx_q=(4,4)):
    n=[0]*16
    def edge(i,j):n[i]|=1<<j;n[j]|=1<<i
    for i in range(1,11):edge(0,i)
    for i in (2,11,12):edge(1,i)
    for i in range(9,16):edge(2,i)
    for i,j in CYCLE:edge(3+i,3+j)
    for k,w in enumerate(OWN):
        for i in range(6):
            if w>>i&1:edge(9+k,3+i)
    # Direct incidence words; both SX omissions are T0.
    for k,w in enumerate((6,6,5,3)):
        for t in range(3):
            if w>>t&1:edge(9+k,13+rename[t])
    for z,w in zip((11,12,*(13+t for t in rename)),(*sy,*rows)):
        for i in range(6):
            if w>>i&1:edge(z,3+i)
    d=[10,10,9]+[10]*6+[0]*7
    for z,k in zip((9,10),sx_q):d[z]=n[z].bit_count()+k
    for z,k in zip((11,12,*(13+t for t in rename)),qend):d[z]=n[z].bit_count()+k
    q=tuple(d[i]-n[i].bit_count() for i in range(16))
    return tuple(n),tuple(d),q

def allowances(n,d):
    return {(i,j):(3 if n[i]>>j&1 else d[i]+d[j]-14)-(n[i]&n[j]).bit_count()
            for i,j in combinations(range(16),2)}
