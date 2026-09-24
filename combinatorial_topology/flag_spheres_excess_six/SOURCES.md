# Sources, overlap, and dependency boundaries

Primary manuscripts were inspected on 24 September 2026. Searches were
graph-first, followed by targeted literature checks. Absence from those
searches is not a historical priority claim.

## Published mathematical inputs

1. Jean-Philippe Labbé and Eran Nevo, *Bounds for entries of gamma-vectors
   of flag homology spheres*, SIAM J. Discrete Math. 31 (2017), 2064--2078.
   [arXiv:1612.01169v2](https://arxiv.org/abs/1612.01169v2).
   PROOF.md specifies the exact numbered inputs. The near-maximal-dimension
   lemmas in Section 4 are derived consequences of their suspension, join,
   and equator results. They are not presented as independent classification
   discoveries. The excess bound for the two-antipode edge link follows
   because it is an induced equator with at least two exterior vertices.
2. Michael W. Davis and Boris Okun, *Vanishing theorems and conjectures for
   the l2-homology of right-angled Coxeter groups*, Geometry & Topology 5
   (2001), 7--74. [arXiv:math/0102104](https://arxiv.org/abs/math/0102104).
   Theorem 11.2.1 provides the flag rational-homology 3-sphere inequality.
   The coefficient-field bridge and the correct dimension-four factor are
   explained in PROOF.md; every face link is treated separately.

## Accepted graph inputs

The all-dimensional conclusion uses these results in dimension five only.
All new gamma_2 and high-dimensional structural statements are independent
of both of them.

- **Seventeen vertices:** every flag generalized homology 5-sphere on
  17 vertices has gamma_3>=0. Original contribution
  `bafkreieceq3ktydrabvxlu6fqn7zllvmi6lk4346k4y35ylczmychowcha`, h1308;
  independent acceptance
  `bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i`, h1340.
  The source is the `charney_davis_17` package in the
  [original research repository](https://github.com/njallskarp/math_source_code_open/tree/main/charney_davis_17).
  The accepted proof derives the unique hypothetical negative complement
  profile `3^16 4^1`, then forces gamma_2=-2 in the degree-four vertex link.
  It includes a partial Lean formalization, not an end-to-end topology proof.
- **Eighteen vertices:**
  [proof and reproducible certificates](../charney_davis_18_vertex_certificate/README.md),
  source commit `26909e416526f7c67d4eaeaa430325e0f8c99559`;
  graph `bafkreifs3epeuwqoiofrkb6q77edryqpntvpbh345tmjzt5f5sotwleraa`, h5836.
  [Independent review](../charney_davis_18_vertex_certificate_review1/REVIEW.md),
  commit `3a21976ca72231137344d6daedccdbd212b18479`;
  graph `bafkreiey3qnfcl3waqlswpd36jn4owkgn33t3i73kr443kvlrmiqiv7j6m`, h5842.
  The reviewer accepted the exact eighteen-vertex claim with high confidence,
  regenerated all 25 checked UNSAT certificates, and supplied a separately
  written LRAT checker and direct integer-model verification.
- **Normalization correction:**
  `bafkreic3c6ylmrfkjerxuc37c2dc5bgsso4jiijvrbyvvmwhzys4ynog5e`, h3585,
  corrects the reciprocal factor in the old seventeen-vertex review.
  This does not affect its nonnegativity argument. The present proof derives
  `2 gamma_2(Y)=sum_v gamma_2(lk(v))` directly in the h basis.

The source graph problem was
`bafkreid3obaz2cfq2nyd3v2ernkylaa3iv7l3otwzok7zwyxymqkukstme`.
The initial committed refresh was h5843. The eighteen-vertex proof and its
new review motivated a reusable transfer instead of another order increment.

## Recent literature overlap

Biplab Basak, Debolina Ghosh, and Raju Kumar Gupta,
[*A Complete Classification of Discrete d-Pseudomanifolds with at Most
2d+7 Vertices*](https://arxiv.org/abs/2606.29753v1), June 2026,
uses **d for the dimension**, whereas this package uses d-1. Their
classification through `2d+6` vertices therefore concerns excess at most
four in our notation. Section 4 treats topology at excess five, and
Section 5 explicitly states gamma_2 nonnegativity through that range.
This overlap is credited: no novelty claim is made for gamma_2 at excess
at most five or for their classified objects. Their preprint is context,
not a proof dependency here; the argument above uses the LN inputs and
the explicitly accepted finite graph theorems.

Targeted searches for all-dimensional nonnegative gamma-vectors at excess
six, the two-antipode high-dimensional reduction, and the eighteen-vertex
base found no earlier source covering the full claimed range. This supports
only a search-relative novelty statement. The new publication packages the
six-excess-vertex theorem and its explicit structural reduction, not a
priority claim about lower-excess results.

## What is and is not checked

The standard-library audit cross-checks closed complement formulas against
direct graph face counts and exact triangular h-to-gamma conversion. It
also checks the general link identity on h-basis polynomials, the complete
small degree-profile calculation, and constructive sphere fixtures.

It does not independently prove the cited topology, classify all spheres,
or replace mathematical review of the induction and dimension bounds.
The solver is absent from this new audit; the inherited eighteen-vertex
theorem still has its documented human reduction and checked-trace boundary.
