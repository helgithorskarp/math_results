# A prime-index Fourier criterion for Ehrhart period

Let `P={x in R^d:A x<=b}` be a bounded full-dimensional rational
polytope with a fixed integral actual-facet description, and suppose `pP`
is a lattice polytope for a prime `p`.  Among the nonempty faces whose
affine spans miss `Z^d`, let `g` be the minimum codimension and `M` the
faces of codimension `g`.  Assume that every `F` in `M` lies in exactly
`g` facets and that

```text
[Z^g : A_F Z^d] = p.
```

The active image is the kernel of a character `epsilon_F` modulo `p`.
Minimality forces every coordinate of this character to be nonzero.  If
`c_F=epsilon_F b_F` and

```text
eta_F = c_F^(-1) epsilon_F in (F_p^*)^g,
```

then `eta_F` is independent of the choice of `epsilon_F`, up to the order
of the containing facets.

Write the Ehrhart quasipolynomial as

```text
L_P(n)=sum_j q_j(n) n^j
```

with every coefficient function represented on `Z/pZ`, put
`zeta=exp(2 pi i/p)`, and use the Fourier convention

```text
qhat_j(h) = (1/p) sum_(r mod p) q_j(r) zeta^(h r).
```

The main theorem gives, for `k=d-g` and every `h=1,...,p-1`,

```text
qhat_k(h)
  = (1/p) sum_(F in M) vol_k(F)
      product_(j=1)^g (1-zeta^(h eta_(F,j)))^(-1).       (1)
```

Consequently `P` has exact Ehrhart quasiperiod `p` whenever one of these
cyclotomic sums is nonzero.  In particular, exact period follows if `M`
has one face, if all normalized character multisets are equal, or if
`g=1`.  At `p=2`, formula (1) is the positive parity coefficient from the
[preceding index-two theorem](../bimodular_ehrhart_period/).

Odd-prime positivity genuinely needs an alignment hypothesis at the
character level: for `p=3`, `g=3`, the profiles `(1,1,1)` and `(2,2,2)`
with equal weights cancel in every nonzero Fourier mode.  This is an
algebraic cancellation in the criterion, not a claim that those two
profiles and weights are realized by a period-collapsing polytope.

[PROOF.md](PROOF.md) supplies the local Euler--Maclaurin argument and
states the scope precisely.  The result is a sufficient criterion, not a
classification of all prime-denominator polytopes.

## Reproduce

Using Python 3.11 or newer and only the standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The verifier performs exact arithmetic in cyclotomic fields.  It compares
formula (1) with direct lattice counts for 48 prime-denominator simplex
products, using 204 residuewise rational interpolations and 204 unused
count values.  It separately checks 198 finite mod-`p` active-image
systems through 5,592 direct residue-membership tests, and verifies the
stated cancellation identity.  The two routes share no Ehrhart coefficient
formula.  The computation checks the normalization and signs;
the universal theorem rests on the written proof and the explicitly cited
Berline--Vergne formula.

This extension has not been formally verified or independently reviewed.
The literature boundary in [SOURCES.md](SOURCES.md) is based on bounded
primary-source searches, not a claim that no equivalent result exists.
