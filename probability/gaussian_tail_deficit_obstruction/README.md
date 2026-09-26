# Gaussian tail correction: a stability obstruction and a signed zero test

A small entropy gap or mean distance deficit cannot uniformly control the
error in the team's spherical approximation to Gaussian hinges. This packet
proves that obstruction for actual injective contractions of two atoms,
and derives the next signed term relevant to the unresolved spherical-zero
case. **The two-atom examples satisfy majorisation.** The negative quantity
is an approximation error, not a hinge gap.

Let `gamma_s` have covariance `s I_3`, put `C_s=(2 pi s)^(-3/2)`, and set

```text
H_f(a) = integral (f-a)_+,
S_mu(lambda) = spherical average of log E_mu exp(lambda theta.X),
J = S_mu-S_nu,
a = C_s exp(-lambda^2 s/2),
N_s(lambda) = [H_(nu*gamma_s)(a)-H_(mu*gamma_s)(a)] / (4 pi lambda s^2 a).
```

Fix **any** `s>0,R>0`. Take `p_m=2^-m`, `lambda_m=2m log(2)/R`, and

```text
mu_m = (1-p_m) delta_0 + p_m delta_(R e_1),
nu_m = (1-p_m) delta_0 + p_m delta_(R e_1/4).
```

The fixed map `T(x)=x/4` is injective and strictly contracting. Nevertheless,

```text
s [N_s(lambda_m)-J(lambda_m)] -> -R^2/16,
D_m = E[|X-X'|^2-|TX-TX'|^2] = 15 p_m(1-p_m) R^2/8 -> 0,
0 <= h(mu_m*gamma_s)-h(nu_m*gamma_s) <= p_m(1-p_m)R^2/(2s) -> 0.
```

Thus no vanishing modulus of either deficit can replace the existing
support-scale error uniformly over laws and thresholds. The proof takes
the moving-weight limit directly at fixed variance; it does not exchange
it with a fixed-law high-variance expansion.

For a fixed bounded law, [Theorem B](PROOF.md) separately proves a uniform
expansion on each compact positive `lambda` interval:

```text
N_s(lambda) = J(lambda) + [C_mu(lambda)-C_nu(lambda)]/s + O(s^-2).
```

The explicit functional `C` uses only the log moment-generating function
and tilted first and second moments. A zero of `J` with negative correction
would give actual Gaussian counterexamples at all sufficiently large
variances. A nonnegative `J` with positive correction at every positive zero
completes eventual full majorisation for finite noncongruent contractions.
No unresolved contraction meeting either new zero condition is supplied.
The full dimension-three conjecture and new Kneser--Poulsen cases remain open.

- [Proof, explicit coefficient, and exact assumptions](PROOF.md)
- [Primary and team dependencies; scope](SOURCES.md)
- [Exact algebra checker](verify.py)
- [Expected audit record](EXPECTED.json)

From the repository root, using CPython 3.11 or later and no packages:

```sh
python3 probability/gaussian_tail_deficit_obstruction/verify.py --check
python3 -O probability/gaussian_tail_deficit_obstruction/verify.py --check
cd probability/gaussian_tail_deficit_obstruction
sha256sum -c SHA256SUMS
```

Expected output:

```text
PASS e7ecfe2733f9e032bdfba4ef3b8bfeac3eb8995330a3126f41435888d43ad18b
```

Checked with CPython 3.11.2 and 3.12.14. The standard-library checker uses
exact rational Laurent polynomials for twelve identities, exponential
moments, a rational strict-sign certificate, and two invalid controls.
Finite fixtures supplement the symbolic identities. No floating-point
quadrature, solver, large artifact, or external package is required.
The analytic limits and uniform remainder bounds rest on the written
proof, not these checks. Independent mathematical review and formalization
are pending.
