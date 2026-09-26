# Validation and trust boundary

PROOF.md establishes the self-contained small-variance endpoint under
explicit geometric and weight hypotheses. ALL_VARIANCES.md combines it
with three credited theorems to obtain a spatial neighborhood valid at
every variance. Its radius is proved positive but has no certified numerical
value. The new checker is supplementary; it does not establish either
continuum theorem solely by executable assertions.

## Exact checks

`verify.py` uses Python arbitrary-precision integers and `fractions.Fraction`.
It verifies:

- All 18 allowed five-bit section memberships for the union identity.
- The inscribed-ball slack 123/40000 and the infinite-radius box budgets.
- The low-threshold margin 1/2000000 - 2080/10^10 = 73/250000000.
- Every rational norm, slab, log-concavity, coarea-band, and anchor budget.
  The negative exponent is 261/400, positive exponent 13/25, and their
  strict separation is 53/400. The signal ratio lower bound is 5*10^12,
  exceeding the required 8192000.
- Exact polynomial identities in epsilon for the sheared geometry,
  including all cross dot products and the four dual vertices. Coefficient
  bounds enclose the polynomials for every real |epsilon| <= 1/1000.
  Rational endpoint and central fixtures are extra controls, not the
  reason the whole interval is covered.
- Inclusion of every probability vector in the stated L1 neighborhood,
  and an exact squared-angle distinction from the original centered rays.
- Invalid geometry and core mass are rejected, an excessive variance fails
  the low-threshold budget, and an excessive spatial displacement fails the
  high-variance spherical budget.
- The all-variance assembly has exactly the claimed constants: displacement
  1/16384, spherical junction 32, uniform perturbed gap 1/256, and
  high-variance cutoff 45056. Norm and anchor bounds persist under
  displacement 1/1000, and the compact stability weight class contains the
  chosen radius-1/25000 ball. No code supplies the existential middle radius.
- Throughout every nonzero shear in the full interval, its new squared
  angle is in (1/5,1/3) and equality with 1/4 would force e(4+e)=0.

The canonical audit hash in README.md and EXPECTED.json identifies the
finite output. It is not a substitute for rerunning the checks. The
`--write-expected` flag regenerates that small record; ordinary execution
compares it exactly and raises an error on a mismatch. All checks remain
active under `python -O`.

The checker passed on CPython 3.11.2 in normal and optimized modes, and
CPython 3.12.14 in normal mode. An intentionally corrupted expected record
was rejected under optimized Python. The source manifest was checked after
the final edits. No packages, solver, floating-point signs, external input,
large generated artifact, or proof assistant is required for this checker.
The separate essential spherical certificate uses Arb, as described below.

## Analytic obligations

The universal proof still requires ordinary mathematical review of:

1. The geometric section comparison and its uniform volume lower bound.
2. The Gaussian-tail and annulus bounds at arbitrarily low thresholds.
3. The antipodal convexity comparison and thin-slab localization.
4. The strong log-concavity and radial coarea estimate, including critical
   levels, and the first-derivative identity for the hinge on the origin ball.
5. Combining the possible negative origin contribution with the separated
   positive anchor contribution, uniformly in the variance and threshold.

All five arguments are written explicitly. No sampled Gaussian integration
or finite moment hierarchy is used to infer their signs. Replaying the same
checker on a second Python version is portability validation, not an
independent proof. Neither this document nor a review of an earlier team
artifact constitutes independent review of the present theorem.

## Essential borrowed finite certificates for the all-variance completion

These inputs were replayed from their own source, rather than copied into
this contribution. The complete statements and analytic bridges were read.

| Certificate | Successful reproduction digest |
|---|---|
| Square-cone orbit matching | `1e7e83d7ba23776bdf657773a71ba1ab3bbb8cc21c94a2b299cb4d36ce748d6e` |
| Separate all-upper-set algorithm | `7c3cbe320451a160565545d9d7d46ec7a03e4ec000a37c78fef941592ab8a311` |
| Spatial stability strictness inputs | `21fe6f1848494e490d45fff26a015f9c36084d6bf681c74b149a7db610c64b47` |
| Asymmetric spherical gap | `fb297e46742dfd051089d0198e0d992f658523fd47afc025bee61ee837cb2897` |

The first three use exact standard-library arithmetic and were replayed on
CPython 3.11.2. The spherical certificate was replayed on CPython 3.12.14
with python-flint 0.9.0, using 128-bit Arb balls on 1024 cells and 26 knots.
It recertified the compact interpolation bound 1290469/128000000 and the
analytic infinite tail. The original source also documents an alternative
192-bit equal-height partition; we did not rerun that optional check here.

The external trust boundary is the exact orbit correlation and strictness
certificates, Arb's enclosure arithmetic and the cubature error proof,
the spatial stability/compactness theorem, and the reviewed eventual-endpoint
transfer with its analytic dependencies. These are essential premises of
ALL_VARIANCES.md; they are not premises of the small-variance theorem in
PROOF.md. Replays are not independent peer review. The existing acceptance
of the eventual-endpoint theorem does not review our new proof.
