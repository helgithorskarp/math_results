# Full Gaussian comparison for orthocentric depth-one flaps

This packet proves Gaussian majorisation for every nonnegative weighting
of the sixteen-label orthocentric flap map, at every positive Gaussian
variance. It also proves both the union and intersection Kneser--Poulsen
volume inequalities for arbitrary assigned radii on this family.

The tetrahedron satisfies v_i.v_j=-c<0 for i!=j. Its anchors stay fixed;
the directed flaps move from v_j-v_i to v_j+v_i. The class includes
asymmetric tetrahedra, all zero/nonzero weight patterns and unequal radii.
It is a fixed positive-depth result, with no small-variance or shallow-depth
qualification. The unrestricted dimension-three problem remains open.

The new construction uses one vertex of outdegree one in a tournament
selector. Two tail directions move at opposite hyperbolic time shifts,
leaving exactly one varying Gram entry. Every affected distance has a
strict contraction margin:

    h_k-2 delta exp(-d) = B^2+AB exp(-d)(2-exp(-d)) > B^2 > 0.

Together with the existing sink motion, this covers all 64 selectors and
closes both ten-point template obligations in
[researcher 7's reduction](../gaussian_flap_tournament_reduction/PROOF.md).
The common-target mixture gives the full Gaussian theorem. Choosing the
larger or smaller radius at each merged target gives the full union or
intersection theorem from the selector motions.

The full sixteen-label motion itself is not supplied: an exact rejection
control shows why the new path fails when all directed flaps move at once.

- [PROOF.md](PROOF.md): universal construction, sign estimate and consequences.
- [verify.py](verify.py), [EXPECTED.json](EXPECTED.json): exact finite controls.
- [VERIFY.md](VERIFY.md): reproduction commands and trust boundary.
- [SOURCES.md](SOURCES.md): primary literature and prior team dependencies.
- [HANDOFF.md](HANDOFF.md): precise closure, review obligations and scope.

Run from the repository root:

```sh
python3 probability/gaussian_flap_selector_motion/verify.py
```

Only the Python standard library is required. The computation uses exact
rational arithmetic and takes a few seconds. It verifies finite algebraic
controls; the universal claim is the written proof and its cited analytic
and geometric transfer theorems.

**Status:** complete author proof, with independent mathematical review
and formalization pending. This is not an independently accepted resolution
of the campaign's headline objective, and no unrestricted theorem is claimed.
