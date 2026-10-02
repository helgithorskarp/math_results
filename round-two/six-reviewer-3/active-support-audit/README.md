# Independent near-middle support audit

Actual reviewer **six-reviewer-3**, independent mathematical reviewer.
[Full review and proof](REVIEW.md) confirms committed9201 and strengthens
its sufficient tail criterion from6 to2: `2n^2 B_(n,k)<=2^(n-1)` for
integer `n>=64, 2<=k<n/2`. It improves the logarithm from `log(12n^2)`
to `log(4n^2)` and forces set sizes17/41/92 at orders64/128/256.
A direct original-coordinate proof gives a quantitative signed outside-
support functional bound without averaging or harmonic completeness.

From this directory with the CPython standard library:

```sh
python3 -I -B audit.py
python3 -I -B -O audit.py
python3 -I -B replay.py
```

The first two regenerate the entire independent [EXPECTED.json](EXPECTED.json).
The replay fetches/hashes eight public pinned author files, verifies the
complete source record and all shared coefficient vectors, runs both
engines in separate serial normal/optimized processes and rejects six
damaged independent fixtures. It uses45-second child guards, all six
native-thread variables1 and an isolated, explicit source-directory
bootstrap for the author's local imports. `--input-directory PATH`
accepts already downloaded inputs named by [INPUTS.json](INPUTS.json).
[VALIDATION.json](VALIDATION.json) records the completed runs.

Closed profiles/base formulas and earlier polynomial certificates retain
source credit. The new dense normalized Q(n) engine and direct-index
checks import no researcher executable. Real PSD/affine/cancellation,
moment and Chernoff bridges are ordinary unformalized mathematics.
Centering/cap are extra hypotheses; no existence, optimality or general
spectral H/I resolution is asserted.
