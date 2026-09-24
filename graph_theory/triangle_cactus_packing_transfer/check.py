"""Exact finite author audit. Run: python3 check.py

Calls the algorithms, then checks their choices and traces from definitions.
It does not import a universal design constructor or infer all-order theorems
from finite checks. Assertion statements are deliberately not used.
"""

from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from random import Random

from assembly import assemble, block_plan
from fixtures import affine_blocks, separated_classes
from rounding import label_and_orient, round_options


def check(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      default=lambda x: str(x) if isinstance(x, Q) else list(x)).encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def audit_rounding(groups, sparsity, certificate):
    """Replay supplied moves without using the constructor's linear algebra."""
    weights, ranges, row_sets = [], [], defaultdict(set)
    for group in groups:
        first = len(weights)
        for option in group:
            j = len(weights)
            weights.append(Q(option['weight']))
            check(len(set(option['rows'])) == len(option['rows']), 'nonbinary input')
            check(len(option['rows']) <= sparsity, 'bad input sparsity')
            for row in option['rows']:
                row_sets[row].add(j)
        ranges.append(list(range(first, len(weights))))
        check(sum(weights[j] for j in ranges[-1]) == 1, 'bad group sum')
    names = sorted(row_sets, key=repr)
    check(names == certificate['rows'], 'row metadata mismatch')
    rows = [row_sets[name] for name in names]
    start = [sum(weights[j] for j in row) for row in rows]
    active, protected_moves = set(range(len(rows))), 0
    for record in certificate['trace']:
        floating = {j for j, x in enumerate(weights) if 0 < x < 1}
        for r in record['dropped']:
            check(r in active, 'duplicate row removal')
            check(len(rows[r] & floating) <= 2*sparsity, 'early row removal')
            check(sum(weights[j] for j in rows[r]) == start[r],
                  'row drift before removal')
            active.remove(r)
        direction = dict(record['direction'])
        check(len(direction) == len(record['direction']) and direction,
              'malformed direction')
        check(all(j in floating and value != 0 for j, value in direction.items()),
              'direction changes a frozen variable')
        for ids in ranges:
            check(sum(direction.get(j, 0) for j in ids) == 0,
                  'hard item equation violated')
        for r in active:
            check(sum(direction.get(j, 0) for j in rows[r]) == 0,
                  'retained soft row violated')
        protected_moves += bool(active)
        step = record['step']
        check(step == min((1-weights[j])/d if d > 0 else -weights[j]/d
                          for j, d in direction.items()) and step > 0,
              'incorrect boundary step')
        for j, d in direction.items():
            weights[j] += step*d
        check(all(0 <= x <= 1 for x in weights), 'move outside cube')
        check(sum(0 < x < 1 for x in weights) < len(floating), 'no strict progress')
    choices = []
    for ids in ranges:
        check(all(weights[j] in (0, 1) for j in ids), 'fractional terminal option')
        selected = [k for k, j in enumerate(ids) if weights[j] == 1]
        check(len(selected) == 1, 'terminal choice not unique')
        choices.append(selected[0])
    check(choices == certificate['choices'], 'choice decoding mismatch')
    errors = [abs(sum(weights[j] for j in row)-start[r])
              for r, row in enumerate(rows)]
    check(all(e <= 2*sparsity for e in errors), 'soft discrepancy too large')
    return {'moves': len(certificate['trace']), 'protected_moves': protected_moves,
            'maximum_error': str(max(errors, default=Q(0))), 'rows': len(rows)}


