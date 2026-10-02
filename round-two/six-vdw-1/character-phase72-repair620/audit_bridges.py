"""Literal audits of the written phase/root actions and field-support lift."""
import hashlib
import json
import math


def need(ok, message):
    if not ok:
        raise ValueError(message)


def crt(r, s):
    return s + 20 * (((r - s) * 14) % 31)


def lift(a, d):
    need(0 <= a < 620 and 1 <= d < 620 and d % 31 != 0, 'nonzero field-step original AP')
    if d > 310:
        a = (a + 6 * d) % 620
        d = 620 - d
    need(1 <= d <= 309, 'half-step has zero field difference and is outside this domain')
    half_flip = int(a >= 310)
    a %= 310
    return a, d, half_flip


if __name__ == '__main__':
    squares = {r * r % 31 for r in range(1, 31)}
    character = [None] + [int(r not in squares) for r in range(1, 31)]
    phase = [int(bool(72 & (1 << (s % 10)))) ^ int(s >= 10) for s in range(20)]
    orbit = {}
    for u in range(20):
        if math.gcd(u, 20) == 1:
            for v in range(20):
                word = [phase[(u * s + v) % 20] for s in range(20)]
                mask = sum(word[s] * (1 << s) for s in range(10))
                orbit.setdefault(mask, (u, v, word))
    phase_points = phase_anti = legal_pairs = 0
    for mask, (u, v, word) in orbit.items():
        multiplier, shift = crt(1, u), crt(0, v)
        need(math.gcd(multiplier, 620) == 1, 'actual phase-affine CRT multiplier is a unit')
        for n in range(620):
            image = (multiplier * n + shift) % 620
            need(image % 31 == n % 31 and word[n % 20] == phase[image % 20], 'all physical phase pushforward points')
            phase_points += 1
        for s in range(10):
            need(word[s + 10] == 1 - word[s], 'whole phase orbit remains antipodal')
            phase_anti += 1
        for s in range(20):
            for d in range(1, 20):
                need(len({word[(s + j * d) % 20] for j in range(7)}) == 2, 'all original phase steps in each orbit member legal')
                legal_pairs += 1
    root_points = 0
    for root in range(1, 31):
        h = -root % 31
        multiplier = crt(h, 1)
        need(math.gcd(multiplier, 620) == 1, 'actual field-scalar CRT multiplier is a unit')
        for n in range(620):
            image = multiplier * n % 620
            need(image % 31 == h * (n % 31) % 31 and image % 20 == n % 20,
                 'literal physical pole and phase-preserving root normalization')
            if n % 31 not in [0, 30]:
                arg = (image % 31 - root) % 31
                need(character[arg] == character[(n % 31 + 1) % 31] ^ character[h],
                     'whole normalized regular nonroot shifted-character point identity')
                root_points += 1
    linear_points = 0
    for alpha in range(1, 31):
        for beta in range(31):
            root = -beta * pow(alpha, -1, 31) % 31
            for r in range(31):
                if r == root:
                    continue
                need(character[(alpha * r + beta) % 31] == character[alpha] ^ character[(r - root) % 31],
                     'all nonzero linear coefficient/root points including regular field0')
                linear_points += 1
    colors = [None if n % 31 == 0 else character[n % 31] ^ phase[n % 20] for n in range(620)]
    support_pairs = bad_pairs = maximum_zero_based = maximum_bad_zero_based = 0
    sha = hashlib.sha256()
    for origin in range(620):
        for diff in range(1, 620):
            if diff % 31 == 0:
                continue
            a, d, flip = lift(origin, diff)
            positions = [a + j * d for j in range(7)]
            original = [(origin + j * diff) % 620 for j in range(7)]
            need({n % 31 for n in positions} == {n % 31 for n in original}, 'every actual lifted field support preserved')
            need(max(positions) <= 2163, 'written uniform one-based prefix2164')
            maximum_zero_based = max(maximum_zero_based, max(positions))
            support_pairs += 1
            values = [colors[n] for n in original]
            if None not in values and len(set(values)) == 1:
                need(all(colors[n % 620] == (values[0] ^ flip) for n in positions), 'all bad original APs have literal monochromatic integer lifts')
                bad_pairs += 1
                maximum_bad_zero_based = max(maximum_bad_zero_based, max(positions))
                sha.update(bytes([origin % 31, diff % 31, flip]))
                sha.update(a.to_bytes(2, 'big') + d.to_bytes(2, 'big'))
    need(support_pairs == 372000 and bad_pairs == 7680, 'complete original nonzero-field and bad-AP domains')
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'COMPLETE_LITERAL_PHASE_ROOT_AND_FIELD_SUPPORT_LIFT_AUDIT',
                      'phase_affine_orbit_masks': sorted(orbit), 'phase_crt_point_identities': phase_points,
                      'phase_antipodal_identities': phase_anti, 'all_orbit_phase_pairs': legal_pairs,
                      'all_normalized_nonzero_root_points': root_points,
                      'all_nonzero_linear_coefficient_regular_points': linear_points,
                      'all_nonzero_field_step_support_lifts': support_pairs,
                      'all_original_bad_AP_integer_lifts': bad_pairs,
                      'uniform_maximum_zero_based_endpoint': maximum_zero_based,
                      'actual_mask72_bad_lift_maximum_zero_based_endpoint': maximum_bad_zero_based,
                      'sufficient_one_based_prefix_length': 2164,
                      'bad_lift_sha256': sha.hexdigest(),
                      'scope': 'Literal checks of written ordinary bridges; no optimal endpoint or phase orbit outside the specified twenty masks.'}, sort_keys=True))
