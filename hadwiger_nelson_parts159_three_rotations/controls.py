"""Second arithmetic representation and deliberate certificate corruptions."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import geometry as G
import verify as V

def signed(e):
    a, b, c, d = e
    return a, c, d, -b

def times(x, y, d):
    """Quotient basis 1,t,r,tr,q,tq,rq,trq; t²=-3,r²=-11,q²=A-Btr."""
    out = [F(0)]*8
    for i, a in enumerate(x):
        if not a:
            continue
        for j, b in enumerate(y):
            if not b:
                continue
            k = i^j
            value = a*b*(-3 if i&j&1 else 1)*(-11 if i&j&2 else 1)
            if i&j&4:
                out[k] += value*d[0]
                factor = (-3 if k&1 else 1)*(-11 if k&2 else 1)
                out[k^3] -= value*d[1]*factor
            else:
                out[k] += value
    return tuple(out)

def conjugate(x):
    return tuple(-a if (i&3).bit_count()%2 else a for i, a in enumerate(x))

def norm(x, d):
    return times(x, conjugate(x), d)

def run():
    data = G.build()
    one = (F(1),)+(F(0),)*7
    A = [signed(a)+(F(0),)*4 for a in data['A']]
    positive, negative, root_checks = 0, 0, 0
    chosen_fields = set()
    for gi, fi, (a, b) in data['roots']:
        d = data['fields'][fi]
        z = signed(a)+signed(b)
        G.require(norm(z, d) == one, 'independent root norm')
        root_checks += 1
        es = data['groups'][gi][1]
        transformed = {}
        for i, j in es:
            if j not in transformed:
                transformed[j] = times(z, A[j], d)
            delta = tuple(x-y for x, y in zip(A[i], transformed[j]))
            G.require(norm(delta, d) == one, 'independent cross-edge norm')
            positive += 1
        if fi not in chosen_fields:
            chosen_fields.add(fi)
            edge_set = set(es)
            # Deterministic nonedges span the point file, rather than a rounded picture.
            for i in range(1, 159, 11):
                for j in range(1, 159, 13):
                    delta = tuple(x-y for x, y in zip(A[i], times(z, A[j], d)))
                    G.require((norm(delta, d) == one) == ((i, j) in edge_set),
                              'independent contact/noncontact')
                    negative += (i, j) not in edge_set
    cert, words, ext, cycles = V.load_certificate(G.HERE/'certificate.json', data['internal'])
    fixed = tuple(G.K.color(a) for a in data['A'])
    corrupt = 0
    for gi, wi in ext.items():
        es = data['groups'][gi][1]
        i, j = es[0]
        bad = list(words[wi]); bad[j] = fixed[i]
        G.require(not V.bridge_ok(fixed, bad, es), 'corrupt extension accepted')
        corrupt += 1
    data['group_map'] = dict(data['groups'])
    for (i, j), indices in cycles.items():
        gi, fi, u = data['roots'][i]
        gj, fj, v = data['roots'][j]
        es, same, kind = G.relative_contacts(data, u, v, data['fields'][fi])
        ca, cb, cc = [words[k] for k in indices]
        a, b = es[0]; bad = list(cc); bad[b] = cb[a]
        G.require(not V.bridge_ok(cb, bad, es, same), 'corrupt cycle accepted')
        corrupt += 1
    # Check sqrt_f's iff test agrees with the prior independent Boolean implementation.
    squares = 0
    for a, b in product(range(-12, 13), repeat=2):
        x = F(a, 7), F(b, 9)
        G.require((G.sqrt_f(x) is not None) == G.C.real_square(x), 'square criterion disagreement')
        squares += 1
    return {'independent_rotation_norms': root_checks,
            'independent_cross_edges': positive,
            'independent_sampled_nonedges': negative,
            'quadratic_fields_sampled': len(chosen_fields),
            'corrupt_colour_witnesses_rejected': corrupt,
            'square_criterion_comparisons': squares}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
