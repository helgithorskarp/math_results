"""Literal full-graph oracle versus the conditional gluing implementation.

The imported glue module is the implementation under test, not the
reference. The reference enumerates all 4096 hole colorings of each
12-vertex fixture and checks physical edge masks of all 792 five-sets.
"""
import argparse
import copy
import hashlib
import itertools as it
import json
from pathlib import Path
import glue

HERE = Path(__file__).resolve().parent


def need(ok,message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256((json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def audit_fixture(path):
    data = json.loads(path.read_text()); need(data['n'] == 12,'fixture order')
    blocks = data['blocks']; need(blocks == [[[0,1],[2,3]],[[4,5],[6,7]],[[8,9],[10,11]]],'fixture blocks')
    holes = [[(u,v) for u in L for v in R] for L,R in blocks]
    all_holes = sum(holes,[]); owner = {e:(k,i) for k,es in enumerate(holes) for i,e in enumerate(es)}
    all_pairs = list(it.combinations(range(12),2)); full_index = {e:i for i,e in enumerate(all_pairs)}
    visible_red = {tuple(e) for e in data['red_visible_edges']}
    base = sum(1 << full_index[e] for e in visible_red)
    fives = []
    for S in it.combinations(range(12),5):
        pairs = list(it.combinations(S,2)); support = {owner[e][0] for e in pairs if e in owner}
        fives.append((S,sum(1 << full_index[e] for e in pairs),support))
    active,fixed_bad = glue.constraints(12,owner,visible_red)
    direct_valid = []; margin_valid = []; degree_lifts = []; witnesses = []
    for packed in range(4096):
        states = [(packed >> (4*k)) & 15 for k in range(3)]
        full = base | sum(1 << full_index[e] for k,es in enumerate(holes)
                          for i,e in enumerate(es) if states[k] >> i & 1)
        first_bad = next(((list(S),'red' if full & mask else 'blue') for S,mask,support in fives
                          if full & mask in (0,mask)),None)
        predicted = fixed_bad is None
        for color,support in active:
            values = [bool(states[k] >> i & 1) for k,mask in support for i in range(4) if mask >> i & 1]
            if all(x == color for x in values):
                predicted = False; break
        need(predicted == (first_bad is None),'pointwise conditional/full-graph agreement')
        if first_bad is None:
            direct_valid.append(packed)
        margins_ok = True
        for k,(L,R) in enumerate(blocks):
            for i,u in enumerate(L):
                margins_ok &= sum(bool(full >> full_index[u,v] & 1) for v in R) == data['row_margins'][k][i]
            for j,v in enumerate(R):
                margins_ok &= sum(bool(full >> full_index[u,v] & 1) for u in L) == data['column_margins'][k][j]
        if margins_ok:
            degree_lifts.append(packed)
            if first_bad is None:
                margin_valid.append(packed)
            else:
                witnesses.append({'states':states,'vertices':first_bad[0],'color':first_bad[1]})
    result = glue.decide(data)
    need(fixed_bad is None,'both fixtures have no fixed visible K5')
    # Independently derive local domains and pair relations from physical
    # five-sets whose hole support is contained in the chosen block set.
    def admissible(chosen):
        full = base | sum(1 << full_index[e] for k,s in chosen.items()
                          for i,e in enumerate(holes[k]) if s >> i & 1)
        return all(full & mask not in (0,mask) for S,mask,support in fives if support <= set(chosen))
    reference_domains = [[s for s in range(16) if s in (6,9) and admissible({k:s})] for k in range(3)]
    need(data['row_margins'] == data['column_margins'] == [[1,1]]*3,'all-one fixture margins')
    reference_relations = {f'{a}-{b}':[[A,B] for A,B in it.product(reference_domains[a],reference_domains[b])
                                     if admissible({a:A,b:B})] for a,b in it.combinations(range(3),2)}
    need(result['domains'] == reference_domains and result['relations'] == reference_relations,
         'every domain state and compatibility edge reconstructed physically')
    triangles = []
    for A,B,C in it.product(*reference_domains):
        if [A,B] in reference_relations['0-1'] and [A,C] in reference_relations['0-2'] and [B,C] in reference_relations['1-2']:
            triangles.append(A+(B << 4)+(C << 8))
    need(sorted(triangles) == margin_valid,'exact joint lift set, not aggregate equality')
    if margin_valid:
        need(result['status'] == 'LIFT_FOUND','positive oracle decision')
        selected = sum(s << (4*k) for k,s in enumerate(result['states']))
        need(selected in margin_valid,'selected lift is among literal valid graphs')
        expected_red = visible_red | {e for k,s in enumerate(result['states']) for i,e in enumerate(holes[k]) if s >> i & 1}
        need(result['graph'] == {'n':12,'red_edges':[list(e) for e in sorted(expected_red)]},'exact decoded graph')
    else:
        need(result['status'] == 'NO_LIFT_PAIRWISE_JOIN' and all(reference_domains) and all(reference_relations.values()),
             'all pairs feasible is insufficient')
    return {'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'all_hole_colorings':4096,
            'literal_five_sets':792,'clique_valid_colorings':len(direct_valid),
            'clique_valid_set_sha256':digest(direct_valid),'margin_correct_colorings':len(degree_lifts),
            'valid_margin_lifts':len(margin_valid),'valid_margin_lift_set':margin_valid,
            'forbidden_five_set_witnesses':witnesses,'oracle':result}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--report',type=Path,required=True); a = p.parse_args()
    reports = {name:audit_fixture(HERE/(name+'.json')) for name in ('negative','positive')}
    need(reports['negative']['valid_margin_lifts'] == 0 and reports['positive']['valid_margin_lifts'] > 0,'fixture roles')
    negative = json.loads((HERE/'negative.json').read_text()); positive = json.loads((HERE/'positive.json').read_text())
    need({tuple(e) for e in negative['red_visible_edges']} ^ {tuple(e) for e in positive['red_visible_edges']} == {(0,4)},
         'single visible edge repair')
    controls = []
    def reject(data,tag):
        try:
            glue.decide(data)
        except (ValueError,IndexError,KeyError,TypeError):
            controls.append(tag); return
        raise ValueError('invalid input accepted: '+tag)
    d = copy.deepcopy(negative); d['blocks'][1][0][0] = 0; reject(d,'overlapping_blocks')
    d = copy.deepcopy(negative); d['red_visible_edges'].append([0,2]); reject(d,'hole_edge_marked_visible')
    d = copy.deepcopy(negative); d['n'] = True; reject(d,'Boolean_order')
    d = copy.deepcopy(negative); d['row_margins'][0][0] = 3; reject(d,'invalid_margin')
    d = copy.deepcopy(negative); d['blocks'][0][0].reverse(); reject(d,'noncanonical_side_order')
    d = copy.deepcopy(negative); d['red_visible_edges'].append([0,1]); reject(d,'duplicate_visible_pair')
    d = copy.deepcopy(negative); d['column_margins'][0].pop(); reject(d,'wrong_margin_length')
    need(glue.decide(negative,0)['status'] == 'INCOMPLETE','zero budget is not an exclusion')
    d = copy.deepcopy(negative); d['red_visible_edges'] = []
    visible_bad = glue.decide(d)
    need(visible_bad['status'] == 'NO_LIFT_VISIBLE_K5','visible-only K5 control')
    S = visible_bad['witness']['vertices']
    holes = {tuple(sorted((u,v))) for L,R in d['blocks'] for u in L for v in R}
    need(all(e not in holes for e in it.combinations(S,2)),'visible-only witness uses no unknown pair')
    result = {'status':'POINTWISE_PHYSICAL_FIXTURE_AND_GLUING_CHECKS_PASSED','fixtures':reports,
              'rejected_input_controls':controls,'budget_zero_status':'INCOMPLETE','single_visible_repair_edge':[0,4],
              'visible_only_control':visible_bad}
    with a.report.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps({'status':result['status'],'pointwise_graphs':8192,
                      'negative_lifts':0,'positive_lifts':reports['positive']['valid_margin_lifts']}),flush=True)


if __name__ == '__main__':
    main()
