"""Physical reconstruction of the entire guarded H92 K5 interface.

No imports from the decomposition producer, projection model, or gluing
oracle. Direct fixed-color-compatible clique recursion supplies all clauses.
"""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path

H = Path(__file__).resolve().parent.parent/'ramsey_r55_antipodal_degree_projection/H92.json'
H_SHA = '926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path,data):
    with path.open('x') as f:
        json.dump(data,f,indent=2,sort_keys=True); f.write('\n')


def physical():
    need(sha(H) == H_SHA,'H input identity'); raw = json.loads(H.read_text())
    need(raw['n'] == 20,'H order'); h = {tuple(e) for e in raw['red_edges']}
    need(len(h) == len(raw['red_edges']) == 92,'simple H')
    stars = {0:set([10,11,12,13,18,19,38,39,40,41,42]+list(range(29,38))),
             1:set([14,15,16,17,18,19,38,39,40,41,42]+list(range(20,29))),38:set(range(20))}
    fixed = {(u,v):(u,v) in h for u in range(20) for v in range(u+1,20)}
    for r,red in stars.items():
        for v in range(43):
            if v == r:
                continue
            e = tuple(sorted((r,v))); color = v in red
            need(e not in fixed or fixed[e] == color,'H/star agreement'); fixed[e] = color
    free = [e for e in it.combinations(range(43),2) if e not in fixed]
    sig = {v:tuple(v in stars[r] for r in (0,1,38)) for v in range(43) if v not in stars}
    hidden = [e for e in free if all(a != b for a,b in zip(sig[e[0]],sig[e[1]]))]
    visible = [e for e in free if e not in set(hidden)]
    # Connected components of hidden pairs recover the three blocks.
    adj = {v:set() for e in hidden for v in e}
    for u,v in hidden:
        adj[u].add(v); adj[v].add(u)
    seen = set(); components = []
    for root in sorted(adj):
        if root in seen:
            continue
        stack = [root]; component = set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v); stack.extend(adj[v]-component)
        seen |= component
        # The side of size four is always unambiguous in this H92 geometry.
        R = adj[root]; L = component-R
        if len(L) != 4:
            L,R = R,L
        need(len(L) == 4 and all(adj[v] == R for v in L) and all(adj[v] == L for v in R),
             'complete bipartite hole component')
        components.append((sorted(L),sorted(R)))
    components.sort(key=lambda p:min(p[1]))
    need([(len(L),len(R)) for L,R in components] == [(4,8),(4,9),(4,9)],'block order and sizes')
    index = {e:i+1 for i,e in enumerate(visible)}
    index.update({e:524+i for i,e in enumerate(hidden)})
    block_pairs = [[tuple(sorted((u,v))) for u in L for v in R] for L,R in components]
    return fixed,visible,components,block_pairs,index,stars


def possible_clauses(fixed,index):
    result = set(); counts = {}
    for color in (False,True):
        after = [sum(1 << v for v in range(u+1,43) if (u,v) not in fixed or fixed[u,v] == color)
                 for u in range(43)]
        count = 0
        def visit(vertices,candidates):
            nonlocal count
            if len(vertices) == 5:
                row = tuple(sorted((1 if not color else -1)*index[e]
                                   for e in it.combinations(vertices,2) if e in index))
                need(row,'fixed K5'); result.add(row); count += 1; return
            while candidates.bit_count() >= 5-len(vertices):
                low = candidates & -candidates; candidates ^= low; v = low.bit_length()-1
                visit(vertices+[v], candidates & after[v])
        visit([], (1 << 43)-1); counts['red' if color else 'blue'] = count
    return sorted(result,key=lambda c:(len(c),c)),counts


def check_schema(schema,physical_data):
    fixed,visible,blocks,block_pairs,index,stars = physical_data
    need(schema['format'] == 'r55-antipodal-guarded-k5-v1' and schema['n'] == 43,'schema format/order')
    need(schema['visible_pairs'] == [list(e) for e in visible],'visible indices')
    need(schema['fixed_pairs'] == [[*e,int(c)] for e,c in sorted(fixed.items())],'all fixed colors')
    need(schema['blocks'] == [{'left':L,'right':R,'pairs':[list(e) for e in pairs]}
                             for (L,R),pairs in zip(blocks,block_pairs)],'block sides and row-major colors')
    targets = [20 if v in stars else 21 for v in range(43)]
    need(schema['degree_targets'] == targets,'physical target degrees')
    residuals = [{'vertex':v,'constant':targets[v]-sum(c for e,c in fixed.items() if v in e),
                  'subtract_variables':[index[e] for e in visible if v in e]} for v in range(43)]
    need(schema['residuals'] == residuals,'all residual degree expressions')
    densities = []
    for root in (0,1):
        Q = sorted(set(range(43))-{root}-stars[root]); pairs = list(it.combinations(Q,2))
        densities.append({'root':root,'sum_variables':[index[e] for e in pairs if e in visible],
                          'equals':124-sum(fixed[e] for e in pairs if e in fixed)})
    need(schema['density_equalities'] == densities,'both density expressions')


