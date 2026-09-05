#!/usr/bin/env python3
"""Literal path checking and complete matching-based neutral-component audit."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_cell_preserving_repair'
INPUT = HERE.parent/'ramsey_r55_neutral_switch_escape/GRAPH.json'
CODE_SHA = '4e92829610eb2fe6956a42365c9de77d5c639541aefd44d3d05b896a94697cd0'
INPUT_SHA = '6ee8bb9e55165e4e742064e96149bea791152de80b244ebce297c17c86ff529c'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = PARENT/'verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==CODE_SHA,'parent source provenance')
    spec = importlib.util.spec_from_file_location('literal_matching_checker',source)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    return parent


def encode(adj):
    return tuple(sum(1 << v for v in row) for row in adj)


def check_path(parent, initial, endpoint, path):
    adj = parent.neighbors(initial)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    quotas = parent.quotas(adj,signatures)
    degrees = list(map(len,adj))
    exceptional = parent.triangles(adj)[:3]
    conditions = parent.conditions(adj)
    scores = [parent.defect(parent.triangles(adj),signatures)]
    require(parent.mixed_failure(adj) is None,'initial mixed K5')
    for move in path['moves']:
        require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
        a,b,c,d = move
        require(signatures[a]==signatures[b],'signature cell mismatch')
        require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'nonalternating move')
        support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
        adj = parent.changed_graph(adj,support)
        triangles = parent.triangles(adj)
        require(list(map(len,adj))==degrees,'degree changed')
        require(parent.quotas(adj,signatures)==quotas,'cell quotas changed')
        require(triangles[:3]==exceptional,'exceptional counts changed')
        require(parent.lifting_failure(adj,conditions) is None,'pointwise failure on path')
        require(parent.mixed_failure(adj) is None,'mixed K5 on path')
        score = parent.defect(triangles,signatures)
        require(score<=scores[-1],'uphill path step')
        scores.append(score)
    require(encode(adj)==tuple(endpoint),'path endpoint mismatch')
    require(path['scores']==scores,'path scores mismatch')
    return scores


def check_closure(graphs, censuses, parent):
    """Consumes complete independent censuses, never search adjacency claims."""
    require(len(set(graphs))==len(graphs)>0,'duplicate/empty component')
    require(len(censuses)==len(graphs),'census coverage')
    ids = {g:i for i,g in enumerate(graphs)}
    adjacency = []
    boundary = []
    for graph,census in zip(graphs,censuses):
        counts = census['counts']
        require(counts.get('decreasing_admissible',0)==0,'strictly improving exit')
        neighbors = []
        for support in census['neutral_switch_supports']:
            changed = encode(parent.changed_graph(parent.neighbors(graph),support))
            require(changed in ids,'neutral exit missing from component')
            neighbors.append(ids[changed])
        require(len(neighbors)==len(set(neighbors)),'duplicate neutral neighbor')
        adjacency.append(sorted(neighbors))
        positive = [int(k) for k,v in census['admissible_score_change_histogram'].items() if v and int(k)>0]
        require(all(int(k)>=0 for k in census['admissible_score_change_histogram']),'negative histogram entry')
        boundary.append(min(positive) if positive else None)
    require(all(i in adjacency[j] for i,row in enumerate(adjacency) for j in row),'neutral adjacency asymmetry')
    reached = {0}
    while True:
        expanded = reached|{j for i in reached for j in adjacency[i]}
        if expanded==reached:
            break
        reached = expanded
    require(len(reached)==len(graphs),'component is not connected to endpoint')
    return adjacency,boundary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'PATH.json')
    parser.add_argument('--component',type=Path,default=HERE/'COMPONENT.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    require(hashlib.sha256(INPUT.read_bytes()).hexdigest()==INPUT_SHA,'input graph provenance')
    parent = load_parent()
    checker = parent.load_audit()
    initial = checker.decode(json.loads(INPUT.read_text()))
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    scores = check_path(parent,initial,endpoint,json.loads(args.path.read_text()))
    certificate = json.loads(args.component.read_text())
    require(certificate['format']=='r55-labeled-neutral-component-v1','component format')
    docs = [{'format':'r55-triple-degree-exact-mixed-graph-v1','red_adjacency_hex':rows} for rows in certificate['graphs']]
    graphs = [checker.decode(doc) for doc in docs]
    require(graphs and graphs[0]==endpoint,'component root mismatch')
    signatures = [tuple(v for v in range(3) if row >> v & 1) for row in initial]
    quotas = parent.quotas(parent.neighbors(initial),signatures)
    audits,censuses = [],[]
    for index,(graph,doc) in enumerate(zip(graphs,docs)):
        audit = checker.inspect(doc)
        adj = parent.neighbors(graph)
        require(parent.quotas(adj,signatures)==quotas,'component cell quotas')
        require(audit['exceptional_local_profiles']==[[92,107]]*3,'component exceptional profiles')
        require(parent.defect(parent.triangles(adj),signatures)==certificate['score']==scores[-1],'component score')
        census = parent.census(adj,signatures)
        audits.append({k:audit[k] for k in ('central_red_K5','central_blue_K5','pointwise_lifts',
                                         'central_vertices_failing_hard_local_caps','full_neighborhood_gaps')})
        censuses.append(census)
        print(json.dumps({'verified_component_vertex':index,'switches':census['counts']['all_switches']},sort_keys=True),flush=True)
    adjacency,boundary = check_closure(graphs,censuses,parent)
    positive = [x for x in boundary if x is not None]
    report = {'input_sha256':INPUT_SHA,'graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),
              'component_sha256':hashlib.sha256(args.component.read_bytes()).hexdigest(),
              'path_scores':scores,'component_score':certificate['score'],
              'component_size':len(graphs),'neutral_adjacency':adjacency,
              'undirected_neutral_edges':sum(map(len,adjacency))//2,
              'minimum_positive_exit_by_vertex':boundary,
              'first_exit_score_lower_bound':certificate['score']+min(positive) if positive else None,
              'total_switches_checked':sum(x['counts']['all_switches'] for x in censuses),
              'corner_audits':audits,'complete_censuses':censuses,
              'scope':'A closed nonincreasing switch component; not a Ramsey graph, global fiber exclusion, or unrestricted edit-radius claim.'}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('corner_audits','complete_censuses')},sort_keys=True))


if __name__=='__main__':
    main()
