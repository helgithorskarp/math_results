# Review of Gaussian contraction equality and quantitative rigidity

Date: 2026-09-22

Target commit: `6d9d63c5a8955f350206f70db2c826f7373587d4`

Target graph reference: `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`

## Verdict

**Accept, with high confidence in the stated scope.** I found no mathematical
defect in the equality classification, quantitative rigidity estimates,
sharp root-mean-square exponent, or posterior maximum-density bound. The
compact path identity, noncompact limiting argument, strictness mechanism,
and Gram-to-rigid-motion reduction form a complete chain. The accompanying
finite evidence reproduces exactly under normal and optimized Python.

The result is an equality-and-stability refinement of a known qualitative
Gaussian Rényi entropy comparison. The verdict does not certify historical
priority. A bounded live primary-source search supports the package's careful
claim that the qualitative comparison is prior work and that no matching
equality/stability result was located.

More precisely, for a Borel probability law `mu` on `R^n`, a 1-Lipschitz
map `T`, Gaussian variance `s>0`, and every positive Rényi order including
Shannon and infinity, the reviewed theorem proves equality (when the input
entropy is finite) exactly when `T` agrees on `supp(mu)` with an ambient
rigid motion. Under radius `R` and `Cov(X)>=kappa I`, it gives an explicit
entropy-loss lower bound by mean pair-distance loss and hence a quantitative
Procrustes bound. It also proves the optimal root-mean-square exponent `1/2`
and the sharp posterior coefficient `1/(4s)` at order infinity.

## Independent proof audit

### 1. Doubled lift and exact entropy dissipation

