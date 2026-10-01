"""Discovery-only first-appearance normalization; the literal checker verifies actual permutations."""
from functools import lru_cache
from orbits import factor_levels

def powers(m):
    return tuple((p,p**len(levels)) for p,levels in factor_levels(m))

def normalize(A):
    names, answer = {}, []
    for m, a in A:
        coordinates = []
        for p, P in powers(m):
            power, encoded = 1, 0
            while power < P:
                labels = names.setdefault((p, power, a % power), {})
                digit = a // power % p
                if digit not in labels:
                    labels[digit] = len(labels)
                encoded += labels[digit] * power
                power *= p
            coordinates.append((P, encoded))
        value = sum(v * (m // P) * pow(m // P, -1, P)
                    for P, v in coordinates) % m
        answer.append((m, value))
    return tuple(answer)
