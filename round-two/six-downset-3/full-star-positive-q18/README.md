# Positive q18/k9 Hoffman certificate

six-downset-3, researcher,2026-10-04. A new rational matrix on the
explicit21-point downset (N278/s58) has every allowed entry>=1/2048,
including the actual empty vertex and loop. Its complete29,802-coordinate
REAL box |t_j|<=1/3814656 retains the same entry floor, both endpoint
ranks277 and simple extremal eigenvalues. Center lower gap1/7040, box
lower gap1/14080; both upper gaps>=1/2048. The new nonstar mass
redistribution exits the prior one-sided obstruction cone. No generalH/I,
other carrier, optimality or historical-priority claim is made.

Read [PROOF.md](PROOF.md). Ordinary bridges are unformalized and this
new point is independently UNREVIEWED. The separate verifier is by the
same author. The older q18 signed result and earlier reviews concern
other matrices; no parent PSD factor, floor or verdict is adopted.

Reproduction uses Python3.11.2 or3.12.14 and the standard library only.
From this directory choose an output path that does not yet exist:

```sh
python3 -I -B validate.py --out /tmp/q18-positive-validation.json
```

This seals the entire defining source before reading mathematical inputs,
then runs three serial normal/optimized/cold replays. Whole outputs must
equal EXPECTED.json. Fourteen semantic defects reject in both modes.
Every child has a fixed45-second guard and all six native thread counts1.
A timeout, exception, incomplete run or resource kill is not mathematical
nonexistence evidence. Runtime depends on the reader's machine.

Individual exact replay:

```sh
python3 -I -B check.py --out /tmp/q18-positive-record.json
python3 -I -B -O check.py --out /tmp/q18-positive-optimized.json
```

CERTIFICATE.json gives all143 new integer values over1048576 and six
new dyadic triangular factors plus six scalar certificates.
COMPARISON.json gives only the preceding signed center's143 values to
check the exact repair mass/loop accounting, with no old PSD premise.
All original proper positions, actual positions, complete physical
basis actions and real-generator lift bounds are regenerated.
EXPECTED.json stores compact results AFTER these exact checks, never
external factors or numerical eigenvalues. SHA256SUMS and BUNDLE.json
bind the source closure; generated records remain in the chosen scratch
path. Numerical phase-I and factor rounding proposed the new values;
NumPy is not a dependency of the proof replay.
