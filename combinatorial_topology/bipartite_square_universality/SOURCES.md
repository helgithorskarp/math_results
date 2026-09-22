# Sources and scope of the increment

Primary-source comparison performed 2026-09-22. This is a construction and
sphere-relation theorem, not a claim to resolve a named classical open
conjecture. Negative searches support only novelty relative to the sources
inspected, not historical priority.

## Established inputs

1. Kazuhiro Kawamura, **A variant of the bipartite relation theorem and its
   application to clique graphs**, Contributions to Discrete Mathematics
   6(2) (2011), 91–100.
   [Publisher PDF](https://cdm.ucalgary.ca/article/download/62059/46707/177343),
   [DOI](https://doi.org/10.55016/ojs/cdm.v6i2.62059).
   Observation 2.1 supplies the square/half-square decomposition;
   Theorem 2.5 gives the Dowker bridge collapses. Proposition 3.2 and
   Theorem 3.3 supply prior relative-homology comparisons. The entire
   ten-page paper was inspected. These abstract mechanisms are prior art.

2. F. Larrión, M. A. Pizaña and R. Villarroel-Flores,
   **The fundamental group of the clique graph**, European Journal of
   Combinatorics 30 (2009), 288–294.
   [Author manuscript](https://xamanek.izt.uam.mx/map/papers/Fundame06w.pdf).
   Theorem 3.1 already gives fundamental-group agreement between a
   bipartite square complex and its two half-square complexes. Our
   simply connected examples are consistent with this general result;
   general fundamental-group agreement is not an increment here.

3. Michał Adamaszek, **Clique complexes and graph powers**.
   [Author preprint](https://arxiv.org/abs/1104.0433),
   [PDF](https://arxiv.org/pdf/1104.0433).
   Proposition 2.2 is the established high-girth collapse theorem, and
   Theorem 5.1 gives `Cl(T(G)) ~= Cl(G) wedge t(G)S2`. Subdivision graphs
   are C4-free and bipartite, so this already proves universality up to
   S2 wedges and arbitrary torsion for that unrestricted class. Those
   consequences must not be attributed to this package. The isolated
   hexagon's square as an octahedral sphere is also already discussed.
   Our additional restrictions and generator relations are described below.

4. Allen Hatcher, **Algebraic Topology**.
   [Author book](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf),
   [Chapter 2](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf).
   We use standard CW cofiber and null-attaching-map facts, suspension
   homology, Hurewicz, and Theorem 2C.5 (a finite CW complex has a finite
   simplicial homotopy model). Barycentric subdivision being flag and
   the finite Moore-space constructions are standard topology.

## Committed graph predecessors

- **Essential hexagonal spheres and exact asphericity for C4-free bipartite
  graph squares**, graph artifact
  `bafkreihv6ayensehg5px7yvyg5tmsvgtpy37vhyf6mwci77hr7rqmmbjke`, height 5500.
  [Source](https://github.com/helgithorskarp/math_results/tree/main/combinatorial_topology/bipartite_square_hexagon).
  Its integral cycle detector already proves that each actual hexagonal
  sphere is primitive and has infinite order. Its graph-like bridge and
  primitivity are reused, with their arguments recalled in PROOF.md.
- The accepted review,
  `bafkreia2hfb4n6q2lc6ts2cn73idlzuipvrw62np6bttcw2wxva2us2m34`, height 5502,
  [review](https://github.com/helgithorskarp/math_results/blob/main/combinatorial_topology/bipartite_square_hexagon_review1/REVIEW.md),
  explicitly leaves the distinction between graph six-cycle relations
  and relations among sphere classes as a structural continuation.
  It accepted the predecessor, not this package.
- The separate total-graph equivariant refinement,
  `bafkreia2so7iwwg6qzolle3cqglyia5poqo3lelm4zpij7v7htom4vrlpu`, height 5364,
  is prior graph context. We do not restate its ordinary total-graph
  decomposition as a new theorem or claim an equivariant wedge splitting.

## Proposed increment and search limits

The proposed contribution is the explicit linear-size C4-free bipartite
construction with one cone half-square, its full homotopy type
`(Cl(G)/G) wedge (2m-n)S2`, and its complete natural integral presentation on
actual hexagonal sphere generators. This realizes all finite simply
connected simplicial homotopy types after adjoining specified S2 wedges
with the additional property that hexagonal spheres generate all H2.
Consequently arbitrary finite torsion occurs inside that sphere subgroup,
although its displayed generators are individually primitive. For ordinary
total graphs, the relative-chain formula shows their hexagonal classes are
independent, so the already-known torsion is outside the hexagon subgroup.
The relative-chain argument also describes sphere relations as an intersection of two integer boundary
images for a general C4-free bipartite graph; the homological tools used to
obtain it are established, not new machinery.

The K4 fan-only obstruction and stored order-two certificate are concrete
consequences, not separate claims of minimality or optimized size. The
six-vertex base triangulation is not claimed to be a new complex.

Bounded live searches combined “C4-free”, “bipartite graph square”, “clique
complex”, “homotopy”, “universality”, and “torsion”; the primary papers above
and the relevant committed graph neighborhoods were compared. No matching
construction/presentation was found. This does not exclude other unpublished,
poorly indexed, or differently phrased prior results. No blanket first
universality theorem for graph complexes is claimed.
