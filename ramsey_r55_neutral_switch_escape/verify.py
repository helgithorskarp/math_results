#!/usr/bin/env python3
"""Check a two-switch escape, its interaction, and its minimum switch depth."""
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_cell_preserving_repair'
INPUT_SHA = '7a832f229bb3fd97f5c3e5dceb060988fb5c5d2df074d1cb37ddbb1dcd5fc8a6'
PARENT_CODE_SHA = '4e92829610eb2fe6956a42365c9de77d5c639541aefd44d3d05b896a94697cd0'
PARENT_REPORT_SHA = '5a1a875de620a14499ff7dbacf18357ea07a5486177a92e140b51315a6a27c89'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = PARENT/'verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest() == PARENT_CODE_SHA,'parent source pin')
    spec = importlib.util.spec_from_file_location('literal_repair_verifier',source)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    return parent


def support(move):
    a,b,c,d = move
    return tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))


def flip(rows, edges):
    out = list(rows)
    for u,v in edges:
        out[u] ^= 1 << v
        out[v] ^= 1 << u
    return tuple(out)


def checked_move(rows, move):
    require(len(move)==4 and len(set(move))==4 and all(type(u) is int and 3<=u<43 for u in move),'move domain')
    a,b,c,d = move
    require(rows[a]&7 == rows[b]&7,'different signature cells')
    require(rows[a] >> c & 1 and rows[b] >> d & 1 and not(rows[a] >> d & 1) and not(rows[b] >> c & 1),'switch is not alternating')
    return flip(rows,support(move))


def literal_triangles(rows):
    out = [0]*len(rows)
    for a,b,c in combinations(range(len(rows)),3):
        if rows[a] >> b & 1 and rows[a] >> c & 1 and rows[b] >> c & 1:
            for u in (a,b,c):
                out[u] += 1
    return out


def penalties(rows, triangles):
    return [0 if v<3 else max(0,t-100,101-(rows[v]&7).bit_count()-t) for v,t in enumerate(triangles)]


def interaction(rows, first, second):
    """Exact mixed finite difference when supports meet at one vertex."""
    A = {v for e in first for v in e}
    B = {v for e in second for v in e}
    require(len(A&B)==1 and not set(first)&set(second),'one shared vertex required')
    w = next(iter(A&B))
    incident_A = [v if u==w else u for u,v in first if w in (u,v)]
    incident_B = [v if u==w else u for u,v in second if w in (u,v)]
    answer = [0]*len(rows)
    for i in incident_A:
        for j in incident_B:
            term = (1-2*(rows[w] >> i & 1))*(1-2*(rows[w] >> j & 1))*(rows[i] >> j & 1)
            for v in (w,i,j):
                answer[v] += term
    return answer


def square(input_rows, path, endpoint):
    require(len(path['moves'])==2,'exact two-switch certificate required')
    S,T = path['moves']
    first = checked_move(input_rows,S)
    second = checked_move(input_rows,T)
    combined = checked_move(first,T)
    reverse = checked_move(second,S)
    require(combined == reverse == tuple(endpoint),'commuting endpoint reconstruction')
    corners = [tuple(input_rows),first,second,combined]
    tt = [literal_triangles(g) for g in corners]
    pp = [penalties(g,t) for g,t in zip(corners,tt)]
    scores = [sum(p) for p in pp]
    require(path['scores'] == [scores[0],scores[1],scores[3]],'path score certificate')
    require(scores[1] == scores[0] and scores[2]>scores[0]>scores[3],'neutral-then-improving and uphill-alone scope')
    predicted = interaction(input_rows,support(S),support(T))
    actual = [d-b-c+a for a,b,c,d in zip(*tt)]
    require(predicted == actual,'triangle mixed-difference identity')
    terms = [{'vertex':v,'triangles':[t[v] for t in tt],'penalties':[p[v] for p in pp],
              'mixed_difference':pp[3][v]-pp[1][v]-pp[2][v]+pp[0][v]} for v in range(43)
             if pp[3][v]-pp[1][v]-pp[2][v]+pp[0][v]]
    return corners,tt,{'corner_order':['G','G_S','G_T','G_ST'],'scores':scores,
                      'moves':path['moves'],'net_changed_edges':[list(e) for e in sorted(set(support(S))^set(support(T)))],
                      'triangle_interaction':[[v,d] for v,d in enumerate(actual) if d],
                      'penalty_interaction_terms':terms,'total_penalty_interaction':scores[3]-scores[1]-scores[2]+scores[0]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'PATH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    raw = (PARENT/'GRAPH.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA,'input graph pin')
    parent = load_parent()
    checker = parent.load_audit()
    initial = checker.decode(json.loads(raw))
    document = json.loads(args.graph.read_text())
    endpoint = checker.decode(document)
    path = json.loads(args.path.read_text())
    corners,tt,report = square(initial,path,endpoint)
    signatures = [tuple(u for u in range(3) if row >> u & 1) for row in initial]
    quotas = parent.quotas(parent.neighbors(initial),signatures)
    corner_reports = []
    for rows,t in zip(corners,tt):
        doc = {'format':document['format'],'red_adjacency_hex':[format(row,'x') for row in rows]}
        exact = checker.inspect(doc)
        require(parent.quotas(parent.neighbors(rows),signatures) == quotas,'cell quotas changed')
        require([x[0] for x in exact['all_local_profiles']] == t,'literal triangle reconstruction')
        require(exact['exceptional_local_profiles'] == [[92,107]]*3,'exceptional counts changed')
        corner_reports.append({key:exact[key] for key in (
            'red_edges','degree_histogram','signature_vector','exceptional_local_profiles',
            'monochromatic_fives_meeting_E','pointwise_lifts','central_red_K5','central_blue_K5',
            'central_vertices_failing_hard_local_caps','full_neighborhood_gaps')})
    # Replay the previously published one-switch boundary as a DEPENDENCY.
    # This is not a new-radius search or a claim of independent peer review.
    parent_raw = (PARENT/'report.json').read_bytes()
    require(hashlib.sha256(parent_raw).hexdigest() == PARENT_REPORT_SHA,'parent report pin')
    census = parent.census(parent.neighbors(initial),signatures)
    require(census == json.loads(parent_raw)['complete_one_switch_census'],'parent boundary replay mismatch')
    report.update(input_sha256=INPUT_SHA,graph_sha256=hashlib.sha256(args.graph.read_bytes()).hexdigest(),
                  corners=corner_reports,parent_boundary_replayed=True,
                  parent_boundary_classification_sha256=census['canonical_classification_sha256'],
                  minimum_admissible_switches_to_any_lower_Phi=2,
                  scope='A neutral-plus-improving two-switch escape; not a Ramsey graph, not a minimal edge-support theorem, and not an endpoint local-minimum claim.')
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'scores':report['scores'],'triangle_interaction':report['triangle_interaction'],
                      'penalty_interaction':report['total_penalty_interaction'],
                      'minimum_switches':2,'endpoint_red_K5':corner_reports[-1]['central_red_K5'],
                      'endpoint_blue_K5':corner_reports[-1]['central_blue_K5'],
                      'endpoint_cap_failures':len(corner_reports[-1]['central_vertices_failing_hard_local_caps'])},sort_keys=True))


if __name__ == '__main__':
    main()
