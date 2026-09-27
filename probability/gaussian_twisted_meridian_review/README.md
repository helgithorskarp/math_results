# Independent review: twisted meridian contractions

This directory independently reviews Discovery Net artifact
`bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq` at source
commit `2de654f1c1f69a3ab543993d1a53553e91e2164b`.

Use standard-library CPython 3.11+:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both modes must report `INDEPENDENT_TWISTED_MERIDIAN_ACCEPT`. The checker
imports no author module or expected record and uses direct Euclidean
coordinate differentiation rather than the author's sparse formal
polynomial implementation. See [REVIEW.md](REVIEW.md) for scope.
