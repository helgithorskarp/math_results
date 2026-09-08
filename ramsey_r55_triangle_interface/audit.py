"""Independent physical reconstruction, projection controls, and full comparisons."""
from collections import Counter
from itertools import combinations, product, zip_longest
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import time
import factor

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent/'ramsey_r55_global_maximal_packing'/'INPUTS.json'
REPRESENTATIVES = HERE.parent/'ramsey_r55_global_maximal_packing'/'FORMULA_AUDIT.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def physical(name, cache):
    prefix, Q, R, C = name.split('-'); q = int(Q[1:]); r = int(R[1:]); index = int(C[1:])
    require(prefix == 'mp1' and 7 <= q <= 10 and 5 <= r <= q, 'task syntax')
    n = 43-4*q; spec = next(row for row in json.loads(INPUTS.read_text()) if row['n'] == n)
    path = Path(cache)/spec['name']; raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == spec['sha256'], 'catalog identity')
    records = raw.splitlines(); require(0 <= index < len(records) == spec['count'], 'catalog index')
    record = records[index]; values = [byte-63 for byte in record]
    require(values[0] == n and all(0 <= x < 64 for x in values), 'graph6 syntax')
    stream = ''.join(format(x, '06b') for x in values[1:])[:comb(n, 2)]
    require(len(stream) == comb(n, 2), 'graph6 length')
    fixed = {}; position = 0
    for v in range(1, n):
        for u in range(v):
            fixed[4*q+u, 4*q+v] = int(stream[position]); position += 1
    for block in range(q):
        for u, v in combinations(range(4*block, 4*block+4), 2):
            fixed[u, v] = int(block < r)
    variables = {}; next_variable = 2
    for edge in combinations(range(43), 2):
        if edge not in fixed:
            variables[edge] = next_variable; next_variable += 1
    require(next_variable-1 == 904-6*q-comb(n, 2), 'physical variable count')
    return {'name': name, 'q': q, 'r': r, 'n': n, 'fixed': fixed, 'variables': variables}


def forbid(data, vertices, color):
    fixed = data['fixed']; variables = data['variables']; answer = []
    for edge in combinations(vertices, 2):
        if edge in fixed:
            if fixed[edge] != color:
                return None
        else:
            answer.append((-1 if color else 1)*variables[edge])
    return tuple(answer)


def root_clauses(data):
    variables = data['variables']
    for block in range(1, data['q']):
        for column in range(3):
            for low in range(16):
                for high in range(low+1, 16):
                    clause = []
                    for vertex, word in [(4*block+column, low), (4*block+column+1, high)]:
                        for row in range(4):
                            clause.append(variables[row, vertex]*(1-2*((word >> row) & 1)))
                    yield tuple(clause)


def anchor(data, vertices, color, clause):
    if len(clause) == 10:
        chosen = tuple(vertices[:3])
    elif len(clause) == 9:
        fixed_edges = [edge for edge in combinations(vertices, 2) if edge in data['fixed']]
        require(len(fixed_edges) == 1 and data['fixed'][fixed_edges[0]] == color, 'width-nine fixed edge')
        chosen = tuple(sorted((*fixed_edges[0], min(set(vertices)-set(fixed_edges[0])))))
    else:
        return None
    inputs = tuple((1 if color else -1)*data['variables'][edge]
                   for edge in combinations(chosen, 2) if edge in data['variables'])
    require(len(inputs) == (3 if len(clause) == 10 else 2), 'anchor size')
    return (color, chosen), inputs


def independent_plan(data):
    inputs = {}; uses = Counter(); target_hist = Counter(); target_count = 0
    for vertices in combinations(range(43), 5):
        for color in (1, 0):
            clause = forbid(data, vertices, color)
            if clause is None:
                continue
            target_count += 1; target_hist[len(clause)] += 1
            item = anchor(data, vertices, color, clause)
            if item is not None:
                key, literals = item
                require(key not in inputs or inputs[key] == literals, 'anchor consistency')
                inputs[key] = literals; uses[key] += 1
    variables = {key: len(data['variables'])+2+i for i, key in enumerate(sorted(inputs))}
    return {'inputs': inputs, 'uses': uses, 'variables': variables,
            'target_count': target_count, 'target_hist': target_hist}


