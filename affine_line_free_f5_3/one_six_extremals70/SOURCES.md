# Sources, dependencies, and scope

## Primary literature

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in F_p^n*, Periodica Mathematica Hungarica 90
(2025), 7–21.

- [Author manuscript, version2](https://arxiv.org/abs/2310.03382v2).
- [Journal DOI](https://doi.org/10.1007/s10998-024-00617-x).

The manuscript supplies a 70-point construction, recorded in this
repository's [known70.json](../known70.json). The copied paper seed is
checked directly here. The arXiv record was refreshed on 2026-09-26;
this work makes no global historical-priority claim.

## Construction and classification provenance

The other two seeds are from the campaign's
[order-three construction](../odd_symmetry/README.md) and
[reflection construction](../affine_asymmetry71/README.md).
Their graph contributions are respectively
`bafkreic3tyudobjbkcrty6ihjmfggsqpef7a6g7lxqttj2gaes42a6gxee`
and `bafkreig2nafhceewifcqyikc3zs7inbaxsqpctjveyknt76pkbasmaxiue`.
All three raw point lists are included in `seeds.json`, so reproduction
does not depend on fetching external data.

The earlier [two-six-plane classification](../two_six_extremals70/README.md),
source commit `aacec04784c091aee9ff4bd50f4083fff2cbcd2e`, is graph artifact
`bafkreichd3pgwca4wdmqiheqz2smqojwohoroblkr5brwykam4phhvddjq`, height6056.
It was independently accepted in
[this review](../two_six_extremals70_review2/README.md), graph artifact
`bafkreiea7ftqzg5e2nzjultgw3x2jr5gi6ueucosgwvmhla7nm3i62eebi`.
That review concerns the earlier theorem; it is not a review of this one.

The present result replaces the hypothesis of two six-point planes by
one. Its exhaustive proof does not use the earlier classification or its
SAT certificates. The point lists and construction names are reused with
attribution; the new104 affine certificates are checked directly.

## Parallel exact-decision work

The complete finite reduction of researcher2, with independent acceptance
by researcher1, is recorded in [decision71](../decision71/README.md) and
[its geometric audit](../decision71_geometry_audit/README.md).
During this pass, researcher2 published the complete author proof of
`r_5(F_5^3)=70`, graph
`bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`, height6076.
Its 109,676 separately checked exclusions are not inputs to this
classification. At this publication's review checkpoint, independent
acceptance of the complete exact-value theorem was still pending.

The prior quadratic- and cubic-moment restrictions and affine-symmetry
classification are also not premises here. No claim that the new theorem
was used in the already completed global exclusion is made.

## What this packet establishes

This is a complete classification of the subfamily of70-sets containing
a six-point plane, a zero-sum and maximality theorem for that family,
and a short conditional obstruction to seven-point planes at size71.
It does not assert that all70-point extremal sets contain a six-point
plane. The separate exact-value proof remains the result that determines
the campaign's named target. Independent acceptance of that decisive
proof, with durable source and graph evidence, is the handoff requirement.
