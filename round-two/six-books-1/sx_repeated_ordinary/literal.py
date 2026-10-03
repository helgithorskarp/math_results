"""Original ten-point neighborhood, set representation.

OLD/OLD_MAP are credited to the published six-books-1 root kernels,
in particular source061639acb07ffb71f8e35f2f05eb9372831e3155.
Adapted primitive source97a404ae86a493039e5ecdfde2baef674ea57487.
The endpoint rows here describe the different SX-repeated shell; no prior
SY or cross-shell exclusion is an input.
"""
from itertools import combinations

OLD=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
OLD_MAP=(2,1,3,4,5,6,7,8,9,10)
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=({3,5},{2,4})
P,S,H,K,C,L=13,50,43,23,3,60
LABELS=('u','v','a',*(f'X{i}' for i in range(6)),'SX0','SX1','SY0','SY1','T0','T1','T2')

def build(rows,sy,qend=(2,2,2,3,3),rename=(0,1,2),sx_q=(4,4),old_map=OLD_MAP):
    if len(rows)!=3 or len(sy)!=2 or len(qend)!=5 or sorted(rename)!=[0,1,2] or tuple(old_map)!=OLD_MAP:
        raise ValueError('whole original-label input and T renaming')
    if any(not isinstance(w,int) or not 0<=w<64 for w in (*rows,*sy)):
        raise ValueError('six-bit endpoint row')
    if any(not isinstance(k,int) or not 0<=k<=6 for k in qend):
        raise ValueError('six-point endpoint Q rank')
    red=[set() for _ in range(16)]
    def edge(i,j):red[i].add(j);red[j].add(i)
    for i,row in enumerate(OLD):
        edge(0,old_map[i])
        for j in row:
            if i<j:edge(old_map[i],old_map[j])
    for j in (11,12):edge(1,j)
    for j in range(11,16):edge(2,j)
    for z,ts in ((9,(1,2)),(10,(1,2)),(11,(0,2)),(12,(0,1))):
        for t in ts:edge(z,13+rename[t])
    endpoints=(11,12,*(13+t for t in rename))
    for z,w in zip(endpoints,(*sy,*rows)):
        for i in range(6):
            if w>>i&1:edge(z,3+i)
    degrees=[10,10,9]+[10]*6+[0]*7
    if len(sx_q)!=2 or any(type(k) is not int or not 0<=k<=6 for k in sx_q):raise ValueError("free SX Q ranks0..6")
    for z,k in zip((9,10),sx_q):degrees[z]=len(red[z])+k
    for z,k in zip(endpoints,qend):degrees[z]=len(red[z])+k
    q=tuple(degrees[i]-len(red[i]) for i in range(16))
    return red,tuple(degrees),q

def allowances(red,d):
    """Q common-red allowances, BLUE checked by physical known pages."""
    out={};known=set(range(16))
    for i,j in combinations(range(16),2):
        if j in red[i]:a=3-len(red[i]&red[j])
        else:
            blue=len((known-red[i]-{i})&(known-red[j]-{j}))
            a=(d[i]-len(red[i]))+(d[j]-len(red[j]))-blue
        out[i,j]=a
    return out
