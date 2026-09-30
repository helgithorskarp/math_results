"""Literal one-word replacement interfaces and sharp local three-charge examples."""
from itertools import combinations
from hashlib import sha256
import json

from exact import insist, encoded, mask, bits, pairs, plane, packing


def configurations():
    first = mask(range(4))
    yield 'parallel', first, mask(range(4, 8)), 0, 4
    yield 'common-marker', first, mask((0, 4, 8, 12)), 0, 0
    yield 'cross-marker', first, mask((0, 4, 8, 12)), 0, 4


def data():
    p = plane()
    records = []
    for name, l1, l2, a1, a2 in configurations():
        tails = (l1 ^ (1 << a1), l2 ^ (1 << a2))
        insist(not tails[0] & tails[1] and (l1 & l2).bit_count() <= 1, 'invalid completion interface')
        shortened = [q for q in p if q not in (l1, l2)]
        star = [q | 1 << 17 for q in shortened] + [t | 1 << 16 | 1 << 17 for t in tails]
        packing(star, size=20)
        charges = [mask((a,) + q) for t, a in zip(tails, (a1, a2)) for q in combinations(tuple(bits(t)), 2)]
        insist(len(set(charges)) == 6, 'charges not distinct')
        four = [mask(q) for q in combinations(range(16), 4)]
        five = [mask(q) for q in combinations(range(16), 5)]
        vwords = [q for q in four if all((q & t).bit_count() <= 1 for t in tails)]
        candidates = [q for q in five if all((q & w).bit_count() <= 2 for w in star)]
        for line in (l1, l2):
            insist(all((q & line).bit_count() <= 1 for q in shortened), 'first-star word fails after completion')
            insist(all((q & line).bit_count() <= 2 for q in vwords), 'remaining second-star interface fails')
        for j, line in enumerate((l1, l2)):
            triple_menu = charges[3*j:3*j+3]
            # Complete literal residual domain, without the rest of the star imposed.
            for q in five:
                if all((q & t).bit_count() <= 2 for t in tails):
                    hit = [c for c in triple_menu if q & c == c]
                    insist(((q & line).bit_count() >= 3) == bool(hit) and len(hit) <= 1,
                           'one-line three-triple characterization fails')
            retained = [w for i, w in enumerate(star) if i != 18+j] + [line | 1 << 17]
            packing(retained, size=20)
            insist(sum(w >> 17 & 1 for w in retained) == 20 and sum(w >> 16 & 1 for w in retained) == 1,
                   'one-word first-star parameter change')
        bad = [q for q in candidates if any((q & line).bit_count() >= 3 for line in (l1, l2))]
        domains = [{w for w in bad if [j for j, c in enumerate(charges) if w & c == c] == [i]} for i in range(6)]
        states = 0

        def choose(available, selected):
            nonlocal states
            states += 1
            if states > 200000:
                raise RuntimeError('INCOMPLETE: local sharpness witness guard')
            if not available:
                return selected
            row = min(available, key=lambda k: (len(available[k]), k))
            for w in sorted(available[row]):
                rest = {j: {z for z in ds if (z & w).bit_count() <= 2}
                        for j, ds in available.items() if j != row}
                if any(not ds for ds in rest.values()):
                    continue
                answer = choose(rest, selected + [w])
                if answer is not None:
                    return answer
            return None

        witness = choose(dict(enumerate(domains)), [])
        insist(witness is not None and len(witness) == 6, 'six-charge local witness not found')
        packing(star + witness, size=26)
        deletions = []
        for j, line in enumerate((l1, l2)):
            discarded = [w for w in witness if (w & line).bit_count() >= 3]
            insist(len(discarded) == 3, 'single-line loss not sharp locally')
            replaced = [w for i, w in enumerate(star) if i != 18+j] + [line | 1 << 17]
            replaced += [w for w in witness if w not in discarded]
            packing(replaced, size=23)
            deletions.append(discarded)
        records.append({'case': name, 'missing_lines': [l1, l2], 'markers': [a1, a2], 'tails': list(tails),
                        'remaining_v_quadruples': len(vwords), 'old_residual_candidates': len(candidates),
                        'charged_candidates': len(bad), 'single_charge_domain_sizes': [len(d) for d in domains],
                        'six_word_witness': witness, 'three_word_deletions': deletions, 'witness_states': states,
                        'witness_second_replication': 2, 'full_saturated_pair_witness': False})
    return records


def baseline(path):
    raw = path.read_bytes()
    lines = raw.decode().splitlines()
    insist(len(lines) == 69 and all(len(s) == 18 and set(s) <= {'0', '1'} for s in lines), 'baseline encoding')
    words = [mask(i for i, c in enumerate(s) if c == '1') for s in lines]
    packing(words, size=69)
    degree = [sum(w >> x & 1 for w in words) for x in range(18)]
    relevant = []
    for u in range(18):
        if degree[u] != 20:
            continue
        for v in range(18):
            if v != u and sum(bool(w >> u & 1) and bool(w >> v & 1) for w in words) == 2:
                relevant.append({'u': u, 'v': v, 'other_replication': degree[v]})
    insist(len(relevant) == 7 and all(r['other_replication'] == 12 for r in relevant), 'second-saturation hypothesis control')
    return {'words': 69, 'oriented_twenty_pair_two_instances': relevant, 'sha256': sha256(raw).hexdigest(),
            'meaning': 'Known69 code disproves dropping the second replication20 hypothesis; not a new construction.'}
