# Reproduction summary

Requirements: CPython 3.11 or later; standard library only.

```sh
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -O -B verify.py --check-expected
python3 -O -B controls.py
sha256sum -c SHA256SUMS
```

Expected terminal markers are JSON with `"status": "PASS"` and
`CONTROLS_OK 4`. The producer command and semantic certificate comparison are
given in `README.md`.
