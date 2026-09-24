"""Construct non-induced block-graph copies from edge-disjoint clique lists."""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def block_plan(blocks, order):
    """Validate an acyclic block-incidence graph and root its components."""
    require(order >= 2 and bool(blocks), "pattern must have an edge")
    owner = list(range(order))

    def find(v):
        while owner[v] != v:
            v = owner[v]
        return v

    for block in blocks:
        require(len(block) >= 2 and len(set(block)) == len(block),
                "invalid clique block")
        require(all(isinstance(u, int) and 0 <= u < order for u in block),
                "abstract role outside pattern")
        roots = [find(u) for u in block]
        require(len(set(roots)) == len(roots), "cyclic block incidence")
        for root in roots[1:]:
            owner[root] = roots[0]
    unused = set(range(len(blocks)))
    plans = []
    while unused:
        first = min(unused)
        unused.remove(first)
        plan = [(first, None, None)]
        seen = set(blocks[first])
        previous = [first]
        while True:
            choices = []
            for b in sorted(unused):
                overlap = set(blocks[b]) & seen
                require(len(overlap) <= 1, "invalid block attachment")
                if overlap:
                    choices.append((b, next(iter(overlap))))
            if not choices:
                break
            b, root = choices[0]
            parent = next(p for p in previous if root in blocks[p])
            plan.append((b, parent, root))
            previous.append(b)
            seen.update(blocks[b])
            unused.remove(b)
        plans.append(plan)
    return plans


def assemble(blocks, instances, role_classes, vertex_classes):
    """Return injective role maps plus a replayable greedy certificate.

    Input lists must be globally edge-disjoint, including between labels.
    The host is described only by its vertices/classes: the checker separately
    verifies that all required edges exist in its explicit host fixtures.
    """
    order = len(role_classes)
    plans = block_plan(blocks, order)
    require(len(instances) == len(blocks), "missing block list")
    edges = set()
    for block, copies in zip(blocks, instances):
        for copy in copies:
            require(len(copy) == len(block) and len(set(copy)) == len(copy),
                    "noninjective block instance")
            for u, v in zip(block, copy):
                require(0 <= v < len(vertex_classes), "host vertex outside range")
                require(role_classes[u] == vertex_classes[v], "role class mismatch")
            for u, v in combinations(copy, 2):
                edge = tuple(sorted((u, v)))
                require(edge not in edges, "input blocks share an edge")
                edges.add(edge)
    components, certificate = [], {'components': [], 'joins': []}
    for plan in plans:
        root = plan[0][0]
        partials = [dict(zip(blocks[root], copy)) for copy in instances[root]]
        component_trace = {'first': root, 'stages': []}
        for b, parent, role in plan[1:]:
            position = blocks[b].index(role)
            buckets = {}
            for j, copy in enumerate(instances[b]):
                buckets.setdefault(copy[position], []).append(j)
            available = set(range(len(instances[b])))
            choices, grown, rejected = [], [], 0
            for partial in partials:
                v = partial[role]
                forbidden = set(partial.values()) - {v}
                selected = -1
                for j in buckets.get(v, []):
                    if j not in available:
                        continue
                    if forbidden.intersection(instances[b][j]):
                        rejected += 1
                        continue
                    selected = j
                    break
                choices.append(selected)
                if selected >= 0:
                    available.remove(selected)
                    result = dict(partial)
                    result.update(zip(blocks[b], instances[b][selected]))
                    grown.append(result)
            component_trace['stages'].append({
                'block': b, 'parent': parent, 'role': role,
                'choices': choices, 'collision_tests_failed': rejected})
            partials = grown
        components.append(partials)
        certificate['components'].append(component_trace)
    partials = components[0]
    for candidates in components[1:]:
        available = set(range(len(candidates)))
        choices, joined, rejected = [], [], 0
        for partial in partials:
            forbidden = set(partial.values())
            selected = -1
            for j in sorted(available):
                if forbidden.intersection(candidates[j].values()):
                    rejected += 1
                    continue
                selected = j
                break
            choices.append(selected)
            if selected >= 0:
                available.remove(selected)
                result = dict(partial)
                result.update(candidates[selected])
                joined.append(result)
        certificate['joins'].append({'choices': choices,
                                     'collision_tests_failed': rejected})
        partials = joined
    isolated = sorted(set(range(order)) - set().union(*map(set, blocks)))
    for partial in partials:
        used = set(partial.values())
        for role in isolated:
            candidate = next((v for v, kind in enumerate(vertex_classes)
                              if kind == role_classes[role] and v not in used), None)
            require(candidate is not None, "infeasible isolated role")
            partial[role] = candidate
            used.add(candidate)
    output = [tuple(partial[u] for u in range(order)) for partial in partials]
    return output, certificate
