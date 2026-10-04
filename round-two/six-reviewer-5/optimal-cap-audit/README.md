# Independent degree-nine constructed-cap audit

Actual six-reviewer-5, independent mathematical reviewer. Ordinary unformalized
proof; written target exposed, author native source/fixtures unexposed.

[REVIEW.md](REVIEW.md) gives the confirming scoped verdict on LEMMA 10212.
[PROOF.md](PROOF.md) supplies the full original-root/analytic cap argument and
the sharp attainable restricted repair cone. [LITERATURE.md](LITERATURE.md)
and [DEPENDENCIES.json](DEPENDENCIES.json) preserve attribution and exact pins.

Standard library only; observed CPython 3.12.14. From this directory:

```sh
python3 -I -B verify.py --output /tmp/cap-audit-validation.json
python3 -I -B -O verify.py --output /tmp/cap-audit-optimized.json
```

The driver verifies complete code hashes, then runs one arithmetic child at
a time, with native threads one and fixed 45-second guards. It reconstructs
14 routes in normal, optimized and cold copies, compares every exact record
with [RECORD.json](RECORD.json), and rejects twenty semantic damages. No CAS
or external author certificate is loaded. A timeout is incompleteness, never
mathematical nonexistence. Generated scratch directories are removed only
when the driver's own context exits; no unrelated research is deleted.

One route may be reproduced independently:

```sh
python3 -I -B check.py --route root --label 7 --output /tmp/original-seven.json
python3 -I -B check.py --route core --output /tmp/objective-and-dual.json
python3 -I -B check.py --route restricted --label 4 --output /tmp/fourth-normal.json
```

The full rational jet record is sparse and lossless, including zero positions
by the declared 12-coordinate field and degree-nine jet convention. Source
and mathematical record hashes are distinct. Finite checks do not formalize
the complete ordinary analytic bridges in PROOF.md or the inherited universal
comparison premises. No universal fourth optimum or global first-power
resolution is asserted.
