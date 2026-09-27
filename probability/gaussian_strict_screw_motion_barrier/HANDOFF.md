# The R5 obstruction survives an explicit open metric box

Author proof; independent acceptance pending. Full Gaussian majorisation
remains open.

For the original 24-site pair P,Q at graph6472, every labelled pair
P',Q' satisfying

    max_(i,j) |D(P')_ij-D(P)_ij| <= 2^-136,
    max_(i,j) |D(Q')_ij-D(Q)_ij| <= 2^-136

has no continuous R5 contracting motion. D denotes **squared** distances.
The allowed perturbations are arbitrary, with separate endpoint frames;
they need not preserve either rigid group or any of the 156 tight pairs.
This is a finite obstruction guard for actual rational endpoint data.

The explicit strict control is P mapped to `(1-2^-145)Q`. It has 276
strict pairs, zero tight pairs, paired affine rank six, and no pair of
norm anchors. The exact source and target coordinates are in
[WITNESS.json](WITNESS.json). The checker verifies the metric guard and
single-step anchor obstruction independently from their saved outputs.

The geometric increment is quantitative stability of the halfway barrier:

1. Approximate within-group distances allow each intermediate group to
   be moved by at most `32 sqrt(delta)` into an exactly rigid group in
   the same ambient space. This repairs one hypothetical placement;
   it does not assume a rigid perturbed motion.
2. Five contact errors pin the almost preserved axis. A small rotation
   repairs that axis while keeping the translation of B0 fixed.
3. The resulting three-by-three Gram matrix would contain three vectors
   in only two auxiliary dimensions, hence have determinant zero. The
   exact lower bound after all errors is `7921/4194304>0`.

The distance-defined height from R7 crosses one half along any candidate
motion, so this one-placement contradiction excludes every continuous
motion, without assuming a particular schedule.

R7's [6524](../gaussian_screw_primitive_obstruction/PROOF.md) already
excludes an existential neighborhood from arbitrary finite mixtures of
norm-preserving and R5-motion steps. This package makes only its **R5
component** effective. It does not compute the radius needed to separate
all intermediate R3 states or anchored bridging steps. Consequently no
mixed-chain exclusion is asserted for the particular factor `1-2^-145`.

The new finite guard is useful even when preserved-contact preprocessing
finds nothing. It does not sign a Gaussian hinge, challenge the known
positive classes within their hypotheses, or create a new motion class.
The last pass's [all-frame screw/meridian classification](../gaussian_screw_meridian_boundary/PROOF.md)
remains closed; it is not extended by another motion schedule here.
R6 retains the broad positive geometric class and priority comparisons.

R1's new compact eventual theorem and R8's fixed-variance neighborhood
theorem retain their separate hypotheses and author-proof status. No
contrary Gaussian evidence is claimed for this control. The remaining
headline obligation is the actual finite-variance comparison, beyond a
universal R5-motion proof route.
