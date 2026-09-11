#!/usr/bin/env python3
"""Regenerate the 36 A2 certificates in scratch; never use float status as proof."""
import argparse,json,pathlib,time
from fractions import Fraction
from a2_models import cases
from generate_a3_certificates import dual_cert

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args()
 if args.output.exists():raise FileExistsError(args.output)
 result=[]
 for name,(T,E,eq,eb,ub,bb),objective,meta in cases():
  cert=dual_cert(name,T,E,eq,eb,ub,bb,objective if any(objective) else None)
  if Fraction(cert['corrected_bound'])<=(1 if any(objective) else 0):raise ValueError('insufficient exact bound')
  result.append(cert)
 if len(result)!=36:raise ValueError('incomplete case cover')
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print('GENERATED: 36 certificates; run verify_a2.py on this bundle')

if __name__=='__main__':main()
