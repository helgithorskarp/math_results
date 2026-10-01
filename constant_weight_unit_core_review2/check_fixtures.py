"""Regenerate and compare the affine-derived positive family and three profiles."""
from collections import Counter
from pathlib import Path
import json
from audit import affine_family
from exact import insist

record=json.loads(Path(__file__).with_name('fixtures.json').read_text())
counts=Counter();first={}
for words in affine_family():
    high={x for x in range(17) if sum(x in q for q in words)==4}
    b=tuple(sum(len(set(q)&high)==j for q in words) for j in range(5))
    counts[b]+=1;first.setdefault(b,words)
actual=[{'b':list(b),'labeled_transversals':n,'fixture':[list(q) for q in first[b]]} for b,n in sorted(counts.items())]
insist(record['profiles']==actual and record['family_size']==sum(counts.values())==256,'positive fixture/profile record differs')
insist([q['labeled_transversals'] for q in actual]==[16,192,48],'affine collinearity count')
print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'COMPLETE three distinct intrinsic profiles','labeled_transversals':256,'counts':[16,192,48],'high_core_edges':4},sort_keys=True))
