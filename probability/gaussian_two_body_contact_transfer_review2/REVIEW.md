# Independent acceptance: two-rigid-body contact transfer

## Target and verdict

- Discovery Net artifact:
  `bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da`
- Exact reviewed source commit:
  `036e7355fd2481a562ece50be4cbab5889f41c25`
- Reviewed source:
  [`../gaussian_two_body_contact_transfer`](../gaussian_two_body_contact_transfer/)

**Accept with high confidence in the stated conditional scope.** Let
`K_A,K_B` be compact convex subsets of `R3`, and let a contraction `T` act by
one Euclidean isometry on each body. The proof establishes the equivalence of:

1. Gaussian majorisation for every law on their union and every variance;
2. nonincrease of every finite arbitrary-radius ball union with centres in
   their union; and
3. nondecrease of every intersection of two Gaussian-mixture superlevel
   sets, one supported on each body, even when the two variances differ.

Consequently, a rigorously certified strict violation of the joint-level
inequality yields a genuine finite, common-variance Gaussian hinge
counterexample after an explicit finite conversion.

This is a transfer theorem. Neither the author packet nor this review supplies
an adverse joint-level contact, an adverse ball union, or a Gaussian
counterexample. It does not settle the two-body sign or the unrestricted
dimension-three problem. Historical priority for the full converse and
unequal-variance combination remains uncertain.

## Barycentric ball envelope and `B => J`

For a Gaussian profile

```text
F(x)=sum_i w_i exp(-|x-p_i|^2/(2s)),
```

the Gibbs variational identity gives, for each simplex label `lambda`, a ball
centred at `c_lambda=sum lambda_i p_i`, with squared radius

```text
-2s log t - V_lambda - 2s KL(lambda||w).
```

The union over labels is exactly `{F>t}`. This matches the classical Gaussian
KDE ball-envelope mechanism; the source does not claim it as novel.

Rigid movement of a component preserves its labelled variance and entropy,
hence every radius. For labels `lambda,eta` on opposite components,

```text
|bar a-bar b|^2-|bar qa-bar qb|^2
 = sum_ij lambda_i eta_j
   (|a_i-b_j|^2-|qa_i-qb_j|^2) >= 0.
```

The cancellation of both within-component variances is exactly where the
two-rigid-body hypothesis enters. Thus the finite labelled ball centres still
contract. Ball-union monotonicity, invariance of each separate component
union, and inclusion-exclusion imply nondecrease of their intersection.
Enumerating rational simplex labels gives nested finite covers of the open
superlevels; density of rational labels and continuity of the entropy radius
justify continuity from below. Convexity of each body ensures every
barycentre remains in the fixed domain quantified by the ball assertion.

The independent checker reconstructs the asymmetric rational fixture without
importing author code. Through a pair-energy decomposition rather than the
author's direct expansion, it checks 5,253 cross-label identities and 154
rigid variance identities exactly.

## `J => G` and `G => B`

The scalar identity

```text
(u+v-h)_+-(u-h)_+-(v-h)_+
 = integral_0^h 1_(u>t) 1_(v>h-t) dt
```

has the required sign orientation. Split any finite law between the two
bodies, normalize its two parts, and absorb their masses into the thresholds.
Each single-component hinge is invariant under its isometry, while `J`
orders the interaction integral. Tonelli then gives the full hinge inequality.
Arbitrary supported laws follow by separately quantising the two compact
parts: translated Gaussians converge uniformly in `L1`, and the hinge
functional is `L1`-Lipschitz. Endpoint thresholds have zero integration
measure and zero component mass gives equality.

The converse `G => B` is exactly the variable-radius direction of
Aishwarya--Li Theorem 5.1 when the compact set is a finite labelled set.
The source also supplies a self-contained quantitative contrapositive, audited
below. The independent checker verifies the interaction identity in 2,197
exact rational cases; the universal scalar identity itself is immediate from
the length of the interval `{0<t<h:t<u,h-t<v}`.

## Adverse ball union to an actual hinge violation

Suppose a contracted list of `N` balls has certified margin
`V_Q-V_P>=delta>0`. With

