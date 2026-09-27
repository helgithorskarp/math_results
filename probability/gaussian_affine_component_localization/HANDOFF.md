# Uniformity interface for the R2/R3/R8 spine

The deliverable is one support-level guard, not a new threshold join.
It signs an entire small-loss sector at every variance, with no number of
atoms in the constants. Its proof is complete at author level and awaits
independent acceptance.

## Mathematical interface

Supply a bounded domain split into finitely many compact components, an
affine contraction on each component, and a globally contracting endpoint
map. Supply any auxiliary law whose component masses are at least `m`,
whose conditional covariances exceed `kappa I3`, and whose global covariance
exceeds `k I3`. The law ultimately being compared can be entirely different,
atomic or diffuse, with arbitrary component masses.

Compute the auxiliary centered squared Gram norm `F`, and bound the domain
diameter by `d` and every cross squared-distance loss below by `delta`.
The two checks are exactly

```text
2F/(km) <= kappa/4,
delta >= (4+78d^2/kappa) 2F/(km).
```

They certify all Gaussian hinge signs for all `s>0,h>=0`, and both
arbitrary-radius ball-volume inequalities for every finite center selection.
If every cross loss is at least `rho epsilon`, with `epsilon` the largest
pair loss, it suffices that the auxiliary mean loss obey

```text
D <= 2rho k m/(4+78d^2/kappa).
```

The bound improves toward zero loss and remains independent of discretization
inside components. At `F=0` the map is an ambient isometry on the domain.
Component count is bounded by `1/m`; it is not unrestricted at fixed `m`.

## Exact box interface

The input schema is demonstrated in [`INPUT.json`](INPUT.json): each
component has a source center, target center, three positive halfwidths,
a 3-by-3 matrix and a positive auxiliary weight. Numbers are integers or
rational strings; weights sum to one. Global and conditional covariance
floors are positive rational inputs. The auxiliary conditional laws are
uniform volume in the boxes.

[`certificate.py`](certificate.py) checks matrix contraction, covariances,
and a lower bound valid on the whole cross product of every pair of boxes.
Thus no additional unchecked actual-map premise remains for a successful
record. The producer uses `O(B^2)` fixed-size rational operations and `O(B)`
storage. The separate [`verify.py`](verify.py) reconstructs the Gram error
from 27 cubature points per box and checks all 64 corners of the
multiaffine cross remainder. It does not assume that the full quadratic
achieves its minimum at a corner.

All thresholds and scales are conclusions, not input grid dimensions.
The full audit also exercises equality, independent target reflection and
translation, scale covariance, two unresolved controls, six damaged records,
eight malformed inputs, seven dependency pins, and the universal parameter
inequalities in the proof.

## What this adds and what remains missing

R4's rigid-block rotation/acceleration mechanism is retained. Auxiliary
covariance supplies uniform affine control; polar paths permit nonzero
within-component losses. Their acceleration contains the additional term
`2 Omega (S-I)`, which is explicitly budgeted. R4's arbitrary-rank rigid
blocks are not all included in this full-rank component theorem.

This signs a sector left outside an eventual large-variance statement,
without selecting a reference Gaussian scale. R8's fixed-variance spatial
and prior perturbations and the accepted support-cap eventual localization
retain their own advantages and hypotheses. R1's new compact-width rigidity
claim is context, not a dependency of this argument.

The present guard fails in general on adjacent affine cells with cross-tight
contacts. It supplies neither a reduction of arbitrary nonlinear maps to
these cells nor a sign certificate for the unrestricted paired-cubature
frontier. A failed record gives no negative hinge. The unrestricted theorem,
counterexample, and any campaign completion gate remain unresolved.

The useful next boundary is a controlled relaxation of the affine or cross
loss hypotheses. Refining the three-cube calibration alone would add no
new uniform frontier.
