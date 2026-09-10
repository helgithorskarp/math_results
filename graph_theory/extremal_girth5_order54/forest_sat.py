"""Full forest cases, partitioned only by forced degree/high-count profiles."""
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from forest_profiles import profiles
FORESTS={'5_0':[2]*5,'5_1':[3,2,2,2],'5_2a':[4,2,2],'5_2b':[3,3,2],
 '5_3a':[5,2],'5_3b':[4,3],'6_0':[2]*6,'6_1':[3,2,2,2,2],
 '6_2a':[4,2,2,2],'6_2b':[3,3,2,2]}
EXCLUDED=('5_3a','5_3b','6_2a')
from seven_edge_sat import lex_chain

def build(name,index,symmetry=True):
    lengths=FORESTS[name];m=sum(x-1 for x in lengths);k=sum(x-2 for x in lengths)
    a,b=profiles(m,k)[index];ds=[8]*13+[6]*17+[7]*24
    H=set();components=[];nextv=13-sum(lengths);isolated=list(range(nextv))
    for length in lengths:
        C=list(range(nextv,nextv+length));nextv+=length;components.append(C);H.update(zip(C,C[1:]))
    hd=[sum(v in e for e in H) for v in range(13)]
    cs=hd+[c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)]
    pool=IDPool();cnf=CNF();low=list(range(13,54))
    E={uv:pool.id(('e',*uv)) for uv in combinations(range(54),2) if uv[1]>=13 or uv in H}
    def edge(u,v):return E.get(tuple(sorted((u,v))))
    def card(lits,bound,mode='eq'):
        if bound<0 or (mode=='eq' and bound>len(lits)):cnf.append([])
        elif mode=='le' and bound>=len(lits):pass
        elif lits:
            f=CardEnc.equals if mode=='eq' else CardEnc.atmost
            cnf.extend(f(lits,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
    for uv in H:cnf.append([E[uv]])
    for v,d in enumerate(ds):
        card([edge(v,u) for u in range(54) if u!=v and edge(v,u)],d)
        card([edge(v,u) for u in range(13) if u!=v and edge(v,u)],cs[v])
        if v<13:
            card([edge(v,u) for u in range(13,30)],3+hd[v])
            card([edge(v,u) for u in range(30,54)],5-2*hd[v])
        terms=[]
        bound=12-sum(hd[u] for u in range(13) if edge(v,u)) if v<13 else 13-d
        for u in low:
            if u==v:continue
            coeff=cs[u]-1
            if coeff<0:terms.extend([-edge(v,u)]*(-coeff));bound-=coeff
            else:terms.extend([edge(v,u)]*coeff)
        if v>=13:
            for t in range(13):terms.extend([edge(v,t)]*hd[t])
        card(terms,bound)
    for u,v in combinations(range(54),2):
        short=[]
        if edge(u,v):short.append(edge(u,v))
        for w in range(54):
            if w in (u,v):continue
            a,b=edge(u,w),edge(v,w)
            if a and b:
                p=pool.id();short.append(p);cnf.extend([[-p,a],[-p,b],[-a,-b,p]])
        card(short,1,'le')
        if u<13 or v<13:cnf.append(short)
    if symmetry:
        for d,c in sorted(set(zip(ds[13:],cs[13:]))):
            group=[v for v in low if ds[v]==d and cs[v]==c]
            lex_chain(cnf,pool,[[edge(v,t) for t in range(13)] for v in group])
        lex_chain(cnf,pool,[[edge(t,v) for v in low] for t in isolated])
        for comp in components:
            lex_chain(cnf,pool,[[edge(t,v) for v in low for t in comp],[edge(t,v) for v in low for t in comp[::-1]]])
        for length in sorted(set(lengths)):
            comps=[c for c in components if len(c)==length]
            lex_chain(cnf,pool,[[edge(t,v) for v in low for t in comp] for comp in comps])
    return cnf,E,pool.top
