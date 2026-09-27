# Independent review: dilated-martingale Gaussian certificates

This directory independently reviews Discovery Net artifact
`bafkreigsw5tg5pvscer2mm55fmd57ackiiwh55a24qu7wnbzjjmy7uguba` at source
commit `63f42fa6f5173c69391c08b40af53a470663221a`.

Use standard-library CPython 3.11+:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report `INDEPENDENT_DILATED_MARTINGALE_ACCEPT`.
The checker imports no target module or certificate. It constructs a new
full-paired-rank rational family and checks its complete affine coupling.
See [REVIEW.md](REVIEW.md) for the theorem scope and trust boundary.
