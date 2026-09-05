#!/usr/bin/env python3
"""Independent full-graph/component census and exact six-edge repair check."""
import argparse
from collections import Counter, deque
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_exceptional_profile_switches'
PARENT_SHA = '2a86489b2a9d3208ec18b1916faf16be8df744066a5967ed1b7bc63b68655f84'
SEED = PARENT/'GRAPH.json'
SEED_SHA = '122ed044228839122d6dba6d0f1cb87480818a6a8e8b277b6e5504d2da2e2cbc'
LEVEL = 358


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = PARENT/'verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==PARENT_SHA,'literal parent pin')
    spec = importlib.util.spec_from_file_location('profile_switch_verifier',source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def support(move):
    a,b,c,d = move
    return tuple(sorted(tuple(sorted(edge)) for edge in ((a,c),(b,d),(a,d),(b,c))))


def check_move(adj, move, literal):
    require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
    a,b,c,d = move
    require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'nonalternating move')
    return literal.changed_graph(adj,support(move))


def decode_component(certificate, parent, checker, initial):
    require(certificate['format']=='r55-actual-k5-neutral-component-v1','component format')
    require(certificate['seed_sha256']==SEED_SHA and type(certificate['level']) is int
            and certificate['level']==LEVEL,'component seed/level')
    graphs = [tuple(checker.decode({'format':'r55-triple-degree-exact-mixed-graph-v1',
                                   'red_adjacency_hex':graph})) for graph in certificate['graphs']]
    require(graphs and graphs[0]==tuple(initial),'component root')
    require(len(set(graphs))==len(graphs),'duplicate component graph')
    require(len(certificate['parents'])==len(certificate['parent_moves'])==len(graphs),'parent tree coverage')
    require(certificate['parents'][0] is None and certificate['parent_moves'][0] is None,'root parent')
    literal = parent.load_parent()
    for i in range(1,len(graphs)):
        p = certificate['parents'][i]
        require(type(p) is int and 0<=p<i,'parent order')
        changed = check_move(literal.neighbors(graphs[p]),certificate['parent_moves'][i],literal)
        require(parent.encode(changed)==graphs[i],'parent move does not reconstruct graph')
    return graphs


