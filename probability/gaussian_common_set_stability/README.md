# Quantitative Gaussian common-set stability

For every fixed finite contraction and every isometric-reference Gaussian
top set, [PROOF.md](PROOF.md) establishes an explicit lower bound

    common-set gap >= expected squared pair-distance loss / C
                   >= 4s(4 pi s)^(n/2) second-energy gap / C.

The constant is uniform over all actual prior weights, including zero
weights. Translation of the target set supplies the missing term when
all pointwise reference slacks vanish. A fixed reference, positive variance
and positive finite volume are required; compact windows are also covered.

The quantitative result builds on researcher 5's
[qualitative isometric-reference theorem](../gaussian_isometric_reference/PROOF.md).
It does not repeat that classification. [INTERFACE.md](INTERFACE.md) gives
the finite-atomic lane the coefficient enclosures and exact geometric data
needed for a certificate, plus a convex quadratic lower model of the
common-set objective.

For the actual profile gap, an additional source-set error must be
subtracted. If the actual and reference source densities differ by at most
epsilon in supremum norm, that error is at most

    integral (epsilon-|reference density-reference level|)_+.

This is o(epsilon), including critical levels. The proof gives a signed
comparison criterion with this cost included. It does not infer full
majorisation from second energy alone or cover arbitrary source sets.
The unrestricted R3 question remains open; no new Kneser--Poulsen class or
unknown numerical comparison is claimed.

Status: complete author derivation; independent mathematical review and
formalization are pending. No program, numerical enclosure, solver,
experimental search or hidden dataset is a premise. Read the analytic
proof and the input/output contract. [SOURCES.md](SOURCES.md) attributes
all ingredients; [INPUTS.json](INPUTS.json) pins the team inputs.

From this directory, check source integrity with:

```sh
sha256sum -c SHA256SUMS
```

Expected: five `OK` lines. This verifies bytes, not the theorem. The input
commits and hashes can be checked with ordinary `git show COMMIT:PATH` and
SHA256. The proof includes all constant branches, an analytic degenerate
control, and the explicit remaining full-question obligations.
