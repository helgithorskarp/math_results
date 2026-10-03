"""Whole fixed-G unit/T0 component: necessary planes plus actual ray-hit witnesses."""
import geometry as g
Q, a = g.Q, g.a

def record(certificate):
    fs = g.facets()
    images = tuple(g.act(g.G, v) for v in g.V)
    R2 = a.dot(g.V[0], g.V[0])
    outside = [k for k, w in enumerate(images) if w not in g.V]
    g.require(len(outside) == 20, 'exactly twenty noncommon original source vertices')
    signs, half, plane_stream, sphere_stream = {}, {}, [], []
    q = g.raw(g.P[1])
    for k in outside:
        w = images[k]
        sphere_stream.extend(R2-a.dot(w, v) for v in g.V)
        g.require(min(sphere_stream[-60:]) > 0 and a.dot(w, w) == R2,
                  'strict sphere separation from actual convex body')
        sigma = -a.dot(w, q).sign()
        g.require(sigma in (-1, 1), 'actual forced ray sign at original feasible corner')
        signs[k] = sigma
        ds = [h-a.dot(N, w) for N, h, _ in fs]
        neg = [i for i, d in enumerate(ds) if d < 0]
        pos = [i for i, d in enumerate(ds) if d > 0]
        zero = [i for i, d in enumerate(ds) if d == 0]
        g.require(neg, 'actual facet sees every separated source point outside')
        rows = []
        for f in neg+zero:
            rows.append((tuple(-sigma*x for x in fs[f][0]), [k, 'sign', f]))
        for f in neg:
            for i in pos:
                rows.append((tuple(sigma*(ds[f]*u-ds[i]*v)
                    for u, v in zip(fs[i][0], fs[f][0])), [k, 'pair', f, i]))
        for coeff, witness in rows:
            form = g.normalize((coeff[1], coeff[0], -coeff[2]))
            g.require(form is not None, 'nonzero necessary actual ray form')
            half.setdefault(form, []).append(witness)
    g.require(len(half) == 1191, 'complete deduplicated necessary form stream')
    for w in half:
        values = [g.value(w, p) for p in g.P]
        g.require(min(values) >= 0, 'all whole-component corner ray controls')
        plane_stream.extend(values)
    for i, side in enumerate(g.SIDES):
        witness = certificate['side_witnesses'][i]
        g.require(witness in half[side], 'each exact outer side is genuinely necessary')
    seen, ray_stream, sign_stream = set(), [], []
    for row in certificate['ray_hits']:
        k, pi = row['source'], row['receiver_corner']
        g.require(k in outside and 0 <= pi < 6 and (k, pi) not in seen,
                  'unique correctly labelled original corner/source ray')
        seen.add((k, pi))
        sigma = signs[k]
        t0 = g.dec([row['t']])[0]
        weights = g.dec(row['barycentric'])
        indices = row['original_triangle']
        face = fs[row['original_facet']][2]
        g.require(len(indices) == 3 and len(set(indices)) == 3 and set(indices) <= set(face),
                  'genuine original facet triangle')
        g.require(t0 > 0 and min(weights) >= 0 and sum(weights, Q()) == 1,
                  'positive ray and actual convex triangle coefficients')
        hit = tuple(sum((weights[j]*g.V[indices[j]][i] for j in range(3)), Q())
                    for i in range(3))
        expected = a.add(images[k], a.scale(sigma*t0, g.raw(g.P[pi])))
        g.require(hit == expected, 'independent literal vertex-convex-combination ray hit')
        d = -sigma*a.dot(images[k], g.raw(g.P[pi]))
        g.require(d > 0, 'strict same ray-sign stratum on the whole closed hexagon')
        sign_stream.append(d)
        ray_stream.append([k, pi, sigma, g.enc(t0), indices, g.vec(weights), g.vec(hit)])
    g.require(seen == {(k, pi) for k in outside for pi in range(6)},
              'EVERY actual noncommon source and receiving corner, none missing')
    return {'common_original_vertices': 40, 'outside_original_sources': outside,
            'actual_spatial_facet_controls': 62*60,
            'strict_sphere_separation_controls': len(sphere_stream),
            'necessary_ray_halfspaces': len(half), 'nonnegative_ray_corner_controls': len(plane_stream),
            'actual_triangle_ray_hits': len(seen), 'strict_ray_sign_controls': len(sign_stream),
            'minimum_ray_sign_margin': g.enc(min(sign_stream)),
            'sphere_stream_sha256': g.digest(list(map(g.enc, sphere_stream))),
            'ray_halfspace_stream_sha256': g.digest(list(map(g.enc, plane_stream))),
            'literal_ray_hit_stream_sha256': g.digest(ray_stream)}
