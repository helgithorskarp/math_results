# Sources and mathematical dependencies

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), arXiv:2609.07041v2,
checked live on 26 September 2026. Conjecture 1.1 in dimension three remains
open. We prove one explicit high-variance region, not that conjecture.

## Direct positive dependency

The final Gaussian implication is Theorem 1 of
[the eventual-endpoint proof](../gaussian_majorisation_eventual_endpoint/PROOF.md),
commit `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`.
Its PROOF.md SHA256 is
`9adbd6c07b271a12252b13c35d76835a2d6edc0592f3dd7285a2d950c9ba330f`.
Graph: `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`.
It gives the bound R^2 max(8,44/kappa) from a uniform spherical gap.
Its [independent accepting review](../gaussian_majorisation_eventual_endpoint_review2/README.md),
commit `c750676fd6e164db43c0891c0093ebed2a49c356`, also accepts the underlying
spherical-tail and signed-window analytic inputs.
Review graph: `bafkreih6v5ttck5sx6ivw5xrvn7oqzvmuqylrfyohzvpek3k7bm6ohbbli`.
That review predates and does not review the present certificate.

The bounded-law tail error, signed-window theorem, and Gaussian hinge
completion are credited to those team artifacts, not claimed new here.
The new finite certificate verifies the missing spherical hypothesis for
a particular explicit open weight family.

## The unresolved example and its reviewed method obstructions

The sites and weights are taken unchanged from researcher7's
[asymmetric bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
commit `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`.
PROOF.md SHA256:
`8ef1e2469806ce0f5f9170bea23a577184ea45784a7ad27ca66dda05ea1b33e1`.
Graph: `bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`.
That work proves the covariance obstruction and deterministic-mixture
exclusions on an L1 weight ball of radius 1/4000, which contains our 1/25000
ball. Its exact geometry originates in the team's
[simplicial-cone and nonsimplicial-frontier proof](../gaussian_simplicial_cone_reflections/PROOF.md).
The atomic common-output rigidity uses researcher8's
[common-target theorem](../gaussian_majorisation_common_target/PROOF.md).
These distinctions explain why this positive class is useful. They are not
required to prove our spherical inequality or Gaussian endpoint.

During the prepublication refresh, the new
[independent accepting review](../gaussian_atomic_bridge_obstruction_review1/REVIEW.md)
was incorporated. Commit: `b89f9f31a95637f92f7235a5693d2edbc5e530f6`.
Review graph: `bafkreigezcyjregjqxi5lasmyightqun6lyowyq436jfjetzyg6li44wpe`.
REVIEW.md SHA256:
`023f33c406214d417ccecbf43e663b44b13149f8483917308b406cffe37942bd`.
It independently checks covariance by Sturm sequences and the complete
contraction catalogue by backtracking. It explicitly recommends a spherical
or signed-hinge mechanism for these examples. The present result provides
such a positive mechanism at sufficiently large variance.

## Other Team B advances incorporated

Researcher6's [axial cone rotations](../gaussian_axial_cone_rotations/README.md)
and the simplicial cone theorem already close substantial all-variance
geometric classes. We do not repeat those classes or infer a motion from
our certificate. Our preceding [scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md)
is a geometric handoff and fails on this norm-preserving square-cone map.
Its graph contribution committed at height6066 during this pass.

Researcher8's new
[tail correction and deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md),
commit `a712230931a5c8ee6d0b90f7910b7afe6bffb4ed`, was read at pass start.
Graph: `bafkreidevccw36nby6zvy3vp5ae2j5lzbpji27qctfk4uyiqib7iwhrku4`.
It blocks a uniform vanishing-deficit normalized tail remainder and supplies
a next-coefficient test at spherical zeros. Here the certified leading gap
is uniformly positive, so neither a deficit-error refinement nor a zero-case
assumption is needed. The covariance-free entropy-rigidity proof remains
preserved; no signed conclusion is inferred from it.

## Validated computation and novelty boundary

The [python-flint Arb documentation](https://python-flint.readthedocs.io/en/latest/arb.html)
describes the midpoint-radius representation and precision controls used
by the checker. Our environment pins python-flint0.8.0; the public current
documentation was inspected for arithmetic semantics. No ordinary floating
approximation is a premise of the certificate.

Jensen cubature, Hessian interpolation bounds, and support-function estimates
are standard techniques. The contribution is their explicit complete
certificate on the team's asymmetric open family and the resulting all-hinge
high-variance theorem. Bounded primary-literature, graph, report, and source
refreshes found no existing positive resolution for this exact family.
No historical-priority claim or new general comparison principle is made.
The result is submitted as `proof_attempt` pending independent review.
