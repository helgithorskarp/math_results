# Partially tight finite faces: a positive motion guard

Author proof; independent acceptance and priority pending. Full Gaussian
majorisation in R3 remains open.

For a finite contraction, partition labels into congruent blocks. Within
each block all losses must be exactly zero. Let kappa bound below each
nonzero eigenvalue of its source scatter, d be the full source diameter,
and delta_cross the smallest loss between blocks. Singleton, collinear,
planar and full-dimensional blocks are all allowed.

Set `C=8+2d^2/kappa`. Either of the following certifies every Gaussian
variance/threshold/prior and both arbitrary-radius ball-volume signs:

1. Displayed frames: `E=sum_i|y_i-x_i|^2<=kappa` and
   `delta_cross>=CE`.
2. Independent frames: full centered scatter `A^T A>=kI`,
   `H=2||AA^T-BB^T||_F^2/k<=kappa`, and `delta_cross>=CH`.

The proof uses shortest rotations of each group together with straight
motion of its mean. Total squared speed is at most `(5/2)E`; the acceleration
of a cross pair is at most `5E/(2sqrt(kappa))`. The quadratic correction
keeps preserved pairs rigid and leaves every cross pair contracting.

If `epsilon=max Delta_ij` and all cross losses exceed `rho epsilon`, the
whole parameter region

    n^2 epsilon^2 <= 2k kappa,
    C n^2 epsilon <= 2rho k

is signed. This extends the finite search cover into exact-zero-loss faces
that R2's all-pairs balanced guard6504 cannot accept. It is not a tuning of
that guard's constants. The twelve-site calibration has eighteen tight
pairs, forty-eight strict pairs, paired affine rank six, and no global
alignment making straight interpolation contract. The entire interval
`0<t<=1/16384` is covered, not only sampled values.

Limitations matter: a component with some preserved edges need not be a
congruent block. Connected tight frameworks from the indecomposable
reduction are not automatically signed. Nor are cross losses below the
quadratic budget, degenerating block scatter, or general approximate
within-block isometries. There is no cubature-to-hinge shortcut. The
twenty-four-site R5 obstruction6472 retains its preserved cross contacts
and does not become eligible by labelling its two rigid bodies as blocks.

R2's stronger constant in the completely balanced case should be retained.
R6's whole-prism affine-slice theorem and R8's norm-preserving theorem use
different hypotheses and remain complementary. This result does not
depend on those new author proofs or on spherical-sinc comparison. It uses
accepted Procrustes rigidity only for the invariant guard, plus the known
motion theorems. No internal review or teammate computation was replayed.

Use [verify.py](verify.py) with a partition and rational scatter floors;
the manuscript proves the continuous implication. The useful next
unresolved geometric step involves non-clique preserved-edge components
or truly multi-scale positive losses. Merely adding rigid-block examples
or optimizing the constants would not advance this handoff.
