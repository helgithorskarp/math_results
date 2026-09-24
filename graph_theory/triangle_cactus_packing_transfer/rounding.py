"""Exact partition-constrained rounding and labeled clique roles.

Standard library only. The universal design-theorem input is not implemented.
Fractions and trace records permit definition-level replay in check.py.
"""

from collections import Counter
from fractions import Fraction
from itertools import permutations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _subtract(target, source, scale):
    for key, value in source.items():
        value = target.get(key, Fraction(0)) - scale * value
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def _dependency(columns):
    """Find a rational linear dependence by sparse column elimination."""
    basis = {}
    for j, column in enumerate(columns):
        vector = {r: Fraction(v) for r, v in column.items() if v}
        expression = {j: Fraction(1)}
        while vector:
            pivot = min(vector)
            scale = vector[pivot]
            if pivot not in basis:
                vector = {r: v / scale for r, v in vector.items()}
                expression = {k: v / scale for k, v in expression.items()}
                basis[pivot] = (vector, expression)
                break
            old_vector, old_expression = basis[pivot]
            _subtract(vector, old_vector, scale)
            _subtract(expression, old_expression, scale)
        else:
            require(bool(expression), "empty null direction")
            return expression
    raise ValueError("expected a dependent column family")


def round_options(groups, sparsity):
    """One option per group, every 0/1 soft row error <= 2*sparsity.

    A group is a list of dictionaries with Fraction-convertible 'weight'
    and a tuple of distinct hashable 'rows'. Extra payload is untouched.
    The returned trace is a certificate, not a published bulk artifact.
    """
    require(isinstance(sparsity, int) and sparsity >= 1, "invalid sparsity")
    flat, group_ids, offsets = [], [], []
    row_members = {}
    for g, options in enumerate(groups):
        require(bool(options), "empty item")
        offsets.append(len(flat))
        total = Fraction(0)
        ids = []
        for option in options:
            weight = Fraction(option['weight'])
            require(0 <= weight <= 1, "weight outside unit interval")
            rows = tuple(option['rows'])
            require(len(rows) == len(set(rows)), "nonbinary row incidence")
            require(len(rows) <= sparsity, "column sparsity exceeded")
            j = len(flat)
            flat.append(weight)
            ids.append(j)
            for row in rows:
                row_members.setdefault(row, set()).add(j)
            total += weight
        require(total == 1, "item weights do not sum to one")
        group_ids.append(ids)
    row_names = sorted(row_members, key=repr)
    members = [row_members[name] for name in row_names]
    active = set(range(len(members)))
    x = flat[:]
    trace = []
    while True:
        floating = {j for j, value in enumerate(x) if 0 < value < 1}
        if not floating:
            break
        dropped = sorted(r for r in active
                         if len(members[r] & floating) <= 2 * sparsity)
        active.difference_update(dropped)
        fractional_groups = []
        for ids in group_ids:
            ids = [j for j in ids if j in floating]
            if ids:
                require(len(ids) >= 2, "one floating option in an item")
                fractional_groups.append(ids)
        require(len(active) + len(fractional_groups) < len(floating),
                "dimension count failed")
        free, anchors, columns = [], [], []
        for ids in fractional_groups:
            anchor = ids[0]
            for j in ids[1:]:
                column = {}
                for r in sorted(active):
                    value = int(j in members[r]) - int(anchor in members[r])
                    if value:
                        column[r] = value
                free.append(j)
                anchors.append(anchor)
                columns.append(column)
        relation = _dependency(columns)
        direction = {}
        for k, value in relation.items():
            j, anchor = free[k], anchors[k]
            direction[j] = direction.get(j, Fraction(0)) + value
            direction[anchor] = direction.get(anchor, Fraction(0)) - value
        direction = {j: v for j, v in direction.items() if v}
        require(bool(direction), "zero direction")
        step = min((1-x[j])/value if value > 0 else -x[j]/value
                   for j, value in direction.items())
        require(step > 0, "nonpositive rounding step")
        for j, value in direction.items():
            x[j] += step * value
        require(all(0 <= value <= 1 for value in x), "rounding escaped cube")
        require(any(x[j] in (0, 1) for j in direction), "no progress")
        trace.append({'dropped': dropped, 'step': step,
                      'direction': sorted(direction.items())})
    choices = []
    for offset, ids in zip(offsets, group_ids):
        selected = [j-offset for j in ids if x[j] == 1]
        require(len(selected) == 1, "nonintegral partition output")
        choices.append(selected[0])
    return {'choices': choices, 'trace': trace, 'rows': row_names}


def label_and_orient(copies, vertex_classes, specs):
    """Lift a single base clique type to true labeled, oriented blocks.

    specs has entries {'mass', 'roles', 'classes', 'true'}; role and class
    tuples have equal length. All labels have the same sorted class type.
    Disposable labels ('true': False) model unused edge capacity.
    """
    require(bool(specs), "no labels")
    size = len(specs[0]['roles'])
    require(size >= 2, "base pattern has no edges")
    kind = sorted(specs[0]['classes'])
    masses = [Fraction(spec['mass']) for spec in specs]
    require(all(x >= 0 for x in masses), "negative label mass")
    total = sum(masses, Fraction(0))
    require(total >= len(copies), "base count exceeds profile")
    for spec in specs:
        require(len(spec['roles']) == size and
                len(set(spec['roles'])) == size, "invalid abstract roles")
        require(sorted(spec['classes']) == kind, "mixed base clique types")
    if total == 0:
        require(not copies, "positive copies at zero mass")
    groups = []
    for copy in copies:
        require(len(copy) == size and len(set(copy)) == size,
                "noninjective base clique")
        require(all(0 <= v < len(vertex_classes) for v in copy),
                "base vertex outside host")
        require(sorted(vertex_classes[v] for v in copy) == kind,
                "base class mismatch")
        options = []
        for ell, spec in enumerate(specs):
            if masses[ell] == 0:
                continue
            maps = [p for p in permutations(copy)
                    if tuple(vertex_classes[v] for v in p) ==
                    tuple(spec['classes'])]
            require(bool(maps), "missing class-respecting bijection")
            for p in maps:
                rows = [('count', ell)]
                rows += [('role', ell, u, v)
                         for u, v in zip(spec['roles'], p)]
                options.append({'weight': masses[ell]/(total*len(maps)),
                                'rows': tuple(rows), 'label': ell,
                                'image': tuple(p)})
        groups.append(options)
    certificate = round_options(groups, size+1)
    lists = [[] for _ in specs]
    for group, choice in zip(groups, certificate['choices']):
        option = group[choice]
        lists[option['label']].append(option['image'])
    before = [len(x) for x in lists]
    for ell, spec in enumerate(specs):
        if spec['true']:
            lists[ell] = lists[ell][:masses[ell].numerator//masses[ell].denominator]
        else:
            lists[ell] = []
    return lists, {'groups': groups, 'rounding': certificate,
                   'before_counts': before}
