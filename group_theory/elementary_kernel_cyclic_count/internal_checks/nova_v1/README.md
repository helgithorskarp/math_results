# Nova's independent elementary-kernel check

Checker: Nova / studio-researcher-3, researcher, Colloquium 2026-10-05.

This is an internal check of Rowan's fixed `PROOF.md` SHA256
`813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de`
and the mathematical outputs of his 22-fixture `EXPECTED.json` SHA256
`a9c019cc56412b79d36658ea18bf3dda6e465552a60e9682ec6ec09015262c8f`.
The universal proof assessment is in [REPORT.md](REPORT.md). These finite
controls supplement that proof; they are not a proof by enumeration.

Run with GAP 4.12.1 and SmallGrp 1.5.1, then Python 3.12:

```sh
gap -A -b -q -m 64m -o 512m --quitonbreak check_extensions.g
python3 compare_expected.py
```

An unpacked GAP needs its kernel path and `-l /path/to/share/gap`.
The recorded run used a serial GAP kernel with a 512 MiB heap ceiling.
It imports no Rowan implementation. `ROWAN_EXPECTED.json` is the fixed
comparison input. `RESULT.json` records the separate group computations;
`COMPARISON.json` records the exact mathematical-field comparison.

All 22 original fixtures match, as do their element-order and cyclic-
subgroup-order histograms, bounds and defects. Four changed inputs
exercise further norm ranks, odd and characteristic-two actions, and
another nonsplit cyclic extension. Three malformed-data guards reject
the same mathematical errors as the author controls. Representation-
dependent set and coordinate hashes are not compared; the checker
instead verifies the affine norm equation directly in every coset.

Publication allowlist: README.md, REPORT.md, check_extensions.g,
compare_expected.py, ROWAN_EXPECTED.json, RESULT.json, COMPARISON.json,
MANIFEST.json. Private debugging transcripts are excluded. No modular-
family supplement is included in this fixed check.
