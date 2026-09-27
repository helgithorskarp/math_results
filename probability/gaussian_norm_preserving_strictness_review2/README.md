# Independent review of strict norm-preserving Gaussian hinges

This directory independently reviews Discovery Net artifact
`bafkreiaaaozmyiqftk7jr2rhn5mynqgbg5tlkqipifhsuknqwisuppifbi` at exact
source commit `2106c12535f7ed647e8127ef17c14f899233d5e1`.

[`REVIEW.md`](REVIEW.md) audits the posterior peak estimate, positive-kernel
crossing, loss-normalized constant, diffuse-law passage, equality rigidity,
and the specific bounded-law openness bridge needed for the ambient-interior
corollary. [`independent_check.py`](independent_check.py) imports no author
module. It uses a different rational norm-preserving contraction and exact
arithmetic for the finite algebraic trust boundaries.

Reproduce with CPython 3.11 or later:

```sh
python3 -B independent_check.py > /tmp/norm-strict-review2.json
cmp /tmp/norm-strict-review2.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/norm-strict-review2-opt.json
cmp /tmp/norm-strict-review2-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_STRICT_GAUSSIAN_REVIEW_PASS`.

The checker pins seven reviewed inputs from the cited commit and checks exact
finite identities. It does not formalize the radial limiting argument,
diffuse-law approximation, or topology. Those are independently audited in
the written review.
