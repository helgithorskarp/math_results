"""Exact two-exception CRT phase normalization and bounded finite controls."""
from collections import Counter
from itertools import combinations
import time


def normalize_phase(phi):
    assert len(phi) == 103 and all(type(v) is int and 0 <= v < 6 for v in phi)
    tau = [v % 3 for v in phi]
    counts = Counter(tau)
    baseline = max(counts, key=counts.get)
    assert counts[baseline] == 101
    exceptions = [x for x in range(103) if tau[x] != baseline]
    p, q = exceptions
    shifted = [(v - baseline) % 6 for v in phi]
    # A y reflection fixes baseline0 and exchanges exception labels1/2.
    reflect = shifted[p] % 3 == 2
    values = [(-v) % 6 for v in shifted] if reflect else shifted
    alpha, beta = (q - p) % 103, p
    result = [values[(alpha*x + beta) % 103] for x in range(103)]
    label = 'same' if result[0] % 3 == result[1] % 3 else 'mixed'
    assert [v % 3 for v in result] == [1, 1 if label == 'same' else 2] + [0]*101
    # The following global color exchange sets u(0), not tau(0).
    complemented = result[0] >= 3
    if complemented:
        result = [(v + 3) % 6 for v in result]
    assert result[0] == 1
    return result, {'case': label, 'alpha': alpha, 'beta': beta,
                    'baseline': baseline, 'reflect': reflect,
                    'global_complement': complemented}


def controls():
    begin = time.monotonic()
    # For all six phases, all y, all baseline shifts, and both reflections,
    # compare actual colors rather than just the ternary labels.
    phase_entries = 0
    for phase in range(6):
        for y in range(6):
            for baseline in range(3):
                for reflect in [False, True]:
                    shifted = (phase - baseline) % 6
                    new_phase = (-shifted) % 6 if reflect else shifted
                    old_y = (baseline + (2-y if reflect else y)) % 6
                    assert int((old_y-phase) % 6 >= 3) == int((y-new_phase) % 6 >= 3)
                    phase_entries += 1
    # All3*C(103,2)*4=63036 ternary skeletons with exactly two exceptions.
    # A single deterministic orientation is used here; the phase truth table
    # above and written formula establish the transformation for every bit.
    orbit_counts = Counter()
    normalized_hashes = set()
    for baseline in range(3):
        labels = [v for v in range(3) if v != baseline]
        for p, q in combinations(range(103), 2):
            for a in labels:
                for b in labels:
                    tau = [baseline]*103
                    tau[p], tau[q] = a, b
                    phi = [v + 3*((x*x+7*x+p+q) % 2) for x, v in enumerate(tau)]
                    normalized, transform = normalize_phase(phi)
                    orbit_counts[transform['case']] += 1
                    normalized_hashes.add(tuple(v % 3 for v in normalized))
    assert dict(orbit_counts) == {'same': 31518, 'mixed': 31518}
    assert normalized_hashes == {(1, 1)+(0,)*101, (1, 2)+(0,)*101}
    # A direct CRT permutation/color comparison for representative input words.
    word_entries = 0
    for baseline in range(3):
        for p, q in [(0, 1), (1, 102), (19, 73), (37, 38)]:
            for a in range(3):
                if a == baseline:
                    continue
                for b in range(3):
                    if b == baseline:
                        continue
                    phi = [baseline + 3*((x*x+5*x+q) % 2) for x in range(103)]
                    phi[p], phi[q] = a + 3*(p % 2), b + 3*(q % 2)
                    normalized, tr = normalize_phase(phi)
                    seen = set()
                    for t in range(618):
                        old_x = (tr['alpha']*(t % 103)+tr['beta']) % 103
                        old_y = (baseline + (2-t % 6 if tr['reflect'] else t % 6)) % 6
                        old_t = next(old_x+103*j for j in range(6) if (old_x+103*j) % 6 == old_y)
                        seen.add(old_t)
                        old_color = int((old_y-phi[old_x]) % 6 >= 3) ^ int(tr['global_complement'])
                        new_color = int((t % 6-normalized[t % 103]) % 6 >= 3)
                        assert old_color == new_color
                        word_entries += 1
                    assert len(seen) == 618
    return {'status': 'ALL63036_TWO_EXCEPTION_SKELETONS_NORMALIZED',
            'same_label_skeletons': orbit_counts['same'],
            'mixed_label_skeletons': orbit_counts['mixed'],
            'arbitrary_orientation_phase_entries': phase_entries,
            'direct_CRT_color_entries': word_entries, 'seconds': time.monotonic()-begin,
            'scope': 'All two-exception ternary skeletons; phase truth table covers arbitrary orientations; no existence/exclusion verdict.'}
