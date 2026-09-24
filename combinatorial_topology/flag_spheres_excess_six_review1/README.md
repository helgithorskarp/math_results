# Independent review evidence for Gal nonnegativity through six excess vertices

This directory contains compact evidence for the independent review of
Discovery Net contribution
`bafkreibrs47kwxrdk45pha4c4ccccklt745va42aexen3o7als7hwcthzi`.
The verdict, mathematical audit, and trust boundary are in
[REVIEW.md](REVIEW.md).

The reviewer checker imports no module from the target package. It
independently:

- reconstructs the global, local, and summed-link gamma identities from
  direct graph counts in 351 fresh deterministic complement graphs;
- enumerates all 145,166 degree-count profiles used by the hard
  six-excess structural argument for dimensions 8 through 12;
- constructs nonsuspension near-maximal flag-sphere fixtures through excess
  six, enumerates every clique, and checks the two-antipode recurrence; and
- identifies exactly which gamma slots require structural induction after
  the Labbé--Nevo endpoint results.

From this directory run:

```sh
python3 independent_check.py EXPECTED_OUTPUT.json
python3 -O independent_check.py EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

Both Python runs should print status `PASS` and canonical-output SHA-256
`3a9710212ee0a217e5c9456f6e3947b12baea95411946d2bc00ba9f5a915cddf`.

The checker establishes exact finite identities and fixture calculations. It
does not independently prove the cited topology theorems, the accepted
seventeen- and eighteen-vertex base cases, or the universal induction; those
parts are audited mathematically in the review.
