# Primary attribution and durable team inputs

Literature and bounded Team B neighbourhood refreshed on 2026-09-26.
This is a synthesis with a quantitative global certificate, not a claim
to invent stochastic order, Hausdorff moments or positive approximation.

## Primary literature

* Gautam Aishwarya and Dongbin Li, [Gaussian Convolution, Internal Energies, and
  the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  The sole problem source. Lemma 3.2 uses stochastic order of sampled
  density values and disintegration; Theorem 1.4 supplies such couplings
  for continuous contractions. Theorem 1.5 explains two-Gaussian-coordinate
  marginalisation; Theorems 1.8 and 5.1 give volume consequences, with
  the latter already treating variable radii by exponential weights.
  Our proof spells out the uniform-variable identity and
  the exact nonzero coupling defect rather than asserting a new coupling
  principle.
* Persi Diaconis and David Freedman, [The Markov Moment Problem and de
  Finetti's Theorem: Part I](https://www.stat.berkeley.edu/users/freedman/631.pdf),
  manuscript dated 15 June 2003. Theorem 1 and Lemma 1 recall the classical
  Hausdorff nonnegative finite-difference criterion. Our beta tests are
  precisely those differences for the existing hinge moments.
* Jian-Guo Liu and Robert L. Pego, [On generating functions of Hausdorff
  moment sequences](https://arxiv.org/html/1401.8052), introduction,
  equations (1)--(2). Another primary source for complete monotonicity
  of finite positive measures on `[0,1]`. We use no later generating
  function characterization or lemma affected by its appended corrigendum.
* Elena E. Berdysheva, Nira Dyn, Elza Farkhi and Alona Mokhov,
  [Metric Approximation of Set-Valued Functions of Bounded Variation by
  Integral Operators](https://link.springer.com/article/10.1007/s00365-024-09681-5),
  Constructive Approximation 61 (2025), 347--377, Section 5.1.
  This primary article records the classical Bernstein--Durrmeyer kernel
  used here. We derive the particular second moment and the Gaussian
  support bound directly. No set-valued approximation result is needed.

## Reused mathematical source

Direct reader links and precise implication boundaries are in
[DEPENDENCIES.md](DEPENDENCIES.md). These commits record the input
versions; links intentionally use readable branch paths.

| Input | Source commit |
|---|---|
| Complete hinge/Hankel reduction | `6f51c67737051a61290c070c9fb960e1da83b75b` |
| Local-lift obstruction | `c363e6b2e9db8cdb18b7a6ad787446f305712e92` |
| Paired-rank and Abel reduction | `f7c122d6a5ade217930d63da27e67f9a9e55a539` |
| Scalar-defect motion | `a8c8a21bde0eb356cf1fc302e3f9b13f1e9b113e` |
| Simplicial cone reflection | `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7` |
| Axial cone rotation | `984e1edaaf7f02bf4572c80754edff1e296fdd19` |
| Axial finite strong-composition obstruction | `8e8cb2a62e575adbf0ec3ff74e681ee9688f1768` |
| Uniform nonlinear axial robustness | `a63bee4157117a2d2abb2a358119dfd57ebb5a9d` |
| Undamped transverse matrix-path principle | `01b707bf3eb19f7bd44b8c45771fffa7b7651b55` |
| Damped cone reflection | `57ff1129224b92a88404817b164bf8c17bd2ecd1` |
| All-variance square-cone density orbits | `241e48a3c393b659ad90fbe5db145a6f58395d6e` |
| Ordered-weight orbit and unequal-radius unions | `6056a43fd6c806cc2d92243e551528e238e40a23` |
| Compact-variance spatial-cloud stability | `b48c5ca31f3c573f2ffe6874944de83bc1a92710` |
| Bounded-law interior and finite positive certificates | `52ef6716a271b31ac1046207764fc78d3db6165c` |
| Paired-layer all-variance completion | `465f892ad569fe12fb2634395c21bc7025abff41` |
| Fixed-core relabelling | `e78d73bcae9a21f1344e74166153abe308bf51e9` |
| Common-target gluing | `3ad6ed0be174d1292b250efcad734d03eed01af5` |
| Common-target independent acceptance | `193f0e8fbf34bba8db0ef54d2aa87efa75de7034` |
| Sparse Hankel hierarchy | `c8df5163dd314544b4f2a611483ab192349a8119` |
| High-noise hinge window | `42fef5f197d9e601db9d1f637b84c4d6215a3039` |
| Spherical tail | `78b38b8cd6caab0e8ef8a7e0efa88b0d1da05f6f` |
| Eventual completion | `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6` |
| Eventual completion independent acceptance | `c750676fd6e164db43c0891c0093ebed2a49c356` |
| Asymmetric eventual certificate | `733f2f1ffeec6a97089fbdaa5bd89aa997da2240` |
| Atomic bridge obstruction | `d05dd54b551a5a14329cfbe31f8b66c13cc0e217` |
| Atomic obstruction independent acceptance | `b89f9f31a95637f92f7235a5693d2edbc5e530f6` |
| Covariance-free entropy rigidity | `a264d277a51683479424060972dafb44123db597` |
| Covariance-free independent acceptance and unsigned hinge bound | `fc25eff113b59c72fa820def81698e914a80d15b` |
| Signed tail-deficit obstruction | `54372e691479d94f8c4a6ee9a7c3a7ab4ffdac3d` |

The written proofs in this packet are self-contained for the global
criterion. Motion claims and the nine-point separation use the credited
team results at their stated status; their inclusion here is not a new
independent review. No priority or general-conjecture resolution is claimed.

## Geometric-endpoint annex

[GEOMETRIC_LIMIT.md](GEOMETRIC_LIMIT.md) specializes the primary Theorem 5.1
to one logarithmic weight path and gives the exact defect scale using our
global criterion. The variable-radius transfer itself is existing work.
The new finite classification concerns the particular coefficient cones
defined in the [square-cone orbit source](../gaussian_majorisation_square_cone_orbits/PROOF.md),
commit `241e48a3c393b659ad90fbe5db145a6f58395d6e`. Its original compact order
certificate is a hash-checked input to the annex audit, not an omitted
dataset. Four exact cone vectors prove attainability; eleven retained
inequalities prove necessity for all finite logarithmic profiles.

The relabelling explanation uses the already available
[paired-rank/coordinate-preserving mechanism](../gaussian_majorisation_rank_abel/PROOF.md)
and the primary planar majorisation theorem. It is included to establish
that the extracted radius family is not a new geometric consequence.
The refreshed [axial-cone scope statement](../gaussian_axial_cone_rotations/SCOPE.md),
commit `79f59b8ab07215fea46a00e8ca57381393d19f67`, also emphasizes the
distinction between new weighted Gaussian comparisons and new volume cases.
This annex does not classify alternative finite orders, arbitrary positive
weight families, or all valid Kneser--Poulsen radius assignments.

The prepublication refresh also incorporates the
[spatial-cloud stability proof](../gaussian_majorisation_open_stability/PROOF.md)
and [paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md)
at the commits recorded above. They supply additional exact-zero classes
in the dependency map, with their stated variance and weight quantifiers.
The annex explains the radius-matching scope of their immediate geometric
endpoints. They are author proofs awaiting review, not new premises of our
fixed-cone classification or independently accepted results here.

## Fixed-atom reduction and refreshed obligations

[ANCHOR_REDUCTION.md](ANCHOR_REDUCTION.md) is an analytic reduction of
the entire open question, using the same global defect. It combines an
explicit contractive anchor extension with the elementary nonnegative
hinge interaction and a Gaussian half-space overlap estimate. The
result is uniform over every threshold. The conditional near-Gaussian
consequences use standard mixture entropy, Gaussian translation, and
coupling identities derived there. These ingredients, and the standard
Kirszbraun extension, carry no priority claim. No counterexample is
assumed or constructed, and no new positive Kneser--Poulsen class is
claimed. The reduction requires no external computational certificate.

The prepublication refresh incorporates three durable advances:

* [Axial finite compositions](../gaussian_axial_cone_rotations/COMPOSITIONS.md):
  all finite aligned strong-coordinate chains are excluded on the stated
  rigid anchored class. This does not constrain post-convolution couplings.
* [Axial nonlinear robustness](../gaussian_axial_cone_rotations/ROBUSTNESS.md):
  a reserved scaling gives one domain-wide bound for nonlinear endpoint
  perturbations, all weights and variances, and arbitrary radii. Its
  geometric input is retained; this source does not cover arbitrary
  remote rare packets solely by their small probabilities.
* [Bounded-law stability](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md):
  strict mean-support and peak gaps and strict hinges describe the exact
  product `W_infinity` interior. Its finite positive moment certificate
  has signed endpoint and localization premises. The fixed-atom
  reduction explicitly records why neither a law-dependent neighborhood
  nor convergence in weaker distances supplies the unrestricted sign.

These author proofs are cited at their stated status, not independently
reviewed here. Their source commits are recorded in the table. The
paired-layer all-variance completion retains its separate spatial and
weight hypotheses. New private searches and finite positive moment
tables from the counterexample lane are not mathematical dependencies.
The fixed-atom reduction leaves the original arbitrary-weight square-cone
origin-adjunction question open; its remote-atom error tending to zero
does not imply positive comparison at finite separation.

The retained covariance-free theorem has an
[independent acceptance](../gaussian_majorisation_bridge_barrier/AUDIT.md)
in graph contribution `bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`
at height 5952. Its quantitative hinge consequence is unsigned. The
separate energy-only obstruction in that packet is not what this audit
accepted, and the audit does not establish the present fixed-atom proof.

## Current inclusion and dependency handoff

[DEPENDENCIES.md](DEPENDENCIES.md) separates equivalent full-question
formulations, sufficient domain-wide geometric classes, the ordered-radius
orbit class, law-dependent closure and narrow examples, stability and
finite certificates, and restrictions on proof mechanisms. Its diagram
gives sufficient implications under labelled hypotheses, without reverse
inclusions or a full classification. This is a source and graph synthesis,
with no new threshold theorem or independent acceptance of cited proofs.

The material new input is researcher 8's
[ordered-weight annex](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md),
at the new commit in the table. Its different finite orders allow
unbounded ordered ratios on the exact square-cone rays. It proves every
hinge for bounded measure-ordered radial laws and ordered-radius unions
for locally finite measures invariant under signed coordinate permutations.
It asserts neither intersections, arbitrary weights nor arbitrary geometry.
Its exposed-ball fixture separates the result from the identified
rematching and motion certificates, without classifying every possible
auxiliary proof or certifying historical priority.

The old logarithmic-profile classification still concerns its specified
fixed-base certificate. The ordered annex meets the earlier positive
extension obligation on these rays with a new certificate. No containment
of either whole weight class in the other is asserted. The old covariance
obstruction is not transferred to new weights. Arbitrary origin mass in
either ray class does not supply the arbitrary remaining packet required
by the fixed-atom reduction.

The ordered source's three exact programs were replayed under CPython
3.11.2, including the separate reconstruction of all 4608 order entries and
all 30,615,202 upper-set pairs. Their expected-report hashes are:

```text
ORDERED_WEIGHT_ORBIT_MATCHINGS_PASS
5ffe59c3dbbf29ff5adc8fa146311857e5ec56f0a249ce1c1cf1b6e400b91738
ORDERED_WEIGHT_ALL_UPPER_SETS_CROSSCHECK_PASS
a5f0522a648bbc98578e42e0d54109ccf31c3e73d1beb4c485db313a31f20b58
ORDERED_RADII_GEOMETRY_FIXTURE_PASS
e0ea0261422b96c48a2d5928b9096a2ceaa48342172dbbc99f2d0c330fd0d7ff
```

Reproduction from `probability/gaussian_majorisation_square_cone_orbits`:

```sh
python3 verify_ordered_weights.py --check
python3 independent_ordered_check.py --check
python3 ordered_geometry.py --check
sha256sum -c SHA256SUMS
```

This is replay of author-provided algorithms, including their two distinct
finite methods, not independent authorship or review of the continuum
transfer. The original global, geometric-limit and fixed-atom programs
and expected outputs here are unchanged by this handoff update.

Current committed connection points are recorded below. Their kind and
review status are not upgraded by this summary.

The final source refresh supplied researcher 6's
[matrix-path extension](../gaussian_axial_cone_rotations/MATRIX_PATHS.md).
Its whole proof was read and its supplementary exact program replayed:
`python3 matrix_path_audit.py --check`, from its source directory, returns
`AXIAL_MATRIX_PATH_AUDITS_PASS` with report SHA256
`148015152cbb1c3a22a75cee680510d272d511a2de841e8f37e4fc7d499aef32`.
Its manifest also passes. The new support-cost principle includes the old
noncircular rotation method and extends the undamped circular range to
`pq<=1/(1+cos(1))`. The exact optimality applies to block-diagonal relative
Gram motions, not to all motions or Gaussian comparisons. These are
author proofs pending review. The handoff preserves this stronger current
geometric input and the distinct ordered-orbit mechanism without claiming
that one contains the other.

| Source contribution | Height | Artifact reference |
|---|---:|---|
| Global coupling/moment criterion | 6088 | `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq` |
| Fixed-cone geometric endpoint | 6096 | `bafkreiefrksdmj7mopgxg5jcujfudenjflfrsvi5xo5lylees5vbpn3puu` |
| Fixed-atom reduction | 6112 | `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai` |
| Original density-orbit theorem | 6086 | `bafkreicpvcw53nvwenb2uiq7fk5fhuhl6sqcnwgucw5bgrgcjsj6m65lfu` |
| Ordered-weight and ordered-radius extension | 6114 | `bafkreihyai4xolryx3kpmntk4velamfjwaywuer6omhwvpttyqvmqexpy4` |
| Axial whole-domain nonlinear robustness | 6104 | `bafkreico6twre4tzlewepj3ej7vay764gyeajof4ni25s4jksd3p4sed2y` |
| Undamped transverse matrix-path extension | 6118 | `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry` |
| Bounded-law interior and finite certificate | 6102 | `bafkreietfhclp4t463gjaeyh4ldpj2eeognjhwdphuywmdxyrepqwskdiu` |
| Paired-layer all-variance neighborhood | 6100 | `bafkreib4j6gpea55bkfajd73g2tcmfr5bvdhulhaeqjcw5v5guw2miflki` |

Lane ownership remains unchanged. Current finite positive search evidence
is not promoted to a theorem. The full dimension-three question remains
open, and all prior source and review boundaries remain in force.


## Eight-lane fixed-atom and global-criterion interface

[INTERFACES.md](INTERFACES.md) composes the existing fixed-atom, endpoint
coupling/moment and common-set formulations with their exact quantifiers.
It supplies an explicit strict-witness error budget by substituting the
anchor estimate, rare-law net estimate and global moment error; it claims
no new theorem, independent review, numerical experiment or sufficient
family. The human-authorized lanes 1--4 retain PDE, finite-atomic,
measure-localization and extremal-map ownership alongside lanes 5--8.

New source dependencies in this handoff:

| Input | Source commit | SHA256 of the linked file |
|---|---|---|
| [Common-set dual and diffuse optimizer](../gaussian_prior_localization/PROOF.md) | `541d4b7de3d73b41444e5350378a8ecc43d914ea` | `1f7d2b83ea42269fd11d64c5cf398bd2d4378d22e0e9cbf1f421f463823d44e7` |
| [Universal finite orthogonal-rule obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md) | `5e686ec7c361a368e562496c23e06dc4706ba281` | `b85af8a5f69a3cc13c584160ce3e0f545876c6c3dcaee6fdbac41ef80a37a5dd` |
| [Functional/stability handoff](../gaussian_majorisation_open_stability/HANDOFF.md) | `d62369c107285b40d0e55afdcac455c9069f4ab5` | `2b582312f8dd220914ccfb82467afe337d83f4d73a76804de78f49f9011c6e23` |

The prepublication source refresh also incorporated these two inputs:

| Input | Source commit | SHA256 of the linked file |
|---|---|---|
| [Heat-profile evolution and initial layer](../gaussian_majorisation_heat_profiles/PROOF.md) | `007ec4fddd5566a57106a7b0464b34fa8d7ad8f2` | `8c98aa80c136f18c36c3c2f1af216434bb2685fea6a54afff80bc64a362ebe02` |
| [Axial/nonlinear review portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md) | `e8fea4c40319da833258d926c4737198b133e670` | `4a3b41baa76b55cad56b3504ccaf8c679dc72dd3aa7698990f660c9f5a6ce4ce` |

The PDE source supplies a regular-rectangle stopped representation, a
coefficient-order obstruction with a positive endpoint comparison, and
the tube-volume scale hidden in the flat atomic initial profile. Its
first-contact proposal and global extension remain open. The geometric
portfolio is a review synthesis; its original axial and nonlinear core
does not depend on acceptance of the later matrix-path optimization.
Neither input changes the arbitrary-packet obligation.

The final source fetch added the map lane's rigid-mesh reduction:

| Input | Source commit | SHA256 of the linked file |
|---|---|---|
| [Extremal maps by rigid support enlargement](../gaussian_majorisation_extremal_maps/PROOF.md) | `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a` | `11c8464f8e4a664f63dbd823a93a1ff2d6594f3e087bbc000f853e921b1d1a08` |

Its classical piecewise-isometric extension and rigidity arguments are
explicit author-proof dependencies, not re-proved or independently accepted
here. The interface retains a prescribed anchor mass by applying its
auxiliary-mass step only to the rare law: the existing total-variation
bound changes the hinge gap by at most `2 epsilon eta`. This is a direct
compatibility calculation, without a new positive class, atom bound or
fixed-domain extremizer claim. The separate uniform-weight variant is not
imposed on that anchored combination.

The common-set source was first committed in `541d4b7` and published after
merging at `2cad43476404881bcd1dbcfa0dc70f96af5faac8`; its proof bytes above
are unchanged. Its contribution
`bafkreiam5rzibygouwnzj7aokt23ld4twuarsvrpr4ffdxvokehvtl7gd4` is committed
at height 6122. The preceding analytic class map is the summary
`bafkreidn73gtnin3ojvmr6hz6hipasfpf6hl7uhhu3szlauiqhwpkvte2q`, height 6120.

The common-set equality retains `(1-epsilon)q(0)` and minimizes only the
rare contribution. Its unique spherical optimizer disproves exact atomic
attainment, not finite detection of a strict negative value. The finite
orthogonal-rule obstruction excludes a single finite rule working for
all weights; even its congruent control has a negative orbit average and
zero integrated gap. Neither source produces a negative contraction
hinge. The functional handoff is an existing-result synthesis and does
not upgrade its cited proofs' review status.

These source dependencies were read in their stated scope. Their
new mathematical proofs remain author work awaiting independent review;
this pass did not replay their programs or claim independent acceptance.
The fixed-atom proof and all mathematical programs/certificates here are
unchanged. The source manifest includes this documentation interface.
Graph references for new handoffs are added only when their
commitment is observed; broadcast receipts are not treated as commitment.

## Uniform localization and the current finite-certificate boundary

The following new sources were read in full at the recorded revisions.
Their author proofs await independent review; this handoff is not acceptance.
The analytic calculations in INTERFACES Section 4 compose these bounds with
the existing global moment and remote-anchor proofs. They establish no
positive comparison family, evaluate no compact maximum, and imply no new
Kneser--Poulsen case.

| Input | Source commit | SHA256 of the linked file |
|---|---|---|
| [Uniform spatial localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md) | `4ed178725774e2fd3bb486f952825f58e52766cc` | `57b179d6cdb98bab9a1fad42f12c441565c09880c3145588c6a39441d9c5180a` |
| [Finite positive-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md) | `9a1047c925763125c72fa862e9200c40717b9c25` | `be277134f471d0e93bf20b8c6b993455dd28720f9c21c847481459ad0b175509` |
| [Geometric benchmark and map interface](../gaussian_axial_cone_rotations/LANE_HANDOFF.md) | `e53a354f22c282b9a040392f610ba9c1d859969d` | `4017d375708b43a1b10ce867b1fd611efe01c3566881aa1e4121e54d12d65a21` |

The localization maximum D_k is within 4/k of the unrestricted defect.
Taking maxima of the existing uniform beta error gives the separate spatial
and moment budget. The displayed N_k=(40k^4)^4 schedule follows from the
written bound K(2k,1)<40k^3; it is not a practical computation or an exact
finite positive certificate. Zero weights and equality configurations are
retained. Localization followed by a new remote anchor uses L=8k and
R=14k+sqrt(8 log(1/epsilon)); its contraction check and overlap error are
written explicitly. This order supplies a different strict witness with
controlled support and exactly the prescribed anchor mass. It neither
preserves that mass under conditioning nor bounds later mesh enlargement.

The functional interface supplies rigorous normalized-moment inputs, an
absolute source-peak test, a local beta modulus and transport reserves.
Its every-instance/exists-certificate equivalence needs signed endpoints
and strict margins; compactness alone does not supply uniform strict degree.
The geometric handoff distinguishes a positive extreme but flexible map
from the rigid-mesh test class and retains the axial theorem's domain.

No exploratory quadrature is a premise or public artifact of this update.
The original proof files, mathematical programs and expected certificates
are unchanged. The manuscript checks the direct compositions; source hashes,
manifest and reader links are validated separately. No new independent
review, Gaussian sign certificate or historical priority claim is made.

The last source refresh added the PDE lane's completed contact reduction:

| Input | Source commit | SHA256 of the linked file |
|---|---|---|
| [Transverse ordered heat contacts](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md) | `1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f` | `949e497add957be5998b6653898308b4df888cf4403111a800392bd053de2c79` |

Its author proof replaces the earlier open first-contact compactification
with an exact reduction to a still-unproved flux sign under global profile
order and contact. Input regularization, a strict contraction and a scalar
target dilation supply initial order, volume-end controls and transversality.
Bulk flux handles critical levels. The auxiliary law is unbounded and the
bounded-law bridges are stated; no uniform contact cutoff is claimed.
The posterior covariance integral is with respect to Lebesgue measure on
the superlevel set, not density-weighted whole-space MMSE. This input changes
the PDE interface, not the premises of our compact moment or anchor bounds.
Independent review remains pending.
