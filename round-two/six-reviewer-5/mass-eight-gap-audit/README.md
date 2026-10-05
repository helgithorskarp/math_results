# Independent mass-eight annular-gap audit

Actual **six-reviewer-5 / independent mathematical reviewer**, 2026-10-05.
**CONFIRMED, high confidence, ordinary unformalized**, at the exact scope
of committed LEMMA 10300, with the parent 10274 exclusion explicit.
For every complex degree-nine polynomial with all original roots in the
closed unit disk and every marked root \(2/3\le |a|\le27/40\),
\[
\sum_{j=1}^8|a-\zeta_j|^{-1}>8+1/340.
\]
This independently proved sufficient refinement implies the target's
weaker 1/350 gap. All multiplicities, closed endpoints and infinite
reciprocal summands are covered. The parent supplies only F<=8 exclusion
on this same annulus. No global first-power or optimal-constant claim.

[REVIEW.md](REVIEW.md) states the referee assessment;
[PROOF.md](PROOF.md) proves the generic centered/face/path bridges;
[ENTRY.md](ENTRY.md) supplies the preceding independent closed entry
and clipping/product lemmas. Source credits and trust boundaries are
explicit. No author executable/EXPECTED/corpus/peer checker was input.

CPython 3.11.2, standard library only. Run each from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
timeout 45s python3 -I -B entry.py > generated-entry.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
timeout 45s python3 -I -B face.py > generated-face.json
sha256sum generated-entry.json generated-face.json
```

Expected ENTIRE records:

| Component | Bytes | SHA256 |
|---|---:|---|
| Entry/path | 350023 | d85a33f87549606f1282d6a4bcf039d455a3dddecf271cdd84813189b1ec3701 |
| All 139 face leaves and 1/340 refinement | 3070840 | b66b192e58bc79e3ab95ad283817bbbeeaaf04be5fa3bef778be945448cc7fda |

Large records regenerate locally and are omitted. SUMMARY.json is a
compact projection, not mathematical input. EVIDENCE.json records the
completed four local/cold normal/optimized checks for each component.
The mathematical source bytes are unchanged from those checked runs.
An optional bounded full face replay is `timeout 210s python3 -I -B validate_math.py`;
it serializes four 45-second children and writes ignored local outputs.
All six native thread variables should be one as above.

Source integrity alone: `python3 -I -B check_sources.py` (also works with
`-O`). It checks all manifest files, owned code/data pins and reversible
document edits without replaying closed mathematics. The source-only
adverse/isolated replay is recorded in SOURCE-VALIDATION.json.

The exact computed leaf roles are 79 scalar-origin, 9 retained-mean
origin (BOTH energy families), 2 standard-polar and 49 joint-polar.
Every coefficient/integral/Bernstein representation is checked, and the
ordinary proof supplies the universal continuum reduction. Neither
record agreement nor a hash supplies that analytic proof.

The real Hilbert Banach theorem, explicit parent exclusion, ordinary
Gauss-Lucas/Hermite/path arguments, CPython/Fraction and checker
correctness remain trust boundaries. No proof-assistant certification
or exclusive priority is claimed. Source publication and accepted
broadcasts have distinct meanings; actual graph commitment must be
confirmed separately.
