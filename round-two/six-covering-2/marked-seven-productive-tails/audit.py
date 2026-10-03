"""Literal physical audit of every field of the H BASE 15/18 calculation."""
import argparse
import copy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

FIXED = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 10), (28, 4))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def physical_records():
    labels = sorted({2 ** a * 3 ** b * 5 ** c * 7 ** d
                     for a, b, c, d in product(range(4), range(3), range(2), range(2))
                     if 2 ** a * 3 ** b * 5 ** c * 7 ** d >= 8})
    free = [m for m in labels if m not in dict(FIXED)]
    require(len(labels) == 41 and len(free) == 35, 'Original inventory incomplete')
    require(all(2520 % m == 0 for m in labels), 'Invalid original BASE divisor')

    def ap(m, a):
        mask = 0
        for x in range(a, 2520, m):
            mask |= 1 << x
        return mask

    occupied = 0
    for m, a in FIXED:
        occupied |= ap(m, a)
    required = ((1 << 2520) - 1) ^ occupied
    require(required.bit_count() == 1396, 'Wrong literal initial holes')
    require(all(bool(required & (1 << x)) == all(x % m != a for m, a in FIXED)
                for x in range(2520)), 'Initial AP union differs at an integer')
    actions = {m: [ap(m, a) for a in range(m)] for m in free}
    remaining = [m for m in free if m not in (15, 18)]
    rows = {}
    for b in reversed(range(18)):
        for a in reversed(range(15)):
            covered = required & (actions[15][a] | actions[18][b])
            unhit = required & ~covered
            marginals = []
            for m in remaining:
                best = 0
                for mask in reversed(actions[m]):
                    gain = (mask & unhit).bit_count()
                    if gain > best:
                        best = gain
                marginals.append(best)
            size = covered.bit_count()
            rows[(a, b)] = [[a, b], size, marginals, size + sum(marginals)]
    ordered = [rows[(a, b)] for a in range(15) for b in range(18)]
    require(len(rows) == 270, 'Missing raw phase pair')
    return {'initial_holes': required.bit_count(), 'free_original_labels': free,
            'raw_free_phase_count': sum(free), 'remaining_originals': remaining,
            'rows': ordered}


def check(candidate, truth):
    require(candidate['original_BASE_prefix'] == [list(x) for x in FIXED],
            'Wrong literal prefix')
    require(candidate['period'] == 2520, 'Wrong physical period')
    for key in ('initial_holes', 'free_original_labels', 'raw_free_phase_count'):
        require(candidate[key] == truth[key], 'Changed actual original inventory: ' + key)
    require(candidate['stable_covered_cutoff'] == 1276, 'Changed uniform cutoff')
    require(len(candidate['stages']) == 1, 'Unexpected or omitted complete stage')
    s = candidate['stages'][0]
    require(s['fixed_originals'] == [15, 18], 'Changed fixed originals')
    require(s['remaining_originals'] == truth['remaining_originals'],
            'Original marginal resources omitted or relabeled')
    require(s['expected_rows'] == 270 and len(s['rows']) == 270,
            'Missing or duplicated original phase pair')
    require(s['rows'] == truth['rows'], 'A physical phase/union/marginal/bound changed')
    digest = sha256(json.dumps(truth['rows'], separators=(',', ':')).encode()).hexdigest()
    require(s['rows_sha256'] == digest, 'Full record digest changed')
    require(s['upper_bound_range'] == [1051, 1219], 'Wrong complete range')
    require(s['retained_phases'] == [], 'Unexpected survivor')
    require(max(row[-1] for row in truth['rows']) == 1219,
            'Global literal upper bound changed')
    # Status strings and producer assertions are not proof premises.
    return {'root_records': 270, 'all_original_marginal_values': 270 * 33,
            'physical_phase_intersections': 270 * (9251 - 15 - 18),
            'initial_BASE_holes': 1396, 'entire_BASE_covered_upper_bound': 1219,
            'minimum_BASE_holes': 177, 'root_records_sha256': digest,
            'all_ordinary_completeness_bridges_formalized': False,
            'independent_reviewer': False, 'full_cover_excluded': False,
            'global_bound_changed': False}


def damage_controls(candidate, truth):
    checks = []
    for name in ('cutoff', 'first-phase', 'last-bound', 'first-marginal',
                 'delete-row', 'duplicate-row', 'omit21-resource', 'prefix14',
                 'initial-hole-count', 'false178-lower-bound'):
        damaged = copy.deepcopy(candidate)
        stage = damaged['stages'][0]
        if name == 'cutoff':
            damaged['stable_covered_cutoff'] = 1275
        elif name == 'first-phase':
            stage['rows'][0][0][0] = 1
        elif name == 'last-bound':
            stage['rows'][-1][-1] += 1
        elif name == 'first-marginal':
            stage['rows'][0][2][-1] += 1
        elif name == 'delete-row':
            stage['rows'].pop()
        elif name == 'duplicate-row':
            stage['rows'][-1] = copy.deepcopy(stage['rows'][0])
        elif name == 'omit21-resource':
            stage['remaining_originals'].remove(21)
        elif name == 'prefix14':
            damaged['original_BASE_prefix'][3][1] = 1
        elif name == 'initial-hole-count':
            damaged['initial_holes'] -= 1
        elif name == 'false178-lower-bound':
            stage['upper_bound_range'][-1] = 1218
        # Repair the digest after semantic damage: hashes alone must not accept it.
        stage['rows_sha256'] = sha256(json.dumps(stage['rows'],
            separators=(',', ':')).encode()).hexdigest()
        try:
            check(damaged, truth)
        except ValueError as error:
            checks.append({'damage': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Semantic damage accepted: ' + name)
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('candidate')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    candidate = json.loads(Path(args.candidate).read_text())
    truth = physical_records()
    summary = check(candidate, truth)
    summary.update({'agent': 'six-covering-2', 'role': 'researcher',
                    'all_full_records_match': True,
                    'controls': damage_controls(candidate, truth)})
    Path(args.out).write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
