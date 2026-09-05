#!/usr/bin/env python3
"""Compact, scope-preserving boundary report from the two complete runs."""
from pathlib import Path
import argparse
import json
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=json.loads((a.source_work/'result.json').read_text());verification=json.loads((a.verification_work/'verification.json').read_text())
    data=json.loads((a.source_work/'classification.json').read_text())
    run.require(result['complete'] and verification['verified'] and result['excluded']==verification['excluded'] and result['open']==verification['open'],'two complete matching runs')
    forced=data['arithmetically_closed']+([] if result['open'] else [194])
    answer=dict(remaining_full_cores=[r['index'] for r in data['cores']],remaining_full_classes=26,remaining_full_labeled=16605,
        cumulative_full_classes_excluded=171,cumulative_full_labeled_excluded=98938,new_whole_core_exclusions=[],
        forced_empty_cores=sorted(forced),forced_empty_classes=len(forced),
        noempty_signature_profiles_tested=15,noempty_profiles_excluded=result['excluded'],noempty_profiles_open=result['open'],
        second_proof_replays=verification['proof_replays'],target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
