#!/usr/bin/env python3
"""Certify exact height-one escape, including a fresh complete lower-bound replay."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
COMPONENT_SHA = 'c366bf0ea4a392c5cf4b1a5789229c5aa74abfb08bd604fe636575ce9e960a2d'
LOWER_CODE_SHA = '4ba90249658107f0a408df2282eaba244045cbea1f268ce91d11facacbd67535'
LOWER_REPORT_SHA = '68cb48283624aaab6058447bcf585e263c2845190fd419774b4b4c6a2b0bdd87'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_lower():
    source = HERE/'verify.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==LOWER_CODE_SHA,'lower checker provenance')
    require(hashlib.sha256((HERE/'COMPONENT.json').read_bytes()).hexdigest()==COMPONENT_SHA,'component provenance')
    spec = importlib.util.spec_from_file_location('literal_component_lower',source)
    lower = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lower)
    return lower


def check_excursion(lower, parent, initial, endpoint, path):
    require(path['component_start_index']==2,'wrong starting component vertex')
    require(path['ceiling']==74,'wrong ceiling')
    adj = parent.neighbors(initial)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    quotas = parent.quotas(adj,signatures)
    degrees = list(map(len,adj))
    exceptional = parent.triangles(adj)[:3]
    conditions = parent.conditions(adj)
    scores = [parent.defect(parent.triangles(adj),signatures)]
    states = [tuple(initial)]
    for move in path['moves']:
        require(len(move)==4 and len(set(move))==4 and all(type(v) is int and 3<=v<43 for v in move),'move domain')
        a,b,c,d = move
        require(signatures[a]==signatures[b],'wrong signature pair')
        require(c in adj[a] and d in adj[b] and d not in adj[a] and c not in adj[b],'nonalternating move')
        support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
        adj = parent.changed_graph(adj,support)
        tt = parent.triangles(adj)
        require(list(map(len,adj))==degrees,'degree changed')
        require(parent.quotas(adj,signatures)==quotas,'quota changed')
        require(tt[:3]==exceptional,'exceptional counts changed')
        require(parent.lifting_failure(adj,conditions) is None,'pointwise path failure')
        require(parent.mixed_failure(adj) is None,'mixed K5 path failure')
        scores.append(parent.defect(tt,signatures))
        require(scores[-1]<=74,'height-one ceiling violated')
        states.append(lower.encode(adj))
    require(states[-1]==tuple(endpoint),'endpoint reconstruction mismatch')
    require(path['scores']==scores,'score certificate mismatch')
    require(scores[0]==73 and scores[-1]<73 and max(scores)==74,'not a height-one lower-score escape')
    return states,scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph',type=Path,default=HERE/'ESCAPE_GRAPH.json')
    parser.add_argument('--path',type=Path,default=HERE/'ESCAPE_PATH.json')
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    lower = load_lower()
    parent = lower.load_parent()
    checker = parent.load_audit()
    component = json.loads((HERE/'COMPONENT.json').read_text())
    initial = checker.decode({'format':'r55-triple-degree-exact-mixed-graph-v1',
                              'red_adjacency_hex':component['graphs'][2]})
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    path = json.loads(args.path.read_text())
    states,scores = check_excursion(lower,parent,initial,endpoint,path)
    audits = []
    for rows in states:
        audit = checker.inspect({'format':'r55-triple-degree-exact-mixed-graph-v1',
                                 'red_adjacency_hex':[format(x,'x') for x in rows]})
        audits.append({k:audit[k] for k in ('central_red_K5','central_blue_K5','pointwise_lifts',
                                         'central_vertices_failing_hard_local_caps','full_neighborhood_gaps')})
    # Full lower-bound replay, not inference from a hash or cached report alone.
    with tempfile.TemporaryDirectory(prefix='r55-escape-lower-') as scratch:
        fresh = Path(scratch)/'report.json'
        command = [sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
        command += [str(HERE/'verify.py'),'--report',str(fresh)]
        subprocess.run(command,check=True)
        original = (HERE/'report.json').read_bytes()
        require(hashlib.sha256(original).hexdigest()==LOWER_REPORT_SHA,'lower report provenance')
        require(fresh.read_bytes()==original,'fresh lower-bound mismatch')
    report = {'component_sha256':COMPONENT_SHA,'starting_component_index':2,'path':path,
              'graph_sha256':hashlib.sha256(args.graph.read_bytes()).hexdigest(),
              'corner_audits':audits,'lower_boundary_replayed':True,
              'lower_boundary_report_sha256':LOWER_REPORT_SHA,
              'minimum_peak_score_to_any_lower_Phi':74,'exact_required_score_increase':1,
              'scope':'Exact communication height for the specified admissible switch component; not a Ramsey graph, shortest-path or unrestricted edit-radius claim.'}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'scores':scores,'exact_required_score_increase':1,
                      'endpoint_red_K5':audits[-1]['central_red_K5'],
                      'endpoint_blue_K5':audits[-1]['central_blue_K5'],
                      'endpoint_cap_failures':len(audits[-1]['central_vertices_failing_hard_local_caps'])},sort_keys=True))


if __name__=='__main__':
    main()
