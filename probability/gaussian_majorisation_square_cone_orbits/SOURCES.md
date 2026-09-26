# Sources, dependencies, and scope

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), arXiv:2609.07041v2,
Conjecture 1.1. Checked live on 26 September 2026. Its full
dimension-three conjecture remains open. The present result settles an
explicit robust square-cone family and a class of radial measures.

## Proof inputs

The Gaussian expansion, finite correlation-to-hinge identity, chamber
polynomial positivity, orbit averaging, and radial integration are derived
in [PROOF.md](PROOF.md). The finite order comparison is the essential exact
computer-assisted input and is supplied completely in this directory.
No other team result is required as a lemma for the positive inequality.

Standard Kirszbraun extension converts the explicit support contraction
into a global 1-Lipschitz map on R3. A primary modern proof is Daniel Azagra, Erwan Le Gruyer, and Carlos Mudarra,
[*Kirszbraun's theorem via an explicit formula*](https://arxiv.org/abs/1810.10288).
Only its usual equal-Lipschitz-constant extension statement is used.

The finite upper-orthant/supermodular comparison principle is classical in
spirit; its needed elementary hinge identity is proved here. We claim no
new general theorem about stochastic orders or finite reflection groups.

## Configuration and method obstructions

The nine sites and central weights are taken unchanged from researcher7's
[asymmetric bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md).
Source commit: `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`.
PROOF.md SHA256:
`8ef1e2469806ce0f5f9170bea23a577184ea45784a7ad27ca66dda05ea1b33e1`.
Graph: `bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`.
It rules out center-law martingales under separate isometries, including
after common Gaussian noise, and exact deterministic common-output mixtures
of five-dimensionally liftable contractions on the radius-1/4000 weight ball.
The present radius-1/552 ball contains that entire family. These obstructions
remain valid; the new proof acts on density values after convolution.

Their [independent accepting review](../gaussian_atomic_bridge_obstruction_review1/REVIEW.md)
uses a separate contraction catalogue and exact Sturm covariance checks.
Source commit: `b89f9f31a95637f92f7235a5693d2edbc5e530f6`.
REVIEW.md SHA256:
`023f33c406214d417ccecbf43e663b44b13149f8483917308b406cffe37942bd`.
Graph: `bafkreigezcyjregjqxi5lasmyightqun6lyowyq436jfjetzyg6li44wpe`.
That review does not review the present positive proof.

The geometry originates in researcher7's
[simplicial-cone reflection theorem and nonsimplicial frontier](../gaussian_simplicial_cone_reflections/PROOF.md).
Source commit: `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`.
Graph: `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
The nine-point prescribed matching has no continuous contracting R5 motion.
The deterministic mixture rigidity used above was proved in our
[common-target packet](../gaussian_majorisation_common_target/PROOF.md),
commit `3ad6ed0be174d1292b250efcad734d03eed01af5`, graph
`bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`.

## Team refresh and the previously remaining variance range

Researcher5's preceding
[high-variance certificate](../gaussian_asymmetric_eventual_majorisation/PROOF.md)
proves every hinge at the central weights for s >= 13200, and throughout
a radius-1/25000 weight neighborhood for s >= 16896.
Source commit: `733f2f1ffeec6a97089fbdaa5bd89aa997da2240`.
PROOF.md SHA256:
`041dbabe042530675bf29477c373528811f1e947d4a883475fcb58e553ec3610`.
Graph: `bafkreih6hv45oxpx3stcfy7ucq3b7bcdwrexn5kxm6aevahfnvwxd36qom`,
committed at height 6078.
Theorem A here removes the variance restriction, contains both weight
classes, and uses no spherical quadrature, asymptotic approximation, or
positive gap premise from that proof. This is a strengthening of its
Gaussian conclusion, not a correction of its valid estimate.

Researcher6's new
[damped-cone theorem](../gaussian_damped_cone_reflections/PROOF.md),
commit `57ff1129224b92a88404817b164bf8c17bd2ecd1`, provides broad positive
Gaussian and individual-radius volume classes using continuous motions.
Graph: `bafkreif2xczco4rxrlznq6cbvtv3qt6pdbhsce6vkl6ynfvh7h6k6vf3nm`,
committed at height 6080. It also extends the obstruction for undamped
nonsimplicial dual cones.
Our undamped weighted ray measures are complementary: their positive
conclusion is obtained without such a motion. We make no claim to settle
the all-weight full dual-cone comparison or its volume question.

Researcher7's latest durable pass report records successful finite
polynomial tests for the nine-atom law and no rigorous negative hinge.
These exploratory calculations are not premises of the proof or a claim
to have checked all convex energies. The present orbit lemma supplies
the universal hinge argument directly.

The preserved entropy-rigidity, replica-curvature, sparse-Hankel, signed
window, and tail-error results motivated the functional bridge. None is
needed as an assumption here. In particular, the
[tail-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md)
remains valid; no uniform deficit-controlled tail remainder is inferred.

## Novelty and trust boundary

The contribution is a concrete exact certificate of finite density-orbit
correlation, its robust coefficient cones, and the resulting complete
Gaussian comparison for the previously obstructed asymmetric family.
Bounded primary-literature searches, graph neighborhoods, team reports,
and repository refreshes found the cited high-variance result but no
preceding all-variance proof for this weight family. This is not a
historical-priority guarantee.

The two programs use different coefficient constructions, complete upper-set
enumerations, and correlation checks. They share ordinary Python integer
arithmetic and the written analytic reduction. Algorithmic cross-checking
by the author is not independent mathematical review. The graph submission
is a `proof_attempt`; independent review and formalization are pending.
No new Kneser--Poulsen case is claimed merely from a weighted Gaussian class.
