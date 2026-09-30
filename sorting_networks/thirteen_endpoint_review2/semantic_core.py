"""Direct semantic audit of the published core, without the full CNF or PySAT.

Only the relevant clause templates are generated. Counter fragments are
audited by all admissible input patterns and exact Horn least models.
"""
from collections import Counter
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canon(clause):
    return tuple(sorted(set(clause)))


def layout(certificate):
    top = 0
    variables = {}

    def allocate(kind, count):
        nonlocal top
        out = list(range(top + 1, top + count + 1))
        top += count
        for index, variable in enumerate(out):
            variables[variable] = (kind, index)
        return out

    def counter(kind, length, bound):
        require(0 <= bound <= length, 'Counter bound out of range')
        count = 0 if bound in (0, length - 1, length) else bound*(length - bound)
        return allocate(kind, count)

    n, slots = 11, 19
    pairs = list(combinations(range(n), 2))
    picks = allocate('pick', slots*len(pairs))
    picks = [picks[t*len(pairs):(t + 1)*len(pairs)] for t in range(slots)]
    use = allocate('use', slots*n)
    use = [use[t*n:(t + 1)*n] for t in range(slots)]
    for t in range(slots):
        counter(('selection_counter', t), len(pairs), 1)
    truth = allocate('truth', 1)[0]
    rows, hits, auxiliary = {}, {}, {}
    for record in certificate['single_threshold_bounds']:
        x = record['state']
        first = (x & -x).bit_length() - 1 if x else n
        last = ((2**n - 1) ^ x).bit_length() - 1
        active = max(0, last - first + 1)
        array = allocate(('row', x), (slots + 1)*active)
        rows[x] = [[-truth if i < first else truth if i > last else
                    array[t*active + i - first] for i in range(n)]
                   for t in range(slots + 1)]
        for polarity, bound in [('high', record['high_cap']), ('low', record['low_cap'])]:
            if bound >= slots:
                continue
            require(bound >= 0, 'Unexpected negative bound')
            hits[x, polarity] = allocate(('hits', x, polarity), slots)
            auxiliary[x, polarity] = counter(('counter', x, polarity), slots, bound)
    auxiliary['maximum'] = counter('maximum_counter', slots, 1)
    counter('minimum_counter', slots, 1)
    allocate('branch_low_hits', slots)
    counter('branch_low_counter', slots, 1)
    allocate('mixed_hits', slots)
    counter('mixed_counter', slots, 2)
    require(top == 40894, 'Literal namespace size')
    return pairs, picks, use, truth, rows, hits, auxiliary, variables


def horn_model(clauses, fixed, auxiliary):
    values = dict(fixed)
    values.update({v: False for v in auxiliary})
    # After fixing inputs, every remaining clause has at most one positive
    # auxiliary literal. The least-model construction is complete for Horn.
    reduced = []
    for clause in clauses:
        if any(abs(lit) in fixed and fixed[abs(lit)] == (lit > 0) for lit in clause):
            continue
        left = [lit for lit in clause if abs(lit) not in fixed]
        require(all(abs(lit) in auxiliary for lit in left), 'Counter uses a foreign variable')
        require(sum(lit > 0 for lit in left) <= 1, 'Non-Horn counter fragment')
        reduced.append(left)
    while True:
        changed = False
        for clause in reduced:
            if any(values[abs(lit)] == (lit > 0) for lit in clause):
                continue
            positive = [lit for lit in clause if lit > 0]
            if not positive:
                return None
            values[positive[0]] = True
            changed = True
        if not changed:
            require(all(any(values[abs(lit)] == (lit > 0) for lit in clause)
                        for clause in clauses), 'Counter model does not satisfy clauses')
            return values


def all_counter_extensions(clauses, inputs, auxiliary, bound):
    require(set(inputs).isdisjoint(auxiliary), 'Counter namespace overlap')
    count = 0
    for size in range(bound + 1):
        for positions in combinations(range(len(inputs)), size):
            ones = set(positions)
            fixed = {v: i in ones for i, v in enumerate(inputs)}
            require(horn_model(clauses, fixed, set(auxiliary)) is not None,
                    'Feasible route count has no counter extension')
            count += 1
    return count


