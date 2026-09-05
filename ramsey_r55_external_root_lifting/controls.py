"""Literal controls for the external-root lifting lemma."""
from itertools import combinations,product
from literal_model import require,ramsey


def graph(n,mask):
    E=[set() for _ in range(n)]
    for k,(a,b) in enumerate(combinations(range(n),2)):
        if mask>>k&1:E[a].add(b);E[b].add(a)
    return E


def ramsey55(G):
    return all(len({b in G[a] for a,b in combinations(S,2)})>1 for S in combinations(range(len(G)),5))


def test_lifting(G,E):
    count=0
    for word in product(range(3),repeat=len(E)):
        A={v for v,c in zip(E,word) if c==1};B={v for v,c in zip(E,word) if c==2}
        if not A|B:continue
        if any(b not in G[a] for a,b in combinations(A,2)):continue
        if any(b in G[a] for a,b in combinations(B,2)):continue
        S={v for v in range(len(G)) if v not in A|B and A<=G[v]
           and all(b not in G[v] for b in B)}
        for u in set(range(len(G)))-set(E):
            if A<=G[u]:
                require(len(G[u]&S)<=ramsey(4-len(A),5-len(B))-1,'red lifted bound')
                count+=1
            if not B&G[u]:
                require(len(S-G[u]-{u})<=ramsey(5-len(A),4-len(B))-1,'blue lifted bound')
                count+=1
    return count


def run():
    cases=0
    for mask in range(1024):
        G=graph(5,mask)
        if ramsey55(G):cases+=test_lifting(G,(0,1,2))
    # Eight-vertex triangle-free side with alpha<4, joined to external roots.
    H=graph(8,5388912);G=[set(s) for s in H]+[set(),set(),set()]
    for u in (8,9):
        for v in range(8):G[u].add(v);G[v].add(u)
    for a,b in ((8,9),(9,10)):G[a].add(b);G[b].add(a)
    require(ramsey55(G),'literal eleven-vertex fixture')
    S=G[8]-G[10]-{10}
    require(S==set(range(8)) and 9 not in S and 8 in G[9] and len(G[9]&S)==8,
            'external, not internal, vertex attains lifted cap eight')
    negatives=0
    for mask in (0,1023):
        try:test_lifting(graph(5,mask),(0,1,2))
        except ValueError:negatives+=1
        else:raise ValueError('missing Ramsey hypothesis not detected')
    return {'small_lifted_inequalities':cases,'sharp_external_vertex_order':11,
            'sharp_external_degree_into_side':8,'non_Ramsey_controls_rejected':negatives}
