"""Semantic controls on actual positive public certificates, not frozen hashes."""
import copy,itertools as it
import triple_check as t
import audit_packet as a

def run(folder):
 bases,old,ownerrows,colorrows=a.inputs(folder);d=t.domain(old[5]);owners,patches=a.decode(d,ownerrows[5],colorrows[5]);cases=[]
 def reject(label,own,patch,expected):
  try:t.audit(d,own,patch)
  except ValueError as e:
   t.need(expected in str(e),'damage failed for wrong reason');cases.append({'damage':label,'predicate':str(e)});return
  raise ValueError('damage accepted: '+label)
 own=owners.copy();own.pop(next(iter(own)));reject('omitted eligible physical word',own,patches,'complete radius-four ownership domain')
 own=owners.copy();own[next(iter(own))]=68;reject('invented blocker label',own,patches,'owner is real removed blocker')
 D=next(iter(patches));patch=copy.deepcopy(patches);patch.pop(D);reject('missing entire critical carrier',owners,patch,'complete sparse five exception carrier')
 patch=copy.deepcopy(patches);patch[D][1<<19]=0;reject('invented physical word',owners,patch,'patch cannot invent vertices')
 # Remove only the new-word color, preserving the critical-domain key.
 D=next(D for D,changes in patches.items() if any(d['blockers'][w].bit_count()==5 for w in changes));patch=copy.deepcopy(patches);w=next(w for w in patch[D] if d['blockers'][w].bit_count()==5);del patch[D][w];reject('five-blocker vertex uncolored',owners,patch,'all carrier vertices have a valid deleted blocker color')
 # Restore the original same VALID owner on a compatible co-occurring pair.
 collision=next(D for D,changes in patches.items() if all(d['blockers'][w].bit_count()<=4 for w in changes));patch=copy.deepcopy(patches);changed=next(iter(patch[collision]));original=owners[changed];patch[collision][changed]=original
 witness=None;field={**{w:i for i,w in enumerate(d['base'])},**owners}
 for other,c in field.items():
  if other!=changed and c==original and d['blockers'][other]&~collision==0 and not(d['words'][other][2]&d['words'][changed][2]):witness=[changed,other,original,collision];break
 t.need(witness is not None,'actual compatible collision witness');reject('shared valid blocker on compatible physical pair',owners,patch,'critical coloring physical compatible collision')
 # Decoder's duplicate check occurs before any expected-record comparison.
 bad=copy.deepcopy(ownerrows[5]);bad['owners'].append(bad['owners'][0])
 try:a.decode(d,bad,colorrows[5])
 except ValueError as e:t.need('duplicate owner word' in str(e),'wrong duplicate predicate');cases.append({'damage':'duplicated owner input','predicate':str(e)})
 else:raise ValueError('duplicate accepted')
 return {'controls':cases,'actual_collision_witness':witness,'positive_control':'Whole unmodified independent certificate record passed before these damages; sealed core/decoder unchanged.'}
if __name__=='__main__':
 import json,pathlib
 p=pathlib.Path(__file__).resolve().parent;(p/'controls-record.json').write_bytes(t.encode(run(p/'original')));print((p/'controls-record.json').read_text())
