"""Check the forced eighth away block and small integer weight obstructions."""
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def residual(join, configuration):
    a, b = configuration['a'], configuration['b']
    require(len(a) == len(b) == 7, 'unexpected surviving join dimensions')
    deficits = [4 - sum(row >> p & 1 for row in b) for p in range(12)]
    if any(value not in (0, 1) for value in deficits):
        return None
    forced = sum(1 << p for p, value in enumerate(deficits) if value)
    require(forced.bit_count() == 6 and forced not in b, 'invalid forced away block')
    require(not forced & ((1 << join['p']) | (1 << join['q'])),
            'forced block meets a completed point link')
    completed_b = b + [forced]
    required = []
    for size in (2, 3):
        family = a if size == 2 else a + completed_b
        for points in combinations(range(12), size):
            target = sum(1 << p for p in points)
            if not any(row & target == target for row in family):
                required.append(target)
    free = [p for p in range(12) if p not in (join['p'], join['q'])]
    candidates = [sum(1 << p for p in points) for points in combinations(free, 5)]
    require(len(candidates) == 252, 'wrong remaining row universe')
    return required, candidates


def check_weights(join, configuration, certificate):
    instance = residual(join, configuration)
    require(instance is not None, 'weight certificate assigned to a degree contradiction')
    required, candidates = instance
    weights = {}
    for target, value in certificate['weights']:
        require(type(target) is int and target in required, 'weight on an unrequired set')
        require(type(value) is int and value > 0, 'invalid weight')
        require(target not in weights, 'duplicate weighted set')
        weights[target] = value
    total = sum(weights.values())
    capacity = max(sum(value for target, value in weights.items()
                       if row & target == target) for row in candidates)
    require(total == certificate['total'] and capacity == certificate['capacity'],
            'weight totals differ from certificate')
    require(total > 5 * capacity, 'no strict five-block weight gap')
    return dict(total=total, capacity=capacity, gap=total - 5 * capacity,
                terms=len(weights), capacity_checks=len(candidates))
