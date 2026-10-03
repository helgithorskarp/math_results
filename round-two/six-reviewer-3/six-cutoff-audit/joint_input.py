"""Preaccess reviewer-defined literal interface; no producer schema or code.

Coordinates are physical orbit keys (core mask,deleted count,retained count),
not positions in a producer quotient. External literal inputs are proof data.
"""
import json
from fractions import Fraction as F
from exact import need

def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate input key');out[k]=v
 return out

def load(path):return json.loads(path.read_text(),object_pairs_hook=unique)

def decode(data,obj):
 need(type(obj)is dict and set(obj)=={'q','k','denominator','planes','weights'},'entire reviewer literal schema')
 need(type(obj['q'])is int and obj['q']==21 and type(obj['k'])is int and obj['k']==6,'literal family')
 den=obj['denominator'];need(type(den)is int and den==4096,'literal rational denominator')
 planes=obj['planes'];need(type(planes)is list and len(planes)==3,'all three planes')
 vectors=[]
 for index,plane in enumerate(planes):
  need(type(plane)is dict and set(plane)=={'kind','coordinates'} and plane['kind']==('cap' if index<2 else 'lower'),'separate cap/cap/lower kinds')
  rows=plane['coordinates'];need(type(rows)is list and len(rows)==len(data['keys'])==23,'all physical coordinates')
  coords={}
  for row in rows:
   need(type(row)is list and len(row)==4 and all(type(x)is int for x in row),'integer physical orbit entry')
   key=tuple(row[:3]);need(key in data['keys'] and key not in coords,'distinct actual physical orbit key')
   coords[key]=F(row[3],den)
  need(set(coords)==set(data['keys']),'entire physical orbit coverage')
  vectors.append([coords[data['keys'][g]] for g in data['g']])
 weights=[]
 need(type(obj['weights'])is list and len(obj['weights'])==3,'three exact weights')
 for w in obj['weights']:
  need(type(w)is list and len(w)==2 and all(type(x)is int for x in w) and w[1]>0,'integer rational dual weight')
  weights.append(F(*w))
 return vectors,weights
