"""Share the triangle part of every width-9/10 target clause."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'ramsey_r55_global_maximal_packing'
PARENT_COMMIT = '1884881efbf52a54bd3a30b1445c211da7caec27'
PARENT_MANIFEST = '4b5eef01603081a0777d5d3cd060b4ba59f48922e101221024b7e7dd29417f2b'


def parent():
    manifest = PARENT/'SHA256SUMS'
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != PARENT_MANIFEST:
        raise ValueError('maximal-packing source manifest identity')
    for line in manifest.read_text().splitlines():
        wanted, name = line.split('  ', 1)
        if hashlib.sha256((PARENT/name).read_bytes()).hexdigest() != wanted:
            raise ValueError('changed maximal-packing source: '+name)
    sys.path.insert(0, str(PARENT))
    module = importlib.import_module('family')
    if Path(module.__file__).resolve().parent != PARENT.resolve():
        raise ValueError('wrong parent module')
    return module


def long_anchor(task, vertices, color, clause):
    """Return the color-literals whose conjunction is shared by this clause."""
    if len(clause) == 10:
        anchor = tuple(vertices[:3])
    elif len(clause) == 9:
        fixed = [edge for edge in combinations(vertices, 2) if edge in task.fixed]
        if len(fixed) != 1 or task.fixed[fixed[0]] != color:
            raise ValueError('width-nine structure')
        anchor = tuple(sorted((*fixed[0], next(v for v in vertices if v not in fixed[0]))))
    else:
        return None
    inputs = tuple((1 if color else -1)*task.variables[edge]
                   for edge in combinations(anchor, 2) if edge in task.variables)
    if len(inputs) != (3 if len(clause) == 10 else 2):
        raise ValueError('anchor variable count')
    return (color, anchor), inputs


def target_records(task):
    for vertices in combinations(range(43), 5):
        for color in (1, 0):
            clause = task.forbid(vertices, color)
            if clause is not None:
                yield vertices, color, clause


def plan(task):
    inputs = {}; uses = Counter(); long_counts = Counter()
    for vertices, color, clause in target_records(task):
        item = long_anchor(task, vertices, color, clause)
        if item is not None:
            key, values = item
            if key in inputs and inputs[key] != values:
                raise ValueError('anchor input identity')
            inputs[key] = values; uses[key] += 1; long_counts[len(clause)] += 1
    keys = sorted(inputs)
    first = len(task.variables)+2
    variables = {key: first+i for i, key in enumerate(keys)}
    return {'inputs': inputs, 'uses': uses, 'variables': variables,
            'long_counts': dict(sorted(long_counts.items()))}


def definition_clauses(plan_data):
    for key, variable in plan_data['variables'].items():
        inputs = plan_data['inputs'][key]
        for literal in inputs:
            yield (-variable, literal)
        yield (variable, *(-literal for literal in inputs))


def clauses(task, plan_data):
    yield 'constant', (1,)
    for clause in task.root_clauses():
        yield 'root_order', clause
    for clause in definition_clauses(plan_data):
        yield 'triangle_definitions', clause
    for vertices, color, clause in target_records(task):
        item = long_anchor(task, vertices, color, clause)
        if item is None:
            yield 'target', clause
        else:
            key, inputs = item
            remove = {abs(x) for x in inputs}
            rest = tuple(x for x in clause if abs(x) not in remove)
            yield 'target', (-plan_data['variables'][key], *rest)
    for vertices in combinations(range(4*task.r, 43), 4):
        clause = task.forbid(vertices, 1)
        if clause is not None:
            yield 'red_four_closure', clause


def measure(task, plan_data, with_hash=False):
    base = task.dimensions(); base_hist = Counter(); new_hist = Counter()
    base_literals = 0; new_literals = 0; sections = Counter()
    for clause in task.clauses():
        base_hist[len(clause)] += 1; base_literals += len(clause)
    digest = hashlib.sha256() if with_hash else None; size = 0
    factored_variables = max(plan_data['variables'].values())
    factored_clauses = base['clauses'] + sum(len(x)+1 for x in plan_data['inputs'].values())
    if digest is not None:
        header = f"p cnf {factored_variables} {factored_clauses}\n".encode()
        digest.update(header); size += len(header)
    for section, clause in clauses(task, plan_data):
        new_hist[len(clause)] += 1; new_literals += len(clause); sections[section] += 1
        if digest is not None:
            line = (' '.join(map(str, clause))+' 0\n').encode()
            digest.update(line); size += len(line)
    k_counts = Counter(len(plan_data['inputs'][key]) for key in plan_data['variables'])
    theoretical = sum(plan_data['uses'][key]*(len(plan_data['inputs'][key])-1)
                      -(3*len(plan_data['inputs'][key])+1) for key in plan_data['variables'])
    if base_literals-new_literals != theoretical:
        raise ValueError('literal reduction identity')
    if max(base_hist) != 10 or max(new_hist) != 8 or theoretical <= 0:
        raise ValueError('tractability gate')
    result = {'task': task.name, 'q': task.q, 'r': task.r, 'core': task.c,
            'physical_variables': len(task.variables),
            'base_variables': base['variables'], 'factored_variables': factored_variables,
            'triangle_variables': len(plan_data['variables']),
            'triangle_variables_by_input_count': dict(sorted(k_counts.items())),
            'base_clauses': base['clauses'], 'factored_clauses': sum(new_hist.values()),
            'definition_clauses': sections['triangle_definitions'],
            'target_clauses': sections['target'], 'closure_clauses': sections['red_four_closure'],
            'base_literals': base_literals, 'factored_literals': new_literals,
            'literal_reduction': theoretical,
            'base_max_width': max(base_hist), 'factored_max_width': max(new_hist),
            'base_histogram': dict(sorted(base_hist.items())),
            'factored_histogram': dict(sorted(new_hist.items())),
            'long_target_clauses': plan_data['long_counts']}
    if sum(new_hist.values()) != factored_clauses:
        raise ValueError('factored clause formula')
    if digest is not None:
        result.update({'bytes': size, 'sha256': digest.hexdigest()})
    return result


def dimensions(task, plan_data):
    return measure(task, plan_data)


def virtual_formula(task, plan_data):
    return measure(task, plan_data, True)


def write(task, path):
    plan_data = plan(task); metadata = dimensions(task, plan_data); path = Path(path)
    with path.open('xb') as stream:
        stream.write(f"p cnf {metadata['factored_variables']} {metadata['factored_clauses']}\n".encode())
        for _, clause in clauses(task, plan_data):
            stream.write((' '.join(map(str, clause))+' 0\n').encode())
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    virtual = virtual_formula(task, plan_data)
    if path.stat().st_size != virtual['bytes'] or actual != virtual['sha256']:
        raise ValueError('written formula identity')
    return virtual


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('cache', type=Path)
    parser.add_argument('--task', required=True); parser.add_argument('--cnf', type=Path)
    args = parser.parse_args(); family = parent(); task = family.Task(args.task, args.cache)
    result = write(task, args.cnf) if args.cnf else virtual_formula(task, plan(task))
    print(json.dumps(result, indent=2, sort_keys=True))
