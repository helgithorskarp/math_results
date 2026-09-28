"""Parameterize three-term additive maps after one sum-free deletion.

The returned relations use integer coefficients without dividing by gcds,
so they also apply to target abelian groups with torsion.
"""
import json


def parameterize(n, deleted):
    if not isinstance(n, int) or n < 1:
        raise ValueError('positive integer endpoint required')
    deleted = set(deleted)
    if not deleted <= set(range(1,n+1)):
        raise ValueError('deleted positions outside the interval')
    if any(x+y in deleted for x in deleted for y in deleted):
        raise ValueError('deleted set is not sum-free, including doubling')
    remaining = set(range(1,n+1))-deleted
    if not remaining:
        return [], {}, []
    if 1 in remaining:
        a = 1
        first_gap = min(deleted) if deleted else n+1
        candidates = [v for v in remaining if v > first_gap]
    else:
        a = 2
        candidates = [v for v in remaining if v % 2]
    b = min(candidates) if candidates else None
    generators = [a] if b is None else [a,b]
    coefficient = {}
    for v in sorted(remaining):
        if v == a:
            coefficient[v] = (1,0)
        elif v == b:
            coefficient[v] = (0,1)
        elif v-a in remaining:
            r,s = coefficient[v-a]
            coefficient[v] = (r+1,s)
        elif b is not None and v-b in remaining:
            r,s = coefficient[v-b]
            coefficient[v] = (r,s+1)
        else:
            raise AssertionError('determination lemma failed')
    relations = set()
    for z in sorted(remaining):
        for x in range(1,z//2+1):
            y=z-x
            if x in remaining and y in remaining:
                relations.add(tuple(coefficient[x][i]+coefficient[y][i]
                                    -coefficient[z][i] for i in (0,1)))
    relations.discard((0,0))
    return generators, coefficient, sorted(relations)


if __name__ == '__main__':
    T={v for v in range(1,538) if v%5 in (2,3)}
    generators, coefficient, relations=parameterize(537,T)
    print(json.dumps({'n':537, 'deleted_positions':len(T),
                      'remaining_positions':len(coefficient),
                      'generators':generators, 'relations':relations},sort_keys=True))
