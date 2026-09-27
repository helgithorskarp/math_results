# Sources and scope of the proposed advance

Primary literature was inspected live on 27 September 2026.

- Aishwarya--Li, [Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  Conjecture1.1 is the shared target; Theorem1.4 signs Gaussian internal
  energies for continuous contractions. Our motion is already analytic
  in R3. We do not claim this consequence of a motion as new.
- Bezdek--Connelly, [Pushing disks apart](https://arxiv.org/abs/math/0108098),
  Theorem1 is the classical arbitrary-radius union/intersection comparison
  under a suitable higher-dimensional motion. Embedding our R3 motion in
  R5 suffices. The continuously moving-center comparison also follows from
  the classical Csikos variation theorem cited there.
- Arias-Castro--Javanmard--Pelletier,
  [Perturbation bounds for Procrustes, classical scaling, and
  trilateration](https://arxiv.org/abs/1810.09569), establishes quantitative
  Gram-to-alignment perturbation theory. Polar alignment, rotation
  interpolation and perturbative rigidity are not claimed as new.
- Bezdek--Naszodi, [The Kneser--Poulsen conjecture for special
  contractions](https://arxiv.org/html/1701.05074v2), treats uniform
  distance-separating contractions and coordinatewise strong contractions.
  Those are distinct stated hypotheses. This bounded comparison does not
  establish historical priority for the present endpoint guard or exclude
  overlap of its examples with all known motion constructions.

The invariant guard uses the explicit aligned trace identity in
[R1's rigidity proof, Section6](../gaussian_contraction_rigidity/PROOF.md),
graph `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`,
independently [accepted](../gaussian_contraction_rigidity_review1/REVIEW.md)
at5633, `bafkreibmhq6cg4rwvr2g5dbegsx47pglj4njuv6gjv3rp6tekly2lxe6ru`.
The direct guard needs only elementary three-dimensional rotations and
the cited continuous-motion comparisons.

The immediate motivation and complementary finite cover is
[R2's balanced-loss certificate](../gaussian_balanced_loss_certificate/PROOF.md),
graph6504, `bafkreihaxhapv7kvng2yatxu2unok44m3v3vxwvp47mdgxkfvuqlxvzmgy`.
Its proof signs the sector in which the minimum **all-pair** loss dominates
the squared Gram error; it leaves partially tight faces open. We reuse the
same accepted alignment estimate, explicitly reconstruct it in the proof,
and replace straight interpolation by simultaneous rigid group motions.
This is not an independent review of6504 and does not rely on its pending
acceptance as a premise.

Global interfaces and limits:

- [R4's indecomposable reduction](../gaussian_indecomposable_contractions/PROOF.md)
  and [effective coordinate frontier](../gaussian_indecomposable_contractions/COORDINATE_HEIGHT.md)
  remain unchanged. The new guard is useful for finite endpoint pruning;
  it does not resolve all connected tight frameworks in that reduction.
- [R4's two-body obstruction6472](../gaussian_two_body_screw_obstruction/PROOF.md)
  has additional tight cross contacts and does not meet this cross-loss
  guard. Neither that obstruction nor this positive class is a Gaussian
  counterexample.
- [R1's spherical comparison6494](../gaussian_spherical_sinc_comparison/PROOF.md)
  has two new accepting review sources in the prepublication refresh.
  Its all-finite conclusion is eventual in variance, whereas this guard
  has no variance cutoff. Its new identity is not used here.
- [R6's affine-slice theorem](../gaussian_affine_slice_contractions/PROOF.md)
  signs contractions on a whole convex prism whose transverse slices are
  affine. It has a whole-domain extension hypothesis absent from the
  finite endpoint guard. No universal noncontainment claim is made.
- [R8's norm-preserving theorem6510](../gaussian_norm_preserving_majorisation/PROOF.md)
  uses a common anchor-radius equality and spherical comparison. The
  current guard imposes no anchor-radius identity and uses a different
  proof. Neither new theorem is imported as a premise.

The proposed contribution is a quantitative positive cover of finite
partially tight faces, including arbitrary block dimensions and independent
endpoint frames. It is a source-backed author result with exact controls,
not a priority determination, independent acceptance, or completion of the
unrestricted campaign target.
