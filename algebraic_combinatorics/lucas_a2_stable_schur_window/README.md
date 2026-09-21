# A stable Schur-positive window for every canonical Lucas `a=2` comparison

This directory proves a parameter-uniform partial result for the Lucas
Bergeron--Vessenes conjecture.  Let

```text
F_0=0, F_1=1, F_(n+1)=e1 F_n+e2 F_(n-1)
```

and write `{n choose k}_F` for the associated Lucas binomial.  If

```text
3 <= b <= c,  bc is even,  d=bc/2,
D_(b,c)={d+2 choose 2}_F-{b+c choose b}_F,
```

then, with `N=bc`,

```text
[s_(N-r,r)] D_(b,c) = 0  for 0 <= r <= 2,
[s_(N-r,r)] D_(b,c) > 0  for 3 <= r <= c.
```

Thus the full pre-numerator window of the entire canonical `a=2` cone is
Schur-positive.  In particular, the first nonzero coefficient is exactly
`[s_(N-3,3)]D_(b,c)=1`.

The proof is in [THEOREM.md](THEOREM.md).  Its main new ingredient is an
at-most-two-to-one map from nonconstant partitions of an even integer using
parts in `{2,...,b}` to partitions of the preceding odd integer.  This gives
the adjacent-layer inequality required by the Lucas anti-involution, without
fixing `b` or using quasipolynomial case splits.

## Reproduction

Only CPython 3.11 or newer and the standard library are required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I \
  algebraic_combinatorics/lucas_a2_stable_schur_window/verify.py

PYTHONDONTWRITEBYTECODE=1 python3 -I \
  algebraic_combinatorics/lucas_a2_stable_schur_window/verify_direct.py

(cd algebraic_combinatorics/lucas_a2_stable_schur_window && \
  sha256sum -c SHA256SUMS)
```

The first checker audits the restricted-partition map entry by entry, checks
the Gaussian layer formula, and verifies every adjacent block in a bounded
grid.  The second checker is independent of that decomposition: it constructs
Lucas polynomials from the defining recurrence, forms literal factorial
quotients in `Z[q]` after setting the second variable to one, and extracts the
two-variable Schur coefficients by first differences.  Expected output is in
`EXPECTED_OUTPUT.txt`.

The theorem is universal because of the written injection and symmetric-
function proof, not because of the finite audit ranges.

## Scope

The result does not prove the remaining coefficients with `r>c`, and hence
does not settle the all-`b` canonical `a=2` family.  It replaces the fixed-
width machinery only before the first Gaussian numerator activation.  Later
layers contain signed translates and require an additional structural idea.

All computations are exact.  There is no floating point, randomness, solver,
CAS, external data, or generated proof certificate.  The computational trust
boundary is CPython's arbitrary-precision integer arithmetic and inspection
of the two small implementations.

## Primary context

- Francois Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979:
  <https://arxiv.org/abs/2608.30979>.
- Bruce Sagan and Carla Savage, *Combinatorial interpretations of binomial
  coefficient analogues related to Lucas sequences*, arXiv:0911.3159:
  <https://arxiv.org/abs/0911.3159>.
- Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187:
  <https://arxiv.org/abs/1709.06187>.