For the lifted path `c_t`, direct expansion gives

    |c_t(x)-c_t(x')|^2
      = cos^2(pi t/2)|x-x'|^2
        + sin^2(pi t/2)|T(x)-T(x')|^2.

Differentiating this identity gives the signed velocity pairing
`-(pi/4) sin(pi t) Delta`. The posterior covariance identity then yields

    div(w_t) = -(pi sin(pi t)/(8s)) M_t/q_t^2.

The sign and factor `1/8` are correct. Applying the continuity equation to
the power integral gives

    d h_alpha(q_t)/dt
      = integral(q_t^alpha div(w_t))/integral(q_t^alpha),

including the Shannon limit. Integrating from the input endpoint to the
contracted endpoint therefore produces the displayed positive dissipation
identity. The endpoint tensorization cancels the auxiliary Gaussian exactly.

For compact input, bounded centers and velocities give the Gaussian tail
bounds needed for differentiation and cutoff integration by parts. This
works for `0<alpha<1`: although negative powers occur after substituting the
posterior formula, the mixture has a Gaussian lower tail bound and the final
integrands remain dominated by Gaussian decay for each fixed positive order.

### 2. Arbitrary laws, equality, and completeness of the rigid extension

The truncations are normalized conditional laws, while the proof keeps the
unnormalized convolutions monotone. The common normalization factors cancel
for power integrals. For Shannon entropy, the auxiliary function
`eta_M(u)=u log(M/u)+u` is nonnegative and increasing on `[0,M]`, so monotone
convergence applies without a moment hypothesis.

For the dissipation numerator, normalized lifted densities and pair kernels
converge pointwise. Denominators are positive and finite: bounded density
handles orders above one, normalization handles order one, and monotonicity
along the compact paths bounds orders below one by the finite input endpoint.
Fatou is used in the correct lower-bound direction. If `Delta` is positive
on a set of positive product measure, every Gaussian factor is strictly
positive, making the limiting lower bound strictly positive. Thus equality
forces `Delta=0` almost everywhere.

Continuity of `Delta` upgrades that conclusion to every pair in
`supp(mu)`. Affinely independent anchors spanning the support's affine hull
determine an isometry of that hull; the distance to the anchors rules out an
orthogonal residual for every further support point. Extending orthonormal
bases gives an ambient orthogonal map. This covers lower-dimensional and
singleton supports, so no hidden full-dimensional assumption enters the
equality classification.

### 3. Explicit compact constants and order infinity

After translating so that the support lies in `B(0,R)` and `T(0)=0`, every
lifted center remains in that same radius ball. On the `2n`-dimensional ball
of radius `sqrt(s)`, the proof's kernel bounds give

    q_t^(alpha-2) M_t
      >= U^alpha exp[-max(2,alpha) A] D.

The split at order two is correct: use the lower bound for the positive
power and the upper bound for the negative power. The power-integral bounds
for orders above and below one, the `2n`-ball volume, and
`integral_0^1 sin(pi t) dt=2/pi` reproduce exactly the stated
`2^(n+2)n!s` denominator.

At infinity, a Gaussian convolution of a finite measure is positive,
continuous, and vanishes at infinity, hence has a mode. Its posterior has
all polynomial moments even when the original law does not. The mode
condition gives posterior mean `z`. Jensen's inequality at the displaced
point `T(z)+m` yields

    G_infinity >= (E r + |m|^2)/(2s)
               = E_{nu_z x nu_z} Delta/(4s).

For compact support, `z` is in the posterior convex hull; consequently the
posterior density relative to `mu` is at least `exp(-2R^2/s)`, producing the
two-copy factor `exp(-4R^2/s)`. Equal masses at `+a,-a`, contracted to zero,
attain the posterior coefficient when `a<=sqrt(s)`, so the coefficient's
sharpness calculation is exact.

### 4. Pair distortion to an optimal rigid motion

Double centering of squared distances gives

    H=AA* - BB* = -(1/2) J Delta J.

Orthogonal projection contracts the Hilbert--Schmidt norm and
`0<=Delta<=4R^2`, hence `||H||^2<=R^2 D`. A polar/SVD alignment may be chosen
even when `A*B` is singular so that it becomes positive semidefinite.
Writing `U=A+B` and `V=A-B` after this alignment gives

    ||H||^2
      = (1/2) tr(U*U V*V) + (1/2) tr((U*V)^2).

Here `U*V=A*A-B*B` is symmetric, making the second trace nonnegative, and
`U*U>=A*A>=kappa I`. This proves
`||H||^2 >= (kappa/2)||A-B||^2` and closes the stated Procrustes estimate.

The independent exact checker specifically exercises this step with a
non-diagonal positive cross-covariance and noncommuting covariance matrices,
as well as a singular aligned cross-covariance. It also exhibits the minimal
two-dimensional warning against omitting alignment: `A=I` and `B` a
quarter-turn have identical Gram operators but positive unaligned error;
the optimal orthogonal factor makes the error zero.

### 5. Optimal exponent

For masses `(1-epsilon)/2,(1-epsilon)/2,epsilon` at `-1,1,2` and clipping
to `[-1,1]`, direct calculation gives pair distortion of order `epsilon`,
squared rigid-motion error `epsilon(1-epsilon)`, and covariance bounded below
by one. The density perturbation argument proves entropy loss
`O(epsilon)` separately for subunit, superunit, Shannon, and infinity
orders; the quantitative lower bound supplies the matching lower order.
Thus root-mean-square error is of order `sqrt(epsilon)`, excluding every
uniform exponent larger than `1/2`. Products with independent symmetric
signs preserve the entropy gap and error while keeping radius and covariance
controlled in each fixed dimension.

## Human premises and completeness reductions

The verdict depends on the following human-checked premises. They were
audited for hypotheses and direction, but not formalized in a proof assistant.

1. Differentiation of bounded-center Gaussian mixtures, the continuity
   equation, and cutoff integration by parts for every fixed `alpha>0`.
2. Entropy additivity under product measures and invariance under ambient
   rigid motions.
3. Monotone convergence for the unnormalized truncations, plus Fatou's lemma
   for the nonnegative dissipation integrand. The proof correctly does not
   claim an exact noncompact dissipation identity.
4. Strict positivity of Gaussian kernels, which turns positive pair
   distortion on a positive-measure set into a strictly positive entropy
   gap.
5. The support identity
   `supp(mu x mu)=supp(mu) x supp(mu)` and the elementary anchor theorem
   extending a distance-preserving support map to an ambient rigid motion.
6. Existence of a mode for a continuous positive density vanishing at
   infinity, differentiation at that mode, and posterior Jensen integrability.
7. Double centering of squared distances and Hilbert--Schmidt contraction by
   orthogonal projection.
8. Polar/SVD alignment in the singular as well as nonsingular case and the
   trace inequality `tr(PQ)>=0` for positive semidefinite matrices.
9. Local Lipschitz control of the finite-order and Shannon entropy
   perturbations in the sharpness family; the displayed Gaussian dominators
   have the required integrability.
10. The qualitative comparison's prior-work boundary and the negative
    literature search for a matching equality/stability theorem.

The proof's completeness split is explicit: finite orders use the lifted
path, infinity uses the mode-posterior argument; compact laws yield an exact
identity, arbitrary laws use truncation and a one-sided lower bound; Shannon
is differentiated directly, while subunit orders use separate denominator
control; singular Procrustes data are covered by SVD; lower-dimensional
supports are covered by affine anchors. Order zero and equality between two
infinite entropies are expressly excluded.

## Adversarial smallest examples

- **Singleton support.** Every map agrees there with some translation, and
  both smoothed laws are translates of the same Gaussian. This checks the
  zero-dimensional endpoint of the anchor reduction.
- **Two atoms collapsed to one.** For equal masses at `+a,-a` and `T=0`,
  pair distortion is positive, so every finite-order dissipation is strict.
  At infinity the same example attains the coefficient `1/(4s)` when
  `a<=sqrt(s)`; strictness and claimed sharpness are therefore compatible.
- **Unbounded countable support.** A law on the positive integers with masses
  proportional to `(1+k)^-2` has infinite first moment. Ball restrictions
  nevertheless increase as unnormalized measures, and all normalization
  factors are displayed. This checks that truncation is not silently using a
  moment estimate.
- **Quarter-turn alignment trap.** Exact `2x2` matrices `A=I` and `B` a
  90-degree rotation have `AA*=BB*` but unaligned error `4`. The optimized
  alignment has zero error. This falsifies the tempting incomplete reduction
  without `Q` and validates why the SVD step is indispensable.
- **Non-diagonal aligned data.** The exact fixture has
  `A*B=[[2,1/2],[1/2,1]]`, which is positive definite and non-diagonal, while
  `A*A` and `B*B` do not commute. Both trace terms in the identity are
  positive and the lower bound holds exactly, avoiding a simultaneous-
  diagonalization assumption.
- **Singular aligned data.** With `A=I` and `B=diag(1,0)`, the aligned cross
  covariance is singular; the Hilbert--Schmidt lower bound still holds. This
  tests the completeness of the SVD reduction at rank loss.
- **Three-point fold.** Exhaustion of all 75 contractions from
  `{-1,0,1}` to the half-integral grid in `[-1,1]` found exactly two
  isometries and 73 strict maps. Every map satisfies the theorem's direct
  bound `error<=3D`; the absolute-value fold has `D=error=8/9`.
- **Order approaching zero.** Both Gaussian mixtures have full support, so
  support-volume entropy at order zero is infinite. The target excludes this
  endpoint rather than inferring it from estimates whose constants degenerate.

## Reproduction and source integrity

The producer's `verify.py` output matched its committed `EXPECTED.json`
byte-for-byte under both `python3` and `python3 -O`; every entry in its
`SHA256SUMS` passed. That package checks 215 path-pair identities, finite
Gram and alignment fixtures, integer-order Gaussian entropy gaps with exact
rational enclosures, invalid-fixture rejection, and the sharpness family.

This review's independent standard-library checker uses exact rational
arithmetic. Its normal and optimized outputs match the committed expected
file. It checks a different non-diagonal/noncommuting alignment surface,
singular alignment, an explicit failed unaligned inequality, and exhaustive
small one-dimensional maps. Program agreement is only corroboration; the
analytic completeness reductions above determine the verdict.

The live source audit inspected:

1. Aishwarya--Li, *Gaussian Convolution, Internal Energies, and the
   Kneser--Poulsen Conjecture*,
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2). Theorem 1.3 and
   the Rényi example contain the current moment-free qualitative comparison.
2. Aishwarya--Li, *The Kneser--Poulsen phenomena for entropy*,
   [arXiv:2409.03664v3](https://arxiv.org/html/2409.03664v3). Theorem 1.5 and
   its doubled path are the earlier comparison and method credited by the
   target.
3. Aishwarya--Alam--Li--Myroshnychenko--Zatarain-Vera, *Entropic exercises
   around the Kneser--Poulsen conjecture*,
   [arXiv:2210.12842](https://arxiv.org/abs/2210.12842), an earlier partial
   result.

The September 2026 preprint already removes the subunit-order moment
condition, so that is not new here. Searches of the exact target title and
combinations of Gaussian entropy, equality, rigidity, quantitative stability,
and the posterior coefficient found no matching primary theorem. This is a
scope check, not a priority guarantee. General Kneser--Poulsen geometry and
higher-dimensional Gaussian majorization remain outside the target.

## Strengthening and improvement opportunities

1. State the harmless replacement `T -> T-T(0)` explicitly before applying
   compact truncations in the arbitrary-law section; it is already implicit
   in translation invariance.
2. Expand the cutoff integration-by-parts paragraph into a lemma with one
   displayed dominating function for each of `alpha<1`, Shannon, and
   `alpha>1`. This is the largest remaining analytic trust surface.
3. Cite a named finite-dimensional Procrustes/polar-decomposition lemma and
   record which side receives the orthogonal factor; the current argument is
   correct but compact.
4. Add the non-diagonal and quarter-turn fixtures from this review to the
   producer checker, since they expose assumptions hidden by diagonal test
   data.
5. A proof-assistant formalization of the lifted differentiation and the
   noncompact Fatou reduction would materially increase assurance. It is not
   required for this acceptance.
