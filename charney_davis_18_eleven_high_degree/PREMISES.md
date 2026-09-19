# Premise ledger

This lists the mathematical dependencies separately from code checks.
No implementation agreement is presented as independent validation of a
human reduction.

| Premise | Source and role | Boundary |
|---|---|---|
| Homology in every face link over a field | Definition of the theorem's input | Global homology alone is insufficient |
| Nonnegative gamma_2 for flag homology 3-spheres | [Davis--Okun, Theorem 11.2.1](https://arxiv.org/abs/math/0102104) | Lower-dimensional external theorem, not the conjectural five-dimensional conclusion |
| Rational coefficients suffice | Universal coefficients and Euler characteristic, applied to every face link | Vanishing field homology forces lower rational Betti numbers zero; the top rational Betti number follows from Euler characteristic. Integral torsion-freeness is not asserted |
| Induced vertex links and antipode acyclicity | [Labbé--Nevo, Lemma 2.1](https://arxiv.org/pdf/1612.01169v2) | Needed in the predecessor's cubic triangle restriction |
| A minimum-antipode vertex with a suspension link forces a cycle join | Same source, Theorem 3.5(i) | The minimum condition is essential. It is applied to cubic vertices of H, or to degree-two vertices after assuming a small sphere has no degree-one complement vertex. It is not applied directly to arbitrary quartic vertices |
| Antipode-two gamma identity and the small gamma_1=2 link types | Same source, Lemma 3.4 and the ell=2 base case of Theorem 5.2 | These imply the thirteen-vertex gamma_2-zero suspension lemma, explicitly recalled in PROOF.md |
| J triangle-free/C4-free, 7<=e<=10; degree-three-root component structure; local link formulas | [Two-triangle note, PROOF.md](../charney_davis_18_two_triangles/PROOF.md) | Human structural dependency; no graph-catalogue completeness premise. Its T<=2 conclusion is not used |
| A suspension link gives an isolated K2 in its induced complement | Definition of suspension and flag induced links | All other neighbors of the pair must lie in N_H(q), which creates the finite local incidence problem |
| Quartic c=2 forces a cubic P4 with degree-two internal vertices | New compatibility lemma in this note | Human proof treats QQ, CQ, QC, CC suspension-pair types. `verify.py` also checks all 100 incidence patterns |
| At least ten cubic complement vertices if the minimum degree is three | [Ten-high-degree theorem](../charney_davis_18_ten_high_degree/PROOF.md) | Used only for the eleven-vertex corollary, not profile exclusion |
| Exactly ten cubics forces 3^10 4^8 | [Ten-cubic rigidity theorem](../charney_davis_18_ten_cubic_rigidity/PROOF.md) | Used only for the corollary; imports its explicit finite degree-profile table |

The earlier [independent review](../charney_davis_18_review1/README.md)
accepts the nine-high-degree theorem. It does not independently validate
the ten-high-degree, ten-cubic rigidity, two-triangle, or present extension.
The current note has no independent review or proof-assistant formalization.

Primary-literature and committed graph searches were refreshed on
19 September 2026. No matching profile-exclusion theorem was found in the
searched sources. This is search-relative evidence, not a global priority
claim. The auxiliary small-sphere suspension statement is credited as a
consequence of the established literature, not as a new classification.
