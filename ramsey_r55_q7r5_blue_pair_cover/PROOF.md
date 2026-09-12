# Blue cross-matchings of size at most three in an original good43 task

Red denotes a graph edge. The original task is `bo1-q7-r5-c000004` in the complete h3887 maximal-packing registry. It remains UNKNOWN unless every retained complete physical unit below is refuted. No good43 or numerical Ramsey bound is established by a positive tail witness.

**Theorem.** In every model of this original task, the blue cross edges between its two prescribed blue K4 blocks form a matching of size at most three. This reduces the complete physical family to four full43 receiver types. The proof refutes all 93 matrix orbits outside this condition; all edges attaching the tail to the remaining twenty vertices are unrestricted. The retained labeled-matrix cover has 185 of the original 37,823 coordinate values.

Three retained types have literal tail witnesses. The zero-blue-edge tail relaxation remains undecided, and no inference is drawn from its unfinished solver trace. The theorem does not require deciding that relaxation.

## 1. Original physical meaning and the allowed relabelings

In this task, vertices 0..19 form five prescribed red K4 blocks, vertices 20..23 and 24..27 form two prescribed blue K4 blocks, and vertices 28..42 induce the literal 15-vertex core specified in CORE.json. The core is record 4 of the pinned McKay R(4,4;15) catalog. The h4001/h4011 table retains this original task; it is not one of the 518 accepted exclusions.

The induced tail on vertices 20..42 has no red K4, by red-packing maximality, and no blue K5, by the target. Relabel its core as 0..14 and its two blue blocks as U=15..18 and V=19..22. Every one of the 136 edges between these three parts is initially free.

Let M be the sixteen-bit red U-to-V matrix, with position (i,j) contributing bit 4i+j. Independently permuting U and V and optionally interchanging them acts by row permutations, column permutations and transpose. The group has order 2(4!)²=1152. It fixes every core vertex and transports every incident edge. Both blue blocks retain their internal color and the tail remains red-K4-free and blue-K5-free.

These operations need not preserve the original root-column ordering. We do not append a second competing ordering to the original formula. We use only the physical target and maximality clauses in the negative implication, and use a separate complete relabeling cover for the future full formulas.

## 2. A complete 97-class physical split

A five-set within U union V contains vertices from both blocks. It is blue exactly when all its cross entries in M are zero. Red K5s there are impossible because red cross edges form a bipartite graph. Literal testing of all sixteen-bit matrices leaves 37,823 allowed words.

The producer finds the orbits of these words by adjacent row swaps, adjacent column swaps and transpose. These generate the entire group. The independent checker instead evaluates every pair of full row/column permutations and both transpose choices at each reported representative. It checks the minimum representative, every orbit size, disjointness, and equality of the resulting union to the independently computed allowed-word set. There are exactly 97 orbits. This is a finite labeled-matrix classification, not a quotient by automorphisms of a hypothetical good43.

Consequently the 97 orbit conditions give a disjoint split of every original-task model. Matrices rejected before taking orbits already violate a physical K5 prohibition. Every member of an allowed orbit has an explicit permissible relabeling to its representative.

## 3. Complete exclusion of the forbidden geometry

For each representative, fix all 105 core edges, twelve internal blue-block edges, and sixteen U-to-V edges. The remaining 120 Boolean variables are exactly the core-to-U/V physical edges in lexicographic pair order. There are no auxiliary variables and no extra ordering constraints in these tail formulas.

For every four-set prohibit all six edges red. For every five-set prohibit all ten edges blue. Omit a clause only when an already fixed edge has the opposite color; otherwise substitute fixed edges and retain every free literal. The resulting CNF is equivalent to the complete tail problem for this representative. Red K5s in the tail are already excluded by red-K4-freeness.

EXPECTED.json records every one of the 97 physical classes: 93 have checked negative decisions, three have literal positive tail words, and one tail is explicitly undecided. Every negative is supported by a checked DRAT refutation of its exact CNF. Every positive tail word has 136 physical bits checked directly. The independent input auditor enumerates potential forbidden cliques through bitset intersections, whereas the producer tests vertex subsets. It reconstructs the actual clause stream and input digest. No interrupted solver run is treated as a decision.

A negative tail refutation excludes the **entire full43 physical subfamily** in that matrix orbit: any original-task model would restrict to a tail, and an allowed blue-block relabeling would give a model of the refuted CNF. All edges incident to the other twenty vertices remain unrestricted in this implication. A positive tail decision leaves its full43 subfamily UNKNOWN.

The four retained representatives are 31711, 31743, 32767 and 65535. Their blue cross edges are respectively matchings of sizes 3, 2, 1 and 0. Their orbit sizes are 96, 72, 16 and 1, summing to 185. The 93 refuted classes consist of all 92 nonmatching types and the blue perfect-matching type. This is a complete proof of the theorem's forbidden branch and an exhaustive physical subdivision with four retained full43 units. It is not an exact feasibility classification of all tail relaxations.