def independent_clauses(data, plan):
    yield 'constant', (1,)
    for clause in root_clauses(data):
        yield 'root_order', clause
    for key, variable in plan['variables'].items():
        literals = plan['inputs'][key]
        for literal in literals:
            yield 'triangle_definitions', (-variable, literal)
        yield 'triangle_definitions', (variable, *(-x for x in literals))
    for vertices in combinations(range(43), 5):
        for color in (1, 0):
            clause = forbid(data, vertices, color)
            if clause is None:
                continue
            item = anchor(data, vertices, color, clause)
            if item is None:
                yield 'target', clause
            else:
                key, literals = item; removed = {abs(x) for x in literals}
                yield 'target', (-plan['variables'][key], *(x for x in clause if abs(x) not in removed))
    for vertices in combinations(range(4*data['r'], 43), 4):
        clause = forbid(data, vertices, 1)
        if clause is not None:
            yield 'red_four_closure', clause


def compare_task(name, cache):
    data = physical(name, cache); independent = independent_plan(data)
    family = factor.parent(); task = family.Task(name, cache); produced = factor.plan(task)
    require(produced['inputs'] == independent['inputs'], 'producer/auditor anchor inputs')
    require(produced['uses'] == independent['uses'], 'producer/auditor anchor uses')
    require(produced['variables'] == independent['variables'], 'producer/auditor auxiliary numbering')
    variable_count = max(independent['variables'].values()); definition_count = sum(len(x)+1 for x in independent['inputs'].values())
    clause_count = task.dimensions()['clauses']+definition_count
    digest = hashlib.sha256(); size = 0; header = f'p cnf {variable_count} {clause_count}\n'.encode()
    digest.update(header); size += len(header); count = 0; literals = 0; histogram = Counter(); sections = Counter()
    for left, right in zip_longest(factor.clauses(task, produced), independent_clauses(data, independent)):
        require(left is not None and right is not None and left == right, f'literal mismatch at {count}')
        section, clause = right; line = (' '.join(map(str, clause))+' 0\n').encode()
        digest.update(line); size += len(line); count += 1; literals += len(clause)
        histogram[len(clause)] += 1; sections[section] += 1
    require(count == clause_count and max(histogram) == 8, 'factored dimensions')
    base_hist = Counter(); base_literals = 0
    base_hist[1] = 1
    for clause in root_clauses(data):
        base_hist[len(clause)] += 1; base_literals += len(clause)
    base_literals += 1
    for length, number in independent['target_hist'].items():
        base_hist[length] += number; base_literals += length*number
    closure_count = 0
    for vertices in combinations(range(4*data['r'], 43), 4):
        clause = forbid(data, vertices, 1)
        if clause is not None:
            base_hist[len(clause)] += 1; base_literals += len(clause); closure_count += 1
    require(sum(base_hist.values()) == task.dimensions()['clauses'], 'base clause reconstruction')
    reduction = base_literals-literals
    require(reduction == sum(independent['uses'][key]*(len(independent['inputs'][key])-1)
                             -(3*len(independent['inputs'][key])+1) for key in independent['variables']),
            'literal reduction identity')
    return {'task': name, 'q': data['q'], 'r': data['r'], 'core': int(name[-6:]),
            'base_variables': len(data['variables'])+1, 'factored_variables': variable_count,
            'triangle_variables': len(independent['variables']), 'base_clauses': sum(base_hist.values()),
            'factored_clauses': count, 'definition_clauses': definition_count,
            'base_literals': base_literals, 'factored_literals': literals,
            'literal_reduction': reduction, 'literal_reduction_ppm': reduction*1000000//base_literals,
            'base_max_width': max(base_hist), 'factored_max_width': max(histogram),
            'base_histogram': dict(sorted(base_hist.items())),
            'factored_histogram': dict(sorted(histogram.items())),
            'sections': dict(sorted(sections.items())), 'bytes': size, 'sha256': digest.hexdigest(),
            'audit': 'EVERY_LITERAL_MATCHED_FROM_INDEPENDENT_PHYSICAL_RECONSTRUCTION'}


