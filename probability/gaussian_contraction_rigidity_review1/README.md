# Independent review evidence for Gaussian contraction rigidity

This directory accompanies an independent review of
[`../gaussian_contraction_rigidity`](../gaussian_contraction_rigidity).
The exact checker concentrates on the least-covered algebraic reduction in
the producer package: passage from a centered Gram-kernel error to optimal
orthogonal alignment.

It uses only Python's standard library and exact `fractions.Fraction`
arithmetic.  From this directory, run

~~~sh
python3 verify_review.py > actual.json
cmp actual.json EXPECTED.json
python3 -O verify_review.py > actual-optimized.json
cmp actual-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
~~~

The checker includes a genuinely non-diagonal positive aligned
cross-covariance whose input and output covariance matrices do not commute,
a singular aligned case, the two-dimensional rotation counterexample showing
why optimization over the orthogonal factor is essential, and exhaustive
one-dimensional three-point maps on a half-integral image grid.

These are finite algebra checks.  They do not replace the human audit of the
Gaussian path, differentiation, truncation, strictness, or literature scope;
see [`REVIEW.md`](REVIEW.md).
