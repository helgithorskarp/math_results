# An all-variance neighborhood of asymmetric paired-layer contractions

Complete author proof, 26 September 2026; independent review and formalization
are pending. The small-variance endpoint in [PROOF.md](PROOF.md), combined
with three credited team results, gives a spatial neighborhood that works
**uniformly over every positive variance**. This is stronger than separate
neighborhoods whose radii may tend to zero at extreme variances. The full
three-dimensional conjecture remains open.

## 1. Statement

Use the reference clouds and weights

```
A0 = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),
B0 = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),
p  = (8,12,7,15,44,21,11,23,43)/184.
```

**Theorem.** There exists a number delta_* > 0 such that the following
holds. Let A=(a_1,...,a_4) and B=(b_1,...,b_4) be four-point clouds in
z=1, each invariant under J(x,y,1)=(-x,-y,1), with

```
max_i |a_i-A0_i| <= delta_*,
max_j |b_j-B0_j| <= delta_*,
a_i dot b_j >= 0 for every i,j.                              (1)
```

Let w be any probability vector with ||w-p||_1 <= 1/25000. Define

```
mu = w_0 delta_0 + sum_i w_i delta_ai + sum_j w_(4+j) delta_(-bj),
nu = w_0 delta_0 + sum_i w_i delta_ai + sum_j w_(4+j) delta_bj.
```

Then, for every s > 0 and every h >= 0,

```
integral (mu*gamma_s-h)_+ <= integral (nu*gamma_s-h)_+.        (2)
```

The prescribed map is a contraction, with a global 1-Lipschitz extension,
because its only nonzero squared-distance losses are 4 a_i dot b_j.
The weights need not have any symmetry. The cloud radius delta_* is
proved to exist, uniformly in w and s; **a numerical value is not certified**.
The explicit endpoint bounds below are separate quantitative statements.

In particular, (2) holds on a nontrivial interval of the undamped shear
family in PROOF.md, Section 8, simultaneously for all variances. It is not
legitimate to substitute 1/1000 or 1/16384 for delta_* without additionally
certifying the middle-variance spatial radius.

## 2. The small-variance endpoint is uniform in geometry

Put s_min=10^-10. If the labelled perturbations are at most 1/1000, the
geometric norm and anchor hypotheses of PROOF.md hold. To see the norm
bounds without approximate square roots, observe

```
(7/5+1/1000)^2 < 2,        (17/10+1/1000)^2 < 3,
(2-1/1000)^2 > 3.
```

At the reference anchor a_4=(0,-1,1), all cross distances are at least 1,
and the distance to b_4=(1,-1,1) is 1. Under the perturbation, every
cross distance from a_4 stays at least 1-2/1000 > 9/10, and the indicated
neighbor distance is at most 1+2/1000 < 101/100. The other hypotheses
are exactly the assumed plane, symmetry and contraction conditions.
Every weight in the stated ball satisfies

```
min_i w_i >= 1/32,       w_0 <= 1/16,       w_4 >= 1/5.
```

Consequently [PROOF.md](PROOF.md) gives (2) for **all** 0 < s <= s_min
and all such perturbations, with no variance-dependent spatial radius.
The proof controls every threshold, including thresholds tending to zero
at an arbitrary rate as s decreases. That uniformity is essential here.

## 3. A quantitative high-variance perturbation bound

We prove (2) for every s >= s_max=45056 whenever the labelled spatial
perturbation is at most d=1/16384. This step uses the earlier
[asymmetric spherical certificate](../gaussian_asymmetric_eventual_majorisation/PROOF.md)
and the [eventual-endpoint theorem](../gaussian_majorisation_eventual_endpoint/PROOF.md).
These are essential mathematical dependencies, not numerical observations.

With normalized sphere area sigma, define

```
S_mu(lambda) = integral_(S^2) log E_mu exp(lambda theta dot Z) d sigma,
J(lambda) = S_mu(lambda)-S_nu(lambda).
```

Let J0,w be the same quantity for the unperturbed reference sites and
weights w. The preceding spherical certificate proves, simultaneously for
every ||w-p||_1 <= 1/25000,

```
J0,w(lambda) >= 1/128                 for every lambda >= 1/4. (3)
```

For corresponding atoms displaced by at most d, the moment-generating
functions at each theta are between exp(-lambda d) and exp(lambda d)
times the original one. Taking logarithms and averaging gives the exact
stability estimate

```
J(lambda) >= J0,w(lambda)-2 lambda d.                          (4)
```

Thus, for 1/4 <= lambda <= 32,

```
J(lambda) >= 1/128-64/16384 = 1/256.                          (5)
```

For the unbounded parameter ray we use the mean-support margin from the
same preceding source. If h_X0,h_Y0 are the reference support functions,

```
integral (h_X0-h_Y0) d sigma >= 1/6.                          (6)
```