def closure(graphs, censuses, parent, literal):
    ids = {g:i for i,g in enumerate(graphs)}
    require(len(ids)==len(graphs)>0 and len(censuses)==len(graphs),'component census coverage')
    adjacency,exits = [],[]
    for i,(graph,census) in enumerate(zip(graphs,censuses)):
        row = []
        for item in census['nonincreasing_switches']:
            changed = parent.encode(literal.changed_graph(literal.neighbors(graph),item['support']))
            if item['delta']==0:
                require(changed in ids,'neutral neighbor missing from component')
                row.append(ids[changed])
            else:
                require(item['delta']<0,'invalid nonincreasing census entry')
                exits.append({'source':i,'support':item['support'],'color_counts':item['counts'],
                              'changes_quotas':item['changes_quotas'],
                              'graph_sha256':hashlib.sha256((json.dumps(parent.document(changed),sort_keys=True,indent=2)+'\n').encode()).hexdigest()})
        require(len(set(row))==len(row) and i not in row,'duplicate or loop neutral adjacency')
        adjacency.append(sorted(row))
    require(all(i in adjacency[j] for i,row in enumerate(adjacency) for j in row),'asymmetric neutral edges')
    distance = [None]*len(graphs)
    distance[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in adjacency[i]:
            if distance[j] is None:
                distance[j] = distance[i]+1
                queue.append(j)
    require(all(x is not None for x in distance),'disconnected component certificate')
    return adjacency,distance,exits


def check_exit(path, endpoint, initial, graphs, parent, literal, checker):
    require(path['seed_sha256']==SEED_SHA and path['moves'],'exit path provenance')
    adj = literal.neighbors(initial)
    rows = tuple(initial)
    ids = {g:i for i,g in enumerate(graphs)}
    steps = []
    for index,move in enumerate(path['moves']):
        require(rows in ids,'path leaves the neutral component prematurely')
        if index==len(path['moves'])-1:
            require(ids[rows]==path['source_component_vertex'],'wrong exit source')
        adj = check_move(adj,move,literal)
        rows = parent.encode(adj)
        if index+1<len(path['moves']):
            require(rows in ids,'intermediate path graph not in component')
        audit = checker.inspect(parent.document(rows))
        current = [audit['central_red_K5'],audit['central_blue_K5']]
        require(sum(current)==LEVEL if index+1<len(path['moves']) else sum(current)<LEVEL,'exit path level')
        steps.append({'move':move,'color_counts':current,'phi':literal.defect(literal.triangles(adj),
                      [tuple(sorted(row&{0,1,2})) for row in adj])})
    require(rows==tuple(endpoint),'exit path endpoint mismatch')
    changed = [(u,v) for u,v in combinations(range(43),2) if bool(initial[u] >> v & 1)!=bool(rows[u] >> v & 1)]
    removed = [edge for edge in changed if initial[edge[0]] >> edge[1] & 1]
    added = [edge for edge in changed if not(initial[edge[0]] >> edge[1] & 1)]
    require(len(changed)==6 and len(removed)==len(added)==3,'expected six-edge repair')
    initial_adj = literal.neighbors(initial)
    signatures = [tuple(sorted(row&{0,1,2})) for row in initial_adj]
    require(literal.quotas(adj,signatures)==literal.quotas(initial_adj,signatures),'exit changes cell quotas')
    require(all((initial[u]&7)^(initial[v]&7)==7 for u,v in changed),'net repair not antipodal')
    # Directly compare all six complete exceptional color-neighborhood graphs.
    for root in range(3):
        for red in (True,False):
            before_side = [v for v in range(43) if v!=root and bool(initial[root] >> v & 1)==red]
            after_side = [v for v in range(43) if v!=root and bool(rows[root] >> v & 1)==red]
            require(before_side==after_side,'exceptional neighborhood vertex set changed')
            require(all(bool(initial[u] >> v & 1)==bool(rows[u] >> v & 1)
                        for u,v in combinations(before_side,2)),'exceptional induced neighborhood graph changed')
    cycle = [20,27,19,29,22,34]
    require(set(changed)=={tuple(sorted((cycle[i],cycle[(i+1)%6]))) for i in range(6)},'alternating six-cycle support')
    require(all(bool(initial[cycle[i]] >> cycle[(i+1)%6] & 1)==(i%2==0) for i in range(6)),'six-cycle colors')
    return {'path_steps':steps,'net_removed_edges':removed,'net_added_edges':added,
            'net_changed_edge_count':len(changed),'alternating_cycle':cycle,
            'all_six_exceptional_neighborhood_graphs_unchanged':True,
            'endpoint_audit':{k:audit[k] for k in ('central_red_K5','central_blue_K5',
                'central_vertices_failing_hard_local_caps','full_neighborhood_gaps','pointwise_lifts')}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--component',type=Path,default=HERE/'COMPONENT.json')
    parser.add_argument('--path',type=Path,default=HERE/'EXIT_PATH.json')
    parser.add_argument('--graph',type=Path,default=HERE/'EXIT_GRAPH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    start = time.monotonic()
    require(hashlib.sha256(SEED.read_bytes()).hexdigest()==SEED_SHA,'seed pin')
    parent = load_parent()
    literal = parent.load_parent()
    checker = literal.load_audit()
    initial = checker.decode(json.loads(SEED.read_text()))
    certificate = json.loads(args.component.read_text())
    graphs = decode_component(certificate,parent,checker,initial)
    signatures = [tuple(sorted(row&{0,1,2})) for row in literal.neighbors(initial)]
    seed_quotas = literal.quotas(literal.neighbors(initial),signatures)
    audits,censuses,projected_digests = [],[],[]
    for i,rows in enumerate(graphs):
        audit = checker.inspect(parent.document(rows))
        require(audit['exceptional_local_profiles']==[[92,107]]*3,'exceptional profiles')
        require(audit['central_red_K5']+audit['central_blue_K5']==LEVEL,'wrong component K5 level')
        entries = []
        census = parent.census(literal,checker,rows,entries)
        digest = hashlib.sha256()
        for supp,kind,violation,counts,changed_quota in entries:
            digest.update((json.dumps([supp,kind,counts,changed_quota],separators=(',',':'))+'\n').encode())
        projected_digests.append(digest.hexdigest())
        censuses.append(census)
        audits.append({'color_counts':[audit['central_red_K5'],audit['central_blue_K5']],
                       'phi':literal.defect(literal.triangles(literal.neighbors(rows)),signatures),
                       'cell_quotas_equal_seed':literal.quotas(literal.neighbors(rows),signatures)==seed_quotas,
                       'central_cap_failures':audit['central_vertices_failing_hard_local_caps']})
        print(json.dumps({'verified_component_vertex':i,'all_switches':census['counts']['all_switches']},sort_keys=True),flush=True)
    adjacency,distances,exits = closure(graphs,censuses,parent,literal)
    path = json.loads(args.path.read_text())
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    exit_check = check_exit(path,endpoint,initial,graphs,parent,literal,checker)
    require(not any(item['source']==0 for item in exits),'seed has a strictly decreasing switch')
    require(exits and len(path['moves'])==2,'two-switch shortest-path certificate')
    best = min(sum(item['color_counts']) for item in exits)
    require(sum(exit_check['path_steps'][-1]['color_counts'])==best,'path not to best one-edge boundary value')
    summary = dict(sorted(sum((Counter(item['counts']) for item in censuses),Counter()).items()))
    report = {'seed_sha256':SEED_SHA,'component_sha256':hashlib.sha256(args.component.read_bytes()).hexdigest(),
              'exit_graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),'level':LEVEL,
              'component_size':len(graphs),'neutral_adjacency':adjacency,'neutral_distances_from_seed':distances,
              'undirected_neutral_edges':sum(map(len,adjacency))//2,'total_census_counts':summary,
              'component_audits':audits,'complete_censuses':censuses,
              'canonical_projected_classification_sha256_by_vertex':projected_digests,
              'negative_exits':exits,'negative_exit_count':len(exits),
              'distinct_negative_exit_graphs':len({item['graph_sha256'] for item in exits}),
              'negative_exit_total_histogram':{str(k):v for k,v in sorted(Counter(sum(x['color_counts']) for x in exits).items())},
              'best_one_edge_exit_K5_total':best,'minimum_nonincreasing_switch_steps_to_lower_total':2,
              'minimum_edge_hamming_distance_to_lower_total_in_retained_relaxation':6,
              'exit_verification':exit_check,
              'scope':'Complete labeled K5=358 neutral component and its one-switch lower boundary; exact six-edge repair distance within fixed degrees, E incidences/profiles, mixed-K5 and pointwise constraints. Not a Ramsey graph, full radius-six classification, or analysis below the first exit.'}
    args.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('component_size','undirected_neutral_edges','negative_exit_count',
                     'distinct_negative_exit_graphs','best_one_edge_exit_K5_total','total_census_counts')},sort_keys=True),flush=True)
    print(json.dumps({'elapsed_seconds':round(time.monotonic()-start,6),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True),flush=True)


if __name__=='__main__':
    main()
