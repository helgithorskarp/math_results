"""Author binary-multiset and red-neighborhood audit; six-books-3, researcher."""
from fractions import Fraction
from itertools import combinations,combinations_with_replacement


def need(ok,message):
    if not ok:raise RuntimeError(message)


def row_rank(rows):
    m=[[Fraction(int(i in row)) for i in range(10)] for row in rows];rank=0
    for column in range(10):
        pivot=next((j for j in range(rank,len(m)) if m[j][column]),None)
        if pivot is None:continue
        m[rank],m[pivot]=m[pivot],m[rank];p=m[rank][column]
        m[rank]=[x/p for x in m[rank]]
        for j in range(rank+1,len(m)):
            if m[j][column]:m[j]=[x-m[j][column]*y for x,y in zip(m[j],m[rank])]
        rank+=1
    return rank


def audit(matrix,neighbors,first,second):
    types=[row for row in combinations(range(10),4)
           if all(matrix[i][j]>=1 for i in row for j in row)]
    need(len(types)==5,'Unexpected positive binary type domain')
    solutions=[];checked=0
    for rows in combinations_with_replacement(types,9):
        checked+=1
        rebuilt=[[sum(i in row and j in row for row in rows) for j in range(10)] for i in range(10)]
        if rebuilt==matrix:solutions.append(rows)
    need(len(solutions)==1 and checked==715,'Binary factorization not unique')
    rows=solutions[0];need(row_rank(rows)==5,'Exact binary row rank')
    misses=list(map(set,[first,second]+list(rows)));A=set(range(10));B=set(range(11));counts=[]
    for b in (0,1):
        count=0
        for raw in combinations(B-{b},6):
            red=set(raw);valid=True
            for a in A:
                if a not in misses[b]:
                    pages=len(neighbors[a]-misses[b])+sum(a not in misses[j] for j in red)
                    if pages>3:valid=False;break
                else:
                    pages=len(misses[b]-neighbors[a]-{a})+sum(a in misses[j] for j in B-{b}-red)
                    if pages>6:valid=False;break
            if valid:count+=1
        counts.append(count)
    need(counts==[0,0],'Positive Gram retains an A--B neighbor row')
    return {'four_subsets':210,'entry_compatible_types':[list(row) for row in types],
            'nine_row_multisets':checked,'binary_factorizations':1,'binary_rows':[list(row) for row in rows],
            'rank':5,'AB_neighborhoods_checked':420,'AB_neighbor_counts':counts}
