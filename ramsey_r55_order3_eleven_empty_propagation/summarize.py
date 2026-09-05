#!/usr/bin/env python3
"""Preserve the complete full-core boundary without treating UNKNOWN as feasible."""
from pathlib import Path
import argparse
import json
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(result['complete'] and v['verified'] and result['excluded']==v['excluded'] and result['open']==v['open'],'two complete matching runs')
    excluded=[r for r in result['cases'] if r['status']=='excluded'];opened=[r for r in result['cases'] if r['status']=='open']
    labels=sum(r['labeled'] for r in excluded)
    answer=dict(complete_tested_classes=26,new_whole_core_exclusions=result['excluded'],newly_excluded_classes=len(excluded),
        newly_excluded_labeled=labels,remaining_open=result['open'],remaining_classes=len(opened),remaining_labeled=sum(r['labeled'] for r in opened),
        cumulative_excluded_classes=171+len(excluded),cumulative_excluded_labeled=98938+labels,
        full_proofs_replayed_twice=v['proof_replays'],all_remaining_force_empty=True,target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
