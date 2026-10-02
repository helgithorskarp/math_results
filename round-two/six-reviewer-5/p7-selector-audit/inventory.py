"""Independent monotone multisets with prescribed excess and physical cuts."""
from collections import Counter
import time
from star_primitives import require, digest


def derive(rows, lam, E_target, t):
    require(sum(lam) == 7 and E_target in (0, 1, 2) and t in (0, 1), 'P7 exact sector')
    a, b, c = lam; D = (14-c, 6-b, 6-a); budget = 6-t
    bases = {r[:3]: r for r in rows if r[3]+r[4] == 0}
    require(set(bases) == {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}, 'four zero-cost fillers')
    positive = tuple(r for r in rows if r[3]+r[4] > 0 and r[3] <= E_target)
    records, survivors, counts = [], [], Counter()
    start_time = time.monotonic(); states = 0

    def visit(chosen, low_index, cost, E, used):
        nonlocal states
        states += 1
        require(states <= 200000 and time.monotonic()-start_time < 20,
                'INCOMPLETE fixed200000-state/20-second sector guard')
        residual = tuple(D[i]-used[i] for i in range(3))
        unmarked = 15-len(chosen)-sum(residual)
        if E == E_target and min(residual) >= 0 and unmarked >= 0 and (budget-cost) % 2 == 0:
            whole = list(chosen)+[bases[(0, 0, 0)]]*unmarked
            for i, n in enumerate(residual):
                key = tuple(int(i == j) for j in range(3))
                whole.extend([bases[key]]*n)
            require(len(whole) == 15, 'complete row population')
            cross_excess = sum(sum(max(d-1, 0) for d in r[:3]) for r in whole)
            ss_excess = sum(5-sum(r[:3])-r[5] for r in whole)
            require(ss_excess == E-cross_excess and ss_excess >= 0, 'row excess conservation')
            if ss_excess % 2 == 0:
                X = ss_excess//2; Q = cost-E; tau = (budget-cost)//2
                low = tuple(sum(r[i] == r[j] == 0 for r in whole) for i, j in ((0, 1), (0, 2), (1, 2)))
                if len(rows[0]) == 9:
                    good = tuple(sum(r[5] for r in whole if r[6+i]) for i in range(3))
                else:
                    good = tuple(sum(r[5] for r in whole if r[i] > 0 and
                                sum(d > 0 for d in r[:3]) == 1 and r[4] == 0 and
                                ((r[3] == 0 and r[i] == 1) or (r[3] == 1 and r[i] == 2))) for i in range(3))
                # This independently weaker audit uses the cohort cut only
                # at X0. Per-row good flags also license it at X>0,
                # but X>0 has no budget-valid row count in these sectors.
                reason = ('low_pair' if any(n > 3*m-t for n, m in zip(low, lam)) else
                          'good_cohort' if X == 0 and max(good) > 28 else 'survivor')
                counts['budget_valid'] += 1; counts[reason] += 1
                record = {'exceptional': chosen, 'filler_counts': (unmarked,)+residual,
                          'E': E, 'Q': Q, 'X': X, 'tau': tau,
                          'low_pair_counts': low, 'good_cohort_degrees': good, 'reason': reason}
                records.append(record)
                if reason == 'survivor':
                    survivors.append(record)
        if cost >= budget or len(chosen) == 6:
            return
        for i in range(low_index, len(positive)):
            r = positive[i]; next_E = E+r[3]; next_cost = cost+r[3]+r[4]
            if next_E > E_target or next_cost > budget:
                continue
            next_used = tuple(used[j]+r[j] for j in range(3))
            if max(next_used[j]-D[j] for j in range(3)) > 0:
                continue
            visit(chosen+[r], i, next_cost, next_E, next_used)

    visit([], 0, 0, 0, (0, 0, 0))
    summary = {'multiplicities': lam, 'E': E_target, 't': t, 'cross_weights': D,
               'counts': dict(counts), 'inventory_sha256': digest(records),
               'survivors_sha256': digest(survivors)}
    return summary, survivors, records, states
