"""Independent physical audit; imports neither model nor flow nor margin tests.

Recover antipodal blocks from root signatures. Reconstruct neighborhood CNF
by scanning actual five-sets. Check the JSON side-condition schema exactly.
The optional prior formula comparison concerns its physical clauses only.
"""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_SHA = '926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466'
G_SHA = '394aee401f7e9d6843affc05968b305bad2f92cd328035c65b5b8a0da9619a3e'
PRIOR_SHA = '4e3361668a02b08602b695e88033b7776dbf26ecb9ebe4e8cbe061405720b055'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def graph(path,n):
    data = json.loads(path.read_text())
    need(data['n'] == n, 'graph order')
    edges = data['red_edges']
    need(isinstance(edges,list), 'edge list')
    need(all(isinstance(e,list) and len(e)==2 and all(type(x) is int for x in e)
             and 0 <= e[0] < e[1] < n for e in edges), 'canonical edges')
    red = {tuple(e) for e in edges}
    need(len(red) == len(edges) and edges == sorted(edges), 'unique sorted edges')
    return red


def geometry():
    need(hashlib.sha256((HERE/'H92.json').read_bytes()).hexdigest() == H_SHA, 'H identity')
    h = graph(HERE/'H92.json',20)
    root_neighbors = {0: {10,11,12,13,18,19,*range(29,43)},
                      1: {*range(14,29),*range(38,43)}, 38: set(range(20))}
    roots = sorted(root_neighbors)
    fixed = {e: e in h for e in it.combinations(range(20),2)}
    for root in roots:
        for vertex in range(43):
            if root == vertex:
                continue
            edge = tuple(sorted((root,vertex)))
            color = vertex in root_neighbors[root]
            need(edge not in fixed or fixed[edge] == color, 'consistent stars')
            fixed[edge] = color
    groups = defaultdict(list)
    for v in range(43):
        if v not in roots:
            groups[tuple(v in root_neighbors[r] for r in roots)].append(v)
    blocks = []
    for signature,vertices in groups.items():
        opposite = tuple(not x for x in signature)
        if signature < opposite and opposite in groups:
            left,right = vertices,groups[opposite]
            if len(left) > len(right):
                left,right = right,left
            blocks.append((left,right))
    blocks.sort(key=lambda p:(len(p[1]),p[0]))
    removed = {tuple(sorted((u,v))) for left,right in blocks for u in left for v in right}
    free = [e for e in it.combinations(range(43),2) if e not in fixed]
    visible = [e for e in free if e not in removed]
    need(len(removed) == 104 and removed <= set(free), 'antipodal free pairs')
    endpoints = [v for L,R in blocks for v in L+R]
    need(len(endpoints) == len(set(endpoints)) == 38, 'independent degree blocks')
    neighborhoods = [(r,col,root_neighbors[r] if col else set(range(43))-{r}-root_neighbors[r])
                     for r in roots for col in (False,True)]
    for e in removed:
        need(all(not set(e) <= N for _,_,N in neighborhoods), 'removed pair absent from every neighborhood')
    return fixed,free,visible,removed,blocks,neighborhoods


def reconstructed_clauses(fixed,visible,neighborhoods):
    index = {e:i+1 for i,e in enumerate(visible)}
    clauses = set(); surviving_conditions = Counter()
    for vertices in it.combinations(range(43),5):
        subset = set(vertices)
        for bad in (False,True):
            tags = []
            for root,col,N in neighborhoods:
                if bad == col and root in subset and subset-{root} <= N:
                    tags.append((root,col,'through_root'))
                elif bad != col and subset <= N:
                    tags.append((root,col,'opposite_inside'))
            if not tags:
                continue
            pairs = list(it.combinations(vertices,2))
            if any(e in fixed and fixed[e] != bad for e in pairs):
                continue
            need(all(e in fixed or e in index for e in pairs), 'clause support visible')
            clause = tuple(sorted((-1 if bad else 1)*index[e] for e in pairs if e not in fixed))
            need(clause, 'not an all-fixed forbidden set')
            clauses.add(clause)
            surviving_conditions.update(tags)
    return sorted(clauses,key=lambda row:(len(row),row)), {
        f'{r}-{int(c)}-{kind}':n for (r,c,kind),n in sorted(surviving_conditions.items())}


