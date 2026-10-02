"""Actual original row variance and whole-entry lift checks."""
from fractions import Fraction as F
from itertools import combinations
from hashlib import sha256
import pins
from literal import core_data
from variance import require, row_classes, scalar_record
from entries import certificate, EDGES


def original(q, k):
    # Preserve the imported literal's q4..11,k2/3 guard.
    X, N, s, C, delta, R, U = core_data(q, k)
    from literal import domain
    require(X == domain(q, k, scan=True), 'full independent bitmask census')
    actual = [sum(row) for row in U]
    classes = row_classes(q, k)
    predicted = []
    for A in X[1:]:
        if A & 6:
            category = 0
        elif A == 1:
            category = 1
        elif A & 1:
            category = 2 if (A >> 3).bit_length() <= k else 3
        elif (A >> 3).bit_count() == 1:
            category = 4 if (A >> 3).bit_length() <= k else 5
        else:
            category = 6+((A >> 3) & ((1 << k)-1)).bit_count()
        predicted.append(classes[category][1])
    require(actual == predicted, 'every actual original constant-row action')
    r = scalar_record(q, k)
    require(str(sum(actual)) == r['e'] and str(sum(x*x for x in actual)) == r['V'],
            'literal exact mean and squared norm')
    return {'q': q, 'k': k, 'N': N, 'original_positions': (N-1)**2,
            'every_literal_row_matches': True, 'e': r['e'], 'V': r['V'],
            'credit': '9259 input reproduction, not new finite classification'}


def whole(q, k, state=None):
    from literal import table, typ
    if state is None:
        require((q, k) == (19, 5), 'new whole-entry baseline singleton q19/k5')
        Z = set(range(3, 8))
        sets = []
        for size in (1, 2, 3):
            for pts in combinations(range(q+3), size):
                core = set(pts) & {0, 1, 2}
                if size == 3 and len(core) < 2:
                    continue
                if core == {1, 2} and len(set(pts) & Z) == 1:
                    continue
                sets.append(sum(1 << i for i in pts))
        X = sorted(sets)
    else:
        require((q, k) == (24, 6), 'exceptional state only q24/k6')
        X = state['X']
    p, M = certificate(q, k)
    N, s = p['N'], p['s']
    require(N == len(X)+1 and len(set(X)) == len(X), 'whole original census')
    w, kappa, t = table(q), F(p['kappa']), F(p['t'])

    def C(A, B):
        if A == B:
            return F(s-1)
        if A & B:
            return F(-1)
        base, slope = w[tuple(sorted((typ(A), typ(B))))]
        return base+kappa*slope-1+t*EDGES.get(tuple(sorted((A, B))), 0)

    rows = [sum(C(A, B) for B in X) for A in X]
    allX = [0]+X
    loop = 1+sum(rows)
    wire = sha256()
    for i, A in enumerate(allX):
        total = F(0)
        star_action = F(0)
        for j, B in enumerate(allX):
            L = loop if not i and not j else 1-rows[(i or j)-1] if not i or not j else 1+C(A, B)
            expected = (L-s*int(i == j))/(N-s)
            actual = M(A, B)
            require(actual == expected, 'every independently lifted original whole entry')
            if A & B:
                require(actual == 0, 'every forbidden original support entry')
            total += actual
            star_action += L*(F(bool(B & 1))-F(s, N))
            wire.update(str(actual).encode()+b'\n')
        require(total == 1 and star_action == 0, 'every whole row and centered-star action')
    return {'q': q, 'k': k, 'N': N, 'whole_positions': N*N,
            'all_direct_lift_rows_support_star_match': True,
            'whole_M_stream_sha256': wire.hexdigest(), 'M_empty_empty': str(M(0, 0)),
            'parameters': p, 'guard': 'new singleton q19/k5 or q24/k6 state only'}
