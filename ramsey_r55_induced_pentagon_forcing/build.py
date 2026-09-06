"""Build a compact certificate for the seven-cycle contact lemma."""
import itertools as it
import json


def certificate():
    def distance(i, j):
        return min((i-j) % 7, (j-i) % 7)
    masks = [m for m in range(128)
             if all(distance(i, j) == 2 for i, j in it.combinations(
                 [k for k in range(7) if m >> k & 1], 2))]
    rows = []
    for s, t in it.product(masks, repeat=2):
        if any(s >> i & 1 and t >> j & 1 and distance(i, j) == 1
               for i in range(7) for j in range(7)):
            continue
        missed = [i for i in range(7) if not ((s | t) >> i & 1)]
        stable = next(q for q in it.combinations(missed, 3)
                      if all(distance(i, j) != 1 for i, j in it.combinations(q, 2)))
        rows.append({'s': s, 't': t, 'independent': list(stable)})
    return {'cycle_order': 7, 'vertex_labels': list(range(7)),
            'allowed_contacts': masks, 'contact_pairs': rows}


if __name__ == '__main__':
    print(json.dumps(certificate(), indent=2, sort_keys=True))
