"""Complete affine point maps, character identities, integer lifts and tiny positives."""
import hashlib
import json
from math import gcd
from check_kernel import symbol


def need(ok, message):
    if not ok:
        raise ValueError(message)


def point_tags(pole, roots, half):
    patterns = {r: tuple(symbol((r - a) % 31) for a in roots)
                for r in range(31) if r != pole and r not in roots}
    keys = sorted(set(patterns.values()))
    need(len(keys) == 8, 'every transported pattern remains present')
    tags = []
    for n in range(62 * half):
        r, s = n % 31, n % (2 * half)
        if r == pole:
            tags.append(None)
        else:
            row = 8 + roots.index(r) if r in roots else keys.index(patterns[r])
            v = row * half + s % half + 1
            tags.append(v if s < half else -v)
    return tags


def check():
    multiplicative = 0
    for a in range(1,31):
        for x in range(1,31):
            need(symbol(a * x % 31) == (symbol(a) ^ symbol(x)), 'entire field character multiplicativity')
            multiplicative += 1
    bit_permutations = 0
    for mask in range(8):
        images = [word ^ mask for word in range(8)]
        need(sorted(images) == list(range(8)), 'independent input-sign flips preserve arbitrary lookup tables')
        bit_permutations += len(images)
    point_maps = 0
    regular_maps = 0
    root_maps = 0
    cases = 0
    transcript = hashlib.sha256()
    for half in [5,10]:
        phase = 2 * half
        period = 31 * phase
        base = point_tags(0, [1,2,4], half)
        inverse_phase = pow(phase, -1, 31)
        for pole in range(31):
            root_sets = set()
            for scale in range(1,31):
                roots = [(pole + scale * r) % 31 for r in [1,2,4]]
                need(pole not in roots and len(set(roots)) == 3, 'retained roots all differ from the physical pole')
                root_sets.add(tuple(sorted(roots)))
                target = point_tags(pole, roots, half)
                multiplier = 1 + phase * ((scale - 1) * inverse_phase % 31)
                shift = phase * (pole * inverse_phase % 31)
                need(gcd(multiplier, period) == 1 and multiplier % 31 == scale
                     and multiplier % phase == 1 and shift % 31 == pole and shift % phase == 0,
                     'actual cyclic CRT affine map is a unit and preserves phase')
                permutation = []
                for row in range(11):
                    mapped = row if row >= 8 or symbol(scale) == 0 else 7 - row
                    permutation.extend(mapped * half + j + 1 for j in range(half))
                need(sorted(permutation) == list(range(1,11 * half + 1)), 'all root and pattern inputs freely permuted')
                seen = set()
                for n, tag in enumerate(base):
                    image = (multiplier * n + shift) % period
                    seen.add(image)
                    expected = None if tag is None else permutation[abs(tag) - 1] * (1 if tag > 0 else -1)
                    need(target[image] == expected, 'EVERY actual affine point tag and root identity')
                    point_maps += 1
                    regular_maps += tag is not None
                    root_maps += n % 31 in [1,2,4]
                    transcript.update(f'{half},{pole},{scale},{n},{image},{expected};'.encode())
                need(len(seen) == period, 'entire physical point map is bijective')
                cases += 1
            need(len(root_sets) == 30, 'thirty distinct relative geometric root triples at each pole')
    lifts = 0
    largest = 0
    for a in range(310):
        for d in range(1,310):
            if d <= 155:
                start, step = a, d
                expected = [(a + j * d) % 310 for j in range(7)]
            else:
                start, step = (a + 6 * d) % 310, 310 - d
                expected = [(a + (6 - j) * d) % 310 for j in range(7)]
            actual = [start + j * step for j in range(7)]
            need([x % 310 for x in actual] == expected and step > 0 and len(set(actual)) == 7,
                 'all original cyclic progressions have distinct positive-step integer lifts')
            need(actual[-1] <= 1239 and 2 * actual[-1] <= 2478, 'uniform finite310 and even620 interval bounds')
            need([(2 * x) % 620 for x in actual] == [(2 * x) % 620 for x in expected], 'entire even-slice AP embedding')
            largest = max(largest, actual[-1])
            lifts += 1
    phase_good = []
    for mask in range(32):
        row = [(mask >> s) & 1 for s in range(5)]
        row += [1 - v for v in row]
        valid = all(len({row[(a + j * d) % 10] for j in range(7)}) == 2
                    for a in range(10) for d in range(1,10))
        if valid:
            phase_good.append(mask)
    need(phase_good == [v for v in range(32) if v not in [10,21]], 'WHOLE tiny antipodal phase inventory')
    tiny_roots = [1,2,4]
    tiny_patterns = {r: tuple(sum((k * ((r - a) % 7)) % 7 > 3 for k in range(1,4)) % 2
                              for a in tiny_roots)
                     for r in [3,5,6]}
    need(len(set(tiny_patterns.values())) == 3, 'three distinct actual q7 patterns plus three free roots')
    tiny_pairs = tiny_regular = 0
    for a in range(70):
        for d in range(1,70):
            terms = [(a + j * d) % 70 for j in range(7)]
            tiny_pairs += 1
            if any(x % 7 == 0 for x in terms):
                continue
            need(d % 7 == 0, 'every regular q7 AP stays in one field')
            tiny_regular += 1
    need(tiny_regular == 540 and tiny_pairs == 4830, 'complete actual positive-control AP domain')
    return {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'COMPLETE_AFFINE_TRANSPORT_AND_FINITE_LIFT_CHECK',
            'character_product_identities': multiplicative, 'input_flip_entries': bit_permutations,
            'affine_cases_per_period': 930, 'period_cases_total': cases, 'all_point_maps': point_maps,
            'regular_point_maps': regular_maps, 'retained_root_point_maps': root_maps,
            'point_map_sha256': transcript.hexdigest(), 'all_original310_lifts': lifts,
            'max310_endpoint': largest, 'max_even620_endpoint': 2 * largest,
            'tiny_phase_inputs': 32, 'tiny_legal_phase_rows': len(phase_good),
            'tiny_original_pairs': tiny_pairs, 'tiny_regular_pairs': tiny_regular,
            'exact_tiny_character_cores': 30 ** 6,
            'scope': 'All930 relative-pole affine transports and two finite sufficient bounds; no optimal cutoff or unrestricted core exclusion.'}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
