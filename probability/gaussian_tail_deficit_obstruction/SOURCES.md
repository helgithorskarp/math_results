# Sources, dependencies, and scope

## Primary literature

The sole problem source remains Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), arXiv:2609.07041v2,
13 September 2026, checked live on 26 September 2026. The target is
Conjecture 1.1 in dimension three. Theorem 1.4 confirms that the explicit
homotheties in this packet have full majorisation at every variance;
their negative approximation errors do not contradict the conjecture.

The finite-support completion in Section 5 also uses the strict point-hull
mean-width comparison of Igors Gorbovickis,
[*Strict Kneser-Poulsen conjecture for large radii*](https://arxiv.org/html/1006.0531v2),
Theorem 1.5, checked live on the same date. This is exactly the geometric
input already used by the team's eventual-endpoint result. It implies
that the leading spherical difference tends to positive infinity for
every noncongruent finite contraction with positive atom weights.
No assertion about arbitrary unequal-radius ball hulls is imported.

## Direct analytic dependencies

1. Researcher 5's
   [spherical-tail reduction](../gaussian_majorisation_spherical_tail/PROOF.md)
   supplies the definition and uniform leading estimate refined here.
   It does not assume that its error vanishes with a contraction deficit.
   Our fixed-variance obstruction leaves that theorem intact.
   Source commit: `78b38b8cd6caab0e8ef8a7e0efa88b0d1da05f6f`.
   PROOF.md SHA256:
   `78ed0501580e9c192b468b41a2d1afda7bd327a0610c5a2fe04f44bd07a0d76b`.
   Graph: `bafkreiakfdyplrgs5zveoa2ocaggbrq4ptyrkfdq5efhatguxxntp7u7pi`,
   height 6002.
2. Researcher 5's
   [eventual full endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md)
   handles a uniformly positive leading spherical gap. Our Section 5 adds
   a sufficient next-coefficient test at its unresolved positive zeros.
   Source commit: `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`.
   PROOF.md SHA256:
   `9adbd6c07b271a12252b13c35d76835a2d6edc0592f3dd7285a2d950c9ba330f`.
   Graph: `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`,
   height 6032.
3. Our [high-noise hinge window](../gaussian_majorisation_high_noise_window/PROOF.md)
   covers the remaining thresholds in that completion. Its variance and
   threshold assumptions are retained exactly. No unrestricted positivity
   of the instantaneous lifted comparison is assumed.
   Source commit: `42fef5f197d9e601db9d1f637b84c4d6215a3039`.
   PROOF.md SHA256:
   `e96063604af579e6ebb8cb25e6eb82ca65c07f6716ecc85f67ae6cc137d0bdf9`.
   Graph: `bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`,
   height 6008.

Theorem A's limit and Theorem B's coefficient are proved here directly.
The earlier estimates are used to formulate the rejected bridge and to
complete the conditional all-threshold conclusion, not to justify an
uncontrolled exchange of variance and moving-threshold limits.

## Context and distinctions

The [covariance-free entropy audit](../gaussian_majorisation_bridge_barrier/README.md),
commit `fc25eff113b59c72fa820def81698e914a80d15b`, remains preserved.
Its earlier all-Renyi obstruction compares Gaussian convolutions that are
not a contraction pair. Here the examples are actual injective contractions,
but the failed conclusion is a uniform normalized approximation bound,
not majorisation. The two assertions must not be conflated.
Audit graph: `bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`.
Earlier energy-only obstruction:
`bafkreiahtwafewpeuhfbid57md6jtcbwrxn222ryy53ypafsmr4maoed3e`.

Researcher 6's [small-mass expansion](../gaussian_majorisation_small_mass/PROOF.md),
commit `5f0f1852d71dc61b7edfa1871cbc6a06673a4c27`, studies fixed variance
and a rare cluster, with a threshold restriction in its general theorem.
Our moving threshold is in the much smaller tail where a vanishing
weight can retain a normalized effect. We do not disprove that theorem
or claim to close its general far-tail sign question.
Graph: `bafkreihtnp3ptickdr4nhikxkarcr3v4uwocvhde5lcj3mx2fhmk7b7jge`,
height 5984. Its later geometric small-mass classes also remain valid.

Our [replica-curvature checkpoint](../gaussian_replica_curvature_sparse_energies/PROOF.md)
at commit `5586f0d772d6b7861bd73207901e183690f4d22b` and
[sparse-Hankel hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md)
at commit `c8df5163dd314544b4f2a611483ab192349a8119` remain unchanged.
They supply finite-order energy control for arbitrary bounded contractions;
neither is treated as an all-threshold theorem. The present result explains
why an unsigned vanishing-deficit tail remainder cannot complete that bridge.

During the prepublication refresh, new team artifacts were inspected:

- [Asymmetric nine-atom bridge obstruction](../gaussian_atomic_bridge_obstruction/README.md),
  commit `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`: extends our
  deterministic common-target obstruction quantitatively and rules out
  the martingale sufficient route for an open set of weights. This is a
  separate obstruction and is not a premise of the present tail proof.
- [Axial cone rotations](../gaussian_axial_cone_rotations/README.md),
  commit `984e1edaaf7f02bf4572c80754edff1e296fdd19`: proves new geometric
  classes through an explicit motion. No such motion is asserted here
  for the unrestricted target.
- [Scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md),
  commit `a8c8a21bde0eb356cf1fc302e3f9b13f1e9b113e`: absorbs one coordinate
  discrepancy in a pointwise distance deficit and constructs a monotone
  motion. This is compatible with our obstruction: its **pairwise**
  hypothesis is different from a modulus of the **mean** deficit controlling
  normalized tail error uniformly in thresholds.
- [Independent accepting review of our previous common-target result](../gaussian_majorisation_common_target_review2/README.md),
  commit `193f0e8fbf34bba8db0ef54d2aa87efa75de7034`. This review does not
  apply to the present new packet.

## Trust and novelty boundary

The primary papers, bounded teammate reports, intervening Team B commits,
and relevant committed graph neighborhood were refreshed before publication.
Searches for Gaussian spherical comparisons and related stability bridges
did not locate this particular moving-weight constant or signed coefficient.
This is a bounded literature audit, not a historical-priority guarantee.

The elementary radial and exponential expansions are not claimed new as
techniques. The contribution is the explicit fixed-variance obstruction
inside the actual contraction class, the next signed invariant, and its
precise conditional implication at a spherical zero. No negative hinge,
new Kneser--Poulsen conclusion, or general spherical sign theorem is claimed.
All finite checks supplement the analytic proof. The graph status is
`proof_attempt`; independent review and formalization remain pending.
