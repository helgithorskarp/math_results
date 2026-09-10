"""All incidence cases with joint roles at the two nonadjacent centers."""
from shared_center_cases import cases,roles,CASES
from forest_sat import build as base_build
from seven_edge_sat import lex_chain
from pysat.formula import IDPool
from itertools import combinations

def build(profile,index):
    if (profile,index) not in CASES:raise ValueError((profile,index))
    cnf,E,nv=base_build('5_2b',profile,symmetry=False);pool=IDPool(start_from=nv+1)
    six,seven,common,groups=roles(profile,index)
    def edge(u,v):return E[tuple(sorted((u,v)))]
    for t,S,v7 in zip((6,9),six,seven):
        group=set(S)|{v7}
        for v in range(13,54):cnf.append([edge(v,t) if v in group else -edge(v,t)])
        for u,v in combinations(sorted(group),2):cnf.append([-edge(u,v)])
    for group in groups:lex_chain(cnf,pool,[[edge(v,t) for t in range(13)] for v in group])
    lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54)] for t in range(5)])
    for C in ((5,7),(8,10),(11,12)):
        lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C],[edge(v,t) for v in range(13,54) for t in C[::-1]]])
    return cnf,E,pool.top
