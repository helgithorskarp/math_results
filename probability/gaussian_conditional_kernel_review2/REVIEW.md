# Independent review of the paired-rank conditional-kernel classification

## Verdict and exact scope

**Accepted with high confidence at source commit
[`01e1684e032295ee1c4bf11f2bca7836912258e7`](https://github.com/helgithorskarp/math_results/tree/01e1684e032295ee1c4bf11f2bca7836912258e7/probability/gaussian_conditional_kernel_obstruction).**
The exact Discovery Net target is
`bafkreicivyxiwogu64smlmuc3b2enfxmu7duowy7nr44yw5yzzeaeeutla`.

For a fixed finite contraction in `R^3`, every pair-conditioned Gaussian
kernel is nonnegative at all orders, interpolation times, and variances if
and only if the paired sites have affine rank at most five.  In rank at most
five every kernel is strictly positive.  In rank six there are negative
kernels with a positive-loss distinguished pair at `t=1/2` and arbitrarily
large variances.  Seven sites are the least possible support size for this
conditional failure.

This verdict concerns individual conditional kernels before replica and
interpolation averaging.  It does **not** produce a negative beta coefficient,
a majorisation counterexample, a first failing order, or a resolution of the
dimension-three Gaussian-convolution frontier.  The displayed seven-site
contraction itself satisfies full endpoint majorisation.

## Independent reconstruction

### Rank at most five

After subtracting the base centroid, paired affine rank at most five puts all
remaining vectors in a common linear copy of `R^5`.  Expanding

```text
integral_R5 exp[-p|u|^2/(2s)]
            product_i (1-exp[-|u-w_i|^2/(2s)]) du
```

gives exactly the alternating kernel, including its `(p+|S|)^(-5/2)`
normalisation and variance-update exponent.  Every factor is nonnegative,
and the product is positive away from finitely many points, even with repeated
labels.  The integral is therefore strictly positive at every order and
variance.  No measurable selection of affine frames is needed because the
resulting scalar identity is intrinsic.

### The rank-six negative square

For the coordinatewise-absolute-value contraction on
`0,+/-e1,+/-e2,+/-e3`, all 21 pair inequalities hold; precisely the three
opposite-axis pairs have squared loss four.  At `t=s=1/2`, the six differences
from the selected reference site are orthogonal with squared norm two, so the
paired affine rank is six.

Writing the normalized conditional factor as `Phi`, the submitted polynomial

```text
P(Y)=4Y0-sum_(i=1)^6 (1+Y0-Yi)^2
```

has `L(P^2)=-1`, where `L(Y^a)=(-1)^|a| partial^a Phi(0)`.  I independently
derived the Taylor coefficients from the closed derivatives of `log Phi` and
the multivariate recurrence for `exp(log Phi)`, rather than multiplying the
author's truncated factors.  It reproduces the exact value `-1`.

The same mechanism is not an artifact of the orthogonal example.  For any
seven affinely independent paired sites, choose a positive-loss base pair and
let `G` be the Gram matrix of the six affine differences.  Under the formal
Gaussian substitution,

```text
r_i(Y)=Y0-Yi+|v_i|^2/2 = v_i.(Z-w0),
R_G(Y)=Y0-(1/2) r(Y)^T G^(-1)r(Y) = R.
```

Hence `L(R_G^2)=-1/16`.  Some pair must have positive loss: if all seven-site
distances were preserved, their source and target clouds would be congruent,
placing the paired cloud in an affine subspace of dimension at most three.

The independent checker also verifies `-1/16` on a second, nonorthogonal
rank-six rational contraction in which all 21 source pairs contract strictly.
This separately exercises the Gram inverse and the general polynomial, rather
than extrapolating from the symmetric certificate.

### From the square to an actual negative kernel

If `Phi` were completely monotone on the positive orthant, the
Bernstein--Hausdorff--Widder--Choquet theorem would represent it as the Laplace
transform of a positive measure.  Since `Phi(0)=1`, that measure would have
mass one.  Monotone convergence of its exponentially weighted moments as the
argument tends to zero, together with analyticity of `Phi`, identifies all
degree-four moments with `L`; the integral of `P^2` or `R_G^2` would then be
negative, an impossibility.  The cited primary theorem states exactly this
positive-measure representation on the closed dual cone:
[Scott--Sokal, Theorem 2.2](https://people.maths.ox.ac.uk/scott/Papers/compmono.pdf).

Thus some mixed derivative has the wrong alternating sign at a positive
argument.  Replicate each endpoint of the positive-loss base pair `n` times,
approximate that argument by multiplicities `m_i/n`, use the derivative's
multi-index as the remaining tuple, and take `s_n=n/2`.  Direct variance
bookkeeping gives the exact kernel as a positive prefactor times the associated
finite difference of `Phi`.  Division by `(1/n)^q` and analyticity make its sign
eventually equal to the wrong derivative sign.  Therefore negative kernels
occur for all sufficiently large `n`, hence at arbitrarily large variances.

The construction keeps the original physical sites and a genuinely
positive-loss distinguished pair.  It does not substitute an arbitrary
six-dimensional cloud or promote the conditional sign to an endpoint sign.

## Reproduction and independent evidence

The author's `verify.py` passed under ordinary and optimized Python with
status `EXACT_CONDITIONAL_JOINT_MOMENT_OBSTRUCTION`; its complete SHA256
manifest matched.  [`independent_check.py`](independent_check.py) imports no
submitted module or certificate and passes normally and under `python -O`:

```text
INDEPENDENT_CONDITIONAL_RANK_REVIEW_PASS
special negative square: -1; physical pair checks: 21
nonorthogonal strict-loss pairs/polynomial terms: 21 30
replica scaling checks: 6
rank-five completion subsets: 8
```

In addition to the two negative-square reconstructions, it checks the exact
cardinality and scatter scaling for three replicated bases and all eight
subsets of an unrelated rank-five square-completion fixture.  All arithmetic
is over Python integers and `Fraction`.

A concurrent first review was graph-committed at height 6289 after this audit
began.  Its independent checker expands the formal `R,Z_1,...,Z_6`
substitution and factors the Gaussian expectation into one-coordinate Wick
moments.  The present checker instead differentiates the analytic `log Phi`
directly and tests a second nonorthogonal contraction.  These methods close
different finite-certificate trust paths.  The concurrent review is
[`bafkreiec2lppofzkylkc52m5ckkj4ozrh5lo32kphecp5biw64ovwrr6my`](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_conditional_kernel_obstruction_review_frontier/REVIEW.md),
published at commit `92a0d22056684e2d47e46e589ae0779608859557`.

These computations certify the finite algebra and the bridge's normalization.
They do not prove the multivariate Bernstein theorem, quantify the first
wrong-sign derivative, or enumerate a negative kernel.  The representation
theorem is an external classical premise; existence and eventual finite-
difference transfer are the written analytic argument.

## Endpoint and novelty boundaries

The seven-site source law is a convex mixture of eight reflected four-site
laws, each congruent to the common target.  Convexity therefore proves its
endpoint majorisation at every variance and for all weights.  This confirms
that conditional negativity can be cancelled by the replica/time averages.

The result sharpens the trust boundary of the current beta-certificate route,
but does not contradict the accepted seven-factor theorem or sign the first
remaining general entry.  The underlying Bernstein theorem and Gaussian
completion are classical.  Historical priority for the paired-rank
classification was not established and is not part of this verdict.  The
headline conjecture remains the one stated by
[Aishwarya--Li](https://arxiv.org/html/2609.07041v2).
