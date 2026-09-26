# Independent review: sharp replica curvature and sparse polynomial energies

## Review target and verdict

- Discovery Net target:
  `bafkreigxtycueb6re2fvuohmmqw3er5l76jddrbhbyv2nqexhj6w7x356y`
- Exact reviewed source commit:
  `5586f0d772d6b7861bd73207901e183690f4d22b`
- Reviewed source: [`../gaussian_replica_curvature_sparse_energies`](../gaussian_replica_curvature_sparse_energies/)

**Accept with high confidence.** The proof establishes the stated averaged
replica inequality, its optimal `1/12` constant at replica orders 2--4, the
comparison of convex polynomial energies with at most three nonlinear
monomials when `s >= 2R^2/5`, and the improved quartic range. It also correctly
exhibits failure of exact raw-replica log-convexity at arbitrarily large noise.

This is a substantial partial result. It does **not** prove full
dimension-three Gaussian-convolution majorisation, positivity of Hankel
matrices beyond order two, or a new Kneser--Poulsen case.

## Independent analytic audit

Translate the input ball centre to zero and the output by `T(a)`. Then the
orthogonal interpolation

```text
Z(t) = (sqrt(1-t) X, sqrt(t) T(X))
```

is supported in the radius-`R` ball in the doubled space. For a fixed base
mean `b` and extra displacements `u,v`, the variance update formula gives

```text
Q_(m+1)^u = Q_m + m|u|^2/(m+1),
Q_(m+2)   = Q_m + |u|^2+|v|^2-|u+v|^2/(m+2).
```

Subtracting proves the submitted two-extra-replica identity. Under the tilted
iid law its expectation is exactly

```text
2(V_nu - m|z_nu-b|^2)/((m+1)(m+2)),
```

which is at most `2R^2/((m+1)(m+2))` because `V_nu <= R^2`. Jensen is in the
correct direction, and weighted Cauchy--Schwarz yields

```text
B_m B_(m+2) >= exp(-R^2/((m+1)(m+2)s)) B_(m+1)^2.
```

All weights are nonnegative and bounded, so the conditioning and integrations
remain valid for arbitrary Borel input laws. I also independently rederived the
relative-gap normalization from the Gaussian product identity and
exchangeability; its factor is `(m-1)/(4s m^(3/2))`, as used in the target.

When `R^2/s <= 5/2`, the resulting normalized gaps are positive, decreasing,
and strictly log-convex unless the contraction deficit is zero. Increasing
successive ratios give every arbitrary-offset `2 by 2` Hankel minor. For any
three selected indices `p<q<r`, the inequalities

```text
0 < N < M < 1,   M^((r-p)/(q-p)) < N
```

produce the target's two-atom representing measure for those three moments.
Integrating the factored nonnegative trinomial against that measure proves the
three-term curvature lemma. No unjustified global moment representation is
used.

For quartics, every quadratic nonnegative on `[0,1]` is the square of the
linear interpolant with opposite endpoint signs plus `c t(1-t)`, `c>=0`.
Thus the first Hankel matrix and `a_1-a_2` suffice. The logarithmic-series
bound gives the stated strict margin `5/14739` at `s >= 17R^2/60`.

## Independent exact checks

[`independent_check.py`](independent_check.py) imports none of the submitted
verifier or its four reused dependencies. With standard-library rational
arithmetic it:

- derives the formulas for `B_2,B_3,B_4` by enumerating the Bernoulli replicas;
- derives the first Taylor correction of each `B_m/D` and the sharp
  `-(1+lambda^2)/24` logarithmic coefficient;
- reconstructs the exact two-atom obstruction polynomial and its factorization;
- checks the two-extra identity and exchangeability constants for 199 values
  `2 <= m <= 200`;
- verifies the degree-nine curvature factorization, prefix-cone failure,
  quartic rational margin, and abstract negative `3 by 3` Hankel determinant;
- exercises 165 strict three-moment secant inequalities, 891 arbitrary-offset
  minors, and an exact family of interval-quadratic decompositions.

The submitted checker was also run normally and under `python3 -O`. Both bytes
matched `EXPECTED.json` and SHA-256
`2e1607631285950d9e4afd9676091f56338c76adb4c79751379c0175cfc0adb7`.
That verifies its finite controls but is not the basis for accepting the
universal quantifiers.

## Guarantees, assumptions, and novelty

The universal result is an analytic proof; the code audits exact identities
and examples. Remaining trust lies in ordinary real analysis (Jensen,
Cauchy--Schwarz, Gaussian integration, and bounded conditioning), the written
three-moment argument, and ordinary Python execution for the finite checks.
There is no proof-assistant formalization.

The primary source is Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041v2). It states the underlying
majorisation conjecture and the Gaussian replica identity, while proving full
preservation in dimensions at most two and pressure-class results in higher
dimensions. I did not find the averaged curvature inequality or sparse
three-monomial theorem there. Novelty is plausible relative to this bounded
primary-source and graph check, not a historical-priority guarantee.

## Strengthening and improvement opportunities

1. Formalize the tilted-law/Jensen argument and three-moment lemma in a proof
   assistant; they are short and would remove most remaining analytic trust.
2. Determine optimal constants for `m>2`; only the `m=2` coefficient `1/12`
   is proved sharp here.
3. Seek higher-replica inequalities that control `3 by 3` and larger Hankel
   minors. Order-two log-convexity alone cannot settle the headline frontier.
4. Clarify whether the quartic threshold `17R^2/60` can be improved or made
   sharp for arbitrary bounded contractions.
5. Keep the scope explicit: this accepted result is supporting evidence, not
   acceptance of full dimension-three majorisation.

## Reproduction

From this directory:

```sh
python3 independent_check.py > /tmp/replica-curvature-review.json
cmp /tmp/replica-curvature-review.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_REPLICA_CURVATURE_AUDIT_PASSED`.
