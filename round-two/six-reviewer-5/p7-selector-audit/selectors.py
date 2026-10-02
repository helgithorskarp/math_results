"""Count certificates for quantified ordinary selectors, never actual codes."""
from star_primitives import require


def expansion(rows, record):
    bases = {r[:3]: r for r in rows if r[3]+r[4] == 0}
    result = list(record['exceptional'])
    for key, n in zip(((0,0,0),(1,0,0),(0,1,0),(0,0,1)), record['filler_counts']):
        result.extend([bases[key]]*n)
    require(len(result) == 15, 'actual whole row statistic population')
    return result


def guaranteed_points(eligible, pair_words, t, outside_edges):
    require(0 <= eligible <= 15 and 0 <= pair_words <= 5 and t in (0,1)
            and 0 <= outside_edges <= 28, 'coverage count domain')
    covered = 3*pair_words-t
    require(0 <= covered <= 15, 'physical pair-tail S population')
    return eligible-(15-covered)-2*outside_edges


def check(rows, lam, E, t, record):
    require(record['E'] == E and record['X'] == record['tau'] == 0, 'selected surviving sector scope')
    whole = expansion(rows, record)
    ks = [sum(d > 0 for d in r[:3]) for r in whole]
    if E in (0, 1):
        require(t == 0 and record['Q'] == 6-E, 'exact low-excess budget')
        require([ks.count(k) for k in range(4)] == ([0,13,0,2] if E == 0 else [0,13,1,1]), 'complete support sectors')
        require(lam in ((1,1,5),(1,2,4),(2,1,4)), 'admitted E0/E1 pair case')
        A = [r for r,k in zip(whole,ks) if k == 1 and r[0] > 0 and r[4] == 0]
        require(all((r[3] == 0 and r[0] == 1 or r[3] == 1 and r[0] == 2)
                    and r[1] == r[2] == 0 for r in A), 'exact unit/mixed isolated-w cohort')
        m = sum(r[3] for r in A); require(m in (0,1), 'at most one heavy A row')
        B = [r for r,k in zip(whole,ks) if k == 1 and r[0] == 0 and
             r[3] == r[4] == 0 and r[1]+r[2] == 1]
        degree = sum(r[5] for r in A); require(degree in (27,28), 'A incidence saturation')
        outside = 28-degree
        lower = guaranteed_points(len(B), lam[2], t, outside)
        require(lower > 0, 'no quantified physical selector guaranteed')
        # Every eligible x has a low-V leave friend y in A. The complete
        # new opposite-hub carrier excludes all UNIT y. At a MIXED y,
        # each of the two low global hubs has a unique leave friend, so
        # at most2m eligible x can map to all mixed rows.
        method = ('unit-friend core incompatibility' if m == 0 else
                  'two-low-friends capacity contradiction' if lower > 2*m else
                  'new mixed opposite-hub sharp61')
        return {'method': method, 'A_size': len(A), 'A_degree': degree,
                'mixed_A_rows': m, 'eligible_unit_rows': len(B),
                'outside_edges': outside, 'guaranteed_usable_points': lower,
                'mixed_friend_capacity': 2*m,
                'local_upper_if_mixed': 61, 'triangle_premise_needed': False}
    require(E == 2 and t == 1 and lam == (2,2,3), 'last heavy sector scope')
    T = [r for r,k in zip(whole,ks) if k == 3]
    q1 = [r for r in whole if r[4] == 1]
    require(len(T) == 1 and T[0][:6] == (3,1,1,2,2,0), 'exact heavy three-hub row')
    require(len(q1) == 1 and q1[0][:6] == (1,0,0,0,1,4), 'required q1 singleton unit row')
    A = [r for r in whole if r[:5] == (1,0,0,0,0)]
    require(len(A) == 7 and sum(r[5] for r in A) == 28 and record['Q'] == 3, 'seven-row exact edge saturation')
    return {'method': 'ordinary high-leave reciprocity contradiction',
            'A_size':7, 'A_degree':28, 'required_q':1, 'forced_q':0,
            'triangle_premise_needed':False}


def remaining_boundary(rows, lam, record):
    """New E2,t0 necessary-inventory cut; survivors are not realizations."""
    require(record['E'] == 2 and record['X'] == 0, 'E2,t0 unit-SS support scope')
    whole = expansion(rows, record)
    A = [r for r in whole if r[6] and r[0] > 0 and r[1] == r[2] == 0]
    require(all(r[3] in (0, 1) and r[0] == r[3]+1 for r in A), 'good singleton-w cohort')
    B = [r for r in whole if r[0] == r[3] == r[4] == 0 and r[1]+r[2] == 1]
    degree = sum(r[5] for r in A); require(degree <= 28, 'independent-cohort edge capacity')
    lower = guaranteed_points(len(B), lam[2], 0, 28-degree)
    return {'excluded': lower > 0, 'guaranteed_usable_points': lower,
            'A_size': len(A), 'A_degree': degree, 'B_size': len(B),
            'mixed_A_rows': sum(r[3] for r in A), 'tau': record['tau']}
