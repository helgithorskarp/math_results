"""Label-free separation upgrades the normalizer quotient to full S18 isomorphism."""
from pathlib import Path
from collections import Counter
import argparse,json
from carrier import *

def invariant(code):
    d=packing(code)
    profile=tuple(sorted(d)); common=None
    if profile==tuple([5,15]+[20]*16):
        low=d.index(5); through=[x for x in code if x>>low&1]
        require(len(through)==5,'unique low point degree')
        meet=(1<<18)-1
        for x in through:meet&=x
        common=meet.bit_count()
    return profile,common

def run(work):
    work=Path(work)
    r=json.loads((work/'RESULT.json').read_text())
    classes=json.loads((work/'centralizer_classes.json').read_text())
    reps=[tuple(c)for c in r['centralizer_representatives']]
    rows=[];keys=[]
    for J in r['normalizer_classes']:
        ids=J['centralizer_classes']; rep=reps[min(ids)]; key=invariant(rep)
        counts=Counter(invariant(c)for j in ids for c in classes[j])
        require(set(counts)=={key} and counts[key]==J['size'],'constant label-free class invariant')
        rows.append({'centralizer_classes':ids,'labelled_size':J['size'],'normalizer_stabilizer':J['stabilizer'],'degree_profile':list(key[0]),'low_five_word_common_points':key[1],'representative':list(rep)})
        keys.append(key)
    require(len(keys)==len(set(keys)),'distinct full point-isomorphism invariants')
    require(sum(x['labelled_size']for x in rows)==len(json.loads((work/'labelled.json').read_text())),'full inventory')
    result={'full_point_isomorphism_classes':len(rows),'classes':rows,'invariant_entry_checks':sum(x['labelled_size']for x in rows)}
    (work/'ISOMORPHISM.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--expect');a=p.parse_args();z=run(a.work)
    if a.expect:require(json.loads(json.dumps(z))==json.loads(Path(a.expect).read_text()),'full isomorphism expected')
