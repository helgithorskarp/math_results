# Convex quartics under Gaussian convolution at large variance

For every probability law supported in a radius-`R` ball in `R^3`, every
1-Lipschitz map, and Gaussian covariance `s I_3`, **all convex polynomial
internal energies of degree at most four compare in the conjectured
direction whenever `s >= 17 R^2/15`**. Convexity is required only on the
attained density interval `[0,(2 pi s)^(-3/2)]`. The slightly stronger
threshold is `R^2/s <= (15/2) log(9/8)`.

The [complete proof](PROOF.md) gives a strict quantitative quartic
determinant bound when some pairwise distances decrease. It also proves
that every fixed level of the team's Hankel hierarchy is positive at
an explicit sufficiently large variance, uniformly over all bounded
input laws and contractions. No covariance nondegeneracy, atom-count
restriction, paired-rank assumption, or small distance deficit is used.

The mechanism is a two-extra-replica variance identity plus weighted
Cauchy--Schwarz. It bounds the failure of log-convexity of the positive
weighted replica gaps. This retains contraction geometry that a purely
entropy-based bridge discards.

These are complete written author proofs, awaiting independent review.
**Full dimension-three majorisation remains open.** The finite-level
variance thresholds grow with degree. No new Kneser--Poulsen case or
optimality of the constants is claimed.

## Reproduce the finite audits

Use the complete repository checkout, with the sibling directories
listed in [SOURCES.md](SOURCES.md). From this directory:

```sh
python3 verify.py > /tmp/quartic-check.json
cmp /tmp/quartic-check.json EXPECTED.json
python3 -O verify.py > /tmp/quartic-check-optimized.json
cmp /tmp/quartic-check-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2, standard library only. All checks use explicit
exceptions, so optimized execution retains them. The output status is
`ALL_FINITE_CHECKS_PASSED`. Expected-output SHA256:

```text
7c4e2425ac26c09569e99efead41fff897983bf65636b35e081b05c23e14a0cb
```

The checker verifies:

- 220 rational two-extra-replica and online variance identities;
- the Jacobi orthogonality, squared norms, and exact inverse Gram
  matrices through level six, including all published constants;
- 64 rational quadratic-cone identities and the exact rational
  improvement in the quartic determinant;
- outward-enclosed moment gaps and positive Hankel pivots for the
  seven-point fold and sixteen-point simplex flap, including the
  degree-six test at `s/R^2=12015`;
- exact zero moment gaps in five isometric cases.

The numerical code deliberately reuses the team's previously published
multinomial replica and rational enclosure implementation. Four source
and fixture files are pinned by SHA256, and a changed dependency causes
failure. This is reuse with attribution, not a claim of independent
numerical implementation. No floating-point sign, numerical quadrature,
solver, Monte Carlo sample, or omitted large dataset is trusted.

The universal quantifiers rest on [PROOF.md](PROOF.md), not on the finite
audits. The trust boundary is the written, unformalized analytic proof
and the standard Python integer/Fraction implementation for the checks.

## Relation to the team frontier

The [relative moment-gap theorem](../gaussian_contraction_moment_gaps/PROOF.md)
supplied the weighted replica representation and already settled convex
cubics. The [Hankel theorem](../gaussian_majorisation_hankel_transport/PROOF.md)
identified the complete finite-polynomial obstruction. The present
quartic and finite-level estimates build directly on these durable
results. The earlier
[entropy bridge obstruction](../gaussian_majorisation_bridge_barrier/PROOF.md)
and the [half-order cancellation obstruction](../gaussian_majorisation_rank_abel/PROOF.md)
explain why entropy or an abstract positive smoothing profile alone
cannot supply the missing hinge sign.

At a fixed variance the next unresolved obligation is to control all
polynomial degrees, or to find a negative finite certificate outside
the regimes excluded here. In particular, adjacent log-convexity alone
does not imply positivity of every Hankel matrix.
