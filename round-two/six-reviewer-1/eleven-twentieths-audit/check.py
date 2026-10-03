"""Independent complete LEMMA10101 finite audit, from its exposed proof inputs.

Dense power coefficients are compared with separately generated complete
Bernstein vectors and integrals. Native producer/EXPECTED are never imported.
"""
import argparse
import json
from pathlib import Path
from arithmetic import (F, require, add, scale, mul, power, integrate, pad,
                        bproduct, bpower, elevate, btopower, bintegrate,
                        kernel_bernstein, ceiling, encode)


def newton_constants():
    c = [F(1), F(0)]
    for l in range(2, 9):
        c.append(sum(c[:l-1], F(0))/l)
    # Independent cycle partitions: the coefficient of exp(sum_{k>=2} x^k/k).
    from math import factorial
    def partition(l, k=2):
        if k > l:
            return F(1) if l == 0 else F(0)
        return sum((partition(l-k*j, k+1) / (k**j * factorial(j))
                    for j in range(l//k+1)), F(0))
    require(c == [F(1), F(0)] + [partition(l) for l in range(2, 9)],
            'all seven Newton bounds')
    return c


def polar_cells(damage=None):
    h, c, b = F(11, 20), F(7, 10), F(279, 400)
    tmax = 56*F(11, 31)**2
    result = []
    for k in range(57):
        L, U = F(k, 8), min(F(k+1, 8), tmax)
        require(L <= U and (k == 0 or L == result[-1]['U']), 'closed polar adjacency')
        P = max(F(0), (3-U)/2)
        d = ceiling(7*U/8, 256)
        if damage == 'ceiling' and k == 0:
            d -= F(1, 256)
        require(d*d >= 7*U/8 and d >= 0, 'polar deviation payment')
        MB, MC = h+c, h+F(3, 4)*(1+d)
        alpha, nu = c/MB, F(3, 4)*(1+d)/MC
        require(0 <= alpha < 1 and 0 <= nu < 1, 'reciprocal series domain')
        g1 = [sum((alpha**j * nu**(n-j) for j in range(n+1)), F(0))/(MB*MC)
              for n in range(5)]
        g2 = [(n+1)*nu**n/MC**2 for n in range(5)]
        if damage == 'reciprocal' and k == 0:
            g2[0] *= 2
        require(g2[0] == 1/MC**2, 'reciprocal coefficient payment')
        z = [F(1), F(-1)]
        K = [F(0)]
        terms = []
        for n in range(5):
            radial, phase = b*b*L*g1[n]/2, F(3, 8)*P*g2[n]
            require(radial >= 0 and phase >= 0, 'nonnegative reciprocal kernel')
            K = add(K, scale([F(0), F(0)] + power(z, n), radial))
            K = add(K, scale([F(0)] + power(z, n), phase))
            terms += [(2, n, radial), (1, n, phase)]
        bracket = add(add([F(1)], scale(K, -1)), scale(mul(K, K), F(1, 2)))
        full = pad(mul(power([h, c], 8), bracket), 20)
        kb = kernel_bernstein(terms, 6)
        require(pad(K, 6) == btopower(kb), 'full polar loss coefficients')
        bracket_b = [F(1)-v+w/2 for v, w in zip(elevate(kb, 12), bproduct(kb, kb))]
        full_b = bproduct(bpower([h, h+c], 8), bracket_b)
        require(full == btopower(full_b), 'all 21 polar coefficients')
        value = integrate(full)
        require(value == bintegrate(full_b), 'whole polar rational integral')
        if damage == 'polar-term' and k == 10:
            full[-1] += 1
        require(full == btopower(full_b), 'polar highest coefficient')
        require(value < F(999, 1000), 'individual polar strict bound')
        result.append(dict(k=k, L=L, U=U, P=P, d=d, MB=MB, MC=MC,
                           alpha=alpha, nu=nu, G1=g1, G2=g2, K=pad(K, 6),
                           coefficients=full, bernstein=full_b, integral=value))
    require(result[0]['L'] == 0 and result[-1]['U'] == tmax, 'whole polar domain')
    return result


def closed_plan(plan, damage=None):
    root = tuple(map(F, plan['root']))
    require(root == (F(1, 2), F(11, 20), F(61, 80), F(1), F(0), F(3, 8)),
            'origin root equals complete stated domain')
    leaves = list(plan['leaves'])
    splits = dict(plan['splits'])
    if damage == 'missing-leaf':
        leaves.pop()
    if damage == 'split-axis':
        splits[''] = 3
    require(len(leaves) == len(set(leaves)) == 48 and len(splits) == 47,
            'complete node census')
    leafset, internal = set(leaves), set(splits)
    prefixes = {p[:i] for p in leaves for i in range(len(p))}
    require(prefixes == internal and not leafset & internal,
            'exact all proper prefixes, prefix-free leaves')
    require(all(set(p) <= {'0', '1'} for p in leafset | internal), 'binary paths')
    require(sum((F(1, 2**len(p)) for p in leaves), F(0)) == 1,
            'complete prefix-code Kraft identity')
    require(all(p+'0' in leafset | internal and p+'1' in leafset | internal
                for p in internal), 'both closed children at every split')
    require(all(type(axis) is int and axis in (0, 1, 2) for axis in splits.values()),
            'legal axes')
    # Derive each box from its entire leaf path, not a producer's recursive walk.
    boxes = {'': root}
    for path in sorted(leafset | internal, key=lambda p: (len(p), p)):
        if not path:
            continue
        parent, bit = path[:-1], int(path[-1])
        box = list(boxes[parent]); axis = splits[parent]*2
        midpoint = (box[axis]+box[axis+1])/2
        box[axis + (1-bit)] = midpoint
        require(box[axis] < box[axis+1], 'nondegenerate closed child')
        boxes[path] = tuple(box)
    for p, axis in splits.items():
        a, b, r = boxes[p+'0'], boxes[p+'1'], boxes[p]
        i = 2*axis
        require(a[i] == r[i] and a[i+1] == b[i] and b[i+1] == r[i+1] and
                all(a[j] == b[j] == r[j] for j in range(6) if j not in (i, i+1)),
                'literal closed midpoint union, including all shared boundaries')
    return root, [(p, boxes[p]) for p in sorted(leaves)], [
        dict(path=p, axis=splits[p], parent=boxes[p], lower=boxes[p+'0'], upper=boxes[p+'1'])
        for p in sorted(splits)]


def origin_leaves(plan, damage=None):
    root, leaves, topology = closed_plan(plan, damage)
    c = newton_constants()
    result = []
    for path, box in leaves:
        A, B, U, V, W, X = box
        s = min(F(1), V*V+X)
        S = 3-8*((1-V)**2+W)
        beta = [F(1), -2*A*U, A*A*s]
        beta1 = sum(beta)
        require(0 < A <= B <= F(11, 20) and F(61, 80) <= U <= V <= 1 and
                0 <= W <= X <= F(3, 8), 'whole box domain')
        require(s >= U*U and S >= 0 and U > A*s and 0 < beta1 < 1 and 1-A*U > 0,
                'origin sign, mean, variance, monotonicity budgets')
        ds, db, dS = ceiling(s, 1024), ceiling(beta1, 1024), ceiling(S, 1024)
        q2 = A*A*(s-U*U)/(2*(1-A*U))
        Q = [F(1), -A*U, q2]
        qb = [F(1), 1-A*U/2, 1-A*U+q2]
        bb = [F(1), 1-A*U, beta1]
        require(btopower(bb) == beta and btopower(qb) == Q and
                min(bb) > 0 and min(qb) > 0, 'positive entire root envelopes')
        numerator = 1-db*beta1**4
        require(numerator > 0, 'positive diagonal numerator')
        D = numerator/(B*ds)
        terms = []
        for l in range(2, 9):
            H = power(beta, (8-l)//2)
            hb = bpower(bb, (8-l)//2)
            if l % 2:
                H = mul(H, Q); hb = bproduct(hb, qb)
            coeff = [F(0)]*l+H
            cb = bproduct([F(0)]*l+[F(1)], hb)
            require(coeff == btopower(cb), 'all origin polynomial coefficients')
            I = integrate(coeff)
            require(I == bintegrate(cb), 'all origin rational integrals')
            weight = 9*B**l*c[l]*S**(l//2)*(dS if l%2 else 1)
            require(weight >= 0, 'complete centered order payment')
            if damage == 'origin-integral' and path == leaves[0][0] and l == 8:
                I -= F(1, 1000000)
            require(I == bintegrate(cb), 'eighth origin term included')
            terms.append(dict(l=l, Newton=c[l], H=H, coefficients=coeff,
                              bernstein=cb, integral=I, weight=weight, term=weight*I))
        R = sum((t['term'] for t in terms), F(0))
        value = D-R
        if damage == 'origin-threshold' and path == leaves[0][0]:
            value = F(257, 256)
        require(len(terms) == 7 and [t['l'] for t in terms] == list(range(2, 9)),
                'every centered order2 through8')
        require(value > F(257, 256), 'individual strict origin margin')
        result.append(dict(path=path, box=box, s=s, S=S, beta=beta, beta1=beta1,
                           Q=Q, ds=ds, db=db, dS=dS, D=D, terms=terms, R=R, bound=value))
    return root, topology, result


def run(damage=None):
    plan = json.loads(Path(__file__).with_name('PLAN.json').read_text())
    polar = polar_cells(damage)
    root, topology, origin = origin_leaves(plan, damage)
    small = power([F(11, 20), F(133, 200)], 8)
    sb = bpower([F(11, 20), F(243, 200)], 8)
    require(small == btopower(sb) and integrate(small) == bintegrate(sb) < 1,
            'full mass-floor polynomial')
    pmax = max(polar, key=lambda p: p['integral'])
    omin = min(origin, key=lambda p: p['bound'])
    require(pmax['integral'] < F(499, 500) and omin['bound'] > F(10047, 10000),
            'independently sharpened reported finite margins')
    return encode(dict(agent='six-reviewer-1', role='independent mathematical reviewer',
                       target='10101/0', blind=False, native_imports=False,
                       mass_floor=dict(coefficients=small, bernstein=sb, integral=integrate(small)),
                       polar=polar, origin_root=root, all_closed_splits=topology, origin=origin,
                       polar_max=dict(k=pmax['k'], value=pmax['integral']),
                       origin_min=dict(path=omin['path'], value=omin['bound']),
                       all57_polar_and48_origin_full_vectors_integrals_checked=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--damage', choices=['ceiling', 'reciprocal', 'polar-term', 'missing-leaf',
                                           'split-axis', 'origin-integral', 'origin-threshold'])
    args = parser.parse_args()
    print(json.dumps(run(args.damage), sort_keys=True, separators=(',', ':')))
