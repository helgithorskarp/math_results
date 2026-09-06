#!/usr/bin/env python3
"""Keep new attachment exclusions separate from unchanged whole-core counts."""
from pathlib import Path
import argparse
import json
import generate as gen
import run


def main():
    p=argparse.ArgumentParser();p.add_argument('--source-work',type=Path,required=True)
    p.add_argument('--verification-work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=json.loads((a.source_work/'result.json').read_text());v=json.loads((a.verification_work/'verification.json').read_text())
    gen.need(r['complete'] and v['verified'],'complete decisions and verification')
    gen.need([(c['index'],c['status']) for c in r['cases']]==[(c['index'],c['status']) for c in v['cases']],'matched local outcomes')
    prev=gen.ROOT.parent/'ramsey_r55_order3_eleven_blue_bound_propagation'/'boundary.json'
    gen.need(gen.info(prev)['sha256']=='999e0c36bbf87c466b816a262d91ca0ff37c86017c0f61c0f0e82378f51294ac','whole-core boundary')
    old=json.loads(prev.read_text());new=r['local_excluded'];remaining=old['remaining_full_cores']
    bounded=sorted(set(old['imported_first_fixed_blue_cycles_at_most_three_in']+new)&set(remaining))
    answer=dict(local_excluded=new,local_witness=r['local_witness'],local_unknown=r['unknown'],
        new_maximal_branch_labeled_exclusions=sum(c['labeled'] for c in r['cases'] if c['status']=='local_excluded'),
        first_empty_blue_bound_at_most_three_in=bounded,remaining_maximal_full_branches=[c for c in remaining if c not in bounded],
        new_whole_core_exclusions=[],remaining_full_classes=old['remaining_full_classes'],remaining_full_labeled=old['remaining_full_labeled'],
        remaining_full_cores=remaining,cumulative_full_classes_excluded=old['cumulative_full_classes_excluded'],
        cumulative_full_labeled_excluded=old['cumulative_full_labeled_excluded'],target_graph=False)
    run.atomic(a.output,answer);print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':main()
