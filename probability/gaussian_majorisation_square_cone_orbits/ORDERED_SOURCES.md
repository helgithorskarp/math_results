# Ordered-weight annex: sources and place in the team landscape

The sole problem source remains Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), arXiv:2609.07041v2,
Conjecture 1.1. The paper was refreshed live on 26 September 2026.
The new result in [ORDERED_WEIGHTS.md](ORDERED_WEIGHTS.md) proves full
Gaussian majorisation on ordered-weight square-cone rays, including bounded
radial laws, and a corresponding unequal-radius ball-union theorem.
The unrestricted R3 conjecture remains open.

## Analytic and computational dependencies

The finite correlation-to-hinge identity, chamber polynomial construction,
and orbit averaging come from our original [PROOF.md](PROOF.md), source
commit `241e48a3c393b659ad90fbe5db145a6f58395d6e`.
Proof SHA256: `772468055235aa579e58f0b29b379ac1f3e05548d154b19fa26e9bdfb2b7a575`.
Graph: `bafkreicpvcw53nvwenb2uiq7fk5fhuhl6sqcnwgucw5bgrgcjsj6m65lfu`
(height 6086). The elementary analytic argument is restated in the annex.
The new input is the exact prefix-cone certificate, which supports arbitrary
ordered weight ratios instead of a bounded neighborhood of one base vector.
Neither weight theorem is claimed to contain the other's entire class.

The original `verify.py` is used by the new primary constructor without
modification. The new independent checker imports neither constructor and
reconstructs all 4608 relation entries before its different complete
enumeration and 30,615,202 direct correlation checks. The two exact programs
share Python's integer arithmetic and the unformalized analytic reduction,
not a proof assistant or independent authorship.

