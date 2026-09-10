"""All graph incidences in the complete P4 high-forest case cover."""
from p4_cases import cases,roles,endpoint_roles,CASES
from forest_sat import build as base_build
from seven_edge_sat import lex_chain
from pysat.formula import IDPool
from itertools import combinations

def build(profile,index,end_case=-1):
    if (profile,index,end_case) not in CASES:raise ValueError((profile,index,end_case))
    cnf,E,nv=base_build('5_2a',profile,symmetry=False);pool=IDPool(start_from=nv+1)
    six,seven,groups=roles(profile,index)
    def edge(u,v):return E[tuple(sorted((u,v)))]
    I=[]
    for t,S,v7 in zip((6,7),six,seven):
        group=set(S)|{v7};I.extend(sorted(group))
        for v in range(13,54):cnf.append([edge(v,t) if v in group else -edge(v,t)])
    for u,v in combinations(I,2):cnf.append([-edge(u,v)])
    if profile==1:
        endpoint6,endpoint7,groups=endpoint_roles(end_case)
        for t,S,T in zip((5,8),endpoint6,endpoint7):
            wanted=S|T
            for v in range(13,54):cnf.append([edge(v,t) if v in wanted else -edge(v,t)])
    for group in groups:lex_chain(cnf,pool,[[edge(v,t) for t in range(13)] for v in group])
    lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54)] for t in range(5)])
    for C in ((9,10),(11,12)):
        lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C],[edge(v,t) for v in range(13,54) for t in C[::-1]]])
    lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C] for C in ((9,10),(11,12))])
    return cnf,E,pool.top
