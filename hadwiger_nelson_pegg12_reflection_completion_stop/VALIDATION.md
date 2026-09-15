# Validation

Author-side runs on 2026-09-15 UTC with CPython 3.11.2:

```text
$ python3 -B verify.py
... "source":{"canonical_four_colorings":756,...}
VERIFIED_PEGG12_REFLECTION_COMPLETION_STOP

$ python3 -B controls.py
VERIFIED_PEGG12_REFLECTION_CONTROLS

$ sha256sum -c SHA256SUMS
README.md: OK
PROVENANCE.md: OK
model.py: OK
verify.py: OK
controls.py: OK
certificate.json: OK
expected.json: OK
```

The verifier took approximately five seconds and the controls approximately
three seconds on the producing host.  Runtime is descriptive, not a premise.
