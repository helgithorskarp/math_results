"""Separate private-entry/blue-neighborhood checker; six-books-3, researcher.
Imports no author generator, census, form recovery or exceptions module.
"""
from itertools import permutations
from math import prod


def need(ok,message):
    if not ok:raise RuntimeError(message)


def audit(record,matrix,neighbors,first,second):
    need(record['matrix']==matrix,'Exception matrix mismatch')
    types=[]
    for word in range(1024):
        if word.bit_count()!=4:continue
        row=tuple(i for i in range(10) if word>>i&1)
        if all(matrix[i][j]>0 for i in row for j in row):types.append(row)
    types.sort();need(len(types)==5,'Exception four-row domain')
    # Every possible row type owns a matrix coordinate no other type contributes.
    # Its multiplicity is forced in any decomposition, so this proves uniqueness.
    counts=[];private=[]
    for k,row in enumerate(types):
        coordinate=next(((i,j) for i in row for j in row if i<=j
                         and all(i not in other or j not in other for t,other in enumerate(types) if t!=k)),None)
        need(coordinate is not None,'No forcing private coordinate')
        i,j=coordinate;count=matrix[i][j]
        need(type(count) is int and 0<=count<=9,'Invalid forced multiplicity')
        counts.append(count);private.append([i,j])
    need(sum(counts)==9,'Exception row total')
    rows=[row for row,count in zip(types,counts) for _ in range(count)]
    need([[sum(i in row and j in row for row in rows) for j in range(10)] for i in range(10)]==matrix,'Exception Gram reconstruction')
    data=record['audit']
    need(data['binary_rows']==[list(row) for row in rows] and data['entry_compatible_types']==[list(row) for row in types], 'Exception binary data differs')
    # Five contributing types bound rank by five; this explicit minor proves equality.
    determinant=0
    for p in permutations(range(5)):
        sign=(-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))
        determinant+=sign*prod(int(p[k] in types[k]) for k in range(5))
    need(abs(determinant)==2 and data['rank']==5,'Exception rank-five minor')
    # Enumerate blue neighborhoods, derive red neighbors by complement, then count
    # full pages using literal22-point neighbor sets, rather than the author formula.
    misses=list(map(set,[first,second]+rows));universe=set(range(22));counts_AB=[]
    red_A=[{0}|{i+1 for i in neighbors[a]}|{j+11 for j in range(11) if a not in misses[j]}
           for a in range(10)]
    for b in (0,1):
        others=[j for j in range(11) if j!=b];passing=visited=0
        for word in range(1024):
            if word.bit_count()!=4:continue
            visited+=1
            blue={others[k] for k in range(10) if word>>k&1}
            red_B={a+1 for a in range(10) if a not in misses[b]}|{j+11 for j in others if j not in blue}
            need(len(red_B)==10 and all(len(row)==10 for row in red_A),'Literal regular neighbor rows')
            valid=True
            for a in range(10):
                if a not in misses[b]:
                    pages=len(red_A[a]&red_B);cap=3
                else:
                    pages=len(universe-({a+1,b+11}|red_A[a]|red_B));cap=6
                if pages>cap:valid=False;break
            if valid:passing+=1
        need(visited==210,'Blue neighborhood coverage');counts_AB.append(passing)
    need(counts_AB==[0,0] and data['AB_neighbor_counts']==counts_AB,'Exception A--B obstruction failed')
    return {'unique_binary_factor':True,'private_coordinates':private,'forced_multiplicities':counts,
            'rank_five_minor':determinant,'AB_neighbor_counts':counts_AB,'AB_neighborhoods_checked':420}
