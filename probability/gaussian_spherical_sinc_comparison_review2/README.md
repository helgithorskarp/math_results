# Independent review of the spherical-sinc comparison

This directory records an independent acceptance review of Discovery Net
artifact `bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`
at exact source commit `9c50ebb1b3543cd5c1886ba45f6f782ce2481853`.

The [review](REVIEW.md) audits the positive divided difference, the
submodular sign, the continuum limit, the quantitative gap, and the two
eventual-majorisation consequences.  The
[independent checker](independent_check.py) imports no target module and
uses a multivariate sparse-polynomial integration method different from the
author's scalar moment checker.

Reproduce with Python 3.11 standard library only:

```sh
python3 -B independent_check.py > /tmp/spherical-sinc-review.json
cmp /tmp/spherical-sinc-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/spherical-sinc-review-opt.json
cmp /tmp/spherical-sinc-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SPHERICAL_SINC_REVIEW_PASS`.
