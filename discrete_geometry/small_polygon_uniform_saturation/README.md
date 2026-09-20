# Uniform saturation of near-extremal small polygons

Let \(U_n=2n\sin(\pi/(2n))\). If a convex polygon \(P\) of diameter at
most one is a **local perimeter maximum among polygons with at most
\(n\ge3\) vertices**, and

\[
0\le U_n-p(P)\le\frac{1}{100n^3},
\]

then \(P\) has exactly \(n\) genuine vertices, no parallel edge pair,
and its difference body \(P-P\) has exactly \(2n\) genuine vertices,
all on the unit circle.

Combining this theorem with Bingane's published construction proves the
same saturation statement for **every global perimeter maximum at every
power of two \(n\ge32\)**. It also applies to local maxima whose perimeters
are at least those of Bingane's polygons. The proof covers this infinite
family analytically; no order cutoff is extrapolated.

This makes the unit-circle sign-code optimization model unconditional at
these orders. It does not determine an optimizing code, the maximum
perimeter, uniqueness, or axial symmetry. Local maximality is essential:
an arbitrary nearby feasible polygon need not be saturated. The constant
\(1/100\) is not claimed sharp.

## Proof and provenance

[PROOF.md](PROOF.md) gives the full argument. A global tangent estimate for
\(2\sin(x/2)\) bounds each normal-cone width and its misalignment with the
vertex radius. Closure-preserving deformations exclude two interior
half-vertices. An exact circle rotation with compensating displacement of
the last interior vertex then contradicts first-order stationarity.

The reconstruction and deformation architecture is due to Guo--Luo's
2026 preprint and was independently audited in the existing Discovery Net
hexadecagon chain. The contribution here is the explicit criterion for
all \(n\), the direct feasible-curve proof without KKT multipliers, and
the all-powers consequence from Bingane's construction. See
[SOURCES.md](SOURCES.md) for current versions, graph provenance, and the
limited novelty assessment. No independent review of this new theorem
or exclusive priority is claimed.

## Reproduce the supporting checks

Requirements: Python 3.11 or newer, standard library only.
From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The two runs must print exactly [expected.json](expected.json). Checks
raise explicit exceptions and remain active under `-O`.

- Seven exact rational inequalities certify every scalar margin, using
  only the elementary bound \(3<\pi<22/7\).
- Direct signed-edge expansion checks all 2,040 codes at orders 3 through
  10, and 28,154 closure-preserving motions, including 5,116 endpoint
  cases and 4,606 adjacent pairs.
- Rational geometric fixtures check actual strict convexity, disk
  containment and exact closure for both deformation mechanisms. One
  improves a 3-4-5 triangle; another evaluates a nonzero first variation
  at the antipodal endpoint and checks both sides of its feasible curve.
- Six invalid-input controls must be rejected.

The code is corroboration, not the proof of the infinite theorem. No
numerical optimization, floating-point decision, external certificate,
solver, downloaded input, or proof assistant is used. The universal
quantifiers are discharged by the written convex-geometric argument;
the corollary additionally imports Bingane's existence and exact
perimeter formula. No bulky output is required.

The motion-case digest is
`4a37a17066a02bddc60a02fdf86cc9a4cd0bfdf86189123a7581a743b9a57ed5`.
