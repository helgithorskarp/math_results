#!/usr/bin/env python3
"""Literal matching/profile census and full graph replay; no search imports."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
SEED = HERE.parent/'ramsey_r55_k5_obstruction_repair/GRAPH.json'
SEED_SHA = 'c343c8ace3fb1c9dff6e90175ecdb1035989e0caf40a976a44d464a1381dc03c'
PARENT_SHA = '4e92829610eb2fe6956a42365c9de77d5c639541aefd44d3d05b896a94697cd0'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = HERE.parent/'ramsey_r55_cell_preserving_repair/verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==PARENT_SHA,'literal parent source pin')
    spec = importlib.util.spec_from_file_location('literal_retained_conditions',source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def encode(adj):
    return tuple(sum(1 << v for v in row) for row in adj)


def document(rows):
    return {'format':'r55-triple-degree-exact-mixed-graph-v1','red_adjacency_hex':[format(x,'x') for x in rows]}


def matching_supports(adj):
    """Enumerate matchings; test literal exceptional local edge-count changes."""
    for a,b,c,d in combinations(range(3,43),4):
        matchings = (((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c)))
        for first,second in combinations(matchings,2):
            colors1 = {v in adj[u] for u,v in first}
            colors2 = {v in adj[u] for u,v in second}
            if len(colors1)!=1 or len(colors2)!=1 or colors1==colors2:
                continue
            support = tuple(sorted(first+second))
            preserved = True
            for root in range(3):
                red_delta = sum((1-2*int(v in adj[u])) for u,v in support
                                if u in adj[root] and v in adj[root])
                blue_delta = sum((2*int(v in adj[u])-1) for u,v in support
                                 if u not in adj[root] and v not in adj[root])
                if red_delta or blue_delta:
                    preserved = False
                    break
            if preserved:
                yield support


def changes_quotas(adj, support):
    delta = Counter()
    for u,v in support:
        key = tuple(sorted((tuple(sorted(adj[u]&{0,1,2})),tuple(sorted(adj[v]&{0,1,2})))))
        delta[key] += 1-2*int(v in adj[u])
    return any(delta.values())


def check_path(parent, checker, initial, endpoint, path):
    require(path['seed_sha256']==SEED_SHA,'path seed pin')
    adj = parent.neighbors(initial)
    initial_adj = adj
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    degrees = list(map(len,adj))
    expected_E = checker.local_profiles(initial)[1][:3]
    audits,counts,phi,quota_steps = [],[],[],[]
    for step in range(len(path['moves'])+1):
        if step:
            move = path['moves'][step-1]
            require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
            a,b,c,d = move
            require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'nonalternating move')
            support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
            if changes_quotas(adj,support):
                quota_steps.append(step)
            adj = parent.changed_graph(adj,support)
        rows = encode(adj)
        require(list(map(len,adj))==degrees,'degrees changed')
        require([tuple(sorted(row&{0,1,2})) for row in adj]==signatures,'exceptional incidences changed')
        require(checker.local_profiles(rows)[1][:3]==expected_E,'exceptional local profiles changed')
        audit = checker.inspect(document(rows))
        current = [audit['central_red_K5'],audit['central_blue_K5']]
        if counts:
            require(sum(current)<sum(counts[-1]),'not strict K5 descent')
        counts.append(current)
        phi.append(parent.defect(parent.triangles(adj),signatures))
        audits.append({k:audit[k] for k in ('central_red_K5','central_blue_K5','pointwise_lifts',
                                         'central_vertices_failing_hard_local_caps','full_neighborhood_gaps')})
        print(json.dumps({'verified_path_step':step,'counts':current,'phi':phi[-1]},sort_keys=True),flush=True)
    require(rows==tuple(endpoint),'wrong path endpoint')
    require(counts==path['color_counts'] and phi==path['phi'],'path statistic mismatch')
    old_q,new_q = parent.quotas(initial_adj,signatures),parent.quotas(adj,signatures)
    quota_change = [[list(map(list,key)),new_q[key]-old_q[key]] for key in sorted(old_q.keys()|new_q.keys()) if old_q[key]!=new_q[key]]
    return {'graph_audits':audits,'quota_changing_steps_one_based':quota_steps,'endpoint_minus_seed_quotas':quota_change,
            'exceptional_local_profiles':expected_E}


def census(parent, checker, rows, entries=None):
    adj = parent.neighbors(rows)
    conditions = parent.conditions(adj)
    require(len(conditions)==884,'pointwise condition count')
    base = tuple(len(checker.monochromatic_bitsets(rows,color)) for color in (True,False))
    summary,histogram,old_histogram = Counter(),Counter(),Counter()
    digest,support_digest = hashlib.sha256(),hashlib.sha256()
    nonincreasing = []
    for support in sorted(matching_supports(adj)):
        summary['all_switches'] += 1
        quota_change = changes_quotas(adj,support)
        summary['quota_changing' if quota_change else 'quota_preserving'] += 1
        support_digest.update((json.dumps(support,separators=(',',':'))+'\n').encode())
        changed = parent.changed_graph(adj,support)
        violation = parent.lifting_failure(changed,conditions)
        full_counts = None
        if violation is not None:
            kind = 'lifting_failure'
        else:
            violation = parent.mixed_failure(changed,support)
            kind = 'mixed_failure' if violation is not None else 'admissible'
        if kind=='admissible':
            summary['admissible_quota_changing' if quota_change else 'admissible_quota_preserving'] += 1
            rr = encode(changed)
            full_counts = tuple(len(checker.monochromatic_bitsets(rr,color)) for color in (True,False))
            delta = sum(full_counts)-sum(base)
            histogram[delta] += 1
            if not quota_change:
                old_histogram[delta] += 1
            if delta<=0:
                nonincreasing.append({'support':support,'counts':full_counts,'delta':delta,'changes_quotas':quota_change})
        summary[kind] += 1
        entry = [support,kind,violation,full_counts,quota_change]
        digest.update((json.dumps(entry,separators=(',',':'))+'\n').encode())
        if entries is not None:
            entries.append(entry)
    return {'counts':dict(sorted(summary.items())),
            'admissible_K5_delta_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'quota_preserving_admissible_K5_delta_histogram':{str(k):v for k,v in sorted(old_histogram.items())},
            'nonincreasing_switches':nonincreasing,'canonical_supports_sha256':support_digest.hexdigest(),
            'canonical_classification_sha256':digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'PATH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    start = time.monotonic()
    require(hashlib.sha256(SEED.read_bytes()).hexdigest()==SEED_SHA,'seed pin')
    parent = load_parent()
    checker = parent.load_audit()
    initial = checker.decode(json.loads(SEED.read_text()))
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    path = json.loads(args.path.read_text())
    audits = check_path(parent,checker,initial,endpoint,path)
    first,last = census(parent,checker,initial),census(parent,checker,endpoint)
    require(all(int(delta)>=0 for delta in last['admissible_K5_delta_histogram']),'endpoint has a decreasing switch')
    require(all(int(delta)>0 for delta in first['quota_preserving_admissible_K5_delta_histogram']),'seed old-family strict barrier contradicted')
    require(any(item['delta']<0 and item['changes_quotas'] for item in first['nonincreasing_switches']),'no broader-family escape established')
    report = {'seed_sha256':SEED_SHA,'graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),
              'path':path,'path_verification':audits,'seed_census':first,'endpoint_census':last,
              'scope':'Exact exceptional-profile switch criterion; quota-release escape and complete endpoint one-switch census. Not a Ramsey graph, neutral-component classification, or whole-profile exclusion.'}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'initial_K5s':sum(path['color_counts'][0]),'final_K5s':sum(path['color_counts'][-1]),
                      'elapsed_seconds':round(time.monotonic()-start,6),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'endpoint_census':last},sort_keys=True))


if __name__=='__main__':
    main()
