"""Literal old-label graphs and physical colored-spine counts."""
from itertools import combinations

OLD=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
OLD_MAP=(2,1,3,4,5,6,7,8,9,10)
LABELS=('u','v','a',*(f'X{i}' for i in range(6)),'SX0','SX1','SY0','SY1','T0','T1','T2')
FORCED_Q={0:frozenset(),1:frozenset(range(6)),2:frozenset(),
          4:frozenset((0,1,4,5)),5:frozenset((0,2,3)),6:frozenset((1,2,3)),
          9:frozenset((0,3,4,5)),10:frozenset((1,3,4,5)),15:frozenset((0,1,2))}

def build(r,rows,sy,old_map=OLD_MAP):
    if r not in (0,1) or len(rows)!=3 or len(sy)!=2:
        raise ValueError('two actual r labels, three T/two SY rows')
    if any(not isinstance(w,int) or not 0<=w<64 for w in (*rows,*sy)):
        raise ValueError('six-bit row domain')
    if tuple(old_map)!=OLD_MAP:
        raise ValueError('literal old-label/coordinate bridge changed')
    red=[set() for _ in range(16)]
    def edge(i,j):red[i].add(j);red[j].add(i)
    for i in range(10):
        edge(0,old_map[i])
        for j in OLD[i]:
            if i<j:edge(old_map[i],old_map[j])
    if sum(len(red[i]&set(range(1,11))) for i in range(1,11))!=26:
        raise ValueError('thirteen literal neighborhood edges')
    for j in (11,12):edge(1,j)
    for j in range(11,16):edge(2,j)
    sx=((14,15),(13,15)) if r==0 else ((13,15),(14,15))
    for i,row in zip((9,10),sx):
        for j in row:edge(i,j)
    for i,row in ((11,(14,15)),(12,(13,14))):
        for j in row:edge(i,j)
    for z,w in zip((11,12,13,14,15),(*sy,*rows)):
        for i in range(6):
            if w>>i&1:edge(z,3+i)
    degrees=[10,10,9]+[10]*8
    qr=[degrees[i]-len(red[i]) for i in range(11)]
    outside_known=set(range(11,16))
    for i in range(11,16):
        qi=4-len(red[i]&outside_known)
        qr.append(qi);degrees.append(len(red[i])+qi)
    if any(not 0<=q<=6 for q in qr):raise ValueError('outside rank outside six-point Q')
    return tuple(frozenset(s) for s in red),tuple(degrees),tuple(qr)

def pair_failures(red,degrees,qr):
    failures=[];K=frozenset(range(16))
    for i,j in combinations(range(16),2):
        if j in red[i]:
            physical=len(red[i]&red[j]);outside=max(0,qr[i]+qr[j]-6);cap=3
        else:
            physical=len((K-red[i]-{i})&(K-red[j]-{j}))
            outside=max(0,6-qr[i]-qr[j]);cap=6
        if physical+outside>cap:failures.append((i,j,physical,outside,cap))
    return failures

def row_options(red,degrees,qr,i):
    """All six-point rows of the prescribed rank satisfying forced-row spines."""
    options=[]
    for word in range(64):
        if word.bit_count()!=qr[i]:continue
        row=frozenset(j for j in range(6) if word>>j&1)
        if all(len(red[i]&red[j])+len(row&F)<=(3 if j in red[i] else degrees[i]+degrees[j]-14)
               for j,F in FORCED_Q.items()):options.append(word)
    return options

def check_q_point(red,degrees,qr,q,known_neighbors,internal,forced):
    """Physical common pages for one Q point; exact known Q rows, minima otherwise."""
    if q in internal or any(not 0<=z<6 for z in internal):
        raise ValueError('Q graph is simple and has six labeled points')
    h=len(internal);dq=len(known_neighbors)+h
    for i in range(16):
        physical=len(red[i]&known_neighbors)
        additional=(len(forced[i]&internal) if i in forced else
                    max(0,qr[i]+h-(6 if i in known_neighbors else 5)))
        cap=3 if i in known_neighbors else degrees[i]+dq-14
        if physical+additional>cap:return False
    return True
