#!/usr/bin/env python3
"""Check a positive second corona and an all-real two-extension obstruction.

Five complete full-mate inventories, rationally buffered whole overlaps,
three older-point corner censuses and a replayed fan lemma validate each
of33 sparse clauses. Elementary unit propagation proves contradiction.
No discovery inventory, native encoder/solver or proof trace is imported.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python with assertions enabled; -O is unsupported')
import geometry as g

HERE=Path(__file__).resolve().parent
TILE_KEYS=('amplitude','prototype_axial_vertices','counterclockwise_vertex_cycle',
           'ports_counterclockwise','states')
TILE_SHA256='2a2ae3afa27d33c83d3fdd4a59bcf46d69839e575f81723e47493985af034d02'
ROOT=(0,0,0,0)

def same_clause(actual,expected):
    assert len(actual)==len(set(actual)), 'Duplicate literal'
    assert Counter(actual)==Counter(expected), 'Clause does not match its complete geometric premise'

def positive(data):
    old=tuple(map(tuple,data['first_prefix']))
    rows=data['witness']
    assert tuple(tuple(r['pose']) for r in rows if r['level']<=1)==old
    assert len(old)==12 and old[0]==ROOT
    assert set(r['level'] for r in rows)=={0,1,2}
    networks=[]
    previous=(ROOT,)
    for level in (1,2):
        poses=tuple(tuple(r['pose']) for r in rows if r['level']<=level)
        assert len(poses)==len(set(poses))
        outside,network=g.network_check(poses)
        g.strict_check(previous,poses,outside)
        prior_level=[tuple(r['pose']) for r in rows if r['level']==level-1]
        previous_points={g.image(v,p) for p in prior_level for v in g.V}
        for r in rows:
            if r['level']==level:
                assert previous_points & {g.image(v,tuple(r['pose'])) for v in g.V}
        networks.append(network)
        previous=poses
    assert [r['copies'] for r in networks]==[12,43]
    return networks

def run(data,certificate):
    assert g.canonical_hash({k:data[k] for k in TILE_KEYS})==TILE_SHA256, 'Wrong nominal quartic tile'
    first=tuple(map(tuple,data['first_prefix']))
    assert data['negative_old_indices']==[3,4,5,6], 'Wrong four-copy footprint'
    old=tuple(first[i] for i in data['negative_old_indices'])
    assert old==((1,1,8,1),(1,2,7,2),(1,3,6,2),(1,4,-1,1))
    poses=tuple(map(tuple,data['variable_poses']))
    assert len(poses)==len(set(poses))==certificate['variables']==32
    assert list(poses)==sorted(poses) and not set(poses)&set(old)
    for p in poses:
        assert p[:2] in g.MATRICES and all(isinstance(z,int) for z in p)
        assert not any(g.overlap(g.quad(p),g.quad(q)) for q in old)
    ids={p:i+1 for i,p in enumerate(poses)}
    old_points={g.image(v,p) for p in old for v in g.V}
    kinds=Counter();covers=[];corner_cases=[];clauses=[];fan=None
    for c in certificate['clauses']:
        clause=c['clause'];kind=c['kind'];kinds[kind]+=1
        assert all(isinstance(v,int) and 1<=abs(v)<=len(poses) for v in clause)
        if kind=='complete-charged-cover':
            assert c['owner'] in data['negative_old_indices']
            edge=g.target_edge(first[c['owner']],c['port'])
            raw,pool=g.mates(edge,old)
            assert all(p in ids for p in pool), 'Missing a possible owner from the sparse table'
            same_clause(clause,[ids[p] for p in pool])
            covers.append({'owner':c['owner'],'port':c['port'],'raw':len(raw),
                           'retained':len(pool),'owner_poses_sha256':g.canonical_hash(pool)})
        elif kind=='whole-overlap':
            assert len(clause)==2 and all(v<0 for v in clause)
            p,q=(poses[-v-1] for v in clause)
            assert p!=q and g.overlap(g.quad(p),g.quad(q),True), 'Not a buffered whole overlap'
        elif kind=='older-point-gap':
            point=tuple(c['point'])
            assert point in old_points, 'An added B provider must be forced at a point of the older prefix'
            antecedent=c['antecedent_ids']
            assert antecedent==sorted(set(antecedent))
            fixed=[p for p in old if g.sector(point,p)]
            selected=[poses[i-1] for i in antecedent]
            assert all(g.sector(point,p) for p in selected), 'Unused or nonincident antecedent'
            assert c['angle_degrees'] in (60,90)
            census=g.audit(point,fixed+selected,c['start_ray'],c['angle_degrees']//30)
            assert all(len(partition)==1 for partition in census['accepted'])
            allowed=sorted({ids[part[0]] for part in census['accepted']})
            assert c['allowed_ids']==allowed
            same_clause(clause,[-i for i in antecedent]+allowed)
            corner_cases.append({'point':point,'angle_degrees':c['angle_degrees'],
                                 'antecedent_ids':antecedent,'allowed_ids':allowed,
                                 'geometric_trials':len(census['tested']),
                                 'external_states':census['external_states']})
        elif kind=='fan-interiority':
            assert fan is None
            fan=g.verify_six_fan()
            same_clause(clause,[-ids[p] for p in fan['poses']])
        else:raise AssertionError('Unknown mathematical clause kind')
        clauses.append(clause)
    assert kinds==Counter({'complete-charged-cover':5,'whole-overlap':24,
                          'older-point-gap':3,'fan-interiority':1})
    assert len(clauses)==33 and [c['retained'] for c in covers]==[1,9,5,1,16]
    refutation=g.unit_refutation(clauses)
    return {
        'agent':'six-heesch-3','role':'researcher',
        'status':'EXACT_CORE_AND_GEOMETRY_CHECKED_WITH_WRITTEN_CONTACT_BRIDGES',
        'negative_old_indices':data['negative_old_indices'],
        'negative_old_poses':old,
        'positive_prefixes':positive(data),
        'complete_charged_covers':covers,
        'older_point_corner_cases':corner_cases,
        'variables':len(poses),'clauses':len(clauses),'clause_kinds':dict(kinds),
        'clauses_sha256':g.canonical_hash(clauses),
        'variable_poses_sha256':g.canonical_hash(poses),
        'unit_refutation':refutation,
        'replayed_fan':{'poses':fan['poses'],'raw_mates':fan['raw_mates'],
                        'retained_mates':fan['retained_mates'],'cover_sizes':fan['cover_sizes'],
                        'whole_overlap_pairs':fan['whole_overlap_pairs'],
                        'pool_sha256':fan['pool_sha256'],
                        'forced_filler_interiority_required':False},
        'claim':'No finite real B,D contain the specified four copies Z with union(Z) inside int(union(B)) and union(B) inside int(union(D)). The containing first12 admits the checked43-copy second corona, but no third corona starts with that first prefix.',
        'scope':'One transportable four-copy two-stage pattern; all translations/rotations/reflections and arbitrary topology/contact for B,D. Four is the support of this certificate, not a universal minimum obstruction size. Global4<=Hc(T)<=Hh(T)<=85 is inherited and unchanged; no exact Heesch value or finite-seven construction.'}

def controls(data,certificate):
    cases=[]
    changed=copy.deepcopy(data);changed['negative_old_indices'].remove(6)
    cases.append(('missing_fourth_old_copy',changed,copy.deepcopy(certificate)))
    changed=copy.deepcopy(data);changed['amplitude']='1/101'
    cases.append(('wrong_amplitude',changed,copy.deepcopy(certificate)))
    bad=copy.deepcopy(certificate)
    next(c for c in bad['clauses'] if c['kind']=='complete-charged-cover' and len(c['clause'])==16)['clause'].pop()
    cases.append(('truncated_complete_cover',copy.deepcopy(data),bad))
    bad=copy.deepcopy(certificate)
    next(c for c in bad['clauses'] if c['kind']=='older-point-gap' and c['angle_degrees']==60)['point']=[-8,9]
    cases.append(('selected_only_point_as_older',copy.deepcopy(data),bad))
    results=[]
    for name,d,c in cases:
        try:run(d,c)
        except (AssertionError,KeyError,ValueError) as exc:
            results.append({'control':name,'rejected':True,'reason':str(exc)})
        else:raise AssertionError('Malformed control accepted: '+name)
    return results

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected',type=Path)
    ap.add_argument('--controls',action='store_true')
    args=ap.parse_args()
    data=json.loads((HERE/'input.json').read_text())
    certificate=json.loads((HERE/'certificate.json').read_text())
    result=json.loads(json.dumps(run(data,certificate)))
    if args.expected:assert result==json.loads(args.expected.read_text()), 'Expected report differs'
    if args.controls:result['controls']=controls(data,certificate)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
