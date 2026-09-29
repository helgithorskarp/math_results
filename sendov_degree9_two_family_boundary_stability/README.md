# Degree-nine first-power boundary stability

Agent: **six-sendov-2**. Role: **researcher**. Ordinary written proof with
exact algebra checks; independent review of this contribution is pending.

Let a degree-nine polynomial have all roots in the closed unit disk and a
distinguished root `a` on the unit circle. For the critical points, counted
with multiplicity, suppose the first-power deficit is finite and

\[
 \tau=\frac18\sum_{j=1}^8|a-\zeta_j|^{-1}-1\le10^{-10}.
\]

Then `tau>=0`, and the roots admit an anchored bijective matching to one of
the two known first-power equality configurations:

| Branch | Original-root maximal matching error | Critical-point conclusion |
| --- | --- | --- |
| Regular nonagon `a exp(2 pi i k/9)` | `2500 tau` | `sum |zeta_j|^2 <=693000 tau` |
| Collapsed `a,-a,...,-a` | `800 sqrt(tau)` | Error `52 sqrt(tau)` to seven copies of `-a` and one `7a/9` |

More precisely, the regular error is at most
`300 D +2500 (77000 tau)^(5/2)`, where
`D=sum_{k=1}^8 (1-|z_k|^2)/|a-z_k|^2` is the weighted radial defect.
If every original root lies on the unit circle, `D=0` and the regular error
improves to `2500 (77000 tau)^(5/2)`. The root exponents `1`, `1/2`, and
the restricted `5/2` are sharp. The collapsed square-root exponent remains
sharp even with all original roots on the unit circle.

The [complete proof](PROOF.md) quantifies the previously known boundary
equality classification. Its new structural bridge is

\[
 L(7-L)\le300000\tau,\qquad
 L=e_2\bigl(|1-\zeta_1/a|^{-1}-\tfrac12,\ldots,
                 |1-\zeta_8/a|^{-1}-\tfrac12\bigr).
\]

The regular branch has `L>=1` and quadratic deficit at most `77000tau`.
The collapsed branch has `L<1` and `L<=50000tau`; direct reciprocal
other-root energy controls the roots despite their limiting multiplicity.
The proof retains both families. First-power equality at the collapsed
family has quadratic deficit `7/4`, so treating all first-power
near-equality configurations as near the regular nonagon would be false.

The regular branch uses [earlier quadratic energy stability](../sendov_degree9_boundary_stability/proof.md).
Its radial interpolation extends the coefficient argument of
[the independent unit-circle refinement](../sendov_degree9_boundary_stability_review2/REFINEMENT.md).
The exact Newton certificate was developed in
[the preceding effective-annulus proof](../sendov_degree9_effective_boundary_first_power/PROOF.md).
See [LITERATURE.md](LITERATURE.md) for status, provenance and prior-art limits.
The full interior first-power Tang–Zhang conjecture remains unresolved here.

## Reproduce

From the repository root, with CPython 3.10 or later (tested with 3.11.2):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 sendov_degree9_two_family_boundary_stability/verify.py
```

Expected output:

```text
PASS: 355 exact checks; 3 certificate mutations rejected.
```

The checker is self-contained standard-library Python using rational
arithmetic. It checks all 266 monomial coefficients of the Newton identity,
the reciprocal, energy and paired-coefficient identities, exact radial
interpolation and matching constants, three sharpness
family factorizations, unit-circle root certificates and equality controls.
The universal analytic estimates and the cited stability inputs are written
proof; Python does not formalize them. No floating-point roots, solver,
private data, external certificate, or large generated artifact is used.
