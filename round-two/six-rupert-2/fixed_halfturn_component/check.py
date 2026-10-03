"""Complete standard-library replay; ordinary cone/width proof in PROOF.md."""
from pathlib import Path
import argparse, hashlib, json, time
import geometry as g
import ray, width

def hull(points):
    points = sorted(set(points))
    def turn(p, u, v):
        return (u[0]-p[0])*(v[1]-p[1])-(u[1]-p[1])*(v[0]-p[0])
    lo, hi = [], []
    for v in points:
        while len(lo) >= 2 and turn(lo[-2], lo[-1], v) <= 0:
            lo.pop()
        lo.append(v)
    for v in reversed(points):
        while len(hi) >= 2 and turn(hi[-2], hi[-1], v) <= 0:
            hi.pop()
        hi.append(v)
    return lo[:-1]+hi[:-1]

def controls():
    stream, hulls, companion_count = [], [], 0
    images = tuple(g.act(g.G, v) for v in g.V)
    GH = g.mm(g.G, g.H)
    g.proper(GH)
    g.require({g.act(GH, v) for v in g.V} == set(images), 'only actual RIGHT H body symmetry')
    for p in g.P:
        def screen(v):
            return (v[0]-p[0]*v[1], v[2]+p[1]*v[1])
        receiver, source = hull([screen(v) for v in g.V]), hull([screen(v) for v in images])
        for v in images:
            q = screen(v)
            for u, w in zip(receiver, receiver[1:]+receiver[:1]):
                value = (w[0]-u[0])*(q[1]-u[1])-(w[1]-u[1])*(q[0]-u[0])
                g.require(value >= 0, 'independent actual projected-hull corner containment')
                stream.append(value)
        hulls.append({'receiver_corners': len(receiver), 'source_corners': len(source),
                      'equal_shadows': receiver == source})
        r = g.raw(p)
        r2 = g.a.dot(r, r)
        Mn = tuple(tuple(g.I[i][j]-2*r[i]*r[j]/r2 for j in range(3)) for i in range(3))
        for pose in (g.G, GH):
            C = g.mm(g.mm(Mn, pose), g.MX)
            g.proper(C)
            for v in g.V:
                g.require(g.projection(g.act(C, v), p) ==
                          g.projection(g.act(pose, g.act(g.MX, v)), p),
                          'actual pointwise proper receiving-plane companion identity')
                companion_count += 1
    g.require(hulls[1]['receiver_corners'] == 13 and hulls[1]['source_corners'] == 12 and
              not hulls[1]['equal_shadows'], 'original extra corner retains proper shadow containment')
    return {'independent_original_projection_controls': len(stream),
            'independent_original_projection_stream_sha256': g.digest(list(map(g.enc, stream))),
            'corner_hulls': hulls, 'actual_companion_point_identities': companion_count}

def record(certificate):
    return {'agent': 'six-rupert-2', 'role': 'researcher',
        'scope': 'complete unit-scale/T0 connected receiving component containing q for fixed original G in raw_y=1 chart; EVERY physical translation and lambda>=1 classified for G, GH and proper Cn companions on whole closed hexagon ONLY',
        'geometry': g.record(), 'ray': ray.record(certificate),
        'width': width.record(certificate), 'author_controls': controls(),
        'global_J74_Rupert_status': 'OPEN', 'arbitrary_source_rotations_classified': False,
        'formalized': False, 'independent_review': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    certificate = json.loads((g.HERE/'certificate.json').read_text())
    result = record(certificate)
    if args.compare:
        g.require(result == json.loads(args.compare.read_text()), 'ENTIRE mathematical output matches')
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'complete': True, 'mathematical_sha256': g.digest(result),
        'wall_seconds': time.monotonic()-started,
        'exact_ray_corner_controls': result['ray']['nonnegative_ray_corner_controls'],
        'exact_width_controls': result['width']['actual_original_support_controls'],
        'independent_projection_controls': result['author_controls']['independent_original_projection_controls'],
        'receiving_leaves': result['width']['closed_receiving_leaves']}, indent=2))
