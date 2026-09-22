# Independent review: symmetric Firey Rogers--Shephard theorem

This directory records an independent review of the proof in
[`symmetric_firey_rogers_shephard`](../symmetric_firey_rogers_shephard/).
The verdict is **accept**, subject to the classical convex-geometric premises
listed in [REVIEW.md](REVIEW.md).

The review rederives the support-curvature calculation, endpoint constant,
and nonsmooth equality reduction.  It also checks the claim against the
current primary paper, which states the all-dimensional inequality as
Conjecture 4.

`verify.py` is deliberately narrower and structurally different from the
producer's checker.  It uses exact rational planar convex hulls and the
definition of the `p=infinity` sum to test the equality geometry.  It also
records a direct `p=2` support-area calculation for the square, including the
exact sharp ratio `2 + pi/2`.  These finite checks are adversarial examples,
not a substitute for the analytic audit.

Run with CPython 3.11+ and no dependencies:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands must reproduce `EXPECTED.json`.  Arithmetic in the
polygon checks is exact (`fractions.Fraction`); the coefficient of `pi` in
the direct square calculation is stored symbolically.

