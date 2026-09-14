"""Reject damaged positive certificates without relying on file hashes."""
from copy import deepcopy
from pathlib import Path
import json
from verify import verify,need
from model import sign

def controls():
 c=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
 verify(c);rejected=[]
 def trial(name,edit):
  d=deepcopy(c);edit(d)
  try:verify(d)
  except ValueError:rejected.append(name)
  else:raise ValueError('accepted corruption: '+name)
 trial('wrong_schema',lambda d:d.__setitem__('schema','bad'))
 trial('no_words',lambda d:d.__setitem__('words',[]))
 trial('short_word',lambda d:d['words'].__setitem__(0,d['words'][0][:-1]))
 trial('fifth_colour',lambda d:d['words'].__setitem__(0,'4'+d['words'][0][1:]))
 trial('improper_unit_edge',lambda d:d['words'].__setitem__(0,'0'*100))
 trial('proper_but_incomplete_relation',lambda d:d.__setitem__('words',[d['words'][0]]*len(d['words'])))
 # Sign fixtures are elementary comparisons, independent of graph counts.
 fixtures=[((0,0,0,0,0,0,0,0),0),((-1,1),1),((-2,1),-1),
           ((0,0,0,-1,1,0,0,0),1),((0,-1,-1,0,1,0,0,0),-1),
           ((-4,1,0,0,1,0,0,0),1),((-1,-1,0,0,1,0,0,0),1)]
 for a,s in fixtures:
  need(sign(a)==s and sign(tuple(-v for v in a))==-s,'exact sign fixture')
 return {'status':'CONTROLS PASS','corruptions_rejected':len(rejected),
         'rejected':rejected,'signed_radical_comparisons':2*len(fixtures)}

if __name__=='__main__':print(json.dumps(controls(),indent=2,sort_keys=True))
