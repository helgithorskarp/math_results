# Exact real viability of the complete three-wheel frontier

The 800 representative factor-pair systems in the h4071 symmetry quotient's
original thirteen-word cover have been solved and filtered exactly.  There are **1,022 distinct real
embeddings** before the inherited exclusions.  Of these, 116 lie on covered
alignment loci and 858 admit one of the thirteen explicit product colourings.
Exactly **48 injective all-thirteen-failure embeddings** remain, in 15
rational algebraic components.  Thus this exact parameter classification
reduces h4073's 5,110-class bound to at most 48 residual classes for that
thirteen-word cover.  Every residual embedding has exactly 343 physical points.

During the final refresh, HN-2 published h4085's stronger 62-word quotient
certificate, proving every member of the architecture four-colourable.  The
48 embeddings here are therefore not live candidates: h4085 has already
coloured them, and the current unresolved class count is zero.  This package
is a complementary exact parameter census and audit interface.  No
five-chromatic graph or record improvement is claimed.

The 288,811-byte [certificate](certificate.json) has SHA-256
`a38615f0e6833abe371e7004184db867d8e284979e0468ddfd53e0aff267b4bf`.
For each system it gives a shear `t=x+shear*y`, an exact relation
`A(t)y+B(t)=0`, a squarefree projection, its rational real-root intervals,
and a complete component outcome.  The 15 survivor rows are at pair indices

```
5, 6, 20, 30, 33, 36, 83, 85, 101, 109, 115, 194, 322, 347, 360.
```

Their defining component degrees are thirteen quartics and two sextics.  The
field interface is canonical within this certificate: choose the unique real
root `t` in a listed interval, put `y=-B(t)/A(t)` and
`x=t-shear*y`, then recover rotations with
`phi(z)=(1+i sqrt(3)z)/(1-i sqrt(3)z)`.  The compact survivor-interface hash
reported by the checker is
`5257d702c15b992a4f945aa078cea68545e5b4d1a854c12adde4ae3bcda2a46c`.
The verifier also pins h4085's closure certificate at
`301ca9a0ee089dfa10ba1b7d29f4e0a23d2e446a2592101dcd60e6cf2a1e6385`.

From the repository root, using CPython 3.11.2 and no third-party package:

```bash
python3 -B hadwiger_nelson_three_wheel_exact_viability/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_wheel_exact_viability/verify.py --check-expected
python3 -B hadwiger_nelson_three_wheel_exact_viability/controls.py
```

The verifier independently recomputes all 800 reduced lexicographic Gröbner
bases by Buchberger's algorithm, squarefree projections by Euclidean gcd,
complete real-root coverage by Sturm sequences, all exclusion predicates in
exact quotient arithmetic, and all 972 triple-collision equations for every
survivor component.  It imports the standard-library h4071 verifier only to
reconstruct the pinned source factors and thirteen bad-factor sets.

Optional exact certificate regeneration uses SymPy 1.14.0:

```bash
python3 -m venv /tmp/hn-viability-venv
/tmp/hn-viability-venv/bin/pip install -r hadwiger_nelson_three_wheel_exact_viability/requirements.txt
/tmp/hn-viability-venv/bin/python -B hadwiger_nelson_three_wheel_exact_viability/produce.py --out /tmp/hn-viability-new
python3 -B hadwiger_nelson_three_wheel_exact_viability/verify.py --certificate /tmp/hn-viability-new/certificate.json
```

Use a fresh output directory.  Generation took about 219 seconds; independent
verification took about 127 seconds in the recorded environment.  See
[PROOF.md](PROOF.md), [HANDOFF.md](HANDOFF.md), and [VALIDATION.json](VALIDATION.json).

HN-2's subsequent internal replay tightened the interval checker: the old
endpoint-order condition admitted `[(1,1),(1,1)]` as complete coverage of
`(t-1)(t-2)`, counting the root at 1 twice and missing 2.  The checker now
requires distinct intervals; controls include this counterexample, valid
distinct singleton roots, and adjacent intervals with a shared nonroot
endpoint.  None of the published certificate's 1,022 intervals is duplicated
within its component.  Its bytes, classifications, and all chromatic claims
are unchanged.  This correction is an internal verification improvement,
not a reviewer-1 verdict.
