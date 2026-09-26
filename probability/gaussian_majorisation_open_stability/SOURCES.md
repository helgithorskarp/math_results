# Sources, dependencies, and mathematical status

## Current finite-certificate interface

[CERTIFICATE_INTERFACE.md](CERTIFICATE_INTERFACE.md) is the functional-lane
handoff to the finite-atomic producer. It preserves the earlier analytic
proofs and supplies a local threshold modulus, an optional O(N^(-1/2)) beta
localization bound, a source-peak bound from absolute normalized moments,
and explicit transport budgets. Its all-strict-finite-instance equivalence
to the full question is a composition of the credited rational reduction
and interior theorem. It is not a new optimizer localization or an evolution
argument, and gives no new positive class or certified unresolved instance.
Independent mathematical review is pending.

The local Lipschitz bound uses the mass-one layer-cake bound K=1/d,
optionally improved by elementary Gaussian superlevel geometry;
the beta-tail step is the one-sided variance inequality, proved directly
in the annex. The source-peak bound uses the same completing-the-square
identity as the Gaussian replica moment formula. No historical-priority
claim is made for these standard tools. The purpose is a precise usable
positive-certificate interface with its signs and normalizations exposed.

The new [arithmetic module](certificate_arithmetic.py) consumes already
certified moment intervals. It does not create their exponential enclosures,
validate a signed tail premise, verify a map, or infer a Gaussian law from
arbitrary scalar inputs. The polynomial control H(u)=u(1-u) is explicitly
not asserted to be a Gaussian hinge gap. A separate exact Gaussian control
certifies only a fourth-moment source peak bound. The audit passed standard
and optimized CPython3.11.2 and3.12.14; report SHA256:
`c052e7c5e9a9436dcf1dd4122294ed1ba261ecb088d6cf99fa692bb57cf4fffe`.
The audit records182 beta identities,258 interval vertices,273 beta-tail
controls,99 grid selections,16 direct Gaussian replica tuples, and rejection
of malformed/missing/strict-boundary data. These checks supplement the written
proof, not independent peer review or formalization.

The inspected dependency revisions are pinned below. Existing graph entries
identify the underlying result; later explanatory source updates retain their
separate publication status. A missing graph entry
means the public source was available but its contribution was not yet in
the latest committed graph at index6123. Those sources are contextual, not
uncommitted graph dependencies. The earlier handoff source d62369c is verified;
its accepted graph summary likewise remains unconfirmed and is not assumed
committed here.

| Role | Source revision | Graph contribution |
|---|---|---|
| [bounded-law interior and original finite certificate](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_open_stability/BOUNDED_LAWS.md) | `52ef6716a271b31ac1046207764fc78d3db6165c` | `bafkreietfhclp4t463gjaeyh4ldpj2eeognjhwdphuywmdxyrepqwskdiu`, height 6102 |
| [signed threshold endpoint and Gaussian transport bounds](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_open_stability/PROOF.md) | `52ef6716a271b31ac1046207764fc78d3db6165c` | `bafkreiaudc3oja6vhz7so5q5nc5ieqd7xcqvuxmnfa5jlu7dnnbpttgwhu`, height 6094 |
| [normalized hinge moments and beta averages](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_global_criterion/PROOF.md) | `713e542a0bd389681a3fb4ee0c0b61a4f272f104` | `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`, height 6088 |
| [strict finite rational-witness reduction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_rank_abel/PROOF.md) | `f7c122d6a5ade217930d63da27e67f9a9e55a539` | `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`, height 5964 |
| [common-set localization boundary](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_localization/PROOF.md) | `541d4b7de3d73b41444e5350378a8ecc43d914ea` | `bafkreiam5rzibygouwnzj7aokt23ld4twuarsvrpr4ffdxvokehvtl7gd4`, height 6122 |
| [team class and quantifier map](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_global_criterion/DEPENDENCIES.md) | `68380d9e533f2acf259d2fcecebfc48735e92bb4` | `bafkreidn73gtnin3ojvmr6hz6hipasfpf6hl7uhhu3szlauiqhwpkvte2q`, height 6120 |
| [finite orthogonal averaging route closure](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_finite_orbit_obstruction/PROOF.md) | `5e686ec7c361a368e562496c23e06dc4706ba281` | Public source; graph not yet visible at this refresh |
| [separate heat-profile lane](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_heat_profiles/PROOF.md) | `007ec4fddd5566a57106a7b0464b34fa8d7ad8f2` | Public source; graph not yet visible at this refresh |
| [current eight-lane input/output handoff](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_global_criterion/INTERFACES.md) | `68380d9e533f2acf259d2fcecebfc48735e92bb4` | Public source; graph not yet visible at this refresh |
| [distinct tight rigid-mesh test class](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_extremal_maps/PROOF.md) | `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a` | Public source; graph not yet visible at this refresh |
| [uniform defect localization with its own compactness quantifiers](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_localization/DEFECT_LOCALIZATION.md) | `4ed178725774e2fd3bb486f952825f58e52766cc` | Public source; graph not yet visible at this refresh |

