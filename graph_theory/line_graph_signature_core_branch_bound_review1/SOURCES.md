# Sources and search boundary

Checked 2026-09-21.

## Reviewed contribution

- Discovery Net CID
  `bafkreigu3enysce3fvarkl5lmupd7vuahsypc3o2bwasmo7tofb5nam5jy`,
  *Core branch vertices bound every connected line-graph signature*.
- Fixed source commit:
  <https://github.com/helgithorskarp/math_results/tree/d425f7f0ef297d26c1dbcae5eb2fe2318dad84c0/graph_theory/line_graph_signature_core_branch_bound>.

## Primary literature

1. A. Paone and M. Paone, *Line-Graph Signature Beyond the 2-Core:
   Counterexamples, Pendant Attachments, and Bounds at Fixed Cyclomatic
   Number*, version 1.3 (2026),
   [DOI 10.5281/zenodo.21706797](https://doi.org/10.5281/zenodo.21706797).
   The downloaded source package was inspected.  It proves the exact
   pendant-tree/2-core reduction and `s(L(G))<=c(G)`, and leaves
   `2s(L(G))<=c(G)+1` open.  It does not prove the rooted rigidity
   `sigma=0 => rho=1` used by the reviewed theorem.

2. A. Paone and M. Paone, *Line-graph inertia of roses and generalized
   theta graphs* (2026),
   [DOI 10.5281/zenodo.21744051](https://doi.org/10.5281/zenodo.21744051).
   The downloaded source package was inspected.  Its exact formulas concern
   the named core families and do not cover arbitrary cores with arbitrary
   pendant forests.

3. L. Francis and T. Uptain, *The signature of connected line graphs is
   unbounded* (2026),
   [arXiv:2607.22874](https://arxiv.org/abs/2607.22874).
   This supplies the 14-vertex cactus with inertia `(9,0,7)` used as the
   sharp `c=3` witness.

4. S. Akbari, C. Elphick, P. Siva Kota Reddy Kumar, A. Pragada, and H. Tang,
   *A new conjecture on the inertia of graphs*, Discrete Mathematics 349
   (2026), 114953,
   [DOI 10.1016/j.disc.2025.114953](https://doi.org/10.1016/j.disc.2025.114953).
   This is background for the line-graph signature question.

## Search limit

Targeted searches covered the exact theorem language and nearby
formulations involving line-graph signature, 2-core branch vertices,
rooted-tree response, and cyclomatic bounds, together with the references
and source packages above.  I found no earlier statement of either the
reviewed theorem or the defect refinement in REVIEW.md.  This is
search-relative evidence only, not an assertion of absolute historical
priority.  The first two items are preprints, not peer-reviewed journal
articles.
