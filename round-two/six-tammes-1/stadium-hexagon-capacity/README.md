# Unconditional short-hexagon region capacity

**six-tammes-1**, researcher, 2026-10-01. Complete author-checked written proof
with exact endpoint certificates; independent review and formalization pending.

In any spherical `c`-code with `14/25<=c<=3/5`, six prescribed cyclic edges
of dot at least `c-1/100` bound a simple hemispherical region containing at most
one other code point. Convexity, facial status, contact equality, coordinates,
radial hypotheses, degrees and irreducibility are unnecessary. For fifteen
points, no such cycle can separate at least two other points on each side.
This is a geometric exclusion, with global numerical Tammes bounds unchanged.

[PROOF.md](PROOF.md) derives interior caps, a great-circle-lune perimeter
comparison valid for concave cycles, and the exact two-cap hull perimeter.
[NUMERICS.md](NUMERICS.md) proves the enclosure semantics. Five fixed monotonic
parameter cells have exact perimeter margin greater than `1/25` radians.

From this directory, with Python >=3.11, standard library only:

```sh
python3 check.py > /tmp/tammes-stadium.json
cmp /tmp/tammes-stadium.json EXPECTED.json
python3 audit.py > /tmp/tammes-stadium-audit.json
cmp /tmp/tammes-stadium-audit.json AUDIT_EXPECTED.json
python3 -O check.py > /tmp/tammes-stadium-optimized.json
cmp /tmp/tammes-stadium-optimized.json EXPECTED.json
python3 -O audit.py > /tmp/tammes-stadium-audit-optimized.json
cmp /tmp/tammes-stadium-audit-optimized.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

`check.py` uses exact dyadic root brackets and an alternating atan enclosure.
`audit.py` imports none of it and uses root bisection and a positive asin
enclosure with a proved Machin pi bracket. Both prove the five scalar inequalities;
their complete rounded records agree. They share CPython/Fraction and are author
implementations, not independent researcher review. There are no runtime data
inputs, coordinate tables, solvers, ordinary floating-point arithmetic or large
enumerations. The expected outputs are receipts rather than proof inputs.

Author validation used CPython3.11.2, one job and one thread. Normal and
optimized outputs matched for both programs; all five endpoint records matched
between programs. Each run took under one second with peak child RSS14892KiB.

The continuous geometric and topological arguments remain unformalized written
mathematics. Passing the scalar checker alone does not prove the exclusion.
The statement concerns the cycle's smaller region and does not automatically
extend to the whole convex hull of a concave cycle. The next global step is
to incorporate this exclusion into a complete contact-pattern or coordinate-box
cover; no such cover is supplied here. [SOURCE_CONTEXT.md](SOURCE_CONTEXT.md)
credits the classical irreducible-face result and the preceding conditional
criteria without asserting historical priority.
