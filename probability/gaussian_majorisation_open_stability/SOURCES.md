# Sources, dependencies, and mathematical status

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, Conjecture1.1, checked live on26 September2026.
The full dimension-three conjecture remains open. Homothetic monotonicity
is an established continuous-contraction phenomenon; our posterior-covariance
calculation supplies the strictness needed for the stability bridge.

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
Finite instances of it, the
[damped-cone class](../gaussian_damped_cone_reflections/PROOF.md),
[scalar-defect class](../gaussian_majorisation_scalar_defect/PROOF.md),
[simplicial class](../gaussian_simplicial_cone_reflections/PROOF.md), and
[common-target class](../gaussian_majorisation_common_target/PROOF.md)
feed the same regularization-and-stability principle. The source requirements
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

The contribution is the strict finite density-orbit certificate, its
positive spatial-cloud stability theorem, and the unifying fixed-variance
regularization principle with the stated endpoint controls. Continuity,
layer-cake formulas, Gaussian differentiation and compactness are standard.
Targeted primary-literature searches and bounded graph/source refreshes did
not locate the same spatial result for this obstruction family. That is
not a historical-priority guarantee.

No approximate numerical sign, solver, external dataset, hidden certificate,
or large computation is a proof premise. The existence of the spatial
radius is analytic, and no numerical value for it is advertised. Exact
Python arithmetic validates the new finite lemma; the cited all-hinge
proof and the analytic arguments remain unformalized. Independent review
is pending. No new Kneser--Poulsen case is claimed from a variance-band result.
