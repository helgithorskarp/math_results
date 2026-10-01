"""Same-author physical-set audit; no production imports or bit masks."""
from functools import lru_cache
import json
import hashlib
from math import gcd
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def nondominated(options):
    options = set(options)
    return tuple(sorted(p for p in options if not any(
        q != p and q[0] >= p[0] and q[1] >= p[1] for q in options)))


def rebuild(a18, c6, consumed):
    labels = tuple(m for m in range(8, 721) if 720 % m == 0)
    pool = tuple(m for m in labels if m not in (8, 9) and m not in consumed)
    known = {x for x in range(720) if x % 8 == 5 or x % 9 == 6 or
             x % 18 == a18 or x % 6 == c6 or any(x % m == a for m, a in consumed.items())}
    residual = set(range(720)) - known
    odds = {x for x in residual if x % 2}
    evens = residual - odds
    phases = {m: tuple((odds.intersection(range(a, 720, m)),
                       evens.intersection(range(a, 720, m))) for a in range(m))
              for m in pool}
    low, high = pool[:12], pool[12:]
    require(len(pool) in (20, 21) and len(low) == 12 and len(high) in (8, 9),
            'independent original resource census')
    pairs = {(m, n): nondominated((len(o | oo), len(e | ee))
                                 for o, e in phases[m] for oo, ee in phases[n])
             for i, m in enumerate(low) for n in low[i + 1:]}
    high_states = {(0, 0)}
    for m in high:
        single = nondominated((len(o), len(e)) for o, e in phases[m])
        high_states = set(nondominated((o + a, e + b)
                                      for o, e in high_states for a, b in single))

    @lru_cache(None)
    def upper(remaining, need):
        if not remaining:
            return max((e for o, e in high_states if o >= need), default=None)
        m, tail = remaining[0], remaining[1:]
        answers = []
        for n in tail:
            reduced = tuple(k for k in tail if k != n)
            values = []
            for o, e in pairs[m, n]:
                child = upper(reduced, max(0, need - o))
                if child is not None:
                    values.append(e + child)
            if not values:
                return None
            answers.append(max(values))
        require(answers, 'independent pool has an unpaired resource')
        return min(answers)

    bound = upper(low, len(odds))
    return [len(odds), len(evens), bound], sum(m * n for m, n in pairs)


def main():
    here = Path(__file__).resolve().parent
    c = json.loads((here / 'certificate.json').read_text())
    labels = [m for m in range(8, 721) if 720 % m == 0]
    reps = [[0, 2], [0, 4], [3, 1], [3, 2], [3, 4], [3, 5]]
    parents = [[0, 2, 4], [0, 2, 10], [0, 2, 11], [0, 4, 2], [0, 4, 7], [0, 4, 8]]
    prior_bytes = (here.parent / 'stage720-six-orbit-reduction' / 'certificate.json').read_bytes()
    prior_hash = '99c433aad2c1f5a6d7246fb619efef9b387de021ddeccac8fe4d4bd59d96cbf2'
    require(hashlib.sha256(prior_bytes).hexdigest() == prior_hash, 'independent dependency pin')
    require(c['schema'] == 'stage720-consumed12-16-v1' and c['period'] == 720 and
            c['original_labels'] == labels and c['fixed'] == [[8, 5], [9, 6]] and
            c['target_divisors'] == [18, 6] and c['low_count'] == 12 and
            c['representatives'] == reps and c['affine_map'] == [17, 48],
            'independent mathematical domain')
    require(c['remaining_targets'] == json.loads(prior_bytes)['remaining_shapes'] and
            c['free_after12'] == [m for m in labels if m not in (8, 9, 12)] and
            c['free_after12_16'] == [m for m in labels if m not in (8, 9, 12, 16)] and
            c['second_parent_prefixes'] == parents,
            'independent target/resource inventory')
    require(c['dependency'] == {'source_commit': 'c87f46d672552ca570cd7bc0293969a4e3688c17',
                               'graph_reference': 'bafkreibhwbabvc6mqjab3riotqp33y52r73wffazskkh7rcpbhwadaz76m',
                               'certificate_sha256': prior_hash}, 'independent dependency identity')
    first, second, combinations = [], [], 0
    for a, d in reps:
        for b in range(12):
            values, count = rebuild(a, d, {12: b})
            first.append([a, d, b, *values])
            combinations += count
    is_strict = lambda r: r[-1] is None or r[-1] < r[-2]
    require([r[:3] for r in first if not is_strict(r)] == parents,
            'independent nonstrict-parent census')
    for a, d, b in parents:
        for f in range(16):
            values, count = rebuild(a, d, {12: b, 16: f})
            second.append([a, d, b, f, *values])
            combinations += count
    require(first == c['first_rows'] and second == c['second_rows'] and
            all(is_strict(r) for r in second), 'independent physical count bounds')
    u, t = 17, 48
    require(gcd(u, 720) == 1, 'independent affine unit')
    targets = set()
    for a, d in reps:
        aa, dd = (u * a + t) % 18, (u * d + t) % 6
        source = {x for x in range(720) if x % 18 == a or x % 6 == d}
        target = {x for x in range(720) if x % 18 == aa or x % 6 == dd}
        require({(u * x + t) % 720 for x in source} == target, 'independent target image')
        targets.update(((a, d), (aa, dd)))
    require(targets == {tuple(row) for row in c['remaining_targets']},
            'independent complete twelve-target transfer')
    phase_checks = 0
    for m in labels:
        for a in range(m):
            source = set(range(a, 720, m))
            target = set(range((u * a + t) % m, 720, m))
            require({(u * x + t) % 720 for x in source} == target,
                    'independent original congruence-family image')
            phase_checks += 1
    fixed = {x for x in range(720) if x % 8 == 5 or x % 9 == 6}
    translations = 0
    for a in range(8):
        for b in range(9):
            shifts = [s for s in range(72) if (a + s) % 8 == 5 and (b + s) % 9 == 6]
            require(len(shifts) == 1, 'independent normalization existence/uniqueness')
            source = {x for x in range(720) if x % 8 == a or x % 9 == b}
            require({(x + shifts[0]) % 720 for x in source} == fixed,
                    'independent physical fixed-set normalization')
            translations += 1
    leaves = [r for r in first if is_strict(r)] + second
    result = {'computed_prefixes': len(first) + len(second),
              'first_cases': len(first), 'first_strict': sum(is_strict(r) for r in first),
              'second_cases': len(second), 'second_strict': sum(is_strict(r) for r in second),
              'strict_leaves': len(leaves),
              'minimum_integer_gap': min(r[-2] - r[-1] for r in leaves if r[-1] is not None),
              'unreachable_count_thresholds': sum(r[-1] is None for r in first + second),
              'complete_original_pair_phase_combinations': combinations,
              'affine_original_phase_checks': phase_checks, 'anchor_translation_checks': translations,
              'remaining_target_shapes': 0, 'global_numerical_bound_changed': False}
    require(result == json.loads((here / 'expected.json').read_text()),
            'independent frozen summary differs')
    print(json.dumps({'agent': 'six-covering-1', 'role': 'researcher', 'status': 'AUDITED',
                      'same_author': True, 'production_imported': False, **result}, sort_keys=True))


if __name__ == '__main__':
    main()
