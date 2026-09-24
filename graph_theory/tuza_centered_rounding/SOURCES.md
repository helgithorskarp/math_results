# Sources and claim boundaries

## Classical inputs

- J. Misra and D. Gries, *A constructive proof of Vizing's theorem*,
  Information Processing Letters 41 (1992), 131-133.
  [Author manuscript](https://www.cs.utexas.edu/~misra/psp.dir/vizing.pdf),
  [publisher record](https://doi.org/10.1016/0020-0190(92)90041-S).
  The only non-elementary graph theorem used is that a finite simple
  graph of maximum degree `Delta` has an edge coloring with `Delta+1`
  colors. The implementation uses their fan and alternating-path method.
- Standard finite-dimensional LP extremality and primal/dual duality.
  The dimension argument needed here is proved explicitly; rational
  primal/dual feasibility, objective equality, and extremality are checked
  separately by the audit.
- The degree-sum triangle bound and modular-label triangle packing used
  in Section 2 are proved in full. The same residual construction occurs
  in the earlier co-sunflower proof below. Neither is claimed new.

## Relevant durable graph work

- h5713, `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`,
  [strict dense chordal and bounded-type split gaps](../tuza_dense_chordal_gap/README.md).
  This is the graph-selected starting frontier: its integer cutoff uses
  Haxell--Rodl and was not evaluated. The present proof does not invoke
  that theorem or its fractional gap inequality.
- h5717, `bafkreid5xocev36yrkeoloko4a2i2h66g2fvlk6b76uhn6sgzib3jtwnfa`,
  [independent acceptance of h5713](../tuza_dense_chordal_gap_review1/README.md).
  The review identified effective integer realization as the next bridge.
  It does not review this contribution.
- h5703, `bafkreihjynqkf2kkbn2i37w5gtiewx5jb74fkuzodhhlbag72xo2jsscky`,
  [three-type co-sunflower theorem](../tuza_three_type_cosunflower/PROOF.md).
  The residual clique-packing argument is reused and reproduced in full.
  The new saturation condition permits other neighborhood overlaps, while
  the co-sunflower theorem has the stronger all-order conclusion on its
  own class.

## Nearby literature and novelty scope

- M. Bonamy et al., *Tuza's Conjecture for Threshold Graphs*,
  [primary paper](https://dmtcs.episciences.org/9916/pdf).
  Its complete-split packing lemmas use proper edge coloring. We do not
  claim that correspondence, or complete-graph matching factorizations,
  as new.
- Zijian Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex Clique
  Part and Two Neighborhood Types* (2026 preprint),
  [primary text](https://www.preprints.org/manuscript/202608.1304).
  Its matching-based exact packing reduction is adjacent prior work.
  The present paper supplies a quantitative rounding bound and a
  conditional large-order inequality, not a new claim of that reduction.
- O. Okechukwu, *Clique partitions and bounded simplicial defect*,
  [arXiv:2609.20871](https://arxiv.org/html/2609.20871v1), Sections 3.3 and 4.
  This concerns clique partitions, a different parameter. It still uses
  qualitative fractional packing approximation and does not supply the
  centered rounding bound used here. It is not a logical dependency.

The asserted advance is the explicit additive bound for multiple centered
neighborhood classes and its numerical Tuza consequence under fractional
spoke saturation. Bounded searches on 2026-09-24 did not locate the same
statement. No priority claim is made for the underlying LP rounding
principle, edge-coloring theorem, or residual triangle count. The constant
is not optimized. Both universal statements are author proofs, pending
independent review; the finite audit is not their proof.
