"""Small exhaustive reductions, existential selector tests, certificate mutations."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import shutil
import tempfile
import analyze
import verify


def fixture(n, code):
    return {'n': n, 'red_edges': [list(e) for j,e in enumerate(itertools.combinations(range(n),2))
                                  if code >> j & 1]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    dp_checks, local_checks = 0, 0
    for n in range(6):
        for code in range(1 << (n*(n-1)//2)):
            doc = fixture(n, code)
            edges = set(map(tuple, doc['red_edges']))
            adj = [sum(1 << w for w in range(n) if tuple(sorted((v,w))) in edges) for v in range(n)]
            dp = analyze.clique_dp(adj)
            for mask in range(1 << n):
                vertices = [v for v in range(n) if mask >> v & 1]
                exact = max(k for k in range(n+1) if any(all(e in edges for e in itertools.combinations(q,2))
                            for q in itertools.combinations(vertices,k)))
                verify.need(dp[mask] == exact, 'subset clique DP control')
                dp_checks += 1
            if n in (3,4) and not (n == 4 and code == 0):
                for s0 in range(1 << n):
                    for s1 in range(1 << n):
                        local = verify.make_local(n, edges, s0, s1)
                        le = set(map(tuple, local['red_edges']))
                        actual = all(len({e in le for e in itertools.combinations(q,2)}) == 2
                                     for q in itertools.combinations(range(n+3),5))
                        criterion = dp[s0] <= 3 and dp[s1] <= 3 and dp[s0 & s1] <= 2
                        verify.need(actual == criterion, 'local25 reduction small control')
                        local_checks += 1
    families, assignments, selector_assignments = 0, 0, 0
    for n in (1,2):
        for k in range(4):
            for selected in itertools.combinations(range(1 << (2*n)),k):
                cases = [{'S0': format(c & ((1 << n)-1), 'x'), 'S1': format(c >> n, 'x')} for c in selected]
                total_primary = 2*n+1  # Includes one genuinely unused primary bit.
                clauses = analyze.boundary_rows(cases, n, total_primary)
                for primaries in range(1 << total_primary):
                    possible = False
                    for aux in range(1 << k):
                        values = primaries | (aux << total_primary)
                        satisfied = all(any(bool(values >> (abs(x)-1) & 1) == (x > 0) for x in row) for row in clauses)
                        possible |= satisfied
                        selector_assignments += 1
                    verify.need(possible == ((primaries & ((1 << (2*n))-1)) in selected), 'existential selector encoding')
                    assignments += 1
                families += 1
    verify.need((dp_checks,local_checks,families,assignments,selector_assignments) ==
                (33867,16640,712,22424,160296), 'control coverage')
    graph_doc = json.loads(analyze.GRAPH.read_text())
    n, edges = verify.decode(graph_doc)
    k4 = verify.clique_masks(n, edges, 4)
    domains, examined = verify.independent_domains(n, k4)
    verify.check_data(a.work, n, edges, k4, domains, examined)
    files = ['result.json','cases.json','LOCAL_GRAPH.json','domain12.bin','domain14.bin','domain15.bin','boundary.cnf']
    rejected = []
    with tempfile.TemporaryDirectory(prefix='r55-marked-controls-') as tmp:
        w = Path(tmp)
        def reset():
            for name in files:
                shutil.copyfile(a.work/name, w/name)
        def json_mutate(name, action):
            data = json.loads((w/name).read_text())
            action(data)
            (w/name).write_text(json.dumps(data))
        def cut_bytes(name):
            data = (w/name).read_bytes()
            (w/name).write_bytes(data[:-4])
        mutations = [
            ('omitted_case',lambda:json_mutate('cases.json',lambda x:x.pop())),
            ('duplicate_case',lambda:json_mutate('cases.json',lambda x:x.append(x[0]))),
            ('wrong_case_mask',lambda:json_mutate('cases.json',lambda x:x[0].update(S0='000000'))),
            ('boolean_case_id',lambda:json_mutate('cases.json',lambda x:x[0].update(id=False))),
            ('wrong_maximum',lambda:json_mutate('result.json',lambda x:x.update(max_red_K4_free_induced_order=15))),
            ('omitted_maximizer',lambda:json_mutate('result.json',lambda x:x['all_maximizers'].pop())),
            ('wrong_obstruction',lambda:json_mutate('result.json',lambda x:x['rejected_common_triangle_pairs'][0].update(red_triangle=[0,1,2]))),
            ('truncated_domain12',lambda:cut_bytes('domain12.bin')),
            ('truncated_domain14',lambda:cut_bytes('domain14.bin')),
            ('wrong_local_graph',lambda:json_mutate('LOCAL_GRAPH.json',lambda x:x['red_edges'].pop())),
            ('boolean_local_vertex',lambda:json_mutate('LOCAL_GRAPH.json',lambda x:x['red_edges'].__setitem__(0,[False,1]))),
            ('extra_boundary_row',lambda:(w/'boundary.cnf').write_text((w/'boundary.cnf').read_text()+'1 0\n')),
            ('missing_boundary_row',lambda:(w/'boundary.cnf').write_text(''.join((w/'boundary.cnf').read_text().splitlines(keepends=True)[:-1]))),
            ('changed_boundary_sign',lambda:(w/'boundary.cnf').write_text((w/'boundary.cnf').read_text().replace('-441 ', '441 ', 1))),
        ]
        for label, mutate in mutations:
            reset()
            mutate()
            try:
                verify.check_data(w,n,edges,k4,domains,examined)
            except (ValueError,KeyError,TypeError):
                rejected.append(label)
            else:
                raise ValueError('accepted corruption: '+label)
    for label, mutate in [
        ('boolean_order',lambda x:x.update(n=True)),
        ('duplicate_edge',lambda x:x['red_edges'].append(x['red_edges'][-1])),
        ('loop',lambda x:x['red_edges'].__setitem__(0,[0,0])),
        ('boolean_vertex',lambda x:x['red_edges'].__setitem__(0,[False,1])),
        ('range',lambda x:x['red_edges'].__setitem__(0,[0,22])),
    ]:
        doc = copy.deepcopy(graph_doc)
        mutate(doc)
        for name, reader in [('producer',analyze.decode),('verifier',verify.decode)]:
            try:
                reader(doc)
            except (ValueError,KeyError,TypeError):
                rejected.append(label+':'+name)
            else:
                raise ValueError('accepted bad graph: '+label+':'+name)
    report = {'status':'PASS','subset_clique_number_checks':dp_checks,
              'literal_local_reduction_graphs':local_checks,'selector_case_families':families,
              'selector_primary_assignments':assignments,'selector_full_assignments':selector_assignments,
              'certificate_mutations_rejected':14,'graph_mutations_rejected_both':5,'rejections':rejected}
    a.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
