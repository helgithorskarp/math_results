#!/usr/bin/env python3
"""Small arithmetic controls and rejection of corrupted positive certificates."""
from copy import deepcopy
from pathlib import Path
import json
import verify as v

def main():
    c=json.loads(Path(__file__).with_name('certificate.json').read_text())
    g=v.geometry();v.verify(c,g)
    for r in v.RAD:
        v.require(v.multiply(v.radical(r),v.radical(r))==v.scalar(r),'radical square')
    v.require(v.multiply(v.radical(21),v.radical(33))==v.radical(77,3),'mixed radical')
    square=[(v.scalar(0),v.scalar(0)),(v.scalar(1),v.scalar(0)),
            (v.scalar(1),v.scalar(1)),(v.scalar(0),v.scalar(1))]
    es=[(i,j) for i in range(4) for j in range(i+1,4) if v.isunit(square[i],square[j],1)]
    v.require(es==[(0,1),(0,3),(1,2),(2,3)],'strict unit-square control')
    v.require(v.norm(v.minus(square[0],square[2]))==v.scalar(2),'square diagonal')
    v.require(v.canonical_count(3,[(0,1),(1,2),(0,2)],2)[0]==0,'triangle 2-colouring')
    v.require(v.canonical_count(3,[(0,1),(1,2),(0,2)],3)[0]==1,'triangle 3-colouring')
    mutants=[]
    x=deepcopy(c);a,b=g['edges'][0];x['four_word'][a]=x['four_word'][b];mutants.append(('physical conflicting edge',x))
    x=deepcopy(c);x['four_word'][0]=True;mutants.append(('boolean colour',x))
    x=deepcopy(c);x['four_word'].pop();mutants.append(('missing vertex colour',x))
    x=deepcopy(c);x['source_ids'][0]=x['source_ids'][1];mutants.append(('carrier collision map',x))
    x=deepcopy(c);x['point_sha256']='0'*64;mutants.append(('coordinate bytes',x))
    x=deepcopy(c);x['edge_sha256']='0'*64;mutants.append(('edge bytes',x))
    x=deepcopy(c);x['edges']-=1;mutants.append(('omitted complete unit edge',x))
    x=deepcopy(c);x['source_five_word'][1]=x['source_five_word'][3];mutants.append(('carrier diagonal five-word',x))
    x=deepcopy(c);x['violated_carrier_diagonals']=[];mutants.append(('concealed failed conversion',x))
    x=deepcopy(c);x['moser_ids'][0]=x['moser_ids'][1];mutants.append(('spindle collision',x))
    x=deepcopy(c);x['denominator']=48;mutants.append(('coordinate scale',x))
    rejected=[]
    for label,x in mutants:
        try:v.verify(x,g)
        except ValueError:rejected.append(label)
        else:raise ValueError('accepted corruption: '+label)
    print(json.dumps({'radical_square_controls':8,'mixed_radical_controls':1,
      'square_geometry_controls':2,'small_colouring_controls':2,
      'rejected_corruptions':rejected,'all_passed':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