def rounding_cases():
    h = sha256()
    cases, moves, protected = 0, 0, 0
    # Exhaustive small 0/1 incidence matrices and nontrivial rational weights.
    # All soft rows here are small; retained-row behavior is tested separately.
    for masks in product(range(4), repeat=4):
        for a, b in product((Q(1, 3), Q(1, 2), Q(2, 3)), repeat=2):
            groups = []
            for g, probability in enumerate((a, b)):
                group = []
                for k, w in enumerate((probability, 1-probability)):
                    mask = masks[2*g+k]
                    group.append({'weight': w,
                                  'rows': tuple(r for r in range(2) if mask >> r & 1)})
                groups.append(group)
            certificate = round_options(groups, 2)
            report = audit_rounding(groups, 2, certificate)
            h.update(encoded([masks, a, b, certificate, report]))
            cases += 1
            moves += report['moves']
    exhaustive = cases
    rng = Random(2026092415)
    stress_hash = sha256()
    for n in (12, 24, 48):
        for options in (2, 3, 4):
            for repetition in range(3):
                groups = []
                for g in range(n):
                    weights = [rng.randrange(1, 8) for _ in range(options)]
                    total = sum(weights)
                    group = []
                    for k, w in enumerate(weights):
                        # A global label row and three overlapping incidence rows.
                        rows = (('label', k), ('a', g % 3, k),
                                ('b', (g+k) % 4), ('c', rng.randrange(4)))
                        group.append({'weight': Q(w, total), 'rows': rows})
                    groups.append(group)
                cert = round_options(groups, 4)
                report = audit_rounding(groups, 4, cert)
                stress_hash.update(encoded([n, options, repetition, groups, cert, report]))
                cases += 1
                moves += report['moves']
                protected += report['protected_moves']
    check(protected > 0, 'no retained-row stress exercised')
    return {'exhaustive_small_cases': exhaustive, 'retained_row_stress_cases': 27,
            'replayed_moves': moves, 'moves_with_retained_rows': protected,
            'seed': 2026092415, 'exhaustive_sha256': h.hexdigest(),
            'stress_sha256': stress_hash.hexdigest()}


def audit_labels(copies, classes, specs, lists, certificate):
    size = len(specs[0]['roles'])
    masses = [Q(s['mass']) for s in specs]
    total, count = sum(masses), len(copies)
    # Recompute all allowed labeled bijections and their exact row weights.
    for copy, group in zip(copies, certificate['groups']):
        expected = []
        for ell, spec in enumerate(specs):
            allowed = [p for p in permutations(copy)
                       if [classes[v] for v in p] == list(spec['classes'])]
            if masses[ell] == 0:
                continue
            for p in allowed:
                expected.append((ell, p, masses[ell]/(total*len(allowed))))
        actual = [(o['label'], o['image'], o['weight']) for o in group]
        check(actual == expected, 'option weight or bijection error')
        for o in group:
            spec = specs[o['label']]
            expected_rows = [('count', o['label'])]
            expected_rows += [('role', o['label'], u, v)
                              for u, v in zip(spec['roles'], o['image'])]
            check(tuple(expected_rows) == o['rows'], 'role row misencoded')
    check(len(copies) == len(certificate['groups']), 'missing base item')
    replay = audit_rounding(certificate['groups'], size+1, certificate['rounding'])
    assigned = [[] for _ in specs]
    for group, choice in zip(certificate['groups'], certificate['rounding']['choices']):
        o = group[choice]
        assigned[o['label']].append(o['image'])
    a = 2*(size+1)
    sizes = Counter(classes)
    incidences = Counter(v for copy in copies for v in copy)
    kind_counts = Counter(specs[0]['classes'])
    base_D = max((abs(Q(incidences[v])-Q(kind_counts[k]*count, sizes[k]))
                  for v, k in enumerate(classes) if k in kind_counts), default=Q(0))
    deficits, removed, max_role_error = Q(0), 0, Q(0)
    for ell, spec in enumerate(specs):
        check(len(assigned[ell]) == certificate['before_counts'][ell],
              'pretrim count mismatch')
        expected = assigned[ell][:int(masses[ell])] if spec['true'] else []
        check(lists[ell] == expected, 'trim output mismatch')
        if not spec['true']:
            continue
        mu = Q(count)*masses[ell]/total if total else Q(0)
        m = len(lists[ell])
        trimmed = len(assigned[ell])-m
        check(0 <= trimmed <= a and m <= masses[ell], 'trimming cap failed')
        check(abs(Q(m)-mu) <= 2*a, 'count transfer error')
        removed += trimmed
        deficits += masses[ell]-m
        for position, role in enumerate(spec['roles']):
            counter = Counter(copy[position] for copy in lists[ell])
            kind = spec['classes'][position]
            for v, k in enumerate(classes):
                if k == kind:
                    error = abs(Q(counter[v])-Q(m, sizes[k]))
                    max_role_error = max(error, max_role_error)
                    check(error <= base_D+4*a, 'lifted role discrepancy failed')
    true_count = sum(s['true'] for s in specs)
    check(deficits <= total-count+2*a*true_count, 'total block deficit failed')
    return {'copies': count, 'labels': len(specs), 'trimmed': removed,
            'true_deficit': str(deficits), 'base_discrepancy': str(base_D),
            'maximum_role_error': str(max_role_error), 'rounding': replay,
            'output_sha256': digest(lists), 'trace_sha256': digest(certificate)}


