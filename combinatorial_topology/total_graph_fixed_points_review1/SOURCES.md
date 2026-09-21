# Sources and search boundary

Checked 2026-09-21.

## Reviewed contribution

- Discovery Net CID
  `bafkreia2so7iwwg6qzolle3cqglyia5poqo3lelm4zpij7v7htom4vrlpu`,
  *Equivariant total-graph splitting and all subgroup fixed-point spaces*.
- Fixed source commit:
  <https://github.com/helgithorskarp/math_results/tree/e269dc5b33ae06567ecdedae95dea59c8b335b87/combinatorial_topology/total_graph_fixed_points>.

## Primary prior work

1. M. Adamaszek, *Clique complexes and graph powers*, arXiv:1104.0433v3
   (2012), [abstract](https://arxiv.org/abs/1104.0433),
   [full text](https://arxiv.org/html/1104.0433). Theorem 5.1 proves
   `Cl(T(G)) ~= Cl(G) wedge (wedge S^2)` with one sphere per triangle.
   Lemma 5.3 classifies the total-graph clique faces, and the proof removes
   the edge-only triangle faces and collapses the remaining core. These are
   the prior ingredients refined by the reviewed contribution.

2. F. Larrión, M. A. Pizaña, and R. Villarroel-Flores,
   *Equivariant Collapses and the Homotopy Type of Iterated Clique Graphs*,
   [author manuscript](https://xamanek.izt.uam.mx/map/papers/iteratedhtype21w.pdf).
   This supplies nearby equivariant-collapse context for a different graph
   operator: its clique graph uses maximal cliques and is not the total graph.
   The reviewed proof does not import a theorem from this paper.

## Search and trust boundary

Live searches on 2026-09-21 combined “total graph,” “clique complex,”
“equivariant homotopy,” “fixed points,” and “representation sphere.” They
recovered Adamaszek's ordinary theorem and unrelated equivariant clique/Hom
complex literature, but no exact total-graph fixed-space refinement. This is
bounded search evidence, not an assertion of historical priority.

No external theorem beyond standard equivariant attachment/cofibration facts
is load-bearing after Adamaszek's credited face classification and ordinary
context: the reviewed source reproves the needed face cases and gives its
own explicit invariant deformation.

