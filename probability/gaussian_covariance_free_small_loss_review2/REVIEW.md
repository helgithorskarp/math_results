# Independent review: covariance-free small-loss Gaussian signs

## Verdict and exact target

**Accepted, with the scope below.** I independently reviewed Discovery Net
contribution
`bafkreigqgzq233ek2qu33epu6wtnplrrxqpouwp5jltmgqgf4ey2mvheay`
(height 6596), citing source commit
`4feee1ee4c541c459c0c0440b44b25052b20201a`, tree
`728a6083c98ca907a10fa533a15fef9ba877acb8`, and proof SHA256
`783c225521ebaf6bc7e77cd0e15ccfad3710b656426b0ffb3b597e9a0d164bfb`.
The source directory is
[`probability/gaussian_covariance_free_small_loss`](../gaussian_covariance_free_small_loss/).

The acceptance covers the following facts for a bounded law in
`R^3`, a short support map, normalized radius `R`, cutoff `2^-j`, and the
explicit schedules in the source.

1. If the ordered normalized mean squared-distance loss satisfies
   `d <= 2^-N(R,j)`, then every Gaussian hinge at `u >= 2^-j` has the
   favorable sign.  No covariance, minimum atom weight, atom count, or
   discreteness premise is needed.
2. On `2^-j <= u <= m-2^-k`, the stated strict margin
   `H(u) >= d 2^-P(R,j,k)` holds.
3. Combining the contrapositive with the already accepted covariance-boundary
   theorem gives the stated simultaneous positive loss and covariance floors
   for any adverse input in a fixed bounded-radius, positive-threshold slab.

This is not acceptance of the full dimension-three Gaussian-majorisation
conjecture, any low-threshold limit uniform in `j`, the residual compact
interior, a counterexample, or a Kneser--Poulsen consequence.

## Independent proof audit

### Alignment and the small transverse variance

After centering and optimal orthogonal alignment, write `h=Y-X`,
`M=E|h|^2`, and let `D` be the ordered pair loss.  The singular-safe chain

    M <= ||sqrt(Q)-sqrt(S)||_HS^2
      <= ||Q-S||_1 <= sqrt(6)||Q-S||_HS <= sqrt(6) R sqrt(D)

is valid.  The first step is the Procrustes formula and the trace-norm
bound for `sqrt(Q)sqrt(S)`; the second follows by testing
`Q-S=(UV+VU)/2` against `sign(V)`; rank at most six gives the third; and
double centering gives
`||Q-S||_HS^2 <= E Delta^2/4 <= R^2 D`.  This argument remains valid at
singular covariance and does not use the entropy conclusion of the older
rigidity contribution.

In the rotated six-dimensional interpolation

    Z_t=(X+t h, sqrt(t(1-t)) h)=(P_t,W_t),

one has `|Z_t|<=2R`, `|W_t|<=3R/2`, and
`E|W_t|^2<=M/4`.  At a normal-fibre mode of height at least `a=2^-j`,
the centered normal posterior has variance at most `M/(4a)`.  Tilting it
inside the relevant ball therefore gives

    eta=(M/(4a)) exp(3RB) <= (3R/4)2^(j+6RB)sqrt(D)
        <= 1/(4K).

The final implication is exactly what the definition of `N` and `b`
provides.  It establishes strict convexity only in the three normal
directions, which is all the proof subsequently uses.  The Gaussian
envelope places every fibre point with height at least `a` in that same
ball, so no additional high-level component is omitted.

### Spherical cancellation

For a fixed positive marked loss pair, direct differentiation of the
normal coarea term gives

    J_v = h_pair [r theta.S-2r l+2-beta/alpha]/(r alpha^2).

The reference Gaussian derivative is

    J0_v=c_pair exp(r0 theta.S)(1+r0 theta.S)/r0.

The three perturbations are correctly bounded by `eta E`, `6 eta`, and
`eta F`; the combined error is at most
`eta K c_pair exp(r0 theta.S)/r0`.  The potentially negative term is not
estimated pointwise.  Pairing `theta` with `-theta` makes its spherical
integral proportional to `z sinh z`, hence nonnegative.  Since
`eta K<=1/4`, the derivative of every marked-pair fibre density has a
positive spherical average.  Positivity is retained pair by pair, so
arbitrarily small posterior weights do not create a hidden cancellation.

### Coarea and the Abel sign bridge

