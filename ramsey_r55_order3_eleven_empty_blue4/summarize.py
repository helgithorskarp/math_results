#!/usr/bin/env python3
"""Report branch exclusions without declaring any new whole-core exclusion."""
from pathlib import Path
import argparse
import json
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    run.cube.require(r['complete'] and v['verified'] and r['excluded']==v['excluded'] and r['open']==v['open'],'two complete matching runs')
    answer=dict(scope='first fixed vertex blue to exactly four blue moving triangles',complete_tested_branches=25,
        blue4_excluded=r['excluded'],blue4_open=r['open'],full_proofs_replayed_twice=v['proof_replays'],
        new_whole_core_exclusions=[],remaining_full_classes=25,remaining_full_labeled=15957,
        remaining_full_cores=[c['index'] for c in run.cube.cases()],
        cumulative_full_classes_excluded=172,cumulative_full_labeled_excluded=99586,target_graph=False,
        first_fixed_blue_cycles_at_most_three_in=r['excluded'])
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
