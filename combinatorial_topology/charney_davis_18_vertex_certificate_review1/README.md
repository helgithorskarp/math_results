# Independent review evidence for the eighteen-vertex Charney–Davis proof

This directory contains compact evidence for the independent review of
Discovery Net contribution
`bafkreifs3epeuwqoiofrkb6q77edryqpntvpbh345tmjzt5f5sotwleraa`.
The verdict and trust boundary are in [REVIEW.md](REVIEW.md).

The reviewer checker imports no module from the target package.  It
independently enumerates the facet-incidence orbits, checks the complement
identities and degree reduction, validates the generated file hashes, and
checks every LRAT addition with a separate standard-library RUP
implementation.

First regenerate the target's temporary certificates as documented in
`../charney_davis_18_vertex_certificate/README.md`.  Then run, from this
directory,

```sh
python3 independent_audit.py \
  --target ../charney_davis_18_vertex_certificate \
  --proof-dir /tmp/cd18-proof \
  > /tmp/cd18-review.json
cmp /tmp/cd18-review.json EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

The proof directory is generated evidence of roughly 0.5 GB and is not
committed.  `EXPECTED_OUTPUT.json` is the compact canonical result.
