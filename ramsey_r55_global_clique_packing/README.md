# An unconditional clique-packing cover for good43

Every hypothetical 43-vertex graph containing neither a clique nor an independent set of size five has a vertex labeling in this **60-branch family**. After exact restrictions on each pair of blocks and normalization relative to one red 4-clique, the family contains **M < 2^787** labeled physical graphs. The unrestricted space has 2^903 graphs, so this is an existential search reduction by a factor greater than 2^116. No cut-rank bound, graph automorphism, parent graph, or fixed neighborhood is assumed.

This does not count good43 graphs. The retained family still contains forbidden five-sets meeting three or more blocks; no branch is solved and no Ramsey bound is improved. All 60 documented physical fixtures fail the target. The result is a complete global cover, an exact candidate-family count, and a reversible search interface.

The decomposition is elementary: pack five red 4-cliques using R(4,5)=25, two further monochromatic 4-cliques using R(4,4)=18, and four monochromatic triangles using R(3,3)=6. Three vertices remain. Their four isomorphism types, the three possible counts of red 4-cliques, and the five possible counts of red forced triangles give 4·3·5=60 branches.

Each branch has 12 vertex blocks, 57 fixed internal edges, and 66 independently chosen cross matrices containing the other 846 physical edges. A matrix is allowed exactly when its two blocks together contain no monochromatic five-set. Sorting each child block by its adjacency signatures to the first red 4-clique preserves target coverage and further reduces the family. For a mixed last triple, only its two interchangeable vertices are sorted. The combined restrictions reduce the packing baseline of 60·2^846 labeled graphs by a factor greater than 2^65. The exact integer M and every branch count are in [COUNTS.json](COUNTS.json); the count follows from a product of genuinely disjoint edge-coordinate domains, without an independence approximation.

`index_family.py` bijects the integer interval `[0,M)` with this retained physical family. It supports deterministic search ranges, exact reconstruction, and sampling. The full target encoder additionally enforces **every** one of the 962,598 five-sets. Read [PROOF.md](PROOF.md), [EXACT_COUNTS.md](EXACT_COUNTS.md), and [HANDOFF.md](HANDOFF.md).

Reproduce from the repository root using Python 3.11 standard library:

```bash
python3 -B ramsey_r55_global_clique_packing/reproduce.py
python3 -O -B ramsey_r55_global_clique_packing/reproduce.py
```

Expected status: `VERIFIED_UNCONDITIONAL_GLOBAL_PACKING_HANDOFF`. Both runs regenerate the domains and counts, independently check every domain entry and the child-automorphism orbit representatives, test the physical interface, and reconstruct every clause in six representative full43 formulas. No SAT solver, external catalog, compiler, network connection, or private artifact is needed. Generated CNFs live in a temporary directory and are removed after each check. See [VALIDATION.md](VALIDATION.md) for exact evidence and trust boundaries.

This reduction uses a new vertex labeling, so its cardinality is not a fraction of the previously retained rank-four or rank-five graphs. Those interfaces remain separate. In particular, their internal distance restrictions must not be discarded when reusing their counts. The global family here covers every potential good43, including any that have no rank-four cut.