def unit_propagate(clauses, assignment):
    values = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            undecided = []
            for literal in clause:
                variable = abs(literal)
                if variable in values:
                    if values[variable] == (literal > 0):
                        break
                else:
                    undecided.append(literal)
            else:
                if not undecided:
                    return None
                if len(undecided) == 1:
                    literal = undecided[0]; variable = abs(literal); value = literal > 0
                    if variable in values and values[variable] != value:
                        return None
                    if variable not in values:
                        values[variable] = value; changed = True
        if not changed:
            return values


def propagation_controls():
    total = 0
    for k in (2, 3):
        m = 7; auxiliary = k+m+1
        inputs = list(range(1, k+1)); rest = list(range(k+1, k+m+1))
        direct = [tuple([-x for x in inputs]+rest)]
        gadget = [(-auxiliary, x) for x in inputs]+[(auxiliary, *[-x for x in inputs]), (-auxiliary, *rest)]
        for states in product((-1, 0, 1), repeat=k+m):
            partial = {i+1: bool(value) for i, value in enumerate(states) if value >= 0}
            left = unit_propagate(direct, partial); right = unit_propagate(gadget, partial)
            require((left is None) == (right is None), 'partial-assignment conflict equivalence')
            if left is not None:
                for variable in range(1, k+m+1):
                    require(left.get(variable) == right.get(variable), 'projected unit propagation equivalence')
            total += 1
    malformed = 0
    for name in ('mp1-q6-r5-c000000', 'mp1-q7-r4-c000000', 'mp1-q7-r5-c999999'):
        try:
            physical(name, '.')
        except (ValueError, StopIteration, FileNotFoundError):
            malformed += 1
        else:
            raise ValueError('malformed task accepted')
    return {'status': 'VERIFIED_PROJECTED_UNIT_PROPAGATION_EQUIVALENCE',
            'partial_assignments': total, 'input_counts': [2, 3], 'remainder_literals': 7,
            'malformed_task_controls': malformed}


def universal_bounds():
    rows = []
    for q in range(7, 11):
        n = 43-4*q; fixed_edges = 6*q+comb(n, 2)
        width10 = 2*(comb(q, 5)*4**5+comb(q, 4)*4**4*n)
        three_anchor_bound = 2*comb(q, 3)*4**3
        two_anchor_bound = 41*fixed_edges
        guaranteed = 2*width10-10*three_anchor_bound-6*two_anchor_bound
        require(guaranteed > 0, 'universal literal reduction')
        rows.append({'q': q, 'core_order': n, 'fixed_edges': fixed_edges,
                     'width10_target_clauses_every_task': width10,
                     'three_input_anchor_upper_bound': three_anchor_bound,
                     'two_input_anchor_upper_bound': two_anchor_bound,
                     'literal_reduction_lower_bound': guaranteed})
    return {'status': 'PROVED_UNIFORM_TRACTABILITY_BOUNDS', 'tasks_covered': 2189178,
            'macro_classes': 18, 'base_max_width': 10, 'factored_max_width': 8, 'rows': rows,
            'derivation': 'Gross saving 2 per width-10 clause; charge 10 per possible 3-input anchor and worst net cost 6 per possible 2-input anchor.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('cache', type=Path)
    parser.add_argument('--shard', type=int, default=0); parser.add_argument('--shards', type=int, default=1)
    parser.add_argument('--output', type=Path); parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args(); require(0 <= args.shard < args.shards, 'shard range'); start = time.monotonic()
    tasks = [row['task'] for row in json.loads(REPRESENTATIVES.read_text())]
    chosen = tasks[args.shard::args.shards]
    result = {'controls': propagation_controls(), 'universal': universal_bounds(),
              'shard': args.shard, 'shards': args.shards, 'tasks': [] if args.controls_only else [compare_task(name, args.cache) for name in chosen]}
    result['seconds'] = time.monotonic()-start
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
