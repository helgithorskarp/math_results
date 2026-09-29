#!/usr/bin/env python3
"""Definition-level integer audit. No imports from any research implementation."""
from collections import Counter
from itertools import combinations, product


def edge(g,u,v,cost):
    assert u != v and cost > 0
    g.setdefault(u,{})[v] = cost
    g.setdefault(v,{})[u] = cost


def floyd(g):
    vertices = sorted(g)
    ix = {v:i for i,v in enumerate(vertices)}
    n = len(vertices)
    d = [[10**12]*n for _ in vertices]
    for u in vertices:
        d[ix[u]][ix[u]] = 0
        for v,c in g[u].items(): d[ix[u]][ix[v]] = c
    for z in range(n):
        for x in range(n):
            row,via = d[x],d[x][z]
            for y in range(n):
                candidate = via+d[z][y]
                if candidate < row[y]: row[y] = candidate
    return {(u,v):d[ix[u]][ix[v]] for u in vertices for v in vertices}


def shortest(g,d,u,v):
    path = [u]
    while path[-1] != v:
        x = path[-1]
        path.append(min(y for y in g[x] if g[x][y]+d[y,v] == d[x,v]))
    return tuple(path)


def components(g,removed):
    remaining = set(g)-set(removed)
    answer = []
    while remaining:
        part = {remaining.pop()}
        todo = list(part)
        while todo:
            for y in g[todo.pop()]:
                if y in remaining:
                    remaining.remove(y);part.add(y);todo.append(y)
        answer.append(part)
    return answer


