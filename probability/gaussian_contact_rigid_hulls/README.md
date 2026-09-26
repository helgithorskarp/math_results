# All-threshold Gaussian comparison near rigid convex configurations

For **every fixed finite source spanning R3 in general position**, with arbitrary
positive weights, this packet proves Gaussian majorisation for every
sufficiently close contracted image, at a fixed variance and
**simultaneously at all thresholds and all finite positive volumes**.
Every nonisometric pair in the explicit neighborhood has a strictly positive
profile gap. There is no bound on the number of atoms. The more general
geometric hypothesis is a rigid convex hull with every remaining source
site strictly inside it.

This is a complete author proof; independent review is pending. The general
dimension-three conjecture remains open. The neighborhood depends on the
variance, geometry and positive weights; no new Kneser--Poulsen consequence
or uniform theorem for Gaussian-regularized unbounded inputs is asserted.

The new analytic step is a relative tail estimate for any separated finite
straight deformation. If delta is its maximum site displacement, then

    [H_target(a_R)-H_source(a_R)]/(a_R R^2)
        = W(source)-W(target) + error,
    |error| <= delta * explicit O(log R/R),
    a_R=(2 pi)^(-3/2) exp(-R^2/2).

Here W is the unnormalized spherical support integral. Hull-edge rigidity
and the contraction constraints at interior atoms give
W(source)-W(target)>=c delta after Procrustes alignment. This closes
the entire low-threshold tail, while the independently accepted local
profile theorem covers all remaining thresholds. The earlier theorem's
volume ceiling is therefore removed under the stated finite-geometric
hypothesis. No continuous contracting path is assumed.

- [Proof, explicit constants and contact consequence](PROOF.md).
- [Attribution, dependencies and R5/R8 handoff](SOURCES.md).
- [Exact rational audit](audit.py) and [expected output](EXPECTED.json).

From this directory, using CPython 3.11 or later and only its standard library:

```sh
python3 audit.py --check
python3 -O audit.py --check
sha256sum -c SHA256SUMS
```

Expected status: `RIGID_HULL_RELATIVE_TAIL_EXACT_CONTROLS_PASS`.
The audit runs in less than a second. It certifies a seven-vertex rational
source's 10 hull facets, 15 edges, rigidity rank 15, gauge rank 21 and
positive constants, then certifies an eighth interior atom's depth and
coercivity constants. It also checks the finite arithmetic in the tail bound.
Deleted-edge and cube controls fail the rank condition as intended.
These checks do not mechanize the analytic proof or establish independent
acceptance. There is no quadrature, numerical solver, large certificate,
external dataset or hidden computation.
