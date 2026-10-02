"""Cold independent reconstruction and complete compact certificate comparison."""
import pathlib,json,hashlib,copy
import independent as I
import controls
P=pathlib.Path(__file__).resolve().parent

def validate(candidate,expected):
 for key in expected:
  I.need(key in candidate and candidate[key]==expected[key],'complete field:'+key)
 I.need(set(candidate)==set(expected),'complete field census')

def damage_checks(expected):
 trials=[]
 c=copy.deepcopy(expected);c['profiles'][0][2]+=1;trials.append(('original deletion cost',c,'profiles'))
 c=copy.deepcopy(expected);c['functions'][0]='ff'+c['functions'][0][2:];trials.append(('full function row',c,'functions'))
 c=copy.deepcopy(expected);c['edges'].pop();trials.append(('missing admissible transition',c,'edges'))
 c=copy.deepcopy(expected);c['exits'].pop(next(iter(c['exits'])));trials.append(('missing all-suffix exit',c,'exits'))
 c=copy.deepcopy(expected);c['longest'][1]+=1;trials.append(('word-length grading',c,'longest'))
 c=copy.deepcopy(expected);c['words'][1].append([0,1]);trials.append(('added word gate',c,'words'))
 c=copy.deepcopy(expected);c['tight_profile_indices'].pop();trials.append(('whole-original-domain coverage',c,'tight_profile_indices'))
 c=copy.deepcopy(expected);c['retained'].append(373);trials.append(('exit retained as a necessary front',c,'retained'))
 results=[]
 for name,c,field in trials:
  try:validate(c,expected)
  except ValueError as e:
   I.need(str(e)=='complete field:'+field,'damaged data rejected for intended reason')
   results.append(name)
  else:raise ValueError('damaged certificate accepted:'+name)
 return results

def run():
 if (P/'INDEPENDENCE.json').exists():
  seal=json.loads((P/'INDEPENDENCE.json').read_text())
  for f in seal['files']:
   raw=(P/f['path']).read_bytes()
   I.need(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'initial pre-native seal unchanged:'+f['path'])
 data=I.build();expected=json.loads(json.dumps(I.evidence(data)))
 raw=(P/'EVIDENCE.json').read_bytes();validate(json.loads(raw),expected)
 record=controls.run(data)
 I.need(json.loads((P/'CONTROLS.json').read_text())==json.loads(json.dumps(record)),'all independent calibration results')
 damage=damage_checks(expected)
 result=dict(status='COMPLETE_ORIGINAL_CUBE_COVER_AND_ACTUAL_SIX_GATE_BOUND_VERIFIED',profiles=len(data['original_profiles']),tight=len(data['tight_profiles']),functions=len(data['defining_cover']['states']),edges=len(data['defining_cover']['edges']),exits=len(data['defining_cover']['exits']),retained=len(data['defining_cover']['retained']),actual_max_preparation=6,evidence_sha256=hashlib.sha256(raw).hexdigest(),evidence_bytes=len(raw),controls=record,damage_rejections=damage)
 print(json.dumps(result,sort_keys=True))
 return result
if __name__=='__main__':run()
