# Reproduction

Run from this directory with CPython 3.11 or later:

```sh
python3 -B verify.py --certificate certificate.json --check-expected --controls
python3 -O -B verify.py --certificate certificate.json --check-expected --controls
tmpdir=$(mktemp -d)
python3 -B produce.py --out "$tmpdir/certificate.json"
cmp certificate.json "$tmpdir/certificate.json"
rm -r "$tmpdir"
sha256sum -c SHA256SUMS
```

The producer output must not already exist.  No network request, solver,
third-party Python package or omitted data file is used.  The sibling source
certificate is part of the same repository and is pinned in
`DEPENDENCIES.json` and in the generated certificate.
