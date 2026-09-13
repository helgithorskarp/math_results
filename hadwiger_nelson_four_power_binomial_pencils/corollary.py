#!/usr/bin/env python3
"""Align all homogeneous nonmonomial pencils with three proved classes.

This certifies the finite scope bridge, not the imported exclusion proofs.
The independent span enumeration uses only Python's standard library.
"""
from itertools import product,combinations
from pathlib import Path
import hashlib,json
import pins
from classification import MUL,P1,normalize,need
HERE=Path(__file__).resolve().parent

def decode(p):return tuple((tuple(n),c) for n,c in p)
def run():
    pins.verify()
    normals=sorted({normalize(n) for n in product(range(4),repeat=4) if any(n)})
    lines=set()
    for a,b in combinations(normals,2):
        line=tuple(sorted((normalize(tuple(MUL[u][x]^MUL[v][y] for x,y in zip(a,b))),0) for u,v in P1))
        need(len(set(line))==5,'five projective directions');lines.add(line)
    need(len(normals)==85 and len(lines)==357,'complete PG(3,4) lines')
    allowed={p for p in lines if all(sum(bool(v) for v in n)>=2 for n,c in p)}
    three={p for p in allowed if any(not any(n[k] for n,c in p) for k in range(4))}
    nobin={p for p in allowed if all(sum(bool(v) for v in n)>=3 for n,c in p)}
    binomial=allowed-three-nobin
    old3=json.loads((HERE.parent/'hadwiger_nelson_homogeneous_three_power_pencils/A5_INTERFACE.json').read_text())
    old4=json.loads((HERE.parent/'hadwiger_nelson_four_power_no_binomial_pencils/PENCILS.json').read_text())
    new=json.loads((HERE/'PENCILS.json').read_text())
    need(three=={decode(p) for p in old3['all_a5_pencils']},'entrywise three-position proof scope')
    need(nobin=={decode(p) for i,p in old4},'entrywise no-binomial proof scope')
    need(binomial=={decode(p) for i,p in new},'entrywise new binomial proof scope')
    need((len(allowed),len(three),len(nobin),len(binomial))==(279,36,54,189),'disjoint exhaustive proof scopes')
    lifts=sum(2**sum(sum(bool(v) for v in n)-1 for n,c in p) for p in allowed)
    need(lifts==502272,'full homogeneous lift count')
    return {'status':'PASS','all_rank_two_spaces':357,'spaces_containing_monomials':78,'homogeneous_nonmonomial_pencils':279,'three_position_pencils':36,'four_position_no_binomial_pencils':54,'four_position_binomial_pencils':189,'total_raw_lifts':lifts,'pencil_set_sha256':hashlib.sha256(json.dumps(sorted(allowed),separators=(',',':')).encode()).hexdigest(),'claim_scope':'physical nonconcurrence; imported proof premises remain explicit'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
