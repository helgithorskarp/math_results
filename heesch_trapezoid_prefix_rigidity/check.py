#!/usr/bin/env python3
"""Check15 first surrounds and100 exclusions, then apply the written rigidity proof.

Standard library only. Prior proof/source dependencies are byte pinned;
native discovery, dense formulas, solver verdicts and saved inventories
are not inputs of this reader.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('Assertions are required by pinned dependencies; -O is unsupported')

HERE=Path(__file__).resolve().parent
ROOT=(0,0,0,0)

def require(condition,message):
    if not condition:raise ValueError(message)

def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def context(repo):
    pins=json.loads((HERE/'dependency_pins.json').read_text())
    for path,digest in pins.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'Changed dependency: '+path)
    directory=repo/'heesch_trapezoid_first_prefix_reduction'
    geometry=load_module('published_prefix_geometry',directory/'geometry.py')
    saved=sys.modules.get('geometry')
    sys.modules['geometry']=geometry
    try:
        parent=load_module('published_prefix_reader',directory/'check.py')
    finally:
        if saved is None:sys.modules.pop('geometry',None)
        else:sys.modules['geometry']=saved
    data=json.loads((directory/'input.json').read_text())
    report=parent.run(data,json.loads((directory/'certificate.json').read_text()))
    require(parent.canonical(report)==parent.canonical(json.loads((directory/'expected.json').read_text())),
            'The pinned115-subset premise does not replay')
    return parent,geometry,data,report,pins

def check_rup(parent,clauses,additions,variables):
    current=[list(row) for row in clauses]
    require(bool(additions) and additions[-1]==[],'No final empty clause')
    for row in additions:
        require(isinstance(row,list) and all(type(v) is int and 1<=abs(v)<=variables for v in row),
                'Malformed proof literal')
        require(parent.propagate(current,[-v for v in row]),'Addition is not RUP')
        current.append(row)
    return len(additions)

def run(data,certificate,ctx):
    parent,g,prior,prior_report,pins=ctx
    require(tuple(data['root'])==ROOT,'Wrong normalized root')
    require(data['required_surrounds_of_subset']==2,'Two further strict surrounds are required')
    require(data['signed120_required_future_surrounds']==1,'Wrong imported pair guard')
    poses=tuple(map(tuple,data['candidate_poses']))
    require(len(poses)==156 and len(set(poses))==156 and ROOT not in poses,'Duplicate or wrong pose table')
    require(all(len(p)==4 and p[:2] in g.MATRICES and all(type(x) is int for x in p) for p in poses),
            'Poses must be exact integral-D6 codes')
    identifiers={p:i+1 for i,p in enumerate(poses)}
    cases=certificate['cases']
    excluded=[case['subset_index'] for case in cases]
    remaining=data['remaining_subset_indices']
    require(len(cases)==len(set(excluded))==100 and len(remaining)==len(set(remaining))==15,
            'Wrong branch counts')
    require(set(excluded).isdisjoint(remaining) and set(excluded)|set(remaining)==set(range(115)),
            'The115 branches are not all accounted for')
    require(excluded==sorted(excluded) and remaining==sorted(remaining),'Noncanonical branch order')
    subsets=prior['necessary_subsets']
    first_poses=tuple(map(tuple,prior['candidate_poses']))
    positives={p:{tuple(sorted((a,b))) for a,b,j,s in g.chords(p) if s==1} for p in poses}
    kind_count=Counter()
    trials=0
    additions=0
    case_reports=[]
    for case in cases:
        index=case['subset_index']
        old=(ROOT,)+tuple(first_poses[v-1] for v in subsets[index])
        old_set=set(old)
        old_points={g.image(v,p) for p in old for v in g.V}
        used={abs(v) for r in case['records'] for v in r['clause']}
        used|={abs(v) for r in case['rup_additions'] for v in r}
        require(all(1<=v<=len(poses) for v in used),'Out-of-domain Boolean variable')
        require(not ({poses[v-1] for v in used}&old_set),'A variable duplicates a fixed copy')
        clauses=[]
        for record in case['records']:
            row=record['clause']
            kind=record['kind']
            require(len(set(row))==len(row) and all(type(v) is int and 1<=abs(v)<=len(poses) for v in row),
                    'Malformed initial clause')
            if kind=='charged-cover':
                owner,port=record['owner'],record['port']
                require(type(owner) is int and 0<=owner<len(old) and type(port) is int and 0<=port<17,
                        'Invalid charged owner/port')
                raw,retained=g.mates(g.target_edge(old[owner],port),old)
                require(not (raw&old_set),'The charged target is already covered internally')
                require(all(p in identifiers for p in retained),'Omitted possible full charged mate')
                require(set(row)=={identifiers[p] for p in retained},'Truncated full charged cover')
            elif kind=='whole-overlap':
                require(len(row)==2 and all(v<0 for v in row),'Wrong whole-overlap clause')
                require(g.overlap(g.quad(poses[-row[0]-1]),g.quad(poses[-row[1]-1]),True),
                        'No buffered whole overlap')
            elif kind=='positive-interface-overlap':
                require(len(row)==2 and all(v<0 for v in row),'Wrong positive-arc clause')
                require(bool(positives[poses[-row[0]-1]]&positives[poses[-row[1]-1]]),'No common positive unit arc')
            elif kind=='interior-pattern':
                require(record['pattern']=='signed120' and record['required_future_surrounds']==1,
                        'Wrong pair or future-interiority guard')
                specification=prior['patterns']['signed120']
                absolute=tuple(map(tuple,specification['poses']))
                normal=parent.inverse(absolute[0])
                images=tuple(g.compose(tuple(record['anchor']),g.compose(normal,p)) for p in absolute)
                require(images==tuple(map(tuple,record['poses'])),'Incorrect pair transport')
                require(all(p in old_set or p in identifiers for p in images),'Missing pair variable')
                require(set(row)=={-identifiers[p] for p in images if p not in old_set},'Wrong forbidden pair clause')
            elif kind=='conditional-older-point-gap':
                point=tuple(record['point'])
                require(point in old_points,'Point is not on a fixed OLD copy')
                antecedent=set(record['antecedent_ids'])
                incident_ids=set(record['incident_ids'])
                require(incident_ids<=antecedent and all(1<=v<=len(poses) for v in antecedent),
                        'Wrong conditional gap antecedent')
                require({-v for v in row if v<0}==antecedent,'Wrong negative gap literals')
                fixed=tuple(p for p in old if g.sector(point,p))
                incident=fixed+tuple(poses[v-1] for v in sorted(incident_ids))
                blockers=old+tuple(poses[v-1] for v in sorted(antecedent))
                require(all(bool(g.sector(point,poses[v-1]))==(v in incident_ids) for v in antecedent),
                        'Incorrect local incident inventory')
                accepted,count=parent.audit_gap(point,record['start_ray'],record['width'],incident,blockers)
                trials+=count
                positive={poses[v-1] for v in row if v>0}
                require(all(positive&set(partition) for partition in accepted),'A full corner partition escapes')
            else:
                raise ValueError('Unknown geometric clause: '+kind)
            clauses.append(row)
            kind_count[kind]+=1
        n=check_rup(parent,clauses,case['rup_additions'],len(poses))
        additions+=n
        case_reports.append({'subset_index':index,'clauses':len(clauses),'variables':len(used),'RUP_additions':n})
    require(sum(kind_count.values())==962 and additions==168,'Wrong compact proof totals')
    surrounds=[]
    families=[]
    for index in remaining:
        family=(ROOT,)+tuple(first_poses[v-1] for v in subsets[index])
        outside,metric=g.network_check(family)
        g.strict_check((ROOT,),family,outside)
        root_points=set(g.V)
        require(all(root_points&{g.image(v,p) for v in g.V} for p in family[1:]),
                'A first-corona copy does not touch the root')
        families.append(frozenset(family))
        surrounds.append({'subset_index':index,**metric})
    require(len(set(families))==15,'Duplicate first surrounds')
    require(all(not a<b for a in families for b in families),'One strict root surround extends another')
    require(prior_report['positive_first_subset_indices']==[0] and 0 in remaining,
            'Known four-corona positive control was pruned')
    return {'agent':'six-heesch-3','role':'researcher',
            'claim':'In every H-corona packing with H>=3, the first prefix is one of15 specified disc surrounds and prefixes through H-2 are integral-D6 aligned after root normalization.',
            'scope':'The exact-first assertion uses the corona neighbor condition. In arbitrary three-strict-surround chains only the root-neighbor subfamily is classified; unrelated copies remain free.',
            'excluded_subsets':excluded,'first_surrounds':surrounds,'pose_variables':len(poses),
            'clauses':sum(kind_count.values()),'clause_kinds':dict(kind_count),
            'checked_older_gap_trials':trials,'RUP_additions':additions,'case_reports':case_reports,
            'parent_replay':{'subsets':prior_report['necessary_subsets'],'clauses':prior_report['compact_clauses'],
                             'RUP_additions':prior_report['logical_refutation']['RUP_additions'],
                             'positive_four_coronas':prior_report['positive_four_coronas']},
            'input_sha256':canonical(data),'certificate_sha256':canonical(certificate),
            'trust_boundary':'Exact Python and byte-pinned published geometry/proofs; written atomic contact, buffered overlap, finite-angle locking, network isotopy, contact-interiority and rerooting induction. No formalization or independent reviewer verdict. Last two prefixes remain unrestricted.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=HERE.parent)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    ctx=context(args.repo_root)
    data=json.loads((HERE/'input.json').read_text())
    certificate=json.loads((HERE/'certificate.json').read_text())
    result=run(data,certificate,ctx)
    if args.expected:
        require(canonical(result)==canonical(json.loads(args.expected.read_text())),'Expected output differs')
    print(json.dumps(result,indent=2))
    if args.controls:
        controls=[]
        changed=copy.deepcopy(certificate)
        next(r for case in changed['cases'] for r in case['records'] if r['kind']=='charged-cover')['clause'].pop()
        controls.append(('truncated_full_cover',data,changed))
        changed=copy.deepcopy(certificate);changed['cases'].pop()
        controls.append(('omitted_branch',data,changed))
        changed=copy.deepcopy(certificate)
        next(r for case in changed['cases'] for r in case['records'] if r['kind']=='conditional-older-point-gap')['point']=[999,999]
        controls.append(('selected_only_point_as_old',data,changed))
        changed=copy.deepcopy(data);changed['required_surrounds_of_subset']=1
        controls.append(('discarded_second_surround',changed,certificate))
        changed=copy.deepcopy(certificate)
        next(case for case in changed['cases'] if case['subset_index']==4)['rup_additions']=[[]]
        controls.append(('false_empty_RUP',data,changed))
        for name,bad_data,bad_certificate in controls:
            try:run(bad_data,bad_certificate,ctx)
            except (ValueError,AssertionError):
                print(json.dumps({'control':name,'status':'rejected'}))
            else:raise AssertionError('Malformed control accepted: '+name)

if __name__=='__main__':main()