def schema(data,fixed,visible,removed,blocks,neighborhoods,cnf_sha):
    index = {e:i+1 for i,e in enumerate(visible)}
    need(data['format'] == 'ramsey-six-neighborhood-degree-projection-v1', 'format')
    need(data['H_sha256'] == H_SHA and data['neighborhood_cnf_sha256'] == cnf_sha, 'input/CNF hashes')
    need(data['variables'] == 523 and data['visible_pairs'] == [list(e) for e in visible], 'visible variables')
    need(data['removed_pairs'] == [list(e) for e in sorted(removed)], 'removed pairs')
    residuals = [{'vertex':v,
                  'constant':(20 if v in (0,1,38) else 21)-sum(c for e,c in fixed.items() if v in e),
                  'subtract_variables':[i for e,i in index.items() if v in e]} for v in range(43)]
    need(data['residuals'] == residuals, 'residual functions')
    need(data['residual_zero_vertices'] == [0,1,18,19,38], 'outside equations')
    densities = []
    for r,c,N in neighborhoods:
        if r in (0,1) and not c:
            pairs = list(it.combinations(sorted(N),2))
            need(not set(pairs)&removed, 'density support')
            densities.append({'root':r,'equals':124-sum(fixed[e] for e in pairs if e in fixed),
                              'sum_variables':[index[e] for e in pairs if e in index]})
    need(data['density_equalities'] == densities, 'both density equations')
    expected = []
    for L,R in blocks:
        subsets = [[L[i] for i in range(4) if mask & (1<<i)] for mask in range(1,16)]
        expected.append({'left':L,'right':R,'row_bounds':[0,len(R)],'column_bounds':[0,4],
                         'equal_margin_totals':True,'subset_cuts':subsets,
                         'cut_semantics':'sum residuals on S <= sum min(residual at j, size(S)) over right j'})
    need(data['blocks'] == expected, 'all bounds, balances and labeled cuts')


