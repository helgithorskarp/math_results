"""Necessary cut rows for the entire selected derived-mark labelled root3 cover.

No deletion prefix or B-internal graph is read. Integer cell equations and
literal ordinary22-point sets independently give every indexed row word.
The supplied neighborhood cover is untrusted and compared with a fresh,
complete selected physical degree-branch enumeration, not an expected hash.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

import frame


def physical_cover(guard):
    """Choose each representative marked pair and exhaust the other eight degree margins."""
    rows=[set() for _ in range(9)];result=set()
    def visit(v):
        guard.tick()
        if v==8:
            frame.require([len(r) for r in rows]==[3]*8+[2], 'Physical cover leaf degrees')
            frame.require(all(not rows[x]&rows[y] for x in range(9) for y in rows[x]),
                          'Physical cover leaf contains a triangle')
            result.add(tuple(sum(1<<x for x in r) for r in rows));return
        need=3-len(rows[v])
        candidates=[x for x in range(v+1,8) if len(rows[x])<3 and not rows[v]&rows[x]]
        if not 0<=need<=len(candidates):return
        for chosen in itertools.combinations(candidates,need):
            guard.tick()
            for x in chosen:rows[v].add(x);rows[x].add(v)
            margins=[3-len(rows[x]) for x in range(v+1,8)]
            positive=sum(n>0 for n in margins)
            if all(0<=n<=max(0,positive-1) for n in margins):visit(v+1)
            for x in chosen:rows[v].remove(x);rows[x].remove(v)
    for pair in tuple(tuple(frame.A.index(x) for x in pair) for pair in frame.ALLOWED_PAIRS):
        frame.require(not any(rows), 'Physical cover recursion failed to revert')
        for x in pair:rows[8].add(x);rows[x].add(8)
        visit(0)
        for x in pair:rows[8].remove(x);rows[x].remove(8)
    return tuple(sorted(result))


def algebraic_row(i,neighbors,guard):
    x=frame.A[i];degree=neighbors.bit_count()
    s=10-frame.TYPES[x].bit_count()-degree
    r=[(3 if frame.TYPES[x]&(1<<j) else 5)-frame.sigma(x,j)-
       sum(bool(frame.TYPES[frame.A[k]]&(1<<j)) for k in range(9) if neighbors&(1<<k))
       for j in range(3)]
    b=2*s-sum(r);a=r[0]+r[1]-s+b;c=s-b-r[1];d=s-b-r[0]
    counts=(a,b,c,d);words=[]
    if all(0<=n<=len(cell) for n,cell in zip(counts,frame.CELLS)):
        for chosen in itertools.product(*(itertools.combinations(cell,n)
                                          for cell,n in zip(frame.CELLS,counts))):
            guard.tick()
            words.append(sum(1<<z for group in chosen for z in group))
    return sorted(words),dict(row_rank=s,remaining_low_counts=r,four_cell_counts=list(counts))


def literal_row(i,neighbors,guard):
    """All physical B subsets; direct red and complement spines on22 labels."""
    x=frame.A[i];s=10-frame.TYPES[x].bit_count()-neighbors.bit_count()
    universe=set(range(22))
    low_red=[{4+h for h,t in enumerate(frame.TYPES) if t&(1<<j)} for j in range(4)]
    base=({j for j in range(4) if frame.TYPES[x]&(1<<j)}|
          {4+frame.A[k] for k in range(9) if neighbors&(1<<k)})
    words=[]
    for chosen in itertools.combinations(range(9),s):
        guard.tick()
        red=base|{4+frame.B[k] for k in chosen}
        blue=universe-red-{4+x};deficits=[]
        for j in range(4):
            if j in red:pages=len(low_red[j]&red);cap=3
            else:pages=len((universe-low_red[j]-{j})&blue);cap=6
            deficits.append(cap-pages)
        if len(red)==10 and deficits==[frame.sigma(x,j) for j in range(4)]:
            words.append(sum(1<<k for k in chosen))
    return sorted(words)


def run(packet):
    guard=frame.Guard();frame.configuration()
    frame.require(packet['selected_case_index']==frame.CASE_INDEX
                  and packet['ordered_A']==list(frame.A) and packet['ordered_B']==list(frame.B)
                  and packet['whole_A_types']==[frame.TYPES[x] for x in frame.A]
                  and packet['all_complete_case_mark_full_tags']==[[k,*frame.MARK_FULL_TAGS[k]] for k in sorted(frame.MATRICES)]
                  and packet['all_complete_case_columns']==
                      [[k,list(c)] for k,c in sorted(frame.MATRICES.items())],
                  'Untrusted cover changes the complete shared type/matrix scope')
    masks=[sum(1<<frame.A.index(x) for x in p) for p in frame.ALLOWED_PAIRS]
    frame.require(packet['whole_allowed_neighbor_masks']==masks
                  and packet['representative_neighbor_masks']==masks,
                  'Untrusted cover changes the necessary neighbor-pair scope')
    graphs=physical_cover(guard)
    frame.require(len(graphs)==1800*len(masks), 'Fresh selected physical cover cardinality differs')
    frame.require([list(g) for g in graphs]==packet['representative_cover_graphs'],
                  'Entire untrusted cover differs from fresh physical enumeration')
    patterns=sorted({(i,g[i]) for g in graphs for i in range(9)})
    domains={};records=[]
    for i,mask in patterns:
        produced,parameters=algebraic_row(i,mask,guard)
        literal=literal_row(i,mask,guard)
        frame.require(produced==literal, 'Whole cell and literal physical cut row differ')
        domains[(i,mask)]=tuple(literal)
        records.append(dict(point=i,physical_high=frame.A[i],A_neighbors=mask,
                            parameters=parameters,all_physical_B_words=literal))
    empty=[];remaining=[];by_first=collections.Counter()
    for k,g in enumerate(graphs):
        guard.tick()
        failure=next((i for i in range(9) if not domains[(i,g[i])]),None)
        if failure is None:remaining.append(k)
        else:empty.append([k,failure]);by_first[failure]+=1
    result=dict(agent='six-books-3',role='researcher',
        status='COMPLETE_NECESSARY_SELECTED_PROFILE3_COVER_ROW_DOMAIN_AUDIT',
        counts=list(frame.COUNTS),columns=list(frame.COLUMNS),root_low=3,case_index=frame.CASE_INDEX,
        full_frame_tags=[[frame.TYPES[x],frame.COLUMNS[x]] for x in frame.A],
        entire_physical_cover_reconstructed=True,whole_representative_graphs=[list(g) for g in graphs],
        whole_pattern_row_records=records,whole_pattern_count=len(patterns),
        distinct_physical_row_word_count=sum(len(r['all_physical_B_words']) for r in records),
        empty_row_graph_witnesses=empty,remaining_graph_indices=remaining,
        empty_row_graph_count=len(empty),remaining_graph_count=len(remaining),
        first_empty_row_counts=[[i,by_first[i]] for i in sorted(by_first)],
        all_indexed_rows_equal_cell_and_literal=True,
        columns_rank5_not_yet_imposed=True,A_pair_spines_not_yet_imposed=True,
        individual_survivor_realizability_asserted=False,
        case_excluded=not remaining,whole_profile_excluded=False,
        actual_host_automorphism_required=False,independent_person_review=False,
        ordinary_bridges_formalized=False,work_units=guard.work,
        work_guard=2000000,internal_seconds_guard=40)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cover',required=True)
    parser.add_argument('--out',required=True);parser.add_argument('--case',type=int,required=True);args=parser.parse_args();frame.select(args.case)
    record=run(json.loads(Path(args.cover).read_bytes()));data=frame.encode(record)
    Path(args.out).write_bytes(data+b'\n')
    print(json.dumps(dict(status=record['status'],whole_graphs=len(record['whole_representative_graphs']),
        row_patterns=record['whole_pattern_count'],empty_row_graphs=record['empty_row_graph_count'],
        remaining_graphs=record['remaining_graph_count'],case_excluded=record['case_excluded'],
        whole_record_bytes=len(data),whole_record_sha256=hashlib.sha256(data).hexdigest(),
        work_units=record['work_units']),sort_keys=True,separators=(',',':')))
