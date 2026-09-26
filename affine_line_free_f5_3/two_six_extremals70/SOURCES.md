# Sources, attribution, and scope

The human-named target is the exact value of \(r_5(\mathbb F_5^3)\).
This contribution supplies a constructive extremal classification and
an obstruction concerning seven-point planes at cardinality 71.
It is not a numerical improvement or an exact-value announcement.

## Primary literature

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in \(\mathbb F_p^n\)*,
Periodica Mathematica Hungarica 90 (2025), 7–21.
[Author manuscript](https://arxiv.org/html/2310.03382v2);
[journal article](https://doi.org/10.1007/s10998-024-00617-x).
Figure 4 supplies the paper's 70-point construction. The repository
transcription used here is [known70.json](../known70.json), last changed
at source commit `33bb5788b6ecf84a706fbd3eea99cf336f23e25b`.
The planar cap is rechecked from definitions in this package.

## Team artifacts

* The [order-three construction](../odd_symmetry/witness70.json),
  source commit `3703f831791312b938f79cae978f11da50b4639f`,
  supplies the second seed.
* The [reflected construction](../affine_asymmetry71/witness70.json),
  source commit `b09e0372b9c9e6e8b416543ff9b6c469e7f07b79`,
  supplies the third seed. Its earlier affine-asymmetry theorem is
  contextual and is not assumed in the classification proof.
* Researcher 2's [complete 71-point cover](../decision71/README.md),
  source commit `6d2f193aecad54cc41dab4cdf67c16f9add58cc2`,
  supplies the two-low-plane quotient method and the direct
  125-variable formula code. `point_model.py` is copied from
  that source; the two quotient enumerators are adaptations to a
  different cardinality and family. Proof-stream handling follows
  the same verified native-stream procedure. The global 71-point
  certificate computation is not replayed or assumed here.
* Researcher 3's [nonzero quadratic-moment theorem](../nonzero_quadratic_moment71/README.md),
  source commit `8465b47f44a08f4273fd76485c5c5d34a47f7640`,
  includes the previous incidence bound \(f+3\epsilon\le5\).
  The present result improves this to \(f+3\epsilon\le4\) without
  using that theorem, its conic argument, or its quartic census.
  `planar_cap.cpp` is copied from its source.
* Researcher 1's [gauged local-consistency obstruction](../gauged_quotient_obstruction71/README.md)
  explains why local planar marginal feasibility cannot settle lifting.
  The present result checks entire integral point sets and does not
  use that insufficient relaxation.

All seed point lists are copied into `seeds.json` and checked
directly. The 48 positive objects in `models.json` carry explicit
affine equivalence certificates. This avoids requiring any earlier
classification or symmetry theorem as a proof premise.

## Software and trust

Tested versions: Python 3.12.14, Python-SAT 1.9.dev15, CaDiCaL 1.9.5,
and GCC 12.2.0. The
[official DRAT-trim repository](https://github.com/marijnheule/drat-trim)
supplies the independent proof checker, at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The replay uses the unmodified checker. It is built separately and is
not vendored here.

The ordinary-language reduction and exact programs are not formalized.
Independent source review of the new classification is pending.
The source search and team refresh found no existing copy of this
classification, but no historical priority claim is made.

The campaign's accepted interval remains 70–71. The exact-value
handoff gate is not met by this contribution.
