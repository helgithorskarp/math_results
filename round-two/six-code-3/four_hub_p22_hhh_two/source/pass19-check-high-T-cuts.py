"""Independent graph-incidence and weak typed-composition certificate check.

No mathematical helper is imported from the producer. Both complete
census records are compared; each original certificate is reconstructed.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

S = Path('round-two/six-code-3/scratch')
CANON = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def compositions(total, slots):
    if slots == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, slots - 1):
            yield (first,) + tail


def fit_support(B, C, J, N, weaken=False):
    for b, c, j, n in zip(B, C, J, N):
        demands = [1 + max(0, 3*d - 2 - q) for count, d, q in ((b, 1, 0), (c, 2, 0), (j, 2, 1)) if count]
        if weaken and c:
            demands = [1 + max(0, 3*d - 2 - q) for count, d, q in ((b, 1, 0), (j, 2, 1)) if count] + [4]
        if demands and n < max(demands):
            return False
    return True


def compatible(first, second):
    return not ((first['e'] == 0 and second['eligible']) or (second['e'] == 0 and first['eligible']))


def main():
    begun = time.monotonic()
    independent = json.loads((S / 'pass19-high-T-polynomial.json').read_text())
    produced = json.loads((S / 'pass19-high-T-producer.json').read_text())
    author = json.loads((S / 'pass19-high-T-cut-producer.json').read_text())
    need(independent['rows'] == produced['rows'] and independent['inventory'] == produced['inventory'],
         'all literal rows and whole completed census records')
    inv = independent['inventory']
    types = inv['types']
    survivors = [dict(branch=[b[k] for k in ('Q', 'T', 'X', 'tau')], population=t['population'])
                 for b in inv['branches'] for t in b['templates'] if not t['failures']]
    need(survivors == author['necessary_populations'], 'complete ordered surviving census stream')
    targets = sorted(D for D in compositions(24, 4) if 5 <= D[0] <= 13 and all(1 <= d <= 9 for d in D[1:]))
    need(len(targets) == author['labelled_D_targets'] == 489, 'full independently generated D rectangle')
    rectangle = set(targets)
    reconstructed = []
    attempts = 0
    support_statistics = []
    for rec in survivors:
        pop = rec['population']
        vertices = [dict(type_id=t, **types[t]) for t, count in pop for _ in range(count)]
        need(len(vertices) == 14, 'all fourteen distinct SAT positions retained')
        unit_ids = [i for i, v in enumerate(vertices) if v['e'] == 0]
        unit_set = set(unit_ids)
        unit_demand = sum(vertices[i]['ss_hist'][0] for i in unit_ids)
        available_internal = [(i, j) for i, j in itertools.combinations(unit_ids, 2)
                              if compatible(vertices[i], vertices[j])]
        internal = min(unit_demand, 2*len(available_internal))
        external = sum(min(v['ss_hist'][0], sum(compatible(vertices[i], v) for i in unit_ids))
                       for j, v in enumerate(vertices) if j not in unit_set)
        if unit_demand > internal + external:
            reconstructed.append(dict(**rec, kind='UNIT_CAPACITY', unit_count=len(unit_ids),
                                      unit_demand=unit_demand, internal_incidence_upper=internal,
                                      external_incidence_upper=external))
            continue
        if unit_ids and external == 0 and unit_demand % 2:
            reconstructed.append(dict(**rec, kind='CLOSED_UNIT_PARITY', unit_count=len(unit_ids),
                                      closed_unit_degree_sum=unit_demand, external_incidence_upper=0))
            continue
        degree = [sum(v['ss_hist']) for v in vertices]
        if all(v['h'] == 4 and v['k'] == 1 for v in vertices) and len(set(degree)) == 1:
            roots = [i for i, v in enumerate(vertices) if v['hub_weight'] == v['q'] == 1]
            if roots:
                i = roots[0]
                friends = 1 + 3*vertices[i]['hub_weight'] - vertices[i]['q']
                lower = len(vertices) - friends
                # Explicit root slots and new slots from each neighbour,
                # permitting all overlaps to disappear gives a safe upper bound.
                upper = 1 + degree[i] + degree[i]*(max(degree) - 1)
                need(lower > upper, 'independent necessary ball inequalities')
                reconstructed.append(dict(**rec, kind='GENERALIZED_RADIUS', root_type=vertices[i]['type_id'],
                                          graph_regular_degree=degree[i], hub_friend_upper=friends,
                                          two_step_ball_lower=lower, two_step_ball_upper=upper))
                continue
        totals = dict(pop)
        need(set(totals) <= {16, 17, 18, 20}, 'all remaining rows require a justified support meaning')
        A, btotal, ctotal, jtotal = (totals.get(t, 0) for t in (16, 17, 18, 20))
        weights = Counter()
        passing = {D: [] for D in targets}
        weakened = []
        tested = 0
        for B, C, J in itertools.product(compositions(btotal, 4), compositions(ctotal, 4), compositions(jtotal, 4)):
            attempts += 1
            tested += 1
            need(attempts <= 500000 and time.monotonic() - begun < 20,
                 'INCOMPLETE unchanged500000/20s independent composition guard')
            D = tuple(b + 2*c + 2*j for b, c, j in zip(B, C, J))
            N = tuple(b + c + j for b, c, j in zip(B, C, J))
            need(sum(D) == 24 and sum(N) == 14 - A, 'actual support totals')
            if D not in rectangle:
                continue
            weights[D] += 1
            witness = dict(B4=list(B), C4=list(C), J4=list(J), N4=list(N), D4=list(D))
            if fit_support(B, C, J, N):
                passing[D].append(witness)
            if fit_support(B, C, J, N, weaken=True):
                weakened.append(witness)
        need(not any(passing.values()), 'independent typed support allocation survives')
        weakened.sort(key=lambda r: (r['D4'], r['N4'], r['J4']))
        rows = [dict(D4=list(D), pre_support_typed_allocations=weights[D], passing_support=passing[D]) for D in targets]
        reconstructed.append(dict(**rec, kind='DISJOINT_SUPPORT', neutral_rows=A, B_rows=btotal,
                                  C_rows=ctotal, J_rows=jtotal, degree_targets=len(targets), target_rows=rows,
                                  pre_support_typed_allocations=sum(weights.values()), passing_support_allocations=0,
                                  weakened_C_threshold=4, weakened_threshold_witnesses=weakened))
        support_statistics.append(dict(B_rows=btotal, C_rows=ctotal, J_rows=jtotal,
                                       typed_compositions=tested, D_rectangle_allocations=sum(weights.values()),
                                       passing=0, weakened_C4=len(weakened)))
    need(reconstructed == author['records'], 'every full certificate, D multiplicity and weakened witness must agree')
    need(len(reconstructed) == 8 and attempts == 42721, 'entire eight-population independent scope')
    # The controls are abstract relaxations, not packing witnesses.
    need(fit_support((0, 0, 2, 2), (3, 4, 0, 2), (1, 0, 0, 0), (4, 4, 2, 4), weaken=True),
         'positive weakened support model')
    need(not fit_support((0, 0, 2, 2), (3, 4, 0, 2), (1, 0, 0, 0), (4, 4, 2, 4)),
         'strict support must reject the weakened model')
    need(1 + 3 + 3*(3 - 1) == 14 - 4, 'positive radius boundary sensitivity control')
    verified_controls = dict(mixed_support_weakened_C4=next(
        r['weakened_C4'] for r in support_statistics if r['B_rows'] == 4 and r['J_rows'] == 1),
        weakened_radius_L4_boundary=int(1 + 3 + 3*(3 - 1) == 14 - 4))
    need(verified_controls == author['controls'], 'independently reconstructed sensitivity controls')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_INDEPENDENT_T3_T4_CERTIFICATE_AGREEMENT',
                  scalar_branches=len(inv['branches']), raw_vectors=sum(len(b['templates']) for b in inv['branches']),
                  checked_populations=len(reconstructed), support_compositions=attempts,
                  all_ordered_census_records_matched=True, all_full_certificates_and_witnesses_matched=True,
                  certificate_records_sha256=hashlib.sha256(CANON(reconstructed)).hexdigest(),
                  support_statistics=support_statistics, controls=verified_controls,
                  external_review=False, ordinary_bridges_formalized=False, unrestricted_code_bound=None,
                  state_guard=500000, time_guard_seconds=20, elapsed_seconds=time.monotonic() - begun)
    out = S / 'pass19-independent-high-T-cuts.json'
    need(not out.exists(), 'fresh independent output required')
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