Moving every labelled atom by at most d changes each support function
pointwise by at most d. Hence the new mean-support gap is at least
1/6-2d >= 1/8. With the minimum weight at least 1/32, the elementary
maximum bounds for weighted exponential sums give

```
J(lambda) >= lambda/8 - log 32 >= 1/2       (lambda >= 32).   (7)
```

Here log 32 < 7/2, certified by the first eight nonnegative Taylor terms
of exp(7/2). This is a bound on the entire infinite parameter ray, not
an extrapolation of (5). Combining (5) and (7) yields

```
J(lambda) >= 1/256                  for every lambda >= 1/4. (8)
```

Both perturbed supports are in B(0,2). The eventual-endpoint theorem,
with R=2 and kappa=1/256, applies to the genuine contraction in (1) and
gives every hinge once

```
s >= R^2 max(8,44/kappa) = 4*44*256 = 45056.                 (9)
```

Thus the high-variance endpoint also has a single positive spatial radius.
The input/output origin is fixed, so the support ball and contraction
normalization required by that theorem are exactly satisfied.

## 4. The intervening interval and completion

Apply researcher 8's
[spatial-cloud stability theorem](../gaussian_majorisation_open_stability/PROOF.md),
Theorem 1, to the compact interval

```
I = [10^-10,45056].
```

It supplies epsilon_I > 0, uniform over all reference probability weights
in the larger L1 ball of radius 1/4000. Replacing each atom independently
by any probability cloud within epsilon_I of that atom preserves every
hinge for every s in I. In particular, it permits our single-atom
perturbations and our smaller weight ball. Its strictness and compactness
proof is an essential dependency; we do not infer this radius from
finite numerical hinge samples.

Choose

```
delta_* = min(epsilon_I,1/16384) > 0.                        (10)
```

Since 1/16384 < 1/1000, Section 2 covers (0,10^-10], Section 4 covers
[10^-10,45056], and Section 3 covers [45056,infinity). All use the same
spatial radius and the same weight set. They cover every positive variance,
proving (2). The value epsilon_I, and therefore the certified numerical
value of delta_*, is not computed in the cited stability theorem or here.
The proof is an existence theorem for a uniform neighborhood.

## 5. Consequence for the counterexample frontier

For the explicit shear family

```
A_e = ((1,0,1),(e,1,1),(-1,0,1),(-e,-1,1)),
B_e = ((1,1-e,1),(-1,1+e,1),(-1,-1+e,1),(1,-1-e,1)),
```

the maximum labelled displacement is |e|. Every cross dot product remains
0 or 2. Consequently the whole interval |e| <= delta_* obeys (2), for
all weights in the radius-1/25000 ball and all variances at once. All these
are undamped reflections of full nonsimplicial dual cones.

This extends beyond the original centered fixed-ray supports, even though
no particular nonzero numerical shear is certified for all variances.
Indeed for every 0 < |e| <= 1/1000, the squared cosine

```
q(e) = (1+e)^2/[2(2+e^2)]
```

is different from every member of {0,1/4,1/9,2/3}. It lies strictly
between 1/5 and 1/3; equality with 1/4 would require e(4+e)=0.
Orthogonal maps and individual positive radial rescalings preserve these
squared angles. This proves departure from the stated centered ray class
throughout the punctured neighborhood, without claiming exclusion of every
other representation or future extension of the orbit method.

The shared positive obligation is now stronger than fixed-variance
stability: there cannot be a sequence of Gaussian counterexamples among
these admissible paired layers whose geometry approaches the reference
pair and whose weights stay in the stated weight ball, **even if their
variances tend to zero or infinity**. In the global criterion this is
Delta_s=0 uniformly over all s>0 on one constrained spatial neighborhood.
This is not an additional obstruction to a proposed proof technique.

No conclusion is made for arbitrary three-dimensional contractions,
arbitrary asymmetric polygons, arbitrary nonatomic perturbations down to
zero variance, or the entire explicit shear interval 1/1000 at all variances.
The latter interval is certified at small variance by PROOF.md. No new
Kneser--Poulsen consequence is asserted. The contribution here is the
uniform small-variance localization and its completion of the two extreme
variance regimes around the credited strict asymmetric benchmark.

## 6. Dependencies and evidence

The all-variance conclusion uses three published statements in addition
to the new self-contained small-variance theorem:

1. The spherical bound (3) and mean-support gap (6) from the asymmetric
   eventual-majorisation source, whose finite cubature uses Arb balls.
2. The eventual-endpoint theorem transferring (8) to every high-variance
   hinge, with its reviewed analytic dependencies.
3. The spatial-cloud stability theorem, including the earlier exact
   all-hinge orbit certificate and its new strictness certificate.

The new exact checker audits the perturbation constants, parameter
interval junctions and geometric bounds. Reproduction of the essential
borrowed finite certificates is documented in README.md and VALIDATION.md.
These checks do not replace review of any of the written continuum proofs.
