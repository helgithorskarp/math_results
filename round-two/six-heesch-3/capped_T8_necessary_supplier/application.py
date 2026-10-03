#!/usr/bin/env python3
"""Bind the two-copy force to the credited literal fifth using the owned decoder.
Actual author six-heesch-3, researcher. Foreign source is data only.
The standalone force lemma needs no external input or neighboring directory.
"""
from hashlib import sha256
import json
from pathlib import Path
import resource
import sys
import time
import check

def run():
    started=time.monotonic();here=Path(__file__).resolve().parent
    previous=here.parent/'external_six_corona_replay'
    sys.path.insert(0,str(previous))
    import decoder
    expected=json.loads((previous/'expected.json').read_text())['h8l']
    foreign=previous/'witness_h8l.txt'
    check.g.require(sha256(foreign.read_bytes()).hexdigest()==expected['foreign_sha256'],
                    'credited input changed')
    data,source=decoder.decode(foreign,8,True,previous/'drafter_tables.py')
    raw=(json.dumps(data,indent=2)+'\n').encode()
    check.g.require(sha256(raw).hexdigest()==check.base.WITNESS_SHA,
                    'entire normalized six-corona input changed')
    document=json.loads((here/'certificate.json').read_text())
    rows=document['certificate']['template']
    for row in rows:
        actual=data['copies'][row['original_index']]
        check.g.require(actual['pose']==row['pose'] and actual['level']==row['original_level']<=5,
                        'template is not in literal fifth')
    matches=[i for i,row in enumerate(data['copies']) if tuple(row['pose'])==check.FORCED]
    check.g.require(matches==[106] and data['copies'][106]['level']==6,'known sixth control changed')
    check.read(document)
    out={'actual_author':'six-heesch-3','role':'researcher',
       'status':'two-copy necessity applies to every strict surround retaining the credited literal fifth',
       'certificate_sha256':document['certificate_sha256'],
       'literal_six_witness_sha256':check.base.WITNESS_SHA,
       'old_fifth_count':sum(row['level']<=5 for row in data['copies']),
       'original_indices':[row['original_index'] for row in rows],
       'original_levels':[row['original_level'] for row in rows],
       'known_sixth_supplier_index':106,'known_sixth_is_a_control_only':True,
       'prior_construction_commit':'35e06b5f68cc76930d5421edeb64af1bb220d756',
       'foreign_checker_or_solver_executed':False,'global_Heesch_upper_claimed':False,
       'independent_review_claimed':False}
    out['stable_mathematical_sha256']=check.base.canonical(out)
    out['elapsed_seconds']=time.monotonic()-started
    out['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return out

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
