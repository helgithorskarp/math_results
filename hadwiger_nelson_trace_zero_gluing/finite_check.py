"""Exhaust the finite field lemma; independently enumerate compatible permutations."""
from itertools import product, permutations
from hashlib import sha256
import json
from coloring import fm, fb, ft, require, residue, e, Q


def main():
    # Independent representation: polynomials modulo t^2+t+1 as binary words.
    def product_mod(x, y):
        z = 0
        for i in range(2):
            if y & (1 << i):
                z ^= x << i
        if z & 4:
            z ^= 7
        return z

    require(all(product_mod(x, y) == fm(x, y) for x in range(4) for y in range(4)),
            'field multiplication representations disagree')
    cases, maps, integral, permutations_count = [], [], 0, 0
    for a in range(4):
        for b in range(4):
            if bool(a) != bool(b):
                require(a != b, 'integral branch collision')
                integral += 1
    for a, b in product(range(1, 4), repeat=2):
        def L(u, z):
            v = product_mod(product_mod(u, u), z)
            return v ^ product_mod(v, v)
        allowed = [(z, w) for z, w in product(range(4), repeat=2) if L(a, z) == L(b, w)]
        require(len(allowed) == 8, 'wrong trace kernel size')
        good = [p for p in permutations(range(4)) if all(z != p[w] for z, w in allowed)]
        require(len(good) == 4, 'wrong independent permutation census')
        permutations_count += len(good)
        lam = fm(fb(b), a)
        shifts = [t for t in range(4) if ft(fm(fb(a), t)) == 1]
        require(len(shifts) == 2, 'wrong shift count')
        for t in shifts:
            perm = tuple(fm(lam, w) ^ t for w in range(4))
            require(perm in good, 'prescribed map not independently accepted')
            maps.append([a, b, lam, t, list(perm)])
            for z, w in allowed:
                require(z != perm[w], 'nonintegral branch collision')
                cases.append([a, b, t, z, w])
        require(any(z == fm(lam, w) for z, w in allowed), 'zero-shift negative control failed')
    rejected = False
    try:
        residue(e(Q(1, 2)))
    except ValueError:
        rejected = True
    require(rejected, 'nonintegral residue was accepted')
    output = {'integral_norm_pairs': integral, 'nonzero_anchor_pairs': 9,
              'prescribed_affine_maps': len(maps), 'allowed_cross_cases': len(cases),
              'independent_good_permutations': permutations_count,
              'missing_shift_fails_all_anchor_pairs': True, 'nonintegral_input_rejected': rejected,
              'affine_maps': maps,
              'case_sha256': sha256((json.dumps(cases, separators=(',', ':'))+'\n').encode()).hexdigest(),
              'arbitrary_depth_claim_requires_PROOF_md': True}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
