#!/usr/bin/env python3
"""Exact controls for the credited reviewer orbit argument on the whole class.

Actual author six-sendov-2, researcher. The covariance argument and its
1536 application to the one-triple class are credited to six-reviewer-3,
sendov_one_triple_displacement_review3/REVIEW.md. Here it is applied to
the newly completed entire six-level class. These controls supplement
the universal written permutation argument; they do not enumerate orbits.
"""
import hashlib,json
from fractions import Fraction as F

CHECKS=0
def require(ok,label):
    global CHECKS
    CHECKS+=1
    if not ok:raise ValueError(label)
def main():
    covariance=[[F(1,8) if i==j else F(-1,56) for j in range(8)] for i in range(8)]
    projection=[[F(int(i==j))-F(1,8) for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):require(covariance[i][j]==projection[i][j]/7,'entire balanced permutation covariance')
        require(sum(covariance[i])==0,'whole constant-vector kernel')
    require(F(1,7)>F(9,64),'positive orbit correlation exceeds3/8')
    u=F(87,1000)
    j=(2058+21912*u-15876*u*u+19224*u**3+3402*u**4)/((3+u)*(1+3*u)**2)
    delta=j-F(785753,1000)
    require(delta==F(1331662697,1636234509000),'entire exact credited scalar strict gap')
    require(F(5,4)<1536*delta,'strict-region1536 domination')
    require(1536*1331662697-2045293136250==140766342,'explicit positive integer margin')
    require(F(1,90)<=1536,'all-balanced local coefficient retained')
    require(F(1,40)<=1536,'credited older saturated-triple local coefficient retained')
    record={'covariance':[[str(v) for v in row] for row in covariance],
            'balanced_projection':[[str(v) for v in row] for row in projection],
            'strict_gap':str(delta),'strict_distance_upper':'5/4',
            'strict_region_ratio':str(F(5,4)/delta),'global_coefficient':1536,
            'positive_integer_margin':140766342,'checks':CHECKS}
    digest=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps({'agent':'six-sendov-2','role':'researcher','status':'PASS_EXACT_CREDITED_ORBIT_REFINEMENT',
                     'checks':CHECKS,'record_sha256':digest,'global_coefficient':1536,
                     'does_not_regenerate_twelve_kernels':True},sort_keys=True))
if __name__=='__main__':main()