def unpack(row,block_pairs,index):
    need(type(row) is list and len(row) == 2,'guarded record shape'); guard,support = row
    need(type(guard) is list and all(type(x) is int and 1 <= abs(x) <= 523 for x in guard), 'guard range')
    need(guard == sorted(set(guard)),'canonical guard')
    need(type(support) is list and len(support) <= 2,'support arity')
    row_literals = list(guard); owners = []
    for part in support:
        need(type(part) is list and len(part) == 2,'support part'); k,local = part
        need(type(k) is int and k in range(3),'block ID')
        need(type(local) is list and local and all(type(x) is int and 1 <= abs(x) <= len(block_pairs[k]) for x in local),
             'block literal range')
        need(local == sorted(set(local)),'canonical local literals'); owners.append(k)
        row_literals.extend(index[block_pairs[k][abs(x)-1]]*(1 if x > 0 else -1) for x in local)
    need(owners == sorted(set(owners)),'distinct sorted block ownership')
    need(row_literals and len({x > 0 for x in row_literals}) == 1,'single-color physical prohibition')
    return tuple(sorted(row_literals))


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a = p.parse_args(); data = physical(); fixed,visible,blocks,block_pairs,index,stars = data
    schema = json.loads((a.work/'schema.json').read_text()); check_schema(schema,data)
    expected,candidates = possible_clauses(fixed,index); counts = Counter(); samples = []
    with (a.work/'clauses.jsonl').open() as f:
        for line_number,physical_row in enumerate(expected):
            line = f.readline(); need(line,'missing physical clause')
            row = json.loads(line); actual = unpack(row,block_pairs,index)
            need(actual == physical_row,'entrywise physical global clause '+str(line_number))
            support = row[1]; shape = tuple(sorted(len(xs) for k,xs in support))
            if len(support) == 1:
                k,xs = support[0]; pairs = [block_pairs[k][abs(x)-1] for x in xs]
                L,R = blocks[k]; lp = {v for e in pairs for v in e if v in L}; rp = {v for e in pairs for v in e if v in R}
                need({tuple(sorted((u,v))) for u in lp for v in rp} == set(pairs),'complete single-block rectangle')
                need(len(lp)+len(rp) <= 5,'rectangle vertex support')
            elif len(support) == 2:
                need(shape in ((1,1),(1,2)),'cross-block width')
                for k,xs in support:
                    if len(xs) == 2:
                        pairs = [set(block_pairs[k][abs(x)-1]) for x in xs]
                        need(len(pairs[0] & pairs[1]) == 1,'cross-block two-edge wedge')
            counts[','.join(map(str,shape)) if shape else 'visible-only'] += 1
            if len(samples) < 3 and len(support) == len(samples):
                samples.append(row)
        need(f.read() == '', 'no extra clause after complete physical stream')
    # A separate finite test of the abstract support bound: all five-vertex
    # occupancies among six bipartition sides and the outside cell.
    occupancies = 0
    for placement in it.combinations_with_replacement(range(7),5):
        sizes = Counter(placement); products = [sizes[2*k]*sizes[2*k+1] for k in range(3)]
        nonzero = sorted(p for p in products if p)
        need(len(nonzero) <= 2 and (len(nonzero) != 2 or nonzero in ([1,1],[1,2])),'abstract block support')
        need(not nonzero or max(nonzero) <= 6,'abstract width six'); occupancies += 1
    controls = []
    def reject(row,expected_row,tag):
        try:
            need(unpack(row,block_pairs,index) == expected_row,tag)
        except (ValueError,IndexError,KeyError,TypeError):
            controls.append(tag); return
        raise ValueError('corrupt record accepted: '+tag)
    need(len(samples) == 3,'samples at all arities')
    sample = samples[2]; wanted = unpack(sample,block_pairs,index)
    import copy
    r = copy.deepcopy(sample); r[1].pop(); reject(r,wanted,'omitted_block')
    r = copy.deepcopy(sample); r[1][0][0] = r[1][1][0]; reject(r,wanted,'aliased_block')
    r = copy.deepcopy(sample); r[1][0][1][0] *= -1; reject(r,wanted,'reversed_hidden_color')
    r = copy.deepcopy(sample); r[0].pop(); reject(r,wanted,'omitted_visible_guard')
    r = copy.deepcopy(sample); r[1].append([2,[1]]); reject(r,wanted,'third_block')
    r = copy.deepcopy(sample); r[1][0][1][0] = 99; reject(r,wanted,'out_of_range_hidden_edge')
    report = {'status':'EXACT_GUARDED_PHYSICAL_DECOMPOSITION_VERIFIED','physical_clauses':len(expected),
              'candidate_five_sets':candidates,'shape_counts':dict(sorted(counts.items())),
              'abstract_occupancy_patterns':occupancies,'rejected_record_controls':controls,
              'schema_sha256':sha(a.work/'schema.json'),'clauses_sha256':sha(a.work/'clauses.jsonl')}
    dump(a.report,report); print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