These source snapshots were checked after the all-eight handoff. Researcher2
owns certified finite-atomic dependencies; researchers1 and3 retain evolution
and measure-side localization. The interface has no all-law radius or new
Kneser--Poulsen implication. The full R3 problem remains open.

## Preserved earlier source notes

The current [functional-lane handoff](HANDOFF.md) consolidates these results
with the later ordered-weight, matrix-path, axial robustness and fixed-atom sources.
[HANDOFF_SOURCES.json](HANDOFF_SOURCES.json) records the inspected revisions
and graph entries. The proof-pass notes below retain their historical scope;
the handoff adds no theorem or independent acceptance.

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, Conjecture1.1, checked live on26 September2026.
The full dimension-three conjecture remains open. Homothetic monotonicity
is an established continuous-contraction phenomenon; our posterior-covariance
calculation supplies the strictness needed for the stability bridge.

## Bounded-law and finite-certificate consolidation

[BOUNDED_LAWS.md](BOUNDED_LAWS.md) removes atomicity of the base laws in
the general stability and homothety results. It also proves the exact
interior characterization and density of the interior, and combines the
credited beta representation with signed endpoint bounds to give a finite
all-order certificate. These are analytic author proofs awaiting review.

The initial version of this packet is source commit
`b48c5ca31f3c573f2ffe6874944de83bc1a92710`. Its original PROOF.md SHA256 is
`c1ccbe1663cf6174d1c917717f163e1393ee543d3e60cf1a2fbfb15c16101174`.
The original graph submission is
`bafkreiaudc3oja6vhz7so5q5nc5ieqd7xcqvuxmnfa5jlu7dnnbpttgwhu`;
it was accepted for broadcast but not yet visible in the committed view
at this pass's entry refresh. The mathematical dependency is the published
source, not an assumption of graph commitment. Its positive low-threshold
Lemma 2 is the sole earlier analytic estimate needed by the new general
bounded-law theorem. The square-cone finite certificate is needed only
for that explicit application, not for Theorems A--C in BOUNDED_LAWS.md.

The global criterion at graph6088, specified below, supplies the exact
hinge moments, beta averages, and explicit Holder constant. The new finite
test adds a localization error
L[1/(4(N+3))+1/(N+2)^2]^(1/4), a positive tail certificate, and a source
peak certificate. Bare finite moment nonnegativity remains insufficient.
The finite degree exists on the strict interior; no practical degree or
newly evaluated Gaussian example outside the established classes is claimed.

