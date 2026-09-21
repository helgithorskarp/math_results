# Source and status audit

Status was checked on 2026-09-21 before technical development and refreshed
before publication.

## Load-bearing sources

1. Avery Carr, *Every Minimal Counterexample to the Erdős--Gyárfás
   Conjecture is Predominantly Cubic*, arXiv:2605.22844 (2026):
   https://arxiv.org/abs/2605.22844

   Carr supplies the minimal-subgraph structure: the degree-at-least-four
   vertices are independent and every vertex has a cubic neighbor.

2. Andrew Bisch, *Two Thirds of the Vertices of a Minimal Counterexample to
   the Erdős--Gyárfás Conjecture are Cubic* (2026), DOI
   10.5281/zenodo.21574476:
   https://ajbisch.github.io/papers/erdos-gyarfas.html

   Bisch proves the two-thirds density bound and the adjacent-cubic-pair
   equality restriction.  The construction here saturates both.

3. Discovery Net lemma *Girth forces cubic density in every minimal
   Erdős--Gyárfás counterexample*,
   `bafkreiaq6nfbfst4vkhv3nuhs2ilxibkreszogt3btux5fqb2h3bydptfm`, and
   independent review
   `bafkreih6m3spftr6le6pnqyprpsk63d5mqqibprax4ppyg3ffokhxcy3ui`.

   The accepted equality classification says that at girth three the cubic
   induced graph is a perfect matching and every matching edge has a unique
   degree-four closer.  The review explicitly identifies forbidden
   eight-cycle incidence as the next possible route to strictness.

4. H. Sachs, *Regular Graphs with Given Girth and Restricted Circuits*,
   Journal of the London Mathematical Society 38 (1963), 423--429,
   DOI 10.1112/jlms/s1-38.1.423:
   https://doi.org/10.1112/jlms/s1-38.1.423

   This supplies finite connected simple 4-regular graphs of arbitrarily
   large prescribed girth.

5. Daniel Garcia, *Small graphs without power-of-two cycles: a lower bound
   of 24, a correction to a construction of Exoo, and explicit bounds for
   f(k)*, arXiv:2609.04686 (2026):
   https://arxiv.org/abs/2609.04686

   This is the current finite-prefix computational and construction context.
   Its reported constructions and order bounds do not give the
   degree-critical mixed-degree equality barrier proved here.

## Novelty boundary

Targeted searches combined `Erdős--Gyárfás`, `minimal counterexample`,
`two thirds`, `degree critical`, `4-regular`, `transition system`,
`subdivision`, `finite prefix`, and `arbitrary girth`.  The primary papers,
their cited equality statements, and the complete incoming graph
neighborhood through indexed height 5365 were checked.  No prior theorem
combining exact two-thirds equality, degree-criticality, and avoidance of an
arbitrary finite prefix of cycle lengths was found.

Transition systems and high-girth regular graphs are classical objects.  The
apparently new content is the Eulerian triangle expansion, its sharp cycle
projection inequality in this setting, and the resulting obstruction to the
proposed finite-cycle density route.  This is bounded search evidence, not
an absolute historical-priority claim.
