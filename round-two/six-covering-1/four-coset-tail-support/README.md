# Four-coset tail support bound

By **six-covering-1**, researcher, 2026-10-02.

If the29 distinct original7d classes, d|720,d>=2, cover every seven-copy
of an actual subset K of {x mod720:x=0 mod4,x!=6 mod9}, then |K|<=115.
Together with the earlier104-hole stage obstruction, the owned
18:3/four:0 construction route must have74..115 actual four-target holes.
The global minimum-exactly-eight problem remains open.

See [proof.md](proof.md) for the complete written argument and its scope.
The exact selected-seven bound is sharp as a relaxation; its sharpness
fixture is not a covering construction.

Run with standard-library Python3.11 or later, from this directory:

```sh
python3 check.py
python3 audit.py
python3 controls.py
python3 -O check.py
python3 -O audit.py
python3 -O controls.py
sha256sum -c SHA256SUMS
```

All arithmetic and set operations are exact. No solver, external library,
network, key, ledger, or unpublished experiment is required. The complete
checker uses598500 tiny cases and stores multiplicity histograms, not a
large search tree. Audit uses physical sets and the separate written case
proof. Expected values were fixed before the independent audit.

Files: proof, complete checker, independent audit, damage controls,
expected values, compact certificate, manifest, and checksums. Proof status
is author-checked and unformalized; no independent reviewer verdict.
