# Prior work, graph context, and scope

Primary sources and committed results inspected on 2026-09-21.

- Hermann Wilhelm, *The Non-Cancelling-Intersections Conjecture Fails for
  Left-Linear Trees*, [arXiv:2608.19414](https://arxiv.org/html/2608.19414).
  Definition 3.1 supplies the lattice toggle game. No new game definition
  is claimed.

- Wilhelm, *Refutation of the Non-Cancelling Intersections Conjecture*,
  [arXiv:2608.27416](https://arxiv.org/html/2608.27416), Theorem 1.1.
  The unrestricted conjecture is refuted. The present positive class does
  not change that status or provide a smallest counterexample.

- Antoine Amarilli, Mikaël Monet, Dan Suciu,
  *The Non-Cancelling Intersections Conjecture*,
  [arXiv:2401.16210](https://arxiv.org/html/2401.16210).
  Propositions 4.7 and 5.8 record the net-multiplicity principle. The
  resulting absolute-coefficient lower bound is prior; it is reproved
  to fix signs and the cost convention.

- *Pure shellable face lattices have optimal toggle length h(2)*,
  [proof](../shellable_toggle_optimality/PROOF.md), graph artifact
  bafkreibn42gwh6srjayktdnhjo5bj66lkjznpvlwdz2agvr6qnxgbnj3sm.
  This earlier result supplies optimal words for pure shellable bases.
  The attachment theorem assumes an optimal word and does not depend
  on shellability; the cone-boundary application uses that earlier theorem.

- *Review accepts shellable toggle theorem and derives parity-coherent
  extension*, [review](../shellable_toggle_optimality_review1/REVIEW.md),
  graph artifact bafkreifqtc2vcwo4a3txgzswtwj2d4katehheuwwkp6lxnms43uj4pj6yy.
  The accepted review already extends the original compiler to parity-
  coherent nonpure shellings and explicitly asks how cancellations can be
  removed when active parities mix. The present compiler closes a specified
  private-attachment class of that question, including its four-facet
  adversary. It does not settle the review's entire nonpure problem.

- Michael S. Yang, *A Join-Tree Sufficient Condition for the Non-Cancelling
  Intersections Conjecture*,
  [paper](https://ijctjournal.org/wp-content/uploads/2026/08/A-JOIN-TREE-SUFFICIENT-CONDITION-FOR-THE-NON-CANCELLING-INTERSECTIONS-CONJECTURE.pdf).
  Theorem 3 uses a join tree with non-cancelling separators. Acyclic-family
  winnability is therefore not claimed new. Our base may lack a join tree,
  and its attachment face may acquire coefficient zero. The new target is
  a cancellation-aware, facewise optimal compiler with exact coefficient
  and cost formulas. That paper's introductory open-status statement
  predates Wilhelm's later refutation and is not current status evidence.

Bounded searches for simplex attachments, optimal toggle words, and
nonpure shelling cancellation did not locate this exact closure theorem.
This is search-relative evidence, not proof of historical priority.

The proof remains unformalized and independent review is pending.
There is no assertion about arbitrary lattices, arbitrary nonpure
shellings, deletion of attachments, or attachments sharing new vertices.
