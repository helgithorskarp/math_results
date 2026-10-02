"""Independent finite controls for the proved arbitrary-prime orbit formula."""
import json
from collections import Counter


def count(prime):
    states = {(t, a, b) for t in range(2, prime) for a in (0, 1) for b in (0, 1)}
    components = []
    while states:
        seed = min(states)
        orbit, frontier = {seed}, [seed]
        while frontier:
            t, a, b = frontier.pop()
            # Two generator actions, with every modular operation explicit.
            images = ((1 - t) % prime, a, a ^ b), (pow(1 - t, -1, prime), a ^ b, a)
            for z in images:
                if z not in orbit:
                    orbit.add(z)
                    frontier.append(z)
        if not orbit <= states:
            raise ValueError('overlapping orbit')
        states -= orbit
        components.append(sorted(orbit))
    roots = [t for t in range(prime) if (t * t - t + 1) % prime == 0]
    numerator = 4 * (prime - 2) + 6 + 2 * len(roots)
    if numerator != 6 * len(components):
        raise ValueError('Burnside control')
    expected = 2 if prime == 3 else (2 * prime + (1 if prime % 3 == 1 else -1)) // 3
    if len(components) != expected:
        raise ValueError('general formula control')
    return {'prime': prime, 'states': 4 * (prime - 2), 'orbits': len(components),
            'quadratic_roots': roots, 'size_histogram': dict(sorted(Counter(map(len, components)).items()))}


if __name__ == '__main__':
    data = [count(p) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 103)]
    print(json.dumps({'status': 'GENERAL_ORBIT_FORMULA_CONTROLS_PASS', 'finite_controls_only': True,
                      'controls': data}, sort_keys=True))
