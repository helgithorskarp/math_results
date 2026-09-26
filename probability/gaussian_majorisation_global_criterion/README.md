# One global criterion for three-dimensional Gaussian majorisation

For a bounded law `mu` in `R^3`, its contraction image, and a fixed Gaussian
variance `s`, this packet identifies the largest failed hinge comparison
with two equivalent quantities:

1. The least failure probability in an endpoint coupling of the two
   five-dimensional Gaussian-smoothed density values.
2. The increasing limit of explicit finite differences of Gaussian
   replica moments, with a uniform error bound over **all** thresholds.

The zero value is exactly full majorisation at this variance. The result
consolidates the team's motion, relabelling, common-target, density-orbit,
Hankel and eventual-majorisation mechanisms into one criterion. It does not prove
that this value is zero for every three-dimensional contraction.

Write `H(u) = integral(g-Cu)_+ - integral(f-Cu)_+`, where
`C=(2*pi*s)^(-3/2)`, and let `Delta=max(-H)_+`. Define

```text
a_j = C integral[(g/C)^(j+2)-(f/C)^(j+2)] / ((j+1)(j+2)),
b_Nk = (N+1) binom(N,k) sum_(l=0)^(N-k) (-1)^l binom(N-k,l) a_(k+l),
D_N = max(0, -min_k b_Nk).
```

Then `D_N` increases to `Delta`. If both supports can be translated into
balls of radius `R`, put `r=R/sqrt(s)` and

```text
K = 2 sqrt(2/pi) [r^3/3 + sqrt(pi) r^2 + 4r + 2sqrt(pi)].
```

For every integer `N>=0`,

```text
D_N <= Delta <= min(1, D_N + K (N+2)^(-1/4)).
```

Any negative `b_Nk` gives a finite convex-energy counterexample certificate.
Finite nonnegative tests give an error bound, not an exact zero certificate.
No such negative Gaussian-contraction certificate is provided here.

[PROOF.md](PROOF.md) proves the identities, coupling minimum, monotonicity,
error bound and closure rules. [DEPENDENCIES.md](DEPENDENCIES.md) maps the
actual geometric classes and analytic mechanisms to this criterion,
with an implication diagram and separate accounts of full-question
equivalences, broad geometric classes, stability and restricted examples.
It preserves lane ownership and distinguishes proof dependencies from
comparisons that merely exclude a particular method.
[SOURCES.md](SOURCES.md) credits the
classical stochastic-order, Hausdorff and Bernstein--Durrmeyer ingredients.
Those ingredients are not claimed as new. Independent review of this
consolidation and its constants is pending.

For the eight-lane campaign, start with [INTERFACES.md](INTERFACES.md).
It connects the fixed-atom reduction to the measure lane's common-set
dual, preserves the anchor compensation term and prior quantifiers, and
gives an explicit error budget for transferring a conditional strict
witness to finite data and the map lane's rigid meshes while retaining
the prescribed dominant atom. It records the finite-atomic lane's new
finite-averaging obstruction without treating it as an integrated
counterexample. This handoff adds no theorem or comparison family.

The later [geometric-endpoint annex](GEOMETRIC_LIMIT.md) specifies the
normalized coupling defect needed along an exponential weight path to
obtain an unequal-radius ball inequality. It also completely classifies
the logarithmic profiles allowed by the orbit theorem's two fixed weight
cones: `lambda_0=lambda_2=lambda_3>=lambda_1`. Every resulting radius
pattern already has a coordinate-preserving relabelling proof. This is a
precise requirement for extending the functional certificate toward a new
volume class; it is not a counterexample or a new Kneser--Poulsen theorem.

That positive extension obligation has now been met for a new restricted
ray class by the team's
[ordered-weight source](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md).
Its new certificate allows unbounded ordered weight ratios and proves
ordered unequal-radius **union** comparisons, even for invariant ambient
measures. The old fixed-cone classification is unchanged. The new result
does not cover arbitrary weights, unordered radii, or intersections; its
exact ray and measure-order hypotheses remain essential. Independent
review of that computer-assisted author proof is pending. The handoff
records how it differs from the domain-wide motion classes and from
law-dependent spatial stability; this update claims no new theorem.
It also includes the latest
[transverse matrix-path principle](../gaussian_axial_cone_rotations/MATRIX_PATHS.md),
which generalizes the old axial rotation while keeping undamped endpoints
and unrestricted weights and radii. Its block-diagonal optimality statement
is kept separate from the unrestricted majorisation question.

The [fixed-atom reduction](ANCHOR_REDUCTION.md) gives an equivalent test
class for the **full** conjecture. For any one fixed `0<epsilon<1`, it is
enough to prove comparison at variance one for every bounded law
`(1-epsilon) delta_0+epsilon rho` and every contraction fixing zero. The
support bound on `rho` is not uniform. A translated rare packet and a
distant common fixed atom give, uniformly in every threshold,

```text
|Delta(F_R,G_R)-epsilon Delta(f,g)|
    <= exp(-(R-M)^2/(8s)).
```

Thus any possible violation would persist arbitrarily close to the same
Gaussian in total variation, every finite Wasserstein distance, each
fixed derivative norm and relative entropy. This is a conditional
reduction; no violation is asserted, and the fixed-atom test is not yet
proved. It specifies the uniform local-to-global obligation for the
analytic and entropy routes. The updated dependency map preserves the
stronger all-weight geometric classes and the bounded-law stability
theorem's distinct support-sensitive hypotheses.

## Reproduction

From this directory, using CPython 3.11 or later, with no packages:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected checker output (verified with CPython 3.11.2):

```text
GLOBAL_CRITERION_EXACT_AUDITS_PASS 629989532f37a348dc848ac6251939ca7132291b9c0b388dba207b27b801846d
```

The checker compares the moment finite differences with direct exact
integration, checks the degree-elevation and variance identities, and
compares cyclic quantile couplings with exhaustive assignment optima for
3,136 pairs of finite scalar laws. Positive, negative and invalid controls
are included. `EXPECTED.json` is compact and deterministic; `--check`
rejects any mismatch and remains active under `python -O`.

These are supplementary algebra and normalization checks. They do not
constitute independent mathematical review, verify arbitrary Gaussian
moment data, or prove the open conjecture. The universal argument is the
written proof, including measure disintegration and its credited motion
theorem. No solver, floating-point computation, external dataset, or large
certificate is required.

For the annex, also run:

```sh
python3 geometric_limit_audit.py --check
python3 -O geometric_limit_audit.py --check
```

Expected:

```text
GEOMETRIC_PROFILE_CLASSIFICATION_PASS 97cccdd40fc962b778df43ed06468a19d2d3cb61cdb6a32017260e07b15f1ee1
```

The exact digest is recorded in the annex's reproduction record. This
audit reads the original orbit order certificate by its relative path in
the same repository and verifies its SHA256 before use; it checks all
366,660 endpoint coefficient inequalities and the eleven selected ratio
constraints. See [GEOMETRIC_LIMIT.md](GEOMETRIC_LIMIT.md) for the analytic
proof, dependency and scope. The original global-criterion audit is unchanged.

For the fixed-atom annex:

```sh
python3 anchor_audit.py --check
python3 -O anchor_audit.py --check
```

Expected:

```text
FIXED_ATOM_REDUCTION_EXACT_AUDITS_PASS 218fbb2cbe4e4163e93bd58d5422e023f382e110c381470ab7079061d84c44dd
```

This supplementary rational audit checks the hinge interaction, mixture
normalizations and a concrete contractive extension. The universal
separation and localization statements are analytic proofs. Its negative
finite-cell control is not a Gaussian-contraction example.