def semantic_audit(certificate, core):
    pairs, picks, use, truth, rows, hits, auxiliary, variables = layout(certificate)
    relevant = {64, 68, 544, 2015}
    templates = {}

    def add(clause, reason):
        if truth in clause or any(-lit in clause for lit in clause):
            return
        clause = canon(lit for lit in clause if lit != -truth)
        templates.setdefault(clause, reason)

    # The actual selected comparator determines the used-wire flags.
    for t in range(19):
        for i in range(11):
            incident = [picks[t][j] for j, pair in enumerate(pairs) if i in pair]
            for selected in incident:
                add([-selected, use[t][i]], 'incidence')
            add([-use[t][i]] + incident, 'incidence')

    # The only relevant sorting rows. Endpoints use exact Boolean AND/OR.
    for x in relevant:
        v = rows[x]
        for i in range(11):
            add([v[0][i] if x >> i & 1 else -v[0][i]], 'initial_row')
            add([v[-1][i] if i >= 11 - x.bit_count() else -v[-1][i]], 'sorted_row')
        for t in range(19):
            for i in range(11):
                add([use[t][i], -v[t][i], v[t + 1][i]], 'untouched_wire')
                add([use[t][i], v[t][i], -v[t + 1][i]], 'untouched_wire')
            for j, (a, b) in enumerate(pairs):
                selected = picks[t][j]
                incoming_a, incoming_b = v[t][a], v[t][b]
                outgoing_a, outgoing_b = v[t + 1][a], v[t + 1][b]
                for clause in [
                    [-selected, -outgoing_a, incoming_a],
                    [-selected, -outgoing_a, incoming_b],
                    [-selected, outgoing_a, -incoming_a, -incoming_b],
                    [-selected, outgoing_b, -incoming_a],
                    [-selected, outgoing_b, -incoming_b],
                    [-selected, -outgoing_b, incoming_a, incoming_b]]:
                    add(clause, 'comparator_transition')

    # Sorted threshold rows1024 and1536 never change. Their high-touch
    # indicators are exactly incidences at10 or at9/10, respectively.
    for x in (1024, 1536):
        for t in range(19):
            hit = hits[x, 'high'][t]
            for j, (a, b) in enumerate(pairs):
                selected = picks[t][j]
                active = bool(x >> a & 1 or x >> b & 1)
                add([-selected, hit if active else -hit], 'sorted_threshold_hit')

    # Maximum route: any gate on10 is (9,10), at most one such gate.
    for t in range(19):
        for j, pair in enumerate(pairs):
            if 10 in pair and pair != (9, 10):
                add([-picks[t][j]], 'maximum_pair')

    # A minimum route pivot exists; wire1 is unused before it and wire0
    # is unused afterwards. This is a consequence of one zero passage.
    pivot_index = pairs.index((0, 1))
    pivots = [slot[pivot_index] for slot in picks]
    add(pivots, 'minimum_pivot_exists')
    for t, pivot in enumerate(pivots):
        for before in range(t):
            add([-pivot, -use[before][1]], 'minimum_phase')
        for after in range(t + 1, 19):
            add([-pivot, -use[after][0]], 'minimum_phase')

    counter_groups = {
        'at_most_one_maximum': (set(auxiliary['maximum']),
                                [slot[10] for slot in use], 1, []),
        'at_most_two_top_pair': (set(auxiliary[1536, 'high']),
                                 hits[1536, 'high'], 2, [])}
    reasons = Counter()
    for clause in core:
        if clause in templates:
            reasons[templates[clause]] += 1
            continue
        found = []
        for name, (aux, inputs, bound, clauses) in counter_groups.items():
            if any(abs(lit) in aux for lit in clause):
                require(all(abs(lit) in aux | set(inputs) for lit in clause),
                        'Counter clause has wrong semantic namespace')
                clauses.append(clause)
                found.append(name)
        require(len(found) == 1, 'Core clause has no independent mathematical explanation: ' + str(clause))
        reasons[found[0]] += 1

    extension_counts = {}
    for name, (aux, inputs, bound, clauses) in counter_groups.items():
        extension_counts[name] = all_counter_extensions(clauses, inputs, aux, bound)
    return {'semantic_clauses': len(core), 'reasons': dict(sorted(reasons.items())),
            'counter_extension_patterns': extension_counts,
            'sorting_rows_needed': sorted(relevant),
            'full_generated_cnf_needed': False, 'solver_or_cardinality_library_needed': False}
