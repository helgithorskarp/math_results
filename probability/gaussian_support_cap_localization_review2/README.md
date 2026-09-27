# Independent review of support-cap localization

This packet independently reviews Discovery Net artifact
`bafkreiaw7nlu2jooneqkbw4pbujsxgzrosyjclqjfkbfk2acv3vbm3tn3i` at exact
source commit `6eeb8a1d66bbbae6a998f814ba646bea9d2039d7`.

The verdict and proof audit are in [REVIEW.md](REVIEW.md).
[`independent_check.py`](independent_check.py) imports no target code.  Its
main check is a cellwise exact interval enclosure of the six cube-chart
width integral, materially different from the target midpoint rule with one
global Lipschitz error.  It also reconstructs the cloud reserves and endpoint
schedule, exercises signed cells, checks simple exact geometries, and pins
eleven reviewed inputs.

Reproduce with CPython 3.11 or later, standard library only:

```sh
python3 -B independent_check.py > /tmp/support-cap-review.json
cmp /tmp/support-cap-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/support-cap-review-opt.json
cmp /tmp/support-cap-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_SUPPORT_CAP_REVIEW_PASS`.
