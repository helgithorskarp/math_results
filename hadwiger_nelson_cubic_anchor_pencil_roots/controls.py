#!/usr/bin/env python3
"""Positive physical collision controls and targeted corrupt-certificate tests."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
from interface import A,HERE,build,selection,pair_interface
spec=importlib.util.spec_from_file_location('cubic_anchor_main_verifier',HERE/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)


def reject(name,fn,expected):
    try:fn()
    except ValueError as e:
        A.need(expected in str(e),'wrong rejection for '+name+': '+str(e));return name
    raise ValueError('corruption accepted: '+name)


def run(path):
    cert=json.loads(Path(path).read_text());factors,_,_,buckets,_=build();V.initialize(factors)
    selected,pairs=pair_interface(selection(buckets),buckets)
    positive=next(c for c in cert['components'] if c.get('point_count')==147)
    other=next(c for c in cert['components'] if c.get('point_count')==108)
    for c in (positive,other):V.check_field(c)
    rejected=[]
    bad=copy.deepcopy(positive);bad['real_embeddings']+=1
    rejected.append(reject('alter_real_root_count',lambda:V.check_field(bad),'real embedding count'))
    bad2=copy.deepcopy(positive);bad2['colour_weights']=[1,1,1,1,1]
    rejected.append(reject('break_collision_colour',lambda:V.check_field(bad2),'colour descends through collisions'))
    bad3=copy.deepcopy(positive);bad3['edge_count']-=1
    rejected.append(reject('omit_physical_unit_edge',lambda:V.check_field(bad3),'physical graph counts'))
    bad4=copy.deepcopy(positive);bad4['active_curves']=bad4['active_curves'][:-1]
    rejected.append(reject('omit_active_event',lambda:V.check_field(bad4),'all active norm events'))
    pairrow=next(r for r in cert['pairs'] if positive['key'] in r['components'])
    a,b=pairrow['pair'];cc=V.root_task((factors[a],factors[b]));bad5=copy.deepcopy(pairrow);bad5['components'].remove(positive['key'])
    rejected.append(reject('omit_exceptional_component',lambda:V.check_pair_record((a,b),cc,bad5),'complete pair-component coverage'))
    records={c['key']:copy.deepcopy(c) for c in cert['components']};idx,domains,pp=selected[0]
    source=next(r for r in cert['pairs'] if tuple(r['pair'])==pp[0]);key=source['components'][0]
    records[key]['active_curves']=sorted(set(records[key]['active_curves'])|{d[0] for d in domains})
    rejected.append(reject('invent_full_pencil_concurrence',lambda:V.concurrency(selected,cert['pairs'],records),'full five-section complex concurrence'))
    return {'status':'PASS','positive_collision_graphs':[[147,651,3],[108,432,3]],'corruptions_rejected':rejected}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);args=p.parse_args();print(json.dumps(run(args.certificate),sort_keys=True,indent=2))
