"""Reject damaged residual proofs at the positive67-word core."""
import copy
import json
from pathlib import Path

import verify_residual as v
import verify_witness as w

HERE=Path(__file__).resolve().parent


def run():
    witness=json.loads((HERE/'witness67.json').read_text())
    positive=w.check(witness)
    core={'blocks':witness['core_blocks'],'core_sha256':witness['core_sha256']}
    certificates=json.loads((HERE/'residual.json').read_text())['certificates']
    certificate=next(c for c in certificates if c['core_sha256']==core['core_sha256'])
    v.check_one(core,certificate)
    v.check(certificate['limit']==22 and certificate['tree']['kind']=='color','control boundary')
    bad=[]
    c=copy.deepcopy(certificate);c['core_sha256']='0'*64;bad.append((core,c))
    c=copy.deepcopy(certificate);c['candidate_sha256']='0'*64;bad.append((core,c))
    c=copy.deepcopy(certificate);c['candidate_count']+=1;bad.append((core,c))
    c=copy.deepcopy(certificate);c['limit']=True;bad.append((core,c))
    c=copy.deepcopy(certificate);c['limit']=21;bad.append((core,c))
    c=copy.deepcopy(certificate);c['tree']={'kind':'size'};bad.append((core,c))
    c=copy.deepcopy(certificate);c['tree']['colors']=[0]*c['candidate_count'];bad.append((core,c))
    c=copy.deepcopy(certificate);c['tree']['colors'][0]=True;bad.append((core,c))
    c=copy.deepcopy(certificate);c['tree']['colors'].pop();bad.append((core,c))
    q=copy.deepcopy(core);q['blocks'][0]=q['blocks'][1];bad.append((q,certificate))
    for q,c in bad:
        try:
            v.check_one(q,c)
        except (ValueError,TypeError,RuntimeError):
            continue
        raise ValueError('damaged capacity evidence accepted')
    result={'status':'PASSED','bad_capacity_rejections':len(bad),'positive_words':positive['words']}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    run()
