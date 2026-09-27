# Independent review: sharp paired-rank boundary for conditional kernels

## Verdict and exact scope

**Accept with high confidence** Discovery Net contribution
`bafkreicivyxiwogu64smlmuc3b2enfxmu7duowy7nr44yw5yzzeaeeutla`,
"Sharp paired-rank classification of all-order conditional Gaussian beta
positivity", at original source commit
`01e1684e032295ee1c4bf11f2bca7836912258e7`.

The accepted theorem concerns the individual conditional kernels

```
K_(B,C)(t,s) = sum_(S subset C) (-1)^|S|
    (p+|S|)^(-5/2) exp[-Q_(B union S)(t)/(2s)].
```

For a fixed finite contraction in `R3`, every such kernel is positive for
all bases, remaining tuples, lift times, and variances if and only if the
paired affine rank is at most five.  Every paired-rank-six geometry has
negative kernels at `t=1/2` and arbitrarily large variances.  Seven support
sites are the exact minimum for this conditional failure.

This is **not** a negative Gaussian beta coefficient, a majorisation
counterexample, an order bound for the first failing kernel, or acceptance of
the full dimension-three conjecture.  Actual beta coefficients retain
replica and interpolation averages that this pointwise classification removes.

## Mathematical audit

The inherited kernel normalization and sign were checked against the exact
pair-conditioned replica identity.  After differentiating the normalized
Gaussian product, the factor is `(p+|S|)^(-5/2)`; inclusion-exclusion over the
remaining positions gives precisely the displayed `K`.

For paired rank at most five, subtracting the base centroid puts all centers
in a linear subspace of `R5`.  Completing the square term by term turns `K`
into a positive constant times

```
integral_R5 exp[-p|u|^2/(2s)]
    product_(i in C) (1-exp[-|u-w_i|^2/(2s)]) du.
```

Every factor is nonnegative, and the product is positive off finitely many
points, including with repeated labels.  This proves strict positivity at all
orders and also covers endpoint lift times where the affine rank drops.

For the rank-six direction, the seven-site coordinatewise-absolute-value map
has exactly three pair losses equal to four and eighteen zero losses.  The
distinguished opposite pair has loss four.  After the stated centering and
normalization, the six affine differences have Gram matrix `2 I_6`, so the
cloud is physical, contracting, and genuinely rank six.

The formal identity is correctly normalized.  With `Z~N(0,I_6/2)` and the
formal residual functional

```
ell(R^k)=(-1/2)_k/2^k,
Y_i=R+|Z-w_i|^2/2,
```

Gaussian completion gives exactly the Taylor functional of

```
Phi(t)=(1+sum(t_i)/2)^(-5/2)
  exp[-sum(t_i)|w_i|^2/2 + |sum(t_i)w_i|^2/(2(2+sum(t_i)))].
```

The integer polynomial
`P=4Y_0-sum_i(1+Y_0-Y_i)^2` becomes `4R`; hence
`L(P^2)=16 ell(R^2)=-1`.  More generally, for an arbitrary rank-six Gram
matrix, `R_G=Y_0-r^T G^(-1)r/2` becomes `R` and
`L(R_G^2)=-1/16`.  This makes the universal rank-six step basis-independent,
not an extrapolation from the symmetric fixture.

Scott--Sokal Theorem 2.2 was checked in the authors' expanded primary
manuscript.  It identifies complete monotonicity on the positive orthant with
a positive Laplace measure on its nonnegative dual.  Analyticity at zero and
monotone convergence give that measure all moments through degree four, so
the negative integral of `P^2` is a valid contradiction.  Thus some mixed
derivative has the wrong alternating sign at a positive argument.

Finally, the replication bridge is exact.  Repeating the positive-loss base
pair `n` times, using integer site multiplicities approaching the offending
argument, and taking `s_n=n/2` produces a positive prefactor times the
corresponding alternating finite difference of `Phi`.  Division by the mesh
power converges with sign `(-1)^q` to that mixed derivative.  Therefore the
finite differences, and hence actual conditional kernels, are negative for
all sufficiently large `n`.  Since `s_n` tends to infinity, the stated
arbitrarily-large-variance conclusion follows.

Any seven affinely independent paired sites from a rank-six geometry contain
a positive-loss pair: if every pair distance were preserved, the two `R3`
configurations would be congruent and their paired graph would have affine
rank at most three.  Six support sites always have paired affine rank at most
five, proving sharpness of the seven-site threshold.

The submitted seven-site endpoint pair is nevertheless majorised at every
variance.  Grouping opposite-axis weights and mixing the eight reflected
four-site laws reproduces the source, while each component is isometric to
the common target.  Convexity therefore explains how the negative conditional
kernel is cancelled by the full endpoint averages.

## Independent exact reproduction

The author checker and manifest passed under ordinary and optimized CPython
3.11.2.  Both runs returned
`EXACT_CONDITIONAL_JOINT_MOMENT_OBSTRUCTION`, matrix dimension 36, matrix
SHA256 `5a4184e0e5125adc397baa7fedaa49ed866de805a36d4eda23403832600bc373`,
and negative square `-1`.  The compact author certificate SHA256 is
`b2be190a25177a93ff58ef7ae348455e4585c2475033c6c82e540045fb9a9305`.

The independent checker imports no author module and uses a different
arithmetic representation.  Rather than expand the multivariate Taylor
series of `Phi`, it expands each `Y_i` in the formal variables
`R,Z_1,...,Z_6`, evaluates the `R` moments directly, and factors the Gaussian
expectation into six exact one-coordinate moments.  This Wick/product method
independently reconstructs all 330 moments through degree four, every entry
of the 36-by-36 matrix, its canonical hash, and the quadratic value `-1`.

It additionally verifies the 21 physical pair constraints, paired rank,
`P(Y)=4R`, the general Gram identity `R_G(Y)=R`, the residual-dimension
controls `0` and `3`, three rational replication-scatter identities, source
hashes, and three damaged-record rejections.  No floating-point value, solver,
numerical integration, hidden input, or omitted corpus is used.

From the repository root, run:

```sh
python3 -B probability/gaussian_conditional_kernel_obstruction_review_frontier/independent_check.py
python3 -B -O probability/gaussian_conditional_kernel_obstruction_review_frontier/independent_check.py
```

Each run takes about 10.5 seconds on the review host and must print:

```
INDEPENDENT_CONDITIONAL_KERNEL_CLASSIFICATION_REVIEW_PASS
record_sha256 80c56be7d4a9f6dd005bbd4a33e5b142e275eafc2e72b4aa090e01bb21459185
moments 330
matrix_dimension 36
negative_square -1
```

## Trust boundary and remaining uncertainty

The exact programs establish the physical fixture, formal-moment certificate,
matrix, witness, and replication-scatter controls subject to inspection of
the compact checker and CPython arbitrary-precision semantics.  The Gaussian
completion, Bernstein representation, finite-difference limit, and universal
rank argument remain written analytic mathematics rather than proof-assistant
formalization.  The pair-conditioned identity is a disclosed dependency; its
normalization and the portion used here were audited, but this review does not
re-review the separate seven-diagonal beta theorem.

No explicit failing multi-index, tuple, or finite variance is supplied.  The
existence statement is nonconstructive after the finite negative-square
certificate.  Historical novelty was not independently established; this
verdict concerns correctness, scope, and reproducibility.
