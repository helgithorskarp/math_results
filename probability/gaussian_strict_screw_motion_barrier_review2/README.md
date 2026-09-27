# Independent review of the strict screw `R5` barrier

This directory independently reviews Discovery Net artifact
`bafkreiaztgiaxvzo42xmk7wkr2ypi77ka3nrs6u2ojsgpagmy77ajlndqa` at exact
source commit `57e474d503119b7c67cdfe4ce92bc4616ed4312a`.

[`REVIEW.md`](REVIEW.md) audits the intrinsic halfway functional, centered-
Gram/polar repair, axis repair, auxiliary Gram determinant, strict rational
witness, and exact six-dimensional upper bound. The independent checker
imports no author module and reconstructs the 24 reference sites from their
displayed formulas.

Reproduce with CPython 3.11 or later:

```sh
python3 -B independent_check.py > /tmp/strict-screw-review2.json
cmp /tmp/strict-screw-review2.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/strict-screw-review2-opt.json
cmp /tmp/strict-screw-review2-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_STRICT_SCREW_R5_REVIEW_PASS`.

The checker pins seven exact inputs and verifies the finite rational and
polynomial boundaries. The universal perturbation, polar-alignment, and
continuity arguments are independently audited mathematics, not consequences
of finite testing or a proof-assistant formalization.
