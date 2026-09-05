#!/usr/bin/env python3
"""Exact whole-core consequences of a complete checked propagation sweep."""
from pathlib import Path
import argparse
import json
import cube


def summarize(source, verification):
    old=json.loads((source/'result.json').read_text());v=json.loads((verification/'verification.json').read_text())
    cube.require(old['complete'] and v['verified'] and v['complete_formula_reconstructions']==34,'complete checked results')
    cases=cube.cases();cube.require([r['index'] for r in old['cases']]==[c['index'] for c in cases],'all cases')
    cube.require([r['index'] for r in v['cases']]==[c['index'] for c in cases],'all reconstructed cases')
    excluded=[];opened=[]
    for case,r,s in zip(cases,old['cases'],v['cases']):
        cube.require(all(r[k]==case[k] and s[k]==case[k] for k in case),'entrywise case identity')
        cube.require(r['status']==s['status'] and r['formula']==s['formula'] and r['audit']==s['audit'],'entrywise evidence')
        if r['status']=='excluded':
            cube.require(r['solver_code']==20 and r['replay']['verified'] and s['replay']['verified'],'two full replays')
            excluded.append(case['index'])
        else:cube.require(r['status']=='open' and r['solver_code']==0,'explicit open case');opened.append(case['index'])
    cube.require(excluded==old['excluded']==v['excluded'] and opened==old['open']==v['open'],'summary partition')
    labels=sum(c['labeled'] for c in cases if c['index'] in excluded)
    return dict(whole_core_exclusions=excluded,remaining_open=opened,newly_excluded_classes=len(excluded),
        newly_excluded_labeled=labels,remaining_classes=len(opened),remaining_labeled=24057-labels,
        cumulative_excluded_classes=163+len(excluded),cumulative_excluded_labeled=91486+labels,
        applied_anchor_inequalities=56,complete_tested_classes=34,full_proofs_replayed_twice=len(excluded))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
    p.add_argument('--verification',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();answer=summarize(a.source,a.verification)
    a.output.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print(json.dumps(answer,sort_keys=True))
