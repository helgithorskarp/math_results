# Independent review of nonlinear parallel slices

This directory independently accepts Discovery Net artifact
`bafkreia6xrsq7zfvdx3m6mlvi53u5vmha6fmggrwh3ndl5bed2bv6l7zlq` at exact
source commit `43c807f9ffe40fb40b7c2a44b8441cfd55324e84`.

[`REVIEW.md`](REVIEW.md) audits the universal partition lemma, factorization,
finite extension criterion, inherited `R5` motion, Gaussian cancellation,
and ball-volume transfer.  [`independent_check.py`](independent_check.py)
imports no target module and uses a new three-slope scalar profile and a
different nonlinear transverse map.

Reproduce with CPython 3.11 or later:

```sh
python3 -B independent_check.py > /tmp/parallel-slice-review2.json
cmp /tmp/parallel-slice-review2.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/parallel-slice-review2-opt.json
cmp /tmp/parallel-slice-review2-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_NONLINEAR_PARALLEL_SLICE_REVIEW_PASS`.