def labeling_cases():
    reports = []
    fixtures = []
    # Fractional targets below one force genuine deletion after rounding.
    fixtures.append(([(0, 1)], [0, 0], [
        {'mass': Q(1, 3), 'roles': (0, 1), 'classes': (0, 0), 'true': True},
        {'mass': Q(2, 3), 'roles': (3, 4), 'classes': (0, 0), 'true': True}]))
    # Repeated roles, six class-respecting orientations, and retained soft rows.
    for d, repetitions in ((2, 1), (3, 2)):
        groups, classes, x = affine_blocks([(0, 1, 2)], d, repetitions)
        copies = groups[0]
        specs = [{'mass': Q(x, 2), 'roles': roles, 'classes': (0, 0, 0), 'true': True}
                 for roles in ((0, 1, 2), (2, 3, 4))]
        fixtures.append((copies, classes, specs))
    # AAB and ABC types with unequal actual part sizes.
    fixtures.append(([(0, 1, 3), (0, 2, 4), (1, 2, 5)], [0]*3+[1]*5, [
        {'mass': Q(7, 4), 'roles': (0, 1, 2), 'classes': (0, 0, 1), 'true': True},
        {'mass': Q(9, 4), 'roles': (4, 5, 6), 'classes': (1, 0, 0), 'true': True}]))
    fixtures.append(([(0, 2, 5), (1, 3, 6)], [0]*2+[1]*3+[2]*4, [
        {'mass': Q(5, 3), 'roles': (0, 1, 2), 'classes': (0, 1, 2), 'true': True},
        {'mass': Q(4, 3), 'roles': (7, 8, 9), 'classes': (2, 0, 1), 'true': True}]))
    fixtures.append(([(0, 2), (1, 3), (0, 4), (1, 2)], [0]*2+[1]*4, [
        {'mass': Q(9, 4), 'roles': (0, 1), 'classes': (0, 1), 'true': True},
        {'mass': Q(7, 4), 'roles': (0, 1), 'classes': (1, 0), 'true': False}]))
    fixtures.append(([], [0, 0], [
        {'mass': Q(0), 'roles': (0, 1), 'classes': (0, 0), 'true': True}]))
    fixtures.append(([], [0, 0, 0], [
        {'mass': Q(7, 9), 'roles': (0, 1, 2), 'classes': (0, 0, 0), 'true': True}]))
    for copies, classes, specs in fixtures:
        lists, certificate = label_and_orient(copies, classes, specs)
        reports.append(audit_labels(copies, classes, specs, lists, certificate))
    check(sum(r['trimmed'] for r in reports) > 0, 'no actual trimming case')
    check(sum(r['rounding']['protected_moves'] for r in reports) > 0,
          'no role lifting with protected rows')
    return reports