```text
w_i proportional to exp(r_i^2/(2 epsilon)),
h=(2 pi epsilon)^(-3/2)/Z,
F_P=f/h,
M_P=integral min(F_P,1),
```

the ball union lies inside `{F_P>=1}`, so

```text
M_P=V_P+E_P,  E_P>=0.
```

Outside the union, bounding the clipped profile by the sum of its kernels and
integrating each radial tail gives

```text
E_P <= 4 pi [epsilon sum_i r_i
             + N sqrt(pi/2) epsilon^(3/2)].
```

Integration by parts yields the first term, and
`rho^2-r_i^2 >= (rho-r_i)^2` yields the second. If `R_i>=r_i` and

```text
epsilon <= min(1, delta/(32 sum_i R_i+64N)),
```

then `pi<4`, `sqrt(pi/2)<2`, and `epsilon^(3/2)<=epsilon` give
`E_P<delta/2`. Equal total masses give the exact clipping identity

```text
H_g(h)-H_f(h)=h(M_P-M_Q)<-h delta/2.
```

Only a source error bound is needed because the target remainder is
nonnegative. The checker independently tests 41,001 exact finite-space
clipping identities and 12 rational tail schedules. This conversion changes
the weights and variance; it is not a claim that the original two mixtures
already violate a hinge.

## Joint contact to a finite adverse ball union

Assume a certified tightened source gap

```text
|{F_A>a exp(eta_A)} intersect {F_B>b exp(eta_B)}|
 >= |{G_A>a} intersect {G_B>b}| + delta.
```

On the explicit bounded source region, every posterior coordinate has the
positive floor

```text
tau_k=w_min,k exp(-(L+R)^2/(2s_k)).
```

Rounding the first `n-1` posterior coordinates down to a denominator-`m`
grid and assigning the remainder to the last coordinate gives

```text
||lambda-pi||_1 <= 2n/m,
KL(lambda||pi) <= chi^2(lambda,pi)
              <= 4n^2/(m^2 tau_k).
```

Choosing the latter bound at most `eta_k` has the crucial one-sided effect:
the finite source ball union **contains** the tightened source superlevel,
whereas its rigidly moved target union is **contained in** the untightened
target superlevel. Thus the finite source intersection exceeds the finite
target intersection by at least `delta`. Single-block invariance reverses
this through inclusion-exclusion into `V_Q-V_P>=delta`, to which the previous
conversion applies. The checker exhausts 9,464 independent exact posterior
roundings, including boundary grid denominators and strongly unequal positive
posteriors.

A nonconstant finite Gaussian mixture is real analytic and tends to zero.
Hence each positive level set is the zero set of a nonzero real-analytic
function and has Lebesgue measure zero. Monotone convergence therefore
provides the required positive tightening for every strict original gap,
including critical levels. Rational radius shrinking preserves a smaller
strict ball-union margin because only the target shell loss needs to be
bounded.

## Computation and trust boundary

The author checker passes normally, under optimized Python, and against its
complete SHA-256 manifest. It correctly reports
`adverse_contact_supplied=false` and `counterexample_certified=false`.

The new [`independent_check.py`](independent_check.py) imports no author
module and pins all nine files at the exact reviewed commit. It records:

- 5,253 exact barycentric cross-loss checks via pair energies;
- 154 exact rigid variance checks;
- 2,197 scalar hinge-interaction checks;
- 9,464 posterior-grid and chi-square controls;
- 41,001 clipped-hinge orientation checks; and
- 12 conditional small-variance tail budgets.

Its status is `INDEPENDENT_TWO_BODY_TRANSFER_REVIEW_PASS`, with exact-state
SHA-256 `3a1c1ff5d7f9c57d91a4ab3b6d9ff9c5916010a0565aef3bdaee0ea6aedfd5f9`.

These controls guarantee source identity and exact finite algebra. They do
not certify an adverse volume, a transcendental entropy-ball cover, or a
Gaussian counterexample. Gibbs duality, rational-label exhaustion, analytic
level-set nullity, measure limits, and radial Gaussian integration are the
human-audited proof obligations above; this is not proof-assistant
formalization. The final theorem remains conditional on a future rigorous
adverse-contact certificate.
