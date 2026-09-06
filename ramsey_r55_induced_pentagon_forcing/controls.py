"""Exact identity, component, extractor, and rejection controls."""
import copy
import hashlib
import itertools as it
import json
import math
import random
from collections import Counter
from pathlib import Path
from check import check
from extract import extract
from verify import verify


def fixture(mode='pentagon', n=43):
    e = {(0, 1)} | {(v, w) for v in (0, 1) for w in range(2, 12)}
    if mode == 'triangle':
        e |= {(2, 3), (2, 4), (3, 4)}
    elif mode == 'pentagon':
        # Petersen graph on2..11: outerC5, inner pentagram and matching.
        for i in range(5):
            e.add(tuple(sorted((2+i, 2+(i+1) % 5))))
            e.add(tuple(sorted((7+i, 7+(i+2) % 5))))
            e.add((2+i, 7+i))
    elif mode != 'independent':
        raise ValueError('fixture mode')
    return {'n': n, 'edges': [list(p) for p in sorted(e)]}


def main():
    identity_graphs = 0
    for n in range(1, 7):
        pairs = list(it.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            red = {p for i, p in enumerate(pairs) if mask >> i & 1}
            degrees = [sum(v in e for e in red) for v in range(n)]
            mono = 0
            for q in it.combinations(range(n), 3):
                colors = [e in red for e in it.combinations(q, 2)]
                mono += all(colors) or not any(colors)
            if 2*mono != 2*math.comb(n, 3) - sum(d*(n-1-d) for d in degrees):
                raise ValueError('mixed-triangle identity')
            book_sum = 0
            for u, v in pairs:
                color = (u, v) in red
                book_sum += sum(((min(u,w), max(u,w)) in red) == color and
                                ((min(v,w), max(v,w)) in red) == color
                                for w in range(n) if w not in (u,v))
            if book_sum != 3*mono:
                raise ValueError('book identity')
            identity_graphs += 1
    # Complete isomorphism-type generation for max-degree2 graphs with noC3,C5.
    component_counts = {}
    for n in (7, 8):
        types = [('path', k) for k in range(1, n+1)] + [('cycle', k) for k in range(4, n+1) if k != 5]
        types.sort()
        def compositions(left, start=0, current=()):
            if left == 0:
                yield current
            for j in range(start, len(types)):
                kind, size = types[j]
                if size <= left:
                    yield from compositions(left-size, j, current+(types[j],))
        count = 0
        for parts in compositions(n):
            red, offset = set(), 0
            for kind, size in parts:
                red |= {(offset+i, offset+i+1) for i in range(size-1)}
                if kind == 'cycle':
                    red.add((offset, offset+size-1))
                offset += size
            has_i4 = any(all(e not in red for e in it.combinations(q, 2)) for q in it.combinations(range(n), 4))
            if not has_i4 and not (n == 7 and parts == (('cycle', 7),)):
                raise ValueError(('component lemma', n, parts))
            count += 1
        component_counts[str(n)] = count
    rng = random.Random(55050942)
    graphs = []
    for n in (42, 43, 44):
        for mode in ('triangle', 'independent', 'pentagon'):
            data = fixture(mode, n)
            for complement in (False, True):
                pairs = set(map(tuple, data['edges']))
                if complement:
                    pairs = set(it.combinations(range(n), 2)) - pairs
                graphs.append({'n':n, 'edges':[list(e) for e in sorted(pairs)]})
                labels = list(range(n)); rng.shuffle(labels)
                graphs.append({'n':n, 'edges':[list(e) for e in sorted(tuple(sorted((labels[u],labels[v]))) for u,v in pairs)]})
        for numerator in (1, 3, 5, 7, 9):
            for _ in range(4):
                graphs.append({'n':n, 'edges':[list(e) for e in it.combinations(range(n), 2) if rng.randrange(10) < numerator]})
    outcomes, stream = Counter(), hashlib.sha256()
    for data in graphs:
        cert = extract(data); verify(data, cert)
        outcomes[cert['kind'] + ':' + cert.get('color', '')] += 1
        stream.update((json.dumps(cert, sort_keys=True)+'\n').encode())
    # Fixtures before scrambling exercise all three mathematical extraction branches.
    branches = [extract(fixture(mode))['kind'] for mode in ('triangle', 'independent', 'pentagon')]
    if branches != ['monochromatic5', 'monochromatic5', 'induced_C5']:
        raise ValueError('fixture branch coverage')
    root = Path(__file__).resolve().parent
    cert = json.loads((root/'certificate.json').read_text())
    bad_certificates = {}
    bad = copy.deepcopy(cert); bad['contact_pairs'].pop(); bad_certificates['missing_pair'] = bad
    bad = copy.deepcopy(cert); bad['allowed_contacts'].pop(); bad_certificates['missing_contact'] = bad
    bad = copy.deepcopy(cert); bad['contact_pairs'][0]['independent'] = [0,1,2]; bad_certificates['wrong_stable_set'] = bad
    bad = copy.deepcopy(cert); bad['contact_pairs'].append(bad['contact_pairs'][0]); bad_certificates['duplicate_pair'] = bad
    rejected_kernel = []
    for name, bad in bad_certificates.items():
        try: check(bad)
        except ValueError: rejected_kernel.append(name)
        else: raise ValueError(('kernel accepted mutation', name))
    data = fixture(); good = extract(data)
    bad_graphs = [dict(data, n=41), dict(data, edges=data['edges']+[data['edges'][0]]),
                  dict(data, edges=[[0,0]]), dict(data, edges=[[1,0]]), dict(data, edges=[[0,43]])]
    for bad in bad_graphs:
        try: extract(bad)
        except ValueError: pass
        else: raise ValueError('accepted malformed graph')
    bad_fives = [dict(good, vertices=[0,0,1,2,3]), dict(good, vertices=[0,1,2,3,43]),
                 dict(good, vertices=[0,1,2,3,4]), dict(good, kind='monochromatic5',color='red'),
                 dict(good, kind='unsupported')]
    for bad in bad_fives:
        try: verify(data, bad)
        except ValueError: pass
        else: raise ValueError('accepted invalid five-set certificate')
    return {'status':'ALL_CONTROLS_PASSED', 'identity_graphs':identity_graphs,
            'max_degree2_component_types':component_counts, 'global_graphs':len(graphs),
            'global_outcomes':dict(sorted(outcomes.items())), 'global_certificate_stream_sha256':stream.hexdigest(),
            'kernel_mutations_rejected':rejected_kernel, 'malformed_graphs_rejected':len(bad_graphs),
            'invalid_five_certificates_rejected':len(bad_fives)}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
