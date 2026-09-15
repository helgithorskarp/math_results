from pathlib import Path
from copy import deepcopy
import json
import verify as v
v.controls()
c=json.loads((Path(__file__).parent/'certificate.json').read_text())
checks=[]
for name in ['new_internal_edge_colour','receiving_word','invented_extra_contact']:
 d=deepcopy(c)
 if name=='new_internal_edge_colour':
  _,_,_,es,_=v.reconstruct();a,b=next(e for e in es if e[0]>=373)
  w=list(d['colour4']);w[b]=w[a];d['colour4']=''.join(w)
 elif name=='receiving_word':d['boundary_word']='3'+d['boundary_word'][1:]
 else:d['expected']['extra_contacts']=1
 try:v.verify(d)
 except ValueError as e:checks.append({'mutation':name,'rejected_by':str(e)})
 else:raise ValueError('damaged certificate accepted')
print(json.dumps({'status':'CONTROLS_PASS','damaged_certificates_rejected':checks},indent=2))
