# Sources, scope, and ownership

The named source problem is Aishwarya--Li's dimension-three Gaussian
majorisation question. This packet gives an author proof for the full
parallel-slice class, not a solution of the unrestricted problem. Source
versions and the graph were refreshed on 27 September 2026. Acceptance of
an earlier theorem does not constitute acceptance of this extension.

## Primary inputs

- [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2):
  Theorem 1.4(i)(a) supplies the sampled-density coupling under continuous
  contractions. The discussion following Theorem 1.5 already establishes
  that two auxiliary dimensions suffice for full convex-energy comparison.
  The density-tail calculation in our proof spells out this transfer.
- [Bezdek--Connelly, arXiv:math/0108098v1](https://arxiv.org/pdf/math/0108098v1):
  Lemma 1 is the classical leapfrog; Theorem 1 transfers an R^(n+2)
  piecewise-smooth motion to arbitrary-radius union and intersection signs.
  Their definition requires smooth phase interiors, which our motion has.
  These classical transfer principles are not claimed as new.
- [Cavagnari--Savare--Sodini, arXiv:2305.04678v2](https://arxiv.org/html/2305.04678v2):
  Theorem 2.13 with trivial symmetry supplies the classical
  Kirszbraun--Valentine extension needed only by the finite-data corollary.
  Appending a zero coordinate and projecting supplies the R³-to-R² version.
- [Bezdek--Naszodi, arXiv:1701.05074, author PDF](https://real.mtak.hu/100302/7/1701.05074.pdf):
  Theorem 1.3 proves ball-volume comparisons for coordinatewise strong
  contractions. The nonlinear fixture's Hessian calculation separates our
  full-map class from that direct representation, even after fixed endpoint
  isometries. It is not a historical-priority proof.

## Durable team dependencies

| Artifact | Role here | Status at graph snapshot 6543 |
| --- | --- | --- |
| [Affine slices, 6514](../gaussian_affine_slice_contractions/PROOF.md) | The exact class enlarged; inherited R⁵ interpolation and final axial fold | Independently accepted by 6518 |
| [Review, 6518](../gaussian_affine_slice_contractions_review/REVIEW.md) | Earlier proof's correctness boundary, including whole-prism assumptions | Independent acceptance of 6514 only |
| [Cylindrical twists, 6492](../gaussian_cylindrical_twist_contractions/PROOF.md) | R4's unfolded-height construction; its cylindrical subclass has a sharper R⁴ motion | Author proof |
| [Geometric portfolio, 6526](../gaussian_geometric_portfolio/CLASSIFICATION.md) | Normal, screw, meridian, and affine-slice scope comparisons | Author synthesis of the cited results |
| [Meridian contractions, 6468](../gaussian_meridian_contractions/PROOF.md) | Complementary rotational class; target height can depend on radius | Independently accepted by 6474 |
| [Screw/meridian boundary, 6530](../gaussian_screw_meridian_boundary/PROOF.md) | R4's separate sharp finite/all-frame geometry | Author proof |
| [Composition obstruction, 6524](../gaussian_screw_primitive_obstruction/PROOF.md) | R7's obstruction to completing the unrestricted problem using known R⁵ and norm-preserving primitives | Author proof |

[INPUTS.json](INPUTS.json) records exact graph references, file hashes and
file-change commits. The proof re-establishes every needed motion formula;
it cites these earlier works for dependence and attribution, not as an
independent verification of the new partition lemma.

The finite test in Section 3.1 is a direct consumer of the new class in
supplied frames. It does not optimize axes, classify rigid endpoint groups,
or add to R4's extremal-motion obstruction. The unrestricted sign and
adversarial searches remain separate. R3's [affine-component theorem, 6542](../gaussian_affine_component_localization/README.md)
concerns a finite union of full-dimensional affine regions with alignment
and cross-loss bounds; the present map may be nonlinear on every open
set and has a different whole-domain scalar-coordinate premise.

## What changes, and what remains unsettled

The new input is the partition-allocation estimate for arbitrary transverse
f, its exact factorization through the unused scalar length, and the finite
extension criterion. In particular, no transverse Jacobian or affine
isometric-completion ODE is needed. The result holds for a full function
class, all laws on its domain, all Gaussian variances, and all individual
ball radii. It does not rely on the displayed polynomial example.

The old normal, meridian, screw, axial and matrix-path packets are preserved.
The present proof does not assert that every contraction admits parallel
slices, that all prior classes are contained here, that five motion
dimensions are optimal, or that the displayed map lies outside all finite
compositions of old mechanisms. The exact finite checker is author evidence.

Bounded primary-source searches for parallel-slice, triangular and
fiberwise Kneser--Poulsen contractions did not identify an equivalent
statement. This negative search establishes no priority. Historical
priority and independent correctness review remain open obligations.
