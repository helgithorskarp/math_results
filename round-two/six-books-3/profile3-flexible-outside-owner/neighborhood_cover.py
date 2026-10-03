"""Complete full physical root3 covers for all38 entire profile3 matrices.

The source-only generic two-algorithm baseline is freshly regenerated.
Separately label the four explicit suppressed-core representatives directly
onto ALL necessary physical neighbor pairs of each selected case, then compare every resulting graph
with the filtered full physical inventory. No pair-search prefix is read.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

import frame
import neighborhoods


def run():
    guard=frame.Guard();frame.configuration()
    pairs=tuple(sum(1<<frame.A.index(x) for x in p) for p in frame.ALLOWED_PAIRS)
    reps=tuple(sum(1<<frame.A.index(x) for x in p) for p in frame.REPRESENTATIVE_PAIRS)
    frame.require(pairs==tuple(sum(1<<frame.A.index(x) for x in p) for p in frame.PAIRS[frame.CASE_INDEX])
                  and reps==pairs,
                  'Whole physical neighbor masks differ')
    # First mechanism: all labelings of the four explicit marked cores.
    images=set();multiplicities=collections.Counter();by_core={}
    for name,(core,edge) in neighborhoods.CORES.items():
        marked=neighborhoods.subdivide(core,edge);local=set();count=0
        source_rest=[x for x in range(8) if x not in edge]
        for mask in reps:
            target=[x for x in range(8) if mask&(1<<x)]
            target_rest=[x for x in range(8) if x not in target]
            for ordered in itertools.permutations(target):
                for tail in itertools.permutations(target_rest):
                    guard.tick();count+=1
                    phi=[0]*9;phi[8]=8
                    for x,y in zip(edge,ordered):phi[x]=y
                    for x,y in zip(source_rest,tail):phi[x]=y
                    graph=neighborhoods.image(marked,phi)
                    frame.require(graph[8]==mask and not neighborhoods.triangles(graph)
                        and [r.bit_count() for r in graph]==[3]*8+[2],
                        'Direct core image violates physical scope')
                    images.add(graph);local.add(graph);multiplicities[graph]+=1
        by_core[name]=dict(label_images=count,distinct_physical_graphs=len(local))
    frame.require(sum(r['label_images'] for r in by_core.values())==4*len(pairs)*2*720,
                  'Incomplete direct marked-core label assignments')
    # The second mechanism covers every physical neighbor pair by direct
    # degree branching, and independently every cubic subdivision. The
    # imported baseline code is unchanged from the credited source.
    baseline,all_graphs,classes=neighborhoods.run(True)
    guard.work+=baseline['work_units'];guard.tick()
    frame.require(len(all_graphs)==50400, 'Fresh generic complete baseline differs')
    allowed=tuple(g for g in all_graphs if g[8] in pairs)
    cover=tuple(g for g in all_graphs if g[8] in reps)
    frame.require(images==set(cover), 'Whole direct core images and physical selected complete physical domain differ')
    all_pair_counts=collections.Counter(g[8] for g in all_graphs)
    frame.require(len(all_pair_counts)==28 and set(all_pair_counts.values())=={1800},
                  'Generic physical neighbor-pair uniformity differs')
    frame.require(len(allowed)==1800*len(pairs) and len(cover)==1800*len(pairs),
                  'Complete restricted physical domain sizes differ')
    phis=frame.actions()
    positions=[tuple(frame.A.index(p[x]) for x in frame.A) for p in phis]
    frame.require(all(all((frame.TYPES[frame.A[i]],frame.COLUMNS[frame.A[i]])==
                          (frame.TYPES[frame.A[p[i]]],frame.COLUMNS[frame.A[p[i]]])
                          for i in range(9)) and p[8]==8 for p in positions),
                  'Root graph transport changes a full tag or mark')
    cover_index={g:i for i,g in enumerate(cover)};transports=[]
    for i,g in enumerate(allowed):
        chosen=None
        for k,p in enumerate(positions):
            guard.tick()
            transformed=neighborhoods.image(g,p)
            if transformed[8] in reps:
                frame.require(transformed in cover_index,
                              'Literal graph image absent from complete representative cover')
                chosen=[i,k,cover_index[transformed]];break
        frame.require(chosen is not None, 'Necessary physical graph has no representative transport')
        transports.append(chosen)
    result=dict(agent='six-books-3',role='researcher',
        status='COMPLETE_NECESSARY_SELECTED_PROFILE3_PHYSICAL_NEIGHBOR_PAIR_COVER',
        selected_case_index=frame.CASE_INDEX,ordered_A=list(frame.A),ordered_B=list(frame.B),
        whole_A_types=[frame.TYPES[x] for x in frame.A],
        all_complete_case_mark_full_tags=[[k,*frame.MARK_FULL_TAGS[k]] for k in sorted(frame.MATRICES)],
        all_complete_case_columns=[[k,list(c)] for k,c in sorted(frame.MATRICES.items())],
        changed_tags_never_quotiented=True,
        whole_allowed_neighbor_masks=list(pairs),representative_neighbor_masks=list(reps),
        generic_classification=baseline,
        generic_source_credit_commit='cc7da2d2365bec8cfaad6a09857e0614bed54bf0',
        generic_source_sha256=hashlib.sha256(Path(neighborhoods.__file__).read_bytes()).hexdigest(),
        all28_physical_pair_counts=[[m,all_pair_counts[m]] for m in sorted(all_pair_counts)],
        core_image_counts=by_core,
        all_core_images_equal_entire_restricted_physical_domain=True,
        allowed_physical_graphs=list(allowed),representative_cover_graphs=list(cover),
        all_literal_label_transports=transports,
        selected_full_tag_preserving_permutations=[list(p) for p in positions],
        allowed_physical_graph_count=len(allowed),representative_cover_count=len(cover),
        cover_count_is_group_orbit_count=False,individual_graph_realizability_asserted=False,
        previous_nonempty_deletion_prefix_used=False,case_excluded=False,
        whole_profile_excluded=False,actual_host_automorphism_required=False,
        ordinary_completeness_and_survival_formalized=False,independent_person_review=False,
        work_units=guard.work,work_guard=2000000,internal_seconds_guard=40)
    return result,all_graphs


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    parser.add_argument('--generic-out',required=True);parser.add_argument('--case',type=int,required=True);args=parser.parse_args();frame.select(args.case)
    result,graphs=run();encoded=frame.encode(result);generic=frame.encode(graphs)
    Path(args.out).write_bytes(encoded+b'\n');Path(args.generic_out).write_bytes(generic+b'\n')
    print(json.dumps(dict(status=result['status'],whole_generic_graphs=len(graphs),
        generic_bytes=len(generic),generic_sha256=hashlib.sha256(generic).hexdigest(),
        allowed_physical_graphs=result['allowed_physical_graph_count'],
        representative_cover=result['representative_cover_count'],
        exact_group_orbits_claimed=False,case_excluded=False,
        whole_record_bytes=len(encoded),whole_record_sha256=hashlib.sha256(encoded).hexdigest(),
        work_units=result['work_units']),sort_keys=True,separators=(',',':')))
