#!/usr/bin/env python3
"""Check a necessary first-prefix cover, not a census of complete coronas.

Exact geometric premises and a small RUP refutation are replayed separately
from the private adaptive SAT search. Published prior lemmas are byte pinned.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('Assertions are required by the pinned geometric dependencies; -O is unsupported')

import geometry as g

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
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

def dependencies(data):
    pins=json.loads((HERE/'dependency_pins.json').read_text())
    for path,digest in pins.items():
        require(hashlib.sha256((REPO/path).read_bytes()).hexdigest()==digest,'Changed dependency: '+path)
    parent=load_module('prior_four_coronas',REPO/'heesch_trapezoid_four_coronas/check.py')
    triple=load_module('prior_two_coronas',REPO/'heesch_trapezoid_two_coronas/check.py')
    old_geometry=load_module('prior_four_geometry',REPO/'heesch_trapezoid_four_copy_obstruction/geometry.py')
    saved=sys.modules.get('geometry')
    sys.modules['geometry']=old_geometry
    try:
        four=load_module('prior_four_copy',REPO/'heesch_trapezoid_four_copy_obstruction/check.py')
    finally:
        sys.modules['geometry']=saved
    tile_fields=('amplitude','prototype_axial_vertices','counterclockwise_vertex_cycle','ports_counterclockwise','states')
    four_data=json.loads((REPO/'heesch_trapezoid_four_copy_obstruction/input.json').read_text())
    for source in (parent.DATA,triple.DATA,four_data,g.DATA):
        for field in tile_fields:require(canonical(source[field])==canonical(data[field]),'Different physical tile in a dependency')
    require(data['amplitude']=='1/100','Wrong nominal amplitude')
    tip=parent.verify_tip()
    root90=parent.verify_root90()
    caps=parent.verify_two_caps()
    prior_four=four.run(four_data,json.loads((REPO/'heesch_trapezoid_four_copy_obstruction/certificate.json').read_text()))
    return parent,triple,{'tip':tip,'root90':root90,'two_caps':caps,
                         'four_copy':prior_four,'pins':pins}

def inverse(p):
    matches=[]
    for h,k in g.MATRICES:
        t=g.image(p[2:],(h,k,0,0))
        q=(h,k,-t[0],-t[1])
        if g.compose(q,p)==ROOT:matches.append(q)
    require(len(matches)==1,'Inverse is not unique')
    q=matches[0]
    require(g.compose(p,q)==ROOT,'Wrong right inverse')
    return q

def angle_partitions(width):
    if not width:return [()]
    result=[]
    for angle in (2,3,4,6):
        if angle<=width:
            result += [(angle,)+tail for tail in angle_partitions(width-angle)]
    return result

def audit_gap(point,start,width,incident,blockers):
    require(width in range(1,8),'Unsupported angle gap')
    occupied=set()
    for p in incident:
        sector=g.sector(point,p)
        require(bool(sector) and not occupied&sector,'Invalid incident sectors')
        occupied |= sector
    require((start,width) in g.gaps(occupied),'Claimed gap is not an actual angular gap')
    if width==1:return [],0
    radial=g.radial(point,incident)
    ends=(start,(start+width)%12)
    require(all(len(radial[r])==1 for r in ends),'Ambiguous gap boundary')
    external={r:radial[r][0] for r in ends}
    require(any(external[r][1] for r in ends),'Unlicensed flat phase discretization')
    accepted=[];trials=0
    for sizes in angle_partitions(width):
        cursor=start;pools=[]
        for size in sizes:
            pools.append(g.fitted(point,cursor,size));cursor+=size
        for poses in product(*pools):
            trials+=1
            seams=g.radial(point,poses)
            if not all(len(seams[r])==1 and g.compatible(external[r],seams[r][0]) for r in ends):continue
            if not all(len(rows)==2 and g.compatible(*rows) for r,rows in seams.items() if r not in ends):continue
            bad=False
            for i,p in enumerate(poses):
                for q in poses[:i]+tuple(blockers):
                    if g.overlap(g.quad(p),g.quad(q),True):bad=True
            if not bad:accepted.append(poses)
    return sorted(set(accepted)),trials

def automorphisms():
    # Unique 60/120-degree corners must be fixed. Their midpoint is the
    # origin, leaving only identity or reflection in their common line.
    require(len(g.sector(g.V[1],ROOT))==2 and len(g.sector(g.V[2],ROOT))==4,'Wrong distinguished corners')
    potential=[(h,k,0,0) for h,k in g.MATRICES
               if g.image(g.V[1],(h,k,0,0))==g.V[1] and g.image(g.V[2],(h,k,0,0))==g.V[2]]
    require(len(potential)==2,'Wrong fixed-line isometries')
    corners={g.V[i] for i in (1,2,16,17)}
    remaining=[p for p in potential if {g.image(v,p) for v in corners}==corners]
    require(remaining==[ROOT],'Physical automorphism is not the identity')
    return {'fixed_corner_isometries':potential,'automorphisms':remaining}

def strip_cap(pattern,triple):
    old=tuple(map(tuple,pattern['poses']))
    expected=((0,5,1,-1),(0,5,3,-1),(0,5,5,-1),(1,2,7,-9))
    require(old==expected and pattern['required_future_surrounds']==2,'Wrong strip-cap hypothesis')
    for i,p in enumerate(old):
        for q in old[:i]:require(not g.overlap(g.quad(p),g.quad(q)),'Overlapping old footprints')
    raw,retained=g.mates(g.target_edge(old[3],1),old)
    require(len(raw)==16 and retained==[(0,4,8,-9)],'Incomplete strip-cap mate census')
    forced=[g.forced_ninety(point,old) for point in ((9,-8),(11,-8))]
    require(forced==[((1,2,16,-16),2),((1,2,18,-16),2)],'Wrong old-point forces')
    providers=tuple(retained+[p for p,n in forced])
    obstruction=triple.pattern_check(providers)
    require(obstruction['raw_mates']==66 and obstruction['retained_mates']==19,
            'Different imported three-copy obstruction')
    return {'old':old,'charged_owner':3,'charged_port':1,'raw_mates':len(raw),
            'retained_mates':retained,'protected_old_points':[(9,-8),(11,-8)],
            'corner_trials':[n for p,n in forced],'forced_B_copies':providers,
            'second_stage_three_copy_check':obstruction,
            'logical_core':[[1],[2],[3],[-1,-2,-3]]}

def propagate(clauses,initial=()):
    assignments={}
    for literal in initial:
        v=abs(literal);value=literal>0
        if v in assignments and assignments[v]!=value:return True
        assignments[v]=value
    while True:
        unit=None
        for clause in clauses:
            if any(assignments.get(abs(v))==(v>0) for v in clause if abs(v) in assignments):continue
            rest=[v for v in clause if abs(v) not in assignments]
            if not rest:return True
            if len(rest)==1:unit=rest[0];break
        if unit is None:return False
        assignments[abs(unit)]=unit>0

def check_rup(clauses,path,variables):
    current=[list(row) for row in clauses]
    additions=deletions=0;empty=False
    for line in path.read_text().splitlines():
        words=line.split()
        if not words:continue
        deletion=words[0]=='d'
        if deletion:words=words[1:]
        values=list(map(int,words))
        require(values and values[-1]==0 and 0 not in values[:-1],'Malformed RUP line')
        row=values[:-1]
        require(all(1<=abs(v)<=variables for v in row),'Out-of-domain proof variable')
        if deletion:
            key=frozenset(row)
            match=next((i for i,c in enumerate(current) if frozenset(c)==key),None)
            require(match is not None,'Deleting an unknown proof clause')
            current.pop(match);deletions+=1
        else:
            require(propagate(current,[-v for v in row]),'A proof addition is not RUP')
            current.append(row);additions+=1
            if not row:empty=True
    require(empty,'Proof does not derive the empty clause')
    return {'answer':'UNSAT','RUP_additions':additions,'deletions':deletions,
            'proof_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def run(data,certificate):
    parent,triple,prior=dependencies(data)
    require(tuple(data['root'])==ROOT,'Wrong normalized central copy')
    poses=tuple(map(tuple,data['candidate_poses']))
    require(all(len(p)==4 and p[:2] in g.MATRICES and all(type(v) is int for v in p) for p in poses),
            'Pose coordinates and orientation codes must be exact integers')
    require(len(poses)==certificate['variables']==110 and len(set(poses))==110 and ROOT not in poses,'Invalid pose variables')
    identifiers={p:i+1 for i,p in enumerate(poses)}
    patterns=data['patterns']
    require(patterns['fan_four']['required_future_surrounds']==2,'Wrong fan generation guard')
    require(patterns['signed120']['required_future_surrounds']==patterns['two_caps']['required_future_surrounds']==1,'Wrong one-stage guards')
    require(tuple(map(tuple,patterns['two_caps']['poses']))==tuple(map(tuple,prior['two_caps']['poses'])),'Wrong imported cap motif')
    imported_fan=json.loads((REPO/'heesch_trapezoid_four_copy_obstruction/input.json').read_text())
    imported_poses=[imported_fan['first_prefix'][i] for i in imported_fan['negative_old_indices']]
    require(patterns['fan_four']['poses']==imported_poses,'Wrong imported four-copy motif')
    signed=tuple(map(tuple,patterns['signed120']['poses']))
    require(signed==(ROOT,(1,4,0,-1)) and not g.audit((0,-1),signed)['accepted'],'Wrong signed120 motif')
    new=strip_cap(patterns['strip_cap'],triple)
    auto=automorphisms()
    subsets=data['necessary_subsets']
    require(len(subsets)==115 and len({tuple(s) for s in subsets})==115,'Invalid necessary subset family')
    root_raw,_=g.mates(g.target_edge(ROOT,2),(ROOT,))
    survivors={tuple(p) for p in prior['tip']['two_corona_survivors']}
    excluded=root_raw-survivors
    require(len(excluded)==15,'Wrong imported root-tip exclusions')
    positive_edges={p:{tuple(sorted((a,b))) for a,b,port,s in g.chords(p) if s==1} for p in poses}
    records=certificate['records'];clauses=[];gap_trials=0
    for r in records:
        row=r['clause'];kind=r['kind']
        require(len(set(row))==len(row) and all(1<=abs(v)<=len(poses) for v in row),'Malformed clause')
        if kind=='charged-cover':
            raw,retained=g.mates(g.target_edge(ROOT,r['port']),(ROOT,))
            require(all(p in identifiers for p in retained),'Missing full charged mate')
            require(set(row)=={identifiers[p] for p in retained},'Truncated complete charged cover')
        elif kind=='whole-overlap':
            require(len(row)==2 and all(v<0 for v in row),'Wrong overlap clause')
            require(g.overlap(g.quad(poses[-row[0]-1]),g.quad(poses[-row[1]-1]),True),'No buffered whole overlap')
        elif kind=='positive-interface-overlap':
            require(len(row)==2 and all(v<0 for v in row),'Wrong positive-overlap clause')
            require(bool(positive_edges[poses[-row[0]-1]]&positive_edges[poses[-row[1]-1]]),'No common positive unit arc')
        elif kind=='published-root-tip-exclusion':
            require(len(row)==1 and row[0]<0 and poses[-row[0]-1] in excluded,'Wrong imported mate exclusion')
        elif kind=='interior-pattern':
            spec=patterns[r['pattern']]
            require(r['required_future_surrounds']==spec['required_future_surrounds'],'Wrong number of future surrounds')
            absolute=tuple(map(tuple,spec['poses']));normal=inverse(absolute[0])
            expected=tuple(g.compose(tuple(r['anchor']),g.compose(normal,p)) for p in absolute)
            require(expected==tuple(map(tuple,r['poses'])),'Wrong common-isometry transport')
            require(all(p==ROOT or p in identifiers for p in expected),'Missing transported variable')
            require(set(row)=={-identifiers[p] for p in expected if p!=ROOT},'Wrong forbidden-conjunction clause')
        elif kind=='conditional-root-point-gap':
            point=tuple(r['point']);start,width=r['start_ray'],r['width']
            require(point in g.V,'Gap is not at an OLD root point')
            antecedent=set(r['antecedent_ids']);incident_ids=set(r['incident_ids'])
            require(incident_ids<=antecedent and {-v for v in row if v<0}==antecedent,'Wrong conditional antecedent')
            incident=(ROOT,)+tuple(poses[i-1] for i in sorted(incident_ids))
            blockers=(ROOT,)+tuple(poses[i-1] for i in sorted(antecedent))
            require(all(bool(g.sector(point,poses[i-1]))==(i in incident_ids) for i in antecedent),'Incorrect incident inventory')
            accepted,trials=audit_gap(point,start,width,incident,blockers);gap_trials+=trials
            positive={poses[v-1] for v in row if v>0}
            require(all(positive&set(partition) for partition in accepted),'A complete gap partition escapes the clause')
        elif kind=='enumeration-blocker':
            subset=subsets[r['subset_index']]
            require(set(row)=={-i for i in subset},'Wrong subset-avoidance clause')
        else:raise ValueError('Unknown geometric clause kind: '+kind)
        clauses.append(row)
    require(len(records)==501,'Wrong compact core size')
    logical=check_rup(clauses,HERE/'proof.rup',len(poses))
    witness=data['positive_four_corona_witness']
    all_poses=tuple(tuple(r['pose']) for r in witness);levels=[r['level'] for r in witness]
    require(Counter(levels)==Counter({0:1,1:11,2:33,3:49,4:53}) and levels==sorted(levels),'Wrong positive fixture')
    old=all_poses[:1];positive_metrics=[]
    for depth in range(1,5):
        prefix=all_poses[:sum(r<=depth for r in levels)]
        outside,metric=g.network_check(prefix);g.strict_check(old,prefix,outside)
        endpoints=[{g.image(v,p) for v in g.V} for p in prefix]
        for i in range(len(old),len(prefix)):
            require(any(levels[j]==depth-1 and endpoints[i]&endpoints[j] for j in range(len(old))),'New copy misses previous corona')
        positive_metrics.append(metric);old=prefix
    first={all_poses[i] for i,level in enumerate(levels) if level<=1}
    truth={i for p,i in identifiers.items() if p in first}
    for r in records:
        if r['kind']=='enumeration-blocker':continue
        require(any((v>0)==(abs(v) in truth) for v in r['clause']),'Positive first prefix violates a geometric premise')
    hits=[i for i,s in enumerate(subsets) if set(s)<=truth]
    require(bool(hits),'The known four-corona first prefix escapes the necessary cover')
    return {'agent':'six-heesch-3','role':'researcher','claim':'Every first cumulative prefix of at least three strict coronas contains the root and one of 115 specified necessary subsets.',
            'variables':len(poses),'compact_clauses':len(clauses),'clause_kinds':dict(Counter(r['kind'] for r in records)),
            'necessary_subsets':len(subsets),'new_strip_cap_two_stage':new,'automorphism_check':auto,
            'checked_root_gap_trials':gap_trials,'logical_refutation':logical,
            'positive_four_coronas':positive_metrics,'positive_first_subset_indices':hits,
            'input_sha256':canonical(data),'certificate_sha256':canonical(certificate),
            'trust_boundary':'Exact Python and byte-pinned published geometry/proofs; written atomic contact, buffered overlap, finite-angle phase locking and network isotopy. No formalization or independent reviewer verdict. Subsets need not be complete coronas.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    data=json.loads((HERE/'input.json').read_text())
    certificate=json.loads((HERE/'certificate.json').read_text())
    result=run(data,certificate)
    if args.expected:require(canonical(result)==canonical(json.loads(args.expected.read_text())),'Expected output differs')
    print(json.dumps(result,indent=2))
    if args.controls:
        controls=[]
        changed=copy.deepcopy(data);changed['amplitude']='1/101'
        controls.append(('wrong_amplitude',changed,certificate))
        changed=copy.deepcopy(certificate)
        next(r for r in changed['records'] if r['kind']=='charged-cover')['clause'].pop()
        controls.append(('truncated_complete_cover',data,changed))
        changed=copy.deepcopy(certificate)
        next(r for r in changed['records'] if r['kind']=='conditional-root-point-gap')['point']=[-9,6]
        controls.append(('selected_only_point_as_old',data,changed))
        changed=copy.deepcopy(data);changed['patterns']['strip_cap']['required_future_surrounds']=1
        controls.append(('wrong_future_generation',changed,certificate))
        changed=copy.deepcopy(data);changed['candidate_poses'][1]=changed['candidate_poses'][0]
        controls.append(('duplicate_physical_pose',changed,certificate))
        outcomes=[]
        for name,changed_data,changed_certificate in controls:
            try:run(changed_data,changed_certificate)
            except (ValueError,AssertionError) as error:
                outcomes.append({'control':name,'rejected':True,'reason':str(error)})
            else:raise ValueError('Malformed control accepted: '+name)
        print(json.dumps({'controls':outcomes},indent=2))

if __name__=='__main__':main()
