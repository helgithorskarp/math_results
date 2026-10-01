# Exact degree-nine angular optimizers below the moving-pair interval

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.

The [written proof](PROOF.md) evaluates the collapsed-root angular quartic
functional for every marked radius

\[
\frac{10\sqrt{305}-105}{164}\le a\le
\frac{6\sqrt{101}-29}{52},\qquad
0.42464934\ldots\le a\le0.60190872\ldots.
\]

An exact spectral sum of squares gives the global optimum and its complete
equality set. The optimizer is the real root multiset of an explicit even
degree-eight polynomial depending on one parameter. It passes through
normalized Hermite-8 roots at `a=(2 sqrt(46)-7)/12`, has eight distinct
slopes in the open interval, and reaches two double outer slopes at the
lower endpoint and the moving pair at the upper endpoint. On compact
interior radius sets the spectral deficit controls squared root-vector
distance to the optimizer orbit, with an existential constant.

The source also evaluates the leading full-disk small-energy minimum
using the expressly cited prior all-radius variational reduction.
It does not classify actual finite-energy minima or prove the unrestricted
first-power Tang--Zhang inequality. The angular functional, its analytic
bridge, the prior moving-pair interval, and the full-disk reduction retain
their authors' credit in [LITERATURE.md](LITERATURE.md).

## Reproduce the exact algebra

From the publication repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B round-two/six-sendov-2/angular-square-optimizer/verify.py
```

Tested with CPython 3.11.2; the Python standard library is the only
dependency. All arithmetic is exact over the rationals. No generated data,
solver, eigensolver, network input, or external proof corpus is required.
The required [expected.json](expected.json) compares complete records;
`--write-expected` is an explicit maintainer operation, not a reproduction
command. Verification also works under Python optimization.

Expected output:

```json
{"damage_controls": 5, "identities": 25, "record_sha256": "23991b096f6cbce356cf2800e20981eab9496e818c5a941a95bc2db49f87bdc8", "records": 35, "status": "all exact checks passed"}
```

The checker validates the projection traces, square completion, entire
ODE and coefficient recurrence, collision-location factorization,
endpoint factorizations and moments, exact radius polynomials, and the
Hermite root response. Its five damage controls are author validation.
The spectral/Schur-complement interpretation, real-root continuation,
uniform local inverse estimate, compactness, and the cited full-disk
analytic reduction remain ordinary mathematics outside a formal kernel.
Independent review of this new result is pending.

The next frontier is below the lower endpoint, where this attained
equality polynomial has two double outer slopes. Finite-energy
continuation is another separate question.