def fixture(fixed,visible,removed,neighborhoods,clauses,lifted_path):
    need(hashlib.sha256((HERE/'G92.json').read_bytes()).hexdigest() == G_SHA, 'original fixture identity')
    old = graph(HERE/'G92.json',43); new = graph(lifted_path,43)
    for red in (old,new):
        need(all((e in red) == c for e,c in fixed.items()), 'fixed graph edges')
        need([sum(v in e for e in red) for v in range(43)] == [20 if v in (0,1,38) else 21 for v in range(43)],
             'full degree sequence')
    need((old ^ new) <= removed, 'only projected edges changed')
    neighborhood_hashes = {}
    for r,c,N in neighborhoods:
        pairs = list(it.combinations(sorted(N),2))
        need([e in old for e in pairs] == [e in new for e in pairs], 'entire induced graph preserved')
        raw = ''.join('1' if e in old else '0' for e in pairs).encode()
        neighborhood_hashes[f'{r}-{int(c)}'] = hashlib.sha256(raw).hexdigest()
        if r in (0,1) and not c:
            need(sum(e in new for e in pairs) == 124, 'Q total 124')
    values = {i+1:e in old for i,e in enumerate(visible)}
    violations = sum(not any(values[abs(x)] == (x>0) for x in row) for row in clauses)
    need(violations == 202, 'fixture is explicitly not a six-neighborhood witness')
    counts = [Counter(),Counter()]; changed = []
    for vs in it.combinations(range(43),5):
        pairs = list(it.combinations(vs,2)); statuses = []
        for i,red in enumerate((old,new)):
            nr = sum(e in red for e in pairs)
            status = 'red' if nr == 10 else 'blue' if nr == 0 else None
            statuses.append(status)
            if status:
                counts[i][status] += 1
        if statuses[0] != statuses[1] and len(changed) < 1:
            need(not set(vs)&{0,1,38}, 'changed K5 is root-free')
            changed.append({'vertices':list(vs),'original':statuses[0],'lifted':statuses[1]})
    need(changed, 'concrete full-K5 nonpreservation example')
    return {'changed_edges':len(old ^ new), 'six_neighborhood_hashes':neighborhood_hashes,
            'neighborhood_clause_violations_both':violations,
            'original_K5':dict(counts[0]), 'lifted_K5':dict(counts[1]),
            'changed_full_K5_example':changed[0],
            'lifted_sha256':hashlib.sha256(lifted_path.read_bytes()).hexdigest(),
            'scope':'fixture tests lifting; neither graph satisfies the projected Ramsey subsystem'}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    p.add_argument('--lifted',type=Path,required=True); p.add_argument('--report',type=Path,required=True)
    p.add_argument('--prior-cnf',type=Path)
    a = p.parse_args()
    fixed,free,visible,removed,blocks,neighborhoods = geometry()
    clauses,tags = reconstructed_clauses(fixed,visible,neighborhoods)
    expected = (f'p cnf 523 {len(clauses)}\n' + ''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()
    actual = (a.work/'neighborhood_clauses.cnf').read_bytes()
    need(actual == expected, 'literal physical five-set CNF/order/EOF')
    cnf_sha = hashlib.sha256(actual).hexdigest()
    data = json.loads((a.work/'projection.json').read_text())
    schema(data,fixed,visible,removed,blocks,neighborhoods,cnf_sha)
    mutations = {}
    altered = copy.deepcopy(data); altered['blocks'][0]['subset_cuts'].pop(); mutations['drop_cut'] = altered
    altered = copy.deepcopy(data); altered['blocks'][1]['row_bounds'][1] -= 1; mutations['change_bound'] = altered
    altered = copy.deepcopy(data); altered['blocks'][2]['equal_margin_totals'] = False; mutations['drop_balance'] = altered
    altered = copy.deepcopy(data); altered['residuals'][2]['constant'] += 1; mutations['change_degree'] = altered
    altered = copy.deepcopy(data); altered['density_equalities'][0]['equals'] += 1; mutations['change_density'] = altered
    altered = copy.deepcopy(data); altered['residual_zero_vertices'].remove(18); mutations['drop_outside_equation'] = altered
    for name,bad in mutations.items():
        try:
            schema(bad,fixed,visible,removed,blocks,neighborhoods,cnf_sha)
        except ValueError:
            pass
        else:
            raise ValueError('corrupted descriptor accepted: '+name)
    prior = None
    if a.prior_cnf:
        raw = a.prior_cnf.read_bytes()
        need(hashlib.sha256(raw).hexdigest() == PRIOR_SHA, 'prior formula identity')
        index = {e:i+1 for i,e in enumerate(visible)}
        old_edges = {i+1:e for i,e in enumerate(free)}
        primary = []
        for line in raw.decode().splitlines()[1:]:
            row = tuple(map(int,line.split()[:-1]))
            if all(abs(x) <= len(free) for x in row):
                need(all(old_edges[abs(x)] in index for x in row), 'old physical clause uses visible pairs only')
                primary.append(tuple(sorted((1 if x>0 else -1)*index[old_edges[abs(x)]] for x in row)))
        need(set(primary) == set(clauses), 'prior physical clause set equals independent reconstruction')
        prior = {'sha256':PRIOR_SHA,'primary_clause_occurrences':len(primary),
                 'distinct_primary_clauses':len(set(primary)),
                 'scope':'physical clause equality only; prior counter encodings not re-proved'}
    report = {'status':'EXACT_PROJECTION_SCHEMA_AND_PHYSICAL_CLAUSES_CHECKED',
              'fixed_pairs':len(fixed),'prior_free_pairs':len(free),'retained_free_pairs':len(visible),
              'removed_pairs':len(removed),'blocks':[{'left':L,'right':R} for L,R in blocks],
              'neighborhood_clauses':len(clauses),'physical_condition_counts':tags,
              'neighborhood_cnf_sha256':cnf_sha,
              'projection_json_sha256':hashlib.sha256((a.work/'projection.json').read_bytes()).hexdigest(),
              'descriptor_mutations_rejected':sorted(mutations), 'prior_formula_comparison':prior,
              'fixture':fixture(fixed,visible,removed,neighborhoods,clauses,a.lifted),
              'trust':'unformalized proof plus independent in-process algorithms; no external review or SAT/UNSAT verdict'}
    with a.report.open('x') as f:
        json.dump(report,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(report,sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
