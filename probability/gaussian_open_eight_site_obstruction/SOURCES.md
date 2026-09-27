# Sources, dependencies, and scope

This is an author proof of an explicit metric-interval obstruction and a
strict perturbation box. Independent correctness review is pending. No
historical priority, smallest number of sites, new Gaussian sign theorem,
or new Kneser--Poulsen volume theorem is asserted.

## Primary literature

1. Gautam Aishwarya and Dongbin Li,
   [*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
   Conjecture*, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   Conjecture 1.1 is the human-named research target. Theorem 1.4 and the
   discussion following Theorem 1.5 explain why a contracting motion in
   `R^(n+2)` suffices for full Gaussian majorisation in `R^n`.
   The source was checked on 27 September 2026; v2, revised 13 September,
   was the current revision. Our obstruction concerns that sufficient
   geometric route, not the truth of Conjecture 1.1.

2. Holun Cheng, Ser Peow Tan and Yidan Zheng,
   [*On continuous expansions of configurations of points in Euclidean
   space*, arXiv:1107.0140](https://arxiv.org/html/1107.0140).
   Theorem 1.3 gives the classical `2n`-dimensional leapfrog. Theorem 2.1
   proves the dimension obstruction for the `(n+1)^2`-point simplex-flap
   construction, crediting independent work of Belk--Connelly. Reversing
   expansions gives contractions. The existence of a general obstruction
   below dimension `2n` is therefore prior work, not a result of this packet.
   Our proof does not invoke their non-liftability theorem: it proves an
   explicit interval separator for a different eight-site geometry, and
   includes a box where none of the endpoint pair distances is preserved.

3. Károly Bezdek and Robert Connelly,
   [*Pushing disks apart--the Kneser--Poulsen conjecture in the plane*,
   arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
   Theorem 1 is the classical ball-volume transfer from suitable monotone
   motions in two extra dimensions. Its conclusion is not contradicted:
   the exhibited pairs fail its motion hypothesis.

Only elementary Euclidean linear algebra, Cauchy--Schwarz, and the
intermediate value theorem are needed for Theorem 1 and Corollary 2. The
classical Euclidean Lipschitz extension theorem is used solely to regard
each finite contraction as a full-space map for the Gaussian problem; see
also the contraction/extension discussion in Aishwarya--Li. The complete
metric-interval obstruction is independent of that external theorem.

## Durable team context

- [Simplicial-cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md),
  original graph6042
  `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`,
  already has a nine-site obstruction using an exactly rigid moving cloud,
  and the binary-weight device for deterministic matching. We reuse the
  latter device with explicit attribution. The interval proof here permits
  both clouds to deform and all endpoint pair losses to be strictly
  positive. It is not a review, correction, or minimality improvement claim
  about that result.
- [Convex normal-ray contractions](../gaussian_radial_contractions/CONVEX_CORES.md),
  original graph6331
  `bafkreifktf3exjltqmj5gnt5wvhpqe2za3cbb7rkdnlt3ha774is52k2j4`,
  has independent correctness acceptance6343, with priority uncertain.
  Its nonnegative normal-distance profile and its bounded reflection
  collar are unchanged. Unrestricted reflected projections onto arbitrary
  convex sets were explicitly outside that theorem. The present deep
  reflections are an obstruction to the low-dimensional motion route,
  not a counterexample to the accepted class.
- [Indecomposable contraction reduction](../gaussian_indecomposable_contractions/PROOF.md)
  and [effective frontier](../gaussian_indecomposable_contractions/LINEAR_HEIGHT.md)
  remain researcher4's deformation/extremal-map results. The new packet
  supplies a concrete finite metric certificate; it proves no
  indecomposability, new extremal reduction, or classification. Its direct
  usefulness to an effective search is that the labelled pair and every
  point in the certified strict box cannot be disposed of by constructing
  a five-dimensional contraction path.
- [Exposed-edge tail bounds](../gaussian_exposed_edge_tail/PROOF.md),
  graph6351, give effective endpoint signs for rational contractions,
  including ones with tight distances. These can be evaluated on any
  chosen rational member here but do not supply its middle-threshold sign.
- [The low-noise degree barrier](../gaussian_low_noise_degree_barrier/PROOF.md),
  graph6360, controls fixed-degree curvature-square tests under positive
  target separation and nearest-pair loss. The strict box does not evade
  those hypotheses; its new information is geometric path exclusion,
  not a proposal that low-noise fixed-degree tests should turn negative.
- [The deep-flap Gaussian cell](../gaussian_deep_flap_cell/PROOF.md), graph6341,
  concerns a different sixteen-site configuration and a fixed-variance
  all-threshold Gaussian certificate. That positive sign is not imported
  into the present geometry. The accepted orthocentric depth-one family is
  also not reopened.

The unrestricted Gaussian sign and counterexample lanes need compensation
or another mechanism on configurations outside the short-lift classes.
This certificate furnishes an open finite input family, including a
deterministically unique weighted matching. It is not evidence that its
Gaussian sign is negative. Arbitrary stochastic couplings and nongeometric
proof methods remain possible. No teammate or reviewer is assigned work
by this artifact.

## Reproducibility and trust boundary

Run the commands in [README.md](README.md). [verify.py](verify.py) imports
no teammate code and uses no solver or external data. [EXPECTED.json](EXPECTED.json)
is compact exact output. [SHA256SUMS](SHA256SUMS) pins the public packet.
The all-configuration estimates and the exclusion of every continuous
path are proved in [PROOF.md](PROOF.md); the checker verifies their finite
identities, rational constants, endpoint data and deliberate rejection
controls. It does not certify a Gaussian integral or formalise the proof.
