#!/usr/bin/env python3
"""Keep first-pair branch restrictions distinct from a whole-core exclusion."""
from pathlib import Path
import argparse
import json
import run


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(r['complete'] and v['verified'] and r['excluded']==v['excluded'] and r['open']==v['open'],'two complete matching runs')
    old=json.loads((run.cube.PREVIOUS/'boundary.json').read_text())
    run.cube.require(old['one_empty_branch_excluded'] and old['remaining_full_classes']==17 and old['remaining_full_labeled']==9153,'complete prior boundary')
    whole=r['excluded']==['blue','red'];remaining=[i for i in old['remaining_full_cores'] if i!=194 or not whole]
    answer=dict(scope='complete Core194 first-empty-pair color split',complete_tested_branches=2,
        excluded_pair_colors=r['excluded'],unknown_pair_colors=r['open'],one_empty_branch_remains_excluded=True,
        new_whole_core_exclusions=[194] if whole else [],full_proofs_replayed_twice=v['proof_replays'],
        remaining_full_cores=remaining,remaining_full_classes=len(remaining),remaining_full_labeled=9153-(81 if whole else 0),
        cumulative_full_classes_excluded=197-len(remaining),cumulative_full_labeled_excluded=old['cumulative_full_labeled_excluded']+(81 if whole else 0),
        untested_full_cores=[i for i in old['remaining_full_cores'] if i!=194],target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))
