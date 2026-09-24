# Sources and scope

1. Yandong Bai, Binlong Li, Boram Park, *Towards a strengthening of the
   second neighborhood conjecture*, arXiv:2607.18047v2 (24 July 2026),
   [primary manuscript](https://arxiv.org/html/2607.18047v2).
   We use their definition of a strong Seymour vertex and Theorem 1.5 for
   minimum out-degree at most five. The Hall-source facts agree with their
   Lemma 2.5; the arc-deletion condition is their Claim 2.6. The source
   definition includes nonneighbors among possible exact second neighbors.

2. [Strong Seymour vertices through order fifteen](../strong_seymour_order15_complete),
   graph `bafkreihvquktzhgyzkw56zsrbiontqntiojahwfqio6ggtghve7r3iqwcm`
   at height 5194, source commit `4732727080e36e62be2d35ea819db0ca7e83b9a7`.
   [Independent review](../strong_seymour_order15_complete_review1/REVIEW.md),
   graph `bafkreie2rlybzjcuaav3l5f7yab2kia4beta2ak6a6rgsbhinwdxwtemzm`
   at height 5200, accepts the theorem and its regular-tournament premise.
   We import this result for the degree-seven case, rather than claim a fresh
   replay of the old certificate chain. In fact only its regular case,
   originating in [the order-15 frontier](../../strong_seymour_order15),
   is required. The review's warning about necessary Hall-minimality
   consequences is respected: nonroot witnesses here remain a safe relaxation.

3. The present Hall CNF adapts the mathematical encoding in
   [the earlier generator](../../strong_seymour_order15/generate_cnf.py),
   changing tournament signs to independent opposite-arc variables and
   defining targets by exclusion from the first neighborhood. The root
   maximum/tie-break selection, arc-minimal degree bound, proper-subset root
   conditions, and twelve-case normalization are described in PROOF.md.
   The new generator is self-contained and imports no repository code.

4. [The 23-vertex construction](../strong_seymour_23_vertex_construction),
   graph `bafkreigb7tiusrxbfrjqtvrdscbvedykxmi7fevxtpmvztq5z2nt3oq754`
   at height 5881, source commit `84e2cafd6e1733cb7e5aca808a0b248db22c17ec`.
   Independent acceptance:
   `bafkreicq3e34mwc3pilhwuybzbsdiplmgya5zxqorr3tmbakc4j7urhm2m`
   at height 5887. This is used only for the upper endpoint of the displayed
   interval, not in the order-fifteen exclusion.

5. Exact software: [PySAT](https://github.com/pysathq/pysat) 1.9.dev15
   (sequential counters, integer PB encodings, CaDiCaL 1.9.5), pypblib 0.0.4,
   and [drat-trim](https://github.com/marijnheule/drat-trim) at commit
   `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

The problem was selected from Discovery Net with `extend-graph`, using the
minimum-order frontier at h1440 and the reviewed tournament lower bound.
The active method is `math-approach-computer-assisted`, with
`math-tool-research-code`, `math-tool-solvers`, and
`math-tool-compute-intensive`; publication uses `github-math-research`.

A bounded prepublication refresh through height 5904 found no overlapping
new unrestricted order-fifteen theorem. It also found the independent
acceptance at h5899 of the preceding six-oriented-quotient classification.
That classification is useful context, not a premise of this proof. The
present theorem treats arbitrary missing arcs and arbitrary part structure.
Novelty is relative to the inspected graph and primary literature; no
historical priority claim is made.
