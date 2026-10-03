"""Bit-count cut proposals checked with literal complete22-point stars.

Every row domain and the whole selected raw labelled physical cover are freshly reconstructed.
This smaller root-cut mechanism does not read or resume the limited original
high-star pair producer. Nonempty cut fixed points are not exclusions.
"""
import argparse
import hashlib
import json
from pathlib import Path

import frame
import row_domains


def compatible(graph,i,j,u,v):
    low=(frame.TYPES[frame.A[i]]&frame.TYPES[frame.A[j]]).bit_count()
    pages=low+(graph[i]&graph[j]).bit_count()+(u&v).bit_count()
    return pages <= (3 if graph[i]&(1<<j) else 6)


def proposal(graph,initial,guard):
    pools=[set(r) for r in initial];cuts=[]
    frame.require(all(pools), 'Pair stage expected a nonempty necessary row domain')
    while True:
        changed=False
        for i in range(9):
            for word in sorted(pools[i]):
                for j in range(9):
                    if i==j:continue
                    supported=False
                    for other in sorted(pools[j]):
                        guard.tick()
                        if compatible(graph,i,j,word,other):supported=True;break
                    if supported:continue
                    pools[i].remove(word);cuts.append([i,word,j]);changed=True
                    if not pools[i]:return cuts,[sorted(r) for r in pools],True
                    break
        if not changed:return cuts,[sorted(r) for r in pools],False


def physical_star(graph,i,word):
    red={j for j in range(4) if frame.TYPES[frame.A[i]]&(1<<j)}
    red|={4+frame.A[k] for k in range(9) if graph[i]&(1<<k)}
    red|={4+frame.B[k] for k in range(9) if word&(1<<k)}
    frame.require(len(red)==10 and 4+frame.A[i] not in red,
                  'Literal cut star violates degree10 or self exclusion')
    return frozenset(red),frozenset(set(range(22))-red-{4+frame.A[i]})


def literal_support(graph,i,j,u,v):
    ri,bi=physical_star(graph,i,u);rj,bj=physical_star(graph,j,v)
    frame.require((4+frame.A[j] in ri)==(4+frame.A[i] in rj),
                  'Physical A pair lacks reciprocal color')
    red=4+frame.A[j] in ri
    pages=len(ri&rj) if red else len(bi&bj)
    return pages <= (3 if red else 6)


def check(graph,initial,cuts,guard):
    pools=[set(r) for r in initial];checked=0
    for i,word,j in cuts:
        frame.require(0<=i<9 and 0<=j<9 and i!=j and word in pools[i],
                      'Proposed cut target/witness is not in the current physical domains')
        for other in sorted(pools[j]):
            guard.tick()
            frame.require(not literal_support(graph,i,j,word,other),
                          'Proposed deletion has a literal ordinary-spine support')
        pools[i].remove(word);checked+=1
    return dict(checked_deletions=checked,final_domains=[sorted(r) for r in pools],
                empty_rows=[i for i,r in enumerate(pools) if not r],
                excluded=any(not r for r in pools))


def run(cover,out):
    guard=frame.Guard()
    rows=row_domains.run(cover);guard.work+=rows['work_units'];guard.tick()
    graphs=rows['whole_representative_graphs']
    domains={(r['point'],r['A_neighbors']):r['all_physical_B_words']
             for r in rows['whole_pattern_row_records']}
    records=[]
    result=dict(agent='six-books-3',role='researcher',
        status='INCOMPLETE_NECESSARY_CUT_PAIR_STAGE',
        counts=list(frame.COUNTS),columns=list(frame.COLUMNS),root_low=3,case_index=frame.CASE_INDEX,
        row_stage_mathematics_sha256=hashlib.sha256(frame.encode(rows)).hexdigest(),
        row_stage_empty_graphs=rows['empty_row_graph_count'],
        row_stage_remaining=rows['remaining_graph_indices'],
        completed_graph_records=records,not_yet_attempted=list(rows['remaining_graph_indices']),
        case_excluded=False,whole_profile_excluded=False,
        previous_original_deletion_prefix_used=False,actual_host_automorphism_required=False,
        ordinary_bridges_formalized=False,independent_person_review=False)
    def save():
        result['work_units']=guard.work
        Path(out).write_bytes(frame.encode(result)+b'\n')
    save()
    for k in rows['remaining_graph_indices']:
        graph=graphs[k];initial=[domains[(i,graph[i])] for i in range(9)]
        cuts,pools,claimed=proposal(graph,initial,guard)
        checked=check(graph,initial,cuts,guard)
        frame.require(checked['final_domains']==pools and checked['excluded']==claimed,
                      'Entire proposed and literal final domains differ')
        records.append(dict(physical_graph_index=k,whole_graph=graph,
            initial_domains=initial,ordered_deletion_proposals=cuts,literal_check=checked,
            status='LITERAL_EMPTY_ROW_EXCLUSION' if claimed else 'NONEMPTY_PAIR_FIXED_POINT_NO_EXCLUSION'))
        result['not_yet_attempted'].remove(k);save()
    survivors=[r['physical_graph_index'] for r in records if not r['literal_check']['excluded']]
    result.update(status='COMPLETE_NECESSARY_CUT_PAIR_STAGE',
        pair_stage_excluded_graphs=sum(r['literal_check']['excluded'] for r in records),
        remaining_graph_indices=survivors,remaining_graph_count=len(survivors),
        literal_checked_deletions=sum(r['literal_check']['checked_deletions'] for r in records),
        case_excluded=not survivors,work_guard=2000000,internal_seconds_guard=40,
        column_rank5_not_yet_imposed=True,B_internal_graph_not_attempted=True)
    save();return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cover',required=True)
    parser.add_argument('--out',required=True);parser.add_argument('--case',type=int,required=True);args=parser.parse_args();frame.select(args.case)
    record=run(json.loads(Path(args.cover).read_bytes()),args.out)
    print(json.dumps(dict(status=record['status'],row_empty=record['row_stage_empty_graphs'],
        pair_excluded=record['pair_stage_excluded_graphs'],remaining=record['remaining_graph_count'],
        literal_deletions=record['literal_checked_deletions'],case_excluded=record['case_excluded'],
        whole_record_bytes=len(frame.encode(record)),
        whole_record_sha256=hashlib.sha256(frame.encode(record)).hexdigest(),
        work_units=record['work_units']),sort_keys=True,separators=(',',':')))
