# A loss-proportional transfer from spherical gaps to Gaussian hinges

The [author proof](PROOF.md) strengthens the existing spherical-tail
approximation for every bounded law and contraction in R3. For support
radius R, variance `s>=64R^2`, and `lambda R>=1/2`, its error is bounded by

```
(mean squared-distance loss / s)
    * [1 + 25 lambda R (1+lambda R)^2 exp(4 lambda R+1)].
```

The approximated quantity is the actual favorable Gaussian hinge at
`b=(2pi s)^(-3/2) exp(-lambda^2 s/2)`, divided by `4pi lambda s^2 b`.
The comparison quantity is the spherical average of the difference of
the source and image log moment-generating functions.

A positive spherical margin normalized by the same distance loss now gives
a variance bound independent of that loss. The accepted high-noise window
overlaps the resulting middle interval. An independently signed tail with
an overlapping cutoff completes a global zero-defect certificate. The
spherical margin and tail are still premises; they are not established
for unrestricted contractions here.

No dominant atom, minimum mass, atom-count bound, covariance condition or
positive loss floor is required. The result is uniform on compact spherical
parameter intervals. Its constant grows exponentially at large parameters.
This is a relative error theorem, not a new unconditional map class or a
Kneser--Poulsen consequence. Independent review is pending.

From the repository root, with standard-library Python 3.11 or later:

```bash
python3 probability/gaussian_relative_spherical_transfer/verify.py
python3 -O probability/gaussian_relative_spherical_transfer/verify.py
```

Both print [EXPECTED.json](EXPECTED.json), status
`EXACT_RELATIVE_TRANSFER_CHECKS_PASS`. The exact checker verifies a formal
radial derivative, rational coefficient and modal budgets, and a two-point
calibration including arbitrarily small losses. That already positive class
is only a control. The checker does not establish the general spherical
margin premise or replace the written continuum proof.

[SOURCES.md](SOURCES.md) records dependencies and the distinction from the
previous absolute-error endpoint theorem and dominant-atom window.
