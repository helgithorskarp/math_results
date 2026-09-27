# Independent review: uniform Lipschitz Gaussian endpoint

This directory independently reviews Discovery Net artifact
`bafkreicig6auyae5d2ofi6rkpoqdkoij34sb6pra2ytn7xbqfyrsnsa7cq` at source
commit `ba0c239ecafa9d02a611dde4960ca3682e9adc17`.

Use standard-library CPython 3.11+:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report `INDEPENDENT_UNIFORM_LIPSCHITZ_ACCEPT`.
The checker imports no author module or certificate. See [REVIEW.md](REVIEW.md)
for the mathematical verdict and the boundary between exact controls and
written analysis.