def audit_assembly(blocks, inputs, role_classes, classes, target,
                   output, certificate, supported_pairs=None):
    """Replay block choices independently, and inspect every output edge."""
    n, q = len(classes), len(role_classes)
    sizes = Counter(classes)
    raw_edges, D = set(), Q(0)
    for b, (roles, copies) in enumerate(zip(blocks, inputs)):
        check(len(copies) <= target, 'above-target block count')
        for copy in copies:
            check(len(copy) == len(roles) and len(set(copy)) == len(copy),
                  'malformed base instance')
            for role, vertex in zip(roles, copy):
                check(0 <= vertex < n and classes[vertex] == role_classes[role],
                      'input role class mismatch')
            for edge in combinations(copy, 2):
                edge = tuple(sorted(edge))
                check(edge not in raw_edges, 'input edge duplication')
                raw_edges.add(edge)
                if supported_pairs is not None:
                    pair = tuple(sorted(classes[v] for v in edge))
                    check(pair in supported_pairs, 'input uses nonexistent host edge')
        for j, role in enumerate(roles):
            counts = Counter(copy[j] for copy in copies)
            kind = role_classes[role]
            for v, k in enumerate(classes):
                if k == kind:
                    D = max(D, abs(Q(counts[v])-Q(len(copies), sizes[k])))
    seen_blocks, components = set(), []
    forbidden_pairs, failed_requests, stages = 0, 0, 0
    demand_discrepancy = Q(0)
    for record in certificate['components']:
        first = record['first']
        check(first not in seen_blocks, 'reused component root')
        seen_blocks.add(first)
        present = set(blocks[first])
        local_blocks = {first}
        partials = [dict(zip(blocks[first], copy)) for copy in inputs[first]]
        for stage in record['stages']:
            b, parent, role = stage['block'], stage['parent'], stage['role']
            check(b not in seen_blocks and parent in local_blocks,
                  'bad parent or repeated block')
            check(set(blocks[b]) & present == {role} and role in blocks[parent],
                  'attachment does not have exactly one old role')
            check(len(stage['choices']) == len(partials), 'wrong request trace length')
            position = blocks[b].index(role)
            candidates = defaultdict(list)
            for j, copy in enumerate(inputs[b]):
                candidates[copy[position]].append(j)
            available = set(range(len(inputs[b])))
            demands = Counter(p[role] for p in partials)
            parent_position = blocks[parent].index(role)
            raw_parent = Counter(copy[parent_position] for copy in inputs[parent])
            check(all(count <= raw_parent[v] for v, count in demands.items()),
                  'partial demand exceeds its original parent role list')
            kind = role_classes[role]
            for v, k in enumerate(classes):
                if k == kind:
                    demand_discrepancy = max(demand_discrepancy,
                        abs(Q(demands[v])-Q(len(partials), sizes[k])))
            matched = Counter()
            next_partials = []
            for partial, chosen in zip(partials, stage['choices']):
                v = partial[role]
                forbidden = set(partial.values()) - {v}
                incompatible = [j for j in candidates[v]
                                if forbidden.intersection(inputs[b][j])]
                check(len(incompatible) <= q-1, 'rooted collision bound failed')
                forbidden_pairs += len(incompatible)
                if chosen < 0:
                    check(all(j not in available or j in incompatible
                              for j in candidates[v]), 'discarded feasible request')
                    failed_requests += 1
                    continue
                check(chosen in available and chosen in candidates[v]
                      and chosen not in incompatible, 'invalid chosen attachment')
                available.remove(chosen)
                new = dict(partial)
                new.update(zip(blocks[b], inputs[b][chosen]))
                check(len(set(new.values())) == len(new), 'attachment collision')
                next_partials.append(new)
                matched[v] += 1
            for v, demand in demands.items():
                check(demand-matched[v] <= max(0, demand-len(candidates[v]))+q,
                      'one-sided greedy loss bound failed')
            delta = target-len(inputs[b])
            kind = role_classes[role]
            check(len(partials)-len(next_partials) <= delta+(2*D+q)*sizes[kind],
                  'parent domination loss bound failed')
            partials = next_partials
            present.update(blocks[b])
            seen_blocks.add(b)
            local_blocks.add(b)
            stages += 1
        components.append(partials)
    check(seen_blocks == set(range(len(blocks))), 'missing component block')
    partials = components[0]
    check(len(certificate['joins']) == len(components)-1, 'missing component join')
    for record, candidates in zip(certificate['joins'], components[1:]):
        check(len(record['choices']) == len(partials), 'bad join trace length')
        containing = Counter(v for copy in candidates for v in copy.values())
        check(all(value <= n-1 for value in containing.values()),
              'component vertex-incidence bound failed')
        available, joined = set(range(len(candidates))), []
        for partial, chosen in zip(partials, record['choices']):
            forbidden = set(partial.values())
            incompatible = {j for j, c in enumerate(candidates)
                            if forbidden.intersection(c.values())}
            check(len(incompatible) <= q*(n-1), 'free-join collision bound failed')
            forbidden_pairs += len(incompatible)
            if chosen < 0:
                check(available <= incompatible, 'discarded feasible free join')
                failed_requests += 1
                continue
            check(chosen in available and chosen not in incompatible,
                  'invalid free-join choice')
            available.remove(chosen)
            new = dict(partial)
            check(not set(new).intersection(candidates[chosen]), 'abstract components overlap')
            new.update(candidates[chosen])
            joined.append(new)
        check(target-len(joined) <= (target-len(partials))+(target-len(candidates))+q*n,
              'free-join deficit bound failed')
        partials = joined
    check(len(output) == len(partials) and len(output) <= target, 'wrong output count')
    pattern_edges = {tuple(sorted(edge)) for block in blocks for edge in combinations(block, 2)}
    output_edges = set()
    for image, partial in zip(output, partials):
        check(len(image) == q and len(set(image)) == q, 'noninjective output')
        check(all(image[u] == v for u, v in partial.items()), 'output changed retained role')
        for role, vertex in enumerate(image):
            check(0 <= vertex < n and classes[vertex] == role_classes[role],
                  'output role class mismatch')
        for u, v in pattern_edges:
            edge = tuple(sorted((image[u], image[v])))
            check(edge in raw_edges, 'output invented an edge')
            check(edge not in output_edges, 'output repeated an edge')
            output_edges.add(edge)
    block_deficit = sum(target-len(x) for x in inputs)
    bound = block_deficit+(len(blocks)-1)*(2*D+q)*n
    check(target-len(output) <= bound, 'assembly theorem inequality failed')
    # Uniform class-orbit averaging realizes the claimed input type mass.
    role_sizes = Counter(role_classes)
    check(all(sizes[k] >= v for k, v in role_sizes.items()), 'infeasible typed pattern')
    edge_types = Counter(tuple(sorted((role_classes[u], role_classes[v])))
                         for u, v in pattern_edges)
    for (i, j), multiplicity in edge_types.items():
        capacity = sizes[i]*sizes[j] if i != j else sizes[i]*(sizes[i]-1)//2
        check(target*multiplicity <= capacity, 'infeasible fractional type capacity')
    return {'vertices': n, 'pattern_vertices': q, 'pattern_edges': len(pattern_edges),
            'blocks': [list(b) for b in blocks], 'block_counts': list(map(len, inputs)),
            'target': str(target), 'assembled': len(output), 'covered_edges': len(output_edges),
            'local_role_discrepancy': str(D), 'deficit': str(target-len(output)),
            'maximum_partial_demand_discrepancy': str(demand_discrepancy),
            'assembly_loss_bound': str(bound), 'attachment_stages': stages,
            'forbidden_request_candidate_pairs': forbidden_pairs,
            'discarded_requests': failed_requests,
            'output_sha256': digest(output), 'trace_sha256': digest(certificate)}