Kirszbraun extension is classical; a primary modern proof is Daniel Azagra,
Erwan Le Gruyer, and Carlos Mudarra,
[*Kirszbraun's theorem via an explicit formula*](https://arxiv.org/abs/1810.10288).
Only the usual equal-Lipschitz-constant extension is used. None of the
entropy-rigidity, replica, sparse-Hankel, or tail-error estimates is needed
as a premise of this positive comparison.

## The geometric bridge and its positive obligation

Researcher5's [GEOMETRIC_LIMIT.md](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md),
source commit `c4ab34bd94a7d08646803a5c1d6ad535bcbe877f`, proves the precise
small-variance, exponential-weight transfer and classifies the original
orbit cones' finite logarithmic profiles as
`lambda_0=lambda_2=lambda_3>=lambda_1` in each cluster.
Proof SHA256: `b6b30d1a051868a7d7b7f058be16168239a4372012ba74a55fd387782dd45af3`.
Graph: `bafkreiefrksdmj7mopgxg5jcujfudenjflfrsvi5xo5lylees5vbpn3puu`
(6096). It shows that the extracted radius patterns already have a
coordinate-preserving rematching proof, and identifies the positive
obligation of allowing genuinely different exponential rates.

The new prefix cones permit all four rates to be strictly ordered at every
shell. The annex proves the transfer directly on every finite orbit,
including ball boundaries, and then for every locally finite invariant
measure. Its all-distinct exposed-sphere fixture excludes endpoint
radius-rematching and gives a strict positive volume gap. This is a new
positive class relative to the earlier team certificates, rather than a
claim that an enlarged bounded weight ball automatically yields new radii.

The no-R5-motion statement used **only for comparison with existing
methods** is researcher7's [simplicial-cone theorem, Theorem D](../gaussian_simplicial_cone_reflections/PROOF.md),
source commit `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`.
Proof SHA256: `6495916425b70062986e55beef5e472f4d2deacfe93bd46f92ea365521713842`.
Graph: `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`
(6042). It concerns the prescribed nine-point geometry, independently of
probability weights or ball radii. We do not transfer the separate covariance
obstruction for the old asymmetric weights to these new ordered weights.

The exclusion of all finite aligned strong-contraction chains is a direct
application of researcher6's existing
[COMPOSITIONS.md, Theorem C1](../gaussian_axial_cone_rotations/COMPOSITIONS.md),
source commit `8e8cb2a62e575adbf0ec3ff74e681ee9688f1768`.
Proof SHA256: `23a3a850c3d2e3b69ede387b99e3d8db4a415d6b54db416ff8248429731e7ac7`.
Graph: `bafkreiddw3bmdgooqxosmfgckzm5qxgnwitkah6dkv4whnafobuqpsvxn4`
(6098). Here the exact dual witness is simply `diag(-1,-1,1)` because the
two square cones are dual. The new geometry checker verifies its generator
values. This scope application does not supply the positive inequality and
does not reopen a negative-bridge project.

## Relationship to the current positive classes

| Existing result | Scope relevant here | Relationship to the new annex |
|---|---|---|
| Original fixed-base orbit cones | All variances and thresholds; bounded radial laws; the certified logarithmic radius limits admit rematching | The prefix orders add an unbounded contrast cone with strictly ordered radius profiles |
| [Bounded-law stability](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md) | Exact strict interior; data-dependent W-infinity neighborhoods and complete finite tests on a compact positive variance band | The new certificate proves a concrete all-order class directly, including the singular geometric variance limit |
| [Paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md) | All variances on a constrained geometric neighborhood and a bounded positive weight ball | Complementary spatial freedom; that bounded weight ball gives equal logarithmic radii |
| [Axial motions](../gaussian_axial_cone_rotations/PROOF.md) and [uniform nonlinear robustness](../gaussian_axial_cone_rotations/ROBUSTNESS.md) | All weights and arbitrary individual radii for domains with an R4 contracting motion | The square-cone fixture has no R5 motion, while our weight/radius ordering and exact ray geometry remain restrictions |
| [Global density-value criterion](../gaussian_majorisation_global_criterion/PROOF.md) | Equivalent complete coupling and all-order defect formulations | The orbit certificate supplies zero hinge defect in its new class without solving an optimal-transport problem |
| [Dominant fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md) | At one fixed variance, all laws with any fixed dominant-atom mass already have the strength of the full conjecture if their remaining packet is arbitrary | The new cone allows any origin mass, including a dominant atom, but still restricts the remaining law to ordered ray measures |

Durable provenance for that comparison:

- Bounded-law stability: commit `52ef6716a271b31ac1046207764fc78d3db6165c`,
  graph `bafkreietfhclp4t463gjaeyh4ldpj2eeognjhwdphuywmdxyrepqwskdiu`
  (6102). Proof SHA256:
  `c57cf927ca818c4d84811cbffbeb0b283a0e14bf48ca44d1732e5fb08bc2c49c`.
- Paired-layer completion: commit `465f892ad569fe12fb2634395c21bc7025abff41`,
  graph `bafkreib4j6gpea55bkfajd73g2tcmfr5bvdhulhaeqjcw5v5guw2miflki`
  (6100). Proof SHA256:
  `f6a1ab91b85aec6e43f43baeea1910b6d23b6746244c11be7b4fba5ef04d33f7`.
- Axial motion: commit `984e1edaaf7f02bf4572c80754edff1e296fdd19`, graph
  `bafkreiao6gmik3rvanspc76z6zukxlkk447ylprpkitnt6ht6tmdayl2zy` (6062).
  Its latest uniform robustness extension is commit
  `a63bee4157117a2d2abb2a358119dfd57ebb5a9d`, graph
  `bafkreico6twre4tzlewepj3ej7vay764gyeajof4ni25s4jksd3p4sed2y` (6104).
  ROBUSTNESS.md SHA256 is
  `50937f311cb364ed3cd2fec5d0adf12e3447a9287df6a85a628ebf61f6e5a410`.
- Global criterion: commit `3177065da9c38e8735e8c1b39c41510e43e4bcde`, graph
  `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq` (6088).

The latest Team B reports were refreshed before publication. Researcher6's
robustness extension was read and incorporated into the comparison.
Researcher7's subsequent exact finite-order audit is not an all-order proof
and is not a premise here. Independent review of the present annex is pending.

The final repository refresh also supplied researcher5's
[fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
commit `138993ba3ec2efde720c789a2a3d887c9c417c69`. Its entire proof was read; proof SHA256:
`80abe01d8d27eabdedbdc167e2200b34eb15b5f8feea7a07187fc26c130d4ee4`.
It transfers any hypothetical violation into a law with an arbitrarily
dominant fixed atom by separating a rare arbitrary packet; it does not
assert that those laws obey majorisation. Our new theorem permits arbitrary
origin mass and all bounded radial supports in its ordered class, but that
class does not contain an arbitrary separated packet or contraction.
Therefore no full-conjecture conclusion follows by combining the two results.
The reduction identifies a useful remaining quantifier, rather than a gap
in either proof. It is context, not a premise of the new certificate.

## Primary geometric context and novelty boundary

K. Bezdek and R. Connelly,
[*Pushing disks apart: the Kneser--Poulsen conjecture in the plane*](https://arxiv.org/abs/math/0108098),
give the classical planar and lifted-motion framework used by the team's
geometric classes. Their author manuscript
[*On the weighted Kneser--Poulsen conjecture*](https://pi.math.cornell.edu/~connelly/Slepian-2.pdf)
(5 February 2008), Sections 3--6, relates ball-flower comparisons to radial
weight functions and records the continuous-motion and planar cases.
That weighted-flower formulation is not the same as integration against an
arbitrary ambient G-invariant measure in our orbitwise conclusion.

K. Bezdek and M. Naszodi,
[*The Kneser--Poulsen conjecture for special contractions*](https://arxiv.org/abs/1701.05074),
prove the union/intersection comparisons for strong coordinatewise
contractions, even for unconditional bodies. The scope exclusion above
uses the team's later finite-composition lemma, not a claim that their
theorem is limited to one coordinate frame.

Live primary-source and bounded graph searches found no earlier result for
this ordered-radius square-cone class. This is a bounded novelty audit,
not a historical-priority guarantee or a classification of all possible
geometric proofs. No new general theorem about stochastic orders,
Kirszbraun extension, or the abstract exponential-weight limit is claimed.
The mathematical advance is the positive prefix correlation certificate,
its all-order radial-law consequence, and the corresponding unequal-radius
union class beyond the identified rematching and motion mechanisms.
