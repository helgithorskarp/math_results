"""Literal moving-pair common blocks and the two complete cap inventories."""
import deps
I=((1,0,0,1),(0,0),(0,0))
A=((-1,3,0,1),(-3,2),(0,2))
B=((-1,0,-1,1),(0,3),(1,2))
C=((1,-3,1,-2),(3,2),(3,2))
Z=((2,-3,1,-1),(0,3),(1,2))
A2=((-1,3,0,1),(-3,2),(0,4))
B2=((-1,0,-1,1),(0,3),(1,4))
C2=((1,-3,1,-2),(3,2),(3,4))
Z2=((2,-3,1,-1),(0,3),(1,4))
ROOT_BLOCK=tuple(((0,u),(1,v)) for u,v in [(4,2),(4,3),(5,3),(6,4),(7,4)])
AFTER_BLOCK=tuple(((0,u),(1,v)) for u,values in
    [(4,range(2,6)),(5,range(3,6)),(6,range(4,7)),(7,range(4,7))] for v in values)
CASES=(
    {'name':'root','point':((0,3),(1,2)),'fixed':(I,),
     'blocked':ROOT_BLOCK,'expected':tuple(sorted((A,B,C,Z))), 'b_min':3},
    {'name':'after_A','point':((0,3),(1,4)),'fixed':(I,A),
     'blocked':AFTER_BLOCK,'expected':tuple(sorted((A2,B2,C2,Z2))), 'b_min':5}
)
