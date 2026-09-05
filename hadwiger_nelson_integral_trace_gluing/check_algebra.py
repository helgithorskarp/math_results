"""Symbolic perturbation identity and exhaustive local unit-trace lifting audit."""
from arithmetic import *
from itertools import product
import json


def symbolic():
    mod = load('sparse_polynomials', 'hadwiger_nelson_cross_six_cycle/identities.py',
               '2c0b7986b5da71c06f5d152a4c83c0c6196c2cdac3942cab6243f5da0541e370')
    A, B, D, E, z, w, r, s, t, v, h = mod.variables('A B D E z w r s t v h')
    def plus(x, y): return tuple(a+b for a, b in zip(x, y))
    def minus(x, y): return tuple(a-b for a, b in zip(x, y))
    def times(x, y):
        a, b = x; c, d = y
        return a*c-b*d, a*d+b*c-b*d
    def conj(x): return x[0]-x[1], -x[1]
    def normp(x): return x[0]*x[0]-x[0]*x[1]+x[1]*x[1]
    def scalar(x, a): return tuple(a*b for b in x)
    def tracep(x): return 2*x[0]-x[1], 0
    def q(x, y): return minus((normp(x)+normp(y), 0), times((t, v), times(conj(x), y)))
    X, Y, Z, W = (A, B), (D, E), (z, w), (r, s)
    linear = minus(plus(tracep(times(conj(X), Z)), tracep(times(conj(Y), W))),
                   times((t, v), plus(times(conj(X), W), times(conj(Z), Y))))
    left = minus(q(plus(X, scalar(Z, h)), plus(Y, scalar(W, h))), q(X, Y))
    right = plus(scalar(linear, h), scalar(q(Z, W), h*h))
    for i in range(2):
        require(not (mod.P(left[i])-mod.P(right[i])).terms, 'perturbation identity failed')
    return {'coefficient_identities': 2, 'left_term_counts': [len(mod.P(x).terms) for x in left]}


def local_audit():
    # Independent quotient multiplication uses evaluation/reduction of degree-2 polynomials.
    def product_poly(x, y, m):
        a, b = x; c, d = y
        coefficients = [a*c, a*d+b*c, b*d]
        return (coefficients[0]-coefficients[2]) % m, (coefficients[1]-coefficients[2]) % m
    M = 16; all_points = list(product(range(M), repeat=2)); records = []
    for t in all_points:
        nt = (t[0]*t[0]-t[0]*t[1]+t[1]*t[1]) % M
        if not nt % 2:
            continue
        invnorm = pow(nt, -1, M)
        inverse_bar = tuple(invnorm*a % M for a in t)
        J = product_poly(t, inverse_bar, M)
        brute = []
        for x in all_points:
            xx, tx = product_poly(x, x, M), product_poly(t, x, M)
            if all((xx[i]-tx[i]+J[i]) % M == 0 for i in range(2)):
                brute.append(x)
        predicted = [rm(t, lift_w(invnorm, 4, branch), M) for branch in (0, 1)]
        require(set(brute) == set(predicted) and len(brute) == 2, 'complete root sets disagree')
        for x in predicted:
            require(rn(x, M) == 1, 'root norm differs')
        require(tuple((predicted[0][i]+predicted[1][i]) % M for i in range(2)) == t,
                'root trace differs')
        records.append([list(t), [list(x) for x in sorted(brute)]])
    require(len(records) == 192, 'wrong unit trace census')
    deep = []
    for constant in (1, 3, 5, 9, 17, 31, 65, 127, 255):
        previous = None
        for bits in range(1, 33):
            m = 1 << bits
            w, other = lift_w(constant, bits, 0), lift_w(constant, bits, 1)
            f = rm(w, w, m)
            require(((f[0]-w[0]+constant) % m, (f[1]-w[1]) % m) == (0, 0), 'lift polynomial failure')
            require(rb(w, m) == other == ((1-w[0]) % m, -w[1] % m), 'conjugate branch failure')
            if previous is not None:
                require(tuple(a % (m//2) for a in w) == previous, 'lift is not compatible')
            previous = w
        deep.append([constant, list(w)])
    for T in (e(0), e(Q(4, 3)), e(Q(1, 2))):
        rejected = False
        try: unit_root(T, 4)
        except ValueError: rejected = True
        require(rejected, 'invalid unit-trace input accepted')
    norm_one = [x for x in product(range(4), repeat=2) if rn(x, 4) == 1]
    trace_residues = sorted({(2*x[0]-x[1]) % 4 for x in norm_one})
    require(len(norm_one) == 6 and trace_residues == [1, 2, 3], 'norm-one trace obstruction failed')
    rejected = False
    try: glue_even([ONE], [e(Q(1, 3))], e(Q(1, 3)), [(0, 0)])
    except ValueError: rejected = True
    require(rejected, 'even-trace recipe accepted a unit trace')
    return {'norm_one_mod4_elements': len(norm_one), 'norm_one_mod4_trace_residues': trace_residues,
            'unit_trace_rejected_by_even_recipe': rejected, 'unit_traces_mod16': len(records), 'candidate_roots_tested': len(records)*len(all_points),
            'exact_roots_matched': 2*len(records), 'mod16_root_sha256': sha256((json.dumps(records,separators=(',',':'))+'\n').encode()).hexdigest(),
            'compatible_lifts': len(deep), 'precision_bits': 32, 'lift_endpoints': deep,
            'nonunit_and_nonintegral_traces_rejected': True}


def main():
    print(json.dumps({'symbolic': symbolic(), 'local_audit': local_audit(),
                      'uniform_claim_requires_PROOF_md': True}, indent=2))


if __name__ == '__main__': main()
