#!/usr/bin/env python3
"""Definition-level controls and boundary examples for the lattice lemma."""
from fractions import Fraction
from itertools import permutations, product
import json
from audit import determinant, identity, multiply, need, rank_by_minors, transpose

def leibniz(a):
    n=len(a);total=0
    for p in permutations(range(n)):
        value=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        for i,j in enumerate(p):value*=a[i][j]
        total+=value
    return total

def root_check(g,s,b,c):
    n=len(g);sq=multiply(s,s)
    need(multiply(transpose(s),g)==multiply(g,s), 'self-adjoint boundary example')
    need(all(sq[i][j]+b*s[i][j]+c*int(i==j)==0
             for i in range(n) for j in range(n)), 'quadratic boundary example')
    return sum(s[i][i] for i in range(n))

def run():
    tests=0
    for flat in product(range(3),repeat=9):
        a=[list(flat[3*i:3*i+3]) for i in range(3)]
        need(determinant(a)==leibniz(a), 'subset determinant versus literal permutation definition')
        tests+=1
    for a,wanted in [([],1),([[0,1],[1,0]],-1),([[0,1,0],[0,0,1],[1,0,0]],1),
                     ([[1,2],[2,4]],0),([[-2,0],[0,3]],-6)]:
        need(determinant(a)==wanted,'determinant boundary')
    for a,wanted in [([[0,0],[0,0]],0),([[1,2],[2,4]],1),([[0,1],[1,0]],2)]:
        need(rank_by_minors(a)==wanted,'rank boundary')
    rejected=0
    for a in [[[True]],[[1,2]],[[Fraction(1,2)]]]:
        try:determinant(a)
        except ValueError:rejected+=1
    need(rejected==3,'invalid determinant inputs rejected')
    # Every symmetric 4x4 A over F2 gives S=J A, and conversely.
    # J is its own inverse, so JS=A is symmetric iff S is J-self-adjoint.
    j=[[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
    positions=[(r,c) for r in range(4) for c in range(r,4)]
    traces=0
    for bits in product(range(2),repeat=len(positions)):
        a=[[0]*4 for _ in range(4)]
        for (r,c),v in zip(positions,bits):a[r][c]=a[c][r]=v
        s=[[x%2 for x in row] for row in multiply(j,a)]
        need(sum(s[i][i] for i in range(4))%2==0,'complete F2 self-adjoint trace census')
        traces+=1
    c=[[0,5],[1,-1]];g0=[[2,0],[0,10]];b=[[1,1],[1,4]]
    g4=[g0[0]+b[0],g0[1]+b[1],b[0]+g0[0],b[1]+g0[1]]
    s4=[[0]*4 for _ in range(4)]
    for offset in (0,2):
        for i in range(2):
            for k in range(2):s4[offset+i][offset+k]=c[i][k]
    need(determinant(g4)==205 and all(g4[i][i]%2==0 for i in range(4)),
         'rank-four even odd-determinant Gram')
    # Orthogonal sum/difference of the two blocks reduces positivity to these two 2x2 matrices.
    for sign,wanted in [(1,41),(-1,5)]:
        g=[[g0[i][k]+sign*b[i][k] for k in range(2)] for i in range(2)]
        need(g[0][0]>0 and determinant(g)==wanted,'rank-four positive definiteness')
    need(root_check(g4,s4,1,-5)==-2,'rank-four integral root exists')
    need(determinant(g0)==20 and root_check(g0,c,1,-5)==-1,
         'dropping odd Gram determinant permits rank two')
    g2=[[2,1],[1,4]];s2=[[0,2],[1,0]]
    need(determinant(g2)==7 and root_check(g2,s2,0,-2)==0,
         'dropping odd linear coefficient permits rank two')
    g=[[2,1],[1,2]];s=[[0,Fraction(5,2)],[2,-1]]
    need(determinant(g)==3 and root_check(g,s,1,-5)==-1,
         'dropping integrality permits an odd trace')
    need(root_check([[2,1],[1,2]],[[0,0],[0,0]],1,0)==0,
         'reducible quadratic need not force half-rank trace')
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'ternary_3x3_determinant_controls':tests,'determinant_boundary_controls':5,
            'rank_boundary_controls':3,'invalid_inputs_rejected':rejected,
            'all_F2_symplectic_rank4_self_adjoint_matrices':traces,
            'lattice_hypothesis_boundary_controls':5,'all_passed':True}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
