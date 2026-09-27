# Gaussian comparison with preserved rigid groups

The [author proof](PROOF.md) gives an explicit finite endpoint certificate
for a contracting motion in R3. Distances inside each supplied group are
preserved; distances between groups decrease enough to absorb a quadratic
rotation error. Groups may have affine dimension zero through three.

Every certified input has Gaussian majorisation for all priors, variances
and thresholds, and both arbitrary-radius Kneser--Poulsen volume signs.
The unrestricted problem, independent acceptance and historical priority
remain open. This is a sufficient parameter-family cover, not an exhaustive
decision procedure or a new proof of the classical motion comparisons.

The [handoff](HANDOFF.md) gives the exact finite-frontier interface and
limits. [SOURCES.md](SOURCES.md) credits the accepted Procrustes identity,
R2's balanced-loss motivation and the classical comparison theorems.

Reproduce from this directory using CPython3.11 and the standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py INPUT.json
sha256sum -c SHA256SUMS
```

The first two commands must match [EXPECTED.json](EXPECTED.json), including
`RIGID_BLOCK_ALL_VARIANCE_CONTROLS_PASSED`. The checker reconstructs 66
pair-loss polynomials, verifies positive Bernstein coefficients over an
entire interval, checks eleven finite controls and rejects three malformed
inputs. It uses no floating-point arithmetic, quadrature, solver or private
input. The mathematical motion is proved in the manuscript; the program
checks its rational hypotheses and algebraic controls.

To certify a new input, use the schema of [INPUT.json](INPUT.json):

- `x`, `y`: equally sized arrays of three rational coordinates, each given
  as an integer or a string such as `"1/3"`; source sites must be distinct.
- `blocks`: at least two nonempty arrays partitioning the zero-based labels.
  Every distance within each block must be preserved.
- `kappa`: positive rational floor on every nonzero eigenvalue of every
  nonsingleton block's unweighted centered scatter.
- `mode`: `direct` for the displayed-frame squared error E, or `invariant`
  for the Gram-error upper bound H after optimal endpoint alignment.
- `k`: positive rational global scatter floor, required for noncongruent
  inputs in invariant mode; harmless and unused in direct mode.

`CERTIFIED_ALL_VARIANCES` and `CERTIFIED_CONGRUENT` are positive verdicts.
`NOT_CERTIFIED` supplies a failed-hypothesis or failed-budget reason and
does not assert a negative Gaussian comparison. Malformed inputs fail with
a nonzero exit. Successful parsing of a negative certificate is not itself
an execution error, so consumers must inspect `status`.

Exact input checking takes O(n^2) rational operations and O(n^2) memory;
rank and PSD calculations have dimension at most three. Integer bit cost
depends on the input. The small packaged controls require no substantial
compute. This is not proof-assistant output or independent review.
