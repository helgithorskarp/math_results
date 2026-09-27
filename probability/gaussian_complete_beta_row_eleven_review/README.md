# Independent review: complete Gaussian beta row eleven

This directory independently reviews Discovery Net artifact
`bafkreifvvmdfgjhav2oddy4b22iqx2b5xhouwe5w5nlimlruet3pgzdysu` at source
commit `663e97310e118d1ebe76562d6318955af7a258f9`.

Run with standard-library CPython 3.11+:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report
`INDEPENDENT_COMPLETE_BETA_ROW_ELEVEN_ACCEPT`. The checker imports no target
module and uses a different exact positivity algorithm from the target.
See [REVIEW.md](REVIEW.md) for the accepted scope and trust boundary.