def assembly_cases():
    patterns = [
        ('friendship_three', [(0, 1, 2), (0, 3, 4), (0, 5, 6)], 7),
        ('triangle_chain_bridge', [(0, 1, 2), (2, 3, 4), (4, 5), (5, 6, 7)], 8),
        ('branching_triangles', [(0, 1, 2), (0, 3, 4), (2, 5, 6)], 7),
        ('disconnected_and_isolated', [(0, 1, 2), (2, 3, 4), (5, 6, 7)], 9),
    ]
    reports = []
    for name, blocks, order in patterns:
        lists, classes, target = affine_blocks(blocks)
        output, trace = assemble(blocks, lists, [0]*order, classes)
        report = audit_assembly(blocks, lists, [0]*order, classes, Q(target), output, trace)
        report['name'] = name
        reports.append(report)
    # Unequal class sizes, independent cells, and only the pattern's cross pairs.
    blocks = patterns[1][1]
    sizes = [3, 5, 8, 13, 21, 34, 55, 89]
    lists, classes, target = separated_classes(blocks, sizes)
    output, trace = assemble(blocks, lists, list(range(8)), classes)
    pairs = {tuple(sorted(e)) for block in blocks for e in combinations(block, 2)}
    report = audit_assembly(blocks, lists, list(range(8)), classes, Q(target), output, trace, pairs)
    report['name'] = 'unequal_independent_classes'
    report['class_sizes'] = sizes
    reports.append(report)
    # Genuine missing blocks, with the actual local discrepancy measured exactly.
    lists, classes, target = affine_blocks(blocks, 5, 2)
    lists = [copies[:len(copies)-(3*b+1)] for b, copies in enumerate(lists)]
    output, trace = assemble(blocks, lists, [0]*8, classes)
    report = audit_assembly(blocks, lists, [0]*8, classes, Q(target), output, trace)
    report['name'] = 'unequal_block_deficits'
    reports.append(report)
    check(reports[0]['assembled'] == int(reports[0]['target']), 'friendship unexpectedly lost copies')
    check(sum(r['forbidden_request_candidate_pairs'] for r in reports) > 0,
          'no actual collision exercised')
    check(all(r['assembled'] > 0 for r in reports), 'empty positive fixture')
    return reports


