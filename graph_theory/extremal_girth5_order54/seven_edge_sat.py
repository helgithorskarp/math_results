"""Whole e(G[V8])=7 subclass for n=54,m=187,girth>=5."""
from itertools import combinations, permutations, product
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType

def lex_chain(cnf,pool,rows):
    """Constrain consecutive Boolean rows in increasing lexicographic order."""
    for left,right in zip(rows,rows[1:]):
        prefix=None
        for x,y in zip(left,right):
            cnf.append(([-prefix] if prefix else [])+[-x,y])
            z=pool.id()
            if prefix:cnf.append([-z,prefix])
            cnf.extend([[-z,-x,y],[-z,x,-y]])
            cnf.append(([-prefix] if prefix else [])+[x,y,z])
            cnf.append(([-prefix] if prefix else [])+[-x,-y,z])
            prefix=z

def motifs(matching):
    cycles=[[0,1,2,3,4]] if matching=='10' else [[0,1],[2,3,4]]
    M={tuple(sorted((2*i,2*i+1))) for i in range(5)}
    K={tuple(sorted((2*i+1,2*j))) for cyc in cycles for i,j in zip(cyc,cyc[1:]+cyc[:1])}
    autos=[]
    for perm in permutations(range(5)):
        for flips in product((0,1),repeat=5):
            p=[2*perm[i]+(b^flips[i]) for i in range(5) for b in range(2)]
            if {tuple(sorted((p[u],p[v]))) for u,v in K}==K:autos.append(p)
    valid=[]
    for I in combinations(range(10),3):
        if any(e in M|K for e in combinations(I,2)):continue
        R=set(range(10))-set(I)-{x^1 for x in I}
        for X in combinations(sorted(R),2):
            Y=tuple(sorted(R-set(X)))
            if tuple(X) in M|K or Y in M|K:continue
            motif=(I,X,Y)
            orbit=[tuple(tuple(sorted(p[x] for x in s)) for s in motif) for p in autos]
            if motif==min(orbit):valid.append(motif)
    return valid

def build(quad_pattern, matching, motif):
    assert quad_pattern in ((1,1),(1,2))
    assert matching in ("10","46")
    assert 0 <= motif < len(motifs(matching))
    ds=[8]*13+[6]*17+[7]*24
    cs=[2]+[1]*12+[3]*15+[4]*2+[1]*11+[2]*13
    high=set(range(13)); low=list(range(13,54))
    fixed={(0,1),(0,2)}|{(i,i+1) for i in range(3,13,2)}
    pool=IDPool();cnf=CNF()
    E={uv:pool.id(('e',*uv)) for uv in combinations(range(54),2) if not set(uv)<=high or uv in fixed}
    def edge(u,v):return E.get(tuple(sorted((u,v))))
    def card(lits,k,mode='eq',guard=None):
        if k<0 or (mode=='eq' and k>len(lits)):clauses=[[]]
        elif mode=='le' and k>=len(lits):clauses=[]
        elif not lits:clauses=[]
        else:
            f=CardEnc.equals if mode=='eq' else CardEnc.atmost
            clauses=f(lits,bound=k,vpool=pool,encoding=EncType.seqcounter).clauses
        for c in clauses:cnf.append(([-guard] if guard else [])+c)
    for uv in fixed:cnf.append([E[uv]])
    for v,d in enumerate(ds):
        card([edge(v,u) for u in range(54) if u!=v and edge(v,u)],d)
        card([edge(v,u) for u in high if u!=v and edge(v,u)],cs[v])
        if v in high:
            card([edge(v,u) for u in range(13,30)],3+cs[v])
            card([edge(v,u) for u in range(30,54)],5-2*cs[v])
            # Pointwise pair coverage by the thirteen high vertices.
            if v==0:
                for u in [28,29]+list(range(41,54)):cnf.append([-edge(v,u)])
            else:
                card([edge(v,u) for u in [28,29]+list(range(41,54))],2 if v in (1,2) else 3)
        else:
            terms=[]
            for u in low:
                if u==v:continue
                terms.extend([edge(v,u)]*(cs[u]-1))
            terms.append(edge(v,0))
            card(terms,13-d-cs[v])
    cnf.append([-edge(28,29)])
    for v in (28,29):
        card([edge(v,u) for u in range(13,28)],1)
        card([edge(v,u) for u in range(41,54)],1)
    for u,v in combinations(low,2):
        for t,s in fixed:
            cnf.extend([[-edge(u,v),-edge(u,t),-edge(v,s)],[-edge(u,v),-edge(u,s),-edge(v,t)]])
    for u,v in combinations(range(54),2):
        short=[]
        if edge(u,v):short.append(edge(u,v))
        for k in range(54):
            if k in (u,v):continue
            a,b=edge(u,k),edge(v,k)
            if not a or not b:continue
            p=pool.id(('p',u,v,k));short.append(p)
            cnf.extend([[-p,a],[-p,b],[-a,-b,p]])
        card(short,1,'le')
        if u in high or v in high:cnf.append(short)
    # Quadruple high-neighborhoods must meet the unique P3 component.
    # Optional case split specifies center/leaf membership of both quadruples.
    for v in (28,29):cnf.append([edge(v,t) for t in range(3)])
    if quad_pattern:
        for v,t in zip((28,29),quad_pattern):cnf.append([edge(v,t)])
        for v,u,t in zip((28,29),(18,19),quad_pattern):
            cnf.append([edge(v,u)]);cnf.append([edge(u,3-t)])
        for v,u in ((28,41),(29,42)):cnf.append([edge(v,u)])
    if matching:
        cycles=[[0,1,2,3,4]] if matching=='10' else [[0,1],[2,3,4]]
        pairs=[]
        for cyc in cycles:
            pairs.extend((4+2*i,3+2*j) for i,j in zip(cyc,cyc[1:]+cyc[:1]))
        for v,(u,w) in zip(range(13,18),pairs):
            for t in high:cnf.append([edge(v,t) if t in (0,u,w) else -edge(v,t)])
        for t in high:cnf.append([edge(30,t) if t==0 else -edge(30,t)])
        for u in (41,42):cnf.append([edge(30,u)])
    if motif is not None:
        I,X,Y=motifs(matching)[motif]
        for v,S in ((28,{1}|{3+x for x in I}),(18,{2}|{3+x for x in X}),(41,{3+x for x in Y})):
            for t in high:cnf.append([edge(v,t) if t in S else -edge(v,t)])
    # Only permutations within these still indistinguishable vertex groups.
    for group in (range(20,28),range(31,41),range(43,54)):
        lex_chain(cnf,pool,[[edge(u,t) for t in high] for u in group])
    return cnf,E,pool.top
