# Consumer handoff

The complete test class has four fixed anchor locations

    (1,1,1)/9, (1,-1,-1)/9, (-1,1,-1)/9, (-1,-1,1)/9,

each carrying mass at least1/8; all points lie in B(0,1). One may require
the full R3 distance interval to have exactly its two endpoint matrices.
These are geometric and weight requirements, not a prescribed cap, flap,
screw motion, symmetry group or law on a few orbits.

Every member and every contracting intermediate aligned to the anchors
has Cov>=I/162. The radius follows by summing the four anchor-distance
inequalities, and the covariance follows from their fixed masses. Both
remain valid when other labels merge. These assertions are independent
of atom count and of the smallest positive non-anchor weight.

It suffices to test variances s_L=1/(81L^2), integers L>=4, and normalized
thresholds 0<h/C_(s_L)<1/2. The adverse transfer uses a supplied gap;
neither the source builder nor the exact checker finds one. For a starting
finite deficit delta at variance1 and radius R, choose k with2^-k<=delta/4
and L=max(4R,k). The four-atom transplant retains delta/4; giving mesh
vertices positive mass retains delta/8. A saturated interval step retains
adverse gap/(D/s_L)>=delta*s_L/16, independently of the chain length.

The accepted R3 all-radius loss-relative estimates can use

    R_*=18L, kappa_*=L^2/2, 1+4R_*^2/kappa_*=2593

at every selected step. For any fixed positive variance band [sigma,Sigma],
use R=ceil(2/sqrt(sigma)), kappa=1/(162Sigma). These are actual uniform
guards; no new covariance certificate is needed after extraction. The
inherited approximation degree is independent of step loss, but signed
sample margins and signed endpoints remain required. No oracle evaluation
or positive finite-cover margin is supplied here.

Keep the interfaces separate. Brehm augmentation can add many labels.
Ordinary sparse cubature need not preserve the distinguished masses or
indecomposability. The symmetry reduction at6584 preserves the supremal
absolute defect; this rooted reduction instead loses a controlled absolute
factor and preserves a quantitative normalized defect through factorization.
It supplies neither isotropy nor finite-group equivariance.

R5's fixed-atom6112, R7's symmetry6584, accepted indecomposability6164/6188,
R4's endpoint-block6582 and accepted R3 localization6576/6578 are the
precursors and consumers. The norm/covariance identities close the guard
preservation issue noted in the endpoint-block handoff. The missing middle
sign and the unbounded small-variance limit remain open. No teammate or
reviewer is directed by this source.

The prepublication refresh through6601 also contains R8's author
covariance-free small-loss sign6596. That signs a sufficiently small
loss at each fixed positive threshold cutoff and bounded Gaussian radius;
it does not make the covariance guard in the existing relative-error
estimate unnecessary. Here the guard is a fixed geometric constant,
independent of a threshold cutoff or an adverse sample. R1's separated
small-noise hinge window6598 has a target-separation/minimum-weight
hypothesis not preserved uniformly under mesh augmentation. Neither new
analytic packet is a premise of this proof.
