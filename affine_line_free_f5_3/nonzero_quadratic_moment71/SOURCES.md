# Sources and dependency boundary

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in \(\mathbb F_p^n\)*,
Periodica Mathematica Hungarica 90 (2025), 7–21.
[Author manuscript](https://arxiv.org/abs/2310.03382);
[version of record](https://doi.org/10.1007/s10998-024-00617-x).
This is the primary source for the named extremal problem and the
70-point construction. Its published upper bound was 73. The present
package independently rechecks the planar upper bound 16.

The author's earlier [quadratic moment package](../quadratic_moments72/THEOREM.md)
introduced the centered-moment route for this campaign at cardinality 72.
Discovery Net:
`bafkreiamle5hqoxrssfa2xe4jatfux5g7u7sxdonwsf7iyus4vytsu7mqe`.
The cardinality-71 [low-plane cover](../low_pair71/README.md) introduced
the five normalized low-profile types and a two-low-plane reduction.
This package builds on the moment viewpoint, but assumes neither
earlier moment exclusions nor the low-plane cover.

The [low_planes72](../low_planes72/README.md) package supplied the
campaign's plane/line incidence template. Discovery Net:
`bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy`.
The planar census here is a new minimal implementation of the same
basic planar-cap input; all required finite facts are regenerated.

Researcher 2's [upper bound 71](../upper_bound71/THEOREM.md) excludes
cardinality 72 through 4,332 exact lifting cases.
Discovery Net:
`bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`,
height 5986; source commit
`e81f511a02ac5ef43f1005408ba370df110b7007`.
Together with the published construction, it leaves the live team
target \(70\le r_5(\mathbb F_5^3)\le71\).
Two accepting independent reviews are now published:
[review 2](../upper_bound71_review2/README.md), at commit
`5265b38b915aeb6701f42f8dbfa8699366b60609`, and
[review 1](../upper_bound71_review1/README.md), at commit
`8f0f8adb9db240c751d0eae6b9d4e43103c9eb34`.
The latter uses fresh complemented-hole formulas and a different gauge.
Their durable source was inspected during the publication refresh;
this package does not claim to have independently replayed those SAT
computations. Neither the upper bound nor its reviews are premises here.

Researcher 1 reported a successful independent replay of the earlier
low-plane cover. Researcher 4's
[affine asymmetry theorem](../affine_asymmetry71/README.md) excludes
nontrivial affine symmetry of a 71-point candidate. These durable
sources and bounded teammate reports were inspected for overlap.
No invariance of a candidate under a moment-preserving transformation
is assumed here, and no symmetry theorem is imported.

Researcher 1's new
[universal local quotient consistency theorem](../quotient_local_consistency71/README.md),
at commit `dbe9b798bbf92f469fdff5369e07890c29f9c7c4`, proves that
ungauged independent projection-plane lifts with full shared-fiber
marginal consistency cannot reject an admissible 71-weight quotient.
The present argument uses a single global cubic and quartic moment;
it does not duplicate that closed local-consistency route.

The [planar marginal relaxation obstruction](../../additive_combinatorics/line_free_planar_lp_obstruction/PROOF.md)
shows that a different point-marginal relaxation is feasible at 71.
Discovery Net:
`bafkreifwjecau65opqj3hmj5ba2d4dlig2advvmkjtkx5xztwpovu24o4y`.
The present proof uses simultaneous global polynomial moments and a
conic incidence identity, not an infeasibility claim about that relaxation.

Targeted primary-source searches were made for finite-field
square-valued ternary quartic classifications. No matching result was
identified in those searches. The finite lemma is established by the
included source; no historical-priority claim is made.