def build(word,uniform=False,control=False):
    k,m = word.count('D'),len(word)
    r = ('r',0)
    A,C = [('a',i) for i in range(k)],[('c',j) for j in range(m)]
    w = {}
    for i,a in enumerate(A):
        edge(w,r,a,4 if uniform else 4*(1+(3*i+m) % 7))
        edge(w,a,A[(i+1) % k],4 if uniform else 4*(1+(5*i+m) % 11))
    wd = floyd(w)
    parent=[];i=0
    for letter in word:
        parent.append(A[i % k]);i += int(letter == 'D')
    s = [4 if uniform else 4*(1+j % 3) for j in range(m)]
    g = {u:dict(row) for u,row in w.items()}
    arcs=[]
    for j,c in enumerate(C):
        edge(g,c,parent[j],s[j])
        b = max(4,wd[parent[j],parent[(j+1) % m]]+abs(s[j]-s[(j+1) % m]))
        prices = [b] if j % 3 == 0 else [3*b//4,b//2,3*b//4]
        if control: prices = [3,2,3] if j == 2 else [4]
        chain = [c]+[('v',j,t) for t in range(len(prices)-1)]+[C[(j+1) % m]]
        for u,v,price in zip(chain,chain[1:],prices): edge(g,u,v,price)
        arcs.append(tuple(chain))
    core=set(g)
    large=max(x for row in g.values() for x in row.values())
    for i,a in enumerate(A):
        for v in [r,a,A[(i+1) % k]]: edge(g,('k',i),v,large)
    return g,w,wd,A,C,arcs,parent,s,core


def check_path(g,d,path):
    assert path and len(path) == len(set(path))
    assert sum(g[u][v] for u,v in zip(path,path[1:])) == d[path[0],path[-1]]


def audit_model(word,uniform,totals,control=False):
    g,w,wd,original_A,original_C,original_arcs,parents,s,core = build(word,uniform,control)
    d = floyd(g)
    for j,c in enumerate(original_C):
        for x in w:
            assert d[c,x] == s[j]+wd[parents[j],x]
            totals['projection_distances'] += 1
    for x in w:
        for y in w: assert d[x,y] == wd[x,y]
    r=('r',0)
    k,m=len(original_A),len(original_C)
    for shift in range(m):
        rotated=word[shift:]+word[:shift]
        offset=word[:shift].count('D')
        A=original_A[offset:]+original_A[:offset]
        C=original_C[shift:]+original_C[:shift]
        arcs=original_arcs[shift:]+original_arcs[:shift]
        heights=s[shift:]+s[:shift]
        anchor={r,A[0],C[0]}
        represented=set(g)-anchor
        alpha=[set()]+[{a} for a in A[1:]]
        gamma=[set()]+[{c} for c in C[1:]]
        tau=[set(t[1:-1]) for t in arcs]
        sectors=[{('k',a[1])} for a in A]
        def side(i,j):
            return set().union(*(alpha[z]|sectors[z] for z in range(i)),
                               *(gamma[z]|tau[z] for z in range(j)))
        i=j=0
        for letter in rotated:
            ni=i+int(letter=='D');nj=j+1
            a,b=A[i % k],A[ni % k]
            L=side(i,j)
            R=represented-side(ni,nj)-alpha[ni % k]-gamma[nj % m]
            arc=arcs[j];x=[0]
            for u,v in zip(arc,arc[1:]):x.append(x[-1]+g[u][v])
            ell=x[-1]
            if letter=='D':
                ea=(C[0],)+shortest(w,wd,A[0],a)
                eb=(C[0],)+shortest(w,wd,A[0],b)
                delta=wd[a,b];change=heights[nj % m]-heights[j]
                threshold=ell+change+wd[r,b]-wd[r,a]
                suffix_cut=ell+change-delta if r in ea else threshold
                prefix_cut=ell+change+delta if r in eb else threshold
                q=next(z for z in range(len(x)) if 2*x[z]>=suffix_cut)
                p=max(z for z in range(len(x)) if 2*x[z]<=prefix_cut)
                suffix=((b,) if r in ea else shortest(w,wd,r,b))+arc[q:][::-1]
                prefix=((a,) if r in eb else shortest(w,wd,r,a))+arc[:p+1]
                pairs=[(ea,suffix),(eb,prefix)]
                heavy=[L|gamma[j]|set(arc[1:q]),R|gamma[nj % m]|set(arc[p+1:-1])]
                bounds=[(heavy[0],R),(L,heavy[1])]
                assert not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented
                assert q<=p+1
                totals['D_transitions']+=1
            else:
                threshold=ell+heights[nj % m]-heights[j]
                p=max(z for z in range(len(x)) if 2*x[z]<=threshold)
                q=next(z for z in range(len(x)) if 2*x[z]>=threshold)
                anchored=shortest(w,wd,r,A[0])+(C[0],)
                rooted=shortest(w,wd,r,a)
                pairs=[(anchored,rooted+arc[:p+1]),(anchored,rooted+arc[q:][::-1])]
                oldR=represented-L-alpha[i % k]-gamma[j]
                newL=side(ni,nj)
                bounds=[(L,oldR-set(arc[1:p+1])),(newL-set(arc[q:-1]),R)]
                assert not bounds[0][1]&bounds[1][0]
                totals['C_transitions']+=1
            for paths,regions in zip(pairs,bounds):
                for path in paths:check_path(g,d,path)
                removed=set().union(*map(set,paths))
                assert anchor<=removed
                for part in components(g,removed):
                    if part&core:assert any(part<=region for region in regions)
                    else:assert len(part)==1 and next(iter(part))[0]=='k'
                totals['component_pairs']+=1
            if control and shift==0 and j==2:
                masses={('a',1):2,('a',4):2,('k',2):1,arc[1]:1,arc[2]:1}
                mass=lambda S:sum(masses.get(v,0) for v in S)
                fixed=(r,A[0],C[0])
                old=[(r,a)+arc[:2],(r,b)+arc[2:][::-1],(a,b,arc[-1]),(b,a,arc[0])]
                old_residual=[]
                for path in old:
                    check_path(g,d,path)
                    old_residual.append(max(map(mass,components(g,set(fixed)|set(path)))))
                new_residual=[max(map(mass,components(g,set().union(*map(set,pair))))) for pair in pairs]
                assert old_residual==[4]*4 and new_residual==[2,2] and sum(masses.values())==7
                totals['old_candidate_failures']=4
                totals['control_total_mass']=7
                totals['control_new_residual']=2
            i,j=ni,nj
    totals['models']+=1


def scope_control(totals):
    g,w,wd,A,C,arcs,parents,s,core=build('DDDDD',True,True)
    r=('r',0)
    masses={A[1]:2,A[4]:2,('k',2):1,arcs[2][1]:1,arcs[2][2]:1}
    faces=[]
    for i,a in enumerate(A):
        b=A[(i+1)%5];v=('k',i)
        faces.extend([(r,a,v),(a,b,v),(b,r,v),(a,)+arcs[i]+(b,)])
    faces.append(tuple(v for arc in arcs for v in arc[:-1])[::-1])
    darts=[(u,v) for face in faces for u,v in zip(face,face[1:]+face[:1])]
    assert len(set(darts))==len(darts) and set(darts)=={(u,v) for u in g for v in g[u]}
    assert len(g)-len(darts)//2+len(faces)==2
    for u in g:
        successor={face[i-1]:face[(i+1)%len(face)] for face in faces for i,v in enumerate(face) if v==u}
        first=min(successor);seen=set();v=first
        while v not in seen:seen.add(v);v=successor[v]
        assert v==first and seen==set(g[u])
    minimum=min(max(sum(masses.get(v,0) for v in part) for part in components(g,face)) for face in faces)
    assert minimum==5
    totals['control_faces']=len(faces)
    totals['control_min_facial_residual']=minimum
    # Suppress degree-two arc interiors; embeddings correspond to this graph.
    suppressed={u:{v:cost for v,cost in row.items() if v[0]!='v'} for u,row in g.items() if u[0]!='v'}
    for i,c in enumerate(C):edge(suppressed,c,C[(i+1)%5],4)
    for size in range(3):
        for removed in combinations(suppressed,size):
            assert len(components(suppressed,removed))==1
            totals['control_connectivity_checks']+=1
    # The capped D^5 core is a minor after removing K's and suppressing arcs.
    minor={u:set(v for v in row if v[0]!='k') for u,row in suppressed.items() if u[0]!='k'}
    def width_three(adj):
        if not adj:return True
        for v in adj:
            neighbors=adj[v]
            if len(neighbors)>3:continue
            nxt={u:set(row)-{v} for u,row in adj.items() if u!=v}
            for u in neighbors:nxt[u]|=neighbors-{u}
            if width_three(nxt):return True
        return False
    assert not width_three(minor)
    totals['control_treewidth_lower_bound']=4


def main():
    totals=Counter()
    for n in range(3,8):
        for letters in product('CD',repeat=n):
            word=''.join(letters)
            if word.count('D')>=3:audit_model(word,False,totals)
    audit_model('DDDDD',True,totals,True)
    scope_control(totals)
    # Violating the arc condition can invalidate the prescribed cross metric.
    g,w,wd,A,C,arcs,parents,s,core=build('DDD',True)
    u,v=arcs[0]
    g[u][v]=g[v][u]=1
    d=floyd(g)
    assert d[C[0],A[1]]<s[0]+wd[A[0],A[1]]
    totals['projection_failure_control']=1
    print(' '.join(f'{k}={v}' for k,v in sorted(totals.items()))+' PASS')


if __name__=='__main__':main()