def orbit_cases():
    """Enumerate literal labeled F copies to check the capacity-profile bridge."""
    cases = [
        ([(0, 1, 2), (2, 3, 4)], [0]*5, [0]*6),
        ([(0, 1, 2), (2, 3, 4)], [1, 2, 0, 1, 2], [0]*2+[1]*3+[2]*3),
        ([(0, 1, 2), (2, 3)], [0, 0, 1, 0], [0]*4+[1]*3),
        ([(0, 1), (2, 3)], [0, 1, 0, 1, 0], [0]*4+[1]*3),
    ]
    results = []
    for blocks, role_classes, classes in cases:
        q, n = len(role_classes), len(classes)
        abstract = {tuple(sorted(e)) for b in blocks for e in combinations(b, 2)}
        frequencies, count = Counter(), 0
        for image in permutations(range(n), q):
            if any(classes[v] != role_classes[u] for u, v in enumerate(image)):
                continue
            count += 1
            for u, v in abstract:
                frequencies[tuple(sorted((image[u], image[v])))] += 1
        sizes = Counter(classes)
        types = Counter(tuple(sorted((role_classes[u], role_classes[v]))) for u, v in abstract)
        for u, v in combinations(range(n), 2):
            i, j = sorted((classes[u], classes[v]))
            cap = sizes[i]*sizes[j] if i != j else sizes[i]*(sizes[i]-1)//2
            check(Q(frequencies[(u, v)], count) == Q(types[(i, j)], cap),
                  'uniform orbit edge-load identity failed')
        results.append({'embeddings': count, 'pattern_vertices': q,
                        'host_vertices': n, 'edge_loads_sha256': digest(sorted(frequencies.items()))})
    return results


