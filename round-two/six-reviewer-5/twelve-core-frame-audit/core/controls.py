"""Definition-level outward-enclosure tests, including signed boundaries."""
import json
from fractions import Fraction as F
from enclosure import Box,SCALE
from frame import scalar_frame,all_points,dot,LABELS,CONTACTS,chart_gap

def contains(x,v):
    if not F(x.lo,SCALE)<=v<=F(x.hi,SCALE):raise ValueError('lost real endpoint')

count=0
samples=(F(-11,7),F(-1,2),F(0),F(1,3),F(1),F(9,5))
for a in samples:
 for b in samples:
  x,y=Box(a),Box(b)
  contains(x+y,a+b);contains(x-y,a-b);contains(x*y,a*b)
  count+=3
  if b:contains(x/y,a/b);count+=1
for a,b in ((F(-3,2),F(7,3)),(F(-9,7),F(-1,11)),(F(0),F(4,5))):
 x=Box(a,b)
 for v in (a,b,(a+b)/2):contains(x.square(),v*v);count+=1
 if a<=0<=b:contains(x.square(),0);count+=1
for x in (Box(F(1,3)),Box(0,2),Box(F(81,49))):
 y=x.sqrt()
 if y.lo*y.lo>x.lo*SCALE or y.hi*y.hi<x.hi*SCALE:raise ValueError('square root rounding')
 count+=1
for x in (Box(-1,1),Box(0),Box(0,2)):
 try:Box(1)/x
 except ArithmeticError:count+=1
 else:raise ValueError('zero denominator accepted')
try:Box(-1,0).sqrt()
except ArithmeticError:count+=1
else:raise ValueError('negative root accepted')

# A rational midpoint probes all four sign constructions, never a packing claim.
t,z=Box(F(577,1000)),Box(F(6,5))
a=scalar_frame(t,z)
for eps in (-1,1):
 for eta in (-1,1):
  points=all_points(a,eps,eta)
  for i in LABELS:contains(dot(points[i],points[i],t),F(1));count+=1
  for i,j in CONTACTS:contains(dot(points[i],points[j],t),F(577,1000));count+=1
if chart_gap(Box(F(14,25)),Box(F(25,11))).lo>0:raise ValueError('chart equality excluded')
print(json.dumps(dict(exact_endpoint_controls=count,all_four_root_controls=128,
 precision_bits=96,zero_and_tangent_retained=True),sort_keys=True))
