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
including the new damped-cone motion and the all-variance density-orbit
proof for the previously obstructed nine-point family.
[SOURCES.md](SOURCES.md) credits the
classical stochastic-order, Hausdorff and Bernstein--Durrmeyer ingredients.
Those ingredients are not claimed as new. Independent review of this
consolidation and its constants is pending.

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
