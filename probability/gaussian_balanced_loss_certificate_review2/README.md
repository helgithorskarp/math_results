# Independent review of the balanced-loss certificate

This directory records an independent acceptance review of Discovery Net
artifact `bafkreihaxhapv7kvng2yatxu2unok44m3v3vxwvp47mdgxkfvuqlxvzmgy`
at exact source commit `91c63ff5a464f725ea6bee38290e56df594f1c60`.

The [review](REVIEW.md) audits the polar alignment, trace decomposition,
pair-displacement guard, straight contracting motion, uniform balanced-loss
cover, and weighted 19-atom corollary.  The
[independent checker](independent_check.py) imports no target module and
checks the geometric path directly on both the published endpoint and a
fresh non-diagonal paired-rank-six fixture.

Reproduce with Python 3.11 standard library only:

```sh
python3 -B independent_check.py > /tmp/balanced-loss-review.json
cmp /tmp/balanced-loss-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/balanced-loss-review-opt.json
cmp /tmp/balanced-loss-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_BALANCED_LOSS_REVIEW_PASS`.