def family_pipeline():
    """Full balanced base profile -> labels/roles -> two pattern objectives."""
    raw, classes, count = affine_blocks([(0, 1, 2)], 3, 2)
    copies = raw[0]
    x = Q(count, 3)
    # The first two labels are one bowtie; the third is a separate K3 type.
    blocks = [(0, 1, 2), (2, 3, 4), (0, 1, 2)]
    specs = [{'mass': x, 'roles': b, 'classes': (0, 0, 0), 'true': True}
             for b in blocks]
    lists, rounding = label_and_orient(copies, classes, specs)
    lifting = audit_labels(copies, classes, specs, lists, rounding)
    n = len(classes)
    triangle_edges = [tuple(sorted(e)) for copy in copies for e in combinations(copy, 2)]
    check(len(set(triangle_edges)) == len(triangle_edges), 'pipeline base edge collision')
    residual = set(combinations(range(n), 2)) - set(triangle_edges)
    residue_degrees = Counter(v for e in residual for v in e)
    triangle_degrees = Counter(v for copy in copies for v in copy)
    check(all(Q(triangle_degrees[v]) == Q(3*count, n) for v in range(n)),
          'pipeline base triangle roles are unbalanced')
    check(all(Q(residue_degrees[v]) == Q(2*len(residual), n) for v in range(n)),
          'pipeline base slack roles are unbalanced')
    check(3*count+len(residual) == n*(n-1)//2, 'pipeline profile is not full')
    family_outputs, reports = [], []
    for chosen, pattern_order in (([0, 1], 5), ([2], 3)):
        pattern_blocks = [blocks[j] for j in chosen]
        inputs = [lists[j] for j in chosen]
        output, trace = assemble(pattern_blocks, inputs, [0]*pattern_order, classes)
        report = audit_assembly(pattern_blocks, inputs, [0]*pattern_order,
                                classes, x, output, trace)
        pattern_edges = {tuple(sorted(e)) for b in pattern_blocks for e in combinations(b, 2)}
        family_outputs.extend(tuple(sorted((image[u], image[v])))
                              for image in output for u, v in pattern_edges)
        reports.append(report)
    check(len(family_outputs) == len(set(family_outputs)),
          'assembled family objectives reuse an edge')
    check(all(report['assembled'] > 0 for report in reports), 'empty family objective')
    return {'host_order': n, 'fractional_target_per_pattern': str(x),
            'base_triangle_count': count, 'slack_edge_count': len(residual),
            'base_component_loss': 0, 'base_role_discrepancy': 0,
            'lifting': lifting, 'patterns': reports,
            'family_edges': len(family_outputs), 'family_edges_sha256': digest(sorted(family_outputs))}


def negative_controls():
    passed = []

    def reject(name, function):
        try:
            function()
        except (ValueError, IndexError):
            passed.append(name)
        else:
            raise ValueError('negative control accepted: '+name)

    reject('bad_item_sum', lambda: round_options([[{'weight': Q(1, 2), 'rows': ()}]], 1))
    reject('duplicate_soft_row', lambda: round_options([[{'weight': 1, 'rows': (0, 0)}]], 2))
    reject('sparsity_violation', lambda: round_options([[{'weight': 1, 'rows': (0, 1)}]], 1))
    groups = [[{'weight': Q(1, 2), 'rows': (0,)}, {'weight': Q(1, 2), 'rows': (1,)}]]
    bad = deepcopy(round_options(groups, 1))
    bad['trace'][0]['direction'][0] = (bad['trace'][0]['direction'][0][0], Q(5))
    reject('tampered_null_direction', lambda: audit_rounding(groups, 1, bad))
    reject('two_vertex_gluing', lambda: block_plan([(0, 1, 2), (0, 1, 3)], 4))
    reject('cycle_of_edge_blocks', lambda: block_plan([(0, 1), (1, 2), (2, 3), (3, 0)], 4))
    reject('duplicate_input_edge', lambda: assemble([(0, 1), (1, 2)],
            [[(0, 1)], [(0, 1)]], [0]*3, [0]*3))
    reject('role_class_mismatch', lambda: assemble([(0, 1)], [[(0, 1)]], [0, 1], [0, 0]))
    reject('infeasible_isolated_role', lambda: assemble([(0, 1)], [[(0, 1)]], [0]*3, [0]*2))
    blocks, inputs, classes = [(0, 1)], [[(0, 1)]], [0]*3
    output, trace = assemble(blocks, inputs, [0]*3, classes)
    bad_output = [(0, 1, 1)]
    reject('noninjective_decoding', lambda: audit_assembly(
        blocks, inputs, [0]*3, classes, Q(1), bad_output, trace))
    return passed


def main():
    result = {'scope': 'finite author audit of rounding and assembly; base design theorem imported',
              'rounding': rounding_cases(), 'labeling': labeling_cases(),
              'assembly': assembly_cases(), 'orbit_averaging': orbit_cases(),
              'family_pipeline': family_pipeline(),
              'negative_controls': negative_controls(), 'status': 'PASS'}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
