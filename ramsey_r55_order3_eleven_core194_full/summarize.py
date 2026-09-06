#!/usr/bin/env python3
"""Whole-core bookkeeping for the single Core194 full-extension test."""
from pathlib import Path
import argparse
import json
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(r['complete'] and v['verified'] and r['excluded']==v['excluded'] and r['open']==v['open'],'two complete matching runs')
    cases=run.cube.cases();old=json.loads((run.cube.PREVIOUS/'boundary.json').read_text())
    remaining=[i for i in old['remaining_full_cores'] if i not in r['excluded']]
    labels=sum(c['labeled'] for c in cases if c['index'] in r['excluded'])
    answer=dict(scope='unrestricted full extensions after Core194 universal empty-vertex bound',complete_tested_cores=1,
        new_whole_core_exclusions=r['excluded'],tested_unknown=r['open'],untested=[i for i in old['remaining_full_cores'] if i not in [c['index'] for c in cases]],
        new_labeled_exclusions=labels,full_proofs_replayed_twice=v['proof_replays'],remaining_full_cores=remaining,
        remaining_full_classes=len(remaining),remaining_full_labeled=old['remaining_full_labeled']-labels,
        cumulative_full_classes_excluded=197-len(remaining),cumulative_full_labeled_excluded=old['cumulative_full_labeled_excluded']+labels,
        first_empty_blue_bound_at_most_three_in=[i for i in old['first_empty_blue_bound_at_most_three_in'] if i in remaining],
        remaining_maximal_full_branches=[],target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
