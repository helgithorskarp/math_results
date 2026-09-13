#!/usr/bin/env python3
"""Collision, colouring, fiber-coverage and concurrence corruption controls."""
import argparse,copy,importlib.util,itertools,json
from pathlib import Path
from interface import A,HERE,build,selection,pair_interface,physical,colour_word
import direct
spec=importlib.util.spec_from_file_location('binomial_main_verifier',HERE/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
def reject(name,fn,expected):
    try:fn()
    except ValueError as e:
        A.need(expected in str(e),'wrong rejection for '+name+': '+str(e));return name
    raise ValueError('corruption accepted: '+name)
def run(path):
    cert=json.loads(Path(path).read_text());factors,_,_,buckets,_=build();V.initialize(factors)
    selected,pairs=pair_interface(selection(buckets),buckets)
    samples=[next(c for c in cert['components'] if c.get('point_count')==n and c.get('edge_count')==e) for n,e in [(129,195),(162,189),(162,219),(27,63)]]
    positive=samples[0];bounds=[]
    for c in samples:
        V.check_field(c);plain=physical.graph(c);cached=direct.graph(c)
        A.need(plain==cached[:4],'complete literal/cache graph alignment')
        if c['point_count']==27:continue
        points,labels,edges,triangle=plain;good=[]
        for tail in itertools.product(range(3),repeat=4):
            w=[1]+list(tail)
            try:word=colour_word(w,labels,len(points));physical.check_word(word,len(points),edges)
            except ValueError:continue
            good.append(w)
        A.need(good and not any(all(w) for w in good),'zero positional weight necessary in this witness family')
        bounds.append({'points':len(points),'edges':len(edges),'all_normalized_weights':81,'valid_weights':good,'all_nonzero_valid_weights':0})
    rejected=[]
    bad=copy.deepcopy(positive);bad['real_embeddings']+=1
    rejected.append(reject('alter_real_root_count',lambda:V.check_field(bad),'real embedding count'))
    bad=copy.deepcopy(positive);bad['colour_weights']=[1,1,1,1,1]
    rejected.append(reject('break_collision_colour',lambda:V.check_field(bad),'colour descends through collisions'))
    bad=copy.deepcopy(positive);bad['edge_count']-=1
    rejected.append(reject('omit_physical_unit_edge',lambda:V.check_field(bad),'physical graph counts'))
    bad=copy.deepcopy(positive);bad['active_curves']=bad['active_curves'][:-1]
    rejected.append(reject('omit_active_event',lambda:V.check_field(bad),'all active norm events'))
    records={c['key']:copy.deepcopy(c) for c in cert['components']}
    row=next(r for r in cert['pairs'] if positive['key'] in r['components']);a,b=row['pair'];cc=[records[k] for k in row['components'] if k!=positive['key']]
    rejected.append(reject('omit_algebraic_component',lambda:V.fiber_audit(((a,b),factors[a],factors[b],cc)),'complete square-free fiber coverage'))
    idx,domains,pp=selected[0];source=next(r for r in cert['pairs'] if tuple(r['pair'])==pp[0]);key=source['components'][0]
    records[key]['active_curves']=sorted(set(records[key]['active_curves'])|{d[0] for d in domains})
    rejected.append(reject('invent_full_pencil_concurrence',lambda:V.concurrency(selected,cert['pairs'],records),'full five-section complex concurrence'))
    return {'status':'PASS','literal_cache_graph_comparisons':[[c['point_count'],c['edge_count']] for c in samples],'zero_weight_boundaries':bounds,'corruptions_rejected':rejected}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.certificate),sort_keys=True,indent=2))
