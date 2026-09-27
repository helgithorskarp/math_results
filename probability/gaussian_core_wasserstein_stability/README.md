# Uniform all-threshold Wasserstein stability with a protected source core

This extends the R2/R3/R8 mixed-chain certificate to arbitrary background
measures and perturbations controlled in Wasserstein-1 distance. Only a
fixed finite source core has a positive mass floor. The actual source can
have unbounded support; the actual target stays in a certified support
envelope. The conclusion holds at every threshold over any specified compact
positive-variance interval, with one explicit budget for the whole family.

The [proof](PROOF.md) combines retained core mass, an asymmetric signed tail,
and the imported R3/R8 middle/peak margins. The finite reduction certifies
an arbitrary measure on a rational background polytope by checking affine
inequalities at its vertices. This includes arbitrarily many atoms, vanishing
background weights and diffuse laws. It is not a collection of positive cells.

**Status:** complete author argument; independent review pending, including
the pending mixed-chain and polynomial-margin imports. The unrestricted
R3 conjecture remains open. The reference geometry and old cap guard are
reused; no new Kneser--Poulsen result or practical unrestricted cover is claimed.

The [input](INPUT.json) certifies the existing non-anchored fifteen-point core
plus any background measure on [-1/3,1/3]^3. Each core weight is at least
1/32; up to 17/32 mass is free background. Its ordered loss floor is 135/256,
width reserve 13/20000, target-envelope thickening 2^-13, and variance
interval [1,4]. The W1 sum budget is **2^-12564298226894**. The denominator
is not constructed. This very small budget is unchanged from the prior
calibration; the advance is the larger uniform measure/perturbation class.

From the repository root, CPython 3.11.2, standard library only:

```sh
python3 -B probability/gaussian_core_wasserstein_stability/verify.py
python3 -O -B probability/gaussian_core_wasserstein_stability/verify.py
python3 -B probability/gaussian_core_wasserstein_stability/verify.py \
  --input probability/gaussian_core_wasserstein_stability/INPUT.json \
  --certificate probability/gaussian_core_wasserstein_stability/CERTIFICATE.json
```

The first two commands reproduce [EXPECTED.json](EXPECTED.json), final status
`CORE_WASSERSTEIN_FAMILY_EXACT_CONTROLS_PASS`. Supplied-record mode verifies
that input, record and pinned dependencies without calling or importing the
producer. To regenerate the certificate without overwriting it:

```sh
python3 -B probability/gaussian_core_wasserstein_stability/certificate.py \
  probability/gaussian_core_wasserstein_stability/INPUT.json
```

The author checks passed normally and under optimization in 3.65/3.91 seconds,
with reported child peak RSS below 23 MiB; supplied-record checking took
0.19 seconds. Controls include 32 deliberate rejections, 270 affine
background checks, five weighted-loss identities, 54 tail-cubic checks,
a core-retention boundary, both motion guards, and zero-loss insertion.
Adding redundant background vertices raises the geometric list from 23 to
50 points, above 2^ell=32, without changing the core loss or budget. The
written affine/convex proof, rather than this finite control, establishes
completeness for every background measure.

Certificate SHA256:
`f1e6b70c30e79090db61fcfab31c461fde38da3e9be883cd5412616e7af08881`.
Expected-record SHA256:
`7a2bd29a086bdfb7e186c8269d0d92f31ce4924c6e0638d395faffd83f8980a1`.

See [FORMAT.md](FORMAT.md) for exact guards and the consumer's W1/support
membership obligations, [HANDOFF.md](HANDOFF.md) for the review boundary,
and [SOURCES.md](SOURCES.md) for attribution and the current unrestricted
frontier. Analytic imports and the written theorem are not formalized or
independently accepted by these exact checks. From this directory run
`sha256sum -c SHA256SUMS` to check the compact file manifest.
