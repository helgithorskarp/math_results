"""Previously proved E1 cuts plus this pass's checked Q/sealed-cell cuts."""
import deps
import json
from pathlib import Path
import strip_parametric_geometry as G
from strip_contact_reader import freeze

H=Path(__file__).resolve().parent
EXCLUDED=[]
for directory in ['strip-e2-branches','strip-e2-forced-p','strip-e2-shift-exclusion']:
    for row in json.loads((H.parent/directory/'inputs.json').read_text())['cases']:
        if 'pose' in row:EXCLUDED.append(freeze(row['pose']))
EXCLUDED.extend((((2,-3,1,-2),(0,5),(0,3)),
                 ((2,-3,1,-1),(0,-1),(0,0))))
EXCLUDED=tuple(EXCLUDED)


def known_bad(rel):
    rows=[]
    for h in (rel,G.inverse(rel)):
        rows.append(G.allowed(h,EXCLUDED))
        if h[0]==(1,0,0,1):
            rows.append(G.both(G.atom('eq',G.sub(h[1],(0,6))),
                G.neg(G.either(G.atom('eq',G.sub(h[2],(-1,3))),
                               G.atom('eq',G.sub(h[2],(-1,4)))))))
            rows.append(G.both(G.atom('eq',G.sub(h[1],(0,5))),
                G.atom('ge',G.sub(h[2],(0,3))),
                G.atom('ge',G.sub((1,1),h[2]))))
    return G.both(G.touching(rel),G.either(*rows))
