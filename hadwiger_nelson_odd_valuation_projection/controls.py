#!/usr/bin/env python3
"""Exact translated unit-vector controls and a missing-hypothesis counterexample."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json
import projection as P
K=P.K

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();args.work.mkdir(parents=True,exist_ok=True)
 cases=[((F(6),F(0)),1),((F(2),F(0)),1),((F(18),F(0)),1),((F(1,2),F(0)),1),((F(330),F(-42)),1),((F(330),F(42)),-1)];checks=0;unit_count=0;nonzero_radical=0
 shifts=[P.ZERO,(K.element(F(1,8),F(1,16),F(-3,32),F(5,64)),K.element(F(1,2),F(-1,4),F(1,8),F(-1,16))),(K.element(F(-7,256),F(13,128),F(5,32),F(-3,16)),K.element(F(5,64),F(3,16),F(-1,4),F(3,2)))];vals=[]
 for d,sign in cases:
  vals.append(P.certify_radicand(d,sign));D=d+(F(0),F(0))
  for a in range(-2,3):
   for b in range(-2,3):
    for den in [1,2,4]:
     q=(K.element(F(a,den)),K.element(F(b,den)));q2=P.mul(q,q,D);threeq=P.mul((K.element(3),K.ZERO),q2,D);z=P.mul(P.add(P.sub(P.ONE,threeq),P.mul((K.element(0,0,2,0),K.ZERO),q,D)),P.inverse(P.add(P.ONE,threeq),D),D)
     P.need(P.mul(z,P.conj(z),D)==P.ONE,'stereographic norm');unit_count+=1;nonzero_radical+=any(z[1])
     for shift in shifts:
      P.need(P.color(shift,d,sign)!=P.color(P.add(shift,z),d,sign),'translated projection collision');checks+=1
 # The excluded D=5 has a physical unit vector whose E projection has colour0.
 bad=(K.element(F(7,8)),K.element(0,0,F(1,8),0));P.need(P.mul(bad,P.conj(bad),K.element(5))==P.ONE,'bad-hypothesis unit vector');P.need(K.color(bad[0])==K.color(K.ZERO),'missing-hypothesis counterexample')
 rejected=0
 for d,sign in [((F(5),F(0)),1),((F(0),F(0)),1),((F(6),F(0)),0),((F(-2),F(0)),1)]:
  try:P.certify_radicand(d,sign)
  except ValueError:rejected+=1
 P.need(rejected==4,'invalid radicand accepted')
 # Precision doubling is exercised beyond the old finite256-bit frontier.
 P.need(P.valuation_real((F(1<<601),F(0)))==601,'large positive valuation');P.need(P.valuation_real((F(1,1<<601),F(0)))==-601,'large negative valuation')
 out={'status':'VERIFIED','fields':len(cases),'valuations':vals,'unit_vectors':unit_count,'nonzero_radical_vectors':nonzero_radical,'translated_colour_checks':checks,'rejected_hypotheses':rejected,'D5_projection_counterexample':True,'extreme_valuations':[601,-601]};(args.work/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
