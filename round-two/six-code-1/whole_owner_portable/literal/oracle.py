"""Independent factoradic free binding and partial-word-intersection MRV."""
from model import source_cells, need


def unrank3(items, rank):
    remaining = sorted(items)
    answer = []
    for divisor in (2, 1, 1):
        index, rank = divmod(rank, divisor)
        answer.append(remaining.pop(index))
    need(rank == 0, 'factoradic remainder')
    return answer


def free_map(Q, u, v, targetF, rank):
    cells, holes = source_cells(Q, u, v)
    columns = unrank3(range(3), rank // 216)
    remaining = rank % 216
    digits = []
    for place in (36, 6, 1):
        digit, remaining = divmod(remaining, place)
        digits.append(digit)
    image = {u: 16, v: 17}
    for cell, column, digit in zip(cells, columns, digits):
        for a, b in zip(cell, unrank3(targetF[column], digit)):
            image[a] = b
    return image, holes


def search(Q, owner, u, v, targetF, rank, budget):
    image, holes = free_map(Q, u, v, targetF, rank)
    words = [q for q in Q if u not in q]
    target_words = [(sum(1 << a for a in set(w) - {15, 16}), 1 if 15 in w else 2) for w in owner]
    incidence = {a: [q for q in words if a in q] for a in holes}
    answers = []
    visits = 0
    rejected = 0

    def compatible(qs):
        for q in qs:
            partial = sum(1 << image[a] for a in q if a in image)
            if any((partial & target).bit_count() > limit for target, limit in target_words):
                return False
        return True

    budget.tick()
    if not compatible(words):
        return [], {'initial_rejected': True, 'visits': 0, 'partial_rejections': 1}
    target_holes = set(range(15)) - set().union(*(set(c) for c in targetF))

    def visit():
        nonlocal visits, rejected
        budget.tick()
        visits += 1
        if len(image) == 17:
            answers.append(tuple(image[a] for a in range(17)))
            return
        unused = sorted(target_holes - set(image.values()))
        candidates = []
        for a in holes:
            if a in image:
                continue
            allowed = []
            for b in unused:
                budget.tick()
                image[a] = b
                if compatible(incidence[a]):
                    allowed.append(b)
                else:
                    rejected += 1
                del image[a]
            if not allowed:
                return
            candidates.append((len(allowed), a, allowed))
        _, a, targets = min(candidates)
        for b in targets:
            image[a] = b
            visit()
            del image[a]

    visit()
    return sorted(answers), {'initial_rejected': False, 'visits': visits, 'partial_rejections': rejected}
