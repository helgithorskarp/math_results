# Radial capacity of short spherical cycles

**six-tammes-1**, researcher, 2026-10-01. Author-checked ordinary proofs;
independent review pending.

[PROOF.md](PROOF.md) gives a template-free capacity criterion. In a spherical
`c`-code with `1/2<=c<=3/5`, a short cycle with edge dots at least `c-1/40`
cannot contain two further points if one interior point has dot at least
`1/6` with every boundary vertex. A strict covering margin `3/5+1/12500`
is proved. Concave cycles and arbitrary numbers of sides are allowed. Both
the covering and capacity conclusions extend to the whole spherical convex hull.
An alternative criterion needs only an interior geometric witness with all
boundary projections in `[2/5,3/5]`; the witness need not be a packing point.
It traps all admissible insertions in a cap of cosine greater than `9/10`.

[HEXAGON.md](HEXAGON.md) computes the exact insertion capacity of the regular
contact hexagon: two up to `(20 sqrt(3)-15)/39`, one above. An explicit
eight-point code at `c=501/1000` keeps the wider conjectural scope honest.
This example is outside the fifteen-point improvement strip. Neither proof
improves a global Tammes bound or proves arbitrary hexagons have capacity one.

From this directory, with Python >=3.11 and only the standard library:

```sh
python3 check.py > /tmp/tammes-radial.json
cmp /tmp/tammes-radial.json EXPECTED.json
python3 -O check.py > /tmp/tammes-radial-optimized.json
cmp /tmp/tammes-radial-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
```

`check.py` has no runtime data inputs or third-party dependencies. It checks
exact rational margins, coefficient-level identities for the regular family,
the algebraic transition, and all 28 pairs of the explicit control using
proved radical bounds. It also checks two deliberate failures of broader
scalar/fixture certificates. It does **not** check the Jordan, ray, cap or
diameter arguments. Those are written proofs, not code enumeration results.
`EXPECTED.json` is a deterministic output receipt, not a proof input.
Normal and optimized runs are expected to agree; no Python `assert` is used
for mathematical verification. No solver, floating-point computation,
coordinate dataset or large corpus is needed.

Author validation used CPython 3.11.2, one mathematical job and one thread.
Normal and optimized output was byte identical; `EXPECTED.json` and `SHA256SUMS`
pin the output. The runs took under one second each with peak child RSS below
20 MiB.

See [SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) for literature, attribution and the
relationship to the existing template and nonconvex-cycle results. The concrete
next frontier is the failure of the radial hypothesis: with two insertions,
each must have a boundary dot below `1/6`. Nothing here excludes that case.
