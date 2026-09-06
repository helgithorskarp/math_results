"""Check the H92 adapter on an already known invalid physical fixture.

This is a regression and witness check, not a fresh family obstruction.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import lift_h92

G = Path(__file__).resolve().parent.parent/'ramsey_r55_joint_neighborhood_degree_realization/G92.json'
G_SHA = '394aee401f7e9d6843affc05968b305bad2f92cd328035c65b5b8a0da9619a3e'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--schema',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True); a = p.parse_args()
    need(hashlib.sha256(G.read_bytes()).hexdigest() == G_SHA,'old physical fixture identity')
    graph = json.loads(G.read_text()); red = {tuple(e) for e in graph['red_edges']}
    schema = json.loads(a.schema.read_text()); values = [tuple(e) in red for e in schema['visible_pairs']]
    need(all(((u,v) in red) == bool(c) for u,v,c in schema['fixed_pairs']),'fixture agrees with fixed colors')
    need([sum(v in e for e in red) for v in range(43)] == schema['degree_targets'],'fixture degree profile')
    for root in (0,1):
        Q = [v for v in range(43) if v != root and tuple(sorted((root,v))) not in red]
        need(sum(e in red for e in it.combinations(Q,2)) == 124,'fixture density')
    result = lift_h92.run(a.schema,values,0)
    need(result['status'] == 'NO_LIFT_VISIBLE_K5','known invalid fixture rejected before state enumeration')
    witness = result['witness']; S = witness['vertices']; color = witness['color'] == 'red'
    holes = {tuple(e) for b in schema['blocks'] for e in b['pairs']}
    need(len(S) == len(set(S)) == 5 and all(e not in holes and ((e in red) == color) for e in it.combinations(S,2)),
         'literal visible-only K5 witness')
    zero = lift_h92.run(a.schema,[False]*523,0)
    need(zero['status'] == 'NO_LIFT_OUTSIDE_DEGREE','all-blue retained assignment degree control')
    v = zero['vertex']; fixed_red = {tuple(e[:2]) for e in schema['fixed_pairs'] if e[2]}
    need(zero['residual'] == schema['degree_targets'][v]-sum(v in e for e in fixed_red) != 0,
         'literal outside degree obstruction')
    rejected = []
    for bad,tag in ((values[:-1],'short_vector'),([int(x) for x in values],'integer_not_Boolean')):
        try:
            lift_h92.run(a.schema,bad,0)
        except ValueError:
            rejected.append(tag)
        else:
            raise ValueError('bad input accepted')
    report = {'status':'H92_ADAPTER_REGRESSION_CHECKED','fixture_sha256':G_SHA,
              'fixture_result':result,'all_blue_visible_control':zero,'rejected_controls':rejected,
              'scope':'old invalid visible coloring only; no decision of the H92 family'}
    with a.report.open('x') as f:
        json.dump(report,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
