# Positive-inertia descent at cardinality `2p+1`

This directory proves a structural extension of the prime-descent method for
finite cyclic Fuglede problems.

## Theorem

Let `p >= 5` be prime, let `gcd(n,p)=1`, and identify

```text
Z/(np)Z = Z/nZ x Z/pZ.
```

If `(A,Lambda)` is a spectral pair with
`|A|=|Lambda|=2p+1`, then at least one member has **p-descent**:

```text
Phi_(dp) | m_E  ==>  Phi_d | m_E             for every d | n.
```

Both projections to `Z/nZ` are injective, and the projected sets form a
spectral pair.  Consequently, if every `(2p+1)`-point spectral subset of
`Z/nZ` tiles, then every `(2p+1)`-point spectral subset of `Z/(np)Z` tiles.

For `n=210` and `p=11`, the known four-prime theorem downstairs implies that
there is no 23-point spectral subset of `Z/2310Z`.

The new bridge is an inertia obstruction.  If both descents fail, the earlier
singleton-level Gram lemma leaves only two possible level profiles:

```text
(p+2,1^(p-1))  or  (3,2^(p-1)).
```

The first profile cannot occur on both sides by the earlier block-Gram
obstruction.  For the second profile, subtract the Gram matrices belonging to
the three-point and a two-point level.  Cross-level Fourier equality makes the
difference block diagonal over the `p` opposite levels.  Every block has
positive trace, so the difference has at least `p` positive eigenvalues.  But
it is `V-W`, where `V` is positive semidefinite of rank at most three and `W`
is positive semidefinite, so it has at most three positive eigenvalues.  This
contradicts `p >= 5`.

The full argument, including all imported lemmas and the `p=3` boundary, is in
[PROOF.md](PROOF.md).

## Reproduction

The theorem is a written exact proof.  The standard-library checker audits the
integer profile classification, the previously used block-Gram quadratic
witness, and the arithmetic specialization to `Z/2310Z`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_profiles.py > /tmp/fuglede-2p1.txt
diff -u EXPECTED_OUTPUT.txt /tmp/fuglede-2p1.txt
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2.  The checker uses exact Python integers, no
third-party packages, floating point, randomness, solver, external dataset, or
generated certificate.  It corroborates the displayed finite arithmetic; it
does not replace the universal Fourier, cyclotomic, and inertia proof.

## Dependencies and scope

The descent and levelwise-cuboid inputs come from Gabor Somlai,
*Fuglede's Conjecture on Cyclic Groups of Square-Free Order: The Case of
Rapidly Growing Prime Factors*, arXiv:2607.26534.  The four-prime base theorem
is G. Kiss, R. D. Malikiosis, G. Somlai, and M. Vizer,
*Fuglede's conjecture holds for cyclic groups of order pqrs*,
arXiv:2011.09578.

This proof also uses the committed Discovery Net singleton-gap refinement and
simultaneous one-fat-level block-Gram obstruction identified precisely in
[PROOF.md](PROOF.md).  The case `p=3` is not claimed: inertia can be saturated
there, and the additional profile `(3,3,1)` survives the counting reduction.
The theorem says nothing about the divisible cardinality `2p`.

Focused searches of the primary literature and committed graph through
2026-09-19 found no matching `2p+1` descent theorem or positive-inertia level
obstruction.  This is search-relative evidence, not a priority claim.
