#!/usr/bin/env python3
"""Ten freshly re-sealed semantic damages and whole-source normalization.
Actual author six-heesch-3, researcher. Ordinary author verification.
"""
from copy import deepcopy
import json
from pathlib import Path
import resource
import time
import check as r

def run():
    started=time.monotonic()
    here=Path(__file__).resolve().parent
    document=json.loads((here/'certificate.json').read_text())
    checked=r.read(document)
    errors={}
    def reject(name,mutation):
        d=deepcopy(document);mutation(d['certificate'])
        d['certificate_sha256']=r.base.canonical(d['certificate'])
        try:r.read(d)
        except ValueError as e:errors[name]=str(e);return
        raise ValueError('resealed damage accepted')
    reject('omit_competitor',lambda c:c['overlap_points'].pop())
    reject('duplicate_competitor',lambda c:c['overlap_points'].append(deepcopy(c['overlap_points'][0])))
    reject('wrong_survivor',lambda c:c.update(forced_pose=[8,1,-98,18]))
    reject('invalid_atom',lambda c:c['overlap_points'][0].update(candidate_atom=25))
    reject('outside_point',lambda c:c['overlap_points'][0].update(strict_interior_point=['999999','999999']))
    reject('root_rotated',lambda c:c['template'][0].update(pose=[4,0,-114,-14]))
    reject('second_body_shifted',lambda c:c['template'][1].update(pose=[2,0,-145,-38]))
    reject('remove_reflex_sector',lambda c:c.update(root_sectors=[]))
    reject('uncapped_source',lambda c:c.update(left_cap_triangle=False))
    reject('global_upper',lambda c:c.update(global_shape_Heesch_upper_claimed=True))
    poses=[tuple(row['pose']) for row in document['certificate']['template']]
    r.g.require(poses==[(2,0,-114,-14),(2,0,-146,-38)],'normalized template changed')
    origin=poses[0][2:]
    def normalize(p):return r.g.point((10,0,0,0),r.g.sub(p,origin))
    atoms,_=r.base.source();vertices={v for atom in atoms for v in atom}
    normal_poses=[(0,0,0,0),(0,0,-52,4),(6,1,76,4)]
    for pose,normal in zip(poses+[r.FORCED],normal_poses):
        r.g.require(all(normalize(r.g.point(pose,v))==r.g.point(normal,v) for v in vertices),
                    'normalization differs on a whole source vertex')
    r.g.require(normalize(r.POINT)==(14,2),'normalized critical point differs')
    result={'agent':'six-heesch-3','role':'researcher',
        'status':'reduced force normalization and ten resealed damages checked',
        'certificate_sha256':document['certificate_sha256'],
        'reader_mathematical_sha256':r.base.canonical(checked),
        'resealed_semantic_damage_rejections':errors,
        'normalized_pair':[list(p) for p in normal_poses[:2]],
        'normalized_necessary_supplier':list(normal_poses[2]),'normalized_point':[14,2],
        'whole_atom_source_vertex_normalization_checked':True,
        'global_Heesch_upper_claimed':False,'independent_review_claimed':False}
    result['stable_mathematical_sha256']=r.base.canonical(result)
    result['elapsed_seconds']=time.monotonic()-started
    result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
