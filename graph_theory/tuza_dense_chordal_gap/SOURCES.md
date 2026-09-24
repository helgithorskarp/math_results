# Sources, dependencies, and novelty scope

The structural contribution is to combine the zero/unit-weight framework
for fractional triangle covers with perfect elimination, giving a strict
quadratic gap in every fixed-density chordal class. Its integer consequence
uses established fractional-packing approximation. None of those classical
inputs is claimed as new.

1. Michael Krivelevich, *On a conjecture of Tuza about packing and covering
   of triangles*, Discrete Mathematics 142 (1995), 281--286.
   [Author-hosted paper](https://www.math.tau.ac.il/~krivelev/2.pdf).
   Input: `tau(H)<=2nu*(H)` for every finite simple graph, including graphs
   obtained by deleting edges from a chordal graph.

2. Penny E. Haxell and Vojtech Rodl, *Integer and fractional packings in
   dense graphs*, Combinatorica 21 (2001), 13--38. The uniform approximation
   `nu*_H(G)-nu_H(G)=o(|V(G)|^2)` for each fixed packed graph `H` is the
   rounding input. A simpler proof and extension are in Raphael Yuster,
   *Integer and fractional packing of families of graphs*, Random
   Structures & Algorithms 26 (2005), 110--118:
   [author's preprint](https://arxiv.org/abs/math/0305350).
   The triangle specialization is also stated as Theorem 2.1 in Peter
   Keevash and Benny Sudakov, *Packing triangles in a graph and its
   complement*, Journal of Graph Theory 47 (2004), 203--216:
   [author-hosted paper](https://people.maths.ox.ac.uk/keevash/papers/triangle-packing-journal.pdf).
   We use a fixed positive accuracy for each fixed density or type count.

3. Raphael Yuster, *Dense graphs with a large triangle cover have a large
   triangle packing*, Combinatorics, Probability and Computing 21 (2012),
   952--962. [Author-hosted paper](https://math.haifa.ac.il/raphy/papers/triangrich.pdf).
   Section 2 uses zero-weight and unit-weight edge sets, deletion of unit
   edges, and complementary slackness. These are the antecedents of
   Section 1 of the present proof. The present argument adds the
   elimination bound `|F0|<=n(1+sqrt(2|F1|))`, without assuming that the
   graph is hard to make triangle-free.

4. Luis Chahua and Juan Gutierrez, *On Tuza's conjecture in dense graphs*,
   Discrete Applied Mathematics 377 (2025), 225--233.
   [Author's preprint](https://arxiv.org/abs/2405.11409).
   An adjacent theorem settles split graphs of minimum degree at least
   `3n/5`. The present theorem uses arbitrary fixed positive edge density
   and sufficiently large order, with no minimum-degree condition.

5. Marthe Bonamy et al., *Tuza's conjecture for threshold graphs*, DMTCS
   24:1 (2022), no. 24.
   [Published open paper](https://dmtcs.episciences.org/9916/pdf).
   This settles threshold graphs at every order. It also distinguishes
   the general asymptotic `tau<=2nu+o(n^2)` statement from full Tuza.

6. Fabio Botler, Cristina G. Fernandes, and Juan Gutierrez,
   *On Tuza's conjecture for triangulations and graphs with small
   treewidth*, Discrete Mathematics 344 (2021), 112281.
   [Author's preprint](https://arxiv.org/abs/2002.07925).
   Their treewidth theorem implies Tuza for `K8`-free chordal graphs;
   this is a different restriction from positive density at large order.

The target was selected from the committed Tuza graph frontier, not from
an external problem search. Relevant durable work in this repository:

* [All-order two-type theorem](../tuza_two_type_complete/README.md), graph
  h5673, `bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`.
  The present bounded-type corollary reuses its general multiplicity-cap
  lemma, with the complete argument repeated here.
* [Independent review](../tuza_two_type_complete_review1/README.md), h5683,
  `bafkreica2wfmycetu7czymbrqofnluglaf3oiomkhbcsnwkhxnjyvmpyra`.
* [Three-type C5 cover structure](../tuza_three_type_c5_core/README.md),
  h5685, `bafkreibn2ff62v4czjnzqlt3huaauspidswmtarid6up6m74rvy4npiium`.
* [All-order co-sunflower subclass](../tuza_three_type_cosunflower/README.md),
  h5703, `bafkreihjynqkf2kkbn2i37w5gtiewx5jb74fkuzodhhlbag72xo2jsscky`.
  The latter two motivated the unrestricted packing bridge; neither is a
  logical prerequisite for the chordal theorem proved here.
  Its [independent review](../tuza_three_type_cosunflower_review1/README.md),
  h5707, `bafkreiexmuwvxoq3mlahoxav6m2simarq35tahd7rzdnfncvzafwjrwj24`,
  accepts that earlier theorem with high confidence. That review does not
  evaluate the present contribution.

Bounded primary-source searches through 2026-09-24 did not locate the
stated elimination-based gap or its every-fixed-density chordal
consequence. This is a novelty assessment within the searched sources,
not a historical priority claim. The constants are deliberately
unoptimized. The main gain is the graph class and the strict eventual
integer inequality, not an improved numerical constant.
