#!/usr/bin/env python3
"""Update whole-core bookkeeping only after matching full proof replays."""
from pathlib import Path
import argparse
import json
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(r['complete'] and v['verified'] and r['excluded']==v['excluded'] and r['open']==v['open'],'two matching complete runs')
    old=json.loads((run.cube.BASE_SOURCE/'result.json').read_text())
    before=[c for c in old['cases'] if c['status']=='open']
    remaining=[c for c in before if c['index'] not in r['excluded']]
    removed=[c for c in before if c['index'] in r['excluded']]
    answer=dict(scope='unrestricted full extensions of19 cores after imported b=4 closure',complete_tested_cores=19,
        new_whole_core_exclusions=r['excluded'],tested_unknown=r['open'],untested=[124,155,159,168,180,194],
        full_proofs_replayed_twice=v['proof_replays'],new_labeled_exclusions=sum(c['labeled'] for c in removed),
        remaining_full_classes=len(remaining),remaining_full_labeled=sum(c['labeled'] for c in remaining),
        remaining_full_cores=[c['index'] for c in remaining],cumulative_full_classes_excluded=197-len(remaining),
        cumulative_full_labeled_excluded=115543-sum(c['labeled'] for c in remaining),target_graph=False,
        imported_first_fixed_blue_cycles_at_most_three_in=[c['index'] for c in run.cube.cases()])
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
