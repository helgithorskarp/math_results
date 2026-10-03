"""Old-label set model. SY Q ranks are proved two; T excesses are inputs."""
from itertools import combinations, product

OLD=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
OLD_MAP=(2,1,3,4,5,6,7,8,9,10)
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
P,S,H,K,C,L=13,50,43,23,3,60
LABELS=('u','v','a',*(f'X{i}' for i in range(6)),'SX0','SX1','SY0','SY1','T0','T1','T2')

def build(r,rows,sy,excess=(0,0,0),old_map=OLD_MAP):
    if r not in (0,1) or len(rows)!=3 or len(sy)!=2 or tuple(old_map)!=OLD_MAP:
        raise ValueError('actual r and literal old-label bridge')
    if any(not isinstance(w,int) or not 0<=w<64 for w in (*rows,*sy)):
        raise ValueError('six-bit endpoint rows')
    if len(excess)!=3 or any(e<0 or not isinstance(e,int) for e in excess):
        raise ValueError('nonnegative integer T excesses')
    red=[set() for _ in range(16)]
    def edge(i,j):red[i].add(j);red[j].add(i)
    for i,row in enumerate(OLD):
        edge(0,old_map[i])
        for j in row:
            if i<j:edge(old_map[i],old_map[j])
    for j in (11,12):edge(1,j)
    for j in range(11,16):edge(2,j)
    for z,row in zip((9,10),((14,15),(13,15)) if r==0 else ((13,15),(14,15))):
        for t in row:edge(z,t)
    for z,row in ((11,(14,15)),(12,(13,14))):
        for t in row:edge(z,t)
    for z,w in zip(range(11,16),(*sy,*rows)):
        for i in range(6):
            if w>>i&1:edge(z,3+i)
    d=[10,10,9]+[10]*8
    q=[d[i]-len(red[i]) for i in range(11)]+[2,2]+[3+excess[0],2+excess[1],3+excess[2]]
    d += [len(red[i])+q[i] for i in range(11,16)]
    if any(not 0<=a<=6 for a in q):raise ValueError('Q rank outside six-point domain')
    return red,tuple(d),tuple(q)

def allowances(red,d):
    out={};known=set(range(16))
    for i,j in combinations(range(16),2):
        if j in red[i]:a=3-len(red[i]&red[j])
        else:
            blue=len((known-red[i]-{i})&(known-red[j]-{j}))
            a=(d[i]-len(red[i]))+(d[j]-len(red[j]))-blue
        out[i,j]=out[j,i]=a
    return out

def column_domains(red,d,q,case):
    """Necessary incidence columns; includes variable actual Q degrees."""
    a=allowances(red,d); answer=[]
    for z in range(6):
        role={11+k for k,row in enumerate(case['SYQ']) if z in row}
        role|={13+k for k,row in enumerate(case['TQ']) if z in row}
        h=case['h'][z]; found=[]
        for w in range(64):
            if any(w>>i&1 and w>>j&1 for i,j in CYCLE):continue
            for p0,p1 in product((0,1),repeat=2):
                n={1}|role|{3+i for i in range(6) if not (w>>i&1)}
                n|={9+i for i,p in enumerate((p0,p1)) if p}
                D=len(n)+h
                for i,j in combinations(range(16),2):
                    bi,bj=int(i in n),int(j in n)
                    lower=bi*bj+max(0,q[i]-bi+q[j]-bj-5)
                    if lower>a[i,j]:break
                else:
                    for i in range(16):
                        edge=i in n
                        lower=max(0,q[i]+h-(6 if edge else 5))
                        cap=3 if edge else d[i]+D-14
                        if len(red[i]&n)+lower>cap:break
                    else:found.append([w,p0,p1,D])
        answer.append(found)
    return answer

def prefix(red,case,choice):
    graph=[set(a) for a in red]+[set() for _ in range(6)]
    for z,(w,p0,p1,D) in enumerate(choice):
        n={1}|{3+i for i in range(6) if not (w>>i&1)}
        n|={9+i for i,p in enumerate((p0,p1)) if p}
        n|={11+k for k,row in enumerate(case['SYQ']) if z in row}
        n|={13+k for k,row in enumerate(case['TQ']) if z in row}
        for i in n:graph[i].add(16+z);graph[16+z].add(i)
    return graph

def known_spines(graph):
    bad=[]; records=[]
    for i,j in combinations(range(16),2):
        edge=j in graph[i]
        pages=sorted(graph[i]&graph[j]) if edge else [k for k in range(22) if k not in (i,j) and k not in graph[i] and k not in graph[j]]
        records.append([i,j,int(edge),pages])
        if len(pages)>(3 if edge else 6):bad.append(records[-1])
    return records,bad
