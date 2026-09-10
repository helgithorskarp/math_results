"""Complete full-incidence formula after common-star normalization."""
from shared_center_cases import roles
from shared_star_cases import star_roles
from forest_sat import build as base_build
from seven_edge_sat import lex_chain
from pysat.formula import IDPool
from itertools import combinations

def build(profile,index,star_index,symmetry=True):
    cnf,E,nv=base_build('5_2b',profile,symmetry=False);pool=IDPool(start_from=nv+1)
    six,seven,common,old_groups=roles(profile,index);high,blocks,groups,iso_groups=star_roles(profile,index,star_index)
    def edge(u,v):return E[tuple(sorted((u,v)))]
    for t,S,v7 in zip((6,9),six,seven):
        I=set(S)|{v7}
        for v in range(13,54):cnf.append([edge(v,t) if v in I else -edge(v,t)])
        for u,v in combinations(sorted(I),2):cnf.append([-edge(u,v)])
    for t in range(13):cnf.append([edge(common,t) if t in high else -edge(common,t)])
    low={v for v,H in blocks}
    for v in range(13,54):
        if v!=common:cnf.append([edge(common,v) if v in low else -edge(common,v)])
    for v,H in blocks:
        for t in range(13):cnf.append([edge(v,t) if t in H else -edge(v,t)])
    if not symmetry:return cnf,E,pool.top
    for G in groups:lex_chain(cnf,pool,[[edge(v,t) for t in range(13)] for v in G])
    for G in iso_groups:lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54)] for t in G])
    for C in ((5,7),(8,10)):
        lex_chain(cnf,pool,[[edge(v,t) for v in range(13,54) for t in C],[edge(v,t) for v in range(13,54) for t in C[::-1]]])
    return cnf,E,pool.top
