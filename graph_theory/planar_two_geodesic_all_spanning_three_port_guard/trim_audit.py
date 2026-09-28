def template(m,missing,case):
    tail=list(range(5,m))
    if missing==1:
        if case=='A':return ([m,0,1],[2,3,4]+tail)
        return ([2,3,1,0,m],[4]+tail)
    if missing==2:
        if case=='A':return ([m,0,1,2],[3,4]+tail)
        return ([m,0]+list(range(m-1,4,-1)),[2,1,3,4])
    if missing==3:return ([m,0,1,2,3],[4]+tail)
    if missing==4:return ([m,0,1,2,3,4],tail)
    raise ValueError(missing)

def components(m,mask):
    g=[set() for _ in range(m+1)]
    for i in range(m):
        if mask>>i&1:
            u,v=i,(i+1)%m;g[u].add(v);g[v].add(u)
    if mask>>m&1:g[0].add(m);g[m].add(0)
    unseen=set(range(m+1));out=[]
    while unseen:
        u=unseen.pop();part={u};todo=[u]
        while todo:
            u=todo.pop()
            for v in g[u]&unseen:
                unseen.remove(v);part.add(v);todo.append(v)
        out.append(part)
    return out,g

def check_path(path,part,g,allow_ear):
    pos=[i for i,v in enumerate(path) if v in part]
    if not pos:return 0
    segment=path[min(pos):max(pos)+1]
    assert segment[0] in part and segment[-1] in part
    for u,v in zip(segment,segment[1:]):
        assert v in g[u] or allow_ear and {u,v}=={1,3},(path,part,segment,u,v)
    return len(part.intersection(segment))

for m in range(12,16):
    count=0;special=0
    for mask in range(1<<(m+1)):
        if all(mask>>e&1 for e in (1,2,3,4)):continue
        missing=next(e for e in (3,4,1,2) if not(mask>>e&1))
        comps,g=components(m,mask)
        for case in ('A','B'):
            if missing==1 and case=='B' and not (mask&1):
                special+=1
                U=[2,3,4]+list(range(5,m))+[0,m]
                for D in comps:
                    if D=={1}:continue
                    assert check_path(U,D,g,False)==len(D)
                continue
            paths=template(m,missing,case)
            assert set(paths[0]).isdisjoint(paths[1])
            assert set(paths[0])|set(paths[1])==set(range(m+1))
            for D in comps:
                assert sum(check_path(p,D,g,case=='B' and missing in (1,2)) for p in paths)==len(D)
            count+=1
    print('m',m,'template_states',count,'special_states',special,'PASS')
