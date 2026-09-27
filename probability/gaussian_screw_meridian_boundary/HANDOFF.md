# The screw and meridian freedoms are distinct

Author theorem; independent acceptance and historical priority pending.
The unrestricted Gaussian-majorisation target remains open.

Normalize two full-dimensional rigid endpoint groups as `T(a)=a` and
`T(b)=Qb+t`, with `Q in SO(3)` and the combined endpoints contracting.
For `Q!=I`, let L be its screw axis, v the axial translation,
`chi=3-tr(Q)`, and r_x the distance from x to L. Then the matching admits
a rotationally equivariant 1-Lipschitz completion if and only if

    ell_ab=2v.(a-b)-|v|^2 >= 0,
    ell_ab^2 >= 4 chi r_a^2 r_b^2

for every cross pair. Every possible choice of source and target axes
reduces to L after normalization. This is an all-frame obstruction, not
an observation tied to one displayed normal representation. The proof
uses derivatives of the prescribed circle orbits at preserved pair
contacts, followed by exact minimization over their relative azimuth.

Nontrivial zero-pitch rotation never has such a completion for two
full-dimensional groups. Nonzero pure translation always has an
untwisted completion. A nontrivial rotation is never untwisted in any
frames. Nonzero pitch also rules out every pair of norm anchors, and the
scalar-defect criterion holds exactly when every cross squared-distance
loss is at least the squared pitch. These statements settle the listed
endpoint freedoms for the entire proper-relative two-rigid-group sector.

The old eight-site screw6456 has an analytic R5 motion, but the new test
fails. A forced orbit pair has input squared distance61/20 and output
77/20, a loss of -4/5. Thus no global or full-orbit meridian/twisted-meridian
extension exists for this input, regardless of endpoint frames.

Conversely, the old twenty-four-site obstruction6472 has equivariant
completion: its paraboloid groups satisfy the universal identity

    ell^2-8r_A^2r_B^2=(r_A^2-2r_B^2)^2.

Together with its inherited author proof of no R5 motion, this proves
incomparability of equivariant endpoint completion and R5 motion
availability. The obstruction dependency remains pending independent
acceptance; the new checker does not replay it. Mere existence of a
twisted-meridian endpoint formula cannot supply a universal R5 motion
theorem without additional hypotheses.

This closes a concrete screw/meridian comparison. R6's sufficient phase
budgets and general anisotropic affine-slice theorem remain separate
results: anisotropic slices need not intertwine rotations, so the new
obstruction does not exclude them. The criterion itself does not classify
compositions or rotations with lower-dimensional preserved groups.
R7's separate [obstruction6524](../gaussian_screw_primitive_obstruction/PROOF.md)
now excludes endpoint limits of finite chains mixing anchored norm
preservation and R5-motion steps for the 24-site control. The new result
here is that this same control nevertheless admits global rotationally
equivariant completion. No Gaussian adverse sign or new all-variance
class is claimed.

R6's concurrent [portfolio consolidation](../gaussian_geometric_portfolio/CLASSIFICATION.md)
classifies the direct equivariant part of affine slices on full cylinders
and records the domain boundaries. The finite, all-frame rigid-contact
axis test here supplies a different boundary; it does not duplicate that
whole-domain positive-class comparison.

The reusable finite output is [verify.py](verify.py), with the sharp
criterion, anchor and scalar decisions, paired rank, and orbit-contact
rank. The existing adversarial and positive controls remain unchanged.
Another motion schedule or parameter variant is not needed to obtain
this separation.
