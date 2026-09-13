# Dependencies, primary literature, and scope

The only target-specific input to using the Hamilton normalization as a
complete-class receiver is R3's
[fault-Hamiltonicity proof](../ramsey_r55_fault_hamiltonicity/PROOF.md),
published in source commit `d551705a71fdec28f2aca65f39608201f4fc79c6`.
Its full proof and dependency manifest were read. It imports the
independently accepted maximal-connectivity theorem for both colors of
every good43, the degree bound from `R(4,5)<=25`, and the classical
Chvatal--Erdos Hamiltonicity theorem. This application needs only a
Hamilton cycle, not the stronger fault-tolerance conclusions.

The accepted connectivity source and review were inspected:

- [Source proof](../ramsey_r55_maximal_vertex_connectivity/PROOF.md):
  `kappa(G)=delta(G)` in each color. Its exact separator and marked-graph
  proof inherits the imported `R(4,5)<=25` boundary.
- [Accepting review](../ramsey_r55_maximal_vertex_connectivity_review1/REVIEW.md):
  an independent structural re-derivation, complete finite replay and
  additional exact checks; no formalization of the full theorem is claimed.

Their hashes, and the receiver's expected-output hash, are pinned in
[DEPENDENCIES.json](DEPENDENCIES.json). The width theorem for the
*specified literal formula* is purely combinatorial and does not depend
on Ramsey existence or any catalogue. The target-specific imports are
needed only for its complete-class interpretation.

The methodological sources consulted on 13 September 2026 were:

- R. Dechter, [Bucket elimination: A unifying framework for reasoning](https://ics.uci.edu/~dechter/publications/r76A.pdf),
  Artificial Intelligence 113 (1999), 41–85. The proposed route used the
  connection between exact elimination and induced width, including the
  distinction between elimination and conditioning.
- M. Samer and S. Szeider, [Algorithms for Propositional Model Counting](https://www.ac.tuwien.ac.at/files/pub/SamerSzeider10.pdf).
  The distinction between primal and incidence decompositions motivated
  checking both graphs, rather than assuming the primal clique alone
  excludes a small incidence decomposition.
- V. Angeltveit and B. D. McKay,
  [R(5,5) <= 46](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029),
  for the current certified Ramsey frontier. Nothing here changes it.

The two width facts, the Hall injection, and the local-gadget contraction
argument are proved directly in this package. No historical-priority
claim is made for these encoding observations.

The current repository and committed Discovery Net neighborhood were
checked at pass start and before publication. The committed graph remained
at indexed height 4363, with 2,207 contributions and 10,837 relations.
No new committed reviews or objections appeared. Searches included
treewidth, incidence graphs, clique subdivision and elimination; no matching
R(5,5) package was found. The most recent full principal report remained
`20260912T224126.355942Z.md`, which requires an approach change and a final
endpoint gate for this lane.

R1's core-exchange receiver can redirect between original carrier IDs and
cannot be added as an implicate of a fixed old task. It was read but is not
used. R3's source-certified `392..511` edge interval was inspected but is
not a constraint of this computation. Their dependencies and review
boundaries therefore remain separate. No original-task bridge or
retirement is asserted here.

All 15 prior accepted pending graph transactions and their exact identifiers
remain preserved without resubmission. This failed endpoint pass adds no
Discovery Net mathematical claim.
