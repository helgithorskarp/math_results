# Primary-source audit, 12 September 2026

The exact target and selection trail remain in the
[parent literature file](../literature.md). This pass retains that target.
The new results here are triangle replacement, perfection of a connected
gem/bull-free prism-containing graph, and the resulting all-order critical
`C6` exclusion. We did not find these statements in the sources checked;
this is not an exhaustive priority claim.

* Beaton and Cameron, *Vertex-critical graphs in co-gem-free graphs*,
  Theoretical Computer Science 1042 (2025), 115234:
  [authors' arXiv text](https://arxiv.org/html/2408.05027v2),
  [journal](https://doi.org/10.1016/j.tcs.2025.115234).
  Their critical co-gem/bull computations agree with the `P3+P1`-free class
  through `k=6`. The all-`k` equality is the campaign target; it should not
  be called their Conjecture 7.1, which concerns a different census.
* Belavadi and Karthick, *Vertex-critical co-gem-free graphs* (2026):
  [primary text](https://arxiv.org/html/2606.11757v1).
  The paper addresses the house and dart finiteness cases, not the bull
  target. The document displays an August 24, 2026 date, while arXiv labels
  the version June 10, 2026; this metadata difference is retained explicitly.
* Chudnovsky, *The structure of bull-free graphs II and III—a summary*,
  revised April 23, 2011:
  [author manuscript](https://web.math.princeton.edu/~mchudnov/bulls_summary.pdf).
  Its Theorem 4.1 forces an **unfriendly** trigraph with a prism to be the
  prism. Unfriendly includes the absence of homogeneous sets and certain
  homogeneous pairs as well as gems. Our connected-graph theorem imposes
  neither of those decomposition assumptions. The proof here does not
  invoke that theorem or assume its hypotheses for a critical graph.
* Chudnovsky, Cook, Davies, and Oum, *Reuniting chi-boundedness with
  polynomial chi-boundedness*, 2025 manuscript:
  [author PDF](https://web.math.princeton.edu/~mchudnov/Pollyanna.pdf).
  The prime gem/bull homogeneous-pair restrictions in Lemma 7.11 and the
  structural decomposition in Theorem 7.12 were inspected. They motivate
  possible later residual arguments but are not used to prove this result.
* Maffray and Pastor, *4-coloring (P6,bull)-free graphs*:
  [author manuscript](https://arxiv.org/abs/1511.08911).
  Its Lemma 2.3 describes attachments to a P3-connected graph. Its
  prime `(P6,bull,gem)` theorem requires `P6`-freeness; that hypothesis
  cannot simply be assumed for the complement of our target graph.
* Chudnovsky, Robertson, Seymour, and Thomas, *The strong perfect graph
  theorem*, Annals of Mathematics 164 (2006), 51–229:
  [journal theorem and abstract](https://annals.math.princeton.edu/2006/164-1/p02),
  [author PDF](https://web.math.princeton.edu/~pds/papers/perfect/perfect.pdf).
  This is the external theorem actually used: a graph is perfect exactly
  when it has no odd hole or odd antihole.

Targeted searches combined gem/bull, prism, triangle replacement or
contraction, critical graphs, and `C6`. No later settlement or duplicate
was identified. The graph and authorized repository were also refreshed
before publication. Other active campaign work concerns modular subset
sums and nonoverlapping binary codes; neither overlaps this result.

No coloring-preservation property is asserted for the triangle operation.
For example, replacing a triangle in a diamond can change the minimum
number of cliques covering its vertices from two to one. The operation
preserves the two forbidden induced subgraphs, which is exactly what the
perfection argument needs.
