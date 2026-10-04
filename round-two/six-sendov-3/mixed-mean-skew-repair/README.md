# Mixed real mean and shrinking skew

Six-sendov-3 / researcher. The complete ordinary [proof](PROOF.md) establishes
an explicit degree-nine boundary construction with all nine original roots
strictly inside the disk on a compact-uniform existence collar. Balanced
real means enlarge the attained shrinking-skew and original-motion constants.
The mixed tenth normal has a favorable sign on nonnegative means, permitting
the real-only inward budget; a full physical fifth calculation determines
the attained central skew through order eta^(3/2).

Status: **unformalized author proof; independently unreviewed**. The global
first-power problem and the all-mode fourth coefficient remain open. The
real-only fifth result is credited10288 prior art. See [dependencies](DEPENDENCIES.json)
and [current primary calibration](LITERATURE.md).

Python3.12 or later, standard library only; the author used Python3.12.14.
From this directory:

```bash
python3 -I -B verify.py --stage forcing
python3 -I -B verify.py --stage unit
python3 -I -B -O verify.py --stage unit
python3 -I -B verify.py --stage unit --output /tmp/mixed-unit-record.json
python3 -I -B -O verify.py --stage unit --check /tmp/mixed-unit-record.json
python3 -I -B validate.py --scratch /tmp/mixed-validation-unique-empty-directory
```

From the repository root use the corresponding path
`round-two/six-sendov-3/mixed-mean-skew-repair/verify.py`.
The verifier sets all six native thread settings to one. Validation launches
one serial child at a time with a fixed45-second guard per child and uses
an initially empty scratch directory outside the source. A timeout is an
incomplete computation and does not prove any mathematical conclusion.

`EXPECTED.json` contains small fingerprints of the complete regenerated
forcing/unit records, with237/370 whole identities respectively. Whole
mathematical coefficient maps are checked before digest comparison; `--check`
additionally compares every nested type and coefficient of a full saved record.
Both physical scalar routes and all nine actual original branches are retained.
The full records and verbose validation logs are generated outside source and
deliberately omitted from Git. `SOURCE.json` seals every declared local source
file before import. `VALIDATION.json` records the bounded reproduction suite;
it is a receipt, not an independent proof or a mathematical input.

The unchanged same-author arithmetic and series engines are credited. The
older `series.direct_first_power` is only a lower-order routine and is not used
for the fifth calculation; `calculation.direct_first` includes the essential
fifth binomial and pair-variance terms through epsilon11. The new source has
no runtime parent fixture, private directory or external package dependency.
