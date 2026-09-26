# Sources, dependencies, and coordination

## Primary literature

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács, Péter Pál
Pach, Dániel Gábor Simon, and Nóra Velich, *Maximal line-free sets in
F_p^n*, Periodica Mathematica Hungarica 90 (2025), 7–21:
[primary manuscript](https://arxiv.org/abs/2310.03382v2),
[publisher DOI](https://doi.org/10.1007/s10998-024-00617-x).

This paper supplies the parameter, a 70-point construction, and the earlier
published upper bound of 73. Its point list is [known70.json](../known70.json)
in this repository and is checked directly against all 775 affine lines.
A bounded primary-source search during this pass found no exact-value
determination. No exhaustive historical-priority claim is made.

## Complete reduction and attribution

The complementary [two-low-plane theorem](../low_pair71/THEOREM.md),
developed by Team A researcher 3, forces two nonparallel planes of size
at most nine. Its moment refinement and fourteen exact integer
certificates supply a complete fifteen-type cover. All fifteen types
occur in the fixed twenty-type family enumerated here; the public
verifier replays that theorem and checks containment. Researcher 1
independently reported a successful replay of that counting package.

The alternative incidence argument in Sections 1–2 of
[THEOREM.md](THEOREM.md) was developed while the stronger teammate result
was in progress. It forces a plane of size at most nine, a second of size
at most ten, and excludes a unique small plane of size eight or nine.
It therefore suffices for the same twenty-type cover without the centered
moment refinement. The stronger teammate result is credited explicitly;
the redundant five types are retained to preserve the complete frozen
proof corpus and give a separate mathematical reduction route.

The incidence-template and planar-census code descend from
[low_planes72](../low_planes72/README.md), with new thresholds and exact
certificates at cardinality 71. A second planar enumeration uses fixed-size
backtracking and line occupancies. The quotient algorithms extend the
earlier deficit and direct-row enumerators in
[upper_bound71](../upper_bound71/README.md) to the full twenty-type domain.
`point_model.py` is the earlier direct point encoding, unchanged byte for
byte. The new full-group audit checks every representative against all
12,000 affine transformations, including cross-type identifications.

The three positive controls are the paper's 70-point set and researcher
4's [order-three example](../odd_symmetry/witness70.json) and
[reflection example](../affine_asymmetry71/witness70.json). Only their
explicit point lists and fresh direct checks are used here. The symmetry
classification results proving their inequivalence are not premises.

## Related results that are not assumptions

The team's earlier [upper bound 71](../upper_bound71/THEOREM.md) excludes
72 points through 4,332 checked lifts. Its
[independent review](../upper_bound71_review2/README.md) accepts that result
after a fresh complete proof replay. The earlier no-eight-plane review
has also been refreshed. These results establish the starting frontier;
their SAT exclusions are not imported into the new 71-point proof family.
The [second accepting review](../upper_bound71_review1/README.md) uses
complemented hole variables and a different gauge, supplying a distinct
encoding check for that earlier theorem.

Researcher 4's [affine-asymmetry theorem](../affine_asymmetry71/PROOF.md)
closes all affine-symmetry routes at size 71. The current lift formulas
impose only coordinate normalization, never invariance under a nonidentity
affine map. Thus all genuinely remaining asymmetric candidates are covered.

The prepublication refresh also added the
[universal local-consistency obstruction](../quotient_local_consistency71/PROOF.md).
It proves that independent projection-plane feasibility and agreement of
all shared-fiber marginal laws cannot eliminate any admissible 71-weight
quotient. The present formulas require one common integral assignment
across all 125 points, so their global lifting obligation is precisely
the information missing from that relaxation. No local completion
test is being counted as a global exclusion here.

Private pilots found no practical benefit from adding all derived
four-point-line clauses to the direct encoding. Two 32-case disjunctions
were slower to certify than their constituent direct formulas. Six
monotone core probes retained total fiber weight 71 and each covered only
its own representative. These are scoped negative observations informing
the selected execution method, not global impossibility claims about
alternative algorithms.

## Software trust

The proof uses exact Python integers, exhaustive C++20 enumeration,
Python-SAT 1.9.dev15 with CaDiCaL 1.9.5 as a trace generator, and separately
executed DRAT-trim. The [checker note](CHECKER.md) records the upstream
source, the two-line allocation patch, its controls, and actual binary
identities. Floating-point optimization was used only to discover the
integer dual certificates; no floating-point verdict enters the proof.

The imported source and point-list hashes are pinned in
[dependencies.json](dependencies.json). Complete source and compact
evidence hashes are in [SHA256SUMS](SHA256SUMS). Generated catalogues,
proof traces, checker logs and run checkpoints remain outside Git.
