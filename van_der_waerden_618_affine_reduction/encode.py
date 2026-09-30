"""Independent reduced CRT encodings and finite normal-form controls."""
import hashlib


def canonical(values):
    values = set(values)
    if any(-v in values for v in values):
        return None
    return min(tuple(sorted(values)), tuple(sorted(-v for v in values)))


def coset_ids(index):
    images = {pow(5, j*(102//index), 103): j for j in range(index)}
    assert len(images) == index
    return [index]+[images[pow(x, 102//index, 103)] for x in range(1, 103)]


def literal(t, family, ids):
    x, y = t % 103, t % 6
    if family == 'reflection':
        if x == 0:
            return 154*(1 if y < 3 else -1)
        if x > 51:
            x, y = 103-x, (2-y) % 6
        v = 3*(x-1)+y % 3+1
    else:
        v = 3*ids[x]+y % 3+1
    return v*(1 if y < 3 else -1)


def encoding(family):
    assert family in ['h2', 'h3', 'reflection']
    index = 51 if family == 'h2' else 34
    ids = coset_ids(index) if family != 'reflection' else None
    constraints = set()
    for a in range(309):
        for d in range(1, 310):
            values = [literal((a+j*d) % 618, family, ids) for j in range(7)]
            if family != 'reflection':
                edge = canonical(values)
                if edge is not None:
                    constraints.add(edge)
                continue
            for sign in [1, -1]:
                clause = {sign*v for v in values}
                if -154 in clause or any(-v in clause for v in clause):
                    continue
                clause.discard(154)  # the normalized zero column is false
                constraints.add(tuple(sorted(clause)))
    if family == 'reflection':
        n, clauses = 153, sorted(constraints)
    else:
        n = 3*(index+1)
        edges = sorted(constraints)
        clauses = edges+[tuple(-v for v in e) for e in edges]
        clauses += [(-(3*index+k+1),) for k in range(3)]
    raw = f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    return raw.encode(), {'variables': n, 'clauses': len(clauses),
                          'cnf_sha256': hashlib.sha256(raw.encode()).hexdigest()}


def controls():
    def column(p):
        return tuple(int((y-p) % 6 >= 3) for y in range(6))
    valid = set()
    for mask in range(64):
        c = tuple((mask >> y) & 1 for y in range(6))
        anti = all(c[y+3] == 1-c[y] for y in range(3))
        triples = all(len({c[(y+2*j) % 6] for j in range(3)}) == 2 for y in [0, 1])
        if anti and triples:
            valid.add(c)
    assert valid == {column(p) for p in range(6)}
    checked = 0
    for p in range(6):
        for q in range(6):
            for shift in range(6):
                equal = all(column(p)[y] == column(q)[(shift-y) % 6] for y in range(6))
                assert equal == (q == (shift-2-p) % 6)
                checked += 1
    return {'local_words_checked': 64, 'reflection_identities_checked': checked,
            'valid_local_columns': 6}
