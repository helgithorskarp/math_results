# Independent review: Mycielski clique-complex Stirling wedge law

This directory contains an independent review of the contribution
“Stirling wedge law and sharp three-step asphericity boundary for Mycielski
clique complexes.”

Verdict: **accept with high confidence**.  See [REVIEW.md](REVIEW.md) for the
complete premise audit, adversarial examples, source boundary, and caveats.

The independent checker imports no target code or output.  It exhausts all
labelled graphs through six vertices, checks every admitted one-step lift over
two finite fields, compares closed and iterated formulas through `k=8`, and
tests all 65,536 triangle subcomplexes of `Cl(M^2(K3))`.

Reproduce with CPython 3.11 or later, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 audit_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_independent.py
sha256sum -c SHA256SUMS
```

Both Python commands compare against `EXPECTED_OUTPUT.json` and print
`"status": "pass"`.  Typical runtime is about 20 seconds per run on the
review machine.

The computation is corroboration, not a finite proof of the universal
homotopy statement.  That statement is accepted from the attachment,
recurrence, noncancellation, and collapse arguments enumerated in the review.
