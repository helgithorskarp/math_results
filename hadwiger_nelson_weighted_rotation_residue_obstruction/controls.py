"""Deliberate witness corruption checks, independent of solver discovery."""
from itertools import product, combinations
import json
from exact import (HERE, ONE, F, points, norm, sub, scale, quotient_colour,
                   quotient_directions, require)

labels = list(product(range(4),repeat=4))
index = {z:i for i,z in enumerate(labels)}
edges = set()
for i,z in enumerate(labels):
    for d in quotient_directions():
        j = index[tuple((x+y)%4 for x,y in zip(z,d))]
        edges.add(tuple(sorted((i,j))))
colours = [quotient_colour(z) for z in labels]
for v in range(256):
    a,b = next(e for e in edges if v in e)
    other = b if a == v else a
    bad = colours[:]
    bad[v] = bad[other]
    require(any(bad[a] == bad[b] for a,b in edges), 'quotient corruption survived')
cert = json.loads((HERE/'auxiliary_certificate.json').read_text())
L = points()
P = [L[i] for i in cert['source_indices']]
edges = [(a,b) for a,b in combinations(range(114),2)
         if norm(sub(P[a],P[b])) in (ONE,scale(ONE,F(4,3)))]
for v,s in enumerate(cert['deletion_four_colourings']):
    a,b = next(e for e in edges if v not in e)
    bad = list(map(int,s))
    bad[a] = bad[b]
    require(any(bad[a] == bad[b] for a,b in edges if v not in (a,b)),
            'auxiliary deletion corruption survived')
print(json.dumps({'quotient_corruptions_rejected':256,
                  'auxiliary_deletion_corruptions_rejected':114},sort_keys=True))
