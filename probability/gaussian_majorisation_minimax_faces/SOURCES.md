# Sources and dependency boundaries

The target is human-named. No graph score or separate example-class objective
was used to select it. All team artifacts below are author claims unless
their own source supplies a durable independent acceptance record.

## Primary literature

1. Gautam Aishwarya and Dongbin Li, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
   The target is full Gaussian-convolution majorisation under a contraction
   in dimension three. Their continuous-contraction framework establishes
   important sufficient cases; this package does not extend its dimensional
   theorem or establish a new Kneser--Poulsen class.
2. L. R. Ford, Jr. and D. R. Fulkerson, *Maximal Flow Through a Network*,
   Canadian Journal of Mathematics 8 (1956), 399--404
   ([primary article PDF](https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf)).
   The weighted bipartite vertex-cover/edge-flow equality in Section 3 is an
   application of classical max-flow/min-cut. The two-point polarization in
   Section 1 is also classical; its elementary proof is included in full.

## Durable campaign inputs

| Input | What is used here | Provenance |
| --- | --- | --- |
| [Common-set minimax formulation](../gaussian_prior_localization/PROOF.md) | Identifies the all-prior inner minimax problem and the meaning of contact potentials; this package supplies exact zero-value test families | Graph height 6122; commit `541d4b7de3d73b41444e5350378a8ecc43d914ea` |
| [Fixed-origin reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md) | Motivates preserving arbitrary fixed origin mass; not needed for the elementary transfer proof | Graph height 6112; commit `138993ba3ec2efde720c789a2a3d887c9c417c69` |
| [Ordered-weight square-cone theorem](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md) | Supplies the canonical directions and a known positive region; no ordered-weight hypothesis is imposed in the all-prior common-set conclusion | Graph height 6114; commit `6056a43fd6c806cc2d92243e551528e238e40a23` |
| [Finite signed certificates and bounded-law stability](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md) | Explains why floating cubature and a positive second energy cannot decide full majorisation | Graph height 6102; commit `52ef6716a271b31ac1046207764fc78d3db6165c` |
| [Prior finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md) | Explains the switch from enlarging a universal orbit rule to integrated common-set searches; not a logical premise | Commit `5e686ec7c361a368e562496c23e06dc4706ba281`; confirmed at graph height 6126 before this publication |
| [Uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md) | Bounds the unrestricted defect within 4/k by a compact maximum over at most k^6 atoms in radius 2k; equality configurations still belong to that compact frontier | Graph height 6134; commit `4ed178725774e2fd3bb486f952825f58e52766cc` |
| [Finite positive-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md) | Requires signed endpoints, absolute moments, and strict beta margins; the present second-energy lower bound supplies only one scalar signal | Graph height 6136; commit `9a1047c925763125c72fa862e9200c40717b9c25` |
| [Transverse heat-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md) | Requires a flux comparison at globally ordered contacts, including critical levels; neither our special test-set theorem nor the second-energy bound supplies that sign | Commit `1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f` |

The common-set formulation and classical polarization are credited rather
than presented as newly discovered general machinery. The contribution here
is the explicit dual-cone test-set theorem and complete exact boundary
certificate for the unrestricted-weight square-cone minimax search, together
with its sharp quantitative reserve. It leaves the decisive arbitrary-set
obligation unresolved.

The axial-cone matrix-path and heat-profile work were checked before this
handoff. Neither is a premise of these certificates. No prior line-free-set
audit was run or used. Exploratory cubature is not a proof input and its raw
logs are deliberately absent from this compact, self-contained package.
