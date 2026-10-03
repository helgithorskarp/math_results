"""All free-cell maps, then fixed-order forbidden-subset DFS on six holes."""
from itertools import combinations, permutations
from model import need, source_cells

ORDERS = tuple(permutations(range(3)))


def free_map(Q, u, v, targetF, rank):
    cells, holes = source_cells(Q, u, v)
    order_rank, inner_rank = divmod(rank, 216)
    order = ORDERS[order_rank]
    ranks = [inner_rank // 36, (inner_rank // 6) % 6, inner_rank % 6]
    image = {u: 16, v: 17}
    for i in range(3):
        target = tuple(permutations(sorted(targetF[order[i]])))[ranks[i]]
        image.update(zip(cells[i], target))
    need(len(image) == len(set(image.values())) == 11, 'producer free binding')
    return image, holes


def search(Q, owner, u, v, targetF, rank, budget):
    image, holes = free_map(Q, u, v, targetF, rank)
    target_holes = sorted(set(range(15)) - set().union(*(set(c) for c in targetF)))
    forbidden2, forbidden3 = set(), set()
    for w in owner:
        if 15 in w:
            forbidden2.update(tuple(sorted(c)) for c in combinations(set(w) - {15, 16}, 2))
        else:
            forbidden3.update(tuple(sorted(c)) for c in combinations(set(w) - {16}, 3))
    subsets = set()
    for q in Q:
        if u not in q:
            subsets.update(tuple(sorted(c)) for c in combinations(q, 2))
            subsets.update(tuple(sorted(c)) for c in combinations(q, 3))
    subsets = sorted(subsets)
    incidence = {a: [s for s in subsets if a in s] for a in holes}
    answers = []
    visits = 0
    rejected = 0

    def safe(constraints):
        for s in constraints:
            if all(a in image for a in s):
                t = tuple(sorted(image[a] for a in s))
                if t in (forbidden2 if len(s) == 2 else forbidden3):
                    return False
        return True

    budget.tick()
    if not safe(subsets):
        return [], {'initial_rejected': True, 'visits': 0, 'partial_rejections': 1}

    def visit(k, unused):
        nonlocal visits, rejected
        budget.tick()
        visits += 1
        if k == 6:
            answers.append(tuple(image[a] for a in range(17)))
            return
        a = holes[k]
        for b in unused:
            budget.tick()
            image[a] = b
            if safe(incidence[a]):
                visit(k + 1, [c for c in unused if c != b])
            else:
                rejected += 1
            del image[a]

    visit(0, target_holes)
    return sorted(answers), {'initial_rejected': False, 'visits': visits, 'partial_rejections': rejected}
