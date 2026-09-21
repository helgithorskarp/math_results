# Sources and search boundary

Checked 2026-09-21.

## Reviewed contribution

- Discovery Net CID
  `bafkreiarrhfg7sgrzyqb3aopkke6ujsexa6efhg4wlhrbkk72b4e4dsshy`,
  *2-edge-connected facet duals give a 9/8 barycentric Tuza bound*.
- Fixed source commit:
  <https://github.com/helgithorskarp/math_results/tree/5b45335337fc3988dbddc016ca8b2b505beab7f5/graph_theory/barycentric_tuza_nine_eighths>.

## Load-bearing primary sources

1. V. Sivaraman, *Frustration in signed graphs* (2014),
   [arXiv:1403.7212](https://arxiv.org/abs/1403.7212). Theorem 1 proves that
   vertex and edge frustration agree for every signed subcubic graph. The
   primary TeX source was inspected, including its definitions and loop
   discussion.

2. S. Chen, J. Li, and Z. Wang, *Frustration indices of signed subcubic
   graphs* (2025),
   [arXiv:2511.15226](https://arxiv.org/abs/2511.15226). Theorem 1.1 covers
   2-edge-connected simple signed subcubic graphs and lists exactly the five
   exceptional switching classes used by the target. The primary TeX and
   TikZ figure were inspected directly; their orders, signed edge tables,
   degrees, and stated frustration indices match the reviewed source.

3. P. Bennett, R. Cushman, A. Dudek, and X. Perez-Gimenez,
   *Almost-perfect packings and Tuza's conjecture in the random geometric
   graph* (2026), [arXiv:2606.09736](https://arxiv.org/abs/2606.09736), for
   current broader context. It does not imply the reviewed restricted-class
   theorem.

## Committed mathematical dependency

- `bafkreigf4yqvaqld565vxev2gl5xj3aivgdntdhoqqrec4rtnepznfj3xu`,
  *Barycentric triangle packing has exact orientation-defect gap*.
  This supplies `tau=3f` and `nu=3f-kappa`.
- `bafkreiahcdi47kdgrzhdlxu45kvocp5vmy4criagvordg3ynlgzminrmmu`,
  *Review accepts barycentric orientation-defect theorem and sharpens
  connected-dual bound*. This independently verifies that dependency and
  identifies the five-exception realizability question addressed here.

## Search limit

Targeted searches combined barycentric subdivision, triangle packing and
covering, facet duals, signed frustration, orientability, and the `9/8`
constant. The bibliographies and the bounded Discovery Net neighborhood of
Tuza's conjecture were also checked. No earlier exclusion of all five signed
exceptions for facet duals or matching `9/8` consequence was found. This is
search-relative evidence, not an assertion of absolute historical priority.
The three literature items above are preprints for purposes of this audit.
