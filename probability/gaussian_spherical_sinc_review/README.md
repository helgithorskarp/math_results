# Independent review: spherical sinc comparison

This directory independently reviews Discovery Net artifact
`bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja` at source
commit `9c50ebb1b3543cd5c1886ba45f6f782ce2481853`.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report `INDEPENDENT_SPHERICAL_SINC_ACCEPT`. The
checker imports no target code. It represents multivariate polynomials by
coefficient dictionaries and integrates the Duhamel kernel directly, rather
than replaying the author's scalar affine-moment expansion. See
[REVIEW.md](REVIEW.md) for the mathematical scope and trust boundary.
