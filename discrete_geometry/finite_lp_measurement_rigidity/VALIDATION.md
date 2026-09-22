# Reproduction and evidence boundary

From this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Both executions must match `expected.json` exactly and end with `VERIFIED`.
The program writes no files and needs only the Python standard library.
The optional `--dump` flag prints a computed summary without comparing it
to the saved summary; it is for inspection, not the normal verification
command. CPython 3.11.2 was used on 2026-09-22.

The exact audit includes:

| Cases | Check |
|---:|---|
| 21 | Spherical moment formula against circle Fourier coefficients and the uniform coordinate law on S^2 |
| 216 | Zonal support variations in dimensions 2 through 10: positive curvature, volume differentiation, pointwise linearization, integration by parts and the classical gap |
| 1,008 | Normalized Lp density variations, including p=3/2 and p=d; both the full polynomial identity and the integrated volume differential |
| 36 | Constant variations at the scale-critical exponent |
| 860 | Exact nonconstant ball eigenvalues, with the normalization and coercivity signs |
| 11 | The excluded p=1 translation-kernel control |
| 192 | Rational checks of the curvature bracket for even p=2 through 128 |
| 4,160 | Degree cases exhausting all planar monomial weights below the chosen p |
| 64 | The first admitted nonzero weight at degree p |
| 15 | Quadratic affine covariance from direct polygon edge sums and shoelace areas |
| 3 | Distinct rationally rotated squares with identical volume and quadratic tensor |
| 1 | Positive-square-root whitening of a rectangle |
| 5 | Rejected wrong signs, missing/extra volume factors, missing normalization, and invalid polynomial input |

Integers and `fractions.Fraction` are used throughout. The zonal determinant
is computed as the product of its meridional and latitudinal radii; its
direct variation is compared coefficient by coefficient with the
differential-operator formula. Spherical monomials are integrated by an
exact recurrence. Tests include nonspherical supports, nonunit volume,
odd and even variation functions, and the critical exponent. Odd variations
audit the underlying calculus more broadly than the symmetric theorem.

For polygon controls, unit-normal lengths cancel in each edge contribution
to the quadratic matrix. Thus this separate calculation uses no square
roots or floating-point geometry. Every compared entry must agree; an
aggregate count is not used as a substitute for entrywise checking.

The normal and optimized executions returned byte-identical output.
Measured elapsed times were 3.715 and 3.912 seconds, respectively, with
peak resident memory 22,304 and 25,496 KiB. The deterministic record digest is

```text
871a137cc92bf10e8e3b7ce588ebe42007d2ce8fc17a60a9337743ca1b496336
```

The saved summary was generated from the source and then replayed. It is
compact corroboration, not an independently supplied certificate. No
solver, random sampling, downloaded dataset, native numerical library or
large artifact participates in verification.

The universal proof is analytic. Its external inputs are the classical
Lp Minkowski inequality and equality condition, ordinary Brunn--Minkowski,
support-function volume calculus, elliptic Fredholm/Schauder theory and
the Banach inverse/implicit function theorems. The Firey application also
imports the explicitly cited Taylor coefficient identity from the earlier
source package. None of these infinite-dimensional or universal claims
is established by the finite checks. There is no proof-assistant
formalization or independent peer review in this package.
