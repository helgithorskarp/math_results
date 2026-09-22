# Source alignment and priority boundary

Primary papers and an author-hosted survey inspected on 2026-09-22. This is a
proved structural theorem with an ordinary proof and exact auxiliary code;
it is not a claim of established publication priority.

- **[STG]** Anton Savostianov, Francesco Tudisco, Nicola Guglielmi,
  *Cholesky-like Preconditioner for Hodge Laplacians via Heavy Collapsible
  Subcomplex*, 2024, [author manuscript](https://arxiv.org/pdf/2401.15492).
  Definition 5.5 uses collapse to a graph; Algorithm 5.1 peels free edges;
  Algorithm 6.1 adds triangles in decreasing weight when collapse remains
  possible. The algorithm is prior art. Our narrow target is an exact
  optimality theorem for it under the hereditary edge bound, via a matroid
  characterization. We do not evaluate or improve its spectral preconditioner.

- **[CFH]** Armindo Costa, Michael Farber, Danijela Horak,
  *Fundamental groups of clique complexes of random graphs*, Transactions
  of the London Mathematical Society 2 (2015), 1--32,
  [author manuscript](https://arxiv.org/pdf/1312.1208).
  Equation (8) relates incidence excess, Euler characteristic and edge density;
  Lemmas 5.1 and 5.6--5.8 analyze closed complexes/minimal cycles. Corollary 5.9
  gives a wedge description under hereditary v/e>1/3 and credits Babson.
  We use the stronger additive bound e<=3v-6 to identify actual sphere
  circuits and all feasible retained sets. The Euler mechanism and broad
  sparse-complex homotopy route are established machinery.

- **[B]** Eric Babson, *Fundamental Groups of Random Clique Complexes*, 2012,
  [author manuscript](https://arxiv.org/pdf/1207.5028).
  Theorem 1.2 is the earlier sparse-complex wedge classification cited by
  [CFH]. We do not present a wedge-of-spheres/circles conclusion as an
  independent discovery without this antecedent.

- **[AB]** Karim Adiprasito, Bruno Benedetti, *Tight complexes in 3-space admit
  perfect discrete Morse functions*, European Journal of Combinatorics 45
  (2015), 71--84, [author manuscript](https://arxiv.org/pdf/1202.3390).
  Lemma 2.3 proves perfection for complexes embedded in the plane. Its
  definition excludes a triangulated sphere. A planar one-skeleton is a
  different hypothesis and can support several sphere cycles; (H) also
  allows nonplanar graphs. No new claim is made for their planar-complex lemma.

- **[CM]** Johannes Carmesin, Tsvetomir Mihaylov, *Outerspatial 2-complexes:
  Extending the class of outerplanar graphs to three dimensions*, Electronic
  Journal of Combinatorics 30(3) (2023), P3.20,
  [author manuscript](https://arxiv.org/pdf/2103.15404).
  Proposition 2.34 characterizes outerspatial simplicial 2-complexes by
  planar one-skeleta; Lemma 2.33 concerns nested triangles. This is relevant
  geometric context, not a new embedding theorem proved here.

- **[C]** William H. Cunningham, *Matching, Matroids, and Extensions*,
  author manuscript dated 2001-08-02,
  [author-hosted text](https://www.math.uwaterloo.ca/~whcunnin/atlan.pdf).
  Theorem 3.1 states maximum-weight matroid greedy, with attribution to
  Rado and Edmonds. That optimization mechanism is classical; our task is
  to prove that the collapse-feasible triangle sets form the requisite matroid.

The targeted searches included planar one-skeleton Morse functions, sparse
complex collapse, matroid collapse optimization, and heavy collapsible
subcomplexes. No inspected source explicitly states the combined
hereditary-edge-bound / sphere-circuit / exact weighted-collapse theorem.
This is a search-relative assessment, not proof that no earlier source does.
No claim is made to solve general Morse optimization, arbitrary collapsible
subcomplex optimization, or the Whitehead conjecture. The universal result
is proved in PROOF.md without assuming an unverified external algorithmic
or homological assertion from the comparison papers.
