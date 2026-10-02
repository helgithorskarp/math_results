"""Independent coordinate bit matrices and ordinary endpoint inequalities."""
from itertools import combinations, product

CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=(40,20)
SHAPES=((3,19,35,50),(13,29,45,61,60),(11,27,43,59,58),(7,23,39,55,54))
E4=((0,4),(0,5),(1,2),(1,3))

def build(r,rows,sy):
    red=[0]*16
    def e(i,j):red[i]|=1<<j;red[j]|=1<<i
    for j in (1,2,*range(3,11)):e(0,j)
    for j in (2,11,12):e(1,j)
    for j in range(9,16):e(2,j)
    for i,j in CYCLE:e(i+3,j+3)
    for j,w in enumerate(OWN):
        for i in range(6):
            if w>>i&1:e(j+9,i+3)
    for j,w in enumerate((6,5) if r==0 else (5,6)):
        for k in range(3):
            if w>>k&1:e(j+9,k+13)
    for j,w in enumerate((6,3)):
        for k in range(3):
            if w>>k&1:e(j+11,k+13)
    for j,w in enumerate((*sy,*rows)):
        for i in range(6):
            if w>>i&1:e(j+11,i+3)
    degrees=(10,10,9,*([10]*8),6+sy[0].bit_count(),6+sy[1].bit_count(),
             6+rows[0].bit_count(),6+rows[1].bit_count(),7+rows[2].bit_count())
    qr=tuple(degrees[i]-red[i].bit_count() for i in range(16))
    return tuple(red),degrees,qr

def valid(red,d,qr):
    return all((red[i]&red[j]).bit_count()+max(0,qr[i]+qr[j]-6)
               <=(3 if red[i]>>j&1 else d[i]+d[j]-14)
               for i,j in combinations(range(16),2))

def simple_conditions(s0,s1,t0,t1):
    # Ordinary equations(5),(6) and three T-neighbor cover bounds.
    return (((s0>>4&1)+(s1>>4&1)+(t1>>4&1)>=2)
            and ((s0>>5&1)+(s1>>5&1)+(t0>>5&1)>=2)
            and all((a&b).bit_count()<=2 for a,b in ((s1,t0),(s1,t1),(s0,t1)))
            and (t0|t1)&49==49)

def elementary_endpoint_cases():
    answer=[]
    for s0,s1,t0,t1 in product(*SHAPES):
        if s0==50:continue # ordinary SY0--SX0 marker-union obstruction
        if simple_conditions(s0,s1,t0,t1):answer.append((t0,t1,s0,s1))
    return sorted(answer)

def transport(r,side):
    x=list(range(6));k=list(range(16));q=list(range(6))
    if r:
        for a,b in ((2,3),(4,5)):x[a],x[b]=x[b],x[a]
        k[9],k[10]=10,9;q[0],q[1]=1,0
    if side=='S':
        swap={0:1,1:0,2:4,4:2,3:5,5:3}
        x=[swap[i] for i in x]
    elif side!='P':raise ValueError('P/S transport')
    for i,j in enumerate(x):k[i+3]=j+3
    return tuple(k),tuple(q)

def transport_row(word,k):
    return sum(1<<(k[i+3]-3) for i in range(6) if word>>i&1)