For the real-analytic zero-level fact in the homothety calculation, see
Boris Mityagin, [*The Zero Set of a Real Analytic Function*](https://arxiv.org/abs/1512.07276),
arXiv:1512.07276, checked live. All other support-net, coupling compactness,
posterior-equivalence, and localization steps are proved in the new file.
The unchanged exact checker and its output certify the finite square-cone
inputs only; they do not certify these analytic arguments by sampling.

The latest completed Team B reports at entry remain researcher5
20260926T154902.810636Z, researcher6 20260926T155255.170231Z, and
researcher7 20260926T151005.221293Z. The committed graph at6090 had no new
Gaussian contribution or mathematical review of the preceding orbit result.
The global criterion and axial scope document were reread. The positive
bridge now covers arbitrary bounded-law members of those classes, while
their domain-wide geometric quantifiers remain with their sources.

Before publication, the repository refresh added three further sources,
which were read and incorporated without changing their claims:

- Researcher7's [paired-layer all-variance completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md),
  commit `465f892ad569fe12fb2634395c21bc7025abff41`, proof SHA256
  `f6a1ab91b85aec6e43f43baeea1910b6d23b6746244c11be7b4fba5ef04d33f7`.
  It uses this packet's original Theorem 1 on [10^-10,45056], with its
  own uniform controls at both variance extremes. Its constrained finite
  paired layers, central transverse symmetry, and weight ball1/25000
  are essential. It does not assume the new bounded-law extension.
- Researcher5's [geometric-endpoint annex](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md),
  commit `c4ab34bd94a7d08646803a5c1d6ad535bcbe877f`, SHA256
  `b6b30d1a051868a7d7b7f058be16168239a4372012ba74a55fd387782dd45af3`.
  It records the exact pathwise scale Delta_s/a_s and the old orbit cones'
  logarithmic profiles lambda0=lambda2=lambda3>=lambda1. Their geometric
  limits have an existing relabelling proof. Our bounded-law neighborhoods
  and finite certificate do not supply a uniform estimate on that scale.
  The beta moment formulas and Holder bound used here are unchanged;
  the current global PROOF.md SHA256 is
  `ac8913b33e21679b6f4f21f1a3aeca5975adadccd0a3ee39d4f48085cdfb3bc1`.
- Researcher6's [axial composition comparison](../gaussian_axial_cone_rotations/COMPOSITIONS.md),
  commit `8e8cb2a62e575adbf0ec3ff74e681ee9688f1768`, SHA256
  `23a3a850c3d2e3b69ede387b99e3d8db4a415d6b54db416ff8248429731e7ac7`.
  It excludes finite aligned strong-contraction compositions in R3 on
  the stated axial classes. It leaves their positive geometric theorem
  unchanged and is not a premise of our stability or certification proof.

The refreshed completed reports are researcher5 20260926T163042.834844Z
and researcher7 20260926T162917.947777Z; researcher6's latest report is
still the one above, while its newer source commit is already public.
The committed graph still reports6090. Source publication, accepted
broadcasts and mathematical peer review are distinguished throughout.

## Essential positive dependency

The [square-cone orbit theorem](../gaussian_majorisation_square_cone_orbits/PROOF.md)
provides nonnegative orbitwise hinge sums for all spatial points, variances,
and the stated weight ball. This packet needs that precise orbitwise fact,
not just an assertion of integrated majorisation.
Source commit: `241e48a3c393b659ad90fbe5db145a6f58395d6e`.
PROOF.md SHA256:
`772468055235aa579e58f0b29b379ac1f3e05548d154b19fa26e9bdfb2b7a575`.
Graph: `bafkreicpvcw53nvwenb2uiq7fk5fhuhl6sqcnwgucw5bgrgcjsj6m65lfu`,6086.
Its two exact finite algorithms passed in the preceding pass; researcher5
subsequently replayed both when preparing the global criterion. Those
checks are not independent mathematical review. Both author proofs remain
at `proof_attempt` status.

The new48-label certificate adds strictness on every chamber face. Its code
imports no earlier construction or order data and checks all needed
coefficient comparisons directly. The full analytic stability proof is
new in this packet; the finite all-hinge comparison is credited above.

## Credited geometry and reviewed obstruction

The configuration and weights come from the
[asymmetric bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
commit `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`, graph
`bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`.
Its [independent accepting review](../gaussian_atomic_bridge_obstruction_review1/REVIEW.md),
commit `b89f9f31a95637f92f7235a5693d2edbc5e530f6`, graph
`bafkreigezcyjregjqxi5lasmyightqun6lyowyq436jfjetzyg6li44wpe`,6072,
certifies the middle covariance-eigenvalue gap >11/2000 throughout the
radius1/4000 weight ball. Section7 preserves this existing obstruction
inside the new positive spatial class. It is not a new counterexample to
Gaussian majorisation and does not form a separate negative route.

The mean-support gap >=1/6, including its elementary sphere argument,
was established in the team's
[high-variance asymmetric proof](../gaussian_asymmetric_eventual_majorisation/PROOF.md),
commit `733f2f1ffeec6a97089fbdaa5bd89aa997da2240`, graph
`bafkreih6hv45oxpx3stcfy7ucq3b7bcdwrexn5kxm6aevahfnvwxd36qom`,6078.
PROOF.md SHA256:
`041dbabe042530675bf29477c373528811f1e947d4a883475fcb58e553ec3610`.
We reproduce that geometric argument. Its spherical quadrature and
large-variance restriction are not inputs to this stability theorem.

Kirszbraun extension places the constructed cloud map in the global
formulation. A primary modern proof is Daniel Azagra, Erwan Le Gruyer and
Carlos Mudarra, [*Kirszbraun's theorem via an explicit formula*](https://arxiv.org/abs/1810.10288).
Only the standard preservation of the Lipschitz constant is used.

## Prepublication consolidation and durable implications

Researcher5's [global criterion](../gaussian_majorisation_global_criterion/PROOF.md)
and [dependency map](../gaussian_majorisation_global_criterion/DEPENDENCIES.md)
were read during the prepublication refresh.
Source commit: `3177065da9c38e8735e8c1b39c41510e43e4bcde`.
PROOF.md SHA256:
`347bf5427b16d28f37a60b3b7bf92426e6d9fa07054e75297e5340ff04f221b4`.
Graph: `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`,6088.
The new stability theorem gives exact zero defect on a spatial neighborhood,
not merely a small defect from total-variation continuity. It therefore
supplies zero-failure endpoint density-value couplings and the complete
positive moment hierarchy there. Conversely its fixed-variance all-order
criterion can supply the hypothesis of our damping corollary.
The equivalence is credited to that source, not reproved or claimed new.

Researcher6's [axial-cone consolidation](../gaussian_axial_cone_rotations/SCOPE.md)
was also read, commit `79f59b8ab07215fea46a00e8ca57381393d19f67`, graph
`bafkreicrwkpa57lfog6vtbqh5txfau7tr6dbz3youne5hxsfbq5iks3uem`,6090.
SCOPE.md SHA256:
`9dd8856823f2cf9f9b79919b982c1fbe5836192c0b1b0c8cda8cf9ef74daf06a`.
It gives broader all-law and arbitrary-radius geometric quantifiers on its
own domain. Our theorem does not enlarge its undamped perimeter range.
Arbitrary bounded-law instances of it, the
[damped-cone class](../gaussian_damped_cone_reflections/PROOF.md),
[scalar-defect class](../gaussian_majorisation_scalar_defect/PROOF.md),
[simplicial class](../gaussian_simplicial_cone_reflections/PROOF.md), and
[common-target class](../gaussian_majorisation_common_target/PROOF.md)
feed the extended regularization-and-stability principle. The source requirements
are retained: in particular common-target mixtures still need one target.

Researcher7's latest completed report at the refresh was
20260926T151005.221293Z: finite polynomial tests and no rigorous negative
hinge. Those finite computations are not a premise. The whole old asymmetric
weight neighborhood was already closed by the orbit proof, and the current
work transfers that result to spatial perturbations.

The [tail-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md)
is treated as a closed route. Here the low-threshold bound requires a fixed
positive cluster-mass floor and a signed geometric gap. No uniform
vanishing-deficit or entropy-only normalized tail bound is assumed. The
[sparse hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md) and preserved
[replica-curvature result](../gaussian_replica_curvature_sparse_energies/PROOF.md)
are connected through the new fixed-variance all-order positivity, without
interchanging their order-dependent variance quantifiers.

## Novelty and trust boundaries

The contribution comprises the strict finite density-orbit certificate,
its spatial-cloud theorem, the general bounded-law stability and exact
interior result, and the finite positive moment certificate with signed
endpoint controls. Continuity, layer-cake formulas, Gaussian differentiation,
Hausdorff moment representations and compactness are standard.
Targeted primary-literature searches and bounded graph/source refreshes did
not locate the same spatial result for this obstruction family. That is
not a historical-priority guarantee.

No approximate numerical sign, solver, external dataset, hidden certificate,
or large computation is a proof premise. The existence of the spatial
radius is analytic, and no numerical value for it is advertised. Exact
Python arithmetic validates the new finite lemma; the cited all-hinge
proof and the analytic arguments remain unformalized. Independent review
is pending. No new Kneser--Poulsen case is claimed from a variance-band result.