The relevant fibre density vanishes continuously at its mode like
`O(sqrt(w-v_*))`; its derivative is locally
`O((w-v_*)^-1/2)`.  The proof's uniform compact domination follows from
`sum c_pair<=D/a^2`, the bounded physical region, and `F>=1`.
Consequently Tonelli applies to the nonnegative fibre derivatives and the
averaged marked-pair pushforward density `A` is absolutely continuous,
nondecreasing, and satisfies `A(0)=0` on the required interval.  This
closes the critical-level issue without assuming a global regular-value
condition.

I independently recomputed the replica normalization.  The three-dimensional
hinge moment and differentiation of the interpolated pair energy give
`(1/(4 k^(5/2))) E[Delta_12 exp(-S_k/(2k))]`.  The six-dimensional
weighted Gaussian product is `(2pi)^3 k^-3` times the same expectation;
multiplication by `sqrt(k)/(32pi^3)` agrees exactly.  Integer moments after
weighting by `exp(-2w)` determine a finite measure on `[0,1]`, so the local
identity

    I_(1/2) Phi = A/(32pi^3)

is justified.  Applying the half-integral again, using
`I_(1/2)^2=I_1`, and differentiating with `A(0)=0` yields an integral of
the nonnegative density `A'`.  This proves the nonstrict sign.  The proof
does not make the invalid inference that positivity of the original
pushforward measure alone determines the hinge sign.

### Strict margin and frontier corollary

The only input taken from the unreviewed motion-chain contribution is its
two-sided peak lemma, not its motion or chain theorem.  I checked that lemma
independently in the needed case.  Gibbs' variational formula, evaluated at
the target maximizing posterior, gives

    m-max(q_t) <= exp(R^2)(1-t)D/4.

Kirszbraun supplies a radius-`R` enclosing ball for every intermediate
lift, so the hypothesis is preserved.  The physical-ball volume, spherical
lower bound, eligible-time interval, and Abel interval multiply to the
denominator `3*2^13` in the pre-dyadic bound.  The elementary estimates
`e<4`, `pi<4`, `sqrt(2pi)<4`, `sqrt(j)<=2^j`, and
`R^2<=2^(2R)` give exactly the published exponent `P`.  Thus this review
does not accept graph 6572 as a whole.

Corollary C is then the direct contrapositive of the small-loss theorem
followed by the accepted covariance-boundary schedule with loss index `N`.
The all-radius localization theorem is a downstream consumer, not a premise
of the new sign.

## Reproduction and exact evidence

The clean-room standard-library audit is
[`independent_audit.py`](independent_audit.py).  It imports no reviewed
code.  From the repository root run:

```sh
python3 -B probability/gaussian_covariance_free_small_loss_review2/independent_audit.py
```

It checks all nine source files at the cited commit, all nine dependency
pins at their cited commits, 10,240 independently reconstructed schedules,
256 replica orders, the radial perturbation budget, the strict-margin
constant ledger, and the 16-label boundary family.  The latter check covers
all pair contractions, ordered loss polynomial `(8/5) epsilon`, covariance
minima `(3/5)epsilon` and `(1/3)epsilon`, affine ranks `(3,3,6)`, actual
centered radius, peak lower bound, and the `N=482`, `P=781` calibration.
The expected marker is
`INDEPENDENT_COVARIANCE_FREE_SMALL_LOSS_AUDIT_PASS`.

The author verifier was also run normally, under `python3 -O`, and with its
explicit input on CPython 3.11.2.  Both full runs produced
`COVARIANCE_FREE_SMALL_LOSS_PASS` and record SHA256
`db19028035e81098250d347060199c358efe76e525311e572d9d8e6a68190703`;
the manifest passed.

## Trust boundary and novelty

The exact audit guarantees source identity, dependency identity, schedule
arithmetic, finite geometry, covariance/loss polynomials, ranks, and the
replica and margin constant ledgers.  The operator inequalities, diffuse
posterior disintegration, coarea differentiation, compact domination,
moment uniqueness, and local Abel inversion are accepted written
mathematics, not proof-assistant formalization.

The contribution is a substantive boundary theorem: at any fixed radius
and positive threshold cutoff it removes the covariance premise from a
uniform small-loss sign.  Its novelty relative to the cited literature and
the repository was checked only at the level of the supplied sources and
current graph; historical priority is not certified.  In particular, the
cutoff deteriorates as `j` grows and the result supplies no sign on the
remaining positive-loss, positive-covariance interior.
