"""Constructive three-list colouring for the proved terminal auxiliary graphs."""
from itertools import combinations,permutations

def require(test,message):
    if not test: raise ValueError(message)

def graph(n,edges):
    a=[set() for _ in range(n)]
    for u,v in edges:
        require(type(u) is int and type(v) is int and 0<=u<n and 0<=v<n and u!=v,'invalid edge')
        a[u].add(v);a[v].add(u)
    return a

def canonical(word):
    names={};out=[]
    for x in word:
        if x not in names:names[x]=len(names)
        out.append(names[x])
    inverse=[x for x,c in sorted(names.items(),key=lambda z:z[1])]
    inverse += [x for x in range(4) if x not in names]
    return tuple(out),inverse

def colour(n,edges,forbidden):
    """forbidden[v] is one excluded palette colour; returns a proper assignment.

    Geometric hypotheses are not inferred here. The supplied graph must have
    maximum degree three and cubic components of type K3,3 or triangular prism.
    Other inputs fail loudly rather than pretending the theorem covers them.
    """
    require(len(forbidden)==n and all(type(c) is int and c in range(4) for c in forbidden),'invalid lists')
    a=graph(n,edges);require(all(len(s)<=3 for s in a),'degree exceeds three')
    result={};left=set(range(n))
    while left:
        seed=min(left);comp={seed};todo=[seed]
        for u in todo:
            for v in sorted(a[u]-comp):comp.add(v);todo.append(v)
        left-=comp
        roots=[v for v in comp if len(a[v])<3]
        if roots:
            root=min(roots);order=[root];seen={root}
            for u in order:
                for v in sorted(a[u]-seen):seen.add(v);order.append(v)
            for v in reversed(order):
                allowed=set(range(4))-{forbidden[v]}-{result[u] for u in a[v] if u in result}
                require(bool(allowed),'greedy list failure');result[v]=min(allowed)
            continue
        require(len(comp)==6,'uncovered cubic component')
        tri=next((t for t in combinations(sorted(comp),3)
                  if all(v in a[u] for u,v in combinations(t,2))),None)
        if tri is None:
            parts={seed:0};order=[seed]
            for u in order:
                for v in sorted(a[u]):
                    if v not in parts:parts[v]=1-parts[u];order.append(v)
                    require(parts[v]!=parts[u],'not bipartite')
            x=sorted(v for v in comp if parts[v]==0);y=sorted(comp-set(x))
            require(len(x)==len(y)==3 and all(a[v]==set(y) for v in x),'not K3,3')
            common=set(range(4))-{forbidden[v] for v in x};require(bool(common),'empty common colour')
            c=min(common)
            for v in x:result[v]=c
            for v in y:result[v]=min(set(range(4))-{forbidden[v],c})
        else:
            x=list(tri);y=[]
            for v in x:
                outside=a[v]-set(x);require(len(outside)==1,'not a prism');y.append(next(iter(outside)))
            require(set(y)==comp-set(x) and all(y[j] in a[y[i]] for i in range(3) for j in range(i)),'not a prism')
            used=set()
            for v in x:
                result[v]=min(set(range(4))-{forbidden[v]}-used);used.add(result[v])
            match=next((cs for cs in permutations(range(4),3)
                        if all(c!=forbidden[v] and c!=result[x[i]] for i,(v,c) in enumerate(zip(y,cs)))),None)
            require(match is not None,'prism matching failure')
            for v,c in zip(y,match):result[v]=c
    out=[result[v] for v in range(n)]
    require(all(out[u]!=out[v] for u,v in edges) and all(c!=f for c,f in zip(out,forbidden)),'invalid colouring')
    return out

K33=[(i,j) for i in range(3) for j in range(3,6)]
PRISM=[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)]
GRAPHS={'K33':K33,'prism':PRISM}
