# Degree-nine first-power monotone and angular cases

Author: **six-sendov-1**, role **researcher**. Complete ordinary written proof;
independent review of this contribution is pending.

For degree-nine disk-root polynomials, [PROOF.md](PROOF.md) establishes:

- At a real root of a real polynomial monotone between the origin and that
  root, the first-power reciprocal sum is at least eight, strictly inside
  the disk. Complex critical points are allowed. A reflection-axis version
  gives the chord-radius bound `8/sqrt(1-h^2)`.
- At a normalized interior root `a`, angular loss
  `A=sum(|q_j|-Re q_j) <=(1-a)/2400` forces the sum to exceed eight.
  In particular `max |arg q_j| <=sqrt((1-a)/9600)` suffices.
- A hypothetical failure must pay the signed and coordinate-weighted phase
  budgets in equations (12)--(13). Odd losses help the origin estimate.
- An exact monotone family has all roots strictly inside the disk while its
  product of the eight other root distances exceeds nine, separating it
  from the existing elementary product-distance sufficient criterion.

The main input is the [preceding positive-coordinate origin gap](../sendov_degree9_collinear_critical_first_power/PROOF.md),
with its 636-entry exact certificate. The new quadratic angular condition
contains that source's earlier linear phase condition. The basic phase
inequality is credited to the complementary lane, and the small-parameter
example uses its already proved root-containment family. A
[concurrent independent review](../sendov_degree9_collinear_critical_review3/README.md)
already proves a quadratic unweighted phase criterion. The signed,
radial-weighted criterion here has actual examples outside that region;
the quadratic order itself is not claimed as new.
The full interior first-power Tang--Zhang conjecture remains open here.
See [LITERATURE.md](LITERATURE.md) for status and prior-art boundaries.

From the repository root, CPython 3.10 or later (tested with 3.11.2):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 sendov_degree9_origin_angular_monotone/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify_interpolation.py
```

The first command checks the new exact algebra and constants and rejects
three mutations; [expected.json](expected.json) records its compact output.
The other commands replay both exact algorithms for the input's complete
636-entry certificate. All use the Python standard library. Written analytic
bridges are not proof-assistant formalizations.
