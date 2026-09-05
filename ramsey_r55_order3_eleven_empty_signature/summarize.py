#!/usr/bin/env python3
"""Derive the residual boundary from complete verified case outcomes."""
import argparse
import json
from pathlib import Path
import classify


def summarize(work, verification):
    r=json.loads((work/'result.json').read_text())
    v=json.loads((verification/'verification.json').read_text())
    cases=classify.classify()
    ids=cases['selected']
    classify.require(r['complete'] and not r['target_graph'] and v['verified'],'complete verified sweep')
    classify.require([c['index'] for c in r['cases']]==ids,'selected case coverage')
    classify.require(r['excluded']==v['excluded'] and r['open']==v['open'],'verified outcomes')
    classify.require(sorted(r['excluded']+r['open'])==ids,'complete partition')
    classify.require(v['proof_replays']==len(r['excluded']) and v['complete_cube_reconstructions']==len(ids),'verification counts')
    old=[c['index'] for c in cases['rows']]
    remaining=[i for i in old if i not in r['excluded']]
    labels={c['index']:c['labeled'] for c in cases['rows']}
    labeled=sum(labels[i] for i in remaining)
    return dict(previous_open=old,newly_excluded=r['excluded'],tested_open=r['open'],
                other_untested=[i for i in old if i not in ids],remaining_open=remaining,
                remaining_classes=len(remaining),remaining_labeled=labeled,
                cumulative_excluded_classes=197-len(remaining),cumulative_excluded_labeled=115543-labeled)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--verification',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=summarize(a.work,a.verification)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['remaining_classes','remaining_labeled','cumulative_excluded_classes']}))
