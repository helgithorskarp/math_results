#!/usr/bin/env python3
"""Full graph/path checks and a matching census using full K5 enumeration."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_cell_preserving_repair'
COMPONENT = HERE.parent/'ramsey_r55_neutral_component_barrier/COMPONENT.json'
CODE_SHA = '4e92829610eb2fe6956a42365c9de77d5c639541aefd44d3d05b896a94697cd0'
COMPONENT_SHA = 'c366bf0ea4a392c5cf4b1a5789229c5aa74abfb08bd604fe636575ce9e960a2d'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = PARENT/'verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==CODE_SHA,'literal parent source pin')
    spec = importlib.util.spec_from_file_location('literal_degree_switches',source)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    return parent


def encode(adj):
    return tuple(sum(1 << v for v in row) for row in adj)


def as_document(rows):
    return {'format':'r55-triple-degree-exact-mixed-graph-v1','red_adjacency_hex':[format(x,'x') for x in rows]}


def check_path(parent, checker, initial, endpoint, path):
    require(path['component_start_index']==2,'starting component index')
    adj = parent.neighbors(initial)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    quotas = parent.quotas(adj,signatures)
    degrees = list(map(len,adj))
    expected_E = parent.triangles(adj)[:3]
    audits = []
    color_counts = []
    phi = []
    for step in range(len(path['moves'])+1):
        if step:
            move = path['moves'][step-1]
            require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
            a,b,c,d = move
            require(signatures[a]==signatures[b],'different signature cells')
            require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'nonalternating move')
            support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
            adj = parent.changed_graph(adj,support)
        rows = encode(adj)
        audit = checker.inspect(as_document(rows))
        require(list(map(len,adj))==degrees and parent.quotas(adj,signatures)==quotas,'degree or quota changed')
        tt = parent.triangles(adj)
        require(tt[:3]==expected_E,'exceptional local count changed')
        current = [audit['central_red_K5'],audit['central_blue_K5']]
        if color_counts:
            require(sum(current)<sum(color_counts[-1]),'not strict K5 descent')
        color_counts.append(current)
        phi.append(parent.defect(tt,signatures))
        audits.append({k:audit[k] for k in ('central_red_K5','central_blue_K5','pointwise_lifts',
                                         'central_vertices_failing_hard_local_caps','full_neighborhood_gaps')})
        print(json.dumps({'verified_path_step':step,'counts':current,'phi':phi[-1]},sort_keys=True),flush=True)
    require(rows==tuple(endpoint),'wrong path endpoint')
    require(color_counts==path['color_counts'] and phi==path['phi'],'path statistic mismatch')
    return audits


def census(parent, checker, rows):
    adj = parent.neighbors(rows)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    conditions = parent.conditions(adj)
    base = tuple(len(checker.monochromatic_bitsets(rows,color)) for color in (True,False))
    summary = Counter()
    histogram = Counter()
    digest = hashlib.sha256()
    supports_digest = hashlib.sha256()
    neutral = []
    for support in sorted(parent.matching_supports(adj,signatures)):
        summary['all_switches'] += 1
        supports_digest.update((json.dumps(support,separators=(',',':'))+'\n').encode())
        changed = parent.changed_graph(adj,support)
        violation = parent.lifting_failure(changed,conditions)
        counts = None
        if violation is not None:
            kind = 'lifting_failure'
        else:
            violation = parent.mixed_failure(changed,support)
            kind = 'mixed_failure' if violation is not None else 'admissible'
        if kind=='admissible':
            # Full graph clique enumeration, not the new incremental formula.
            rr = encode(changed)
            counts = tuple(len(checker.monochromatic_bitsets(rr,color)) for color in (True,False))
            delta = sum(counts)-sum(base)
            require(delta>=0,'K5-decreasing admissible switch found')
            histogram[delta] += 1
            if delta==0:
                neutral.append([list(e) for e in support])
        summary[kind] += 1
        digest.update((json.dumps([support,kind,violation,counts],separators=(',',':'))+'\n').encode())
    return {'counts':dict(sorted(summary.items())),
            'admissible_K5_delta_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'neutral_supports':neutral,'canonical_supports_sha256':supports_digest.hexdigest(),
            'canonical_classification_sha256':digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'PATH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    require(hashlib.sha256(COMPONENT.read_bytes()).hexdigest()==COMPONENT_SHA,'input component pin')
    parent = load_parent()
    checker = parent.load_audit()
    initial = checker.decode({'format':'r55-triple-degree-exact-mixed-graph-v1',
                              'red_adjacency_hex':json.loads(COMPONENT.read_text())['graphs'][2]})
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    path = json.loads(args.path.read_text())
    audits = check_path(parent,checker,initial,endpoint,path)
    complete = census(parent,checker,endpoint)
    report = {'component_sha256':COMPONENT_SHA,'graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),
              'path':path,'path_graph_audits':audits,'complete_one_switch_census':complete,
              'scope':'Strict actual-K5 descent and complete restricted one-switch barrier; not a Ramsey graph, larger-edit or whole-fiber exclusion.'}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'initial_K5s':sum(path['color_counts'][0]),'final_K5s':sum(path['color_counts'][-1]),
                      'final_phi':path['phi'][-1],'census':complete},sort_keys=True))


if __name__=='__main__':
    main()
