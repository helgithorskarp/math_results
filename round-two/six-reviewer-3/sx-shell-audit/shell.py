"""Fresh labelled-set interpretation of the full original 22-point shell."""
from itertools import combinations

V=('u','v','a',*(f'X{i}' for i in range(6)),'SX0','SX1','SY0','SY1','T0','T1','T2',*(f'Q{i}' for i in range(6)))
X=tuple(f'X{i}' for i in range(6));Q=tuple(f'Q{i}' for i in range(6));D=('SY0','SY1','T0','T1','T2')
MIXED=((0,4),(0,5),(1,2),(1,3))

def need(ok,message):
    if not ok:raise ValueError(message)

def pair(a,b):
    need(a!=b,'simple graph has no loop');return tuple(sorted((a,b)))

def specification():
    need(len(V)==22 and len(set(V))==22,'distinct original22 labels')
    free={pair(a,b) for a in X for b in D}
    free|={pair(a,b) for a in (*X,'SX0','SX1','SY0','SY1','T0','T1','T2') for b in Q}
    free|={pair(a,b) for a,b in combinations(Q,2)}
    red=set()
    def edge(a,b):red.add(pair(a,b))
    for a in ('v','a',*X,'SX0','SX1'):edge('u',a)
    for a in ('v','SX0','SX1','SY0','SY1','T0','T1','T2'):edge('a',a)
    for a in ('SY0','SY1',*Q):edge('v',a)
    cycle=(0,4,3,1,2,5)
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):edge(X[a],X[b])
    for a in ('X3','X5','T1','T2'):edge('SX0',a)
    for a in ('X2','X4','T1','T2'):edge('SX1',a)
    for a in ('T0','T2'):edge('SY0',a)
    for a in ('T0','T1'):edge('SY1',a)
    need(not(red&free),'fixed/free domains disjoint')
    return {pair(a,b):None if pair(a,b) in free else int(pair(a,b) in red) for a,b in combinations(V,2)}

def rows(spec):
    red={v:set() for v in V};blue={v:set() for v in V}
    need(set(spec)=={pair(a,b) for a,b in combinations(V,2)},'whole original pair domain')
    for (a,b),value in spec.items():
        need(value in (0,1,None),'three-state color')
        if value is not None:
            table=red if value==1 else blue;table[a].add(b);table[b].add(a)
    return red,blue

def members(mask,universe):return {v for i,v in enumerate(universe) if mask>>i&1}

def assign(spec,label,universe,mask):
    out=dict(spec)
    for i,v in enumerate(universe):
        p=pair(label,v);value=(mask>>i)&1
        need(out[p] is None or out[p]==value,'free assignment cannot change fixed color')
        out[p]=value
    return out

def cover(row):return all((row>>a&1) or(row>>b&1) for a,b in MIXED)
def independent(row):return all(not((row>>a&1) and(row>>b&1)) for a,b in MIXED)

def witness(spec,a,b,color,pages):
    need(spec[pair(a,b)]==color,'actual witness spine color')
    red,blue=rows(spec);actual=sorted((red if color else blue)[a]&(red if color else blue)[b])
    need(sorted(pages)==actual,'whole literal witness page list')
    need(len(pages)==len(set(pages)) and a not in pages and b not in pages,'distinct nonendpoint pages')
    return actual
