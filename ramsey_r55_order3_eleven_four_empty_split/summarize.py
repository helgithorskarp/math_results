#!/usr/bin/env python3
"""Distinguish whole-core exclusions from restrictions on empty multiplicity."""
from pathlib import Path
import argparse
import json
import cube


def summarize(source, verification):
    result=json.loads((source/'result.json').read_text());verified=json.loads((verification/'verification.json').read_text())
    cube.require(result['complete'] and not result['target_graph'] and verified['verified'],'complete checked outcomes')
    cases=cube.cases();cube.require([r['id'] for r in result['cases']]==[c['id'] for c in cases],'case coverage')
    cube.require(result['excluded']==verified['excluded'] and result['open']==verified['open'],'checked partition')
    cube.require(sorted(result['excluded']+result['open'])==[c['id'] for c in cases] and verified['proof_replays']==len(result['excluded']),'complete partition/replays')
    rows={r['id']:r['status'] for r in result['cases']};closed=[];at_least_two=[];exactly_one=[];unrestricted=[]
    for core in cube.cores():
        i=core['index'];one=rows[f'c{i}_one'];multiple=rows[f'c{i}_multiple']
        if one==multiple=='excluded':closed.append(i)
        elif one=='excluded':at_least_two.append(i)
        elif multiple=='excluded':exactly_one.append(i)
        else:unrestricted.append(i)
    old=json.loads((cube.PREVIOUS/'boundary.json').read_text());remaining=[i for i in old['remaining_open'] if i not in closed]
    labels={r['index']:r['labeled'] for r in json.loads((cube.PREVIOUS/'classification.json').read_text())['rows']}
    count=sum(labels[i] for i in remaining)
    return dict(whole_core_exclusions=closed,at_least_two_empty=at_least_two,exactly_one_empty=exactly_one,both_branches_open=unrestricted,
                excluded_subcases=result['excluded'],open_subcases=result['open'],remaining_open=remaining,remaining_classes=len(remaining),remaining_labeled=count,cumulative_excluded_classes=197-len(remaining),cumulative_excluded_labeled=115543-count)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--verification',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=summarize(a.source,a.verification)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
