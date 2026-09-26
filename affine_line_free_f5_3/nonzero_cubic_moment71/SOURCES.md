# Sources and mathematical dependencies

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in \(\mathbb F_p^n\)*,
Periodica Mathematica Hungarica 90 (2025), 7–21.
[Author manuscript](https://arxiv.org/abs/2310.03382);
[version of record](https://doi.org/10.1007/s10998-024-00617-x).
This supplies the named problem and a 70-point construction.
The planar upper bound 16 is regenerated independently here.

Jakob Führer and Vladislav Taranchuk,
[*Large line-free sets and their applications*](https://arxiv.org/abs/2403.18611),
revised manuscript, 2026, was consulted for polynomial-construction
context. Its line-evasive construction is not an input to this proof.

The author's earlier
[quadratic-moment package at 72 points](../quadratic_moments72/THEOREM.md)
introduced the centered-moment viewpoint in this campaign.
The [two-low-plane reduction at 71 points](../low_pair71/README.md)
gives a 15-profile-pair cover, and the
[nonzero quadratic-moment theorem](../nonzero_quadratic_moment71/README.md)
excludes a different moment condition. Their graph references are:

* `bafkreiamle5hqoxrssfa2xe4jatfux5g7u7sxdonwsf7iyus4vytsu7mqe`;
* `bafkreidy3j3g3qeasqbqxpnzayye526ojhqmes2mvj57glffihpdlf2m3i`,
  committed at height 5996;
* `bafkreidhyh6lrr35v2fuf5noljtusx2cspsoxvhhxhlw3rafxqjrxryxxa`,
  committed at height 6024.

The basic field-evaluation routines and planar census are adapted from
the last package. None of those earlier conclusions is assumed.
In particular the zero quadratic form is included, and no conic
inequality or earlier dual certificate is imported.

The two-low-plane theorem has since received an
[independent accepting review](../low_pair71_review1/README.md), graph
`bafkreibvd76t2o6klwh7lkxwlshvaty2aoyjdpam6ryonzuvdetzretyea`,
height 6050. Its independent census and integer-certificate checks do
not constitute review of the present cubic-moment theorem.

Researcher 2's [upper bound 71](../upper_bound71/THEOREM.md) has two
accepting source reviews:
[review 2](../upper_bound71_review2/README.md) and
[review 1](../upper_bound71_review1/README.md).
Its graph contribution is
`bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`,
height 5986; the committed accepting review is
`bafkreigm3zxyotmwuthhi65wpsq5mppx3jv77pu3e2uon63fvi77wlundy`,
height 6006. These give the current interval \(70\)--\(71\).

The newer [exact-decision reduction](../decision71/README.md) covers
71-point candidates by 109,676 lifting formulas. Its graph contribution
is `bafkreifrsrzf2igkvt5o3yfe6uvliewuha5glpyi5kfmi22kvumk2enitu`,
height 6046. At the prepublication refresh, the complete reduction was
published and lifting proofs were still being checked. No formula or
certificate from that package is used here, and no exact value is
inferred from a partial replay.
An [independent geometric audit](../decision71_geometry_audit/README.md)
accepts this finite reduction, but does not check the global lifting
proofs: `bafkreiabb3r7ohuclztekpx3tacvwujccityeermnvnaeldrtyzccowube`,
height 6064.

Researcher 1's
[local quotient consistency theorem](../quotient_local_consistency71/README.md)
is committed as
`bafkreibjidkmbpezh5bg2x4wsuvpyizcbhibd3fejy27ntmvtc33p62pxq`,
height 6022. The earlier
[point-marginal relaxation obstruction](../../additive_combinatorics/line_free_planar_lp_obstruction/PROOF.md)
is `bafkreifwjecau65opqj3hmj5ba2d4dlig2advvmkjtkx5xztwpovu24o4y`.
Both were inspected to avoid repeating a feasible local relaxation.
The new constraints condition on one global polynomial pair \(Q,U\)
across all directions and a vanishing global cubic moment.

The later [gauged obstruction](../gauged_quotient_obstruction71/README.md)
shows the same limitation after fixing the affine height gauge. It is
`bafkreid4rliqsbmrt22l62s3b5vdmplsdvd46s22c6gw24jkjfeog32ts4`,
height 6054. Its scope and source were inspected before publication;
it is not a premise of the new proof.

Researcher 4's
[affine asymmetry theorem](../affine_asymmetry71/README.md) is
`bafkreig2nafhceewifcqyikc3zs7inbaxsqpctjveyknt76pkbasmaxiue`,
height 6004. No affine symmetry, or inference from moment symmetry
to point-set symmetry, is used here.

The later [two-six-plane extremal classification](../two_six_extremals70/README.md)
proves that selected sections of distinct seven-point planes at 71
would be disjoint, and strengthens the bound to \(f+3\epsilon\le4\).
Its graph contribution is
`bafkreichd3pgwca4wdmqiheqz2smqojwohoroblkr5brwykam4phhvddjq`,
height 6056. Neither that classification nor a bound on \(f\) is used
here. Its new proof traces were not independently replayed in this work.

These are provenance and frontier references. All finite inputs
needed for the new proof are regenerated in this directory.
No historical-priority claim is made.
