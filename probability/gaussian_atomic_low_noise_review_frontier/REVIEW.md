# Independent acceptance: finite-atomic low-noise exclusion

## Verdict

I independently accept the theorem in source commit
`02b579d7e9c77053d7399096fe9314b9fdfca6f1`: for every fixed finite
contraction with positive common weights, either all labelled distances are
preserved and every endpoint gap vanishes, or every fixed complete endpoint
Hankel matrix is positive definite at all sufficiently small positive
variances.  This includes tight nearest target pairs and arbitrary target
collision patterns.

This is a bounded-degree exclusion theorem, not full Gaussian-convolution
majorisation.  It does not settle a single moderate variance, a degree growing
with inverse noise, a degenerating family of data, any negative hinge, or a new
Kneser--Poulsen case.  Novelty and historical priority were not audited.

## What was independently checked

I inspected the exact cited commit and pinned all seven target packet files,
plus the precise Hankel-criterion proof used for the witness interpretation.
The author's normal and optimized checkers reproduce their committed expected
output, and the directory-relative manifest passes.

The decisive distinct-target argument is valid.  Replica tuples containing no
shortened pair cancel exactly.  For a fixed active pair, target scatter is a
concave quadratic in the count vector, so its minimum on the count simplex is
at `e_i+e_j+(m-2)e_k`.  A candidate with `a+d>=c` loses to the corresponding
two-label branch.  If `a+d<c` and either leg to `k` is shortened, it loses to
that leg's two-label branch.  Thus every surviving three-label branch has two
tight legs and

```text
B = 2(a+d)-c = |x_i+x_j-2x_k|^2 + ell_ij >= beta.
```

For `f(m)=A/2-B/(2m)`, direct algebra gives

```text
f(i+j+2)-[f(2i+2)+f(2j+2)]/2
 = B(i-j)^2/[8(i+1)(j+1)(i+j+2)].
```

The replica lower bound retains one minimizing count vector, whose
multinomial multiplicity is at least `m`, label probability at least `p^m`,
and source-minus-target scatter at least `beta`.  Together with log-convexity
of `c_m=1/[m^(5/2)(m-1)]`, this yields the claimed normalized off-diagonal
bound.  The stated `K_D,L_(D,b)` make every off-diagonal strictly less than
`1/(2D)`, and the normalized matrix is at least `I/2` by diagonal dominance.

The separate collision argument is also valid.  Zero-scatter tuples converge
to the exact merger moments; every residual tuple has scatter at least
`(m-1)delta`, giving the one-sided exponential perturbation bound.  The merger
hinge is nonnegative everywhere and at least `p/64` on `[p/4,p/2]`.  Its moment
matrix therefore dominates the monomial Gram matrix there.  The shifted
Legendre coefficient estimate gives the advertised inverse-trace margin, and
the inequalities defining `Lc<=27bD` make the perturbation no larger than half
that limiting margin.

Finally, the normalization and witness bridge agree with the pinned complete
Hankel criterion: `v^T H_D v` is exactly the internal-energy gap for curvature
`P^2`.  A globally nonnegative univariate polynomial is a sum of two squares,
so positive definiteness excludes every non-affine globally convex polynomial
of the stated bounded degree.  This does not include arbitrary polynomials
convex only on the attained density interval.

## Independent executable evidence

`independent_check.py` does not import the target checker or reuse its four
fixtures.  It performs exact rational checks using:

* a new `5-12-13` tight-leg triangle, with `beta=100/169`, direct enumeration
  of every active count vector through replica order 20, and all curvature
  pairs through Hankel order 24;
* a new four-atom, two-collision partition, direct reconstruction of the
  source and target zero-scatter probabilities through replica order 10, and
  direct merger-hinge checks;
* definition-level rational LDL decomposition and Gauss--Jordan inversion of
  the collision interval Gram matrices, rather than the target's Legendre
  recurrence implementation; and
* 4,096 exact parameter-budget checks for `1<=D<=256`, `1<=b<=16`, including
  the degree-rate and collision perturbation constants.

Run from this directory with standard-library Python 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected marker: `INDEPENDENT_ATOMIC_LOW_NOISE_REVIEW_PASS`.

## Trust boundary

The executable evidence checks the exact source bytes, new adversarial finite
instances, matrix algebra, and all displayed scalar constants over broad
finite ranges.  The universal reduction, Gaussian product identity,
concavity argument, merger-hinge lower bound, and all-parameter inequalities
remain reviewed written mathematics rather than formal proof.  The checks do
not infer the theorem from sampling.  The accepted conclusion remains
conditional on the standard Gaussian integration identity and the pinned
complete Hankel criterion; no solver, floating-point computation, private
dataset, or ledger state is a proof premise.
