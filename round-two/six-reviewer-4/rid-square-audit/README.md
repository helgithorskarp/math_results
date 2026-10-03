# Independent RID square-collar review

Actual author: six-reviewer-4, independent mathematical reviewer, 2026-10-03.
[Assessment](REVIEW.md) and [complete ordinary proof](PROOF.md) confirm the
original whole-segment claim and establish its exact first-companion threshold.
No unknown-source entry or global RID theorem is asserted.

CPython3.11.2; standard library only. From the repository root run serially:

```sh
python3 -B round-two/six-reviewer-4/rid-square-audit/verify.py
python3 -B -O round-two/six-reviewer-4/rid-square-audit/verify.py
python3 -B round-two/six-reviewer-4/rid-square-audit/verify.py --controls
python3 -B -O round-two/six-reviewer-4/rid-square-audit/verify.py --controls
```

The wrapper validates the complete source manifest before any mathematical
import, sets all six numerical-library thread variables to one, and runs one
child at a time with a fixed30-second deadline. Both normal and optimized modes
compare the complete fresh summary to the declared compact record. Eleven
damaged mathematical fixtures must all reject. A failure or timeout is incomplete
verification and supplies no mathematical nonexistence conclusion.

To regenerate the complete individual-value record, keeping it outside the source:

```sh
python3 -B round-two/six-reviewer-4/rid-square-audit/audit.py --record scratch/rid-record-normal.json
python3 -B -O round-two/six-reviewer-4/rid-square-audit/audit.py --record scratch/rid-record-optimized.json
cmp scratch/rid-record-normal.json scratch/rid-record-optimized.json
```

Set the six thread variables to one for those direct commands as well. Their
complete mathematical canonical hash is in expected.json. For a minimal cold
replay, copy only exact.py, audit.py and controls.py to a fresh empty directory;
these three files are the entire mathematical runtime. Compare each regenerated
full record with the original, and each summary/control record with the compact
public expected file. The release validation did this in both modes.

The records regenerate all individual finite controls. The ordinary proof is
required for the continuum and quantifier consequences. It is unformalized.
No third-party code, target executable/data, solver, native library, old proof
forest or local private file is needed. The defined standard coordinate model
and Python exact arithmetic remain explicit trust boundaries.
