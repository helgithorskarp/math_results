"""Exact all-degree-four Tammes-15 T/Q exclusion. six-tammes-1, researcher.
Standard library only. Written original-face bridges are in PROOF.md.
"""
from pathlib import Path
from collections import Counter, deque
import copy
import json
import atlas
from polynomial import T, ONE, need, bernstein
from rational import Rat

C = Rat(T)
U = Rat(ONE)
H = U + 2*C

def signp(p):
    b = bernstein(p)
    for s in (-1, 1):
        if b and all(s*x >= 0 for x in b) and any(s*x > 0 for x in b):
            return s
    return 0

def positive(r):
    need(signp(r.n)*signp(r.d) == 1, 'strict positive rational certificate')

def record(r):
    return {'n': r.n, 'd': r.d,
            'denominator_Bernstein': list(map(str, bernstein(r.d)))}

def cycle_key(f):
    need(len(f) in (3, 4) and len(set(f)) == len(f), 'simple T/Q face')
    forms = []
    for v in (tuple(f), tuple(reversed(f))):
        forms.extend(v[k:] + v[:k] for k in range(len(v)))
    return min(forms)

def complex_key(ts, qs):
    need(len(ts) == 8 and len(qs) == 9, 'all eight T and nine Q faces')
    need(all(len(f) == 3 for f in ts) and all(len(f) == 4 for f in qs), 'face arities')
    return Counter(map(cycle_key, ts)), Counter(map(cycle_key, qs))

def angle_links(cert):
    ts, qs = cert['Ts'], cert['Qs']
    tc = Counter(v for f in ts for v in f)
    need(set(v for f in ts+qs for v in f) == set(range(15)), 'all original vertex labels')
    corners = {}; links = []
    for i, f in enumerate(qs):
        links.append((2*i, 2*i+1, 'rho'))
        for k, v in enumerate(f):
            corners.setdefault(v, []).append(2*i + k%2)
    for v in range(15):
        need(tc[v] <= 2 and len(corners[v]) == 4-tc[v], 'original degree-four star')
        if tc[v] == 2:
            links.append((*corners[v], 'S'))
    return links, corners, tc

def angle_identity(cert):
    links, corners, tc = angle_links(cert)
    labels = {}
    nb = [[] for _ in range(18)]
    for a, b, kind in links:
        need(a != b, 'distinct incident angle slots')
        key = tuple(sorted((a, b)))
        need(key not in labels or labels[key] == kind, 'one involution per link')
        labels[key] = kind
        nb[a].append((b, kind)); nb[b].append((a, kind))
    walk = cert['closure_cycle']
    need(len(walk) >= 4 and walk[0] == walk[-1], 'closed original angle walk')
    word = []; original_word = []
    for a, b in zip(walk, walk[1:]):
        need(tuple(sorted((a,b))) in labels, 'actual angle-link walk')
        kind = labels[tuple(sorted((a,b)))]; original_word.append(kind)
        if word and word[-1] == kind:
            word.pop()
        else:
            word.append(kind)
    need(word == ['rho', 'S', 'rho'] and original_word[0] == 'rho', 'conjugate S fixed-point closure')
    # rho(u) = S(rho(u)) forces rho(u)=A/2=pi-alpha.
    center = walk[1]
    z = {center: U}; todo = deque([center]); paths = {center: [center]}
    while todo:
        a = todo.popleft()
        for b, kind in nb[a]:
            if kind == 'rho':
                den = C*H*z[a]; positive(den); value = U/den
            else:
                den = H*z[a]-C; positive(den); value = (U+C*z[a])/den
            positive(value)
            if b in z:
                need(not (z[b]-value).n, 'all original angle link identities')
            else:
                z[b] = value; paths[b] = paths[a]+[b]; todo.append(b)
    need(set(z) == set(range(18)), 'whole original angle-slot component')
    d = cert['one_T_vertex']; upper = cert['upper_bound_slot']
    need(d in range(15) and tc[d] == 1, 'one-T original degree-four star')
    ds = corners[d]; fixed = [a for a in ds if not (z[a]-U).n]
    need(len(fixed) == 1 and upper in ds and upper not in fixed, 'star has one pi-alpha corner and specified strict Q upper bound')
    other = next(a for a in ds if a not in fixed and a != upper)
    # The D star gives theta_upper+theta_other=pi, so their half-tangent
    # product is one. The forbidden Q upper endpoint has tan(alpha)=h/c.
    residual = H*z[upper]*z[other]-U
    difference = z[upper]-U/C
    need(not (residual+difference).n, 'D star equation equals negative Q upper-bound difference')
    positive(C*(U-2*C*C))
    need(not (residual-(U-3*C*C)/(C*(U-2*C*C))).n, 'exact reduced star residual')
    return {'closure_original_word': original_word, 'closure_reduced_word': word,
            'pi_minus_alpha_slot': center, 'propagation_paths': paths,
            'half_tangent_over_h': {i:record(z[i]) for i in range(18)},
            'one_T_star': d, 'star_angle_slots': ds,
            'pi_minus_alpha_star_slot': fixed[0], 'critical_Q_slot': upper,
            'other_star_slot': other, 'star_half_tangent_product_minus_one': record(residual),
            'critical_Q_half_tangent_over_h_minus_one_over_c': record(difference),
            'two_rational_residuals_sum_identically_zero': True,
            'conclusion': 'The necessary D-star equation forces a Q corner equal to 2alpha, contradicting its strict bound.'}

