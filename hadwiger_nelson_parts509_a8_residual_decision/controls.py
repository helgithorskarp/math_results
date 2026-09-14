#!/usr/bin/env python3
from pathlib import Path
from itertools import combinations,product
from copy import deepcopy
import json
import check
import reduction

def main():
 prefix=reduction.controls();degree=0
 for d in range(9):
  for need in range(-1,d+2):
   clauses=[]
   if need>d:clauses=[[-(d+1)]]
   elif need>0:clauses=[[-(d+1)]+[i+1 for i in subset] for subset in combinations(range(d),d-need+1)]
   for bits in product([False,True],repeat=d+1):
    got=reduction.satisfies(clauses,{i+1:v for i,v in enumerate(bits)})
    reduction.require(got==(not bits[-1] or sum(bits[:-1])>=need),'degree truth table');degree+=1
 m=check.module('accepted_geometry',check.REPO/'hadwiger_nelson_parts509_shape8_transfer/verify.py');den,points,vertices,U,E,words,pins=m.inputs()
 third=json.loads((check.HERE/'baseline_cuts.json').read_text())[-1];damaged=[]
 for name in ['duplicate_D','bad_label','bad_word','bad_domain','bad_class']:
  r=deepcopy(third)
  if name=='duplicate_D':r['D'].append(r['D'][0])
  if name=='bad_label':r['D'][0]=999999
  if name=='bad_word':r['c']='0'*303
  if name=='bad_domain':r['c']=r['c'][:-1]
  if name=='bad_class':r['p']=20
  damaged.append(r)
 for r in damaged:
  try:check.check_positive(r,U,E,words)
  except (ValueError,IndexError,KeyError):pass
  else:raise ValueError('corrupted cut accepted')
 print(json.dumps({'status':'CONTROLS_PASS','counter_input_cases':prefix,'direct_degree_cases':degree,'corrupted_cut_rejections':len(damaged)},sort_keys=True))

if __name__=='__main__':main()
