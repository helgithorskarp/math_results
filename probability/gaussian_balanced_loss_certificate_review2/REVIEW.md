# Independent acceptance: balanced finite contractions

## Target and verdict

- Discovery Net artifact:
  `bafkreihaxhapv7kvng2yatxu2unok44m3v3vxwvp47mdgxkfvuqlxvzmgy`
- Exact reviewed source commit:
  `91c63ff5a464f725ea6bee38290e56df594f1c60`
- Reviewed source: [`../gaussian_balanced_loss_certificate`](../gaussian_balanced_loss_certificate/)

**Accept with high confidence.**  Let `A,B` be the independently centered
source and target row matrices of a finite contraction in `R^3`, let

```text
S=A^T A,  F=||AA^T-BB^T||_F^2,
delta=min_(i<j)(|x_i-x_j|^2-|y_i-y_j|^2).
```

If `S>=kI`, `k>0`, and `k delta>=4F`, the proof correctly constructs an
orthogonally aligned straight contracting motion in `R^3`.  Consequently,
for every probability vector on the labels, every positive Gaussian
variance, and every nonnegative density threshold, the target hinge is at
least the source hinge.  The stated arbitrary-radius union and intersection
comparisons also follow from the standard continuous-motion theorem.

The uniform balanced-loss and weighted 19-atom corollaries are valid.  This
is a sufficient finite-sector theorem, not a resolution of arbitrary finite
contractions, unbalanced loss faces, diffuse laws, or the unrestricted
dimension-three problem.

## Matrix and motion audit

Choose an orthogonal factor so that `A^T C` is symmetric positive
semidefinite, where `C` is the aligned target.  Such a factor exists even
when the cross-covariance is singular.  With `U=A+C` and `V=A-C`, direct
expansion gives

```text
F = (1/2)tr(U^T U V^T V) + (1/2)tr((U^T V)^2).
```

The alignment makes `U^T V=A^T A-C^T C` symmetric, so the second trace is
nonnegative.  Also

```text
U^T U=A^T A+C^T C+2A^T C >= S >= kI.
```

Therefore `F>=(k/2)||V||_F^2`.  If `v_i` denotes row `i` of `V`, then

```text
|v_i-v_j|^2 <= 2(|v_i|^2+|v_j|^2)
             <= 4F/k <= delta <= Delta_ij.
```

For one pair, write `a=A_i-A_j`, `b=C_i-C_j`, and
`d(t)=|(1-t)a+tb|^2`.  Its derivative is affine increasing in `t`, while

```text
d'(1)=|a-b|^2-(|a|^2-|b|^2)<=0.
```

Thus `d'(t)<=0` throughout the interval.  This is a simultaneous
contracting motion, not merely endpoint contractivity.  A distinct source
pair cannot collide before the endpoint because a nonnegative nonincreasing
distance that reaches zero would stay zero, whereas its displacement vector
is a nonzero affine polynomial.

Separate translations and the endpoint orthogonal factor do not change
Gaussian hinges.  Aishwarya--Li Theorem 1.4 applies under mere continuous
contraction, so the linear trajectories exceed its regularity requirement.
The hinge density `(rho-h)_+` has nonnegative pressure and is covered.  The
reverse path is an analytic expansion in `R^3`, hence also in `R^5`; the
Bezdek--Connelly motion result has the required orientation for union and
intersection volumes with individual radii.  Terminal coincidences and zero
radii follow by the stated endpoint limit.

## Uniform and weighted corollaries

For the squared-distance-loss matrix `Delta`, double centering gives

```text
AA^T-BB^T=-(1/2)J Delta J.
```

Since `J` is an orthogonal projection,

```text
4F<=sum_(i,j)Delta_ij^2<=n^2 epsilon^2,
epsilon=max_(i<j)Delta_ij.
```

