# Independent geometric review of the universal beta sign strips

[The review](REVIEW.md) accepts with high confidence researcher 5's
six-column projection theorem and researcher 2's seven-column
affine-conditioning theorem, including its quantitative pair-loss bound.
For every bounded R3 input, contraction and Gaussian variance, the beta
tests with N-k<=6 and their polarized coefficients have the claimed signs.
The reviewed source commits are respectively
`8a1e00a5328e9e340b2e511b2adf6893231e5d03` and
`a649ce1267fac02c0e11972a988e545ffab0db79`.

The review reconstructs the projection using an alternative centering,
checks the affine-offset probability representation, the quantitative
constant, and the polarized normalization term by term. It does not
accept a solution of the full conjecture, the columns N-k>=7, historical
priority, or a new Kneser--Poulsen case. The separate flap determinant
fixture is not independently reproduced. This is an independent agent
review, not external human peer review or formalization.

Run in this directory with standard-library CPython 3.11 or later:

```sh
python3 independent_check.py --check
python3 -O independent_check.py --check
sha256sum -c SHA256SUMS
```

CPython 3.11.2 produces in both modes:

```text
INDEPENDENT_GAUSSIAN_BETA_GEOMETRY_REVIEW_PASS
fd8a936e309ce0618a8b09dfeb9df8868653e607b76a1552a37d5a7f0b3eb522
```

The exact checks compare 193 linear-projection subsets, 194 affine-offset
subsets, 147 scalar controls and 31,234 individual polarized symbols,
and reject seven deliberate mistakes. A run takes about one second on
the reviewer's host. No author checker or certificate is imported.
The finite checks supplement the written review; they do not infer a
universal sign from examples. [INPUTS.json](INPUTS.json) pins inspected
sources; [EXPECTED.json](EXPECTED.json) is this checker's compact output.
No large artifact is required.
