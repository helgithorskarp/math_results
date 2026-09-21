# Sources, attribution and claim boundary

Checked 21 September 2026.

1. Illya Ivanov, *Illuminating Primitive Polytopes*,
   [arXiv:2607.08944](https://arxiv.org/abs/2607.08944),
   [version 1 full text](https://arxiv.org/html/2607.08944v1).
   Section 1.3 defines primitive polytopes by unboundedness after facet
   deletion. Conjecture 6 in Section 1.4 proposes the vertex bound and its
   equality characterization. These are the exact targets refuted here.
   The current submission history lists only v1, submitted 9 July 2026.
   The paper's Theorem 2 concerns illumination and is not contradicted by
   a large vertex count. Its illumination proof is not an input here.

2. Francisco Santos, *A counterexample to the Hirsch conjecture*,
   [arXiv:1006.2814](https://arxiv.org/abs/1006.2814),
   [full text](https://arxiv.org/html/1006.2814), Section 2.1.
   This gives the classical one-point suspension and its face description,
   with references to older sources. By polarity this is the facet wedge:
   vertices on the chosen facet remain single, and other vertices double.
   The repeated-wedge operation and this counting rule are established
   constructions, not innovations claimed in the present note.

3. The official [polymake wedge documentation](https://polymake.org/release_docs/3.4/polytope.html)
   gives a direct polytope construction and a square-to-triangular-prism
   example. It corroborates terminology only. The checker neither imports
   polymake nor relies on its output.

The particular inequality family can be obtained from a polygon by wedging
each of its noncoordinate facets once. The proof is self-contained so that
checking the counterexample requires no software package or wedge convention.

Focused searches for the paper's title, its Conjecture 6, primitive
polytope vertex bounds, positive bases and facet wedges did not locate
the same refutation. They do not establish historical priority for the
construction or the count. Terminology is especially important here:
primitive lattice polytopes, primitive zonotopes defined by lattice
generators, and primitive fixing systems are different notions.

The graph-first starting point was the existing Hadwiger--Boltyanski
illumination problem. Its circuit, cactus, two-hub and reciprocal torus
covering results are not used or generalized here. This is a separate
vertex-count obstruction found in current primary literature attached
to that subject.

No claim is made about the smallest possible counterexample dimension,
the maximum vertex count at a fixed dimension, or the illumination number
of the examples. No independent peer review or proof-assistant
formalization is included.