The physical ledger contains proved UNSAT subfamilies and explicitly retained UNKNOWN subfamilies. Neither a local SAT word nor the one undecided tail is promoted to a full physical decision.

## 4. Checked connection to original source and future joins

The map from tail labels to original labels is

    [28,...,42, 20,...,27].

For every representative, `bridge.py` checks all fixed edges and sixteen matrix units, then maps every actual tail clause to the pinned original h3873 physical clause after precisely those constant substitutions. Red four-clauses map into the required maximality region 20..42; blue five-clauses map into the global target. The ordered h3887 formula contains these physical clauses unchanged. The ordinary relabeling argument in Sections 1–3 is part of the trust boundary, not an assumption that the old ordering is invariant.

For each retained representative, the full receiver formula fixes the same core, the two blue blocks and their entire cross matrix, and all five red K4 blocks. It leaves every other edge free and includes every physical K5 prohibition and the entire tail red-K4 exclusion. The five red blocks alone are normalized by increasing core-adjacency signatures within each block and increasing complete core-signature words between blocks. Core vertices and the blue matrix remain fixed. Ties are allowed. These are genuine red-block vertex permutations, so every original-task model is represented in at least one of these full formulas. Every full model is directly a good43.

The suffix comparators have their usual prefix-equality semantics. No blue-block core-signature ordering is added after fixing the blue-pair matrix: arbitrary such permutations could change that matrix.

The executable join checks actual tail proof bytes and the original source mapping. A future full refutation is accepted only against the exact generated full input and an independently checked proof. Missing full proofs remain UNKNOWN. Only when all retained full units are refuted may the join output `CERTIFIED_ORIGINAL_TASK_UNSAT`. Metadata claiming UNSAT without a proof is never an admission certificate. A proof of one physical child never retires the original ID.

The original registry has 2,189,178 tasks, of which 518 are already excluded. The q10 physical ledger and its color redirects are separate. They are never added to the original exclusion count here.

## 5. An exact labeled-carrier consequence

In the original h3887 code for this one task, the U-to-V matrix is an independent coordinate with 37,823 values. The root-block sorting constraints use other coordinates. Therefore if W is the sum of the orbit sizes of retained representatives, the present proof leaves exactly a fraction W/37823 of this task's **bare labeled carrier** as a sufficient retained cover. This follows directly from its product indexing; no unrelated reduction percentages are multiplied. The retained codes can still violate other constraints and are not counted good43 graphs.

COUNTS.json gives the exact integer consequence from the pinned original per-task count. No whole original task is subtracted while W is positive and its full physical units are undecided.

## 6. A uniform check on the red perfect-matching branch

There is a short certificate for one complete type, independent of the particular core. Here it is the **red** U-to-V graph that is a perfect matching, not the blue matchings in the main theorem. Let its pairs be P1,...,P4, and suppose the remaining core has no monochromatic K4.

Each core vertex must be red-adjacent to both ends of some Pi. Otherwise choose one blue neighbor in each pair. The four chosen vertices form a blue K4, since the only red edges among U union V are the matched pairs; together with the core vertex they form a blue K5.

For a fixed pair Pi, its common red neighbors in the core contain no red edge, since that edge and Pi would form a red K4 in the tail. Those common neighbors form a blue clique and therefore number at most three. The four such sets cover the core, giving core order at most 4·3=12. A core of order 15 is impossible.

This excludes the entire matching orbit for every q7,r5 core, including all 122 retained original tasks. It excludes a physical subfamily in each, not the whole task. The inequality needs no disjointness of the covering sets. `controls.py` exhausts all 256 single-vertex contact words against the matching graph. This is an elementary pigeonhole application; no historical priority is asserted.

## 7. Evidence and limits

The complete physical cut uses CaDiCaL300 in python-sat 1.9.dev15, with every negative checked by the separately built drat-trim version pinned in TOOLS.json. The large proof corpus and input files stay outside Git; manifests and reproduction source preserve their identities and regenerate the entire proved cut. Replay does not attempt the undecided zero-blue-edge tail, because its feasibility is not a premise. A fresh valid proof need not have the original byte digest.

The compact checker audits the complete orbit cover, encodings and positive tails; it expressly does not re-establish negative results without their actual proof bytes. The full verifier and join require those bytes. Source publication is not an independent mathematical review.

Individual exclusions depend on a literal core and finite proof verification. Catalog completeness is imported for the global carrier theorem, not for deciding this one fixed-core subfamily. Trust also includes the ordinary relabeling and restriction proofs, exact code, DRAT soundness, compiler/interpreter/runtime, SHA-256, OS and hardware. The historical order-five automorphism claim, unfinished solver traces, q8 cohort-0 gate and Eulerian family are not premises.
