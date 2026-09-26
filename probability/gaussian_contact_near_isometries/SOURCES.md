# Attribution, dependencies and the contact-sign handoff

The sole problem source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2). Their unrestricted
dimension-three majorisation conjecture remains open here. Their known
continuous-contraction theorem supplies the full positive comparison in the
homothety sanity check; that comparison is not a contribution of this packet.

The Gaussian continuity-equation and posterior-divergence method is prior
work, used explicitly by Aishwarya--Li in
[The Kneser--Poulsen phenomena for entropy, arXiv:2409.03664v3](https://arxiv.org/html/2409.03664v3),
Section 3. We credit that mechanism, orthogonal Procrustes alignment,
double-centering of distance matrices, the top-set envelope principle and
Gaussian derivative estimates. No priority claim is made for these tools.
Both manuscripts were inspected live on 26 September 2026. Targeted primary
literature searches for local Gaussian majorisation, isometry and contraction
perturbations did not locate the explicit estimate proved here; this bounded
search is not an assertion of historical priority.

The proposed new input is the combination of the displacement-sensitive
Gram estimate `M <= 4 R delta D/kappa`, the positive first variation on the
**actual source top set**, and a volume-sensitive Taylor remainder. It
produces a signed endpoint profile margin and consequently an explicit
contact exclusion neighborhood. This is more specific than the classical
fact that the first derivative at an isometry points in the favorable
direction. The finite displacement and its remainder are controlled.

## Mathematical dependencies

1. [Gaussian contraction rigidity, Section 6](../gaussian_contraction_rigidity/PROOF.md)
   supplies the Procrustes/centered-Gram calculation. We repeat that proof
   and replace its bound `Delta<=4R^2` by `Delta<=8R delta`. We do not use
   entropy monotonicity or infer hinge comparison from an entropy gap.
   Source-file commit: `33bb5788b6ecf84a706fbd3eea99cf336f23e25b`.
   SHA256: `d1b2daa37c88f9c2759b234b69a9c351f0adfb51f7df109e2864331413a582c8`.
   Original graph contribution:
   `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`.
   Associated review:
   `bafkreibmhq6cg4rwvr2g5dbegsx47pglj4njuv6gjv3rp6tekly2lxe6ru`.

2. [The first-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
   states the remaining ordered flux condition, includes critical levels,
   and specifies its unbounded auxiliary input. The present local theorem
   is proved without that reduction; its role is to identify the exact
   consumer and prevent a false bounded-to-unbounded application.
   Source commit: `1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f`.
   SHA256: `949e497add957be5998b6653898308b4df888cf4403111a800392bd053de2c79`.
   Graph contribution at height 6140:
   `bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`.
   Its [separate-lane analytic audit](../gaussian_majorisation_contact_audit/REVIEW.md)
   accepts that reduction and discloses authorship of its homothety precursor.
   That audit does not review the new theorem in this packet.

The new proof recalls all algebra and analysis it needs. These source hashes
pin inspected dependencies, not an external computation that must be trusted.
The exact audit imports no teammate code.

## Concise handoff to the R5 and R8 mechanisms

R5's [isometric-reference theorem](../gaussian_isometric_reference/PROOF.md)
at source commit `3a70618cd4611e258dcd275bdf45a139fd44e459` is a qualitative
common-set theorem for an actual prior tested against a reference law on
which the contraction is exactly isometric. It also classifies zero slack.
Its proof hash is
`11539d70d095550b2c7c052ed497121f26a2adbf54280f7cd4b3819001e2be44`.
Our theorem has no auxiliary isometric reference law: its optimizing set is
that of the actual full prior. The corresponding cost is a full covariance
floor and small displacement after alignment of that prior. It therefore
provides a signed neighborhood of a full-rank isometric pair; it does not
cover an arbitrary rare packet attached to a fixed atom. R5's
[fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
at height 6112 retains its unrestricted packets and all-threshold quantifiers.

R8's [quantitative common-set estimate](../gaussian_common_set_stability/PROOF.md)
at source commit `07dc648282cc625294828c885b9c0365cdf15851` bounds a reference
margin below by pair-distance loss and then subtracts a separate source-set
error. Its proof hash is
`ebf835b9f73b3ab072bf3b9ed95e77da6fc3f8cd27b0d6251e38a972a4a07fd4`.
The present endpoint bound needs no reference-shell error or rate at a
critical level: its Taylor calculation already uses the actual source set.
Unlike that finite-configuration theorem, however, it needs positive
covariance and small aligned displacement. These are complementary signed
criteria, with different uniformity and degeneration boundaries. Neither
is asserted to imply the unrestricted contact inequality.

For both consumers the immediately usable statement is this: if a bounded
core has mass m, satisfies the displayed proximity condition, and has
conditional loss D_0, then the FULL profile gap is at least

    m [v (2 pi t)^(-n/2) q/(8t)] D_0 - (1-m).

A positive certified value excludes contact for that law, including the
Gaussian-tailed auxiliary laws when its conditions are actually checked.
Global profile order alone has not been shown to give those conditions.
No quantitative bound is claimed across covariance collapse or arbitrarily
large volumes. No prescribed fixed atom or lower support-mass bound is
introduced silently.

## Refresh and overlap checks

Before publication, all seven other researchers' newest completed reports
and the relevant source and graph neighborhood were refreshed. Two newly
published comparisons matter directly to the interpretation:

- R3's [reference-test coverage obstruction](../gaussian_uniform_set_reduction/REFERENCE_MIXTURE_BOUNDARY.md)
  shows why positive same-volume averaging of reference source sets cannot
  generally recover the actual source optimizer. Our proof does not use
  that coverage step. Its result does not invalidate R8's signed
  margin-minus-error criterion, as that source explicitly records.
- R4's [shallow-flap first variation](../gaussian_flap_depth_boundary/PROOF.md)
  gives a strict derivative and a compact-threshold exclusion for its
  particular geometry and weight reserve. The shared divergence method
  is credited prior work. Our estimate concerns arbitrary bounded
  contractions near an aligned full-rank isometry, supplies an explicit
  finite remainder, and uses volume rather than threshold. We do not
  claim to strengthen every branch of the flap theorem.

The certificate-degree obstruction, the geometric map-class separation,
and the latest unsuccessful numerical searches are context, not premises.
No numerical candidate, positive map class or prior theorem is repackaged
as evidence for the unrestricted sign. Source publication and finite
arithmetic checks are not independent mathematical acceptance.
