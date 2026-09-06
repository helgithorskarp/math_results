#!/usr/bin/env python3
"""Keep branch exclusions distinct from a complete Core194 exclusion."""
from pathlib import Path
import argparse
import json
import run


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(r['complete'] and v['verified'] and r['excluded']==v['excluded'] and r['open']==v['open'],'two complete matching runs')
    old=json.loads((run.cube.BOUNDARY/'boundary.json').read_text())
    run.cube.require(old['remaining_full_classes']==17 and old['remaining_full_labeled']==9153 and 194 in old['remaining_full_cores'],'current frontier')
    one=[c['id'] for c in run.cube.cases() if c['branch']=='one']
    all_one=all(k in r['excluded'] for k in one);multiple='multiple' in r['excluded'];whole=all_one and multiple
    remaining=[i for i in old['remaining_full_cores'] if i!=194 or not whole]
    answer=dict(scope='complete seven-case Core194 multiplicity split',complete_tested_branches=7,
        excluded_branches=r['excluded'],unknown_branches=r['open'],one_empty_branch_excluded=all_one,
        multiple_empty_branch_excluded=multiple,new_whole_core_exclusions=[194] if whole else [],
        remaining_one_empty_missing_pairs=[c['missing_pair'] for c in run.cube.cases() if c['branch']=='one' and c['id'] not in r['excluded']],
        full_proofs_replayed_twice=v['proof_replays'],remaining_full_cores=remaining,remaining_full_classes=len(remaining),
        remaining_full_labeled=9153-(81 if whole else 0),cumulative_full_classes_excluded=197-len(remaining),
        cumulative_full_labeled_excluded=old['cumulative_full_labeled_excluded']+(81 if whole else 0),
        untested_full_cores=[i for i in old['remaining_full_cores'] if i!=194],target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))