def verify(cert, cover):
    target = complex_key(cert['Ts'], cert['Qs'])
    need(len(cover['survivors']) == 2, 'both surviving orientation choices covered')
    for s in cover['survivors']:
        need(s['graph_mask'] == cert['graph_mask'], 'all surviving graph types match')
        need(complex_key(s['Ts'], s['Qs']) == target, 'full original unoriented face complex matches')
    return angle_identity(cert)

def controls(cert, cover):
    changes = [
        ('wrong_graph_type', lambda c:c.update(graph_mask=c['graph_mask']^1)),
        ('omitted_T_face', lambda c:c['Ts'].pop()),
        ('omitted_Q_face', lambda c:c['Qs'].pop()),
        ('wrong_Q_diagonal_order', lambda c:c['Qs'][0].__setitem__(slice(1,3),list(reversed(c['Qs'][0][1:3])))),
        ('reused_original_face_vertex', lambda c:c['Qs'][0].__setitem__(2,6)),
        ('open_angle_walk', lambda c:c['closure_cycle'].pop()),
        ('fake_angle_walk_edge', lambda c:c['closure_cycle'].__setitem__(2,13)),
        ('cancelled_trivial_angle_walk', lambda c:c.update(closure_cycle=[0,1,0])),
        ('wrong_one_T_star', lambda c:c.update(one_T_vertex=0)),
        ('wrong_forbidden_Q_corner', lambda c:c.update(upper_bound_slot=13)),
    ]
    result = []
    for name, mutate in changes:
        c = copy.deepcopy(cert); mutate(c)
        try:
            verify(c, cover)
        except (ValueError, KeyError) as err:
            result.append({'name':name, 'rejected':True, 'reason':str(err)})
        else:
            raise ValueError('Invalid certificate accepted: '+name)
    reflected = copy.deepcopy(cert)
    for name in ('Ts','Qs'):
        reflected[name] = [[f[0]]+list(reversed(f[1:])) for f in reflected[name]]
    need(verify(reflected, cover) == verify(cert, cover), 'global reflected face orders preserve full angle certificate')
    return result

def main():
    cert = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    cover = atlas.run(); proof = verify(cert, cover)
    out = {'agent':'six-tammes-1', 'role':'researcher',
           'proof_interval':['1/2','3/5'], 'cover':cover, 'angle_certificate':proof,
           'controls':controls(cert, cover), 'reflected_face_order_control':True,
           'conclusion':'No complete connected strictly convex simple hemispherical T/Q contact graph on fifteen distinct points with all degrees four in the stated interval.'}
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