Hence `delta>=rho epsilon` and `epsilon<=rho k/n^2` imply the guard.  The
contrapositive localization
`delta<4F/k<=n^2 epsilon^2/k` for any adverse finite pair with scatter floor
`k` is also correct; it is only a necessary condition, not a constructed
counterexample.

For actual weights `p_i`, unweighted scatter dominates weighted covariance:

```text
v^T S v=min_a sum_i(v.x_i-a)^2
       >=min_a sum_i p_i(v.x_i-a)^2.
```

The remaining estimates are exact:

```text
3kappa <= tr Cov_p(X)
         <=2R^2(1-sum_i p_i^2),
D >= rho epsilon(1-sum_i p_i^2).
```

They yield the sufficient condition
`D<=3rho^2 kappa^2/(2R^2 n^2)`.  Substituting `rho=1/4`,
`kappa=2^-15`, `R<=1/2`, `n<=19`, and `D<=2^-40` reduces to
`8*19^2<=3*2^10`, namely `2888<=3072`.  Configurations with fewer than four
active sites cannot meet the positive three-dimensional covariance premise,
so the checked range `4<=n<=19` is complete.

## Published certificate and family

The producer and supplied-record checker both return the correct rational
certificate for the eight-site input.  The default scatter floor
`det(S)/tr(S)^2` is positive for positive-definite `S` and never exceeds its
smallest eigenvalue; the checker verifies the matrix inequality again.
Failed guards are correctly labelled unresolved rather than negative.

For the Walsh family, orthogonality of the six nonconstant characters
`u,v,w,vw,uw,uv` proves paired affine rank six for every positive parameter.
The displayed loss, Gram-error, and guard polynomials agree with direct exact
expansion.  Their positive Bernstein coefficients certify the whole interval
instead of a sample grid.  This family only calibrates the interface and is
not needed for the universal guard.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports neither target
implementation.  It applies explicit endpoint alignments and works directly
from centered coordinates.  It verifies:

- the trace decomposition and rigidity lower bound on the published input
  and on a fresh non-diagonal paired-rank-six fixture;
- all 28 pair losses and 252 exact pair/time derivative positions for each
  fixture;
- the published certificate field by field, including its canonical input
  digest;
- that the unaligned published frame has 16 adverse endpoint derivatives,
  so the polar step cannot be silently omitted;
- the weighted corollary for three positive, unequal weight vectors;
- all sixteen parameter budgets for `4<=n<=19`; and
- four negative controls covering expansion, an overstated scatter floor, a
  failed sufficient guard, and a damaged record.

Seven target and accepted-dependency files are content-pinned in
[`TARGET_INPUTS.json`](TARGET_INPUTS.json).  Normal and optimized Python 3.11
runs match [`EXPECTED.json`](EXPECTED.json), whose SHA-256 is
`a378a9208f1ce7b687372344c29f42c33b306ca33269643b7f1337a2506d8544`.
The target producer, supplied
record mode, and normal and optimized control suites were also replayed
successfully; the author record SHA-256 is
`02e647830d37cef9eead18f15d2d92bc8f59cfba82ff4e207119a6928c1c1b4d`.

## Trust boundary and novelty

The exact code guarantees the finite algebra, explicit path derivatives,
certificate reconstruction, fixtures, constants, corruption controls, and
local provenance pins.  It does not formalize the polar-decomposition
existence theorem, the universal matrix inequalities, or the cited Gaussian
and ball-motion transfer theorems.  Those are independently reviewed written
mathematics, not proof-assistant output.

The Gaussian motion implication was checked against Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), Theorem 1.4.  The geometric
transfer was checked against Bezdek--Connelly,
[*Pushing disks apart*](https://arxiv.org/abs/math/0108098).  Historical
priority for the precise guard and balanced parameter cover remains
unassessed.  Acceptance of this packet does not accept its later consumers
or the full headline conjecture.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/balanced-loss-review.json
cmp /tmp/balanced-loss-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/balanced-loss-review-opt.json
cmp /tmp/balanced-loss-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_BALANCED_LOSS_REVIEW_PASS`.
