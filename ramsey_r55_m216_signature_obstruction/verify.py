#!/usr/bin/env python3
"""Exact, solver-free proof replay and literal Ramsey deletion checks.

The proof path reconstructs clauses by literal five-subsets, not by the
root-clique construction in model.py. No submitted/source-witness module,
SAT solver, proof-trimmer, floating arithmetic, or graph catalog is imported.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_SHA = '61c0953591ffe94ee2d61efeeab5f9d60cbc5f6278f1cc4fa7ab468a66968372'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def literal_layout(template, deleted=None):
    k = template['core_order']
    labels = [None]*k
    for signature, count in template['cells']:
        labels.extend([signature]*count)
    vertices = tuple(v for v in range(len(labels)) if v != deleted)
    # Number bits by an explicit upper-triangular walk, independent of model.py.
    core = {}
    bit = 0
    for u in range(k):
        for v in range(u+1, k):
            core[u, v] = (template['core_mask'] >> bit) & 1
            bit += 1
    fixed, variable_pairs = {}, []
    for u in vertices:
        for v in vertices:
            if u >= v:
                continue
            if v < k:
                fixed[u, v] = core[u, v]
            elif u < k:
                fixed[u, v] = (labels[v] >> u) & 1
            else:
                variable_pairs.append((u, v))
    return vertices, fixed, tuple(variable_pairs)


def literal_formula(template, deleted=None, full=False):
    vertices, fixed, variables = literal_layout(template, deleted)
    index = {edge: i+1 for i, edge in enumerate(variables)}
    parents = {}
    for five in combinations(vertices, 5):
        if not full and not any(v < template['core_order'] for v in five):
            continue
        edges = tuple(combinations(five, 2))
        known = {fixed[e] for e in edges if e in fixed}
        for color in (0, 1):
            if known - {color}:
                continue
            clause = tuple(sorted((-index[e] if color else index[e])
                                  for e in edges if e not in fixed))
            parents.setdefault(clause, (five, color))
    return variables, parents


def parse_cnf(path, variable_count):
    clauses, header = [], None
    for line in path.read_text().splitlines():
        if not line or line.startswith('c '):
            continue
        if line.startswith('p '):
            require(header is None, 'duplicate header')
            words = line.split()
            require(len(words) == 4 and words[:2] == ['p', 'cnf'], 'bad header')
            header = tuple(map(int, words[2:]))
            continue
        clause = parse_clause(line, variable_count)
        clauses.append(clause)
    require(header == (variable_count, len(clauses)), 'CNF dimensions')
    require(len(set(clauses)) == len(clauses), 'duplicate support clause')
    return tuple(clauses)


def parse_clause(line, variable_count):
    row = tuple(map(int, line.split()))
    require(bool(row) and row[-1] == 0 and 0 not in row[:-1], 'clause terminator')
    clause = tuple(sorted(row[:-1]))
    require(all(1 <= abs(lit) <= variable_count for lit in clause), 'variable range')
    require(len(set(clause)) == len(clause), 'repeated literal')
    require(not any(-lit in clause for lit in clause), 'tautological certificate clause')
    return clause


def rup(premises, conclusion):
    """Negate the proposed clause, then scan literally for forced units."""
    true_literals = {-literal for literal in conclusion}
    while True:
        forced = None
        for clause in premises:
            if any(literal in true_literals for literal in clause):
                continue
            undecided = [literal for literal in clause if -literal not in true_literals]
            if not undecided:
                return True
            if len(undecided) == 1:
                forced = undecided[0]
                break
        if forced is None:
            return False
        true_literals.add(forced)


def replay(support, proof):
    require(bool(proof) and proof[-1] == (), 'final empty clause missing')
    require(() not in proof[:-1], 'premature empty clause')
    current = list(support)
    for step, clause in enumerate(proof):
        require(rup(current, clause), f'unsupported RUP step {step}')
        current.append(clause)
    return len(proof)


def deletion_graph(template, record):
    deleted = record['deleted']
    require(type(deleted) is int and 0 <= deleted < 18, 'deletion vertex')
    vertices, fixed, variable_pairs = literal_layout(template, deleted)
    text = record['central_red_mask_hex']
    require(type(text) is str and text and all(c in '0123456789abcdef' for c in text), 'mask encoding')
    mask = int(text, 16)
    require(0 <= mask < 1 << len(variable_pairs), 'deletion mask range')
    edge_colors = dict(fixed)
    edge_colors.update({edge: (mask >> bit) & 1 for bit, edge in enumerate(variable_pairs)})
    count = 0
    for five in combinations(vertices, 5):
        require(len({edge_colors[e] for e in combinations(five, 2)}) == 2,
                f'monochromatic K5 after deleting {deleted}: {five}')
        count += 1
    return count


def embedding(template, source):
    record = source['record']
    require(record['core_mask'] == template['core_mask'], 'source core mismatch')
    source_cells = dict(record['cells'])
    require(all(source_cells.get(s, 0) >= n for s, n in template['cells']), 'threshold cut not violated')
    labels = [None]*template['core_order']
    for s, n in sorted(source_cells.items()):
        labels.extend([s]*n)
    selected = list(range(template['core_order']))
    for s, n in template['cells']:
        selected.extend([v for v, t in enumerate(labels) if t == s][:n])
    require(len(selected) == len(set(selected)) == 18, 'bad source embedding')
    return selected


def small_controls():
    """All 1024 complete five-vertex colorings, with six choices of root prefix."""
    from model import formula
    tested = 0
    pairs = tuple(combinations(range(5), 2))
    for mask in range(1024):
        colors = {e: (mask >> bit) & 1 for bit, e in enumerate(pairs)}
        valid = mask not in (0, 1023)
        for k in range(6):
            core_mask = sum(colors[e] << bit for bit, e in enumerate(combinations(range(k), 2)))
            cells = [[sum(colors[u, v] << u for u in range(k)), 1] for v in range(k, 5)]
            t = {'core_order': k, 'core_mask': core_mask, 'cells': cells}
            variables, reference = literal_formula(t, full=True)
            other_variables, clauses = formula(t, full=True)
            require(variables == other_variables and set(reference) == set(clauses), 'small formula mismatch')
            values = {i+1: colors[e] for i, e in enumerate(variables)}
            satisfied = all(any(values[abs(lit)] == (lit > 0) for lit in clause) for clause in reference)
            require(satisfied == valid, 'five-vertex truth-table mismatch')
            tested += 1
    return tested


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path)
    p.add_argument('--certificate-dir', type=Path, default=HERE)
    args = p.parse_args()
    directory = args.certificate_dir
    template = json.loads((HERE/'TEMPLATE.json').read_text())
    require(template == {'core_order': 7, 'core_mask': 409383,
                        'cells': [[49,1],[50,2],[60,1],[73,2],[116,2],[120,3]],
                        'format': 'r55-seven-root-six-cell-obstruction-v1'}, 'template scope')
    variables, reference = literal_formula(template)
    require(len(variables) == 55 and len(reference) == 521, 'mixed formula size')
    # Secondary comparison does not participate in deriving the proof premises.
    from model import formula, dimacs
    other_variables, other_clauses = formula(template)
    require(variables == other_variables and set(reference) == set(other_clauses), 'full formula reconstruction')
    support = parse_cnf(directory/'SUPPORT.cnf', 55)
    require(set(support) <= set(reference), 'support clause not justified by a literal five-set')
    proof = tuple(parse_clause(line, 55) for line in (directory/'CERTIFICATE.rup').read_text().splitlines())
    steps = replay(support, proof)
    deletions = json.loads((directory/'DELETIONS.json').read_text())
    require(len(deletions) == 18 and sorted(r['deleted'] for r in deletions) == list(range(18)),
            'complete single-vertex deletion cover')
    five_checks = sum(deletion_graph(template, record) for record in deletions)
    raw_input = (HERE/'INPUT_EDGE_LIFT.json').read_bytes()
    require(hashlib.sha256(raw_input).hexdigest() == INPUT_SHA, 'incoming certificate provenance')
    source = json.loads(raw_input)
    selected = embedding(template, source)

    controls = []
    try:
        replay(support, proof[:-1])
    except ValueError:
        controls.append('missing_final_empty')
    else:
        raise ValueError('truncated proof accepted')
    unsupported = next((lit,) for lit in range(1,56) if not rup(support, (lit,)))
    try:
        replay(support, (unsupported, ()) )
    except ValueError:
        controls.append('unsupported_unit')
    else:
        raise ValueError('unproved unit accepted')
    missing_cell = deepcopy(source)
    missing_cell['record']['cells'] = [[s, max(0, n-1)] if s == 49 else [s,n]
                                     for s,n in missing_cell['record']['cells']]
    try:
        embedding(template, missing_cell)
    except ValueError:
        controls.append('missing_threshold_vertex')
    else:
        raise ValueError('false source embedding accepted')
    # Find, and then independently reject, one central-edge mutation of a
    # positive deletion witness. This tests Ramsey checking rather than hashes.
    mutation = None
    for record in deletions:
        _, _, pairs = literal_layout(template, record['deleted'])
        for bit in range(len(pairs)):
            altered = dict(record, central_red_mask_hex=format(int(record['central_red_mask_hex'],16) ^ (1 << bit),'x'))
            try:
                deletion_graph(template, altered)
            except ValueError:
                mutation = [record['deleted'], bit]
                break
        if mutation is not None:
            break
    require(mutation is not None, 'no failing deletion mutation found')
    controls.append('altered_deletion_edge')
    report = {
        'template_vertices': 18, 'exceptional_vertices': 7, 'central_vertices': 11,
        'central_edge_variables': len(variables), 'complete_mixed_clauses': len(reference),
        'mixed_clause_length_histogram': dict(sorted(Counter(map(len, reference)).items())),
        'support_clauses': len(support), 'support_variables': len({abs(lit) for c in support for lit in c}),
        'rup_additions_including_empty': steps,
        'vertex_deletion_witnesses': len(deletions), 'literal_five_sets_checked_in_deletions': five_checks,
        'small_truth_table_cases': small_controls(), 'negative_controls_rejected': controls,
        'failing_deletion_mutation': mutation, 'unsupported_unit_control': list(unsupported),
        'source_certificate_sha256': INPUT_SHA, 'source_embedding': selected,
        'formula_sha256': hashlib.sha256(dimacs(variables, other_clauses).encode()).hexdigest(),
        'certificate_sha256': hashlib.sha256((directory/'CERTIFICATE.rup').read_bytes()).hexdigest(),
        'scope': 'one vertex-minimal partial-coloring obstruction; not a whole-profile exclusion',
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
