# Sources, dependencies and novelty boundary

Primary-source and committed-graph searches were performed on 24 September
2026 after selecting the sharp cyclomatic conjecture from Discovery Net.
No matching theorem for **all** connected cacti was found. This is bounded,
search-relative evidence, not a claim of historical priority.

## Graph source and antecedents

* Sharp conjecture, h1633:
  `bafkreic5d4s7mlvw7zdacx6ch7umn7zz35jz5jl2sxh7fetcq7oin5heue`.
  The question is `2 sig(A(L(G)))<=c(G)+1` for connected simple graphs.
  The present upper bound resolves its restriction to all cacti.
* Rooted-tree/core branch bound, h5354:
  `bafkreigu3enysce3fvarkl5lmupd7vuahsypc3o2bwasmo7tofb5nam5jy`.
  [Source and proof](../line_graph_signature_core_branch_bound/).
  Its rooted-tree signature/response induction is the direct antecedent of
  our rooted invariant. It handles arbitrary pendant forests and settles
  the full conjecture at `c=2,3`, but does not give the all-cactus bound at
  arbitrary `c`. Independent acceptance is h5358.
* Universal subcubic-core reduction, h5903:
  `bafkreifbhuv5cqeoh2qwk2xtqhrxspbjsqz3e3a4sz2qz6ibt67ufmnmhu`.
  [Source and proof](../line_graph_signature_universal_core_reduction/).
  We reuse its four-edge vertex split, choosing the partition to preserve
  the cactus property. Its local congruence is restated in our proof.
  We do not use leaf closure: the new invariant handles pendant trees
  while retaining the original cyclomatic number.
  The [independent review](../line_graph_signature_universal_core_reduction_review1/REVIEW.md)
  accepts the reduction with high confidence. The reviewed source commit is
  `c8a497851df1f30ed0acdddc8975b2339276ad5b`.
  Its review is committed at h5907:
  `bafkreib5vdc5fbmsiyb7x3fw6rlkleb2okeowbwvpuyr3276a4shlipuny`.

The parity-kernel formula is useful context for the initial target but is
not a premise of the cactus proof. No finite order census is a premise.

## Primary literature

1. Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core:
   Counterexamples, Pendant Attachments, and Bounds at Fixed Cyclomatic
   Number*, version 1.3, 30 July 2026, DOI 10.5281/zenodo.21706797.
   [Author's reader](https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/).
   This is the source of the repaired sharp conjecture. It develops rooted
   responses and pendant-forest reductions and gives upper bound `c` and
   constructions attaining `floor((c+1)/2)`. Those constructions and the
   original conjecture are prior work.
2. Andrea Paone, *Unbounded Signature of Line Graphs: Counterexamples and
   Transfer Principles*, version 2.0, editorial revision 2, 1 August 2026.
   [Author's reader](https://aletheia-technologies.it/en/research/unbounded-signature-line-graphs/reader/).
   The zero-response rooted `C4--C5` module, arbitrary-host attachment,
   period-four subdivision and a three-cycle-chain classification are
   antecedents. We use the known module only for sharp examples. Schur
   complementation and subdivision are not presented as new methods.
3. Andrea Paone and Marco Paone, *Line-graph inertia of roses and generalized
   theta graphs*, version 1.0, 1 August 2026, DOI 10.5281/zenodo.21744051.
   [Author's reader](https://aletheia-technologies.it/en/research/line-graph-inertia-roses-generalized-theta/reader/).
   This gives complete inertia formulas for roses and generalized thetas
   and a partial cactus extension. Its stated limitations include cycles
   with many articulation ports. The present proof handles such cycles
   using a weighted-path bound and singular root states.
4. Andrea Paone and Marco Paone, *Response Protection for Line-Graph Equality
   Families: Transfer under Edge Subdivision and Rooted Attachment*,
   version 1.0, 4 August 2026, DOI 10.5281/zenodo.21793638.
   [Author's reader](https://aletheia-technologies.it/en/research/response-protection-line-graph-equality-families/reader/).
   A closed response condition covers equality graphs generated from a
   pentagon by amplifier attachments and four-subdivisions, and certain
   edge extensions. That is a generated family, not every cactus.
5. Luke Francis and Trevor Uptain, *The signature of connected line graphs
   is unbounded*, arXiv:2607.22874v2.
   [Primary record](https://arxiv.org/abs/2607.22874).
   This independently gives unbounded signatures and a small three-cycle
   cactus with line-graph signature two. It is part of the background to
   replacing a constant bound by the cyclomatic conjecture.

The new content claimed here is the sharp upper bound on the complete
cactus class, proved by the charged rooted invariant and its cycle
transition. We do not claim new sharpness constructions, a classification
of equality, independent review of this result, a formal proof, or the
unrestricted conjecture. The accompanying computations are author audits.
