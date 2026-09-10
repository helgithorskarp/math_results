"""Whole H=2P3+2P2+3K1 exclusion with forced center roles."""
from forest_sat import build as base_build
from seven_edge_sat import lex_chain
from pysat.formula import IDPool
from two_p3_cases import PATTERNS,CASES,role_groups

def build(profile,index=0):
    if (profile,index) not in CASES:raise ValueError((profile,index))
    if profile not in (0,3):return base_build('6_2b',profile)
    cnf,E,nv=base_build('6_2b',profile,symmetry=False);pool=IDPool(start_from=nv+1)
    def edge(u,v):return E[tuple(sorted((u,v)))]
    center_six,center_seven,groups=role_groups(profile,index)
    for t,six,seven in zip((4,7),center_six,center_seven):
        for v in range(13,30):cnf.append([edge(v,t) if v in six else -edge(v,t)])
        for v in range(30,54):cnf.append([edge(v,t) if v==seven else -edge(v,t)])
    for group in groups:
        lex_chain(cnf,pool,[[edge(v,t) for t in range(13)] for v in group])
    # High automorphisms fixing both centers individually, compatible
    # with the fixed low-vertex roles and all center-membership cases.
    lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54)] for t in (0,1,2)])
    for C in ((3,4,5),(6,7,8),(9,10),(11,12)):
        lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C],[edge(v,t) for v in range(13,54) for t in C[::-1]]])
    lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C] for C in ((9,10),(11,12))])
    return cnf,E,pool.top
